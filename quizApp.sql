CREATE DATABASE IF NOT EXISTS quizApp;
USE quizApp;

CREATE TABLE IF NOT EXISTS registration(
   regid INT PRIMARY KEY AUTO_INCREMENT,
   regfname TEXT,
   reglname TEXT,
   regmobile VARCHAR(13),
   regemail TEXT,
   regpassword TEXT
);

CREATE TABLE IF NOT EXISTS questions(
   questid INT PRIMARY KEY,
   question TEXT,
   answerkey TEXT
);

CREATE TABLE IF NOT EXISTS answers(
   questid INT,
   answerid INT PRIMARY KEY,
   answer TEXT,
   FOREIGN KEY (questid) REFERENCES questions(questid)
);

CREATE TABLE IF NOT EXISTS result (
    resultid INT AUTO_INCREMENT PRIMARY KEY,
    regid INT,
    totalquestion INT,
    correctquestion INT,
    wrongquestion INT,
    totalmarks INT,
    obtainmarks INT,
    per DECIMAL(5,2),
    status VARCHAR(20),
    noofattempt INT,
    resultdate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (regid) REFERENCES registration(regid)
);

INSERT IGNORE INTO questions (questid, question, answerkey) VALUES
(1, 'Which SQL keyword is used to get data from a table?', 'A'),
(2, 'Which SQL keyword adds a new row to a table?', 'B'),
(3, 'Which SQL keyword removes a row from a table?', 'C'),
(4, 'Which SQL keyword changes existing data in a table?', 'A'),
(5, 'Which SQL keyword creates a new table?', 'B'),
(6, 'Which SQL keyword is used to filter results?', 'C'),
(7, 'Which SQL keyword sorts the results?', 'A'),
(8, 'Which SQL keyword deletes an entire table?', 'B'),
(9, 'How do you write a comment in Python?', 'C'),
(10, 'Which keyword is used to create a function in Python?', 'A'),
(11, 'Which function is used to print something in Python?', 'B'),
(12, 'What is used to store True or False in Python?', 'C'),
(13, 'Which symbol is used for multiplication in Python?', 'A'),
(14, 'Which symbol is used for division in Python?', 'B'),
(15, 'What do you call a group of code inside a function?', 'C'),
(16, 'Which data type stores whole numbers in Python?', 'A'),
(17, 'Which data type stores decimal numbers in Python?', 'B'),
(18, 'Which loop repeats code a fixed number of times?', 'C'),
(19, 'What is used to store text in Python?', 'A'),
(20, 'What symbol ends a line of code in most languages, but not Python?', 'B');

INSERT IGNORE INTO answers (questid, answerid, answer) VALUES
(1, 1, 'A) SELECT'), (1, 2, 'B) GET'), (1, 3, 'C) OPEN'),
(2, 4, 'A) NEW'), (2, 5, 'B) INSERT'), (2, 6, 'C) CREATE'),
(3, 7, 'A) REMOVE'), (3, 8, 'B) CLEAR'), (3, 9, 'C) DELETE'),
(4, 10, 'A) UPDATE'), (4, 11, 'B) CHANGE'), (4, 12, 'C) EDIT'),
(5, 13, 'A) MAKE TABLE'), (5, 14, 'B) CREATE TABLE'), (5, 15, 'C) NEW TABLE'),
(6, 16, 'A) SORT'), (6, 17, 'B) FIND'), (6, 18, 'C) WHERE'),
(7, 19, 'A) ORDER BY'), (7, 20, 'B) SORT BY'), (7, 21, 'C) ARRANGE'),
(8, 22, 'A) REMOVE TABLE'), (8, 23, 'B) DROP TABLE'), (8, 24, 'C) DELETE TABLE'),
(9, 25, 'A) // comment'), (9, 26, 'B) -- comment'), (9, 27, 'C) # comment'),
(10, 28, 'A) def'), (10, 29, 'B) function'), (10, 30, 'C) create'),
(11, 31, 'A) show()'), (11, 32, 'B) print()'), (11, 33, 'C) display()'),
(12, 34, 'A) int'), (12, 35, 'B) str'), (12, 36, 'C) bool'),
(13, 37, 'A) *'), (13, 38, 'B) x'), (13, 39, 'C) times'),
(14, 40, 'A) //'), (14, 41, 'B) /'), (14, 42, 'C) div'),
(15, 43, 'A) module'), (15, 44, 'B) loop'), (15, 45, 'C) block'),
(16, 46, 'A) int'), (16, 47, 'B) float'), (16, 48, 'C) str'),
(17, 49, 'A) int'), (17, 50, 'B) float'), (17, 51, 'C) str'),
(18, 52, 'A) while'), (18, 53, 'B) if'), (18, 54, 'C) for'),
(19, 55, 'A) string'), (19, 56, 'B) number'), (19, 57, 'C) boolean'),
(20, 58, 'A) colon'), (20, 59, 'B) semicolon'), (20, 60, 'C) period');
