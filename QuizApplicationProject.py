import mysql.connector as dbconnector
import tkinter as tk
from PIL import Image, ImageTk
conn = dbconnector.connect(host= "localhost", user= "root", password = "my_password", database = "quizApp")
queryexe = conn.cursor()

frame = tk.Tk()
frame.geometry("800x800")
frame.config(bg="#2C3E50")
img = Image.open("mitt.png")
# img = img.resize((wid))  
photo = ImageTk.PhotoImage(img)  
image_label = tk.Label(frame, image=photo, bg="#2C3E50") 
image_label.place(x=1050, y=275) 

label1 = tk.Label(frame, text="Welcome to MIT Testing System", font=("Segoe UI", 33, "bold"), fg="white", bg="#2C3E50")
label1.place(x=295, y=300) 
label2 = tk.Label(frame, text="Login to your account", font=("Calibri", 24, "italic"), fg="white", bg="#2C3E50")
label2.place(x=295, y=370)
label3 = tk.Label(frame, text="Email:", font=("Calibri", 19), fg="white", bg="#2C3E50")
label3.place(x=295, y=450)
label4 = tk.Label(frame, text="Password:", font=("Calibri", 19), fg="white", bg="#2C3E50")
label4.place(x=295, y=500)

entry1 = tk.Entry(frame, font=("Calibri", 14))
entry1.place(x=450, y=450, height=28, width=240)
entry2 = tk.Entry(frame, show="•", font=("Calibri", 14)) 
entry2.place(x=450, y=500, height=28, width=240)

def check_login():
    email = entry1.get()
    password = entry2.get()
    query = "SELECT * FROM registration WHERE regemail= %s AND regpassword = %s"
    queryexe.execute(query, (email, password))
    row = queryexe.fetchone()
    if row:
        frame.withdraw()
        logged_in_id = row[0]
        logged_in_name = row[1]
        open_quiz_menu(logged_in_id, logged_in_name)
    else:
        label6 = tk.Label(frame, text="Invalid Email or Password!", font=20, fg="white", bg="red")
        label6.place(x=430, y=700, width=300)


