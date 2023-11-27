import Back_Trufas
import PySimpleGUI as sg


class sistema():

    def janela_inicio():
        sg.theme('DarkTeal10')
        layout = [[sg.Text('Bem vindo a Melhor Trufa do Mundo Distribuidora LTDA')],
                  [sg.Text('Selecione o que deseja fazer:')],
                  [sg.Button('Novo Pedido'), sg.Button('Consultar Pedido')],
                  [sg.Button('Sair')]]

        janela_inicio = sg.Window('Melhor Trufa do Mundo Distribuidora LTDA', layout, resizable=True, finalize=True, size=(360, 125))

        event, values = janela_inicio.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            elif event == 'Novo Pedido':
                janela_inicio.close()
                sistema.adicionar_pedido()
                break
            elif event == 'Consultar Pedido':
                janela_inicio.close()
                sistema.consultar_pedido()
                break
        janela_inicio.close()

    def adicionar_pedido():
        info_pedido = []
        heading = ['Produto', 'Valor', 'Quantidade', 'Total']
        layout = [[sg.Text('Bem vindo a Melhor Trufa do Mundo Distribuidora LTDA')],
                  [sg.Text('Cliente:'), sg.InputText(k=('-CLIENTE-'), do_not_clear=True)],
                  [sg.Text('Produto:'), sg.Input(size=(25, 0), k=('-PRODUTO-'), do_not_clear=False),
                   sg.Text('Valor:'), sg.InputText(size=(10, 1), k=('-VALOR-'), do_not_clear=False),
                   sg.Text('Quantidade:'), sg.InputText(size=(5, 1), k=('-QTD-'), do_not_clear=False)],
                  [sg.Button('Adicionar Produto')],
                  [sg.Table(values=info_pedido, headings=heading,
                            key='-TABELA-', auto_size_columns=True,
                            display_row_numbers=False,
                            alternating_row_color='blue',
                            justification='center')],
                  [sg.Button('Registrar Pedido'), sg.Button('Voltar')]]

        janela_novo_pedido = sg.Window('Novo Pedido', layout, resizable=True)

        while True:
            event, values = janela_novo_pedido.read()
            if event in (sg.WIN_CLOSED, 'Voltar'):
                break
            elif event == 'Adicionar Produto':
                total_produto = Back_Trufas.totalizando_produto((values['-VALOR-']), values['-QTD-'])
                info = [values['-PRODUTO-'], values['-VALOR-'], values['-QTD-'], total_produto]
                info_pedido.append(info)
                janela_novo_pedido['-TABELA-'].update(values=info_pedido)
            elif event == 'Registrar Pedido':
                Back_Trufas.tratar_dados(Back_Trufas.numero_pedido(), values['-CLIENTE-'], info_pedido)
                break
        janela_novo_pedido.close()
        sistema.janela_inicio()

    def consultar_pedido():
        info_consulta = Back_Trufas.consultar_tudo()
        heading = ['Pedido', 'Data', 'Cliente', 'Produto', 'Valor', 'Quantidade']

        layout = [[sg.Text('Consultar Pedido')],
                  [sg.Text('Digite o nome do cliente:'), sg.InputText(size=(25, 0), k='-CLIENTE-')],
                  [sg.Text('Digite o número do pedido:'), sg.InputText(size=(25, 0), k='-PEDIDO-')],
                  [sg.Button('Consultar', k='-CONSULTAR-'), sg.Button('Excluir Pedido', k='-EXCLUIR-')],
                  [sg.Table(values=info_consulta, headings=heading, auto_size_columns=True, display_row_numbers=False, alternating_row_color='blue', justification='center', enable_events=True, key='-TABELA-')],
                  [sg.Button('Voltar')]]

        janela_consultar_pedido = sg.Window('Consultar Pedido', layout, resizable=True, modal=True)
        seleção = ''
        while True:
            event, values = janela_consultar_pedido.read()
            if event in (sg.WIN_CLOSED, 'Voltar'):
                break
            elif '-CONSULTAR-' in event:
                if values['-CLIENTE-'] != '':
                    cliente = Back_Trufas.consultar_cliente(values['-CLIENTE-'])
                    if len(cliente) == 0 :
                        sg.popup('Cliente não encontrado!')
                    else:
                        janela_consultar_pedido['-TABELA-'].update(values=cliente)
                elif values['-PEDIDO-'] != '':
                    pedido = Back_Trufas.consultar_pedido(values['-PEDIDO-'])
                    if len(pedido) == 0 :
                        sg.popup('Pedido não encontrado!')
                    else:
                        janela_consultar_pedido['-TABELA-'].update(values=pedido)
                else:
                    sg.popup('Digite nome do cliente ou número do pedido!')
                    janela_consultar_pedido['-TABELA-'].update(values=info_consulta)
            elif '-EXCLUIR-' in event:
                if values['-PEDIDO-'] != '':
                    retorno = Back_Trufas.excluir_pedido(values['-PEDIDO-'])
                    if retorno == 'Pedido não encontrado':
                        sg.popup('Pedido não encontrado')
                    else:
                        sg.popup('Pedido Excluido!')
                        janela_consultar_pedido.close()
                        sistema.consultar_pedido()
            elif event == '-TABELA-':
                pedido_selecionado = values['-TABELA-'][0]
                seleção = info_consulta[pedido_selecionado]
                janela_consultar_pedido.close()
                sistema.atualizar_excluir_pedido(seleção)
                break

        janela_consultar_pedido.close()
        sistema.janela_inicio()

    def atualizar_excluir_pedido(linha_selecionada):
        antigo = linha_selecionada
        layout = [[sg.Text('Data:'),sg.InputText(f'{linha_selecionada[1]}', k='-NOVA DATA-')],
                  [sg.Text('Cliente:'), sg.InputText(f'{linha_selecionada[2]}',k='-NOVO CLIENTE-')],
                  [sg.Text('Produto:'), sg.InputText(f'{linha_selecionada[3]}', k='-NOVO PRODUTO-')],
                  [sg.Text('Valor:'), sg.InputText(f'{linha_selecionada[4]}', k='-NOVO VALOR-')],
                  [sg.Text('Quantidade:'), sg.InputText(f'{linha_selecionada[5]}', k='-NOVA QTD-')],
                  [sg.Button('Atualizar Pedido'), sg.Button('Excluir Produto')],
                  [sg.Button('Sair')] ]
        
        janela_editar = sg.Window('Editar Pedido', layout, resizable=True, modal=True)
        while True:
            event,values = janela_editar.read()
            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            elif event == 'Atualizar Pedido':
                retorno = Back_Trufas.atualizar_pedido(antigo, values)
                if retorno == 'Valores iguais':
                    sg.popup('Valores iguais, não houve alteração!')
                else:
                    sg.popup('Pedido atualizado!')
                    break
            elif event == 'Excluir Produto':
                retorno = Back_Trufas.excluir_linha(antigo)
                if retorno == 'Pedido não encontrado':
                    sg.popup('Produto não encontrado! Verifique novamente!')
                else:
                    sg.popup('Produto excluido!')
                    break
        
        janela_editar.close()
        sistema.consultar_pedido()

sistema.janela_inicio()
