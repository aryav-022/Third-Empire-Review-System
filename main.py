from threading import Thread, Timer
from random import randint
from tkinter import *
import cv2
from PIL import Image, ImageTk
from functools import partial


def show(speed):
    global frameNumber, timer
    
    if speed > 0:
        if frameNumber == numberOfFrames - 1:
            return
    else:
        if frameNumber == 0:
            return
        
    cv2image = cv2.cvtColor(frame_list[frameNumber], cv2.COLOR_BGR2RGBA)

    if speed > 0:
        frameNumber = scale.get() + 1
        scale.set(frameNumber)
    else:
        frameNumber = scale.get() - 1
        scale.set(frameNumber)
    
    img = Image.fromarray(cv2image).resize((700, 500))
    imgtk = ImageTk.PhotoImage(img)
    mainScreen.imgtk = imgtk
    mainScreen.config(image=imgtk)
    timer = mainScreen.after(abs(speed), show, speed)


def pause():
    global timer
    mainScreen.after_cancel(timer)
    mainScreen.after_cancel(timer)
    mainScreen.after_cancel(timer)


def change_speed(speed):
    pause()
    # Calling show function with new speed
    show(speed)


def pending(out):
    pause()
    
    def decision():
        if out:
            im = ImageTk.PhotoImage(image=Image.open("out.png"))
        else:
            im = ImageTk.PhotoImage(image=Image.open("not_out.png"))
            
        mainScreen.imtk = im
        mainScreen.config(image=im)
        
    im = ImageTk.PhotoImage(image=Image.open("pending.png"))
    mainScreen.imtk = im
    mainScreen.config(image=im)
    
    Timer(randint(1, 3), decision).start()


# Creating a video object
cap = cv2.VideoCapture("clip.mp4")

# cap.read() returns a tuple. First element tells if there is image and second is the actual image
check, vid = cap.read()

# Creating a list which will contain all frames
frame_list = []

while check:
    check, vid = cap.read()
    frame_list.append(vid)
    
cap.release()

# Last element of frame_list is None. Thus removing it
frame_list.pop()
numberOfFrames = len(frame_list)

# Creating Main window
window = Tk()
window.geometry("+0+0")

# Main Screen (Video will be played here)
im = PhotoImage(file="welcome.png")
mainScreen = Label(window, image=im)
mainScreen.imtk = im
mainScreen.pack()

# Video Slider
scale = Scale(window, orient=HORIZONTAL, length=700, width=7, from_=0, to=(numberOfFrames - 1), cursor="hand2", showvalue=0)
scale.pack()

# Button Pallet
buttonPalette = Frame(window, height=300, width=700)
buttonPalette.pack(pady=10)

Button(buttonPalette, text="Pause", width=30, cursor="hand2", command=pause).grid(row=0, column=1, columnspan=2)
Button(buttonPalette, text="Normal >>", width=30, cursor="hand2", command=partial(change_speed, 500)).grid(row=1, column=1, columnspan=2)
Button(buttonPalette, text="Slow >>", width=30, cursor="hand2", command=partial(change_speed, 2000)).grid(row=2, column=1, columnspan=2)
Button(buttonPalette, text="<< Normal", width=30, cursor="hand2", command=partial(change_speed, -500)).grid(row=3, column=1, columnspan=2)
Button(buttonPalette, text="<< Slow", width=30, cursor="hand2", command=partial(change_speed, -2000)).grid(row=4, column=1, columnspan=2)
Button(buttonPalette, text="OUT", width=15, bg="red", foreground="white", cursor="hand2", command=partial(pending, True)).grid(row=5, column=1)
Button(buttonPalette, text="NOT OUT", width=15, bg="green", foreground="white", cursor="hand2", command=partial(pending, False)).grid(row=5, column=2)

frameNumber = 0

def sponsor():
    im = PhotoImage(file="sponsor.png")
    mainScreen.imtk = im
    mainScreen.config(image=im)
    Timer(2, show, (500, )).start()


Timer(2, sponsor).start()


window.mainloop()