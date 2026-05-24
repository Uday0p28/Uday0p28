from tkinter import *
import webbrowser

root = Tk()
theLabel = Label(root, text="Hacked, hacked, hacked, hacked, hacked, hacked, hacked, hacked, hacked")
theLabel.pack()

topFrame = Frame(root)
topFrame.pack()

def func():
    webbrowser.open("/Users/udayshandil/Documents")
button = Button(topFrame, text="boom", fg="red", command=func)
button.pack()

root.mainloop()