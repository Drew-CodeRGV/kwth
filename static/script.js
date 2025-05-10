// Game state
let currentGameMode = '';
let currentAirport = null;
let hintsUsed = 0;
let score = 0;
let currentImageIndex = 0;

// UI Functions
function showGameModeSelect() {
    document.getElementById('splashScreen').classList.add('hidden');
    document.getElementById('gameModeSelect').classList.remove('hidden');
}

function backToSplash() {
    document.getElementById('gameModeSelect').classList.add('hidden');
    document.getElementById('splashScreen').classList.remove('hidden');
}

function backToGameSelect() {
    document.getElementById('gameScreen').classList.add('hidden');
    document.getElementById('meaningScreen').classList.add('hidden');
    document.getElementById('resultScreen').classList.add('hidden');
    document.getElementById('gameModeSelect').classList.remove('hidden');
    resetGame();
}

function backToGame() {
    document.getElementById('meaningScreen').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');
}

// Game Functions
async function startGame(mode) {
    currentGameMode = mode;
    document.getElementById('gameModeSelect').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');
    
    await loadNewAirport();
}

async function loadNewAirport() {
    try {
        const response = await fetch(`/get_airport?mode=${currentGameMode}`);
        const data = await response.json();
        
        currentAirport = data;
        hintsUsed = 0;
        
        // Update UI
        updateGameUI();
        
    } catch (error) {
        console.error('Error loading airport:', error);
        alert('Error loading airport. Please try again.');
    }
}

function updateGameUI() {
    // Clear previous state
    document.getElementById('answerInput').value = '';
    document.getElementById('hintText').classList.add('hidden');
    document.getElementById('hintButton').textContent = '💡 Hint (0/3)';
    document.getElementById('hintButton').disabled = false;
    
    // Update images
    document.getElementById('terminalImage').src = currentAirport.images.terminal;
    document.getElementById('overheadImage').src = currentAirport.images.overhead;
    document.getElementById('entranceImage').src = currentAirport.images.entrance;
    
    // Reset image slider
    currentImageIndex = 0;
    showImage(0);
    
    // Update question
    if (currentGameMode === 'guess_code') {
        document.getElementById('questionText').textContent = `What is the airport code for ${currentAirport.city}?`;
        document.getElementById('airportCodeDisplay').classList.add('hidden');
        document.getElementById('airplaneIcons').classList.remove('hidden');
        document.getElementById('answerInput').placeholder = 'Enter 3-letter code';
        document.getElementById('answerInput').maxLength = 3;
    } else {
        document.getElementById('questionText').textContent = 'Which city has this airport code?';
        document.getElementById('airplaneIcons').classList.add('hidden');
        
        // Display airport code as luggage tag
        const codeDisplay = document.getElementById('airportCodeDisplay');
        codeDisplay.classList.remove('hidden');
        const code = currentAirport.code;
        const colors = ['red', 'blue', 'yellow', 'orange', 'green'];
        let html = '<div class="luggage-tag">';
        for (let i = 0; i < code.length; i++) {
            html += `<div class="tag-letter ${colors[i % colors.length]}">${code[i]}</div>`;
        }
        html += '</div>';
        codeDisplay.innerHTML = html;
        
        document.getElementById('answerInput').placeholder = 'Enter city name';
        document.getElementById('answerInput').maxLength = 50;
    }
    
    // Update score
    document.getElementById('score').textContent = score;
}

function showImage(index) {
    const images = document.querySelectorAll('.airport-image');
    const dots = document.querySelectorAll('.dot');
    
    images.forEach((img, i) => {
        img.classList.toggle('active', i === index);
    });
    
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
    
    currentImageIndex = index;
}

