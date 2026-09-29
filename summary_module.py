from gemini_client import generate_text


def summarize_text(text: str):

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following study material.

Requirements:

1. Keep the important information.
2. Remove repetition.
3. Use simple language.
4. Make it useful for quick revision.
5. Give a short overview.
6. Give important points as bullets.
7. Do not add facts that are not present in the original text.

Study Material:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=1800
    )