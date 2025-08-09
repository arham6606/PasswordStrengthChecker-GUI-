# 🔒 Password Strength Checker GUI

A sleek and user-friendly PyQt5 application that evaluates password strength in real-time, detects breaches, and provides actionable suggestions — designed for security-conscious users and beginner developers alike.

---

## Project Overview

Strong passwords are the cornerstone of cybersecurity. This desktop GUI tool measures password strength dynamically as you type and verifies if your password has appeared in known breach databases, empowering users to create safer passwords effortlessly.

Built with Python and PyQt5, it bridges backend security logic with polished front-end user experience, making it a practical beginner-to-intermediate project that combines theory with real-world application.

---

## Features

- Real-time strength meter with a visual progress bar  
- On-demand breach detection that alerts if the password appears in data breaches  
- Password visibility toggle with an eye icon for secure input confirmation  
- Tailored, actionable suggestions to improve password quality  
- Dark-themed, modern, and clean UI design  
- Debounced input handling for efficient evaluation without UI lag  

---

## Tech Stack

- Python 3.x  
- PyQt5 GUI framework  
- Custom password strength and breach detection modules  

---

## Installation Instructions

1. Clone the repository:  
   `git clone https://github.com/YourUsername/PasswordStrengthChecker-GUI.git`  
   and navigate into the directory.

2. (Recommended) Create and activate a Python virtual environment.

3. Install required packages:  
   `pip install -r requirement.txt`

4. Run the application:  
   `python gui/window.py`

---

## Project Structure Overview

- `data/`: Contains weak password lists and image assets  
- `checker/`: Core modules for password strength calculation, breach checking, and suggestions  
- `gui/`: PyQt5 UI and window management  
- `README.md`: Project documentation  
- `venv`: Python dependencies  

---

## Future Enhancements

- Offline breach database integration for instant local checks  
- Multi-language support to broaden accessibility  
- Exportable password strength reports and logs  
- UI refinement with animations and theming options  
- Advanced strength metrics using entropy calculations  

---

## About Me

I am a Computer Engineering student at ITU, Pakistan, focusing on backend development and cybersecurity. This project reflects my dedication to building secure software with a clean user experience.  

Connect with me on [LinkedIn](https://www.linkedin.com/in/-arham) to collaborate or provide feedback.

---

