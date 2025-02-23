# flet-todo-list

## Summary

Simple todo-list project writtein in flutter-based framework Flet.

This serves as an excercise in GUI application development and using related patterns (MVP)

## Features

This application features:

- A list of tasks that you can manage.
- Add and Edit description for the tasks.
- Views for All, Active and Completed tasks.
- Undo completed tasks if needed.
- Delete all completed tasks.
- Store and Load tasks in local database.

## Screenshots

Main view of the application:

![Main view](./meta/images/main-view.png)

Added some tasks, with and without description (details):

![Example tasks](./meta/images/example-tasks.png)

View with only active tasks:

![Only active tasks](./meta/images/only-active.png)

And with only completed tasks:

![Only completed tasks](./meta/images/only-completed.png)

## Install

Python version: 3.10.16

1. Create and Activate virtual environment:

    ```bash
    python -m venv .venv
    ```

    On Linux:

    ```bash
    source .venv/bin/activate
    ```

    On Windows:

    ```bash
    source .venv/scripts/activate
    ```

2. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

3. Run:

    ```bash
    python app.py
    ```
