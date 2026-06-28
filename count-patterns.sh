#!/bin/bash
cd "C:/Users/saura/Documents/Codex/2026-06-02/agent-failure-modes"
for d in healthcare legal-contracts devops devops-infrastructure supply-chain support-services customer-support financial-services hr-recruiting sales-crm content-marketing insurance; do
  count=$(find agents/by-use-case/$d -name "*.md" -path "*/failures/*.md" 2>/dev/null | wc -l)
  echo "$d: $count"
done
