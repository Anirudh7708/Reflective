//MOTIVE TEXT
window.addEventListener('load', () => {
    document.querySelector('.motive-text').classList.add('show');
});
//BODY
setTimeout(function() {
    document.querySelector('.loading-screen').style.opacity = '0'; 
    setTimeout(() => {
        document.querySelector('.loading-screen').style.display = 'none'; 
        document.querySelector('.container').style.display = 'block'; 
    }, 1000); 
}, 3000); 
//TRANSITIONS
function logo() {
    const body = document.body;
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6'); 
    const paras = document.querySelectorAll('p'); 
    const links = document.querySelectorAll('a'); 
    const section = document.querySelectorAll('section');
    const blockquote = document.querySelectorAll('blockquote')
    if (body.style.backgroundColor === 'white' || body.style.backgroundColor === '') {
        body.style.backgroundColor = '#000220';
        body.style.color = 'white';
                headings.forEach(heading => heading.style.color = 'white');
        paras.forEach(para => para.style.color = 'white');
        links.forEach(link => link.style.color = 'white');
        section.forEach(section => section.style.backgroundColor = 'black');
        section.forEach(section => section.style.color = 'white');
        blockquote.forEach(blockquote => blockquote.style.backgroundColor = 'black');
        
    } else {
        body.style.backgroundColor = 'white';
        body.style.color = 'black';
        
        headings.forEach(heading => heading.style.color = 'black');
        paras.forEach(para => para.style.color = 'white');
        links.forEach(link => link.style.color = 'black'); 
    }
    
    body.style.transition = 'background-color 0.5s, color 0.5s';
}



//functuon for smooth homer page transition

/*function checkAnimation() {
    // Check if the user has seen the animation before using localStorage
    const hasSeenAnimation = localStorage.getItem('hasSeenAnimation');

    if (hasSeenAnimation) {
        // If user has seen the animation before, skip it
        document.querySelector('.loading-screen').style.display = 'none';
        document.querySelector('.container').style.display = 'block';
    } else {
        // Show the animation for first-time visitors
        setTimeout(() => {
            // Fade out the animation screen after 3 seconds
            document.querySelector('.loading-screen').style.opacity = '0';
            setTimeout(() => {
                // Hide the animation screen and show main content
                document.querySelector('.loading-screen').style.display = 'none';
                document.querySelector('.container').style.display = 'block';
                // Mark animation as seen in localStorage
                localStorage.setItem('hasSeenAnimation', 'true');
            }, 1000); // Fade-out duration
        }, 3000); // Duration of the animation
    }
}*/

// Function to apply smooth transitions for light/dark theme change


//LOADING SCREEN
window.addEventListener("load", function() {
    const loadingScreen = document.querySelector(".loading-screen");
    const container = document.querySelector(".container");
    const paragraph = document.querySelector(".motive-text-para");

    setTimeout(() => {
        loadingScreen.style.display = "none";
        container.style.display = "block";

        setTimeout(() => {
            paragraph.classList.add("transition-active");
        }, 100); 
    }, 3000); 
});
document.getElementById('home').addEventListener('click', function() {
    // Hide the "ABOUT" page and show the "HOME" page (s-container)
    document.querySelector('.container').style.display = 'block'; // Show home page
    document.querySelector('.about-page').style.display = 'none'; // Hide about page
});
// LOGIN FORM
let loginform = document.getElementById("login-form");
let Regform = document.getElementById("registration-form");  
let indicator = document.getElementById("Indicator");

function reg() {
    Regform.style.transform = "translateX(0px)";  
    loginform.style.transform = "translateX(0px)";  
    indicator.style.transform = "translateX(100px)";s
}

function login() {
    Regform.style.transform = "translateX(378px)";  
    loginform.style.transform = "translateX(400px)"; 
    indicator.style.transform = "translateX(0px)";
}

// Call applyTransitions() to toggle between light and dark theme
document.addEventListener("DOMContentLoaded", () => {
    // Automatically apply theme transitions on page load
    applyTransitions();
});
//form
const questions = [
    { text: 'Name', type: 'text', options: [] },
    { text: 'Review', type: 'text', options: [] },
    { text: 'Rating', type: 'radio', options: ['1', '2', '3', '4', '5'] }
];
const removedQuestions = []; 

