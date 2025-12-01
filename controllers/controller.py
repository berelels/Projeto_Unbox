import flet as ft
from models import Unbox_Model
from views import TelaPrincipalView
from datetime import datetime
import os
from fpdf import FPDF
import pandas as pd

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
           
    #RF 53:
    
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
 
    