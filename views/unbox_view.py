
import flet as ft
import sqlite3
class TelaPrincipalView:
     def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        self.controller.registrar_view(self)
 
        self.categoria = None
        self.item = None
        self.historico_list = None
        
        self.content_area = ft.Container(content=ft.Text("Carregando"))
        self.navigation_rail = None
       
     def construir(self):
            
            self.page.title = "UNBOX | Sistema de Inventário Escolar"
            self.page.window_width = 1000
            self.page.window_height = 800
            self.page.window_resizable = True 
            self.page.padding = 0 
            
            
            self.navigation_rail = ft.NavigationRail(
                selected_index=0, 
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100, 
                min_extended_width=200, 
                group_alignment=-1.0, 
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.Icons.DASHBOARD_OUTLINED,
                        selected_icon=ft.Icons.DASHBOARD,
                        label="Dashboard",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.CATEGORY_OUTLINED,
                        selected_icon=ft.Icons.CATEGORY,
                        label="Categorias",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.INVENTORY_2_OUTLINED,
                        selected_icon=ft.Icons.INVENTORY_2,
                        label="Itens",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.SWAP_HORIZ_OUTLINED,
                        selected_icon=ft.Icons.SWAP_HORIZ,
                        label="Movimentações",
                    ),
                ],
                on_change=self.controller.handle_navigation_change 
            )

           
            self.content_area.expand = True 
            self.content_area.padding = ft.padding.only(left=20, top=20, right=20)
            
           
            layout_principal = ft.Row(
                controls=[
                    self.navigation_rail,
                    ft.VerticalDivider(width=1), 
                    self.content_area,
                ],
                expand=True, 
                spacing=0 
            )

           
            self.page.add(layout_principal)
            
            
            self.controller.handle_navigation_change(type("E", (), {"data": "0"}))



 
     def _layout_cadastro_categoria(self):
    
        self.nome_categoria_input = ft.TextField(
        label="Nome da Categoria (Eletrônico, Mobiliário,Esportivo,Material Didático,Limpeza)",
        width=400,
        hint_text="Nome Único (Exigência do Carlos)"
    )

        self.categorias_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
        ],
        rows=[], 
    )
    
        return ft.Column([
        ft.Text(" Cadastro de Categorias", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        
        ft.Row([
            self.nome_categoria_input,
            ft.ElevatedButton(
                "Salvar Categoria",
                icon=ft.Icons.SAVE,
                
                on_click=self.controller.salvar_nova_categoria 
            ),
        ], alignment=ft.MainAxisAlignment.START),
        
        ft.Divider(),
        
        
        ft.Text("Categorias Existentes:", size=18, weight=ft.FontWeight.W_600),
        ft.Container(
            content=self.categorias_data_table,
            
            scroll=ft.ScrollMode.ADAPTIVE, 
            expand=True 
        )
    ], expand=True)

     def _layout_movimentacao(self):
        
      
        self.input_patrimonio_emprestimo = ft.TextField(
            label="Nº do Patrimônio",
            width=250,
            hint_text="Número na plaquinha de metal do item"
        )
        self.input_pessoa_emprestimo = ft.TextField(
            label="Nome do Professor/Responsável",
            width=300,
            hint_text=" Prof. Admistrador "
        )
        self.input_patrimonio_devolucao = ft.TextField(
            label="Nº do Patrimônio",
            width=250,
            hint_text="Item a ser devolvido"
        )
        self.movimentacoes_data_table = ft.DataTable(
            columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patrimônio")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Emprestado Para")),
            ft.DataColumn(ft.Text("Desde já")),
            ft.DataColumn(ft.Text("Ação")),
            ],
            rows=[]
        )

        return ft.Column([
        ft.Text(" Emprestimo e Devoluçao", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
                          