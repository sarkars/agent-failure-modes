# Goal: Accurate Text Extraction

Text extraction accuracy is the foundation of any OCR agent. Even small errors can cascade into significant problems in downstream processing.

## Business Context

- Invoice amounts extracted incorrectly cause payment errors
- ID verification failures block legitimate users
- Form data errors require manual correction

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Character Confusion](failures/character-confusion.md) | Very Common | High |
| [Punctuation Errors](failures/punctuation-errors.md) | Common | High |
| [Font and Style Handling](failures/font-handling.md) | Occasional | Medium |
| [Handwritten Text](failures/handwritten-text.md) | Common | High |
| [Low Resolution](failures/low-resolution.md) | Very Common | High |
| [Skew and Rotation](failures/skew-rotation.md) | Common | Medium |
| [Background Interference](failures/background-interference.md) | Common | Medium |
| [Stamps and Overlays](failures/stamps-overlays.md) | Occasional | Medium |

## Key Metrics

- Character Error Rate (CER)
- Word Error Rate (WER)
- Field-level accuracy
