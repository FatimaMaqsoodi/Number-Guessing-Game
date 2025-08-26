# Number-Guessing-Game
A fun and interactive **Flask web app** where players try to guess a secret number within a given range.  
It features a **light/dark theme toggle 🌙☀️**, **best score tracking 🏆**, and a **modern UI** styled with **Bootstrap 5** + **custom CSS**.

---

## ✨ Features

- 🎯 **Custom Range Selection** (0–100 enforced)  
- 🌙 **Dark/Light Theme Toggle**  
- 🏆 **Best Score Tracking** (saved per session)  
- 🔔 **Real-time Feedback** (too high, too low, won, or lost)  
- 📱 **Responsive & Mobile-Friendly UI**  
- 🎨 **Professional UI/UX with Bootstrap Icons**  

## 🛠️ Tech Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)  
- **Frontend**:  
  - HTML5 + Jinja2 templating  
  - Bootstrap 5  
  - Bootstrap Icons  
  - Custom CSS (dark/light theme)  
- **JavaScript**: Vanilla JS (fetch API for guesses)  

---

## 📂 Project Structure

```

number-guessing-game/
│
├── app.py              # Flask backend
├── templates/
│   └── game.html       # Main game UI
├── static/
│   ├── style.css       # Custom styles (dark/light, animations)
│   └── script.js       # Frontend game logic
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies

````

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/number-guessing-game.git
cd number-guessing-game
````

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

* **Windows (PowerShell)**:

  ```bash
  venv\Scripts\Activate.ps1
  ```
* **Linux/Mac**:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask App

```bash
python app.py
```

App will start on:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🖥️ Usage

1. Start the app in your browser.
2. Enter a **min and max range** (0–100).
3. Guess the secret number:

   * ⬆️ Too high → try lower.
   * ⬇️ Too low → try higher.
   * ✅ Correct → win the game!
4. Track your **attempts** and compete for the **best score**.
5. Toggle between **dark/light theme** anytime.

---
Do you want me to generate that file too?
```
