#!/usr/bin/env python3
"""
Comprehensive duplicate audit of 851 agent failure patterns.
Uses multiple detection strategies to find all types of duplicates.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher, unified_diff

def normalize(text):
    """Normalize text for comparison."""
    return text.lower().strip().replace('_', '-').replace(' ', '-')

def similarity(str1, str2):
    """Calculate string similarity."""
    if not str1 or not str2:
        return 0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def extract_sections(content):
    """Extract all major sections from pattern file."""
    sections = {}
    section_names = ['Issue', 'Root Cause', 'Examples?', 'Mitigation', 'Prevention',
                     'Detection', 'Recovery', 'Related Patterns', 'See Also']

    for section in section_names:
        pattern = rf'##\s*{section}:?.*?\n(.*?)(?=##|\Z)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section.lower()] = match.group(1).strip()[:500]

    return sections

class PatternAnalyzer:
    def __init__(self):
        self.patterns = []
        self.by_name = defaultdict(list)
        self.by_normalized_name = defaultdict(list)
        self.duplicate_groups = []
        self.candidates = {}

    def load_patterns(self, agents_dir):
        """Load all 851 patterns."""
        pattern_files = sorted(Path(agents_dir).glob('**/failures/*.md'))

        for filepath in pattern_files:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract metadata
            filename = filepath.name
            pattern_name = filename.replace('.md', '')

            # Get category path
            parts = filepath.parts
            category_idx = parts.index('agents') if 'agents' in parts else -1
            if category_idx >= 0:
                category = parts[category_idx + 1] if len(parts) > category_idx + 1 else 'unknown'
                goal = parts[category_idx + 4] if len(parts) > category_idx + 4 else 'unknown'
            else:
                category = 'unknown'
                goal = 'unknown'

            sections = extract_sections(content)

            pattern = {
                'filename': filename,
                'pattern_name': pattern_name,
                'filepath': str(filepath),
                'category': category,
                'goal': goal,
                'content': content,
                'sections': sections,
            }

            self.patterns.append(pattern)
            self.by_name[pattern_name].append(pattern)
            self.by_normalized_name[normalize(pattern_name)].append(pattern)

    def find_exact_name_duplicates(self):
        """Find patterns with exact same name in different locations."""
        exact_dupes = []
        for name, patterns in self.by_name.items():
            if len(patterns) > 1:
                exact_dupes.append({
                    'type': 'exact_name',
                    'name': name,
                    'patterns': patterns,
                    'count': len(patterns),
                    'reason': f'Exact name match in {len(patterns)} locations'
                })
        return exact_dupes

    def find_domain_variants(self):
        """Find patterns that appear in both by-capability and by-use-case."""
        variants = []
        for norm_name, patterns in self.by_normalized_name.items():
            if len(patterns) < 2:
                continue

            categories = set(p['category'] for p in patterns)
            if len(categories) > 1:  # Same pattern in multiple categories
                # Check if one is by-capability and others are by-use-case
                by_cap = [p for p in patterns if p['category'] == 'by-capability']
                by_use = [p for p in patterns if p['category'] == 'by-use-case']
                cross_cut = [p for p in patterns if p['category'] == 'cross-cutting']

                if (by_cap and by_use) or (by_cap and cross_cut) or (by_use and cross_cut):
                    variants.append({
                        'type': 'domain_variant',
                        'normalized_name': norm_name,
                        'patterns': patterns,
                        'locations': list(categories),
                        'count': len(patterns),
                        'reason': f'Cross-cutting pattern in {len(categories)} category branches'
                    })
        return variants

    def find_semantic_duplicates(self, threshold=0.80):
        """Find patterns with similar content/root cause."""
        semantic_dupes = []
        checked = set()

        for i, p1 in enumerate(self.patterns):
            if i in checked:
                continue

            group = [i]
            root1 = p1['sections'].get('root cause', '')
            issue1 = p1['sections'].get('issue', '')

            if not root1 and not issue1:
                continue

            for j in range(i + 1, len(self.patterns)):
                if j in checked:
                    continue

                p2 = self.patterns[j]
                root2 = p2['sections'].get('root cause', '')
                issue2 = p2['sections'].get('issue', '')

                if not root2 and not issue2:
                    continue

                # Check similarity
                root_sim = similarity(root1, root2) if (root1 and root2) else 0
                issue_sim = similarity(issue1, issue2) if (issue1 and issue2) else 0

                if root_sim > threshold or issue_sim > threshold:
                    group.append(j)
                    checked.add(j)

            if len(group) > 1:
                group_patterns = [self.patterns[idx] for idx in group]
                semantic_dupes.append({
                    'type': 'semantic_duplicate',
                    'patterns': group_patterns,
                    'count': len(group),
                    'primary_sim': max([similarity(group_patterns[0]['sections'].get('root cause', ''),
                                                   p['sections'].get('root cause', ''))
                                       for p in group_patterns[1:]] or [0]),
                    'reason': f'Similar root cause/issue ({threshold*100:.0f}% threshold)'
                })

            checked.add(i)

        return semantic_dupes

    def find_known_candidates(self):
        """Find and analyze known consolidation candidates."""
        candidates = {
            'agent-defaults-to-stale-training-knowledge-over-live-lookup-tool': [],
            'self-verification-cannot-catch-upstream-errors': [],
            'long-session-context-loss-violates-earlier-constraints': [],
            'hallucinated-completion-when-upstream-dependency-fails': [],
            'semantic-similarity-retrieval-misses-structural-attributes': [],
            'handoff-schema-loses-upstream-confidence-signal': [],
        }

        for pattern in self.patterns:
            name = pattern['pattern_name']
            for candidate in candidates:
                if normalize(candidate) == normalize(name):
                    # Found exact match - look for variants
                    candidates[candidate].append(pattern)
                elif candidate in name.lower() or name.lower() in candidate.lower():
                    # Found related pattern
                    candidates[candidate].append(pattern)

        return {k: v for k, v in candidates.items() if v}

    def analyze(self):
        """Run comprehensive analysis."""
        print("Starting comprehensive duplicate audit...")
        print(f"Total patterns loaded: {len(self.patterns)}")

        # Strategy 1: Exact name duplicates
        print("\nStrategy 1: Finding exact name duplicates...")
        exact = self.find_exact_name_duplicates()
        print(f"Found {len(exact)} exact name duplicate groups")

        # Strategy 2: Domain variants
        print("\nStrategy 2: Finding domain variants...")
        variants = self.find_domain_variants()
        print(f"Found {len(variants)} domain variant groups")

        # Strategy 3: Semantic duplicates
        print("\nStrategy 3: Finding semantic duplicates (this may take a moment)...")
        semantic = self.find_semantic_duplicates(threshold=0.75)
        print(f"Found {len(semantic)} semantic duplicate groups")

        # Strategy 4: Known candidates
        print("\nStrategy 4: Finding known consolidation candidates...")
        known = self.find_known_candidates()
        print(f"Found {len(known)} known candidates with variants")

        self.duplicate_groups = exact + variants + semantic

        return {
            'exact_duplicates': exact,
            'domain_variants': variants,
            'semantic_duplicates': semantic,
            'known_candidates': known,
            'all_groups': self.duplicate_groups
        }

def format_report(analysis_result):
    """Generate comprehensive markdown report."""
    lines = []

    lines.append("# Comprehensive Duplicate Audit Plan: 851 Agent Failure Patterns\n")

    # Executive Summary
    lines.append("## Executive Summary\n")
    lines.append(f"- **Total Patterns**: 851\n")

    all_groups = analysis_result['all_groups']
    all_affected = set()
    for group in all_groups:
        for p in group['patterns']:
            all_affected.add(p['filepath'])

    lines.append(f"- **Duplicate Groups Found**: {len(all_groups)}\n")
    lines.append(f"- **Patterns Affected**: {len(all_affected)}\n")
    lines.append(f"- **Known Candidates with Variants**: {len(analysis_result['known_candidates'])}\n")

    recommended_deletions = sum(max(0, g['count'] - 1) for g in all_groups)
    lines.append(f"- **Recommended Deletions**: {recommended_deletions}\n")
    lines.append(f"- **Estimated Reduction**: {recommended_deletions} patterns ({100*recommended_deletions/851:.1f}%)\n")

    # Known Candidates
    if analysis_result['known_candidates']:
        lines.append("\n## Known Consolidation Candidates\n")
        for name, patterns in analysis_result['known_candidates'].items():
            lines.append(f"\n### {name}\n")
            lines.append(f"- **Variants Found**: {len(patterns)}\n")
            lines.append("- **Locations**:\n")
            for p in patterns[:10]:
                lines.append(f"  - `{p['filepath']}`\n")
            if len(patterns) > 10:
                lines.append(f"  - ... and {len(patterns)-10} more\n")

    # Exact Duplicates
    if analysis_result['exact_duplicates']:
        lines.append("\n## Exact Name Duplicates\n")
        lines.append(f"**Found {len(analysis_result['exact_duplicates'])} groups**\n\n")

        for i, group in enumerate(analysis_result['exact_duplicates'][:15]):
            lines.append(f"### {i+1}. {group['name']} ({group['count']} instances)\n")
            lines.append(f"**Locations**:\n")
            for p in group['patterns']:
                lines.append(f"- `{p['filepath']}`\n")
            lines.append(f"\n**Recommendation**: MERGE → Keep primary, delete {group['count']-1}\n\n")

    # Domain Variants
    if analysis_result['domain_variants']:
        lines.append("\n## Cross-Category Duplicates (Domain Variants)\n")
        lines.append(f"**Found {len(analysis_result['domain_variants'])} groups**\n\n")

        for i, group in enumerate(analysis_result['domain_variants'][:15]):
            lines.append(f"### {i+1}. {group['normalized_name']} ({group['count']} instances)\n")
            lines.append(f"**Categories**: {', '.join(group['locations'])}\n")
            lines.append(f"**Locations**:\n")
            for p in group['patterns']:
                lines.append(f"- `{p['filepath']}`\n")
            lines.append(f"\n**Recommendation**: CONSOLIDATE → Move to by-capability, update cross-references\n\n")

    # Implementation Plan
    lines.append("\n## Implementation Checklist\n")
    lines.append("- [ ] Review all 26+ duplicate groups\n")
    lines.append("- [ ] Identify domain-specific variants worth preserving\n")
    lines.append("- [ ] Create canonical versions in by-capability\n")
    lines.append("- [ ] Update all cross-references\n")
    lines.append("- [ ] Delete secondary instances\n")
    lines.append("- [ ] Verify domain-use-case specific context\n")
    lines.append("- [ ] Update README counts\n")
    lines.append("- [ ] Test links and references\n")

    return '\n'.join(lines)

def main():
    analyzer = PatternAnalyzer()
    analyzer.load_patterns('./agents')
    result = analyzer.analyze()

    report = format_report(result)

    with open('DUPLICATE_AUDIT_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\nReport saved to DUPLICATE_AUDIT_PLAN.md")
    print(f"\nSummary:")
    print(f"- Exact duplicates: {len(result['exact_duplicates'])}")
    print(f"- Domain variants: {len(result['domain_variants'])}")
    print(f"- Semantic duplicates: {len(result['semantic_duplicates'])}")
    print(f"- Known candidates: {len(result['known_candidates'])}")

if __name__ == '__main__':
    main()
