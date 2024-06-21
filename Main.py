import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append({"task": task, "completed": False})

    def view_tasks(self):
        return self.tasks

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            del self.tasks[task_number - 1]
        else:
            print("Invalid task number")

    def mark_task_completed(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]["completed"] = True
        else:
            print("Invalid task number")

    def save_tasks(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.tasks, file)

    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            print("No saved tasks found.")

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        
        self.todo_list = ToDoList()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_entry = tk.Entry(self.frame, width=50)
        self.task_entry.grid(row=0, column=0, padx=10)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1)

        self.tasks_listbox = tk.Listbox(self.root, width=60, height=15)
        self.tasks_listbox.pack(pady=10)

        self.complete_button = tk.Button(self.root, text="Mark as Completed", command=self.mark_task_completed)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.todo_list.add_task(task)
            self.task_entry.delete(0, tk.END)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for i, task in enumerate(self.todo_list.view_tasks()):
            status = "Completed" if task["completed"] else "Pending"
            self.tasks_listbox.insert(tk.END, f"{i + 1}. {task['task']} - {status}")

    def mark_task_completed(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task_number = selected_task_index[0] + 1
            self.todo_list.mark_task_completed(task_number)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task.")

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task_number = selected_task_index[0] + 1
            self.todo_list.delete_task(task_number)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task.")

    def save_tasks(self):
        filename = simpledialog.askstring("Save Tasks", "Enter the filename:")
        if filename:
            self.todo_list.save_tasks(filename)
            messagebox.showinfo("Info", "Tasks saved successfully.")
        else:
            messagebox.showwarning("Warning", "You must enter a filename.")

    def load_tasks(self):
        filename = simpledialog.askstring("Load Tasks", "Enter the filename:")
        if filename:
            self.todo_list.load_tasks(filename)
            self.update_tasks_listbox()
            messagebox.showinfo("Info", "Tasks loaded successfully.")
        else:
            messagebox.showwarning("Warning", "You must enter a filename.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
