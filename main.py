import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageDraw, ImageFont
import re
import random
import sqlite3
import os
import win32api
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_email

window = tk.Tk()
window.geometry('600x600')
window.title("Student Management and Registration System")

bg_color = '#273b7a'

#Icons
login_stud_icon = tk.PhotoImage(file='Images/login_student_img.png')
login_admin_icon = tk.PhotoImage(file='Images/admin_img.png')
add_stud_icon = tk.PhotoImage(file='Images/add_student_img.png')
locked_icon = tk.PhotoImage(file='Images/locked.png')
unlocked_icon = tk.PhotoImage(file='Images/unlocked.png')
add_student_pic_icon = tk.PhotoImage(file='Images/add_image.png')


def init_database():
    if os.path.exists('students_accounts.db'):
        connection = sqlite3.connect('students_accounts.db')

        cursor = connection.cursor()

        cursor.execute("""  
                SELECT * FROM data
                """)

        connection.commit()
        print(cursor.fetchall())
        connection.close()


    else:
        connection = sqlite3.connect('students_accounts.db')

        cursor = connection.cursor()

        cursor.execute("""  
        CREATE TABLE data(
        id_number text,
        password text,
        name text,
        age text,
        gender text,
        phone_number text,
        class text,
        email text,
        image blob
        )
        """)

        connection.commit()
        connection.close()


