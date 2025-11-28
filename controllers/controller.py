import flet as ft
from models import Unbox_Model
from views import TelaPrincipalView

class Unbox_Controller:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = TelaPrincipalView()
        self.view = TelaPrincipalView(page)

        self.view.controller = self
        self.view.carregar_interface()
        self.preencher_categorias()

    def preencher_categorias(self):
        try:
            dados_categorias = self.model.obter_categorias()
            opcoes_drop = []
            for id, nome in dados_categorias:
                opcoes_drop.append(ft.dropdown.Option(text=nome))
                
        except Exception as e:
            self.view.mostrar_mensagem(f"Erro ao carregar categorias: {e}", ft.colors.RED)
        self.view.dd_categoria.options = opcoes_drop

    def salvar_item(self, e):
        patrimonio = self.view.txt_patrimonio.value
        nome_item = self.view.txt_nome.value
        categoria = self.view.dd_categoria.value

        if not patrimonio or not nome_item or not categoria:
            self.view.mostrar_mensagem("Atenção: Preencha todos os campos!", ft.colors.ORANGE)
            self.view.txt_patrimonio.focus()
            return
        
        resultado = self.model.insert_item(patrimonio, nome_item, categoria)
        #caminho certo:
        if resultado == "Sucesso":
            self.view.mostrar_mensagem(f"Item '{nome_item}' cadastrado com sucesso!", ft.colors.GREEN)
            self.view.limpar_campos()
        #caminho errado:
        elif resultado == "Erro_duplicado":
            self.view.mostrar_mensagem(f"ERRO: O Patrimônio '{patrimonio}' já existe no sistema.", ft.colors.RED)
            self.view.txt_patrimonio.focus()

        else:
            #erro genérico
            self.view.mostrar_mensagem(f"Erro interno do sistema: {resultado}", ft.colors.RED_900)
 
        #atualizando a UI
        self.page.update()
