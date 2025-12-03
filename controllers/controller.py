import flet as ft
from models.unbox_model import Unbox_Model
from datetime import datetime
import os
from fpdf import FPDF
import pandas as pd
 
class Unbox_Controller:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = Unbox_Model()
        self.view = None
 
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
        
        if index == 0:  # Dashboard
            self.view.content_area.content = self.view._layout_dashboard()
            self.carregar_dashboard_stats()
        elif index == 1:  # Categorias
            self.view.content_area.content = self.view._layout_cadastro_categoria()
            self.carregar_categorias_tabela()
        elif index == 2:  # Itens
            self.view.content_area.content = self.view._layout_cadastro_item()
            self.preencher_categorias()
            self.carregar_itens_tabela()
        elif index == 3:  # Movimentações
            self.view.content_area.content = self.view._layout_movimentacao()
            self.carregar_itens_disponiveis()
            self.carregar_movimentacoes_tabela()
        
        self.page.update()
 
    def carregar_dashboard_stats(self):
        """Carrega estatísticas do dashboard"""
        try:
            if not self.view:
                return
                
            stats = self.model.get_dashboard_stats()
            print(f"[DEBUG] Stats carregados: {stats}")  # Debug
            
            # Atualiza low stock
            if hasattr(self.view, 'low_stock_count_text') and self.view.low_stock_count_text:
                self.view.low_stock_count_text.value = str(stats.get('low_stock', 0))
            
            # Atualiza total de itens
            if hasattr(self.view, 'total_items_text') and self.view.total_items_text:
                self.view.total_items_text.value = str(stats.get('total_items', 0))
            
            # Atualiza itens emprestados
            if hasattr(self.view, 'borrowed_items_text') and self.view.borrowed_items_text:
                self.view.borrowed_items_text.value = str(stats.get('borrowed_items', 0))
            
            self.page.update()
            print("[DEBUG] Dashboard atualizado com sucesso!")  # Debug
            
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
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(id_cat))),
                    ft.DataCell(ft.Text(nome_cat)),
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
            
            # Cria local padrão se não existir
            self.model.create_location("Estoque Principal", "Principal")
            
            # Cria o item
            self.model.create_item(
                name=nome,
                serial_number=patrimonio,
                category_name=categoria,
                location_name="Estoque Principal",
                min_stock=1
            )
            
            # Adiciona quantidade inicial
            self.model.create_staff("Sistema", "Sistema")
            self.model.register_movement(patrimonio, "IN", int(quantidade), "Sistema")
            
            self.mostrar_snackbar(f"Item '{nome}' cadastrado!", ft.Colors.GREEN)
            self.limpar_campos_item()
            self.carregar_itens_tabela()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro ao salvar item: {ex}", ft.Colors.RED)
 
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
                
                # Busca nome da categoria
                categorias = self.model.obter_categorias()
                nome_cat = next((c[1] for c in categorias if c[0] == cat_id), "N/A")
                
                # Define status
                status_text = "Disponível" if qtd > 0 else "Sem estoque"
                status_color = ft.Colors.GREEN if qtd > 0 else ft.Colors.RED
                
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
                ])
                self.view.itens_data_table.rows.append(row)
            
            self.page.update()
            
        except Exception as e:
            print(f"Erro ao carregar itens: {e}")
 
    def carregar_itens_disponiveis(self):
        """Carrega itens disponíveis no dropdown de empréstimo"""
        try:
            if not self.view or not hasattr(self.view, 'item_emprestimo_dropdown'):
                return
                
            self.view.item_emprestimo_dropdown.options.clear()
            itens = self.model.get_items_paginated(1, 100)
            
            for item in itens:
                id_item, nome, serial, cat_id, loc_id, qtd, min_stock = item
                if qtd > 0:  # Apenas itens disponíveis
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
            
            # Cria staff se não existir
            self.model.create_staff(pessoa, "Professor")
            
            # Registra saída
            self.model.register_movement(item_selecionado, "OUT", 1, pessoa)
            
            self.mostrar_snackbar(f"Empréstimo registrado para {pessoa}!", ft.Colors.GREEN)
            self.gerar_recibo_pdf(item_selecionado, pessoa)
            
            # Limpa campos
            self.view.item_emprestimo_dropdown.value = None
            self.view.input_pessoa_emprestimo.value = ""
            
            self.carregar_itens_disponiveis()
            self.carregar_movimentacoes_tabela()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro ao realizar empréstimo: {ex}", ft.Colors.RED)
 
    def registrar_devolucao(self, e):
        """Registra devolução de item"""
        try:
            patrimonio = self.view.input_patrimonio_devolucao.value.strip()
            
            if not patrimonio:
                self.mostrar_snackbar("Informe o patrimônio!", ft.Colors.ORANGE)
                return
            
            # Registra entrada (sistema)
            self.model.register_movement(patrimonio, "IN", 1, "Sistema")
            
            self.mostrar_snackbar(f"Devolução registrada: {patrimonio}", ft.Colors.BLUE)
            self.view.input_patrimonio_devolucao.value = ""
            
            self.carregar_itens_disponiveis()
            self.carregar_movimentacoes_tabela()
            
        except Exception as ex:
            self.mostrar_snackbar(f"Erro ao registrar devolução: {ex}", ft.Colors.RED)
 
    def carregar_movimentacoes_tabela(self):
        """Carrega movimentações na tabela"""
        try:
            if not self.view or not hasattr(self.view, 'movimentacoes_data_table'):
                return
                
            # Por enquanto, deixa vazio - implementar consulta de movimentos ativos
            self.view.movimentacoes_data_table.rows.clear()
            self.page.update()
            
        except Exception as e:
            print(f"Erro ao carregar movimentações: {e}")
 
    def gerar_recibo_pdf(self, patrimonio, pessoa):
        """Gera recibo em PDF"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="RECIBO DE EMPRESTIMO DE ATIVO", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=12)
            texto = f"""
Declaro que recebi o item abaixo listado em perfeitas condicoes de uso.
Comprometo-me a devolve-lo quando solicitado.

Dados do Emprestimo:
------------------------------------------------
Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Responsavel: {pessoa}
Item Patrimonio: {patrimonio}
------------------------------------------------
            """
            pdf.multi_cell(0, 10, txt=texto)
            pdf.ln(20)
            
            pdf.cell(200, 10, txt="_" * 50, ln=1, align='C')
            pdf.cell(200, 10, txt="Assinatura do Responsavel", ln=1, align='C')
            
            nome_arquivo = f"recibo_{patrimonio}.pdf"
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
            self.mostrar_snackbar(f"Erro ao exportar: {ex}", ft.Colors.RED)
 
    def mostrar_snackbar(self, mensagem, cor):
        """Exibe snackbar com mensagem"""
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=cor
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()