/* Global */
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    margin: 0;
    padding: 0;
}

/* Container */
.container {
    max-width: 500px;
    margin: 2rem auto;
    padding: 1rem;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    backdrop-filter: blur(8px);
}

/* Headings */
h1, h2 {
    text-align: center;
    margin-bottom: 0.5rem;
}

/* Inputs */
input {
    width: 100%;
    padding: 0.6rem;
    border-radius: 8px;
    border: none;
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

/* Buttons */
button {
    width: 100%;
    padding: 0.7rem;
    border: none;
    border-radius: 8px;
    background: #ff6a00;
    color: #fff;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

button:hover {
    background: #ff8c42;
}

/* Lists */
.app-list {
    list-style: none;
    padding: 0;
}

.app-list li {
    padding: 0.5rem;
    border-radius: 5px;
    margin-bottom: 0.3rem;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.app-list li.success {
    background: rgba(0, 255, 0, 0.2);
    color: #00ff00;
}

.app-list li.fail {
    background: rgba(255, 0, 0, 0.2);
    color: #ff4d4d;
}

/* Loader */
.loader {
    border: 4px solid rgba(255,255,255,0.2);
    border-top: 4px solid #fff;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    animation: spin 1s linear infinite;
    margin-left: 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg);}
    100% { transform: rotate(360deg);}
}

/* Footer */
footer {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.8rem;
    opacity: 0.7;
}
