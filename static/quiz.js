document.addEventListener("DOMContentLoaded", () => {
    const optionButtons = document.querySelectorAll(".option-btn");
    const feedbackMessage = document.getElementById("feedback-message");
    const correctAnswer = document.querySelector(".quiz-container").getAttribute("data-correct-answer");
    const nextButtonForm = document.querySelector(".next-question form");
    const timerElement = document.getElementById("timer");

    // Get Time Limit
    let timeRemaining = parseInt(timerElement.dataset.timeLimit, 10);

    function startTimer() {
        const timerInterval = setInterval(() => {
            timerElement.textContent = `${timeRemaining} seconds`;
            timeRemaining--;

            // If time runs out, submit the next question
            if (timeRemaining < 0) {
                clearInterval(timerInterval);
                nextButtonForm.submit();
            }
        }, 1000);
    }

    startTimer();

    optionButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Disable all option buttons after selection
            optionButtons.forEach(btn => btn.disabled = true);

            // Check if selected option is correct
            if (button.getAttribute("data-option-id") === correctAnswer) {
                feedbackMessage.textContent = "Correct!";
                feedbackMessage.style.color = "green";
                button.classList.add("correct");

                // Send score update to the server
                fetch("/update_score", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ increment: 1 })  // Only increment if correct
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Score updated:", data.user_score);
                })
                .catch(error => console.error("Error updating score:", error));

            } else {
                feedbackMessage.textContent = "Wrong answer!";
                feedbackMessage.style.color = "red";
                button.classList.add("incorrect");
                document.querySelector(`.option-btn[data-option-id="${correctAnswer}"]`).classList.add("correct");
            }

            // Auto-submit the next question after a brief delay
            setTimeout(() => {
                nextButtonForm.submit();
            }, 1500); // 1.5-second delay to allow user to see feedback
        });
    });
});
