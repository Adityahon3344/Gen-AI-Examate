# RAG Configuration Evaluation

| Metric | Config A (1000 / Top-3) | Config B (500 / Top-5) |
|---|---:|---:|
| Average keyword coverage | 0.6667 | 0.6667 |
| Citation rate | 0.7143 | 0.7143 |
| Correct abstentions | 1 | 1 |
| Successful generations | 15 | 15 |
| Generation errors | 0 | 0 |

## Evaluation notes

- Keyword coverage is an automatic retrieval proxy, not proof of factual correctness.
- Citation rate measures whether an answer contains a [Source] reference.
- Correct abstentions measure whether unanswerable questions received an 'I don't know' response.
- Manually verify answers against official scheme guidelines before claiming factual accuracy.

## Configuration settings

| Setting | Config A | Config B |
|---|---:|---:|
| Chunk size (words) | 1000 | 500 |
| Overlap (words) | 150 | 75 |
| Top-k | 3 | 5 |