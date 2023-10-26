import tkinter as tk
from datetime import date
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import *
import pandas as pd
import chromadb
import pandas as pd
from database import search
import ast
from tkinter import scrolledtext


CONTENT_NAME = 'textContent_notags_eng100'
client = chromadb.HttpClient(host='localhost', port=8000)
df = pd.read_csv("preprocessed_2023_100.csv")
df['index'] = df.index

global current_ids


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


CLEANR = re.compile('<.*?>')
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  cleantext = re.sub(' +', ' ', cleantext)
  return cleantext


def on_result_selected(event):
    # Pobierz zaznaczony element
    selected_index = results_listbox.curselection()
    if selected_index:
        selected_item = results_listbox.get(selected_index[0])
        # Ukryj listę wyników i pokaż szczegóły
        results_frame.pack_forget()

        item_id = current_ids[selected_index[0]]
        my_row = df.loc[item_id, :]
        text_html = my_row['textContent']
        text_good = cleanhtml(text_html)

        details_label.config(text=f"Szczegóły dla: {selected_item} \n"+
                                  f"Typ organu orzekającego:  {my_row['courtType']} \n" +
                             f"Data: {my_row['judgmentDate']}\n "+
                             f"Rodzaj orzeczenia: {my_row['judgmentType']}\n"
                             )

        print(my_row)

        details_label.pack(pady=10, fill=tk.BOTH, expand=True)
        back_button.pack(pady=10)
        print()


def go_back():
    details_label.pack_forget()
    back_button.pack_forget()
    results_frame.pack(fill=tk.BOTH, expand=True)


content = client.get_collection(CONTENT_NAME)

app = tk.Tk()
app.title("Okoliczni Prawnicy")

header_frame = tk.Frame(app, bg="gray")
header_frame.pack(side=tk.TOP, fill=tk.X)
header_label = tk.Label(header_frame, text="Okoliczni Prawnicy", bg="gray", fg="white", font=("Arial", 16))
header_label.pack(pady=10)

sidebar_frame = tk.Frame(app)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
filter_label = tk.Label(sidebar_frame, text="Kryteria wyszukiwania", padx=20)
filter_label.pack(pady=10)

text_input = tk.Entry(sidebar_frame, width=30)
text_input.pack(padx=5)

start_date_label = tk.Label(sidebar_frame, text="Data początkowa:")
start_date_label.pack(anchor="w", pady=(5, 5), padx=10)
start_date_entry = DateEntry(sidebar_frame, width=12, background='blue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
start_date_entry.set_date(date(2020, 1, 1))
start_date_entry.pack(anchor="w", pady=(5, 10), padx=10)

end_date_label = tk.Label(sidebar_frame, text="Data końcowa:")
end_date_label.pack(anchor="w", pady=(5, 5), padx=10)
end_date_entry = DateEntry(sidebar_frame, width=12, background='blue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
end_date_entry.pack(anchor="w", pady=5, padx=10)


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


combo_label = tk.Label(sidebar_frame, text="Kluczowe frazy", padx=20)
combo_label.pack(pady=10)

e = Entry(sidebar_frame)
e.pack()
e.bind('<KeyRelease>', checkkey)

lb = Listbox(sidebar_frame, selectmode='multiple')
lb.pack()
update(keywords)


def keywordFilter(ser, keywords):
    l = ser.to_list()
    res = []
    for el in l:
        x = True
        for keyword in keywords:
            if keyword in el:
                res.append(True)
                x = False
                break                
        if x:
            res.append(False)
    return res


def get_row(selected_index): # upoślodzony wiersz TODO
    val = results_listbox.get(selected_index)
    print(val)
    row = df[df['courtCases'] == val]
    print(row)
    return row


def get_text():
    i = 0
    results_listbox.delete(0, END)
    entered_text = text_input.get()
    selection = [lb.get(i) for i in lb.curselection()]
    rowsSelected = df[keywordFilter(df['keywords'], selection)]
    n = len(rowsSelected['keywords'].to_list())
    quantity = 20
    keywordsIds = rowsSelected['index'].to_list()
    ids = search(content, entered_text, quantity)
    ids = [eval(i) for i in ids]
    print(ids)
    print(keywordsIds)
    st1 = [val for val in keywordsIds if val in ids]
    nd2 = [val for val in keywordsIds if not val in ids]
    rd3 = [val for val in ids if not val in keywordsIds]
    for el in st1:
        results_listbox.insert(i, rowsSelected[rowsSelected['index'] == el]['courtCases'].values[0])
        i+=1
    for el in nd2:
        if i <= 20:
            results_listbox.insert(i, df[df['index'] == el]['courtCases'].values[0])
            i+=1
    for el in rd3:
        if i <= 20:
            print(el)
            print(df[df['index'] == el])
            results_listbox.insert(i, df[df['index'] == el]['courtCases'].values[0])
            i+=1
    global current_ids
    current_ids = ids


button = tk.Button(sidebar_frame, text="Enter", command=get_text, width=15)
button.pack()


main_frame = tk.Frame(app)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


results_frame = tk.Frame(main_frame)
results_frame.pack(fill=tk.BOTH, expand=True)


results_listbox = tk.Listbox(results_frame, yscrollcommand=lambda f1, f2: scrollbar.set(f1, f2))
results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
results_listbox.bind("<<ListboxSelect>>", on_result_selected)


scrollbar = tk.Scrollbar(results_frame, command=results_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_listbox.config(yscrollcommand=scrollbar.set)


details_label = tk.Label(main_frame)

back_button = tk.Button(main_frame, text="Powrót", command=go_back)

app.geometry("800x600")
app.resizable(False, False)

app.mainloop()
