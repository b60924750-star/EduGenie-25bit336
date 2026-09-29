from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "Beginner",
    weeks: int = 6
):

    prompt = f"""
You are EduGenie, a personalized learning mentor.

Create a structured learning path.

Topic:
{topic}

Current Level:
{level}

Available Time:
{weeks} weeks

Requirements:

1. Start from the learner's current level.
2. Progress from beginner concepts to advanced concepts.
3. Divide the plan week-by-week.
4. Give topics to study for each week.
5. Give a practical activity for each week.
6. Give a learning outcome for each week.
7. Suggest resource types such as:
   - Videos
   - Articles
   - Documentation
   - Books
   - Practice websites
8. Do not invent exact URLs.
9. Include a final revision/project stage.
10. Keep the plan realistic for a student.

Use Markdown headings and bullet points.
"""

    return generate_text(
        prompt,
        temperature=0.45,
        max_output_tokens=3000
    )