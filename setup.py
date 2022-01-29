import os
import sys

try:
    import PySimpleGUI as sg

    from Scripts.insert_dados import InsertDados
    from Scripts.finalize_order import FinalizeOrder
    from Scripts.new_chart import NewChart
    from Scripts.reports import Relatorios
    from Scripts.edit_order import EditDados
    from Scripts.sqlite import SQLite

    from Design.menu_principal import MenuPrincipal
    from Design.nova_encomenda import NovaEncomenda
    from Design.listar_encomendas import ListarEncomendas
    from Design.baixa_encomenda import BaixaEncomenda
    from Design.graficos import Graficos
    from Design.relatorios import FrontRelatorio
    from Design.deletar_encomenda import DeletarEncomenda
    from Design.editar_encomenda import EditarEncomenda
    from Design.faturamento import Faturamento
    from Scripts.revenues import Revenues
    from Design.lucro_mes import Lucromensal
    from Scripts.pronfit_in_the_month import Gasto
    from Scripts.sicronizar import Sicronizar
    from Scripts.cadastrar_caminho import Criar
    from Scripts.cadastrar_caminho import Editar
    from Design.criar_caminho import FrtCam
    from Design.recuperar import Recuperar
    
except ImportError:
    os.system("pip3 install -r requirements.txt")
    print("Bibliotecas instaladas com sucesso!")
    print("Reabra o programa.")
    sys.exit()

