import flet as ft
from models.unbox_model import Unbox_Model
from views.unbox_view import TelaPrincipalView

class Unbox_Controller:
    def __init__(self, model, view=None):
        self.model = model
        self.view = view

    def registrar_view(self, view):
        """Método chamado pela View para se conectar ao Controller"""
        self.view = view
        self.carregar_categorias_no_dropdown()

    def handle_navigation_change(self, e):
        """Gerencia a troca de telas no NavigationRail"""
        if isinstance(e, int):
            index = e
        elif hasattr(e, "control"):
            index = e.control.selected_index
        else:
            try:
                index = int(e.data)
            except:
                index = 0

        self.view.content_area.content = ft.Container(content=ft.Text(f"Carregando tela {index}..."))
        
        if index == 0:
             self.view.content_area.content = ft.Text("Dashboard (Em construção)")
        elif index == 1:
             self.view.content_area.content = self.view._layout_cadastro_categoria()
             self.carregar_categorias_update_table()
        elif index == 2:
             self.view.content_area.content = ft.Text("Tela de Itens (Em construção)")
        elif index == 3:
             self.view.content_area.content = ft.Text("Tela de Movimentações (Em construção)")

        self.view.page.update()

    def carregar_categorias_no_dropdown(self):
        """Preenche dropdowns (se existirem na tela atual)"""
        pass 

    def carregar_categorias_update_table(self):
        """Busca categorias no banco e atualiza a tabela da View"""
        dados = self.model.get_categories()
        
        self.view.categorias_data_table.rows.clear()
        
        for cat_id, cat_nome in dados:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(cat_id))),
                ft.DataCell(ft.Text(cat_nome)),
            ])
            self.view.categorias_data_table.rows.append(row)
        
        self.view.page.update()

    def salvar_nova_categoria(self, e):
        """Chamado pelo botão Salvar na tela de Categorias"""
        nome = self.view.nome_categoria_input.value
        
        if not nome:
            self.view.page.snack_bar = ft.SnackBar(ft.Text("Digite um nome para a categoria!"), bgcolor=ft.colors.RED)
            self.view.page.snack_bar.open = True
            self.view.page.update()
            return

        self.model.create_category(nome)
        
        self.view.nome_categoria_input.value = ""
        self.view.page.snack_bar = ft.SnackBar(ft.Text(f"Categoria '{nome}' salva!"), bgcolor=ft.colors.GREEN)
        self.view.page.snack_bar.open = True
        
        self.carregar_categorias_update_table()
        self.view.page.update()