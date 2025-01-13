import tkinter as tk
from PIL import Image, ImageTk
import cv2
import datetime

rec = None
recording = None

background = cv2.createBackgroundSubtractorMOG2()

#Function for displaying the live feed and detecting motion
def show_frame():
    global rec, recording
    _, frame = cap.read()
    fgmask = background.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(fgmask, kernel, iterations=2)
    now = datetime.datetime.now()

    time = now.strftime("%H-%M-%S")
    date = now.strftime("%d-%m-%Y")
    time_label.configure(text=time)
    date_label.configure(text=date)

    contours = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    motion_detected = False
    #Loop for the contours
    for c in contours:
            if cv2.contourArea(c) > 5000:
                motion_detected = True
                status_label.configure(text="RECORDING - Motion Detected")
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #If motion is detected statement
    if motion_detected:
            #If it is not currently recording, it starts recording and writing the frames
            if not rec:
                vid_title = date+"--"+time+".avi"
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                recording = cv2.VideoWriter(vid_title, fourcc, 25.0, (640,480))
                rec = True
            recording.write(frame)
    #If no motion is detected
    else:
        #If it is currently recording, stop recording
        if rec:
            status_label.configure(text="")
            rec = False
            recording.release()
            recording = None
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

#Function for the Picture Button
def take_picture():
    _, frame = cap.read()
    now = datetime.datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%d-%m-%Y")
    img_title = date+"--"+time+".jpg"
    cv2.imwrite(img_title, frame)
    status_label.configure(text="Picture Taken")

#Function for the Exit Button
def exit_func():
    root.destroy()

#Define the root
root = tk.Tk()
root.title("CCTV Camera")
root.geometry("700x670")
root.configure(bg="grey")

#Define the labels and the buttons
time_label = tk.Label(root, font=("Helvetica", 12, "bold"), fg='red', bg="grey")
date_label = tk.Label(root, font=("Helvetica", 12, "bold"), fg='red', bg="grey")
status_label = tk.Label(root, font=("Helvetica", 12, "bold"), fg='red', bg='grey')
picture_Btn = tk.Button(root, text="Take Picture", command=take_picture, width=20, height=2)
exit_Btn = tk.Button(root, text="EXIT", fg='red', command=exit_func, width=20, height=2)

#Pack the created labels and on the root
time_label.pack()
date_label.pack()
lmain = tk.Label(root)
lmain.pack()
cap = cv2.VideoCapture(0)
status_label.pack()
picture_Btn.pack()
exit_Btn.pack()

show_frame()
root.mainloop()
