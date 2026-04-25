############################################# IMPORTING ################################################

import tkinter as tk

from tkinter import ttk

from tkinter import messagebox as mess

import tkinter.simpledialog as tsd

import cv2, os

import csv

import numpy as np

from PIL import Image, ImageTk

import pandas as pd

import datetime

import time

import multiprocessing

import threading


############################################# THEME SETTINGS ################################################

# Adjusted theme for improved spacing and layout

theme = {

    "window_bg": "#2C3E50",         # Dark blue-grey

    "frame_bg": "#34495E",          # Slightly lighter blue-grey

    "title_fg": "#ECF0F1",          # Very light gray/white

    "title_font": ('Courier', 28, 'bold'),  # Reduced font size for title

    "new_reg_header_bg": "#1ABC9C", # Turquoise

    "new_reg_header_fg": "white",

    "reg_header_bg": "#F1C40F",     # Yellow

    "reg_header_fg": "black",

    "label_bg": "#34495E",

    "label_fg": "white",

    "status_bg": "#2C3E50",

    "status_fg": "white",

    "btn_clear_bg": "#E67E22",      # Orange

    "btn_take_img_bg": "#3498DB",   # Blue

    "btn_save_profile_bg": "#1ABC9C",  # Turquoise

    "btn_take_att_bg": "#F1C40F",   # Yellow

    "btn_reload_att_bg": "#27AE60", # Green

    "btn_quit_bg": "#E74C3C"        # Red

}


############################################# FUNCTIONS ################################################


def tick():
    try:
        time_string = time.strftime('%H:%M:%S')
        clock.configure(text=time_string)
        clock.after(200, tick)
    except:
        return
    
def assure_path_exists(path):

    d = os.path.dirname(path)

    if not os.path.exists(d):

        os.makedirs(d)




def TakeImages():
    try:
        Id = txt.get()
        name = txt2.get()
    except:
        print("UI not available")
        return

    if not Id.isnumeric() or not name.isalpha():
        mess.showerror("Error", "Enter numeric ID and alphabetic Name")
        return


    assure_path_exists("TrainingImage/")
    assure_path_exists("StudentDetails/")

    details_file = "StudentDetails/StudentDetails.csv"

    if not os.path.exists(details_file):
        with open(details_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["SERIAL NO.", "ID", "NAME"])
        serial = 1
    else:
        with open(details_file, "r") as f:
            serial = len(f.readlines())

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    sampleNum = 0

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg",
                        gray[y:y+h, x:x+w])

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Taking Images', img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum > 60:
            break

    cam.release()
    cv2.destroyAllWindows()

    with open(details_file, "a+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([serial, Id, name])

    try:
        window.after(0, lambda: message1.configure(
            text=f"Images Taken for ID : {Id}, Name : {name}"
    ))
    except:
        pass


def clear():

    txt.delete(0, 'end')

    message1.configure(text="1) Take Images  >>>  2) Save Profile")


def clear2():

    txt2.delete(0, 'end')

    message1.configure(text="1) Take Images  >>>  2) Save Profile")


def contact():

    mess._show(title='Contact us', message="Please contact us on : 'rohitvmore.work@gmail.com'")


def save_pass():

    assure_path_exists("TrainingImageLabel/")

    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")

    if exists1:

        tf = open("TrainingImageLabel\psd.txt", "r")

        key = tf.read()

    else:

        master.destroy()

        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')

        if new_pas == None:

            mess._show(title='No Password Entered', message='Password not set!! Please try again')

        else:

            tf = open("TrainingImageLabel\psd.txt", "w")

            tf.write(new_pas)

            mess._show(title='Password Registered', message='New password was registered successfully!!')

            return

    op = (old.get())

    newp= (new.get())

    nnewp = (nnew.get())

    if (op == key):

        if(newp == nnewp):

            txf = open("TrainingImageLabel\psd.txt", "w")

            txf.write(newp)

        else:

            mess._show(title='Error', message='Confirm new password again!!!')

            return

    else:

        mess._show(title='Wrong Password', message='Please enter correct old password.')

        return

    mess._show(title='Password Changed', message='Password changed successfully!!')

    master.destroy()



def change_pass():

    global master

    master = tk.Tk()

    master.geometry("400x160")

    master.resizable(False,False)

    master.title("Change Password")

    master.configure(background="white")

    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))

    lbl4.place(x=10,y=10)

    global old

    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')

    old.place(x=180,y=10)

    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))

    lbl5.place(x=10, y=45)

    global new

    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')

    new.place(x=180, y=45)

    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))

    lbl6.place(x=10, y=80)

    global nnew

    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')

    nnew.place(x=180, y=80)

    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))

    cancel.place(x=200, y=120)

    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))

    save1.place(x=10, y=120)

    master.mainloop()



