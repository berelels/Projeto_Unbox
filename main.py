import flet as ft
from views.unbox_view import TelaPrincipalView
from assets.login import LoginView 
from controllers.controller import Unbox_Controller
from models.unbox_model import Unbox_Model

def main(page: ft.Page):
    user_model = Unbox_Model()
    usuario_logado = None
    
    def iniciar_sistema(user_data):
        nonlocal usuario_logado
        usuario_logado = user_data
        
        page.clean()
        page.controls.clear()
        page.window.width = 1200
        page.window.height = 800
        page.window.resizable = True
        page.title = f"UNBOX | {usuario_logado['usuario']} ({usuario_logado['tipo']})"
        
        # ✅ PASSAR usuario_logado para o controller
        controller = Unbox_Controller(page, usuario_logado=usuario_logado)
        view = TelaPrincipalView(page=page, controller=controller, usuario_logado=usuario_logado)
        view.construir()
        adicionar_barra_usuario(view)
    
    def adicionar_barra_usuario(view):
        def fazer_logout(e):
            user_model.logout()
            page.clean()
            page.controls.clear()
            main(page)
        
        barra_usuario = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE),
                ft.Text(
                    f"{usuario_logado['usuario']} ({usuario_logado['tipo']})",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Sair",
                    on_click=fazer_logout
                ),
            ], spacing=10),
            bgcolor=ft.Colors.BLUE_700,
            padding=10,
        )
        
        page.controls.insert(0, barra_usuario)
        page.update()
    
    login_view = LoginView(page, user_model, iniciar_sistema)
    login_view.construir()

if __name__ == "__main__":
    ft.app(target=main)
