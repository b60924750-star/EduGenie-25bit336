import os

from gemini_client import generate_text


def local_lamini_explanation(topic: str):

    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model="MBZUAI/LaMini-Flan-T5-783M",
        max_new_tokens=300
    )

    prompt = f"""
Explain the following topic to a beginner.

Topic:

{topic}

Use:

1. Simple definition
2. How it works
3. Easy example
4. Important points
"""

    result = generator(prompt)[0][
        "generated_text"
    ]

    return result.strip()


def explain_topic(topic: str):

    mode = os.getenv(
        "EXPLAINER_MODE",
        "gemini"
    ).lower().strip()

    # Optional local LaMini model
    if mode == "local":

        try:

            return local_lamini_explanation(
                topic
            )

        except ImportError:

            raise RuntimeError(
                "Local explanation mode requires "
                "transformers. Run:\n"
                "pip install -r requirements-local.txt"
            )

        except Exception as exc:

            raise RuntimeError(
                f"Local LaMini explanation failed: {exc}"
            )

    # Default Gemini explanation
    prompt = f"""
You are EduGenie, a beginner-friendly teacher.

Explain this topic in very simple language:

{topic}

Use this structure:

1. What is it?
2. How does it work?
3. Simple real-world example
4. Important points to remember

Rules:

- Avoid unnecessary jargon.
- Define technical terms.
- Keep the explanation easy to understand.
- Use examples whenever possible.
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1600
    )