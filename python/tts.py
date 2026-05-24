from tkinter import *
import pyttsx3

root = Tk()
root.title("Uday tts")
root.geometry("250x350")

def talk():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(my_entry.get())
    engine.runAndWait()
    my_entry.delete(0,END)

my_entry = Entry(root, font=("Helvetica", 28))
my_entry.pack(pady=20)

mybutton = Button(root, text="Speak", command=talk)
mybutton.pack(pady=20)

root.mainloop()