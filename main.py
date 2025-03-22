import customtkinter as ctk
import json as js
import threading as th
from ai.api import api
from sys import exit

slang = js.load(open("translate.json", "r", encoding="utf-8"))


def GetDefinition(input):
    return api(input)


class App:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("750x500")
        self.window.title("Slang Translator")

        self.ConfigureGrid()
        self.CreateUI()
        self.GridUI()

        self.window.bind("<Return>", self.enterPressed)
        self.window.mainloop()
        exit()

    def ConfigureGrid(self):
        self.window.columnconfigure(index=0, weight=1, uniform="a")
        self.window.columnconfigure(index=1, weight=4, uniform="a")
        self.window.columnconfigure(index=2, weight=1, uniform="a")

        self.window.rowconfigure(index=0, weight=2, uniform="a")
        self.window.rowconfigure(index=1, weight=2, uniform="a")
        self.window.rowconfigure(index=2, weight=3, uniform="a")
        self.window.rowconfigure(index=3, weight=1, uniform="a")
        self.window.rowconfigure(index=4, weight=1, uniform="a")

    def CreateUI(self):
        self.name = ctk.CTkLabel(
            master=self.window, text="Переводчик Слэнга", font=("Arial", 40)
        )
        self.inputField = ctk.CTkEntry(
            master=self.window, font=("Arial", 40), corner_radius=20
        )
        self.output = ctk.CTkLabel(master=self.window, text="", font=("Arial", 20))
        self.confButton = ctk.CTkButton(
            master=self.window,
            text="ПЕРЕВЕСТИ",
            command=self.Click,
            fg_color="#000000",
            corner_radius=20,
            font=("Arial", 25),
            hover_color="#AAAAAA",
        )

    def GridUI(self):
        self.name.grid(row=0, column=1, sticky="nsew")
        self.inputField.grid(row=1, column=1, sticky="nsew")
        self.output.grid(row=2, column=1, sticky="nsew")
        self.confButton.grid(row=3, column=1, sticky="nsew")

    def Click(self):
        t = th.Thread(target=self.Processing)
        t.daemon = True
        t.start()
    
    def Processing(self):
        value = self.inputField.get().lower().strip()
        if value not in slang.keys():
            out = GetDefinition(value)
        else:
            out = slang[value]
        if len(out) <= 22:
            self.output.configure(font=("Arial", 40))
        elif len(out) <= 29:
            self.output.configure(font=("Arial", 30))
        else:
            self.output.configure(font=("Arial", 20))
        self.output.configure(text=out.capitalize()[:45])

    def enterPressed(self, event):
        self.Click()


app = App()
