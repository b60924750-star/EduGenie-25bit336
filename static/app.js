const task =
    document.getElementById("task");

const levelField =
    document.getElementById("levelField");

const weeksField =
    document.getElementById("weeksField");

const level =
    document.getElementById("level");

const weeks =
    document.getElementById("weeks");

const inputText =
    document.getElementById("inputText");

const inputLabel =
    document.getElementById("inputLabel");

const submitBtn =
    document.getElementById("submitBtn");

const clearBtn =
    document.getElementById("clearBtn");

const copyBtn =
    document.getElementById("copyBtn");

const errorBox =
    document.getElementById("errorBox");

const resultCard =
    document.getElementById("resultCard");

const resultTitle =
    document.getElementById("resultTitle");

const result =
    document.getElementById("result");


/* TASK INFORMATION */

const taskMeta = {

    qa: {

        label: "Your Question",

        placeholder:
            "Example: What is the difference between TCP and UDP?"

    },

    explain: {

        label: "Topic to Explain",

        placeholder:
            "Example: Explain normalization in DBMS for a beginner."

    },

    quiz: {

        label: "Topic or Study Passage",

        placeholder:
            "Paste a passage or enter a topic from which the quiz should be created."

    },

    summarize: {

        label: "Text to Summarize",

        placeholder:
            "Paste your educational notes or a long paragraph here."

    },

    learn: {

        label: "Topic for Your Learning Path",

        placeholder:
            "Example: SQL, Python, Computer Networks, Data Science..."

    }

};


/* UPDATE UI */

function updateTaskUI() {

    const selected =
        task.value;

    const meta =
        taskMeta[selected];

    inputLabel.textContent =
        meta.label;

    inputText.placeholder =
        meta.placeholder;


    const isLearn =
        selected === "learn";


    levelField.classList.toggle(
        "hidden",
        !isLearn
    );


    weeksField.classList.toggle(
        "hidden",
        !isLearn
    );

}


/* ERROR */

function showError(message) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


function clearError() {

    errorBox.textContent =
        "";

    errorBox.classList.add(
        "hidden"
    );

}


/* NORMAL RESULT */

function renderPlainText(text) {

    result.textContent =
        text;

}


/* QUIZ RESULT */

function renderQuiz(data) {

    result.innerHTML = "";


    data.questions.forEach(
        (q, qIndex) => {

            const box =
                document.createElement(
                    "div"
                );

            box.className =
                "quiz-question";


            const title =
                document.createElement(
                    "h3"
                );

            title.textContent =
                `${qIndex + 1}. ${q.question}`;


            box.appendChild(
                title
            );


            const feedback =
                document.createElement(
                    "div"
                );

            feedback.className =
                "quiz-feedback";

            feedback.textContent =
                "Choose one option.";


            q.options.forEach(
                option => {

                    const label =
                        document.createElement(
                            "label"
                        );

                    label.className =
                        "option";


                    const radio =
                        document.createElement(
                            "input"
                        );

                    radio.type =
                        "radio";

                    radio.name =
                        `q-${qIndex}`;

                    radio.value =
                        option;


                    radio.addEventListener(
                        "change",
                        () => {

                            box
                                .querySelectorAll(
                                    ".option"
                                )
                                .forEach(
                                    element => {

                                        element.classList.remove(
                                            "correct",
                                            "wrong"
                                        );

                                    }
                                );


                            if (
                                option ===
                                q.answer
                            ) {

                                label.classList.add(
                                    "correct"
                                );

                                feedback.textContent =
                                    "Correct! 🎉";

                            }

                            else {

                                label.classList.add(
                                    "wrong"
                                );

                                feedback.textContent =
                                    `Not quite. Correct answer: ${q.answer}`;

                            }

                        }
                    );


                    label.appendChild(
                        radio
                    );


                    label.append(
                        ` ${option}`
                    );


                    box.appendChild(
                        label
                    );

                }
            );


            box.appendChild(
                feedback
            );


            result.appendChild(
                box
            );

        }
    );

}


/* SUBMIT */

async function submitTask() {

    clearError();


    const value =
        inputText.value.trim();


    if (!value) {

        showError(
            "Please enter a question, topic, or study text first."
        );

        inputText.focus();

        return;

    }


    submitBtn.disabled =
        true;

    submitBtn.textContent =
        "Thinking...";


    const selected =
        task.value;


    let endpoint = "";

    let payload = {};


    if (selected === "qa") {

        endpoint =
            "/qa";

        payload = {
            text: value
        };

    }


    else if (selected === "explain") {

        endpoint =
            "/explain";

        payload = {
            text: value
        };

    }


    else if (selected === "quiz") {

        endpoint =
            "/quiz";

        payload = {

            text: value,

            count: 3

        };

    }


    else if (selected === "summarize") {

        endpoint =
            "/summarize";

        payload = {

            text: value

        };

    }


    else if (selected === "learn") {

        endpoint =
            "/learn/recommendations";

        payload = {

            topic: value,

            level:
                level.value,

            weeks:
                Number(weeks.value)

        };

    }


    try {

        const response =
            await fetch(
                endpoint,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            payload
                        )

                }
            );


        const body =
            await response.json();


        if (
            !response.ok ||
            !body.success
        ) {

            throw new Error(
                body.detail ||
                "The server could not complete the request."
            );

        }


        resultCard.classList.remove(
            "hidden"
        );


        const titles = {

            qa:
                "Answer",

            explain:
                "Simple Explanation",

            quiz:
                "Practice Quiz",

            summarize:
                "Quick Summary",

            learn:
                "Personalized Learning Path"

        };


        resultTitle.textContent =
            titles[selected];


        if (
            selected === "quiz"
        ) {

            renderQuiz(
                body.result
            );

        }

        else {

            renderPlainText(
                body.result
            );

        }


        resultCard.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }


    catch (error) {

        showError(
            error.message ||
            "Something went wrong."
        );

    }


    finally {

        submitBtn.disabled =
            false;

        submitBtn.textContent =
            "Generate Answer";

    }

}


/* TASK CHANGE */

task.addEventListener(
    "change",
    updateTaskUI
);


/* SUBMIT */

submitBtn.addEventListener(
    "click",
    submitTask
);


/* CLEAR */

clearBtn.addEventListener(
    "click",
    () => {

        inputText.value =
            "";

        clearError();

        result.innerHTML =
            "";

        resultCard.classList.add(
            "hidden"
        );

        inputText.focus();

    }
);


/* COPY */

copyBtn.addEventListener(
    "click",
    async () => {

        const text =
            result.innerText.trim();


        if (!text) {

            return;

        }


        try {

            await navigator.clipboard.writeText(
                text
            );


            copyBtn.textContent =
                "Copied!";


            setTimeout(
                () => {

                    copyBtn.textContent =
                        "Copy";

                },
                1200
            );

        }

        catch {

            showError(
                "Copy failed. Select the result and copy it manually."
            );

        }

    }
);


/* INITIAL UI */

updateTaskUI();