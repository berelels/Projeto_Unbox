import flet as ft
from models import Unbox_Model
from views import TelaPrincipalView
from datetime import datetime
import os
from fpdf import FPDF
import pandas as pd

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
            #erro genérico
            self.view.mostrar_mensagem(f"Erro interno do sistema: {resultado}", ft.colors.RED_900)
 
        #atualizando a UI
        self.page.update()

#CONTINUAÇÃO DO CONTROLLER COM BASE NOS REQUISITOS FUNCIONAIS

    def carregar_dashboard(self):
        stats = self.model.get_dashboard_stats()
        print(f"Stats carregados: {stats}")
    #RF 50:
    def registrar_emprestimo(self, e):
        patrimonio = self.view.txt_emp_patrimonio.value.strip()
        pessoa = self.view.txt_emp_pessoa.value.strip()
        if not patrimonio or not pessoa:
            self.view.mostrar_mensagem("Erro: Informe Patrimônio e Responsável.", ft.colors.ORANGE)
            return
        resultado = self.model.registrar_emprestimo(patrimonio, pessoa)
        if resultado == "POSITIVO":
            self.view.mostrar_mensagem(f"Saída registrada: {patrimonio} -> {pessoa}", ft.colors.GREEN)
            self.view.limpar_campos_emprestimo()
            self.carregar_dashboard_stats()
            self.carregar_lista_itens()
    #RF 51:          
            self.gerar_recibo_pdf(patrimonio, pessoa)
        elif resultado == "ITEM_INDISPONIVEL":
            self.view.mostrar_mensagem(f"Erro: Item {patrimonio} não existe ou já está emprestado!", ft.colors.RED)
        else:
            self.view.mostrar_mensagem(f"Erro no banco: {resultado}", ft.colors.RED_900)
           
    #RF 53: check-in inteligente
    
    def acao_registrar_devolucao(self, e):
        patrimonio = self.view.txt_emp_patrimonio.value.strip()
        if not patrimonio:
            self.view.mostrar_mensagem("Digite o Patrimônio para devolver.", ft.colors.ORANGE)
            return
        resultado = self.model.registrar_devolucao(patrimonio)
        if resultado == "SUCESSO":
            self.view.mostrar_mensagem(f"Item {patrimonio} devolvido com sucesso!", ft.colors.BLUE)
            self.view.limpar_campos_emprestimo()
            self.carregar_lista_itens()
        elif resultado == "ITEM_NAO_EMPRESTADO":
             self.view.mostrar_mensagem("Este item não consta como emprestado.", ft.colors.ORANGE)
        else:
             self.view.mostrar_mensagem(f"Erro: {resultado}", ft.colors.RED)

    def acao_salvar_item(self, e):
        pat = self.view.txt_patrimonio.value
        nome = self.view.txt_nome.value
        cat = self.view.dd_categoria.value 
        if not pat or not nome or not cat:
            self.view.mostrar_mensagem("Preencha todos os campos!", ft.colors.RED)
            return
        #persistência
        res = self.model.insert_item(pat, nome, cat)
 
        if res == "SUCESSO":
            self.view.mostrar_mensagem("Item salvo!", ft.colors.GREEN)
            self.view.limpar_campos_cadastro()
            self.carregar_lista_itens()
        elif res == "ERRO_DUPLICADO":
            self.view.mostrar_mensagem("Erro: Patrimônio já cadastrado.", ft.colors.RED)
 
    
    def carregar_lista_itens(self):
        #limpa linhas antigas
        self.view.tabela_itens.rows.clear()
       
        #busca novos dados
        dados = self.model.search_itens("")
       
        for p, n, c, s in dados:
            #logica visual de status
            status_text = "Disponível"
            status_color = ft.colors.GREEN
            if s == 1:
                status_text = "Emprestado"
                status_color = ft.colors.ORANGE
            elif s == 2:
                status_text = "Manutenção"
                status_color = ft.colors.RED
 
            #cria a linha
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p)),
                    ft.DataCell(ft.Text(n)),
                    ft.DataCell(ft.Text(str(c))),
                    ft.DataCell(ft.Container(
                        content=ft.Text(status_text, color="white", size=12),
                        bgcolor=status_color,
                        padding=5,
                        border_radius=5
                    )),])
            self.view.tabela_itens.rows.append(row)
       
        self.view.page.update()
 
    #RF 051: geração do recibo em pdf
    def gerar_recibo_pdf(self, patrimonio, pessoa):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
           
            #cabeçalho
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="RECIBO DE EMPRÉSTIMO DE ATIVO", ln=1, align='C')
            pdf.ln(10)
           
            #corpo
            pdf.set_font("Arial", size=12)
            texto = f"""
            Declaro que recebi o item abaixo listado em perfeitas condições de uso e funcionamento.
            Comprometo-me a devolvê-lo na data estipulada ou quando solicitado pela coordenação.
           
            Dados do Empréstimo:
            ------------------------------------------------
            Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            Responsável: {pessoa}
            Item Patrimônio: {patrimonio}
            ------------------------------------------------
            """
            pdf.multi_cell(0, 10, txt=texto)
            pdf.ln(20)
           
            #assinatura
            pdf.cell(200, 10, txt="_" * 50, ln=1, align='C')
            pdf.cell(200, 10, txt="Assinatura do Responsável", ln=1, align='C')
           
            #salvar e abrir
            nome_arquivo = f"recibo_{patrimonio}.pdf"
            pdf.output(nome_arquivo)
           
            #abre o PDF automaticamente
            os.startfile(nome_arquivo)
           
        except Exception as ex:
            print(f"Erro ao gerar PDF: {ex}")
            self.view.mostrar_mensagem("Empréstimo ok, mas erro ao gerar PDF.", ft.colors.ORANGE)
 
    #RF 052: exportação excel
    def exportar_relatorio(self, e):
        try:
            dados = self.model.search_itens("")
            #cria dataFrame com pandas
            df = pd.DataFrame(dados, columns=["Patrimônio", "Nome", "Categoria", "Status Code"])
           
            status_map = {0: 'Disponível', 1: 'Emprestado', 2: 'Manutenção'}
            df['Status Code'] = df['Status Code'].map(status_map)
           
            df.to_excel("inventario_escolar.xlsx", index=False)
            self.view.mostrar_mensagem("Relatório 'inventario_escolar.xlsx' gerado!", ft.colors.BLUE)
            #abre a pasta onde salvou
            os.startfile(".")
        except Exception as ex:
            self.view.mostrar_mensagem(f"Erro ao exportar Excel: {ex}", ft.colors.RED)
