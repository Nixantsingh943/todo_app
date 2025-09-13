
# Todo App (Python, Tkinter, SQLite)

This is a simple desktop Todo application built with Python, Tkinter for the graphical user interface, and SQLite for persistent storage.  
It allows users to add, edit, delete, mark tasks as complete, and export tasks to a CSV file.

## Features
- Add new tasks with title, description, and due date
- Edit existing tasks
- Delete tasks
- Mark tasks as completed or active
- Filter tasks (All, Active, Completed)
- Export tasks to a CSV file
- Data stored locally in SQLite database

## Requirements
- Python 3.x
- Tkinter (Python standard library, install with `sudo apt-get install python3-tk` on Ubuntu if missing)
- SQLite (bundled with Python)

## Installation
1. Clone the repository:
     ```bash
     git clone https://github.com/Nixantsingh943/todo_app.git
   cd todo_app
    ````

2. Run the application:

   ```bash
   python3 app.py
   ```

## Project Structure

```
todo_app/
│── app.py        # Main Tkinter GUI application
│── db.py         # SQLite database handler
│── README.md     # Project documentation
│── .gitignore    # Git ignore rules
```

## Usage

* Launch the app using `python3 app.py`
* Use the **Add** button to create a new task
* Select a task and click **Edit** or **Delete** to modify it
* Use **Toggle Complete** to mark a task as done
* Use the filter buttons to switch between All, Active, and Completed tasks
* Use **Export CSV** to export all tasks to a `todos_export.csv` file



