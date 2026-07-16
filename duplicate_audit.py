#!/usr/bin/env python3
"""
Comprehensive duplicate audit of 851 agent failure patterns.
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import hashlib

def normalize_name(name):
    """Normalize pattern names for comparison."""
    return name.lower().strip().replace('_', ' ').replace('-', ' ')

def extract_pattern_metadata(filepath):
    """Extract metadata from a pattern file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    # Extract pattern name from filename
    filename = os.path.basename(filepath)
    pattern_name = filename.replace('.md', '').replace('-', ' ').title()

    # Extract Issue section
    issue_match = re.search(r'## Issue:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
    issue = issue_match.group(1).strip()[:200] if issue_match else ""

    # Extract Root Cause section
    root_match = re.search(r'## Root Cause:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
    root_cause = root_match.group(1).strip()[:200] if root_match else ""

    # Extract Examples section
    example_match = re.search(r'## Example:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
    examples = example_match.group(1).strip()[:300] if example_match else ""

    # Extract Mitigation section
    miti_match = re.search(r'## Mitigation:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
    mitigation = miti_match.group(1).strip()[:300] if miti_match else ""

    # Get category path
    rel_path = filepath.replace(os.sep, '/')
    parts = rel_path.split('/')
    category = parts[1] if len(parts) > 1 else 'unknown'
    subcategory = parts[2] if len(parts) > 2 else 'unknown'
    goal = parts[4] if len(parts) > 4 else 'unknown'

    return {
        'name': pattern_name,
        'filename': filename,
        'filepath': filepath,
        'category': category,
        'subcategory': subcategory,
        'goal': goal,
        'issue': issue,
        'root_cause': root_cause,
        'examples': examples,
        'mitigation': mitigation,
        'content': content,
    }

def similarity_score(str1, str2):
    """Calculate similarity between two strings."""
    if not str1 or not str2:
        return 0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_duplicate_groups(patterns):
    """Find duplicate groups using multiple signals."""
    groups = defaultdict(list)
    used = set()

    for i, p1 in enumerate(patterns):
        if i in used:
            continue

        group = [i]
        used.add(i)

        for j in range(i + 1, len(patterns)):
            if j in used:
                continue

            p2 = patterns[j]

            # Signal 1: Exact name match
            name_match = normalize_name(p1['name']) == normalize_name(p2['name'])

            # Signal 2: Similar filename (edit distance)
            name_sim = similarity_score(p1['filename'], p2['filename'])

            # Signal 3: Same root cause keywords (80%+ overlap)
            root_sim = similarity_score(p1['root_cause'], p2['root_cause'])

            # Signal 4: Similar examples
            example_sim = similarity_score(p1['examples'], p2['examples'])

            # Signal 5: Similar mitigation
            miti_sim = similarity_score(p1['mitigation'], p2['mitigation'])

            # Signal 6: Same issue description
            issue_sim = similarity_score(p1['issue'], p2['issue'])

            # Decide if duplicate based on weighted signals
            is_duplicate = False
            signals_triggered = []

            if name_match:
                is_duplicate = True
                signals_triggered.append('exact_name')
            elif name_sim > 0.85:
                is_duplicate = True
                signals_triggered.append(f'name_sim_{name_sim:.2f}')
            elif root_sim > 0.75 and (example_sim > 0.6 or miti_sim > 0.6):
                is_duplicate = True
                signals_triggered.append(f'root_cause_{root_sim:.2f}')
            elif example_sim > 0.80:
                is_duplicate = True
                signals_triggered.append(f'examples_{example_sim:.2f}')
            elif miti_sim > 0.80 and root_sim > 0.6:
                is_duplicate = True
                signals_triggered.append(f'mitigation_{miti_sim:.2f}')
            elif issue_sim > 0.85:
                is_duplicate = True
                signals_triggered.append(f'issue_{issue_sim:.2f}')

            if is_duplicate:
                group.append(j)
                used.add(j)
                print(f"Duplicate found: {p1['filename']} <-> {p2['filename']}")
                print(f"  Signals: {', '.join(signals_triggered)}")

        if len(group) > 1:
            key = f"Group_{len(groups)}"
            groups[key] = group

    return groups

def analyze_duplicate_group(patterns, group_indices):
    """Analyze a group of duplicate patterns."""
    group_patterns = [patterns[i] for i in group_indices]

    # Find canonical (most complete)
    canonical_idx = max(group_indices, key=lambda i: len(patterns[i]['content']))
    canonical = patterns[canonical_idx]

    # Analyze root causes
    root_causes = [p['root_cause'] for p in group_patterns if p['root_cause']]
    examples = [p['examples'] for p in group_patterns if p['examples']]
    mitigations = [p['mitigation'] for p in group_patterns if p['mitigation']]

    return {
        'patterns': group_patterns,
        'canonical': canonical,
        'canonical_idx': canonical_idx,
        'root_causes': root_causes,
        'examples': examples,
        'mitigations': mitigations,
        'size': len(group_indices),
    }

def main():
    """Main analysis."""
    agents_dir = Path('./agents')
    pattern_files = sorted(agents_dir.glob('**/failures/*.md'))

    print(f"Found {len(pattern_files)} patterns")

    # Extract metadata
    patterns = []
    for filepath in pattern_files:
        rel_path = str(filepath).replace('\\', '/')
        metadata = extract_pattern_metadata(str(filepath))
        if metadata:
            patterns.append(metadata)

    print(f"Successfully parsed {len(patterns)} patterns")

    # Find duplicates
    print("\nFinding duplicates...")
    duplicate_groups = find_duplicate_groups(patterns)

    print(f"\nFound {len(duplicate_groups)} duplicate groups")

    # Analyze each group
    group_analyses = []
    for group_key, group_indices in duplicate_groups.items():
        analysis = analyze_duplicate_group(patterns, group_indices)
        group_analyses.append(analysis)

    # Sort by size
    group_analyses.sort(key=lambda x: x['size'], reverse=True)

    # Generate report
    report = generate_report(patterns, group_analyses)

    # Save report
    with open('DUPLICATE_AUDIT_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\nReport saved to DUPLICATE_AUDIT_PLAN.md")

def generate_report(patterns, group_analyses):
    """Generate comprehensive report."""
    report = []

    # Executive Summary
    total_affected = sum(g['size'] for g in group_analyses)
    avg_group_size = total_affected / len(group_analyses) if group_analyses else 0

    report.append("# Duplicate Audit Plan: 851 Agent Failure Patterns\n")
    report.append("## Executive Summary\n")
    report.append(f"- **Total Patterns**: 851\n")
    report.append(f"- **Duplicate Groups Found**: {len(group_analyses)}\n")
    report.append(f"- **Patterns Affected**: {total_affected}\n")
    report.append(f"- **Average Group Size**: {avg_group_size:.1f}\n")

    recommended_deletions = sum(g['size'] - 1 for g in group_analyses)
    report.append(f"- **Recommended Deletions**: {recommended_deletions}\n")
    report.append(f"- **Estimated Net Reduction**: {recommended_deletions} patterns ({100*recommended_deletions/851:.1f}%)\n")

    # Category breakdown
    report.append("\n## Duplicate Groups by Category\n")

    category_groups = defaultdict(list)
    for analysis in group_analyses:
        category = analysis['canonical']['category']
        category_groups[category].append(analysis)

    for category in sorted(category_groups.keys()):
        groups = category_groups[category]
        total_in_category = sum(g['size'] for g in groups)
        report.append(f"\n### {category}\n")
        report.append(f"- Groups: {len(groups)}\n")
        report.append(f"- Patterns affected: {total_in_category}\n")
        report.append(f"- Deletions: {sum(g['size'] - 1 for g in groups)}\n")

    # Top duplicate groups
    report.append("\n## Largest Duplicate Groups\n")

    for i, analysis in enumerate(group_analyses[:20]):
        canonical = analysis['canonical']
        size = analysis['size']

        report.append(f"\n### Group {i+1}: {canonical['filename']} ({size} patterns)\n")
        report.append(f"**Category**: {canonical['category']} > {canonical['goal']}\n\n")
        report.append("**Duplicate Instances**:\n")

        for pattern in analysis['patterns']:
            report.append(f"- `{pattern['filepath']}`\n")

        report.append(f"\n**Root Cause**: {canonical['root_cause'][:150]}...\n\n")
        report.append(f"**Recommendation**: MERGE → Keep canonical, delete {size-1} instances\n")

    report.append("\n## Implementation Checklist\n")
    report.append("- [ ] Review top 20 duplicate groups\n")
    report.append("- [ ] Identify domain-specific variants to preserve\n")
    report.append("- [ ] Create consolidated patterns in primary locations\n")
    report.append("- [ ] Update cross-references and links\n")
    report.append("- [ ] Delete secondary/duplicate patterns\n")
    report.append("- [ ] Recategorize miscategorized patterns\n")
    report.append("- [ ] Update README pattern counts\n")
    report.append("- [ ] Verify no broken links\n")

    return '\n'.join(report)

if __name__ == '__main__':
    main()
