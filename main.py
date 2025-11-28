import flet as ft
from views.unbox_view import TelaPrincipalView

class AppController:
    #lógica de navegação aqui

    def main(page: ft.Page):
        controller = AppController(page)
        app_view = TelaPrincipalView(page, controller)
        app_view.construir()
        
    if __name__ == "__main__":
        ft.app(target=main)
