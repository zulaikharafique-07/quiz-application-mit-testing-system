# Quiz Application (MIT Testing System)

A desktop quiz app built with Python, tkinter, and MySQL.

## Features
- User registration and login
- 20 multiple-choice questions (SQL and Python basics)
- Score, percentage, and Pass/Fail result (pass mark: 40%)
- Results saved in the database
- Maximum of 3 attempts per user

## Tools Used
- Python
- tkinter (GUI)
- MySQL (database)
- Pillow (logo image)

## Files
- `QuizApplicationProject.py` - Main application code
- `quizApp.sql` - Database tables and sample questions
- `mitt.png` - Logo image

## How to Run
1. Install MySQL and the required libraries:
   ```
   python -m pip install mysql-connector-python pillow
   ```
2. Run `quizApp.sql` in MySQL Workbench to create the database.
3. In `QuizApplicationProject.py`, replace `my_password` with your own MySQL password.
4. Keep `mitt.png` in the same folder as the Python file.
5. Run the Python file:
   ```
   python QuizApplicationProject.py
   ```
   Note: After finishing a quiz, close the app and run it again to log in for the next attempt.

## Author
Zulaikha Rafique
