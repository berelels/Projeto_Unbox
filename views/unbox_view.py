import flet as ft

class TelaPrincipalView:
    def __init__(self, page: ft.Page, controller, usuario_logado=None):
        self.page = page
        self.controller = controller
        self.usuario_logado = usuario_logado
        
        # Inicializa TODOS os componentes no __init__
        self._inicializar_componentes()
        
        # Layout principal
        self.content_area = ft.Container(content=ft.Text("Carregando..."))
        self.navigation_rail = None
    
    def _inicializar_componentes(self):
        """Inicializa todos os componentes uma única vez"""
        # Componentes do Dashboard
        self.low_stock_count_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE)
        self.total_items_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
        self.borrowed_items_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
        
        self.low_stock_card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=50, color=ft.Colors.ORANGE),
                ft.Text("Alerta de Estoque Baixo", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                self.low_stock_count_text,
                ft.Text("Itens abaixo do estoque mínimo", color=ft.Colors.BLACK),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=300,
            height=300,
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border=ft.border.all(5, ft.Colors.ORANGE_200),
            alignment=ft.alignment.center,
        )
        
        self.total_items_card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.INVENTORY_2, size=50, color=ft.Colors.BLUE_700),
                ft.Text("Total de Itens", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                self.total_items_text,
                ft.Text("Cadastrados no sistema", color=ft.Colors.BLACK),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=300,
            height=300,
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(5, ft.Colors.BLUE_200),
            alignment=ft.alignment.center,
        )
        
        self.borrowed_items_card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.OUTBOX, size=50, color=ft.Colors.GREEN_700),
                ft.Text("Itens Emprestados", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                self.borrowed_items_text,
                ft.Text("Saídas do estoque", color=ft.Colors.BLACK),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=300,
            height=300,
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border=ft.border.all(5, ft.Colors.GREEN_200),
            alignment=ft.alignment.center,
        )
        
        # Componentes de Categorias
        self.nome_categoria_input = ft.TextField(
            label="Nome da Categoria",
            width=400,
            hint_text="Ex: Eletrônico, Mobiliário, Esportivo...",
            prefix_icon=ft.Icons.CATEGORY
        )
        self.categorias_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
        )
        
        # Componentes de Itens
        self.patrimonio_input = ft.TextField(
            label="Nº de Patrimônio",
            width=200,
            hint_text="Ex: 001234",
            prefix_icon=ft.Icons.NUMBERS,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.nome_item_input = ft.TextField(
            label="Nome do Item",
            width=400,
            hint_text="Ex: Projetor Epson X20",
            prefix_icon=ft.Icons.INVENTORY
        )
        self.categoria_dropdown = ft.Dropdown(
            label="Categoria",
            width=300,
            hint_text="Selecione a categoria",
            prefix_icon=ft.Icons.CATEGORY,
            options=[]
        )
        self.quantidade_input = ft.TextField(
            label="Quantidade",
            width=150,
            hint_text="Ex: 10",
            prefix_icon=ft.Icons.NUMBERS,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.status_dropdown = ft.Dropdown(
            label="Status Inicial",
            width=200,
            options=[
                ft.dropdown.Option("Disponível"),
                ft.dropdown.Option("Manutenção"),
            ],
            value="Disponível"
        )
        self.itens_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Patrimônio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoria", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Qtd.", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
        )
        
        # Componentes de Usuários
        self.usuario_input = ft.TextField(
            label="Usuário",
            width=300,
            prefix_icon=ft.Icons.PERSON,
            autofocus=True
        )
        
        self.senha_input = ft.TextField(
            label="Senha",
            width=300,
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True
        )
        
        self.tipo_input = ft.Dropdown(
            options=[
                ft.dropdown.Option("ADMIN"),
                ft.dropdown.Option("DIRETOR"),
                ft.dropdown.Option("COORDENADOR"),
                ft.dropdown.Option("PROFESSOR"),
            ],
            width=300,
            label="Tipo de Usuário",
            prefix_icon=ft.Icons.BADGE,
        )
        
        self.mensagem_erro = ft.Text(
            "",
            color=ft.Colors.RED,
            size=14,
            visible=False
        )
        
        self.usuarios_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Usuário", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data Criação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
        )
        
        # Componentes de Movimentações
        self.item_emprestimo_dropdown = ft.Dropdown(
            label="Selecionar Item",
            width=400,
            hint_text="Digite para buscar...",
            options=[],
            prefix_icon=ft.Icons.SEARCH,
        )
        self.input_pessoa_emprestimo = ft.TextField(
            label="Nome do Professor/Responsável",
            width=350,
            hint_text="Ex: Prof. João Silva",
            prefix_icon=ft.Icons.PERSON
        )
        self.input_patrimonio_devolucao = ft.TextField(
            label="Nº do Patrimônio",
            width=250,
            hint_text="Item a devolver",
            prefix_icon=ft.Icons.NUMBERS
        )
        
        self.input_pessoa_devolucao = ft.TextField(
            label="Nome de quem está devolvendo",
            width=350,
            hint_text="Ex: Prof. Maria Santos",
            prefix_icon=ft.Icons.PERSON
        )
        
        self.movimentacoes_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Patrimônio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Item", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Responsável", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
        )
       
    def construir(self):
        """Constrói a interface principal"""
        self.page.title = "UNBOX | Sistema de Inventário Escolar"
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.resizable = True
        self.page.padding = 0
        
        # Navigation Rail - Adiciona aba de Usuários
        destinations = [
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
        ]
        
        # Adiciona aba de Usuários apenas para ADMIN
        if self.usuario_logado and self.usuario_logado.get("tipo") == "ADMIN":
            destinations.append(
                ft.NavigationRailDestination(
                    icon=ft.Icons.PEOPLE_OUTLINED,
                    selected_icon=ft.Icons.PEOPLE,
                    label="Usuários",
                )
            )
        
        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-1.0,
            destinations=destinations,
            on_change=self.controller.handle_navigation_change
        )

        # Área de conteúdo
        self.content_area.expand = True
        self.content_area.padding = ft.padding.only(left=20, top=20, right=20, bottom=20)
        
        # Layout principal
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
        
        # Registra view no controller
        self.controller.registrar_view(self)
        
        # Carrega dashboard inicial
        self.controller.handle_navigation_change(type("E", (), {"data": "0"}))

    def _layout_dashboard(self):
        """Layout do Dashboard - REUTILIZA componentes existentes"""
        return ft.Column([
            ft.Text("📊 Dashboard - Visão Geral", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, thickness=2),
            ft.Row([
                self.total_items_card,
                self.borrowed_items_card,
                self.low_stock_card,
            ], alignment=ft.MainAxisAlignment.START, wrap=True, spacing=20)
        ], expand=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START)

    def _layout_cadastro_categoria(self):
        """Layout de Cadastro de Categorias - REUTILIZA componentes"""
        return ft.Column([
            ft.Text("📁 Cadastro de Categorias", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, thickness=2),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Nova Categoria", size=18, weight=ft.FontWeight.W_600),
                        self.nome_categoria_input,
                        ft.ElevatedButton(
                            "Salvar Categoria",
                            icon=ft.Icons.SAVE,
                            on_click=self.controller.salvar_nova_categoria
                        ),
                    ]),
                    padding=20,
                ),
                elevation=3
            ),
            
            ft.Divider(height=20),
            
            ft.Text("Categorias Cadastradas:", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=self.categorias_data_table,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10,
            )
        ], expand=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START)

    def _layout_cadastro_item(self):
        """Layout de Cadastro de Itens - REUTILIZA componentes"""
        return ft.Column([
            ft.Text("📦 Cadastro de Itens e Ativos", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, thickness=2),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Novo Item", size=18, weight=ft.FontWeight.W_600),
                        ft.Row([
                            self.nome_item_input,
                            self.patrimonio_input,
                        ], wrap=True),
                        ft.Row([
                            self.categoria_dropdown,
                            self.quantidade_input,
                            self.status_dropdown,
                        ], wrap=True),
                        ft.ElevatedButton(
                            "Salvar Item",
                            icon=ft.Icons.SAVE,
                            on_click=self.controller.salvar_novo_item
                        ),
                    ]),
                    padding=20,
                ),
                elevation=3
            ),

            ft.Divider(height=20),
            
            ft.Text("Inventário Atual:", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=self.itens_data_table,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10,
            )
        ], expand=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START)

    def _layout_movimentacao(self):
        """Layout de Movimentações - REUTILIZA componentes COM CAMPO DE DEVOLUÇÃO"""
        return ft.Column([
            ft.Text("📤 Movimentações - Empréstimo e Devolução", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, thickness=2),

            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.OUTBOX, color=ft.Colors.BLUE_700, size=30),
                                ft.Text("Empréstimo (Saída)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_700),
                            ]),
                            ft.Divider(),
                            self.item_emprestimo_dropdown,
                            self.input_pessoa_emprestimo,
                            ft.ElevatedButton(
                                "Realizar Empréstimo",
                                icon=ft.Icons.SEND,
                                on_click=self.controller.realizar_emprestimo,
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        width=450,
                        height=370,
                    ),
                    elevation=5
                ),
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.INBOX, color=ft.Colors.GREEN_700, size=30),
                                ft.Text("Devolução (Entrada)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.GREEN_700),
                            ]),
                            ft.Divider(),
                            self.input_patrimonio_devolucao,
                            self.input_pessoa_devolucao,  # NOVO CAMPO
                            ft.ElevatedButton(
                                "Registrar Devolução",
                                icon=ft.Icons.CHECK_CIRCLE,
                                on_click=self.controller.registrar_devolucao,
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        width=450,
                        height=370,
                    ),
                    elevation=5
                ),
            ], wrap=True, alignment=ft.MainAxisAlignment.START, spacing=20),
            
            ft.Divider(height=30),
            
            ft.Text("Histórico de Movimentações:", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=self.movimentacoes_data_table,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10,
            )
        ], expand=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START)
    
    
    def _layout_usuarios(self):
        """Layout de Gerenciamento de Usuários - COMPLETO"""
        return ft.Column([
            ft.Text("👥 Gerenciamento de Usuários", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, thickness=2),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Novo Usuário", size=18, weight=ft.FontWeight.W_600),
                        ft.Divider(height=10),
                        self.usuario_input,
                        self.senha_input,
                        self.tipo_input,
                        ft.ElevatedButton(
                            text="Cadastrar Usuário",
                            width=300,
                            on_click=self.salvar_usuario_click,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE
                        ),
                        self.mensagem_erro,
                    ], horizontal_alignment=ft.CrossAxisAlignment.START),
                    padding=20,
                ),
                elevation=3
            ),
            
            ft.Divider(height=20),
            
            ft.Text("Usuários Cadastrados:", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=self.usuarios_data_table,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10,
            )
        ], expand=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START)
    
    
    def salvar_usuario_click(self, e):
        """Callback do botão de salvar usuário"""
        self.controller.salvar_novo_usuario(e)