def open_quiz_menu(logged_in_id, logged_in_name):
    quiz_frame = tk.Toplevel(frame)
    quiz_frame.geometry("800x800")
    quiz_frame.config(bg="#2C3E50")
    label17 = tk.Label(quiz_frame, text=f"Welcome, {logged_in_name}!", font=("Segoe UI", 45, "bold", "italic"), fg="white", bg="#2C3E50") 
    label17.place(x=738, y=300)

    attempt_query = "SELECT COUNT(*) FROM result WHERE regid = %s"
    queryexe.execute(attempt_query, (logged_in_id,))
    attempt_count = queryexe.fetchone()[0]

    if attempt_count >= 3:
        payment_label = tk.Label(quiz_frame, text="Payment Required to attempt the quiz again!", font=("Segoe UI", 20, "bold"), fg="white", bg="red")
        payment_label.place(x=710, y=420)
        return 

    label_ready = tk.Label(quiz_frame, text="Are you ready for the Quiz?", font=("Calibri", 23, "italic"), fg="white", bg="#2C3E50")
    label_ready.place(x=790, y=400) 


    def start_quiz():
        label17.destroy()
        label_ready.destroy()
        start_button.destroy()

        query = "SELECT * FROM questions"
        queryexe.execute(query)
        all_questions = queryexe.fetchall()

        query = "SELECT * FROM answers"
        queryexe.execute(query)
        all_answers = queryexe.fetchall()

        current_index = [0]
        selected_answers = {}
        selected_option = tk.StringVar()

        question_label = tk.Label(quiz_frame, text="", font=("Calibri", 20), fg="white", bg="#2C3E50", wraplength=600, justify="left")
        question_label.place(x=200, y=200)

        radio_buttons = []

        next_button = tk.Button(quiz_frame, text="Next", font=("Calibri", 16))
        next_button.place(x=650, y=550)

        def show_question():
            for r in radio_buttons:
                r.destroy()
            radio_buttons.clear()

            current_question = all_questions[current_index[0]]
            current_questid = current_question[0]

            matching_answer = []
            for ans in all_answers:
                if ans[0] == current_questid:
                    matching_answer.append(ans)

            question_label.config(text=f"{current_index[0]+1}. {current_question[1]}")

            selected_option.set("")

            if current_questid in selected_answers:
                selected_option.set(selected_answers[current_questid])

            for i, ans in enumerate(matching_answer):
                answer_text = ans[2]
                radio = tk.Radiobutton(
                    quiz_frame,
                    text=answer_text,
                    variable=selected_option,
                    value=answer_text,
                    font=("Calibri", 16),
                    fg="white",
                    bg="#2C3E50",
                    selectcolor="#2C3E50"
                )
                radio.place(x=220, y=280 + (i * 40))
                radio_buttons.append(radio)

            if current_index[0] == len(all_questions) - 1:
                next_button.config(text="Submit", command=finish_quiz)
            else:
                next_button.config(text="Next", command=go_next)

        def go_next():
            current_question = all_questions[current_index[0]]
            current_questid = current_question[0]
            if selected_option.get():
                selected_answers[current_questid] = selected_option.get()
            current_index[0] += 1
            show_question()

        def finish_quiz():
            current_question = all_questions[current_index[0]]
            current_questid = current_question[0]
            if selected_option.get():
                selected_answers[current_questid] = selected_option.get()

            correct = 0
            wrong = 0
            for q in all_questions:
                quesid = q[0]
                answerkey = q[2]
                student_answer = selected_answers.get(quesid, "")
                if student_answer.startswith(answerkey + ")"):
                    correct += 1
                else:
                    wrong += 1

            total = len(all_questions)
            percentage = round((correct / total) * 100, 2)
            status = "Pass" if percentage >= 40 else "Fail"

            insert_query = """INSERT INTO result 
                (regid, totalquestion, correctquestion, wrongquestion, totalmarks, obtainmarks, per, status, noofattempt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            queryexe.execute(insert_query, (logged_in_id, total, correct, wrong, total, correct, percentage, status, attempt_count + 1))
            conn.commit()

            for r in radio_buttons:
                r.destroy()
            next_button.destroy()
            question_label.destroy()

            result_label = tk.Label(quiz_frame, text=f"Quiz Finished!\nScore: {correct}/{total} ({percentage}%)\nStatus: {status}",
                                    font=("Calibri", 24, "bold"), fg="white", bg="#2C3E50", justify="center")
            result_label.place(relx=0.5, y=300, anchor="n")

        show_question()

    start_button = tk.Button(quiz_frame, text="Start Quiz", font=("Calibri", 19), width=10, command=start_quiz)
    start_button.place(x=920, y=498) 

def reg_window():
    reg_frame = tk.Toplevel()
    reg_frame.geometry("800x800")
    reg_frame.config(bg="#2C3E50")

    label7 = tk.Label(reg_frame, text="Registration Form", font=("Segoe UI", 35, "bold"), fg="white", bg="#2C3E50")
    label7.place(x=735, y=100)
    label14 = tk.Label(reg_frame, text="Let's create an Account to get started!", font=("Calibri", 20, "italic"), fg="gray", bg="#2C3E50")
    label14.place(x=714, y=180)

    label8 = tk.Label(reg_frame, text="First Name:", font=("Calibri", 23), fg="white", bg="#2C3E50")
    label8.place(x=615, y=300)
    entry3 = tk.Entry(reg_frame, font=("Calibri", 19))
    entry3.place(x=620, y=345, height=28, width=300)

    label9 = tk.Label(reg_frame, text="Last Name:", font=("Calibri", 23), fg="white", bg="#2C3E50")
    label9.place(x=1029, y=300)
    entry4 = tk.Entry(reg_frame, font=("Calibri", 19))
    entry4.place(x=1035, y=345, height=28, width=300)

    label10 = tk.Label(reg_frame, text="Mobile:", font=("Calibri", 23), fg="white", bg="#2C3E50")
    label10.place(x=615, y=400)
    entry5 = tk.Entry(reg_frame, font=("Calibri", 19))
    entry5.place(x=620, y=445, height=28, width=300)

    label11 = tk.Label(reg_frame, text="Email:", font=("Calibri", 23), fg="white", bg="#2C3E50")
    label11.place(x=1029, y=400)
    entry6 = tk.Entry(reg_frame, font=("Calibri", 19))
    entry6.place(x=1035, y=445, height=28, width=300)

    label12 = tk.Label(reg_frame, text="Password:", font=("Calibri", 23), fg="white", bg="#2C3E50")
    label12.place(x=615, y=500)
    entry7 = tk.Entry(reg_frame, font=("Calibri", 19), show="•")
    entry7.place(x=620, y=545, height=28, width=300) 

    def submit():
            fname = entry3.get()
            lname = entry4.get()
            mobile = entry5.get()
            email = entry6.get()
            password = entry7.get()
    
            query = "INSERT INTO registration (regfname, reglname, regmobile, regemail, regpassword) VALUES (%s, %s, %s, %s, %s)"
            queryexe.execute(query, (fname, lname, mobile, email, password))
            conn.commit()
    
            label16 = tk.Label(reg_frame, text="Registration Successfully done!", font=("Calibri", 21), fg="white", bg="#2C3E50")
            label16.place(x=767, y=800)

    button3 = tk.Button(reg_frame, text="Submit", font=("Calibri", 19), width=11, command=submit)
    button3.place(x=899, y=600)

    
button1 = tk.Button(frame, text="Login", font=("Calibri", 19), command=check_login)
button1.place(x=445, y=550) 
label5 = tk.Label(frame, text="No Account? ➤", font=("Calibri", 15), fg="white", bg="#2C3E50")
label5.place(x=295, y=630)
button2 = tk.Button(frame, text="Register", font=("Calibri", 19), width=10, command=reg_window)
button2.place(x=445, y=620)





def check_reg():
    query = "SELECT * FROM registration"
    queryexe.execute(query) 


frame.mainloop()
queryexe.close()
conn.close()

