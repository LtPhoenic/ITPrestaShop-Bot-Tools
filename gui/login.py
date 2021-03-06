from tkinter import *
from tkinter import messagebox
from db import *
import time
import hashlib
import webbrowser
from main import *


class Application():
    def __init__(self):
        """
            build up the login gui and check if it possible to connect with the database
        """
        self.db = DB()
        self.offline = False
        try:
            self.db.connect()
        except pymysql.err.OperationalError:
            self.offline = True

        self.loginframe = Tk()
        self.loginframe.iconbitmap(default="./img./ico.ico")
        self.loginframe.title("Administration Control Panel")
        self.loginframe.resizable(width=FALSE, height=FALSE)
        self.loginframe.geometry("340x460")

        self.bgImg = PhotoImage(file="./img/bg_overlay_status.png")
        self.bg1 = Label(self.loginframe, image=self.bgImg).pack()

        self.passVar = StringVar()
        self.passwordTb = Entry(self.loginframe, show="*", textvariable=self.passVar)
        self.passwordTb.place(x=100, y=285)

        self.ubImg = PhotoImage(file="./img/field.png")
        self.userVar = StringVar()
        self.usernameTb = Entry(self.loginframe, textvariable=self.userVar)
        self.usernameTb.place(x=100, y=238)

        self.btnImg = PhotoImage(file="./img/button.png")
        self.loginBtn = Button(self.loginframe, command=self.checkContent, height=33, width=149,
                               image=self.btnImg)  # Login Button
        self.loginBtn.place(x=99, y=330)

        self.visitImg = PhotoImage(file="./img/visbg.png")
        self.visitLbl = Label(self.loginframe, image=self.visitImg)
        self.visitLbl.place(x=-2, y=405)

        self.visitLbl.bind("<Button-1>", self.visitUs)
        if self.offline is False:
            self.statusOn = Label(self.loginframe, text="Online", bg="white", fg="green")
            self.statusOn.place(x=160, y=200)
        else:
            self.statusOff = Label(self.loginframe, text="Offline", bg="white", fg="red")
            self.statusOff.place(x=160, y=200)

        self.loginframe.bind("<Return>", self.returnFunc)

        self.loginframe.mainloop()  # MAINLOOP END

    def returnFunc(self, event):
        """
            return key hook
        """
        self.checkContent()

    def checkContent(self):
        """
            open the main gui if login accepted or give an Error message
        """
        hashObj = hashlib.sha256(self.passVar.get().encode())
        userQuery = self.db.query("SELECT * FROM ita_user WHERE username = '%s' AND password = '%s'" % (
        self.userVar.get(), hashObj.hexdigest()))
        if len(userQuery.fetchall()):
            self.loginframe.withdraw()
            Mainframe(self.userVar.get())
        else:
            messagebox.showinfo("Error", "Invalid Input: Wrong username or password, please try again!", icon="error")

    def visitUs(self, event):
        """
            open our website
        """
        webbrowser.open_new_tab("https://github.com/Gurkengewuerz/prestashop-bot")


Application()
