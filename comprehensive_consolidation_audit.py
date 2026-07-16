#!/usr/bin/env python3
"""
Comprehensive consolidation audit combining:
1. Exact name duplicates
2. Cross-category patterns
3. Semantic variants of known candidates
4. Miscategorized patterns
"""

import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def similarity(s1, s2):
    if not s1 or not s2:
        return 0
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def extract_content(filepath):
    """Extract key sections from pattern."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return None

    issue_match = re.search(r'## Issue:?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.DOTALL)
    issue = issue_match.group(1).strip() if issue_match else ""

    root_match = re.search(r'## (?:Root Cause|Root Cause Theory):?\s*\n(.*?)(?:\n\n|\n##|\Z)', content, re.IGNORECASE | re.DOTALL)
    root = root_match.group(1).strip() if root_match else ""

    return {'issue': issue[:400], 'root': root[:400], 'full': content}

def load_all_patterns():
    """Load all 851 patterns."""
    patterns = []
    for filepath in sorted(Path('./agents').glob('**/failures/*.md')):
        filename = filepath.name
        content_data = extract_content(str(filepath))
        if content_data:
            parts = filepath.parts
            patterns.append({
                'filename': filename,
                'filepath': str(filepath),
                'category': parts[1] if len(parts) > 1 else 'unknown',
                'goal': parts[4] if len(parts) > 4 else 'unknown',
                'content': content_data,
            })
    return patterns

def group_by_similarity(patterns, threshold=0.50):
    """Group patterns by semantic similarity."""
    groups = []
    used = set()

    for i, p1 in enumerate(patterns):
        if i in used:
            continue

        group = [i]
        used.add(i)

        p1_issue = p1['content']['issue']
        p1_root = p1['content']['root']

        if not p1_issue and not p1_root:
            continue

        for j in range(i + 1, len(patterns)):
            if j in used:
                continue

            p2 = patterns[j]
            p2_issue = p2['content']['issue']
            p2_root = p2['content']['root']

            if not p2_issue and not p2_root:
                continue

            # Calculate similarity
            issue_sim = similarity(p1_issue, p2_issue) if (p1_issue and p2_issue) else 0
            root_sim = similarity(p1_root, p2_root) if (p1_root and p2_root) else 0

            # High threshold groups
            if (root_sim > 0.70 and issue_sim > 0.40) or (root_sim > 0.80):
                group.append(j)
                used.add(j)

        if len(group) > 1:
            groups.append({
                'indices': group,
                'patterns': [patterns[idx] for idx in group],
                'size': len(group),
                'avg_root_sim': root_sim if len(group) > 1 else 0,
            })

        used.add(i)

    return groups

def main():
    print("Loading all patterns...")
    patterns = load_all_patterns()
    print(f"Loaded {len(patterns)} patterns\n")

    # Find similarity groups
    print("Finding semantic similarity groups (high threshold)...")
    sim_groups = group_by_similarity(patterns, threshold=0.50)
    print(f"Found {len(sim_groups)} semantic groups\n")

    # Find exact name duplicates
    print("Finding exact name duplicates...")
    by_name = defaultdict(list)
    for i, p in enumerate(patterns):
        by_name[p['filename'].lower()].append(i)

    exact_dupes = [by_name[name] for name in by_name if len(by_name[name]) > 1]
    print(f"Found {len(exact_dupes)} exact duplicate groups\n")

    # Find cross-category patterns
    print("Finding cross-category duplicates...")
    by_norm_name = defaultdict(list)
    for i, p in enumerate(patterns):
        norm_name = p['filename'].replace('-', ' ').lower()
        by_norm_name[norm_name].append(i)

    cross_dupes = []
    for name, indices in by_norm_name.items():
        if len(indices) > 1:
            cats = set(patterns[i]['category'] for i in indices)
            if len(cats) > 1:
                cross_dupes.append(indices)

    print(f"Found {len(cross_dupes)} cross-category patterns\n")

    # Generate comprehensive report
    report = generate_report(patterns, sim_groups, exact_dupes, cross_dupes)

    with open('DUPLICATE_AUDIT_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("Report saved to DUPLICATE_AUDIT_PLAN.md")
    print("\n=== Summary ===")
    print(f"Semantic groups: {len(sim_groups)}")
    print(f"Exact duplicates: {len(exact_dupes)}")
    print(f"Cross-category: {len(cross_dupes)}")

    all_groups = sim_groups + [{'patterns': [patterns[i] for i in idx], 'indices': idx, 'size': len(idx)} for idx in exact_dupes + cross_dupes]
    affected = set()
    for group in all_groups:
        for p in group['patterns']:
            affected.add(p['filepath'])

    deletions = sum(max(0, g['size']-1) for g in all_groups)
    print(f"Total affected patterns: {len(affected)}")
    print(f"Recommended deletions: {deletions}")
    print(f"Estimated reduction: {100*deletions/len(patterns):.1f}%")

def generate_report(patterns, sim_groups, exact_dupes, cross_dupes):
    """Generate comprehensive report."""
    lines = []

    lines.append("# Comprehensive Duplicate Audit: 851 Agent Failure Patterns\n\n")

    all_groups = sim_groups + [{'patterns': [patterns[i] for i in idx], 'size': len(idx), 'type': 'exact'} for idx in exact_dupes + cross_dupes]
    affected = set()
    for group in all_groups:
        for p in group['patterns']:
            affected.add(p['filepath'])

    deletions = sum(max(0, g['size']-1) for g in all_groups)

    lines.append("## Executive Summary\n\n")
    lines.append(f"- **Total Patterns**: 851\n")
    lines.append(f"- **Exact Name Duplicates**: {len(exact_dupes)} groups\n")
    lines.append(f"- **Cross-Category Duplicates**: {len(cross_dupes)} groups\n")
    lines.append(f"- **Semantic Similarity Groups**: {len(sim_groups)} groups\n")
    lines.append(f"- **Total Duplicate Groups**: {len(all_groups)}\n")
    lines.append(f"- **Patterns Affected**: {len(affected)}\n")
    lines.append(f"- **Recommended Deletions**: {deletions}\n")
    lines.append(f"- **Estimated Reduction**: {100*deletions/851:.1f}%\n\n")

    # Sort and display top groups
    sorted_groups = sorted(all_groups, key=lambda g: g['size'], reverse=True)

    lines.append("## Largest Duplicate Groups\n\n")

    for i, group in enumerate(sorted_groups[:50]):
        if not group['patterns']:
            continue

        primary = group['patterns'][0]
        lines.append(f"### Group {i+1}: {primary['filename']} ({group['size']} instances)\n\n")
        lines.append(f"**Category**: {primary['category']}\n\n")
        lines.append(f"**Locations**:\n")

        for p in group['patterns']:
            lines.append(f"- `{p['filepath']}`\n")

        lines.append(f"\n**Recommendation**: CONSOLIDATE → Delete {group['size']-1} secondary instances\n\n")

    lines.append("## Implementation Checklist\n\n")
    lines.append("- [ ] Review all duplicate groups\n")
    lines.append("- [ ] Identify canonical versions\n")
    lines.append("- [ ] Create consolidated patterns\n")
    lines.append("- [ ] Update cross-references\n")
    lines.append("- [ ] Delete secondary patterns\n")
    lines.append("- [ ] Update README counts\n")
    lines.append("- [ ] Verify links\n")

    return ''.join(lines)

if __name__ == '__main__':
    main()
