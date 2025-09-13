# app.py
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import db

# Initialize database
db.init_db()

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("750x500")
        self.root.configure(bg="#2c3e50")

        # Apply ttk theme for modern look
        style = ttk.Style()
        style.theme_use("clam")

        # Title Label
        title = tk.Label(
            root,
            text="My Todo List",
            font=("Helvetica", 22, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title.pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(root, bg="#2c3e50")
        button_frame.pack(pady=5)

        btn_config = {
            "font": ("Helvetica", 12, "bold"),
            "width": 12,
            "relief": "raised",
            "bd": 2
        }

        tk.Button(button_frame, text="Add Task", command=self.add_task, bg="#27ae60", fg="white", **btn_config).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Task", command=self.edit_task, bg="#2980b9", fg="white", **btn_config).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg="#c0392b", fg="white", **btn_config).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Toggle Complete", command=self.toggle_task, bg="#f39c12", fg="black", **btn_config).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Export CSV", command=self.export_csv, bg="#8e44ad", fg="white", **btn_config).grid(row=0, column=4, padx=5)

        # Filter Buttons
        filter_frame = tk.Frame(root, bg="#2c3e50")
        filter_frame.pack(pady=5)

        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", command=self.load_tasks).pack(side="left", padx=10)
        ttk.Radiobutton(filter_frame, text="Active", variable=self.filter_var, value="active", command=self.load_tasks).pack(side="left", padx=10)
        ttk.Radiobutton(filter_frame, text="Completed", variable=self.filter_var, value="completed", command=self.load_tasks).pack(side="left", padx=10)

        # Task List (Treeview)
        columns = ("ID", "Title", "Description", "Due Date", "Completed")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)

        self.tree.pack(pady=10, fill="x")

        self.load_tasks()

    # Load tasks from DB
    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = db.get_tasks(self.filter_var.get())
        for task in tasks:
            self.tree.insert("", "end", values=(
                task[0], task[1], task[2], task[3],
                "Yes" if task[4] else "No"
            ))

    # Add task window
    def add_task(self):
        self.task_window("Add Task")

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to edit")
            return
        task_id, title, desc, due, _ = self.tree.item(selected[0])["values"]
        self.task_window("Edit Task", task_id, title, desc, due)

    def task_window(self, action, task_id=None, title="", desc="", due=""):
        win = tk.Toplevel(self.root)
        win.title(action)
        win.geometry("400x300")
        win.configure(bg="#34495e")

        tk.Label(win, text="Title:", font=("Arial", 12, "bold"), bg="#34495e", fg="white").pack(pady=5)
        title_entry = tk.Entry(win, width=40)
        title_entry.insert(0, title)
        title_entry.pack(pady=5)

        tk.Label(win, text="Description:", font=("Arial", 12, "bold"), bg="#34495e", fg="white").pack(pady=5)
        desc_entry = tk.Entry(win, width=40)
        desc_entry.insert(0, desc)
        desc_entry.pack(pady=5)

        tk.Label(win, text="Due Date:", font=("Arial", 12, "bold"), bg="#34495e", fg="white").pack(pady=5)
        due_entry = tk.Entry(win, width=40)
        due_entry.insert(0, due)
        due_entry.pack(pady=5)

        def save():
            t, d, du = title_entry.get(), desc_entry.get(), due_entry.get()
            if not t.strip():
                messagebox.showwarning("Warning", "Title cannot be empty")
                return
            if action == "Add Task":
                db.add_task(t, d, du)
            else:
                db.update_task(task_id, t, d, du)
            win.destroy()
            self.load_tasks()

        tk.Button(win, text="Save", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=save).pack(pady=15)

    def toggle_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to toggle")
            return
        task_id, _, _, _, completed = self.tree.item(selected[0])["values"]
        db.toggle_task(task_id, 0 if completed == "Yes" else 1)
        self.load_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to delete")
            return
        task_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirm", "Delete this task?")
        if confirm:
            db.delete_task(task_id)
            self.load_tasks()

    def export_csv(self):
        tasks = db.get_tasks("all")
        with open("todos_export.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Description", "Due Date", "Completed"])
            for task in tasks:
                writer.writerow([task[0], task[1], task[2], task[3], "Yes" if task[4] else "No"])
        messagebox.showinfo("Success", "Tasks exported to todos_export.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
