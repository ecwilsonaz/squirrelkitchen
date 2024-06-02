const steps = [
    {
        type: 'prep',
        instructions: 'Prepare the salmon on a plate:',
        ingredients: [
            { name: '2 4-6 oz salmon fillets, patted dry', icon: '🐟', time: 3, voice: 'salmon' }
        ]
    },
    {
        type: 'prep',
        instructions: 'Mix the spice rub into a bowl:',
        ingredients: [
            { name: '2 tablespoons olive oil', icon: '🫒', time: 0.5, voice: 'olive oil' },
            { name: '1 clove garlic, minced or crushed', icon: '🧄', time: 3, voice: 'garlic' },
            { name: '1/2 teaspoon chili powder', icon: '🫙', time: 0.5, voice: 'chili powder' },
            { name: '1/2 teaspoon cumin', icon: '🫙', time: 0.5, voice: 'cumin'},
            { name: '1/2 teaspoon onion powder', icon: '🫙', time: 0.5, voice: 'onion powder' },
            { name: '1/4 teaspoon black pepper', icon: '🫙', time: 0.5, voice: 'pepper' },
            { name: '1/4 teaspoon salt', icon: '🫙', time: 0.5, voice: 'salt' }
        ]
    },
    {
        type: 'prep',
        instructions: 'Add the salsa ingredients into a bowl:',
        ingredients: [
            { name: '1 ripe avocado, pitted and diced', icon: '🥑', time: 2, voice: 'avocado' },
            { name: '2 tablespoons onion, diced', icon: '🧅', time: 3, voice: 'onion'},
            { name: '2 tablespoons cilantro, minced', icon: '🌿', time: 3, voice: 'cilantro' },
            { name: '1 tablespoon olive oil', icon: '🫒', time: 0.5, voice: 'olive oil' },
            { name: '1 tablespoon lime juice', icon: '🍋‍🟩', time: 1.5, voice: 'lime'},
            { name: 'salt and pepper to taste', icon: '🫙', time: 0.5, voice: 'salt' }
        ]
    },
    {
        type: 'cooking',
        instructions: 'Gently mix the avocado salsa until fully combined.',
        time: 1 
    },
    {
        type: 'cooking',
        instructions: 'Brush or rub salmon with the spice mixture.',
        time: 1
    },
    {
        type: 'cooking',
        instructions: 'Heat a large heavy-duty (preferably non-stick) pan or grill to 🔥 medium-high heat.',
        time: 3
    },
    {
        type: 'cooking',
        instructions: 'Add salmon to the pan and cook for ⏳ 6 minutes, skin side down. Use this time to clean up, or just be present with your senses!',
        timer: 6,
        time: 6.5,
        timerLabel: 'Cook salmon (skin side down)'
    },
    {
        type: 'cooking',
        instructions: 'Flip the salmon and cook for another 3 minutes.',
        timer: 3,
        time: 3.5,
        timerLabel: 'Cook salmon (skin side up)'
    },
    {
        type: 'cooking',
        instructions: 'Remove from salmon from pan, top with avocado salsa, and serve immediately.',
        time: 1
    },
    {
        type: 'finish',
        instructions: 'Enjoy!',
        time: 0
    }
];

let currentStep = 0;
let totalTime = steps.reduce((acc, step) => {
    if (step.ingredients) {
        return acc + step.ingredients.reduce((sum, ingredient) => sum + ingredient.time, 0);
    } else {
        return acc + step.time;
    }
}, 0);
let completedTime = 0;

let activeTimers = {};  // To keep track of active timers

