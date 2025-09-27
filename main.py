import tkinter as tk

app = tk.Tk()
app.title("Заметки")
app.geometry("330x500")

def create_note():
    def save_note():
        with open("notes.txt", "a", encoding="utf-8") as file:
            file.write(text_widget.get("1.0", tk.END) + "\n")
    
    new_window = tk.Toplevel(app)
    new_window.title("Новая заметка")
    new_window.geometry("300x400")
    text_widget = tk.Text(new_window)
    text_widget.pack(expand=True, fill="both")
    
    button_2 = tk.Button(new_window, text="Сохранить", font=("Arial", 12), command=save_note)
    button_2.place(relx=0.5, rely=1.0, x=0, y=-10, anchor="s", width=100, height=30)


button_1 = tk.Button(app, text="+", font=("Arial", 25), command=create_note)
button_1.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se", width=50, height=50)

app.mainloop()