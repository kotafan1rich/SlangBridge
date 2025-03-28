import json as js
import threading as th
import time
from PIL import Image
from sys import exit
import customtkinter as ctk
from config import TRANSLATE_FILE
from utils import get_definition, split_on_strings

slang = js.load(open(TRANSLATE_FILE, "r", encoding="utf-8"))


class App:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("750x500")
        self.window.title("Slang Bridge")

        self.processed = ctk.IntVar(value=0)

        self.ConfigureGrid()
        self.CreateUI()
        self.GridUI()

        self.window.bind("<Return>", self.enterPressed)
        self.window.mainloop()
        exit()

    def ConfigureGrid(self):
        self.window.columnconfigure(index=0, weight=2, uniform="a")
        self.window.columnconfigure(index=1, weight=4, uniform="a")
        self.window.columnconfigure(index=2, weight=3, uniform="a")
        self.window.columnconfigure(index=3, weight=1, uniform="a")
        self.window.columnconfigure(index=4, weight=2, uniform="a")

        self.window.rowconfigure(index=0, weight=3, uniform="a")
        self.window.rowconfigure(index=1, weight=2, uniform="a")
        self.window.rowconfigure(index=2, weight=2, uniform="a")
        self.window.rowconfigure(index=3, weight=2, uniform="a")
        self.window.rowconfigure(index=4, weight=6, uniform="a")
        self.window.rowconfigure(index=5, weight=1, uniform="a")
        self.window.rowconfigure(index=6, weight=2, uniform="a")
        self.window.rowconfigure(index=7, weight=2, uniform="a")

    def CreateUI(self):
        self.name = ctk.CTkLabel(
            master=self.window, text="Slang Bridge", font=("Arial", 40)
        )
        self.inputField = ctk.CTkEntry(
            master=self.window, font=("Arial", 40), corner_radius=20
        )
        self.outFrame = ctk.CTkScrollableFrame(master=self.window)
        self.output = ctk.CTkLabel(master=self.outFrame, text="", font=("Arial", 20))
        self.confButton = ctk.CTkButton(
            master=self.window,
            text="ПЕРЕВЕСТИ",
            command=self.Click,
            fg_color="#000000",
            corner_radius=20,
            font=("Arial", 25),
            hover_color="#AAAAAA",
            border_width=1,
            border_color="#FFFFFF",
        )
        self.modelOption = ctk.CTkOptionMenu(
            master=self.window,
            values=[
                "gpt-4o-mini",
                "Claude 3.5 Haiku",
                "Claude 3.7 Sonnet",
                "deepseek-v3",
            ],
        )
        self.optionName = ctk.CTkLabel(
            master=self.window, text="Модели для перевода: ", font=("Arial", 20)
        )
        self.radioText = ctk.CTkRadioButton(
            master=self.window, variable=self.processed, value=0, text="Слово"
        )
        self.radioSentence = ctk.CTkRadioButton(
            master=self.window, variable=self.processed, value=1, text="Предложение"
        )
        self.vScroll = ctk.CTkScrollbar(master=self.window, orientation="vertical")
        imageCopy = ctk.CTkImage(light_image=Image.open("static/copyIcon.png"))
        self.copyButton = ctk.CTkButton(
            master=self.window,
            command=self.CopyText,
            fg_color="#000000",
            corner_radius=20,
            font=("Arial", 12),
            hover_color="#AAAAAA",
            border_width=1,
            border_color="#FFFFFF",
            text="",
            image=imageCopy,
        )

    def GridUI(self):
        self.name.grid(row=0, column=1, sticky="nsew", columnspan=3)
        self.inputField.grid(row=1, column=1, sticky="nsew", columnspan=3)
        self.optionName.grid(row=2, column=1, sticky="nsew")
        self.modelOption.grid(row=2, column=2, sticky="we", columnspan=2)
        self.radioText.grid(row=3, column=1, sticky="nsew")
        self.radioSentence.grid(row=3, column=2, sticky="nsew", columnspan=2)
        self.outFrame.grid(row=4, column=1, columnspan=3, sticky="nsew")
        self.output.grid(row=0, column=0, sticky="nsew", columnspan=3)
        self.confButton.grid(row=6, column=1, sticky="nsew", columnspan=2)
        self.copyButton.grid(row=6, column=3, sticky="ns")

    def Click(self):
        t = th.Thread(target=self.Processing)
        t.daemon = True
        t.start()

    def CopyText(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.output._text)

    def LoadingStatus(self):
        self.isLoading = True
        self.output.configure(font=("Arial", 40))
        while self.isLoading:
            self.output.configure(text="Загрузка .")
            time.sleep(0.5)
            if not self.isLoading:
                break
            self.output.configure(text="Загрузка ..")
            time.sleep(0.5)
            if not self.isLoading:
                break
            self.output.configure(text="Загрузка ...")
            time.sleep(0.5)

    def Processing(self):
        value = self.inputField.get().lower().strip()
        if value == "":
            return 0
        if len(self.inputField.get().split()) != 1 and self.processed.get() == 0:
            self.output.configure(
                text="Введите только одно слово для этого режима", font=("Arial", 20)
            )
            return 0
        p = th.Thread(target=self.LoadingStatus)
        p.daemon = True
        p.start()
        self.output.configure(text="")
        if value not in slang.keys():
            out = get_definition(value, self.modelOption.get(), self.processed.get())
        else:
            out = slang[value]
        if len(out) <= 22:
            self.output.configure(font=("Arial", 40))
        elif len(out) <= 29:
            self.output.configure(font=("Arial", 30))
        else:
            self.output.configure(font=("Arial", 20))
        self.isLoading = False
        self.output.configure(text=split_on_strings(out.capitalize()))

    def enterPressed(self, event):
        self.Click()


if __name__ == "__main__":
    app = App()
