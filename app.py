import flet as ft

from presentation.page.tasks.tasks_page import TasksPage
from presentation.page.tasks.tasks_presenter import TasksPresenter


def main(page: ft.Page):
    """Main function that is used to start the application with Flet"""
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Create application instance
    presenter = TasksPresenter()
    tasks_page = TasksPage(presenter, page)
    page.add(tasks_page)
    presenter.bind(tasks_page)

    # Add application's root control to the page


if __name__ == "__main__":
    ft.app(target=main)
