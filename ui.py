# generalnie scrap, ale może się jeszcze przyda

import tkinter as tk
from tkinter import *
import pandas as pd
import chromadb
import pandas as pd
from database import search
import ast


CONTENT_NAME = 'textContent_notags_eng100'
client = chromadb.HttpClient(host='localhost', port=8000)

# klaska

class MultiSelectInput(tk.Frame):
    def __init__(self, master=None, label="Wybór", choices=None, default=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=label)
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for choice in choices:
            self.listbox.insert(tk.END, choice)

        if default and default in choices:
            default_idx = choices.index(default)
            self.listbox.select_set(default_idx)

    def get_selected(self):
        return [self.listbox.get(i) for i in self.listbox.curselection()]

# klaska end


def on_result_selected(event):
    # Pobierz zaznaczony element
    selected_index = results_listbox.curselection()
    if selected_index:
        selected_item = results_listbox.get(selected_index[0])
        # Ukryj listę wyników i pokaż szczegóły
        results_frame.pack_forget()
        details_label.config(text=f"Szczegóły dla: {selected_item}")
        details_label.pack(pady=10, fill=tk.BOTH, expand=True)
        back_button.pack(pady=10)

def go_back():
    # Ukryj szczegóły i pokaż listę wyników
    details_label.pack_forget()
    back_button.pack_forget()
    results_frame.pack(fill=tk.BOTH, expand=True)
    
content = client.get_collection(CLIENT_NAME) 

app = tk.Tk()
app.title("Okoliczni Prawnicy TYTUL APKI OMG OMG")

# Górny pasek z nazwą aplikacji
header_frame = tk.Frame(app, bg="gray")
header_frame.pack(side=tk.TOP, fill=tk.X)
header_label = tk.Label(header_frame, text="Okoliczni Prawnicy 🍆💦", bg="gray", fg="white", font=("Arial", 16))
header_label.pack(pady=10)

# Pasek boczny z kryteriami wyszukiwania
sidebar_frame = tk.Frame(app)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
filter_label = tk.Label(sidebar_frame, text="Kryteria wyszukiwania")
filter_label.pack(pady=10)
# TODO: Dodaj tutaj więcej kontrolek do filtrowania
# nowe

# Create a label to describe the text input
# label = tk.Label(sidebar_frame, text="Enter Text:")
# label.pack()

# Create a text input field
text_input = tk.Entry(sidebar_frame, width=30)
text_input.pack()

# Autocomplete combobox
def checkkey(event):
    value = event.widget.get()
    print(value)
    if value == '':
        data = list(keywords)
    else:
        data = [item for item in keywords if value.lower() in item.lower()]
    update(data)

def update(data):
    lb.delete(0, 'end')
    for item in data:
        lb.insert('end', item)

df['keywords'] = df['keywords'].apply(ast.literal_eval)
keywordsList = df['keywords'].tolist()
keywords = set()
for listk in keywordsList:
    for el in listk:
        keywords.add(el)

e = Entry(sidebar_frame)
e.pack()
e.bind('<KeyRelease>', checkkey)

lb = Listbox(sidebar_frame, selectmode='multiple')
lb.pack()
update(keywords)

# Function to get the text when a button is clicked
def get_text():
    entered_text = text_input.get()
    selection = [lb.get(i) for i in lb.curselection()]
    for keyword in selection:
        rows = df[keyword in df['keywords']]

# Create a button to trigger an action
button = tk.Button(sidebar_frame, text="Enter", command=get_text, width=15)
button.pack()


# nowe end


# Główne okno
main_frame = tk.Frame(app)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Ramka dla listy wyników i paska przewijania
results_frame = tk.Frame(main_frame)
results_frame.pack(fill=tk.BOTH, expand=True)

# Przewijalna lista wyników
results_listbox = tk.Listbox(results_frame, yscrollcommand=lambda f1, f2: scrollbar.set(f1, f2))
results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
results_listbox.bind("<<ListboxSelect>>", on_result_selected)

# Scrollbar
scrollbar = tk.Scrollbar(results_frame, command=results_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_listbox.config(yscrollcommand=scrollbar.set)

# Dodajmy kilka przykładowych wyników
for i in range(100):
    results_listbox.insert(tk.END, f"Wynik {i}")

# Etykieta do wyświetlania szczegółów
details_label = tk.Label(main_frame)

# Przycisk powrotu
back_button = tk.Button(main_frame, text="Powrót", command=go_back)

app.geometry("800x600")
app.resizable(False, False)

app.mainloop()
