#!/usr/bin/env python3
"""
Deep semantic analysis to find related patterns that should be consolidated.
Focuses on finding patterns with similar root causes, issue descriptions, and mitigation strategies.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def normalize(text):
    """Normalize text for comparison."""
    return text.lower().strip().replace('_', '-').replace(' ', '-')

def similarity(str1, str2):
    """Calculate string similarity (0-1)."""
    if not str1 or not str2:
        return 0
    s1 = str1.lower()
    s2 = str2.lower()
    return SequenceMatcher(None, s1, s2).ratio()

def extract_content(filepath):
    """Extract key content from pattern file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return None

    # Extract Issue section
    issue_match = re.search(r'## Issue:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
    issue = issue_match.group(1).strip() if issue_match else ""

    # Extract Root Cause section (may be capitalized differently)
    root_match = re.search(r'## (?:Root Cause|Root Cause Theory|Failure Mechanism):?\s*\n(.*?)(?:\n##|\Z)', content, re.IGNORECASE | re.DOTALL)
    root_cause = root_match.group(1).strip() if root_match else ""

    # Extract Examples section
    example_match = re.search(r'## Example:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    examples = example_match.group(1).strip() if example_match else ""

    # Extract Mitigation section
    miti_match = re.search(r'## Mitigation:?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    mitigation = miti_match.group(1).strip() if miti_match else ""

    # Extract Detection/Prevention
    detect_match = re.search(r'## (?:Detection|Prevention):?\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    detection = detect_match.group(1).strip() if detect_match else ""

    return {
        'issue': issue[:300],
        'root_cause': root_cause[:400],
        'examples': examples[:300],
        'mitigation': mitigation[:300],
        'detection': detection[:200],
        'full_content': content,
    }

def extract_keywords(text, max_keywords=10):
    """Extract meaningful keywords from text."""
    if not text:
        return []
    # Remove common words and extract meaningful terms
    common_words = {'the', 'a', 'an', 'and', 'or', 'is', 'are', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                    'should', 'may', 'might', 'must', 'can', 'in', 'on', 'at', 'to', 'for',
                    'from', 'of', 'with', 'by', 'as', 'when', 'where', 'what', 'which'}

    # Extract words
    words = re.findall(r'\b\w{4,}\b', text.lower())  # Words 4+ chars
    unique_words = set(w for w in words if w not in common_words)
    return sorted(list(unique_words))[:max_keywords]

def load_all_patterns():
    """Load all patterns with extracted content."""
    patterns = []
    agent_dir = Path('./agents')

    for filepath in sorted(agent_dir.glob('**/failures/*.md')):
        filename = filepath.name
        pattern_name = filename.replace('.md', '')

        # Get category path
        parts = filepath.parts
        cat_idx = parts.index('agents') if 'agents' in parts else -1
        if cat_idx >= 0:
            category = parts[cat_idx + 1] if len(parts) > cat_idx + 1 else 'unknown'
            goal = parts[cat_idx + 4] if len(parts) > cat_idx + 4 else 'unknown'
        else:
            category = goal = 'unknown'

        content_data = extract_content(str(filepath))
        if content_data:
            patterns.append({
                'filename': filename,
                'pattern_name': pattern_name,
                'filepath': str(filepath),
                'category': category,
                'goal': goal,
                'content': content_data,
                'keywords': extract_keywords(content_data['root_cause'] + ' ' + content_data['issue']),
            })

    return patterns

def find_semantic_clusters(patterns, threshold=0.65):
    """Find clusters of semantically similar patterns."""
    clusters = []
    used = set()

    for i, p1 in enumerate(patterns):
        if i in used:
            continue

        cluster = [i]
        used.add(i)

        # Use root cause + issue as primary comparison
        p1_primary = (p1['content']['root_cause'] + ' ' + p1['content']['issue'])

        if not p1_primary.strip():
            continue

        for j in range(i + 1, len(patterns)):
            if j in used:
                continue

            p2 = patterns[j]
            p2_primary = (p2['content']['root_cause'] + ' ' + p2['content']['issue'])

            if not p2_primary.strip():
                continue

            # Calculate similarity on multiple dimensions
            root_sim = similarity(p1['content']['root_cause'], p2['content']['root_cause'])
            issue_sim = similarity(p1['content']['issue'], p2['content']['issue'])
            miti_sim = similarity(p1['content']['mitigation'], p2['content']['mitigation'])
            detect_sim = similarity(p1['content']['detection'], p2['content']['detection'])

            # Keyword overlap
            keywords_p1 = set(p1['keywords'])
            keywords_p2 = set(p2['keywords'])
            if keywords_p1 and keywords_p2:
                keyword_overlap = len(keywords_p1 & keywords_p2) / len(keywords_p1 | keywords_p2)
            else:
                keyword_overlap = 0

            # Weighted similarity score
            score = (root_sim * 0.4 + issue_sim * 0.3 +
                    miti_sim * 0.15 + detect_sim * 0.05 + keyword_overlap * 0.1)

            if score >= threshold:
                cluster.append(j)
                used.add(j)

        if len(cluster) > 1:
            patterns_in_cluster = [patterns[idx] for idx in cluster]
            clusters.append({
                'indices': cluster,
                'patterns': patterns_in_cluster,
                'primary_pattern': patterns[i],
                'size': len(cluster),
                'avg_similarity': sum([
                    similarity(p1['content']['root_cause'], p['content']['root_cause'])
                    for p in patterns_in_cluster[1:]
                ]) / (len(cluster) - 1) if len(cluster) > 1 else 0,
            })

        used.add(i)

    return clusters

def analyze_known_consolidation_candidates():
    """Analyze the known large consolidation candidates."""
    print("\nAnalyzing known consolidation candidates...")
    candidates = {
        'stale-training-knowledge': [],
        'upstream-errors': [],
        'context-loss': [],
        'hallucinated-completion': [],
        'semantic-similarity-retrieval': [],
        'handoff-schema': [],
    }

    patterns = load_all_patterns()

    # For each pattern, check if it might be a variant
    for p in patterns:
        name = p['pattern_name'].lower()
        content = (p['content']['root_cause'] + ' ' + p['content']['issue']).lower()

        if 'stale' in name or 'stale' in content:
            candidates['stale-training-knowledge'].append(p)
        if 'verification' in name or 'upstream' in content or 'external' in content:
            candidates['upstream-errors'].append(p)
        if 'context' in name or 'session' in name or 'memory' in content:
            candidates['context-loss'].append(p)
        if 'hallucin' in name or 'fabricat' in name or 'hallucin' in content:
            candidates['hallucinated-completion'].append(p)
        if 'semantic' in name or 'retriev' in name or 'embedding' in name:
            candidates['semantic-similarity-retrieval'].append(p)
        if 'handoff' in name or 'handoff' in content or 'schema' in content:
            candidates['handoff-schema'].append(p)

    return {k: v for k, v in candidates.items() if v}

def main():
    print("Starting deep semantic audit...")

    # Load all patterns
    patterns = load_all_patterns()
    print(f"Loaded {len(patterns)} patterns")

    # Find semantic clusters
    print("\nFinding semantic clusters (this may take a moment)...")
    clusters = find_semantic_clusters(patterns, threshold=0.60)

    # Sort by size
    clusters.sort(key=lambda x: x['size'], reverse=True)

    print(f"Found {len(clusters)} semantic clusters")

    # Analyze known candidates
    candidates = analyze_known_consolidation_candidates()
    print(f"\nFound {len(candidates)} known consolidation candidate groups:")
    for name, group in candidates.items():
        print(f"  - {name}: {len(group)} related patterns")

    # Generate detailed report
    report = generate_detailed_report(patterns, clusters, candidates)

    with open('DUPLICATE_AUDIT_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\nDetailed report saved to DUPLICATE_AUDIT_PLAN.md")

def generate_detailed_report(patterns, clusters, candidates):
    """Generate comprehensive report."""
    lines = []

    lines.append("# Deep Semantic Duplicate Audit: 851 Agent Failure Patterns\n")

    lines.append("## Executive Summary\n")
    lines.append(f"- **Total Patterns**: 851\n")
    lines.append(f"- **Semantic Clusters Found**: {len(clusters)}\n")

    affected_patterns = set()
    for cluster in clusters:
        for p in cluster['patterns']:
            affected_patterns.add(p['filepath'])

    lines.append(f"- **Patterns in Clusters**: {len(affected_patterns)}\n")
    deletions = sum(c['size'] - 1 for c in clusters)
    lines.append(f"- **Recommended Deletions**: {deletions}\n")
    lines.append(f"- **Estimated Reduction**: {deletions} patterns ({100*deletions/851:.1f}%)\n")
    lines.append(f"- **Known Consolidation Candidates**: {len(candidates)}\n\n")

    # Largest clusters
    lines.append("## Largest Semantic Clusters (Top 30)\n\n")

    for i, cluster in enumerate(clusters[:30]):
        lines.append(f"### Cluster {i+1}: {cluster['primary_pattern']['pattern_name']} ({cluster['size']} patterns)\n")
        lines.append(f"**Primary Pattern**: `{cluster['primary_pattern']['filepath']}`\n\n")
        lines.append(f"**Root Cause**: {cluster['primary_pattern']['content']['root_cause'][:200]}...\n\n")
        lines.append(f"**Similar Patterns**:\n")

        for p in cluster['patterns'][1:]:
            lines.append(f"- `{p['filepath']}`\n")

        lines.append(f"\n**Recommendation**: CONSOLIDATE → Keep primary, merge/delete {cluster['size']-1} related patterns\n")
        lines.append(f"**Avg Similarity Score**: {cluster['avg_similarity']:.2f}\n\n")

    # Known candidates
    lines.append("\n## Known Consolidation Candidate Groups\n")
    lines.append("These are related patterns that should likely be consolidated:\n\n")

    for name, group in sorted(candidates.items(), key=lambda x: -len(x[1])):
        lines.append(f"### {name.replace('-', ' ').title()}\n")
        lines.append(f"**Related Patterns**: {len(group)}\n\n")

        for p in group[:10]:
            lines.append(f"- `{p['filepath']}`\n")

        if len(group) > 10:
            lines.append(f"- ... and {len(group)-10} more\n")

        lines.append("\n")

    # Implementation checklist
    lines.append("## Implementation Strategy\n\n")
    lines.append("### Phase 1: Review & Merge\n")
    lines.append("- [ ] Review all semantic clusters\n")
    lines.append("- [ ] Create consolidated patterns with references to domain variants\n")
    lines.append("- [ ] Document each consolidation decision\n")
    lines.append("- [ ] Identify domain-specific context to preserve\n\n")

    lines.append("### Phase 2: Reorganize\n")
    lines.append("- [ ] Move patterns to canonical locations (by-capability > cross-cutting)\n")
    lines.append("- [ ] Create cross-references from domain-specific locations\n")
    lines.append("- [ ] Update README with consolidated counts\n")
    lines.append("- [ ] Update PREVENTION_PROTOCOL documentation\n\n")

    lines.append("### Phase 3: Validate\n")
    lines.append("- [ ] Check all links and references\n")
    lines.append("- [ ] Verify no broken cross-references\n")
    lines.append("- [ ] Test pattern lookup by category\n")

    return ''.join(lines)

if __name__ == '__main__':
    main()
