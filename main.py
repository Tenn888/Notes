import tkinter as tk
import itertools
import os

X = 330
Y = 500

# Создание главного окна
app = tk.Tk()
app.title("Заметки")
app.geometry("{}x{}".format(X, Y))

# Создание прокручиваемой области
canvas = tk.Canvas(app)
# Создание вертикальной полосы прокрутки
scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
# Связывание полосы прокрутки с холстом
canvas.configure(yscrollcommand=scrollbar.set)

# Размещение элементов
scrollbar.pack(side="right", fill="y")
canvas.pack(fill="both", expand=True)

# Создание внутреннего фрейма для размещения заметок
scrollable_frame = tk.Frame(canvas)

# Добавление внутреннего фрейма на холст
frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Обновление области прокрутки при изменении размера внутреннего фрейма
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Обновление ширины внутреннего фрейма при изменении размера холста
canvas.bind(
    "<Configure>", 
    lambda e: canvas.itemconfig(frame_id, width=e.width)
)

# Обработка прокрутки колесиком мыши
def on_mousewheel(event):
    bbox = canvas.bbox("all")
    if bbox:
        x0, y0, x1, y1 = bbox
        content_height = y1 - y0
        # Прокручиваем только если содержимого больше видимой области
        if content_height > canvas.winfo_height():
            canvas.yview_scroll(-event.delta//120, "units")

# Привязка события прокрутки к холсту
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Функции для создания новой заметки
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
    
    # Создание нового окна для заметки
    new_window = tk.Toplevel(scrollable_frame)
    new_window.title("Новая заметка")
    new_window.geometry("300x410")
    text_widget = tk.Text(new_window)
    text_widget.pack(expand=True, fill="both")
    
    # Панель инструментов для кнопок
    toolbar = tk.Frame(new_window, height=20)
    toolbar.pack(side=tk.LEFT, fill=tk.X, expand=True)
    toolbar.pack_propagate(False)

    # Кнопка сохранения заметки
    tk.Button(toolbar, text="Сохранить", font=("Arial", 12), command=save_note).pack(side=tk.LEFT, padx=1)

# Функция для редактирования заметки
def edit_note(idx):
    def save_note():
        with open(f'notes_{idx}.txt', 'w', encoding="utf-8") as file:
            file.write(text_widget.get("1.0", tk.END))
        
        view_notes()

    def delete_note(idx, window):
        os.remove(f'notes_{idx}.txt')
        view_notes()
    
    # Создание нового окна для редактирования заметки
    new_window = tk.Toplevel(scrollable_frame)
    new_window.title("Редактирование заметки")
    new_window.geometry("300x410")
    text_widget = tk.Text(new_window)
    text_widget.pack(expand=True, fill="both")

    # Загрузка содержимого заметки в текстовый виджет
    with open(f'notes_{idx}.txt', 'r', encoding="utf-8") as file:
        content = file.read()
        text_widget.insert(tk.END, content)
    
    # Панель инструментов для кнопок
    toolbar = tk.Frame(new_window, height=20)
    toolbar.pack(side=tk.LEFT, fill=tk.X, expand=True)
    toolbar.pack_propagate(False)

    # Кнопки сохранения и удаления заметки
    tk.Button(toolbar, text="Сохранить", font=("Arial", 12), command=save_note).pack(side=tk.LEFT, padx=1)
    tk.Button(toolbar, text="Удалить", font=("Arial", 12), command=lambda: delete_note(idx, new_window)).pack(side=tk.LEFT, padx=1)

# Функция для отображения всех заметок
def view_notes():
    # Очистка текущих заметок
    for widget in scrollable_frame.winfo_children():
        if widget != button_1:
            widget.destroy()
    
    # Загрузка и отображение всех заметок
    for i in itertools.count():
        try:
            with open(f'notes_{i}.txt', 'r', encoding="utf-8") as file:
                note_content = file.read()
                note_label = tk.Label(scrollable_frame, text=note_content, bg="lightyellow", anchor="w", justify="left", wraplength=300)
                note_label.pack(pady=5, padx=5, fill="x")
                note_label.bind("<Button-1>", lambda event, idx=i: edit_note(idx))
        except FileNotFoundError:
            break

view_notes()

# Кнопка для создания новой заметки
button_1 = tk.Button(app, text="+", font=("Arial", 25), command=create_note)
button_1.place(relx=1.0, rely=1.0, x=-30, y=-10, anchor="se", width=50, height=50)
button_1.lift()


# Запуск главного цикла приложения
app.update()
app.mainloop()