def TrainImages():

    

    assure_path_exists("TrainingImageLabel/")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces, IDs = getImagesAndLabels("TrainingImage")

    try:

        recognizer.train(faces, np.array(IDs))

    except Exception as e:

        mess._show(title='No Registrations', message='Please Register someone first!!!')

        return

    recognizer.save("TrainingImageLabel/Trainner.yml")

    res = "Profile Saved Successfully"

    message1.configure(text=res)

    message.configure(text='Total Registrations till now  : ' + str(len(IDs)))


def getImagesAndLabels(path):

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []

    Ids = []

    for imagePath in imagePaths:

        pilImage = Image.open(imagePath).convert('L')

        imageNp = np.array(pilImage, 'uint8')

        ID = int(os.path.split(imagePath)[-1].split(".")[1])

        faces.append(imageNp)

        Ids.append(ID)

    return faces, Ids


def psw():

    assure_path_exists("TrainingImageLabel/")

    password_file = os.path.join("TrainingImageLabel", "psd.txt")

    if os.path.isfile(password_file):

        with open(password_file, "r") as tf:

            key = tf.read()

    else:

        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')

        if new_pas is None:

            mess._show(title='No Password Entered', message='Password not set!! Please try again')

            return

        else:

            with open(password_file, "w") as tf:

                tf.write(new_pas)

            mess._show(title='Password Registered', message='New password was registered successfully!!')

            return

    password = tsd.askstring('Password', 'Enter Password', show='*')

    if password == key:

        TrainImages()

    elif password is None:

        pass

    else:

        mess._show(title='Wrong Password', message='You have entered wrong password')