async function showHint() {
    if (hintsUsed >= 3) return;
    
    hintsUsed++;
    const hintText = document.getElementById('hintText');
    const hintButton = document.getElementById('hintButton');
    
    hintButton.textContent = `💡 Hint (${hintsUsed}/3)`;
    
    let hint = '';
    if (currentGameMode === 'guess_code') {
        // Code guessing hints
        if (hintsUsed === 1) {
            hint = `Airport name: ${currentAirport.name}`;
        } else if (hintsUsed === 2) {
            hint = `Location: ${currentAirport.city}, ${currentAirport.country}`;
        } else {
            hint = `The code "${currentAirport.code}" stands for: ${currentAirport.meaning_options[0]}`;
        }
    } else {
        // City guessing hints
        if (hintsUsed <= currentAirport.city_facts.length) {
            hint = currentAirport.city_facts[hintsUsed - 1];
        } else {
            hint = `This airport serves the metropolitan area of ${currentAirport.city}`;
        }
    }
    
    hintText.textContent = hint;
    hintText.classList.remove('hidden', 'fade-in');
    void hintText.offsetWidth; // Force reflow
    hintText.classList.add('fade-in');
    
    if (hintsUsed >= 3) {
        hintButton.disabled = true;
    }
}

async function submitAnswer() {
    const userAnswer = document.getElementById('answerInput').value.trim();
    if (!userAnswer) return;
    
    const correctAnswer = currentGameMode === 'guess_code' ? currentAirport.code : currentAirport.city;
    
    const response = await fetch('/check_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            mode: currentGameMode,
            answer: userAnswer,
            correct: correctAnswer
        })
    });
    
    const result = await response.json();
    
    if (result.correct) {
        score += (3 - hintsUsed) * 10; // Bonus points for using fewer hints
        showMeaningQuestion();
    } else {
        showResult(false, `Incorrect! The correct answer is: ${correctAnswer}`);
    }
}

function showMeaningQuestion() {
    document.getElementById('gameScreen').classList.add('hidden');
    document.getElementById('meaningScreen').classList.remove('hidden');
    
    // Update meaning question
    document.getElementById('meaningCode').textContent = currentAirport.code;
    
    // Create meaning options
    const optionsContainer = document.getElementById('meaningOptions');
    optionsContainer.innerHTML = '';
    
    currentAirport.meaning_options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'meaning-option';
        button.textContent = option;
        button.onclick = () => submitMeaning(option);
        optionsContainer.appendChild(button);
    });
}

async function submitMeaning(selected) {
    const isCorrect = selected === currentAirport.correct_meaning;
    
    if (isCorrect) {
        score += 15; // Bonus for correct meaning
        showResult(true, `Excellent! ${currentAirport.code} stands for: ${selected}`);
    } else {
        showResult(false, `Not quite. ${currentAirport.code} stands for: ${currentAirport.correct_meaning}`);
    }
}

function showResult(success, message) {
    document.getElementById('gameScreen').classList.add('hidden');
    document.getElementById('meaningScreen').classList.add('hidden');
    document.getElementById('resultScreen').classList.remove('hidden');
    
    const resultMessage = document.getElementById('resultMessage');
    const correctAnswer = document.getElementById('correctAnswer');
    
    resultMessage.textContent = success ? '🎉 Correct!' : '❌ Incorrect';
    resultMessage.style.color = success ? '#34C759' : '#FF3B30';
    correctAnswer.textContent = message;
    
    document.getElementById('score').textContent = score;
}

async function playAgain() {
    document.getElementById('resultScreen').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');
    await loadNewAirport();
}

function resetGame() {
    score = 0;
    hintsUsed = 0;
    currentAirport = null;
    currentImageIndex = 0;
}

// Auto-advance images
setInterval(() => {
    const nextIndex = (currentImageIndex + 1) % 3;
    showImage(nextIndex);
}, 5000);

// Handle Enter key for answer submission
document.getElementById('answerInput').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        submitAnswer();
    }
});

// Prevent zoom on double-tap
document.addEventListener('touchend', function(event) {
    if (event.target.tagName !== 'INPUT') {
        event.preventDefault();
    }
}, { passive: false });

// Uppercase input for airport codes
document.getElementById('answerInput').addEventListener('input', function(e) {
    if (currentGameMode === 'guess_code') {
        this.value = this.value.toUpperCase();
    }
});
