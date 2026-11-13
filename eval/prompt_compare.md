# KrishiYojana – Prompt Comparison and Evaluation

## 1. Objective

Compare two prompt versions for the KrishiYojana agricultural scheme assistant using 10 farmer questions and the same scheme dataset.

## 2. Evaluation Setup

| Item | Details |
|---|---|
| LLM Provider | Groq |
| Model | Configured Groq model |
| Dataset | 19 scheme records |
| Evaluation Questions | 10 |
| Prompt Versions | Version 1 and Version 2 |
| Total Generated Responses | 20 |

## 3. Prompt Versions

### Version 1 – Basic Prompt

- Identifies relevant government schemes.
- Explains benefits, eligibility and documents when available.
- Uses simple English.
- Includes basic instructions against making up information.

### Version 2 – Improved Prompt

- Uses only the available scheme information.
- Explicitly handles unavailable information.
- Prevents unsupported claims about subsidies, deadlines and eligibility.
- Avoids guaranteeing scheme approval.
- Encourages relevant follow-up questions.
- Uses structured and clear responses.

## 4. Evaluation Questions

The evaluation uses the 10 questions documented in `docs/user_questions.md`.

## 5. Evaluation Execution

The evaluation script `eval/run_prompt_eval.py` was executed successfully.

| Prompt Version | Questions Tested | Responses Generated |
|---|---:|---:|
| Version 1 | 10 | 10 |
| Version 2 | 10 | 10 |
| Total | 10 | 20 |

Results were saved in `eval/results.json`.

## 6. Evaluation Criteria

| Criteria | Description |
|---|---|
| Accuracy | Whether the response is supported by scheme records |
| Relevance | Whether it answers the farmer's question |
| Completeness | Whether available details are included |
| Clarity | Whether the answer is easy to understand |
| Missing Information Handling | Whether unavailable information is identified |
| Follow-up Questions | Whether useful additional information is requested |

## 7. Preliminary Observations

The generated responses demonstrate the following prompt-design differences:

- Version 1 provides general scheme information with basic instructions.
- Version 2 provides more explicit guidance about eligibility limitations and missing information.
- Version 2 encourages follow-up questions when additional farmer details are needed.

These are observations about the prompt instructions and generated examples. A complete accuracy comparison requires reviewing all 20 responses against the source records.

## 8. Limitations

- The quality of responses depends on the completeness and accuracy of the 19 scheme records.
- Scheme information and eligibility conditions should be checked against current official government guidelines.
- AI-generated answers may contain unsupported details.
- The model-generated confidence score is not a calibrated probability.
- The assistant does not provide official government eligibility approval.

## 9. Conclusion

Both prompt versions were tested against the same 10 farmer questions using 19 scheme records, generating 20 responses in total.

Version 2 includes stronger instructions for handling missing information, avoiding unsupported claims and asking follow-up questions. Further manual review is required before concluding that it performs better in factual accuracy.

## 10. Evaluation Files

- `prompts/eval_prompt_v1.txt`
- `prompts/eval_prompt_v2.txt`
- `eval/run_prompt_eval.py`
- `eval/results.json`
- `docs/user_questions.md`