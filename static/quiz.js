document.addEventListener("DOMContentLoaded", () => {
    const optionButtons = document.querySelectorAll(".option-btn");
    const feedbackMessage = document.getElementById("feedback-message");
    const correctAnswer = document.querySelector(".quiz-container").getAttribute("data-correct-answer");
    const nextButtonForm = document.querySelector(".next-question form");
    const timerElement = document.getElementById("timer");

    let timeRemaining = parseInt(timerElement.getAttribute("data-time-limit")) * 60; // Convert minutes to seconds

    function startTimer() {
        const timerInterval = setInterval(() => {
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            timerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
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

            } else {
                feedbackMessage.textContent = "Wrong answer!";
                feedbackMessage.style.color = "red";
                button.classList.add("incorrect");
                // Mark the correct answer as green
                document.querySelector(`.option-btn[data-option-id="${correctAnswer}"]`).classList.add("correct");
            }

            // Auto-submit the next question after a brief delay
            setTimeout(() => {
                nextButtonForm.submit();
            }, 1500); // 1.5-second delay to allow user to see feedback
        });
    });
});
