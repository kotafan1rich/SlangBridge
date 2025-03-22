import customtkinter as ctk
import json as js

class App:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("800x600")
        self.window.title("SL")

        self.ConfigureGrid()
        self.CreateUI()
        self.GridUI()

        self.window.mainloop()
    
    def ConfigureGrid(self):
        self.window.columnconfigure(index=0, weight=1, uniform="a")
        self.window.columnconfigure(index=1, weight=4, uniform="a")
        self.window.columnconfigure(index=2, weight=1, uniform="a")

        self.window.rowconfigure(index=0, weight=2, uniform="a")
        self.window.rowconfigure(index=1, weight=2, uniform="a")
        self.window.rowconfigure(index=2, weight=4, uniform="a")
        self.window.rowconfigure(index=3, weight=1, uniform="a")
        self.window.rowconfigure(index=4, weight=2, uniform="a")
    
    def CreateUI(self):
        self.name = ctk.CTkLabel(master=self.window, text="Slang Translator", font=("Arial", 40))
        self.inputField = ctk.CTkEntry(master=self.window, font=("Arial", 40), corner_radius=20)
        self.output = ctk.CTkLabel(master=self.window, text="lskjgdgrnkbgzgrlgjldgr", font=("Arial", 40))
        self.confButton = ctk.CTkButton(master=self.window, text="TRANSLATE", command=self.Click, fg_color="#000000", corner_radius=20, font=("Arial", 25))
    
    def GridUI(self):
        self.name.grid(row=0, column=1, sticky="nsew")
        self.inputField.grid(row=1, column=1, sticky="nsew")
        self.output.grid(row=2, column=1, sticky="nsew")
        self.confButton.grid(row=3, column=1, sticky="nsew")
    
    def Click(self):
        ...


app = App()
