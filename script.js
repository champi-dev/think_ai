const startButton = document.getElementById('start-button');
const listeningIndicator = document.getElementById('listening-indicator');
const transcriptDiv = document.getElementById('transcript');
const responseDiv = document.getElementById('response');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.onstart = () => {
    listeningIndicator.classList.add('listening');
    startButton.textContent = 'Listening...';
};

recognition.onend = () => {
    listeningIndicator.classList.remove('listening');
    startButton.textContent = 'Start Listening';
};

recognition.onresult = (event) => {
    const current = event.resultIndex;
    const transcript = event.results[current][0].transcript;
    transcriptDiv.textContent = `You said: ${transcript}`;
    handleCommand(transcript);
};

startButton.addEventListener('click', () => {
    recognition.start();
});

function handleCommand(command) {
    let response = '';
    if (command.includes('hello')) {
        response = 'Hello there!';
    } else if (command.includes('what time is it')) {
        const time = new Date().toLocaleTimeString();
        response = `The time is ${time}`;
    } else if (command.includes('what is the date')) {
        const date = new Date().toLocaleDateString();
        response = `Today's date is ${date}`;
    } else {
        response = "I'm not sure how to respond to that.";
    }
    speak(response);
    responseDiv.textContent = `Response: ${response}`;
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}
