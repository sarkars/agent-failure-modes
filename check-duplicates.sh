#!/bin/bash

# Deduplication Checker for Agent Failure Patterns
# Usage: ./check-duplicates.sh "pattern-title" "root-cause-keywords"
# Example: ./check-duplicates.sh "tool selection hallucination" "tool selection confidence"

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
AGENTS_DIR="$REPO_ROOT/agents"

if [ $# -lt 1 ]; then
    echo "❌ Usage: $0 \"pattern-name\" [\"root-cause-keywords\"]"
    echo ""
    echo "Examples:"
    echo "  $0 \"tool selection hallucination\""
    echo "  $0 \"tool selection hallucination\" \"confidence mechanism\""
    exit 1
fi

PATTERN_NAME="$1"
ROOT_CAUSE_KEYWORDS="${2:-$1}"

echo "🔍 Deduplication Check for: '$PATTERN_NAME'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Layer 1: Check for exact pattern name matches
echo "📋 Layer 1: Exact Name Match"
NAME_MATCHES=$(grep -r "^# $PATTERN_NAME$" "$AGENTS_DIR" --include="*.md" 2>/dev/null | wc -l)
if [ "$NAME_MATCHES" -gt 0 ]; then
    echo "⚠️  FOUND: $NAME_MATCHES existing pattern(s) with exact title match"
    grep -r "^# $PATTERN_NAME$" "$AGENTS_DIR" --include="*.md" 2>/dev/null | cut -d: -f1
    echo ""
else
    echo "✅ No exact name matches found"
    echo ""
fi

# Layer 2: Check for similar pattern names
echo "📋 Layer 2: Similar Pattern Names"
PATTERN_WORDS=$(echo "$PATTERN_NAME" | tr ' ' '\|')
SIMILAR=$(grep -r "^# .*\($PATTERN_WORDS\)" "$AGENTS_DIR" --include="*.md" 2>/dev/null | wc -l)
if [ "$SIMILAR" -gt 1 ]; then
    echo "⚠️  FOUND: $SIMILAR patterns with similar keywords"
    grep -r "^# .*\($PATTERN_WORDS\)" "$AGENTS_DIR" --include="*.md" 2>/dev/null | head -10
    echo ""
else
    echo "✅ No significantly similar pattern names found"
    echo ""
fi

# Layer 3: Check for root cause overlaps
echo "📋 Layer 3: Root Cause Mechanism Check"
RC_KEYWORDS=$(echo "$ROOT_CAUSE_KEYWORDS" | tr ' ' '\|')
RC_MATCHES=$(grep -r "Root Cause" "$AGENTS_DIR" -A 3 --include="*.md" 2>/dev/null | grep -i "$RC_KEYWORDS" | wc -l)
if [ "$RC_MATCHES" -gt 0 ]; then
    echo "⚠️  FOUND: $RC_MATCHES patterns with overlapping root cause keywords"
    grep -r "Root Cause" "$AGENTS_DIR" -A 3 --include="*.md" 2>/dev/null | grep -B 1 -i "$RC_KEYWORDS" | head -20
    echo ""
else
    echo "✅ No root cause overlaps detected"
    echo ""
fi

# Layer 4: Check for symptom overlaps
echo "📋 Layer 4: Symptom Overlap Check"
SYMPTOM_KEYWORDS=$(echo "$PATTERN_NAME" | cut -d' ' -f1-2)
SYMPTOM_MATCHES=$(grep -r "## Symptoms" "$AGENTS_DIR" -A 10 --include="*.md" 2>/dev/null | grep -i "$SYMPTOM_KEYWORDS" | wc -l)
if [ "$SYMPTOM_MATCHES" -gt 0 ]; then
    echo "⚠️  FOUND: $SYMPTOM_MATCHES patterns with similar symptoms"
    grep -r "## Symptoms" "$AGENTS_DIR" -A 10 --include="*.md" 2>/dev/null | grep -B 2 -i "$SYMPTOM_KEYWORDS" | head -20
    echo ""
else
    echo "✅ No significant symptom overlaps detected"
    echo ""
fi

# Summary & Recommendation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary:"
TOTAL_CONCERNS=$((NAME_MATCHES + SIMILAR - 1 + RC_MATCHES + SYMPTOM_MATCHES))
if [ "$TOTAL_CONCERNS" -eq 0 ]; then
    echo "✅ GREEN: Low duplication risk. Proceed with new pattern."
    exit 0
elif [ "$TOTAL_CONCERNS" -le 2 ]; then
    echo "🟡 YELLOW: Some overlap detected. Review similar patterns before authoring."
    echo "   Action: Check if this should consolidate to existing pattern"
    exit 1
else
    echo "🔴 RED: High duplication risk. Check existing patterns carefully."
    echo "   Action: This pattern may already exist or overlap significantly"
    exit 2
fi
