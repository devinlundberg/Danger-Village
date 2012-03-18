# -*- coding: utf-8 -*-
from Tkinter import *

class MyDialog:

    def __init__(self, parent):
        self.top = Toplevel(parent)
        top=self.top
        Label(top, text="Value").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        print "value is", self.e.get()
        self.top.destroy()


root = Tk()
Button(root, text="Hello!", bg="blue").pack()
root.update()

d = MyDialog(root)

root.wait_window(d.top)