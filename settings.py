import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import speech_recognition as sr
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# общее окно
def settings_window():
        # Создаем новое окно
        global new_window
        new_window = tk.Toplevel()
        new_window.config(bg='#bec3c6')
        new_window.title("Команды")
        new_window.geometry(f"600x300")
        new_window.resizable(False, False)
        read_file(new_window)
        new_window.grab_set()

# добавление новой команды в текстовый файл
def add():
    global text
    global folder_path
    with open(f'{dir_path}\\commands.txt', "a", encoding='utf-8') as file:
        file.write(f'{text};{folder_path}' + "\n")
    append_window.destroy()

# распознаёт голос для создания новой команды
def recognize_speech():
    global speech
    global text
    global folder_path
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU") # type: ignore
            speech.config(text=text)
            try:
                if folder_path:
                    append = tk.Button(append_window, text="Добавить команду", command=add, font=('Fira Sans Regular', 10))
                    append.pack(pady=30)
            except:
                pass
        except sr.UnknownValueError:
            speech.config(text="Не удалось распознать речь")
        except sr.RequestError:
            speech.config(text="Ошибка запроса")

# окно добавления команды
def append_com():
    def on_closing():
        append_window.destroy()
        settings_window()
    
    global speech
    global append_window
    new_window.destroy()
    append_window = tk.Toplevel()
    append_window.config(bg='#bec3c6')
    append_window.title("Добавление команды")
    append_window.geometry('500x180')
    append_window.resizable(False, False)
    append_window.grab_set()
    append_window.protocol("WM_DELETE_WINDOW", on_closing)

    # функция выбора файла
    def select_folder():
        global folder_path
        folder_path = filedialog.askopenfilename()
        if folder_path:
            print("Выбранная файл:", folder_path)
            path.config(text=f'{folder_path}')
            try:
                if speech:
                    append = tk.Button(append_window, text="Добавить команду", command=add, font=('Fira Sans Regular', 10))
                    append.pack(pady=30)
            except:
                pass

    button_frame = tk.Frame(append_window, bg='#bec3c6')
    button_frame.pack(anchor="w", padx=10, pady=10)
    button = tk.Button(button_frame, text="Распознать команду", command=recognize_speech, font=('Fira Sans Regular', 10))
    button.pack(side=tk.LEFT)
    speech = tk.Label(button_frame, text="", bg='#bec3c6')
    speech.pack(side=tk.LEFT)

    button2_frame = tk.Frame(append_window, bg='#bec3c6')
    button2_frame.pack(anchor="w", padx=10)
    button2 = tk.Button(button2_frame, text="Выбрать файл", command=select_folder, font=('Fira Sans Regular', 10))
    button2.pack(side=tk.LEFT)
    path = tk.Label(button2_frame, text="", bg='#bec3c6')
    path.pack(side=tk.LEFT)

# удаление команды 
def save_num():
    global entry
    global del_window
    inp = entry.get()
    if 1 <= int(inp) <= x:
        with open(f'{dir_path}\\commands.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines.pop(int(inp) - 1)
        with open(f'{dir_path}\\commands.txt', 'w', encoding='utf-8') as file:
            file.writelines(lines)
        del_window.destroy()
        settings_window()
    else:
        entry.delete(0, tk.END)
        label = tk.Label(del_window, text="Нет такого номера!", font=('Fira Sans Regular', 14), bg='#bec3c6')
        label.pack(pady=10)

# окно удаления команд
def del_com():
    def on_closing():
        print("Новое окно закрыто")
        del_window.destroy()
        settings_window()

    global del_window
    new_window.destroy()
    del_window = tk.Toplevel()
    del_window.config(bg='#bec3c6')
    del_window.title("Удаление команды")
    del_window.geometry('300x300')
    del_window.resizable(False, False)
    del_window.grab_set()
    del_window.protocol("WM_DELETE_WINDOW", on_closing)

    label = tk.Label(del_window, text="Введите номер команды,\nкоторую хотите удалить:", font=('Fira Sans Regular', 14), bg='#bec3c6')
    label.pack(pady=10)

    def validate_input(char):
        if char.isdigit() or char == "":
            return True
        else:
            return False

    global entry
    entry = tk.Entry(del_window, width=10, font=('Fira Sans', 12))
    entry.config(validate="key", validatecommand=(del_window.register(validate_input), "%S"))
    entry.pack(pady=10)

    save = tk.Button(del_window, text="Удалить", command=save_num)
    save.pack(pady=10)

# интерфейс для общего окна
def read_file(window):
    with open(f'{dir_path}\\commands.txt', 'r', encoding='utf-8') as file:
        global x

        table = ttk.Treeview(window, columns=('n', "Word1", "Word2"), show="headings")
        table.heading("n", text="№")
        table.heading("Word1", text="Команда")
        table.heading("Word2", text="Приложение")
        table.column("n", width=1)
        table.column("Word1", width=130)
        table.column("Word2", width=250)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=('Fira Sans Regular', 10))
        style.configure("Treeview.Heading", font=('Fira Sans Regular', 10))
        
        lines = file.readlines()
        x = len(lines)
        for i in range(10):
            try:
                words = lines[i].strip().split(';')
                if len(words) == 2:
                    table.insert("", "end", values=(i + 1, words[0], words[1]))
            except Exception:
                break

        table.pack(fill="both", expand=True)

        if len(lines) < 10:
            button = tk.Button(window, text="Добавить команду", command=append_com, font=('Fira Sans Regular', 10))
            button.pack(fill="x")

        if len(lines) > 0:
            button2 = tk.Button(window, text="Удалить команду", command=del_com, font=('Fira Sans Regular', 10))
            button2.pack(side="left", fill="x", expand=True)