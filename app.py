import flet as ft
from modules.todo_list import TodoList

def main(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    todo = TodoList()

    # add application's root control to the page
    page.add(todo)

if __name__ == '__main__':
    ft.app(target=main)