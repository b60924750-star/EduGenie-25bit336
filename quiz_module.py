import json
import re

from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str):

    cleaned = text.strip()

    # Remove Markdown JSON block
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    # Find JSON object
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "No JSON object found."
        )

    return cleaned[
        start:end + 1
    ]


def validate_quiz(
    data: Any,
    count: int
):

    if not isinstance(data, dict):

        raise ValueError(
            "Quiz response must be a JSON object."
        )

    questions = data.get(
        "questions"
    )

    if not isinstance(
        questions,
        list
    ):

        raise ValueError(
            "Quiz JSON must contain questions."
        )

    if not questions:

        raise ValueError(
            "No questions generated."
        )

    final_questions = []

    for index, item in enumerate(
        questions[:count],
        start=1
    ):

        if not isinstance(
            item,
            dict
        ):

            raise ValueError(
                f"Question {index} is invalid."
            )

        question = str(
            item.get(
                "question",
                ""
            )
        ).strip()

        options = item.get(
            "options"
        )

        answer = str(
            item.get(
                "answer",
                ""
            )
        ).strip()

        if not question:

            raise ValueError(
                f"Question {index} is empty."
            )

        if not isinstance(
            options,
            list
        ):

            raise ValueError(
                f"Question {index} options are invalid."
            )

        if len(options) != 4:

            raise ValueError(
                f"Question {index} must contain exactly 4 options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if any(
            not option
            for option in options
        ):

            raise ValueError(
                f"Question {index} has an empty option."
            )

        if answer not in options:

            # Support numeric answer indexes
            if (
                answer.isdigit()
                and 0 <= int(answer) < 4
            ):

                answer = options[
                    int(answer)
                ]

            else:

                raise ValueError(
                    f"Question {index} has invalid answer."
                )

        final_questions.append(
            {
                "question": question,
                "options": options,
                "answer": answer
            }
        )

    return {
        "questions": final_questions
    }


def generate_quiz(
    text: str,
    count: int = 3
):

    count = max(
        1,
        min(count, 10)
    )

    prompt = f"""
Create exactly {count} multiple-choice questions
from the following educational material.

Requirements:

- Exactly {count} questions.
- Every question must have exactly 4 options.
- Only one option is correct.
- Questions must be based on the supplied material.
- Distractors should be plausible.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not add explanations outside JSON.

Required JSON format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option"
        }}
    ]
}}

Educational material:

{text}
"""

    raw = generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=2600
    )

    try:

        cleaned = clean_json_block(
            raw
        )

        data = json.loads(
            cleaned
        )

        return validate_quiz(
            data,
            count
        )

    except Exception as first_error:

        # Automatic repair attempt
        repair_prompt = f"""
Convert the following quiz into valid JSON.

Return ONLY JSON.

Required format:

{{
    "questions": [
        {{
            "question": "Question",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option"
        }}
    ]
}}

Keep exactly {count} questions.

Quiz:

{raw}
"""

        repaired = generate_text(
            repair_prompt,
            temperature=0.1,
            max_output_tokens=2600
        )

        try:

            cleaned = clean_json_block(
                repaired
            )

            data = json.loads(
                cleaned
            )

            return validate_quiz(
                data,
                count
            )

        except Exception as second_error:

            raise RuntimeError(
                "Quiz generation failed.\n"
                f"Initial error: {first_error}\n"
                f"Repair error: {second_error}"
            )