class Program:

    def __init__(self):

        # Menu initializes next to the class
        self.menu = MenuPrincipal.menu_principal()

        # Definition of windows in the builder
        self.nova_encomenda = None
        self.dados_cliente = None
        self.lista_encomenda = None
        self.menu_encomenda = None
        self.dar_baixa_encomenda = None
        self.salgadinhos = None
        self.mais_informacoes = None
        self.graficos = None
        self.relatorios = None
        self.deletar_encomenda = None 
        self.editar_encomenda = None
        self.faturamento = None
        self.lucro_do_mes = None
        self.local = None
        self.recuperar = None

        self._window = None
        self._event = None
        self._value = None

        # Program startup run method
        self.__run()
        
    # deactivate buttons
    def buttons(self, on_off):
        keys = {
            1: "-NOVA_ENCOMENDA-", 
            2: "-LISTAR_ENCOMENDAS-",
            3: "-DAR_BAIXA_ENCOMENDA-",
            4: "-EDITAR_ENCOMENDA-",
            5: "-GRAFICOS-",
            6: "-RELATORIOS-",
            7: "-FATURAMENTO-",
            8: "-DELETAR_ENCOMENDA-",
            9: "-LUCRO_MENSAL-",
            10: "-LOCAL-",
            11: "-RECUPERAR-",
            12: "-SAIR-"
        }

        if on_off == "on":
            for key in range(len(keys)):
                self.menu[keys[key+1]].update(disabled=False)
        else: 
            for key in range(len(keys)):
                self.menu[keys[key+1]].update(disabled=True)
    # functions menu
    def functionsMenu(self, event):

        if event == sg.WIN_CLOSED or event == "-SAIR-":
        
            try:    
                if os.path.getsize("caminhos.csv") == 0:
                    sg.popup_ok("Não há caminhos cadastrados no sistema", "Cadastre um para que possa ser feito o backup" )
                    return False 
                else:
                    localOriginal = 'dados.db'
                    file = 'caminhos.csv'

                    with open(file, 'r') as f:
                        caminhos = f.readlines() 

                    novolocal = caminhos[0].strip()          
                    sincronizar = Sicronizar(localOriginal, novolocal)
                    sincronizar.sincronizar()
                    return False

            except FileNotFoundError:
                sg.popup_ok("Caminho inválido, edite-o. Para que o backup possa ser feito.")
                return False

        elif event == "-NOVA_ENCOMENDA-":
            self.nova_encomenda = NovaEncomenda.nova_encomenda("Nova Encomenda")
            self.buttons("off")

        elif event == "-LISTAR_ENCOMENDAS-":
            self.menu_encomenda = ListarEncomendas.listar_encomendas("Pendente")
            self.buttons("off")

        elif event == "-DAR_BAIXA_ENCOMENDA-":
            self.dar_baixa_encomenda = BaixaEncomenda.baixa_encomenda()
            self.buttons("off")

        elif event == "-GRAFICOS-":
            self.graficos = Graficos.menu_graficos()
            self.buttons("off")

        elif event == "-RELATORIOS-":
            self.relatorios = FrontRelatorio.menu_relatorios()
            self.buttons("off")

        elif event == "-FATURAMENTO-":
            self.faturamento = Faturamento.faturamento()
            self.buttons("off")

        elif event == "-EDITAR_ENCOMENDA-":
            self.editar_encomenda = EditarEncomenda.listar_encomendas("Pendente")
            self.buttons("off")

        elif event == "-DELETAR_ENCOMENDA-":
            self.deletar_encomenda = DeletarEncomenda.deletar_encomenda("Pendente")
            self.buttons("off")

        elif event == "-LUCRO_MENSAL-":
            self.lucro_do_mes = Lucromensal.lucro()
            self.buttons("off")

        elif event == "-LOCAL-":
            self.local = FrtCam.tela()
            self.buttons("off")

        elif event == "-RECUPERAR-":
            self.recuperar = Recuperar.escolher_arquivo()
    # insert new order into the database
    def newOrder(self, event, value):

        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.nova_encomenda.hide()
            self.buttons("on")
            return

        elif event == "-CONFIRMAR-":
            status_menssage = InsertDados([
                str(value["-NOME_CLIENTE-"]), 
                str(value["-DATA_ENTREGA-"]), 
                str(value["-HORA_ENTREGA-"]), 
                int(value["-BOLO_ANIVERSARIO-"]),
                int(value["-BOLO_CASAMENTO-"]), 
                int(value["-QTD_MINI-"]), 
                int(value["-QTD_NORMAL-"]), 
                str(value["-INFO_COMPLEMENTARES-"]) 
            ])

            msg = status_menssage()

            if msg == True:
                sg.popup("Dados inseridos com sucesso!", title="Sucesso!")
                self.nova_encomenda.hide()
                self.buttons("on")
                return
            else:
                sg.popup(msg, title="Erro!")
                return
    # llist orders in database
    def listOrder(self, event, value):
        
        status_concluido = value["-STATUS_CONCLUIDO-"] 
        status_pendente = value["-STATUS_PENDENTE-"]

        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.menu_encomenda.hide()
            self.buttons("on")
            return

        elif event == "-FILTRAR-":
            if status_concluido == True:
                self.menu_encomenda["-INDEX_ENCOMENDA-"].update(
                    values=SQLite('dados.db').select(
                        'dados', '*', 'status = "Concluído"'
                        )
                    )
                self.menu_encomenda["-STATUS_CONCLUIDO-"].update(True)
            elif status_pendente == True:
                self.menu_encomenda["-INDEX_ENCOMENDA-"].update(
                    values=SQLite('dados.db').select(
                        'dados', '*', 'status = "Pendente"'
                        )
                    )
                self.menu_encomenda["-STATUS_PENDENTE-"].update(True)
            return

        elif event == "-MAIS_INFORMACOES-":
            try:
                index = int(value["-INDEX_ENCOMENDA-"][0])

                if status_concluido == True:
                    self.mais_informacoes = ListarEncomendas.mais_informacoes(
                        "Concluído", index
                        )
                    self.menu_encomenda.hide()

                elif status_pendente == True:
                    self.mais_informacoes = ListarEncomendas.mais_informacoes(
                        "Pendente", index
                        )
                    self.menu_encomenda.hide()
                return
            except:
                sg.popup("Selecione uma encomenda para mais informações!")
                return
    # low the order in the database
    def lowOrder(self, event, value):

        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.dar_baixa_encomenda.hide()
            self.buttons("on")
            return

        elif event == "-FINALIZAR_ENCOMENDA-":
            try:
                index_encomenda = value["-TABLE_LISTAR_ENCOMENDA-"]
                kg_aniversario = value["-BOLO_ANIVERSARIO-"]
                kg_casamento = value["-BOLO_CASAMENTO-"]
                lista_encomendas = SQLite('dados.db').select(
                        'dados', '*', 'status = "Pendente"'
                    )

                preco_final = FinalizeOrder(
                    lista_encomendas, index_encomenda, 
                    kg_aniversario, kg_casamento
                    ).get_preco_final()

                self.dar_baixa_encomenda["-VALOR_FINAL-"].update("R$" + str(preco_final))
                self.dar_baixa_encomenda["-FINALIZAR_ENCOMENDA-"].update(disabled=True)
                return
            except:
                sg.popup("Selecione uma encomenda para finalizar!")
                return

        elif event == "-ATUALIZAR_LISTA-":
            self.dar_baixa_encomenda["-TABLE_LISTAR_ENCOMENDA-"].update(
                SQLite('dados.db').select(
                    'dados', '*', 'status = "Pendente"'
                )
            )

            self.dar_baixa_encomenda["-FINALIZAR_ENCOMENDA-"].update(disabled=False)
            self.dar_baixa_encomenda["-VALOR_FINAL-"].update("R$0,00")
            self.dar_baixa_encomenda["-BOLO_ANIVERSARIO-"].update(0)
            self.dar_baixa_encomenda["-BOLO_CASAMENTO-"].update(0)
            return
    # graphics 
    def graphics(self, event):

        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.graficos.hide() 
            self.buttons("on")

        elif event == "-STATUS_PEDIDO-":
            NewChart.graficoPizza()

        elif event == "-TIPO_BOLO-":
            NewChart.graficoTipoBolo()

        elif event == "-TIPO_SALGADO-":
            NewChart.graficoTipoSalgados()

        elif event == "-MENSAIS-":
            NewChart.graficoBarrasPedidos()

        elif event == "-LUCRO_MENSAL-":
            NewChart.graficoganho()
    
        elif event == "-LUCRO_POR_TIPO_DE_FESTAS-":
            NewChart.lucroporfesta()
    # reports
    def reports(self, event):      
        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.relatorios.hide()
            self.buttons("on")
        
        elif event == "-PEDIDOS_ENTREGUES-":
            Relatorios.historico_pedidos_concluido()
            sg.popup("Relatório gerado com sucesso!")

        elif event == "-PEDIDOS_NAO_ENTREGUES-":
            Relatorios.historico_pedidos_naoentregues()
            sg.popup("Relatório gerado com sucesso!")

        elif event == "-PEDIDOS_PENDENTES-":
            Relatorios.pedidos_pendentes()
            sg.popup("Relatório gerado com sucesso!")

        elif event == "-TODOS_PEDIDOS-":
            Relatorios.historico_todos_pedidos()
            sg.popup("Relatório gerado com sucesso!")
    # delete order from database
    def delOrder(self, event, value):

        status_concluido = value["-STATUS_CONCLUIDO-"] 
        status_pendente = value["-STATUS_PENDENTE-"]

        def status(concluido, pendente):
            if concluido == True:
                self.deletar_encomenda["-INDEX_ENCOMENDA-"].update(
                    values=SQLite('dados.db').select(
                        'dados', '*', 'status = "Concluído"'
                        )
                    )
                self.deletar_encomenda["-STATUS_CONCLUIDO-"].update(True)

            elif pendente == True:
                self.deletar_encomenda["-INDEX_ENCOMENDA-"].update(
                    values=SQLite('dados.db').select(
                        'dados', '*', 'status = "Pendente"'
                        )
                    )
                self.deletar_encomenda["-STATUS_CONCLUIDO-"].update(False)
            
        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.deletar_encomenda.hide()
            self.buttons("on")
            return
        
        elif event == "-FILTRAR-":
            status(status_concluido, status_pendente)
            return

        ##########################DELETAR ENCOMENDA###############################

        elif event == "-DELETAR_ENCOMENDA-":
            try:
                index = int(value["-INDEX_ENCOMENDA-"][0])

                if status_pendente == True:
                    lista_encomendas = SQLite('dados.db').select(
                        'dados', 'id', 'status = "Pendente"'
                    )
                elif status_concluido == True:
                    lista_encomendas = SQLite('dados.db').select(
                        'dados', 'id', 'status = "Concluído"'
                    )

                id = lista_encomendas[index][0]
                SQLite('dados.db').delete('dados', f'id={id}')

                status(status_concluido, status_pendente)

            except:
                sg.popup("Nenhuma encomenda selecionada!")
                return
    # edit data order from database
    def editOrder(self, event, value):
        id = 0

        try:
            status_concluido = value["-STATUS_CONCLUIDO-"] 
            status_pendente = value["-STATUS_PENDENTE-"]
        except:
            pass

        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.editar_encomenda.hide()
            self.buttons("on")
            return

        elif event == "-FILTRAR-":
            if status_concluido == True:
                self.editar_encomenda["-INDEX_ENCOMENDA-"].update(
                    values=SQLite('dados.db').select(
                        'dados', '*', 'status = "Concluído"'
                        )
                    )
                self.editar_encomenda["-STATUS_CONCLUIDO-"].update(True)

            elif status_pendente == True:
                self.editar_encomenda["-INDEX_ENCOMENDA-"].update(
                    values=SQLite('dados.db').select(
                        'dados', '*', 'status = "Pendente"'
                        )
                    )
                self.editar_encomenda["-STATUS_CONCLUIDO-"].update(False)
            return

        ###############################EDITAR ENCOMENDA###########################

        elif event == "-EDITAR-":
            try:
                index = int(value["-INDEX_ENCOMENDA-"][0])

                if status_pendente == True:
                    lista_encomendas = SQLite('dados.db').select(
                        'dados', '*', 'status = "Pendente"'
                    )
                elif status_concluido == True:
                    lista_encomendas = SQLite('dados.db').select(
                        'dados', '*', 'status = "Concluído"'
                    )
                dados = lista_encomendas[index]
                id = dados[0]

                self.editar_encomenda.close()
                self.editar_encomenda = EditarEncomenda.edit_info()

                self.editar_encomenda["-NOME_CLIENTE-"].update(dados[1])
                self.editar_encomenda["-DATA_ENTREGA-"].update(dados[2])
                self.editar_encomenda["-HORA_ENTREGA-"].update(dados[3])
                self.editar_encomenda["-BOLO_ANIVERSARIO-"].update(dados[4])
                self.editar_encomenda["-BOLO_CASAMENTO-"].update(dados[5])
                self.editar_encomenda["-QTD_MINI-"].update(dados[6])
                self.editar_encomenda["-QTD_NORMAL-"].update(dados[7])
                self.editar_encomenda["-INFO_COMPLEMENTARES-"].update(dados[9])
            
            except:
                sg.popup("Nenhuma encomenda selecionada!")
                

        elif event == "-CONFIRMAR-":
            status_menssage = EditDados([
                str(value["-NOME_CLIENTE-"]), 
                str(value["-DATA_ENTREGA-"]), 
                str(value["-HORA_ENTREGA-"]), 
                int(value["-BOLO_ANIVERSARIO-"]),
                int(value["-BOLO_CASAMENTO-"]), 
                int(value["-QTD_MINI-"]), 
                int(value["-QTD_NORMAL-"]), 
                str(value["-INFO_COMPLEMENTARES-"]) 
            ], id)

            msg = status_menssage()

            if msg == True:
                sg.popup("Dados atualizados com sucesso!", title="Sucesso!")
                self.editar_encomenda.hide()
                self.buttons("on")
                return
            else:
                sg.popup(msg, title="Erro!")
                return
    # show full value of revenue
    def revenues(self, event, value):
        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.faturamento.close()
            self.buttons("on")

        elif event == "-FILTRAR-":
            data_inicial = value["-DATA_INICIAL-"]
            data_final = value["-DATA_FINAL-"]
            
            full_value = Revenues(data_inicial, data_final).get_value()
            self.faturamento["-VALOR_FATURAMENTO-"].update(full_value)
    # monthly earnings calculator
    def monthlyPronfit(self, event, value):
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            self.lucro_do_mes.close()
            self.buttons("on")
        
        elif event == "-ENVIAR-":
            try:
                funcionarios = float(value['-INPUT_FUNCIONARIOS-'])
                mercadorias = float(value['-INPUT_MERCADORIAS-'])
                impostos = float(value['-INPUT_IMPOSTOS-'])
                outros = float(value['-INPUT_OUTROS-'])

                total = Gasto.descobrirGanhoMes() - (funcionarios + mercadorias + impostos + outros) 
                self.lucro_do_mes['-OUTPUT-'].update(total)
                self.lucro_do_mes['-OUTPUT-'].update(f'O lucro mensal será {total} reais')

            except ValueError:
                self.lucro_do_mes['-OUTPUT-'].update('Por favor, digite apenas números.')
    # register new path to database backup
    def registerPath(self, event):
        if event == sg.WIN_CLOSED or event == "-VOLTAR-":
            self.local.close()
            self.buttons("on")

        elif event == "-PROCURAR-":
            Criar.criar()

        elif event == "-EDITAR-":
            Editar.editar()
    # run method
    def __run(self):

        self.menu.maximize()

        while True:

            self._window, self._event, self._value = sg.read_all_windows()

            if self._window == self.menu:
                sair = self.functionsMenu(self._event)

                if sair == False:
                    break

            elif self._window == self.nova_encomenda:
                self.newOrder(self._event, self._value)

            elif self._window == self.menu_encomenda:
                self.listOrder(self._event, self._value)

            elif (self._window == self.mais_informacoes and self._event == sg.WIN_CLOSED 
                or self._window == self.mais_informacoes and self._event == "-VOLTAR-"):
                self.mais_informacoes.hide()
                self.menu_encomenda.un_hide()

            elif self._window == self.dar_baixa_encomenda:
                self.lowOrder(self._event, self._value)

            elif self._window == self.graficos:
                self.graphics(self._event)

            elif self._window == self.relatorios:
                self.reports(self._event)

            elif self._window == self.deletar_encomenda:
                self.delOrder(self._event, self._value)

            elif self._window == self.editar_encomenda:
                self.editOrder(self._event, self._value)

            elif self._window == self.faturamento:
                self.revenues(self._event, self._value)

            elif self._window == self.lucro_do_mes:
                self.monthlyPronfit(self._event, self._value)

            if self._window == self.local:
                self.registerPath(self._event)

if __name__ == "__main__":
    program = Program()