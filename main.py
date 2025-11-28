import flet as ft
from views.unbox_view import TelaPrincipalView
from controllers.controller import Unbox_Controller
from models.unbox_model import Unbox_Model

def main(page: ft.Page):
    """
    Função principal que inicializa o MVC.
    """
    modelo = Unbox_Model()
    controlador = Unbox_Controller(model=modelo, view=None) 
    visao = TelaPrincipalView(page=page, controller=controlador)
    visao.construir()

if __name__ == "__main__":
    ft.app(target=main)