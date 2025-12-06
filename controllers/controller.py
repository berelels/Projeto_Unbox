import flet as ft
from models.unbox_model import Unbox_Model
from views.unbox_view import TelaPrincipalView
from datetime import datetime
import pytz
import os
from fpdf import FPDF
import pandas as pd
 
class Unbox_Controller:
    def __init__(self, page: ft.Page, usuario_logado=None):
        self.page = page
        self.model = Unbox_Model()
        self.view = None
        self.timezone = pytz.timezone('America/Sao_Paulo')
        self.usuario_logado = usuario_logado
        
        print(f"[DEBUG] Controller iniciado com usuário: {self.usuario_logado}")
 
    def registrar_view(self, view):
        """Registra a view no controller"""
        self.view = view
        self.preencher_categorias()
        self.carregar_dashboard_stats()
 
    def preencher_categorias(self):
        """Preenche o dropdown de categorias"""
        try:
            if not self.view or not hasattr(self.view, 'categoria_dropdown'):
                return
                
            dados_categorias = self.model.obter_categorias()
            opcoes_drop = []
            for id, nome in dados_categorias:
                opcoes_drop.append(ft.dropdown.Option(text=nome))
            
            self.view.categoria_dropdown.options = opcoes_drop
            self.page.update()
               
        except Exception as e:
            if self.view:
                self.mostrar_snackbar(f"Erro ao carregar categorias: {e}", ft.Colors.RED)
 
    def handle_navigation_change(self, e):
        """Manipula mudanças na navegação"""
        if not self.view:
            return
            
        index = int(e.data) if hasattr(e, 'data') else e
        
        print(f"[DEBUG] Navegação mudou para índice: {index}")
        print(f"[DEBUG] Usuário logado: {self.usuario_logado}")
        print(f"[DEBUG] Tipo do usuário: {self.usuario_logado.get('tipo') if self.usuario_logado else 'NENHUM'}")
        
        if index == 0:  # Dashboard
            self.view.content_area.content = self.view._layout_dashboard()
            self.carregar_dashboard_stats()
        elif index == 1:  # Categorias
            self.view.content_area.content = self.view._layout_cadastro_categoria()
            self.view.categorias_data_table.rows.clear()
            self.carregar_categorias_tabela()
        elif index == 2:  # Itens
            self.view.content_area.content = self.view._layout_cadastro_item()
            self.preencher_categorias()
            self.view.itens_data_table.rows.clear()
            self.carregar_itens_tabela()
        elif index == 3:  # Movimentações
            self.view.content_area.content = self.view._layout_movimentacao()
            self.carregar_itens_disponiveis()
            self.carregar_movimentacoes_tabela()
        elif index == 4:  # Usuários (apenas para ADMIN)
            print(f"[DEBUG] Tentando acessar aba de Usuários...")
            
            if self.usuario_logado and self.usuario_logado.get("tipo") == "ADMIN":
                print("[DEBUG] ✅ Acesso concedido! Carregando tela de usuários...")
                self.view.content_area.content = self.view._layout_usuarios()
                self.carregar_usuarios_tabela()
            else:
                print(f"[DEBUG] ❌ Acesso negado! Tipo: {self.usuario_logado.get('tipo') if self.usuario_logado else 'NENHUM'}")
                self.mostrar_snackbar("❌ Acesso negado! Apenas ADMIN pode gerenciar usuários.", ft.Colors.RED)
                # Volta para o Dashboard
                self.view.navigation_rail.selected_index = 0
                self.view.content_area.content = self.view._layout_dashboard()
                self.carregar_dashboard_stats()
        
        self.page.update()

    def salvar_novo_usuario(self, e):
        """Salva um novo usuário"""
        try:
            nome = self.view.usuario_input.value.strip()
            senha = self.view.senha_input.value.strip()
            tipo = self.view.tipo_input.value
            
            if not all([nome, senha, tipo]):
                self.mostrar_snackbar("Preencha todos os campos!", ft.Colors.ORANGE)
                return
            
            # Cria o usuário
            self.model.criar_usuario(nome, senha, tipo, self.usuario_logado["usuario"])
            
            self.mostrar_snackbar(f"✅ Usuário '{nome}' cadastrado com sucesso!", ft.Colors.GREEN)
            
            # Limpa campos
            self.view.usuario_input.value = ""
            self.view.senha_input.value = ""
            self.view.tipo_input.value = None
            
            # Recarrega tabela
            self.carregar_usuarios_tabela()
            
        except ValueError as ex:
            self.mostrar_snackbar(f"❌ {str(ex)}", ft.Colors.RED)
        except Exception as ex:
            self.mostrar_snackbar(f"Erro ao salvar usuário: {ex}", ft.Colors.RED)

    def carregar_usuarios_tabela(self):
        """Carrega usuários na tabela com botão de deletar"""
        try:
            if not self.view or not hasattr(self.view, 'usuarios_data_table'):
                return
            
            self.view.usuarios_data_table.rows.clear()
            usuarios = self.model.obter_usuarios()
            
            print(f"[DEBUG] Carregando {len(usuarios)} usuários na tabela...")
            
            for user in usuarios:
                nome = user["usuario"]
                tipo = user["tipo"]
                data_criacao = user.get("data_criacao", "N/A")
                
                # Botão de deletar - NÃO PODE DELETAR ADMIN
                if tipo == "ADMIN":
                    btn_deletar = ft.Container(
                        content=ft.Text("🔒 Protegido", color=ft.Colors.RED, size=12),
                    )
                else:
                    btn_deletar = ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Deletar usuário",
                        on_click=lambda e, user_name=nome: self.deletar_usuario(user_name)
                    )
                
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nome)),
                    ft.DataCell(ft.Text(tipo)),
                    ft.DataCell(ft.Text(data_criacao)),
                    ft.DataCell(btn_deletar),
                ])
                self.view.usuarios_data_table.rows.append(row)
            
            self.page.update()
            print("[DEBUG] ✅ Tabela de usuários atualizada!")
            
        except Exception as e:
            print(f"[ERRO] Erro ao carregar usuários: {e}")
            import traceback
            traceback.print_exc()

    def deletar_usuario(self, nome_usuario):
        """Deleta um usuário após confirmação"""
        def confirmar_exclusao(e):
            try:
                self.model.excluir_usuario(nome_usuario, self.usuario_logado["usuario"])
                self.mostrar_snackbar(f"✅ Usuário '{nome_usuario}' deletado!", ft.Colors.GREEN)
                self.carregar_usuarios_tabela()
                dialog.open = False
                self.page.update()
            except Exception as ex:
                self.mostrar_snackbar(f"❌ {str(ex)}", ft.Colors.RED)
                dialog.open = False
                self.page.update()
        
        def cancelar(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente deletar o usuário '{nome_usuario}'?\n\nEsta ação não pode ser desfeita!"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Deletar", on_click=confirmar_exclusao, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
 
    def carregar_dashboard_stats(self):
        """Carrega estatísticas do dashboard"""
        try:
            if not self.view:
                return
                
            stats = self.model.get_dashboard_stats()
            
            if hasattr(self.view, 'low_stock_count_text') and self.view.low_stock_count_text:
                self.view.low_stock_count_text.value = str(stats.get('low_stock', 0))
            
            if hasattr(self.view, 'total_items_text') and self.view.total_items_text:
                self.view.total_items_text.value = str(stats.get('total_items', 0))
            
            if hasattr(self.view, 'borrowed_items_text') and self.view.borrowed_items_text:
                self.view.borrowed_items_text.value = str(stats.get('borrowed_items', 0))
            
            self.page.update()
            
        except Exception as e:
            print(f"[ERRO] Erro ao carregar dashboard: {e}")
            import traceback
            traceback.print_exc()
 
    def salvar_nova_categoria(self, e):
        """Salva uma nova categoria"""
        try:
            nome = self.view.nome_categoria_input.value.strip()
            
            if not nome:
                self.mostrar_snackbar("Digite o nome da categoria!", ft.Colors.ORANGE)
                return
            
            self.model.create_category(nome)
            self.mostrar_snackbar(f"Categoria '{nome}' cadastrada!", ft.Colors.GREEN)
            self.view.nome_categoria_input.value = ""
            
            self.view.categorias_data_table.rows.clear()
            self.carregar_categorias_tabela()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro ao salvar categoria: {ex}", ft.Colors.RED)
 
    def carregar_categorias_tabela(self):
        """Carrega categorias na tabela"""
        try:
            if not self.view or not hasattr(self.view, 'categorias_data_table'):
                return
                
            self.view.categorias_data_table.rows.clear()
            categorias = self.model.obter_categorias()
            
            for id_cat, nome_cat in categorias:
                btn_deletar = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED,
                    tooltip="Deletar categoria",
                    on_click=lambda e, cat_id=id_cat, nome=nome_cat: self.deletar_categoria(cat_id, nome)
                )
                
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(id_cat))),
                    ft.DataCell(ft.Text(nome_cat)),
                    ft.DataCell(btn_deletar),
                ])
                self.view.categorias_data_table.rows.append(row)
            
            self.page.update()
            
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
 
    def salvar_novo_item(self, e):
        """Salva um novo item"""
        try:
            patrimonio = self.view.patrimonio_input.value.strip()
            nome = self.view.nome_item_input.value.strip()
            categoria = self.view.categoria_dropdown.value
            quantidade = self.view.quantidade_input.value.strip()
            
            if not all([patrimonio, nome, categoria, quantidade]):
                self.mostrar_snackbar("Preencha todos os campos!", ft.Colors.ORANGE)
                return
            
            if self.model.verifica_patrimonio_existe(patrimonio):
                self.mostrar_snackbar(f"❌ Patrimônio '{patrimonio}' já cadastrado!", ft.Colors.RED)
                return
            
            self.model.create_location("Estoque Principal", "Principal")
            self.model.create_item(
                name=nome,
                serial_number=patrimonio,
                category_name=categoria,
                location_name="Estoque Principal",
                min_stock=1
            )
            
            self.model.create_staff("Sistema", "Sistema")
            self.model.register_movement(patrimonio, "IN", int(quantidade), "Sistema")
            
            self.mostrar_snackbar(f"✅ Item '{nome}' cadastrado!", ft.Colors.GREEN)
            self.limpar_campos_item()
            
            self.view.itens_data_table.rows.clear()
            self.carregar_itens_tabela()
            self.carregar_dashboard_stats()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro: {ex}", ft.Colors.RED)
 
    def limpar_campos_item(self):
        """Limpa os campos do formulário de item"""
        if self.view:
            self.view.patrimonio_input.value = ""
            self.view.nome_item_input.value = ""
            self.view.quantidade_input.value = ""
            self.view.categoria_dropdown.value = None
            self.page.update()
 
    def carregar_itens_tabela(self):
        """Carrega itens na tabela"""
        try:
            if not self.view or not hasattr(self.view, 'itens_data_table'):
                return
                
            self.view.itens_data_table.rows.clear()
            itens = self.model.get_items_paginated(1, 100)
            
            for item in itens:
                id_item, nome, serial, cat_id, loc_id, qtd, min_stock = item
                
                categorias = self.model.obter_categorias()
                nome_cat = next((c[1] for c in categorias if c[0] == cat_id), "N/A")
                
                if qtd <= min_stock and qtd > 0:
                    status_text = "⚠️ Estoque Baixo"
                    status_color = ft.Colors.ORANGE
                elif qtd > min_stock:
                    status_text = "Disponível"
                    status_color = ft.Colors.GREEN
                else:
                    status_text = "Sem estoque"
                    status_color = ft.Colors.RED
                
                btn_deletar = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED,
                    tooltip="Deletar item",
                    on_click=lambda e, patrimonio=serial, n=nome: self.deletar_item(patrimonio, n)
                )
                
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(serial)),
                    ft.DataCell(ft.Text(nome)),
                    ft.DataCell(ft.Text(nome_cat)),
                    ft.DataCell(ft.Text(str(qtd))),
                    ft.DataCell(ft.Container(
                        content=ft.Text(status_text, color="white", size=12),
                        bgcolor=status_color,
                        padding=5,
                        border_radius=5
                    )),
                    ft.DataCell(btn_deletar),
                ])
                self.view.itens_data_table.rows.append(row)
            
            self.page.update()
            
        except Exception as e:
            print(f"Erro ao carregar itens: {e}")
 
    def carregar_itens_disponiveis(self):
        """Carrega itens disponíveis no dropdown"""
        try:
            if not self.view or not hasattr(self.view, 'item_emprestimo_dropdown'):
                return
                
            self.view.item_emprestimo_dropdown.options.clear()
            itens = self.model.get_items_paginated(1, 100)
            
            for item in itens:
                id_item, nome, serial, cat_id, loc_id, qtd, min_stock = item
                if qtd > 0:
                    opcao = ft.dropdown.Option(
                        key=serial,
                        text=f"{serial} - {nome} (Qtd: {qtd})"
                    )
                    self.view.item_emprestimo_dropdown.options.append(opcao)
            
            self.page.update()
            
        except Exception as e:
            print(f"Erro ao carregar itens disponíveis: {e}")
 
    def realizar_emprestimo(self, e):
        """Realiza empréstimo de item"""
        try:
            item_selecionado = self.view.item_emprestimo_dropdown.value
            pessoa = self.view.input_pessoa_emprestimo.value.strip()
            
            if not item_selecionado or not pessoa:
                self.mostrar_snackbar("Selecione um item e informe o responsável!", ft.Colors.ORANGE)
                return
            
            self.model.create_staff(pessoa, "Professor")
            self.model.register_movement(item_selecionado, "OUT", 1, pessoa)
            
            self.mostrar_snackbar(f"✅ Empréstimo registrado para {pessoa}!", ft.Colors.GREEN)
            self.gerar_recibo_pdf(item_selecionado, pessoa)
            
            self.view.item_emprestimo_dropdown.value = None
            self.view.input_pessoa_emprestimo.value = ""
            
            self.carregar_itens_disponiveis()
            self.carregar_movimentacoes_tabela()
            self.carregar_dashboard_stats()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro: {ex}", ft.Colors.RED)
 
    def registrar_devolucao(self, e):
        """Registra devolução de item"""
        try:
            patrimonio = self.view.input_patrimonio_devolucao.value.strip()
            pessoa_devolvendo = self.view.input_pessoa_devolucao.value.strip()
            
            if not patrimonio or not pessoa_devolvendo:
                self.mostrar_snackbar("Preencha todos os campos!", ft.Colors.ORANGE)
                return
            
            ultimo_responsavel = self.model.verificar_ultimo_emprestimo(patrimonio)
            
            if not ultimo_responsavel:
                self.mostrar_snackbar(f"❌ Item '{patrimonio}' não está emprestado!", ft.Colors.RED)
                return
            
            if pessoa_devolvendo.strip().lower() != ultimo_responsavel.strip().lower():
                self.mostrar_snackbar(f"❌ Apenas '{ultimo_responsavel}' pode devolver!", ft.Colors.RED)
                return
            
            self.model.create_staff(pessoa_devolvendo, "Professor")
            self.model.register_movement(patrimonio, "IN", 1, pessoa_devolvendo)
            
            self.mostrar_snackbar(f"✅ Devolução registrada!", ft.Colors.BLUE)
            self.view.input_patrimonio_devolucao.value = ""
            self.view.input_pessoa_devolucao.value = ""
            
            self.carregar_itens_disponiveis()
            self.carregar_movimentacoes_tabela()
            self.carregar_dashboard_stats()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro: {ex}", ft.Colors.RED)
 
    def formatar_timestamp_local(self, timestamp_str):
        """Converte timestamp UTC para horário local"""
        try:
            if isinstance(timestamp_str, str):
                formatos = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M:%S.%f",
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%dT%H:%M:%S.%f"
                ]
                
                data_obj = None
                for formato in formatos:
                    try:
                        data_obj = datetime.strptime(timestamp_str, formato)
                        break
                    except ValueError:
                        continue
                
                if data_obj is None:
                    return timestamp_str
            else:
                data_obj = timestamp_str
            
            utc_tz = pytz.UTC
            if data_obj.tzinfo is None:
                data_obj = utc_tz.localize(data_obj)
            
            local_dt = data_obj.astimezone(self.timezone)
            return local_dt.strftime("%d/%m/%Y %H:%M:%S")
            
        except Exception as e:
            return timestamp_str
 
    def carregar_movimentacoes_tabela(self):
        """Carrega movimentações na tabela"""
        try:
            if not self.view or not hasattr(self.view, 'movimentacoes_data_table'):
                return
                
            self.view.movimentacoes_data_table.rows.clear()
            movimentos = self.model.get_recent_movements(50)
            
            for mov in movimentos:
                mov_id, inv_id, staff_id, tipo, qtd, timestamp, item_nome, item_serial, staff_nome = mov
                
                tipo_text = "Saída" if tipo == "OUT" else "Entrada"
                tipo_color = ft.Colors.RED if tipo == "OUT" else ft.Colors.GREEN
                data_formatada = self.formatar_timestamp_local(timestamp)
                
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(mov_id))),
                    ft.DataCell(ft.Text(item_serial)),
                    ft.DataCell(ft.Text(item_nome)),
                    ft.DataCell(ft.Text(staff_nome)),
                    ft.DataCell(ft.Text(data_formatada)),
                    ft.DataCell(ft.Container(
                        content=ft.Text(tipo_text, color="white", size=12),
                        bgcolor=tipo_color,
                        padding=5,
                        border_radius=5
                    )),
                ])
                self.view.movimentacoes_data_table.rows.append(row)
            
            self.page.update()
            
        except Exception as e:
            print(f"Erro ao carregar movimentações: {e}")
 
    def gerar_recibo_pdf(self, patrimonio, pessoa):
        """Gera recibo em PDF"""
        try:
            item_info = self.model.buscar_item_por_patrimonio(patrimonio)
            if not item_info:
                return
            
            nome_item = item_info[1]
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="RECIBO DE EMPRESTIMO", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=12)
            
            agora_local = datetime.now(self.timezone)
            data_formatada = agora_local.strftime("%d/%m/%Y %H:%M:%S")
            codigo_pessoa = f"{abs(hash(pessoa)) % 1000:03d}"
            
            texto = f"""
Item: {nome_item}
Patrimonio: {patrimonio}
Responsavel: {pessoa}
Codigo: {codigo_pessoa}
Data: {data_formatada}
            """
            pdf.multi_cell(0, 10, txt=texto)
            
            nome_arquivo = f"recibo_{patrimonio}_{codigo_pessoa}.pdf"
            pdf.output(nome_arquivo)
            os.startfile(nome_arquivo)
            
        except Exception as ex:
            print(f"Erro ao gerar PDF: {ex}")
 
    def exportar_relatorio(self, e):
        """Exporta relatório Excel"""
        try:
            itens = self.model.get_items_paginated(1, 1000)
            df = pd.DataFrame(itens, columns=[
                "ID", "Nome", "Patrimonio", "Categoria", "Local", "Quantidade", "Min Stock"
            ])
            
            df.to_excel("inventario_escolar.xlsx", index=False)
            self.mostrar_snackbar("Relatório exportado!", ft.Colors.BLUE)
            os.startfile(".")
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro: {ex}", ft.Colors.RED)
 
    def mostrar_snackbar(self, mensagem, cor):
        """Exibe snackbar com mensagem"""
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=cor
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()
    
    def deletar_categoria(self, categoria_id, nome_categoria):
        """Deleta uma categoria"""
        def confirmar_exclusao(e):
            try:
                self.model.deletar_categoria(categoria_id)
                self.mostrar_snackbar(f"✅ Categoria deletada!", ft.Colors.GREEN)
                self.view.categorias_data_table.rows.clear()
                self.carregar_categorias_tabela()
                dialog.open = False
                self.page.update()
            except Exception as ex:
                self.mostrar_snackbar(f"❌ {str(ex)}", ft.Colors.RED)
                dialog.open = False
                self.page.update()
        
        def cancelar(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar Exclusão"),
            content=ft.Text(f"Deseja deletar '{nome_categoria}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Deletar", on_click=confirmar_exclusao, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def deletar_item(self, patrimonio, nome_item):
        """Deleta um item"""
        def confirmar_exclusao(e):
            try:
                self.model.deletar_item(patrimonio)
                self.mostrar_snackbar(f"✅ Item deletado!", ft.Colors.GREEN)
                self.view.itens_data_table.rows.clear()
                self.carregar_itens_tabela()
                self.carregar_dashboard_stats()
                dialog.open = False
                self.page.update()
            except Exception as ex:
                self.mostrar_snackbar(f"❌ {str(ex)}", ft.Colors.RED)
                dialog.open = False
                self.page.update()
        
        def cancelar(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar Exclusão"),
            content=ft.Text(f"Deseja deletar '{nome_item}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Deletar", on_click=confirmar_exclusao, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()