def check_id_already_exists(id_number):
    connection = sqlite3.connect('students_accounts.db')

    cursor = connection.cursor()

    cursor.execute(f"""  
                SELECT id_number from data where id_number == '{id_number}'
                """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response


def check_valid_password(id_number,password):
    connection = sqlite3.connect('students_accounts.db')

    cursor = connection.cursor()

    cursor.execute(f"""  
                SELECT id_number from data where id_number == '{id_number}' AND password == '{password}'
                """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response


def add_data(id_number, password, name,age,gender,phone_number, student_class, email, pic_data):
    connection = sqlite3.connect('students_accounts.db')

    cursor = connection.cursor()

    cursor.execute(f"""  
            INSERT INTO data VALUES('{id_number}','{password}','{name}',
            '{age}','{gender}','{phone_number}','{student_class}','{email}',?)
            """,[pic_data])

    connection.commit()
    connection.close()


def confirmation_box(message):

    answer = tk.BooleanVar()
    answer.set(False)

    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()

    confirmation_box_fm = tk.Frame(window, highlightbackground=bg_color,
                                   highlightthickness=3)

    message_lb = tk.Label(confirmation_box_fm, text=message, font=('Bold',15))
    message_lb.pack(pady=20)

    cancel_btn = tk.Button(confirmation_box_fm,text='Cancel', font=('Bold',15),bd=0, bg=bg_color, fg='white',
                           command=lambda: action(False))
    cancel_btn.place(x=50,y=140)

    yes_btn = tk.Button(confirmation_box_fm, text='Yes', font=('Bold', 15), bd=0, bg=bg_color, fg='white',
                        command=lambda: action(True))
    yes_btn.place(x=190, y=140,width=80)

    confirmation_box_fm.place(x=160, y=120, width=320, height=220)

    window.wait_window(confirmation_box_fm)
    return answer.get()

def message_box(message):
    message_box_fm = tk.Frame(window, highlightbackground=bg_color,
                                   highlightthickness=3)

    close_btn = tk.Button(message_box_fm, text='X', bd=0, font=('bold',13),
                          fg=bg_color,command=lambda :message_box_fm.destroy())
    close_btn.place(x=290, y=5)

    message_lb = tk.Label(message_box_fm, text=message,font=('bold',15))
    message_lb.pack(pady=50)

    message_box_fm.place(x=160, y=120, width=320, height=220)

def draw_student_card(student_pic_path, student_data):
    labels = """
ID Number:
Name:
Gender:
Age:
Class:
Contact:
Email:    
"""

    student_card = Image.open('Images/student_card_frame.png')
    pic = Image.open(student_pic_path).resize((100, 100))

    student_card.paste(pic,(15,25))

    draw = ImageDraw.Draw(student_card)
    heading_font = ImageFont.truetype('bahnschrift',18)
    labels_font = ImageFont.truetype('arial', 15)
    data_font = ImageFont.truetype('bahnschrift', 12)

    draw.text(xy=(150,60),text='Student Card',fill=(0,0,0),font=heading_font)

    draw.multiline_text(xy=(15,120),text=labels, fill=(0,0,0),
                        font=labels_font,spacing=6)

    draw.multiline_text(xy=(95,123),text=student_data,fill=(0,0,0),
                        font=data_font,spacing=10)

    return student_card

def student_card_page(student_card_obj):

    def save_student_card():
        path = askdirectory()

        if path:
            student_card_obj.save(f'{path}/student_card.png')

    def print_student_card():
        path = askdirectory()

        if path:
            student_card_obj.save(f'{path}/student_card.png')
            win32api.ShellExecute(0, 'print', f'{path}/student_card.png',None,'.',0)

    def close_page():
        student_card_page_fm.destroy()
        window.update()
        student_login_page()

    student_card_img = ImageTk.PhotoImage(student_card_obj)

    student_card_page_fm = tk.Frame(window,highlightbackground=bg_color,highlightthickness=3)

    heading_lb = tk.Label(student_card_page_fm,text='Student Card',bg=bg_color,fg='white', font=('Bold',18))
    heading_lb.place(x=0,y=0,width=400)

    close_btn = tk.Button(student_card_page_fm, text='X', bg=bg_color,
                          fg='white', font=('Bold',13), bd=0,
                          command=close_page)
    close_btn.place(x=370,y=0)

    #card_img = ImageTk.PhotoImage(Image.open('Card.png'))


    student_card_lb = tk.Label(student_card_page_fm,image=student_card_img)
    student_card_lb.place(x=50, y=50)

    student_card_lb.image = student_card_img

    save_student_card_btn = tk.Button(student_card_page_fm, text='Save Student Card',
                                      bg=bg_color, fg='white', font=('Bold',15),
                                      bd=1,command=save_student_card)
    save_student_card_btn.place(x=80, y=375)

    print_student_card_btn = tk.Button(student_card_page_fm, text='    🖨️',
                                      bg=bg_color, fg='white', font=('Bold', 18),
                                      bd=1,width=3,command=print_student_card)
    print_student_card_btn.place(x=270, y=370)

    student_card_page_fm.place(x=50, y=30, width=400, height=450)


def welcome_page():

    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        window.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        window.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        window.update()
        create_account_page()

    #welcome page
    welcome_page_fm = tk.Frame(window,highlightbackground=bg_color,highlightthickness=3)

    #heading
    heading_lb = tk.Label(welcome_page_fm,text = 'Welcome To Student Registration\n and Management System',
                      bg=bg_color,fg='white',font=('Bold',18))

    heading_lb.place(x=0, y=0, width=450)

    #Buttons
    student_login_btn = tk.Button(welcome_page_fm, text='Login Student',bg = bg_color,
                              fg = 'white',font=('Bold',15),bd=0,command=forward_to_student_login_page)
    student_login_btn.place(x=120, y=125, width=200)

    student_login_img = tk.Button(welcome_page_fm, image=login_stud_icon,bd=0)
    student_login_img.place(x=60, y=100)

    admin_login_btn = tk.Button(welcome_page_fm, text='Login Admin',bg = bg_color,
                              fg = 'white',font=('Bold',15),bd=0,command=forward_to_admin_login_page)
    admin_login_btn.place(x=120, y=225, width=200)

    admin_login_img = tk.Button(welcome_page_fm, image=login_admin_icon,bd=0)
    admin_login_img.place(x=60, y=200)

    add_stud_btn = tk.Button(welcome_page_fm, text='Create Account',bg = bg_color,
                              fg = 'white',font=('Bold',15),bd=0,command=forward_to_add_account_page)
    add_stud_btn.place(x=120, y=325, width=200)

    add_stud_img = tk.Button(welcome_page_fm, image=add_stud_icon,bd=0)
    add_stud_img.place(x=60, y=300)


    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=450,height=500)

def sendmail_to_student(email,message,subject):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = my_email.email_address
    password = my_email.password

    msg = MIMEMultipart()

    msg['Subject']=subject
    msg['From']=username
    msg['To']=email

    msg.attach(MIMEText(_text=message, _subtype='html'))

    smtp_connection = smtplib.SMTP(host=smtp_server, port=smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username, password=password)
    smtp_connection.sendmail(from_addr=username, to_addrs=email, msg=msg.as_string())
    print('Email Sent Successfully')



def forget_password_page():

    def recover_password():

        if check_id_already_exists(id_number=student_id_ent.get()):
            connection = sqlite3.connect('Students_accounts.db')
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT password FROM data WHERE id_number=='{student_id_ent.get()}'
            """)
            connection.commit()
            recovered_password = cursor.fetchall()[0][0]
            cursor.execute(f"""
                       SELECT email FROM data WHERE id_number=='{student_id_ent.get()}'
                       """)
            connection.commit()
            student_email = cursor.fetchall()[0][0]
            connection.close()

            confirmation = confirmation_box(message=f"""We will Send\nYour Forgot Password
via Your Email Address:
{student_email}
Do You Want to Continue?""")
            if confirmation:
                msg = f"""<h1>Your Forgot Password is :</h1>
                <h2>{recovered_password}</h2>
                <p>Once Remember Your Password, After Delete This Message</p>"""
                sendmail_to_student(email=student_email, message=msg,subject='Password Recovery')

        else:
            print('Incorrect ID')
            message_box(message='Invalid ID Number')


    forget_password_page_fm = tk.Frame(window, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(forget_password_page_fm, text='⚠️ Forgetting Password', font=('Bold',15),
                          bg = bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=350)

    close_btn = tk.Button(forget_password_page_fm, text='X',
                          font=('Bold',13),bg=bg_color,fg='white',
                          bd=0,command=lambda : forget_password_page_fm.destroy())
    close_btn.place(x=320,y=0)

    student_id_lb = tk.Label(forget_password_page_fm, text='Enter Student ID Number',
                             font=('Bold',13))
    student_id_lb.place(x=70,y=40)

    student_id_ent = tk.Entry(forget_password_page_fm,font=('Bold',15), justify=tk.CENTER)
    student_id_ent.place(x=70, y=70, width=180)

    info_lb = tk.Label(forget_password_page_fm,
                       text="""Via Your Email Address 
We will Send to You
Your Forget Password.""",justify=tk.LEFT)
    info_lb.place(x=75, y=110)

    next_btn = tk.Button(forget_password_page_fm,
                         text='Next', font=('Bold',13), bg=bg_color,
                         fg='white',command=recover_password)
    next_btn.place(x=130, y=200, width=80)

    forget_password_page_fm.place(x=75, y=120, width=350,height=250)


def student_login_page():

    def show_hide_password():
        if passwoed_ent['show']=='*':
            passwoed_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:
            passwoed_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        window.update()
        welcome_page()

    def forward_to_forget_password_page():
        forget_password_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'grey':
            if entry.get() != '':
                entry.config(highlightcolor=bg_color, highlightbackground='grey')



    def login_account():
        verify_id_number = check_id_already_exists(id_number=id_number_ent.get())
        if verify_id_number:
            print('ID is Correct')

            verify_password = check_valid_password(id_number=id_number_ent.get(),
                                                   password=passwoed_ent.get())

            if verify_password:
                print('password is correct')
            else:
                print('oops! password is Incorrect')
                passwoed_ent.config(highlightcolor='red', highlightbackground='red')
                message_box(message='Incorrect Password')



        else:
            print('oops! ID is Incorrect')
            id_number_ent.config(highlightcolor='red', highlightbackground ='red')
            message_box(message='Please Enter Valid Student ID')


    student_login_page_fm = tk.Frame(window, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(student_login_page_fm,text = 'Student Login Page',
              bg=bg_color,fg='white',font=('Bold',18))
    heading_lb.place(x=0, y=0, width=450)

    back_btn = tk.Button(student_login_page_fm, text='←',font=('Bold',20),fg=bg_color,bd=0,command=forward_to_welcome_page)
    back_btn.place(x=8, y=40)

    student_login_img = tk.Button(student_login_page_fm, image=login_stud_icon, bd=0)
    student_login_img.place(x=180, y=70)

    id_number_lb = tk.Label(student_login_page_fm, text= 'Enter Student ID Number',font=('Bold',15),fg = bg_color)
    id_number_lb.place(x=110, y=180)

    id_number_ent = tk.Entry(student_login_page_fm, font=('Bold',15), justify=tk.CENTER, highlightcolor=bg_color,
                 highlightbackground='grey',highlightthickness=2)
    id_number_ent.place(x=110, y = 230)
    id_number_ent.bind('<KeyRelease>', lambda e:remove_highlight_warning(entry=id_number_ent))


    password_lb = tk.Label(student_login_page_fm, text= 'Enter Student Password',font=('Bold',15),fg = bg_color)
    password_lb.place(x=110, y=280)

    passwoed_ent = tk.Entry(student_login_page_fm, font=('Bold',15), justify=tk.CENTER, highlightcolor=bg_color,
                 highlightbackground='grey',highlightthickness=2, show='*')
    passwoed_ent.place(x=110, y = 330)
    passwoed_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=passwoed_ent))


    show_hide_btn = tk.Button(student_login_page_fm,image=locked_icon, bd=0,
                  command=show_hide_password)
    show_hide_btn.place(x=340, y=320)

    login_btn = tk.Button(student_login_page_fm, text='Login',bg = bg_color,
                      fg = 'white',font=('Bold',15),bd=0,command=login_account)
    login_btn.place(x=110, y=390, width=230)

    forget_password_btn = tk.Button(student_login_page_fm, text='⚠\nForget  Password',fg=bg_color, bd=0,
                                    command=forward_to_forget_password_page)
    forget_password_btn.place(x = 180, y = 430)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=450, height=500)



def admin_login_page():
    def show_hide_password():
        if passwoed_ent['show']=='*':
            passwoed_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:
            passwoed_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        welcome_page()

    admin_login_page_fm = tk.Frame(window, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(admin_login_page_fm,text = 'Admin Login Page',
              bg=bg_color,fg='white',font=('Bold',18))
    heading_lb.place(x=0, y=0, width=450)

    back_btn = tk.Button(admin_login_page_fm, text='←', font=('Bold', 20), fg=bg_color, bd=0,command=forward_to_welcome_page)
    back_btn.place(x=8, y=40)

    admin_login_img = tk.Button(admin_login_page_fm, image=login_admin_icon, bd=0)
    admin_login_img.place(x=180, y=70)

    username_lb = tk.Label(admin_login_page_fm, text= 'Enter Admin User Name',font=('Bold',15),fg = bg_color)
    username_lb.place(x=110, y=180)

    username_ent = tk.Entry(admin_login_page_fm, font=('Bold',15), justify=tk.CENTER, highlightcolor=bg_color,
                 highlightbackground='grey',highlightthickness=2)
    username_ent.place(x=110, y = 230)

    password_lb = tk.Label(admin_login_page_fm, text= 'Enter Admin Password',font=('Bold',15),fg = bg_color)
    password_lb.place(x=110, y=280)

    passwoed_ent = tk.Entry(admin_login_page_fm, font=('Bold',15), justify=tk.CENTER, highlightcolor=bg_color,
                 highlightbackground='grey',highlightthickness=2, show='*')
    passwoed_ent.place(x=110, y = 330)

    show_hide_btn = tk.Button(admin_login_page_fm,image=locked_icon, bd=0,
                  command=show_hide_password)
    show_hide_btn.place(x=340, y=320)

    login_btn = tk.Button(admin_login_page_fm, text='Login',bg = bg_color,
                      fg = 'white',font=('Bold',15),bd=0)
    login_btn.place(x=110, y=390, width=230)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=450, height=500)



student_gender = tk.StringVar()
class_list = ['1st Year','2nd Year','3rd Year','B.Tech']

def create_account_page():

    pic_path = tk.StringVar()
    pic_path.set('')

    def open_pic():
        path = askopenfilename()

        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            pic_path.set(path)
            add_pic_btn.config(image=img)
            add_pic_btn.image = img

    def forward_to_welcome_page():

        ans = confirmation_box(message="Do You Want To Leave\n Registration Foam?")

        if ans:
             add_account_page_fm.destroy()
             window.update()
             welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'grey':
            if entry.get() != '':
                entry.config(highlightcolor=bg_color, highlightbackground='grey')

    def check_invalid_email(email):

        pattern = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

        match = re.match(pattern=pattern, string=email)
        return match

    def generate_id_number():
        generated_id = ''

        for r in range(6):
            generated_id+=str(random.randint(0,9))


        if not check_id_already_exists(id_number=generated_id):

            student_id.config(state=tk.NORMAL)
            student_id.delete(0, tk.END)
            student_id.insert(tk.END,generated_id)
            student_id.config(state='readonly')

        else:
            generate_id_number()

    def check_input_validation():

        if student_name_ent.get() == '':
            student_name_ent.config(highlightcolor='red',highlightbackground='red')
            student_name_ent.focus()
            message_box(message='Student Full Name is Required')

        elif student_age_ent.get()== '':
            student_age_ent.config(highlightcolor='red', highlightbackground='red')
            student_age_ent.focus()
            message_box(message='Enter Student Age is Required')

        elif student_contact_ent.get()=='':
            student_contact_ent.config(highlightcolor='red', highlightbackground='red')
            student_contact_ent.focus()
            message_box(message='Student Contact Number is Required')

        elif select_class_btn.get()=='':
            select_class_btn.focus()
            message_box(message='Select Student Class is Required')

        elif student_email_ent.get()=='':
            student_email_ent.config(highlightcolor='red', highlightbackground='red')
            student_email_ent.focus()
            message_box(message='Student Email Address is Required')

        elif not check_invalid_email(email=student_email_ent.get().lower()):
            student_email_ent.config(highlightcolor='red', highlightbackground='red')
            student_email_ent.focus()
            message_box(message='Please Enter a Valid\nEmail Address')

        elif create_acpwd_ent.get()=='':
            create_acpwd_ent.config(highlightcolor='red', highlightbackground='red')
            create_acpwd_ent.focus()
            message_box(message='Create a Password is Required')

        else:

            pic_data = b''

            if pic_path.get() != '':
                resize_pic = Image.open(pic_path.get()).resize((100,100))
                resize_pic.save('temp_pic.png')

                read_data = open('temp_pic.png','rb')
                pic_data = read_data.read()
                read_data.close()

            else :
                read_data = open('Images/add_image.png', 'rb')
                pic_data = read_data.read()
                read_data.close()
                pic_path.set('Images/add_image.png')



            add_data(id_number=student_id.get(),password=create_acpwd_ent.get(),
                     name=student_name_ent.get(),age=student_age_ent.get(),
                     gender=student_gender.get(),phone_number=student_contact_ent.get(),
                     student_class=select_class_btn.get(),email=student_email_ent.get(),
                     pic_data=pic_data)


            data=f"""
{student_id.get()}
{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{select_class_btn.get()}
{student_contact_ent.get()}
{student_email_ent.get()}                    
"""

            get_student_card=draw_student_card(student_pic_path=pic_path.get(),
                              student_data=data)
            student_card_page(student_card_obj=get_student_card)

            add_account_page_fm.destroy()
            window.update()
            message_box('Account Successfully Created')

    add_account_page_fm = tk.Frame(window, highlightbackground=bg_color, highlightthickness=3)

    add_pic_section_fm = tk.Frame(add_account_page_fm, highlightbackground=bg_color, highlightthickness=3)

    add_pic_btn = tk.Button(add_pic_section_fm, image=add_student_pic_icon,bd=0,command=open_pic)
    add_pic_btn.pack()

    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    student_name_lb = tk.Label(add_account_page_fm,text='Enter Student Full Name',font=('Bold',12))
    student_name_lb.place(x=5,y=130)

    student_name_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='grey',highlightthickness=2)
    student_name_ent.place(x=5,y=160, width=180)
    student_name_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_name_ent))

    student_gender_lb = tk.Label(add_account_page_fm,text='Select Student Gender',font=('Bold',12))
    student_gender_lb.place(x=5,y=210)

    male_gender_btn = tk.Radiobutton(add_account_page_fm, text='Male',font=('Bold',12),variable=student_gender,value='male')
    male_gender_btn.place(x=5, y=235)

    female_gender_btn = tk.Radiobutton(add_account_page_fm, text='Female',font=('Bold',12),variable=student_gender,value='female')
    female_gender_btn.place(x=75, y=235)

    student_gender.set('male')

    student_age_lb = tk.Label(add_account_page_fm,text='Enter Student Age',font=('Bold',12))
    student_age_lb.place(x=5,y=275)

    student_age_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='grey',highlightthickness=2)
    student_age_ent.place(x=5,y=305, width=180)
    student_age_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_age_ent))

    student_contact_lb = tk.Label(add_account_page_fm,text='Enter Contact Number',font=('Bold',12))
    student_contact_lb.place(x=5,y=360)

    student_contact_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='grey',highlightthickness=2)
    student_contact_ent.place(x=5,y=390, width=180)
    student_contact_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_contact_ent))

    student_class_lb = tk.Label(add_account_page_fm,text='Select Student Class',font=('Bold',12))
    student_class_lb.place(x=5,y=445)

    select_class_btn = Combobox(add_account_page_fm, font=('Bold',15),state='readonly',values=class_list)
    select_class_btn.place(x=5,y=475,width=180,height=30)
    select_class_btn.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=select_class_btn))

    student_id_lb = tk.Label(add_account_page_fm, text='Student ID Number: ',font=('Bold',12))
    student_id_lb.place(x=240, y =35)

    student_id = tk.Entry(add_account_page_fm,font=('Bold',18))
    student_id.place(x=380, y=35, width=80)

    student_id.config(state='readonly')

    generate_id_number()

    id_info_lb = tk.Label(add_account_page_fm, text="""Automatically Generated ID Number
! Remember Using This ID Number 
Student Will Login Account""",justify=tk.LEFT)
    id_info_lb.place(x=240, y=65)

    student_email_lb = tk.Label(add_account_page_fm,text='Enter Student Email Address',font=('Bold',12))
    student_email_lb.place(x=240,y=130)

    student_email_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='grey',highlightthickness=2)
    student_email_ent.place(x=240,y=160, width=180)
    student_email_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_email_ent))

    email_info_lb = tk.Label(add_account_page_fm, text="""Via Email Address Student
Can Recover Account
! In Case Forgetting Password And Also 
Student Will get Further Notification""",justify=tk.LEFT)
    email_info_lb.place(x=240, y=200)

    create_acpwd_lb = tk.Label(add_account_page_fm,text='Create Account Password',font=('Bold',12))
    create_acpwd_lb.place(x=240,y=275)

    create_acpwd_ent = tk.Entry(add_account_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='grey',highlightthickness=2)
    create_acpwd_ent.place(x=240,y=305, width=180)
    create_acpwd_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=create_acpwd_ent))

    password_info_lb = tk.Label(add_account_page_fm, text="""Via Student Created Password
And Provided Student ID Number
Student Can Login Account.""",justify=tk.LEFT)
    password_info_lb.place(x=240, y=345)

    home_btn = tk.Button(add_account_page_fm, text='Home',font=('Bold',15),bg='red',fg='white',bd=0,command=forward_to_welcome_page)
    home_btn.place(x=240, y =420)

    submit_btn = tk.Button(add_account_page_fm, text='Submit',font=('Bold',15),bg=bg_color,fg='white',bd=0,command=check_input_validation)
    submit_btn.place(x=360, y =420)

    add_account_page_fm.pack(pady=30)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=480, height=580)

init_database()
welcome_page()
window.mainloop()