import tkinter as tk
import speech_recognition as sr
import threading
from settings import settings_window
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
count = 0

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.config(bg='#bec3c6')
        self.title("Evelyn")
        self.resizable(False, False)
        self.rect = tk.PhotoImage(file=f"{dir_path}\\start.png")
        self.button = tk.Button(self, command=self.start_function, image=self.rect, bd=0, bg='#bec3c6', highlightthickness=0)
        self.button.place(x=105, y=65, width=200, height=60)
        
        self.image = tk.PhotoImage(file=f"{dir_path}\\settings.png")
        self.button_com = tk.Button(self, image=self.image, command=settings_window, bd=0, bg='#bec3c6', highlightthickness=0)
        self.button_com.place(x=350, y=10, width=40, height=40)

        self.function_running = False


    def start_function(self):
        self.running = True
        self.thread = threading.Thread(target=self.run_function)
        self.thread.start()


    def stop_function(self):
        self.running = False


    def run_function(self):
        global thread_run
        global count
        if not self.function_running:
            self.function_running = True
            thread_run = True
            self.pause = tk.PhotoImage(file=f"{dir_path}\\pause.png")
            self.button.config(image=self.pause)
            if count == 0:
                thread = threading.Thread(target=self.assistant)
                thread.start()
        else:
            thread_run = False
            self.function_running = False
            self.button.config(text="Нажми меня", image=self.rect)


    def assistant(self):
        global thread_run
        global count
        while self.running:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Говорите...")
                count = 1
                # слушаем голос с микрофона
                audio = r.listen(source)
                if thread_run:
                    try:
                        # распознаем слова
                        text = r.recognize_google(audio, language="ru-RU") # type: ignore
                        print("Вы сказали:", text)
                        self.check_com(text)
                    except sr.UnknownValueError:
                        print("Не удалось распознать слова")
                    except sr.RequestError as e:
                        print("Ошибка:", e)
                else:
                    print("Пауза")
                    count = 0
                    break
    

    def check_com(self, text):
        d = {}
        with open(f'{dir_path}\\commands.txt', 'r', encoding='utf-8') as file: 
            lines = file.readlines()
            for i in range(10):
                try:
                    words = lines[i].strip().split(';')
                    if len(words) == 2:
                        d[words[0]] = words[1]
                except Exception:
                    break
        for el in list(d.keys()):
            if el in text:
                os.startfile(d[text])
            

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
    thread_run = False