#!/usr/bin/env python3
"""
Final comprehensive duplicate audit combining all analysis strategies.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def similarity(str1, str2):
    if not str1 or not str2:
        return 0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def load_patterns():
    """Load all patterns with metadata."""
    patterns = []
    for filepath in sorted(Path('./agents').glob('**/failures/*.md')):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            continue

        filename = filepath.name
        pattern_name = filename.replace('.md', '')

        # Extract metadata
        parts = filepath.parts
        cat_idx = parts.index('agents') if 'agents' in parts else -1
        category = parts[cat_idx + 1] if cat_idx >= 0 and len(parts) > cat_idx + 1 else 'unknown'
        goal = parts[cat_idx + 4] if cat_idx >= 0 and len(parts) > cat_idx + 4 else 'unknown'

        # Extract Issue
        issue_match = re.search(r'## Issue:?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.DOTALL)
        issue = issue_match.group(1).strip() if issue_match else ""

        # Extract Root Cause
        root_match = re.search(r'## (?:Root Cause|Root Cause Theory):?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.IGNORECASE | re.DOTALL)
        root = root_match.group(1).strip() if root_match else ""

        patterns.append({
            'filename': filename,
            'name': pattern_name,
            'path': str(filepath),
            'category': category,
            'goal': goal,
            'issue': issue[:200],
            'root': root[:300],
            'content': content,
        })

    return patterns

class DuplicateAudit:
    def __init__(self, patterns):
        self.patterns = patterns
        self.groups = []
        self.by_name = defaultdict(list)

        for p in patterns:
            self.by_name[p['name'].lower()].append(p)

    def find_all_groups(self):
        """Find all duplicate groups using multiple strategies."""
        exact_groups = self._find_exact_duplicates()
        cross_groups = self._find_cross_category_duplicates()
        return exact_groups + cross_groups

    def _find_exact_duplicates(self):
        """Find patterns with exact same filename in different locations."""
        groups = []
        for name, patterns in self.by_name.items():
            if len(patterns) > 1:
                groups.append({
                    'type': 'exact_name',
                    'name': name,
                    'patterns': patterns,
                    'canonical': patterns[0],
                    'secondaries': patterns[1:],
                })
        return groups

    def _find_cross_category_duplicates(self):
        """Find same pattern in multiple categories."""
        groups = []
        seen = set()

        for name, patterns in self.by_name.items():
            if len(patterns) < 2:
                continue

            categories = set(p['category'] for p in patterns)
            if len(categories) > 1 and name not in seen:
                groups.append({
                    'type': 'cross_category',
                    'name': name,
                    'patterns': patterns,
                    'categories': list(categories),
                    'canonical': patterns[0],  # Prefer by-capability
                    'secondaries': patterns[1:],
                })
                seen.add(name)

        return groups

def analyze_by_category(audit):
    """Analyze duplicate distribution by category."""
    by_cat = defaultdict(list)
    for group in audit.groups:
        for p in group['patterns']:
            by_cat[p['category']].append(group)

    return by_cat

def main():
    print("Loading patterns...")
    patterns = load_patterns()
    print(f"Loaded {len(patterns)} patterns\n")

    audit = DuplicateAudit(patterns)
    audit.groups = audit.find_all_groups()

    print(f"Found {len(audit.groups)} duplicate groups\n")

    # Analyze
    by_category = analyze_by_category(audit)

    # Count affected patterns
    affected = set()
    total_deletions = 0
    for group in audit.groups:
        for p in group['patterns']:
            affected.add(p['path'])
        total_deletions += len(group['secondaries'])

    # Generate comprehensive report
    report = generate_comprehensive_report(
        patterns, audit.groups, by_category, len(affected), total_deletions
    )

    with open('DUPLICATE_AUDIT_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Saved report to DUPLICATE_AUDIT_PLAN.md")

def generate_comprehensive_report(patterns, groups, by_category, affected_count, deletions):
    """Generate final comprehensive report."""
    lines = []

    lines.append("# Comprehensive Duplicate Audit Plan: 851 Agent Failure Patterns\n")
    lines.append("\n")

    # Executive Summary
    lines.append("## Executive Summary\n")
    lines.append(f"- **Total Patterns Analyzed**: 851\n")
    lines.append(f"- **Duplicate Groups Identified**: {len(groups)}\n")
    lines.append(f"- **Patterns Affected**: {affected_count}\n")
    lines.append(f"- **Recommended Deletions**: {deletions}\n")
    lines.append(f"- **Estimated Net Reduction**: {deletions} patterns ({100*deletions/851:.1f}%)\n")
    lines.append(f"- **After Consolidation**: ~{851-deletions} canonical patterns\n")
    lines.append("\n")

    # Category Breakdown
    lines.append("## Duplicate Distribution by Category\n")
    lines.append("\n")

    category_stats = defaultdict(lambda: {'groups': 0, 'affected': 0, 'deletions': 0})
    for group in groups:
        for p in group['patterns']:
            cat = p['category']
            if cat not in category_stats:
                category_stats[cat] = {'groups': 0, 'affected': 0, 'deletions': 0}
            category_stats[cat]['affected'] += 1

        # Count groups and deletions per category
        for cat in set(p['category'] for p in group['patterns']):
            category_stats[cat]['groups'] += 1
            category_stats[cat]['deletions'] += len(group['secondaries'])

    for cat in sorted(category_stats.keys()):
        stats = category_stats[cat]
        lines.append(f"### {cat}\n")
        lines.append(f"- Groups: {stats['groups']}\n")
        lines.append(f"- Affected patterns: {stats['affected']}\n")
        lines.append(f"- Recommended deletions: {stats['deletions']}\n")
        lines.append("\n")

    # All Duplicate Groups
    lines.append("## All Duplicate Groups (Sorted by Impact)\n")
    lines.append("\n")

    # Sort groups by size
    sorted_groups = sorted(groups, key=lambda g: len(g['patterns']), reverse=True)

    for i, group in enumerate(sorted_groups, 1):
        canonical = group['canonical']
        lines.append(f"### Group {i}: {group['name']} ({len(group['patterns'])} instances)\n")
        lines.append(f"**Type**: {group['type'].replace('_', ' ').title()}\n")
        lines.append(f"**Location**: {group['categories'] if 'categories' in group else canonical['category']}\n")
        lines.append(f"\n**Canonical Pattern**:\n")
        lines.append(f"- `{canonical['path']}`\n")
        lines.append(f"\n**Secondary/Duplicate Patterns** ({len(group['secondaries'])}):\n")

        for p in group['secondaries']:
            lines.append(f"- `{p['path']}`\n")

        lines.append(f"\n**Recommendation**: ")
        if group['type'] == 'cross_category':
            lines.append("CONSOLIDATE to by-capability, update references from domain-specific locations\n")
        else:
            lines.append("MERGE, keep canonical in primary location\n")

        lines.append(f"\n**Root Cause**: {canonical['root'][:100]}...\n")
        lines.append("\n")

    # Consolidation Strategy
    lines.append("\n## Consolidation Strategy\n")
    lines.append("\n### Phase 1: Exact Duplicate Resolution\n")
    lines.append("\nFor patterns with exact same name in different locations:\n")
    lines.append("1. Compare content completeness\n")
    lines.append("2. Keep version with most comprehensive examples and mitigations\n")
    lines.append("3. Delete duplicates\n")
    lines.append("4. Update README pattern count\n")
    lines.append("\n")

    lines.append("### Phase 2: Cross-Category Consolidation\n")
    lines.append("\nFor patterns appearing in multiple category branches:\n")
    lines.append("1. Create canonical version in by-capability (primary location)\n")
    lines.append("2. Keep domain-specific variants if they provide unique context\n")
    lines.append("3. Create cross-references from domain-specific locations\n")
    lines.append("4. Update category navigation\n")
    lines.append("\n")

    lines.append("### Phase 3: Verification\n")
    lines.append("1. Run pattern consistency checks\n")
    lines.append("2. Verify all cross-references\n")
    lines.append("3. Test README generation\n")
    lines.append("4. Validate category tree structure\n")
    lines.append("\n")

    # Implementation Checklist
    lines.append("## Implementation Checklist\n")
    lines.append("\n- [ ] Review all duplicate groups (priority: groups > 2 instances)\n")
    lines.append("- [ ] Identify which instances to keep as canonical\n")
    lines.append("- [ ] Create consolidated pattern versions\n")
    lines.append("- [ ] Update all cross-references and links\n")
    lines.append("- [ ] Delete secondary/duplicate files\n")
    lines.append("- [ ] Create reference/redirect patterns if needed for SEO/navigation\n")
    lines.append("- [ ] Update README.md with new pattern count\n")
    lines.append("- [ ] Update AUTHORSHIP_CHECKLIST.md\n")
    lines.append("- [ ] Verify git history is clean\n")
    lines.append("- [ ] Test README generation and navigation\n")
    lines.append("\n")

    # Impact Analysis
    lines.append("## Impact Analysis\n")
    lines.append("\n### Pattern Reduction by Category\n\n")
    lines.append("| Category | Before | Deletions | After | Reduction % |\n")
    lines.append("|----------|--------|-----------|-------|-------------|\n")

    for cat in sorted(category_stats.keys()):
        before = len([p for p in patterns if p['category'] == cat])
        after = before - category_stats[cat]['deletions']
        reduction = 100 * category_stats[cat]['deletions'] / before if before > 0 else 0
        lines.append(f"| {cat} | {before} | {category_stats[cat]['deletions']} | {after} | {reduction:.1f}% |\n")

    lines.append(f"\n**Total Before**: 851\n")
    lines.append(f"**Total After**: {851 - deletions}\n")
    lines.append(f"**Total Reduction**: {deletions} patterns ({100*deletions/851:.1f}%)\n")

    return ''.join(lines)

if __name__ == '__main__':
    main()
