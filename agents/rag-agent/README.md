# RAG Agent

RAG (Retrieval-Augmented Generation) Agents combine information retrieval with language generation to answer questions based on a knowledge base. They're used for document Q&A, knowledge management, enterprise search, and customer support.

## Goals

| Goal | Description | Failure Patterns |
|------|-------------|------------------|
| [Retrieval Quality](goals/retrieval-quality/) | Find relevant documents for user queries | 7 patterns |
| [Answer Synthesis](goals/answer-synthesis/) | Generate accurate answers from retrieved content | 7 patterns |
| [Citation Accuracy](goals/citation-accuracy/) | Correctly attribute information to sources | 6 patterns |
| [Query Understanding](goals/query-understanding/) | Interpret user questions correctly | 6 patterns |

## Structure

```
rag-agent/
├── README.md
└── goals/
    ├── retrieval-quality/
    │   ├── README.md
    │   └── failures/
    │       ├── semantic-mismatch.md
    │       ├── chunk-boundary.md
    │       └── ...
    ├── answer-synthesis/
    ├── citation-accuracy/
    └── query-understanding/
```

## Key Challenges

1. **Retrieval-Generation Gap**: Retrieved docs may not contain answer in usable form
2. **Chunk Boundaries**: Relevant information split across chunks
3. **Conflicting Sources**: Multiple documents with different information
4. **Hallucination Despite RAG**: Model generates beyond retrieved content
5. **Query-Document Mismatch**: User phrasing differs from document language
6. **Stale Knowledge**: Index contains outdated information
7. **Citation Grounding**: Ensuring claims are actually supported by cited sources

## Key Statistics (2026)

| Finding | Source |
|---------|--------|
| Legal RAG tools hallucinate 17-33% | Stanford Study |
| RAGAS fails on 83% of production cases | Benchmark Study |
| 52% of enterprise AI responses contain fabrications with ungoverned RAG | Enterprise Survey 2026 |
| RAG reduces hallucination by only 30-50% vs. baseline | Research Analysis |
| 70% of RAG failures are retrieval failures, not generation | Industry Analysis |

## Common Evaluation Metrics

- Retrieval precision and recall
- Answer correctness (vs. ground truth)
- Faithfulness (answer supported by sources)
- Citation precision (all citations valid)
- Answer relevance (addresses the question)
- Context utilization (uses retrieved content effectively)
