import tkinter as tk
import itertools

app = tk.Tk()
app.title("Заметки")
app.geometry("330x500")

def create_note():
    def save_note():
        for i in itertools.count():
            try:
                with open(f'notes_{i}.txt', 'r') as file:
                    continue
            except FileNotFoundError:
                with open(f'notes_{i}.txt', 'w', encoding="utf-8") as file:
                    file.write(text_widget.get("1.0", tk.END))
                view_notes()
                break
    
    new_window = tk.Toplevel(app)
    new_window.title("Новая заметка")
    new_window.geometry("300x400")
    text_widget = tk.Text(new_window)
    text_widget.pack(expand=True, fill="both")
    
    button_2 = tk.Button(new_window, text="Сохранить", font=("Arial", 12), command=save_note)
    button_2.place(relx=0.5, rely=1.0, x=0, y=-10, anchor="s", width=100, height=30)

def edit_note(idx):
    def save_note():
        with open(f'notes_{idx}.txt', 'w', encoding="utf-8") as file:
            file.write(text_widget.get("1.0", tk.END))
        
        view_notes()
    
    new_window = tk.Toplevel(app)
    new_window.title("Редактирование заметки")
    new_window.geometry("300x400")
    text_widget = tk.Text(new_window)
    text_widget.pack(expand=True, fill="both")

    with open(f'notes_{idx}.txt', 'r', encoding="utf-8") as file:
        content = file.read()
        text_widget.insert(tk.END, content)
    
    button_2 = tk.Button(new_window, text="Сохранить", font=("Arial", 12), command=save_note)
    button_2.place(relx=0.5, rely=1.0, x=0, y=-10, anchor="s", width=100, height=30)

def view_notes():
    for widget in app.winfo_children():
        if widget != button_1:
            widget.destroy()
    
    for i in itertools.count():
        try:
            with open(f'notes_{i}.txt', 'r', encoding="utf-8") as file:
                note_content = file.read()
                note_label = tk.Label(app, text=note_content, bg="lightyellow", anchor="w", justify="left", wraplength=300)
                note_label.pack(pady=5, padx=5, fill="x")
                note_label.bind("<Button-1>", lambda event, idx=i: edit_note(idx))
        except FileNotFoundError:
            break

view_notes()

button_1 = tk.Button(app, text="+", font=("Arial", 25), command=create_note)
button_1.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se", width=50, height=50)

app.update()
app.mainloop()