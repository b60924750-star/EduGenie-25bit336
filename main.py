from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    version="1.0.0",
    description="AI-powered educational learning assistant"
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EduGenie AI</title>
        <style>
            body {
                font-family: Arial;
                background: #f2f4f8;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #333;
            }
            .box {
                background: white;
                padding: 30px;
                border-radius: 15px;
                max-width: 600px;
                margin: auto;
                box-shadow: 0 4px 15px #ccc;
            }
            input, textarea, button {
                width: 90%;
                padding: 12px;
                margin: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            button {
                background: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>🎓 EduGenie AI</h1>
            <p>AI Powered Educational Learning Assistant</p>

            <textarea id="question"
                placeholder="Enter your question here..."></textarea>

            <button onclick="askQuestion()">Ask Question</button>

            <h3>Answer:</h3>
            <p id="answer">Your answer will appear here.</p>
        </div>

        <script>
            async function askQuestion() {
                let question =
                    document.getElementById("question").value;

                let response = await fetch("/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: question
                    })
                });

                let data = await response.json();

                document.getElementById("answer").innerText =
                    data.answer;
            }
        </script>
    </body>
    </html>
    """


@app.post("/ask")
def ask_question(data: dict):
    question = data.get("question", "")

    if not question:
        return {"answer": "Please enter a question."}

    return {
        "answer": f"You asked: {question}"
    }


@app.get("/health")
def health():
    return {
        "status": "running",
        "message": "EduGenie AI is working!"
    }