document.addEventListener('DOMContentLoaded', () => {
    const stepContainer = document.getElementById('step-container');
    const progressBar = document.getElementById('progress');
    const progressText = document.getElementById('progress-text');
    const nextStepButton = document.getElementById('next-step');
    const activeTimersContainer = document.getElementById('active-timers');
    const alarmSound = document.getElementById('alarm-sound');

    function renderStep(stepIndex) {
        stepContainer.innerHTML = '';
        const step = steps[stepIndex];

        const stepElement = document.createElement('div');
        stepElement.className = 'step active';
        stepElement.innerHTML = `<p>${step.instructions}</p>`;

        if (step.type === 'prep') {
            const ingredientContainer = document.createElement('div');
            ingredientContainer.className = 'ingredient-container';
            step.ingredients.forEach(ingredient => {
                const ingredientElement = document.createElement('div');
                ingredientElement.className = 'ingredient';
                ingredientElement.innerHTML = `${ingredient.icon} ${ingredient.name}`;
                ingredientElement.addEventListener('click', () => {
                    ingredientElement.classList.toggle('checked');
                    if (ingredientElement.classList.contains('checked')) {
                        completedTime += ingredient.time;
                    } else {
                        completedTime -= ingredient.time;
                    }
                    updateProgressBar();
                });
                ingredientContainer.appendChild(ingredientElement);
            });
            stepElement.appendChild(ingredientContainer);
        }

        if (step.type === 'cooking' && step.timer) {
            const timerWrapper = document.createElement('div');
            timerWrapper.className = 'timer-wrapper';
            const timerElement = document.createElement('div');
            timerElement.className = 'timer';
            const timerId = `start-timer-${stepIndex}`;
            timerElement.innerHTML = `<button id="${timerId}" class="start-timer-btn">Start timer for ${step.timer} minutes</button>`;
            timerWrapper.appendChild(timerElement);
            stepElement.appendChild(timerWrapper);

            console.log(`Created timer button for step ${stepIndex}`);

            stepContainer.appendChild(stepElement);

            // Attach event listeners after elements are in the DOM
            const startButton = document.getElementById(timerId);
            if (startButton) {
                console.log(`Attaching event listener to start button for step ${stepIndex}`);
                startButton.addEventListener('click', () => {
                    console.log(`Start timer button clicked for step ${stepIndex}`);
                    startTimer(step.timer * 60, step.timerLabel, stepIndex);
                    timerWrapper.style.display = 'none';  // Hide the div containing the start timer button
                });
            } else {
                console.error(`Start button not found for step ${stepIndex}`);
            }
        } else {
            stepContainer.appendChild(stepElement);
        }

        // Show confetti if it's the final step
        if (stepIndex === steps.length - 1) {
            showConfetti();
        }

        updateProgressBar();
    }

    function updateProgressBar() {
        const progress = (completedTime / totalTime) * 100;
        const remainingTime = totalTime - completedTime;
        progressBar.style.width = `${progress}%`;
        progressText.textContent = `${Math.round(progress)}% Complete (ETA: ${remainingTime} minutes)`;
        
        // Show confetti if ETA is 0 minutes
        if (remainingTime === 0) {
            showConfetti();
        }
    }

    function startTimer(duration, label, stepIndex) {
        let timer = duration, minutes, seconds;
        const timerElement = document.createElement('div');
        timerElement.className = 'active-timer';
        const timerId = `active-timer-${stepIndex}`;
        timerElement.id = timerId;

        const timeSpan = document.createElement('span');
        timeSpan.className = 'timer-time';
        timeSpan.innerHTML = `⏳ <strong>${formatTime(duration)}</strong>`;

        const labelSpan = document.createElement('span');
        labelSpan.className = 'timer-label';
        labelSpan.textContent = ` - ${label}`;

        timerElement.appendChild(timeSpan);
        timerElement.appendChild(labelSpan);

        activeTimersContainer.appendChild(timerElement);

        const interval = setInterval(() => {
            if (!activeTimers[stepIndex]) {
                clearInterval(interval);
                return;
            }

            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            timeSpan.innerHTML = `⏳ <strong>${formatTime(timer)}</strong>`;

            if (--timer < 0) {
                clearInterval(interval);
                timeSpan.innerHTML = `<strong>0:00</strong>`;
                delete activeTimers[stepIndex];
                alarmSound.play();  // Play alarm sound when timer reaches 0
            }
        }, 1000);

        activeTimers[stepIndex] = { interval, timeSpan, labelSpan };
        console.log(`Timer started for step ${stepIndex} with duration ${duration} seconds`);
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }

    function showConfetti() {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }

    nextStepButton.addEventListener('click', () => {
        if (currentStep < steps.length - 1) {
            // Assume all items were checked off for the sake of calculating progress
            if (steps[currentStep].type === 'prep') {
                const uncheckedItems = steps[currentStep].ingredients.filter(ingredient => {
                    const ingredientElement = Array.from(document.querySelectorAll('.ingredient')).find(el => el.textContent.includes(ingredient.name));
                    return !ingredientElement.classList.contains('checked');
                });
                uncheckedItems.forEach(item => completedTime += item.time);
            } else if (steps[currentStep].type === 'cooking') {
                completedTime += steps[currentStep].time;
            }

            currentStep++;
            renderStep(currentStep);

            updateProgressBar();
        } else {
            // Final step completed, show confetti
            showConfetti();
        }

        alarmSound.pause();  // Stop alarm sound when progressing to the next step
        alarmSound.currentTime = 0;  // Reset alarm sound
    });

    // Initial render
    renderStep(currentStep);

    // Voice Control Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        let recognitionActive = false;

        function startRecognition() {
            if (!recognitionActive) {
                try {
                    recognition.start();
                    recognitionActive = true;
                    console.log('Speech recognition started');
                } catch (error) {
                    console.error('Error starting speech recognition:', error);
                }
            }
        }

        recognition.onstart = () => {
            recognitionActive = true;
            console.log('Speech recognition started');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[event.resultIndex][0].transcript.trim().toLowerCase();
            console.log(`Recognized: ${transcript}`);

            if (transcript === 'next') {
                nextStepButton.click();
            } else if (transcript === 'start timer') {
                const startButton = document.querySelector('.start-timer-btn:not([disabled])');
                if (startButton) {
                    startButton.click();
                }
            } else {
                checkIngredient(transcript);
            }
        };

        recognition.onerror = (event) => {
            console.error(`Speech recognition error: ${event.error}`);
            recognitionActive = false;
            if (event.error === 'aborted' || event.error === 'network') {
                recognition.stop();
                setTimeout(startRecognition, 1000);
            }
        };

        recognition.onend = () => {
            console.log('Speech recognition ended, restarting...');
            recognitionActive = false;
            setTimeout(startRecognition, 1000);
        };

        startRecognition();
    } else {
        console.error('Speech recognition not supported in this browser.');
    }

   function checkIngredient(transcript) {
        const currentIngredients = steps[currentStep]?.ingredients || [];
        currentIngredients.forEach(ingredient => {
            const ingredientElement = Array.from(document.querySelectorAll('.ingredient')).find(el => el.textContent.includes(ingredient.name));
            if (ingredientElement) {
                if (transcript.includes(ingredient.voice.toLowerCase())) {
                    if (!ingredientElement.classList.contains('checked')) {
                        ingredientElement.classList.add('checked');
                        completedTime += ingredient.time;
                        updateProgressBar();
                        console.log(`Checked off ingredient: ${ingredient.name}`);
                    }
                }
            }
        });
    }
});