document.addEventListener('DOMContentLoaded', updatePreviewForm);

function adjustInput(input) {
    input.style.width = Math.max(200, input.value.length * 8) + "px";
}

function adjustTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + "px";
}

function addQuestion() {
    const questionText = document.getElementById('question').value;
    const questionType = document.getElementById('type').value;

    if (!questionText) {
        showErrorMessage('Please enter a question.');
        return;
    }

    const question = { text: questionText, type: questionType, options: [] };
    questions.push(question);
    displayQuestion(question);
    updatePreviewForm();
}

function displayQuestion(question) {
    const formContainer = document.getElementById('form-container');
    const questionDiv = document.createElement('div');
    questionDiv.className = 'question-item';

    const label = document.createElement('label');
    label.innerText = question.text;
    questionDiv.appendChild(label);

    const deleteButton = document.createElement('button');
    deleteButton.innerText = 'Delete';
    deleteButton.onclick = function() {
        if (questions.indexOf(question) < 3) {
            showErrorMessage('This question cannot be removed in the middle!');
            return;
        }
        deleteQuestion(questions.indexOf(question), questionDiv);
    };
    questionDiv.appendChild(deleteButton);

    const addBackButton = document.createElement('button');
    addBackButton.innerText = 'Add Back';
    addBackButton.style.display = 'none';
    addBackButton.onclick = function() {
        addBackQuestion(question, questionDiv);
    };
    questionDiv.appendChild(addBackButton);

    formContainer.appendChild(questionDiv);
}

function updatePreviewForm() {
    const previewForm = document.getElementById('preview-form');
    previewForm.innerHTML = '';

    questions.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        const label = document.createElement('label');
        label.innerText = `${index + 1}. ${question.text}`;
        questionDiv.appendChild(label);

        if (question.type === 'text') {
            const input = document.createElement('input');
            input.type = 'text';
            input.oninput = () => adjustInput(input);
            questionDiv.appendChild(input);
        } else if (question.type === 'radio' || question.type === 'checkbox') {
            question.options.forEach(option => {
                const optionDiv = document.createElement('div');
                const input = document.createElement('input');
                input.type = question.type;
                input.name = question.text;
                input.value = option;

                const optionLabel = document.createElement('label');
                optionLabel.innerText = option;

                optionDiv.appendChild(input);
                optionDiv.appendChild(optionLabel);
                questionDiv.appendChild(optionDiv);
            });
        }

        previewForm.appendChild(questionDiv);
    });
}

function deleteQuestion(index, questionDiv) {
    const removedQuestion = questions.splice(index, 1)[0];
    removedQuestions.push(removedQuestion);
    questionDiv.querySelector('button:nth-child(3)').style.display = 'inline';
    updatePreviewForm();
}

function addBackQuestion(question, questionDiv) {
    questions.push(question);
    const lastIndex = removedQuestions.indexOf(question);
    if (lastIndex > -1) removedQuestions.splice(lastIndex, 1);

    questionDiv.querySelector('button:nth-child(3)').style.display = 'none';
    updatePreviewForm();
}

function generateLink() {
    const formData = JSON.stringify(questions);
    const encodedData = encodeURIComponent(formData);
    const shareableLink = `${window.location.href}?data=${encodedData}`;

    document.getElementById('shareable-link').innerText = `Share this link: ${shareableLink}`;
}

function saveForm() {
    const saveButton = document.getElementById('save-button');
    const savedMessage = document.getElementById('saved-message');

    saveButton.style.display = 'none';

    savedMessage.style.display = 'block';

    savedMessage.style.position = 'fixed';
    savedMessage.style.top = '50%';
    savedMessage.style.left = '50%';
    savedMessage.style.transform = 'translate(-50%, -50%)';
    savedMessage.style.padding = '20px';
    savedMessage.style.backgroundColor = 'green';
    savedMessage.style.color = 'white';
    savedMessage.style.borderRadius = '8px';
    savedMessage.style.fontSize = '18px';

    setTimeout(() => {
        savedMessage.style.display = 'none';
        saveButton.style.display = 'block';
    }, 3000); 
}

function showErrorMessage(message) {
    const errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.innerText = message;
    errorMessageDiv.style.display = 'block';
    
    setTimeout(() => {
        errorMessageDiv.style.display = 'none';
    }, 3000);
}