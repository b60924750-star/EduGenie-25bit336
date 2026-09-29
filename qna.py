from gemini_client import generate_text


def answer_question(question: str):

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question accurately.

Student Question:

{question}

Instructions:

1. Give the direct answer first.
2. Explain the answer clearly.
3. Use simple language.
4. Use examples when helpful.
5. Use bullet points if appropriate.
6. Avoid unnecessary technical language.
7. Do not invent information.
8. If the question is ambiguous, mention the assumption.

Make the answer useful for a student.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1800
    )