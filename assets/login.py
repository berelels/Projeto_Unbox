import flet as ft

class LoginView:
    def __init__(self, page: ft.Page, model, callback_sucesso):
        self.page = page
        self.model = model
        self.callback_sucesso = callback_sucesso
        
        # Componentes
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
        
        self.mensagem_erro = ft.Text(
            "",
            color=ft.Colors.RED,
            size=14,
            visible=False
        )
    
    def construir(self):
        """Constrói a tela de login"""
        self.page.title = "UNBOX | Login"
        self.page.window.width = 500
        self.page.window.height = 600
        self.page.window.resizable = False
        self.page.padding = 0
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Card de login
        login_card = ft.Container(
            content=ft.Column([
                # Logo/Título
                ft.Icon(
                    ft.Icons.INVENTORY_2,
                    size=80,
                    color=ft.Colors.BLUE_700
                ),
                ft.Text(
                    "UNBOX",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                ),
                ft.Text(
                    "Sistema de Inventário Escolar",
                    size=16,
                    color=ft.Colors.GREY_700
                ),
                
                ft.Divider(height=30, thickness=2),
                
                # Campos de login
                self.usuario_input,
                self.senha_input,
                
                # Mensagem de erro
                self.mensagem_erro,
                
                # Botão de login
                ft.ElevatedButton(
                    "Entrar",
                    icon=ft.Icons.LOGIN,
                    width=300,
                    height=50,
                    on_click=self.fazer_login,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),

                
                # ft.Divider(height=20),  <-- Comentei o divisor também para melhorar a estética
                
                # Info padrão
                # ft.Container(
                #     content=ft.Column([
                #         ft.Text(
                #             "Usuário padrão:",
                #             size=12,
                #             color=ft.Colors.GREY_600
                #         ),
                #         ft.Text(
                #             "Usuário: admin | Senha: admin123",
                #             size=12,
                #             weight=ft.FontWeight.BOLD,
                #             color=ft.Colors.GREY_700
                #         ),
                #     ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                #     bgcolor=ft.Colors.BLUE_50,
                #     padding=10,
                #     border_radius=8,
                #     width=300
                # ),
                
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            width=400,
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLUE_GREY_100,
            )
        )
        
        
        # Container principal com fundo
        main_container = ft.Container(
            content=login_card,
            alignment=ft.alignment.center,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_50, ft.Colors.BLUE_100]
            )
        )
        
        self.page.add(main_container)
    
    def fazer_login(self, e):
        """Realiza o login"""
        usuario = self.usuario_input.value.strip()
        senha = self.senha_input.value.strip()
        
        # Validação básica
        if not usuario or not senha:
            self.mostrar_erro("Preencha todos os campos!")
            return
        
        # Tenta validar login
        usuario_data = self.model.validar_login(usuario, senha)
        
        if usuario_data:
            # Login bem-sucedido
            self.callback_sucesso(usuario_data)
        else:
            # Login falhou
            self.mostrar_erro("❌ Usuário ou senha incorretos!")
            self.senha_input.value = ""
            self.page.update()
    
    def mostrar_erro(self, mensagem):
        """Exibe mensagem de erro"""
        self.mensagem_erro.value = mensagem
        self.mensagem_erro.visible = True
        self.page.update()