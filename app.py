import flet as ft

from view.page.task_page import TasksPage


def main(page: ft.Page):
    """Main function that is used to start the application with Flet"""
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    # Create application instance
    todo1 = TasksPage()

    # Add application's root control to the page
    page.add(todo1)


if __name__ == "__main__":
    ft.app(target=main)