def TrackImages():
    """
    Opens a separate cv2 window for attendance.
    Recognized faces are recorded in a CSV.
    Auto-stops after 30 seconds, 'q' press, or window close.
    """

    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    # Load recognizer
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except:
        mess.showerror("Error", "Install opencv-contrib-python")
        return

    train_file = os.path.join("TrainingImageLabel", "Trainner.yml")
    if not os.path.isfile(train_file):
        mess.showerror("Error", "Please click on Save Profile first!")
        return

    recognizer.read(train_file)

    # Load Haarcascade (FIXED PATH)
    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    if faceCascade.empty():
        mess.showerror("Error", "Failed to load Haarcascade")
        return

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Load student data
    student_file = os.path.join("StudentDetails", "StudentDetails.csv")
    if not os.path.isfile(student_file):
        mess.showerror("Error", "Student details missing!")
        cam.release()
        return

    df = pd.read_csv(student_file)
    df.columns = ["SERIAL NO.", "ID", "NAME"]

    attendance_file = f"Attendance/Attendance_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv"
    existing_records = set()

    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as file:
            existing_records = {line.split(",")[0] for line in file}

    start_time = time.time()

    while True:
        ret, im = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)

            try:
                serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
            except:
                continue

            if conf < 50:
                try:
                    student_id = str(df.loc[df['SERIAL NO.'] == serial]['ID'].values[0])
                    student_name = str(df.loc[df['SERIAL NO.'] == serial]['NAME'].values[0])
                except:
                    student_id = "Unknown"
                    student_name = "Unknown"

                if student_id not in existing_records:
                    existing_records.add(student_id)

                    with open(attendance_file, 'a+', newline='') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow([
                            student_id, '', student_name, '',
                            datetime.datetime.now().strftime('%d-%m-%Y'), '',
                            datetime.datetime.now().strftime('%H:%M:%S')
                        ])
            else:
                student_name = "Unknown"

            display_text = student_name if student_name != "Unknown" else "Unknown"
            cv2.putText(im, display_text, (x, y+h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        # 🔥 EXIT CONDITIONS

        # 1. Press 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 2. If OpenCV window closed manually
        if cv2.getWindowProperty('Taking Attendance', cv2.WND_PROP_VISIBLE) < 1:
            break

        # 3. If Tkinter window closed
        try:
            if not window.winfo_exists():
                break
        except:
            break

        # 4. Auto-stop after 30 seconds
        if time.time() - start_time > 30:
            break

    cam.release()
    cv2.destroyAllWindows()

def reload_attendance():

    """

    Reload today's attendance records into the TreeView.

    """

    tv.delete(*tv.get_children())

    attendance_file = f"Attendance/Attendance_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv"

    if os.path.isfile(attendance_file):

        with open(attendance_file, 'r') as csvfile:

            reader = csv.reader(csvfile)

            for row in reader:

                if len(row) >= 7:

                    tv.insert('', 'end', text=row[0], values=(row[2], row[4], row[6]))

    else:

        mess._show(title='No Attendance', message='No attendance records found for today.')


def start_TrackImages():
    threading.Thread(target=TrackImages, daemon=True).start()
    

def clear_data():

    # Ask for password first

    pw = tsd.askstring("Password", "Enter password to clear student data:", show="*")

    if pw is None:

        return

    # Read the password from "psd.txt"

    try:

        with open("TrainingImageLabel/psd.txt", "r") as f:

            stored_pw = f.read().strip()

    except Exception as e:

        mess.showerror("Error", "Password file not found!")

        return

    if pw != stored_pw:

        mess.showerror("Error", "Incorrect password!")

        return

    # If password is correct, clear the StudentDetails CSV file by writing just the header row

    details_file = "StudentDetails/StudentDetails.csv"

    with open(details_file, "w", newline='') as f:

        writer = csv.writer(f)

        writer.writerow(["SERIAL NO.", "ID", "NAME"])

    mess.showinfo("Data Cleared", "All student data has been cleared.")



##################################################################################

######################################## USED STUFFS ############################################

global key

key = ''


ts = time.time()

date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

day, month, year = date.split("-")


mont = {

    '01': 'January', '02': 'February', '03': 'March', '04': 'April',

    '05': 'May', '06': 'June', '07': 'July', '08': 'August',

    '09': 'September', '10': 'October', '11': 'November', '12': 'December'

}


# Global variable to hold the attendance process handle

attendance_process = None


##################################################################################

######################################## MAIN GUI CODE ###########################################

if __name__ == '__main__':

    multiprocessing.freeze_support()

    def on_closing():
        try:
            window.destroy()
        except:
            pass
        

    window = tk.Tk()


    window.geometry("1280x800")

    window.resizable(True, True)

    window.title("Attendance System")

    window.configure(background=theme["window_bg"])

    

    window.protocol("WM_DELETE_WINDOW", on_closing)

    

    frame1 = tk.Frame(window, bg=theme["frame_bg"])

    frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

    

    

    frame2 = tk.Frame(window, bg=theme["frame_bg"])

    frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

    

    message3 = tk.Label(window, text="FaceTrack", fg=theme["title_fg"], bg=theme["window_bg"],

                        width=55, height=1, font=theme["title_font"])

    message3.place(relx=0.5, y=20, anchor="n")

    

    frame3 = tk.Frame(window, bg=theme["window_bg"])

    frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

    

    frame4 = tk.Frame(window, bg=theme["window_bg"])

    frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

    

    datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "   | ",

                    fg=theme["title_fg"], bg=theme["window_bg"],

                    width=55, height=1, font=('comic',19, 'bold'))

    datef.pack(fill='both', expand=1)

    

    clock = tk.Label(frame3, fg=theme["title_fg"], bg=theme["window_bg"],

                    width=55, height=1, font=('comic', 19, ' bold '))

    clock.pack(fill='both', expand=True)

    tick()

    

    head2 = tk.Label(frame2, text="                       For New Registrations                       ",

    fg="white", bg=theme["new_reg_header_bg"], font=('Helvetica', 17, ' bold '))

    head2.grid(row=1, column=2)

    

    head1 = tk.Label(frame1, text="                       For Already Registered                       ",

    fg="white", bg=theme["reg_header_bg"], font=('Helvetica', 17, ' bold '))

    head1.place(x=0, y=1)

    

    lbl = tk.Label(frame2, text="Enter ID", width=20, height=1,

                    fg="white", bg=theme["frame_bg"], font=('times', 17, ' bold '))

    lbl.place(x=80, y=55)

    

    txt = tk.Entry(frame2, width=29, fg="black", font=('times', 15, ' bold '))

    txt.place(x=30, y=88)

    

    lbl2 = tk.Label(frame2, text="Enter Name", width=20,

                    fg="white", bg=theme["frame_bg"], font=('times', 17, ' bold '))

    lbl2.place(x=80, y=140)

    

    txt2 = tk.Entry(frame2, width=29, fg="black", font=('times', 15, ' bold '))

    txt2.place(x=30, y=173)

    

    message1 = tk.Label(frame2, text="1)Take Images     2)Save Profile",

                        bg=theme["window_bg"], fg="white", width=39, height=1,

                        activebackground="yellow", font=('Georgia', 13, ' bold '))

    message1.place(x=7, y=230)

    

    message = tk.Label(frame2, text="",

                    bg=theme["window_bg"], fg="white", width=39, height=1,

                    activebackground="yellow", font=('times', 16, ' bold '))

    message.place(x=7, y=450)

    

    lbl3 = tk.Label(frame1, text="Attendance", width=20,

                    fg="white", bg=theme["frame_bg"], height=1, font=('times', 17, ' bold '))

    lbl3.place(x=100, y=115)

    

    res = 0

    exists = os.path.isfile("StudentDetails/StudentDetails.csv")

    if exists:

        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:

            reader1 = csv.reader(csvFile1)

            for l in reader1:

                res = res + 1

        # If only header exists, set count to 0; otherwise, use your formula.

        if res <= 1:

            res = 0

        else:

            res = (res // 2) - 1

    else:

        res = 0

    message.configure(text='Total Registrations till now  : ' + str(res))



    

    

    menubar = tk.Menu(window, relief='ridge')

    filemenu = tk.Menu(menubar, tearoff=0)

    filemenu.add_command(label='Change Password', command=change_pass)

    filemenu.add_command(label='Contact Us', command=contact)

    filemenu.add_command(label='Exit', command=on_closing)

    menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu)

    

    tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))

    tv.column('#0', width=82)

    tv.column('name', width=130)

    tv.column('date', width=133)

    tv.column('time', width=133)

    tv.grid(row=2, column=0, sticky="nsew", padx=(0, 1), pady=(150, 0), columnspan=4)

    tv.heading('#0', text='ID')

    tv.heading('name', text='NAME')

    tv.heading('date', text='DATE')

    tv.heading('time', text='TIME')

    

    scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)

    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')

    tv.configure(yscrollcommand=scroll.set)

    

    clearButton = tk.Button(frame2, text="Clear", command=clear,

                        fg="white", bg=theme["btn_clear_bg"], width=11,

                        activebackground="white", font=('Arial', 11, ' bold '))

    clearButton.place(x=335, y=86)


    

    clearButton2 = tk.Button(frame2, text="Clear", command=clear2,

                        fg="white", bg=theme["btn_clear_bg"], width=11,

                        activebackground="white", font=('Arial', 11, ' bold '))

    clearButton2.place(x=335, y=172)

    

    takeImg = tk.Button(frame2, text="Take Images", command=TakeImages,

                        fg="white", bg=theme["btn_take_img_bg"], width=34, height=1,

                        activebackground="white", font=('comic', 15, ' bold '))

    takeImg.place(x=30, y=300)

    

    trainImg = tk.Button(frame2, text="Save Profile", command=psw,

                        fg="white", bg=theme["btn_save_profile_bg"], width=34, height=1,

                        activebackground="white", font=('comic', 15, ' bold '))

    trainImg.place(x=30, y=380)


    clear_data_btn = tk.Button(frame2, text="Clear Data", command=clear_data,

                        fg="white", bg=theme["btn_clear_bg"], width=34, height=1, font=('times', 15, 'bold'))

    clear_data_btn.place(x=30, y=500)

    

    start_TrackImages_btn = tk.Button(frame1, text="Take Attendance",

                                command=start_TrackImages,

                                fg="black", bg=theme["btn_take_att_bg"], width=35, height=1,

                                activebackground="white", font=('times', 15, ' bold '))

    start_TrackImages_btn.place(x=35, y=50)

    

    reload_btn = tk.Button(frame1, text="Reload Attendance", command=reload_attendance,

                        fg="white", bg=theme["btn_reload_att_bg"], width=35, height=1,

                        activebackground="white", font=('comic;', 15, ' bold '))

    reload_btn.place(x=30, y=450)

    

    quitWindow = tk.Button(frame1, text="Quit", command=on_closing,

                        fg="white", bg=theme["btn_quit_bg"], width=35, height=1,

                        activebackground="white", font=('comic', 15, ' bold '))

    quitWindow.place(x=30, y=500)

    

    window.configure(menu=menubar)

    window.mainloop()