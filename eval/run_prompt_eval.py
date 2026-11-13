
import sys
import json
from pathlib import Path

# Add project root to Python import path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.records import load_json_records
from app.smart_search import smart_search
from app.llm import generate_response

PROMPTS_DIR = BASE_DIR / "prompts"
QUESTIONS_FILE = BASE_DIR / "docs" / "user_questions.md"
RESULTS_FILE = BASE_DIR / "eval" / "results.json"


def load_prompt(filename):
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8")


def load_questions():
    """Load questions written in Markdown format (**Q1.** Question)."""
    content = QUESTIONS_FILE.read_text(encoding="utf-8")
    questions = []

    for line in content.splitlines():
        line = line.strip()

        if line.startswith("**Q") and "**" in line[2:]:
            question = line.split("**", 2)[2].strip()

            if question:
                questions.append(question)

    return questions


def build_context(question, records):
    results = smart_search(records, question, top_k=5)

    context = "\n\n".join(
        f"Scheme: {record.scheme_name}\n"
        f"Department: {record.department}\n"
        f"Benefits: {record.benefit}\n"
        f"Eligibility: {', '.join(record.eligibility)}\n"
        f"Documents: {', '.join(record.required_documents)}"
        for record in results
    )

    return context or "No matching scheme information was found."


def main():
    print("Starting KrishiYojana Prompt Evaluation...")

    try:
        records = load_json_records()
        questions = load_questions()
    except (OSError, ValueError) as error:
        print(f"Error loading project data: {error}")
        return

    if not records:
        print("Error: No scheme records were loaded.")
        return

    if len(questions) != 10:
        print(f"Error: Expected 10 questions, but found {len(questions)}.")
        return

    print(f"Records loaded: {len(records)}")
    print(f"Questions loaded: {len(questions)}")

    prompt_versions = {
        "version_1": load_prompt("eval_prompt_v1.txt"),
        "version_2": load_prompt("eval_prompt_v2.txt")
    }

    evaluation_results = []

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {question}")

        context = build_context(question, records)

        for version, template in prompt_versions.items():
            prompt = template.format(
                question=question,
                context=context
            )

            try:
                answer = generate_response(
                    prompt,
                    "You are KrishiYojana, an agricultural scheme assistant."
                )
            except Exception as error:
                answer = f"ERROR: {error}"

            print(f"\n{version.upper()}:\n{answer}")

            evaluation_results.append({
                "question_number": number,
                "question": question,
                "prompt_version": version,
                "answer": answer
            })

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    RESULTS_FILE.write_text(
        json.dumps(
            evaluation_results,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\nEvaluation completed!")
    print(f"Total results: {len(evaluation_results)}")
    print(f"Results saved at: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
