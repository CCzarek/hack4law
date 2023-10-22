# generalnie scrap, ale może się jeszcze przyda

import tkinter as tk
from tkinter import ttk

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
scrollbar = ttk.Scrollbar(results_frame, command=results_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_listbox.config(yscrollcommand=scrollbar.set)

# Dodajmy kilka przykładowych wyników
for i in range(100):
    results_listbox.insert(tk.END, f"Wynik {i}")

# Etykieta do wyświetlania szczegółów
details_label = tk.Label(main_frame)

# Przycisk powrotu
back_button = tk.Button(main_frame, text="Powrót", command=go_back)

app.geometry("1280x720")
app.resizable(False, False)

app.mainloop()
