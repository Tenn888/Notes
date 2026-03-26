import tkinter as tk
import TKinterModernThemes as TKMT
import os

X = 330
Y = 550

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, title="Notes", theme="park", mode="light", usecommandlineargs=True, usethemeconfigfile=True, X=X, Y=Y):
        super().__init__(title, theme, mode, usecommandlineargs, usethemeconfigfile)

        self.root.geometry("{}x{}".format(X, Y))

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas)

        self.frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.frame_id, width=e.width)
        )

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.view_notes()

        self.add_button = tk.Button(self.root, text="⋮", font=("Arial", 25), command=self.options)
        self.add_button.place(relx=1.0, rely=1.0, x=-30, y=-10, anchor="se", width=50, height=50)
        self.add_button.lift()

    def on_mousewheel(self, event):
        bbox = self.canvas.bbox("all")
        if bbox:
            x0, y0, x1, y1 = bbox
            content_height = y1 - y0
            if content_height > self.canvas.winfo_height():
                self.canvas.yview_scroll(-event.delta // 120, "units")

    def get_notes_files(self):
        files = [f for f in os.listdir() if f.startswith("notes_") and f.endswith(".txt")]
        return files
    
    def options(self):
        pass

    def create_note(self):
        def save_note(window, text_widget):
            used_ind = set()
            for name in self.get_notes_files():
                try:
                    used_ind.add(int(name[6:-4]))
                except ValueError:
                    continue

            new_idx = 1
            while new_idx in used_ind:
                new_idx += 1

            with open(f'notes_{new_idx}.txt', 'w', encoding="utf-8") as file:
                file.write(text_widget.get("1.0", tk.END))
            self.view_notes()
            window.destroy()

        self.new_window = tk.Toplevel(self.scrollable_frame)
        self.new_window.title("Новая заметка")
        self.new_window.geometry("300x410")

        toolbar = tk.Frame(self.new_window)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        text_widget = tk.Text(self.new_window)
        text_widget.pack(side=tk.TOP, expand=True, fill="both")

        tk.Button(toolbar, text="Сохранить", font=("Arial", 12), command=lambda: save_note(self.new_window, text_widget)).pack(side=tk.LEFT, padx=1)

    def edit_note(self, note_filename):
        def save_note():
            with open(note_filename, 'w', encoding="utf-8") as file:
                file.write(text_widget.get("1.0", tk.END))
            self.view_notes()

        def delete_note(window):
            os.remove(note_filename)

            for name in self.get_notes_files():
                try:
                    current_idx = int(name[6:-4])
                except ValueError:
                    continue
                if current_idx > int(note_filename[6:-4]):
                    new_name = f'notes_{current_idx - 1}.txt'
                    os.rename(name, new_name)

            self.view_notes()
            window.destroy()

        self.new_window = tk.Toplevel(self.scrollable_frame)
        self.new_window.title("Редактирование заметки")
        self.new_window.geometry("300x410")

        toolbar = tk.Frame(self.new_window)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        text_widget = tk.Text(self.new_window)
        text_widget.pack(side=tk.TOP,expand=True, fill="both")

        with open(note_filename, 'r', encoding="utf-8") as file:
            content = file.read()
            text_widget.insert(tk.END, content)

        tk.Button(toolbar, text="Сохранить", font=("Arial", 12), command=save_note).pack(side=tk.LEFT, padx=1)
        tk.Button(toolbar, text="Удалить", font=("Arial", 12), command=lambda: delete_note(self.new_window)).pack(side=tk.LEFT, padx=1)

    def view_notes(self):
        list_notes = self.get_notes_files()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for filename in list_notes:
            with open(filename, 'r', encoding="utf-8") as file:
                note_content = file.read()
                note_label = tk.Label(
                    self.scrollable_frame,
                    text=note_content,
                    bg="lightyellow",
                    anchor="w",
                    justify="left",
                    wraplength=300
                )
                note_label.pack(pady=5, padx=5, fill="x")
                note_label.bind("<Button-1>", lambda event, note_filename=filename: self.edit_note(note_filename))
    
    def run(self):
        self.add_button.lift()
        super().run()


if __name__ == "__main__":
    app = App()
    app.run()
