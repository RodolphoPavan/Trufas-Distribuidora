import Back_Trufas
import PySimpleGUI as sg


class sistema():

    def janela_inicio():
        sg.theme('DarkTeal10')
        layout = [[sg.Text('Bem vindo a Melhor Trufa do Mundo Distribuidora LTDA')],
                  [sg.Text('Selecione o que deseja fazer:')],
                  [sg.Button('Novo Pedido')],
                  [sg.Button('Sair')]]

        janela_inicio = sg.Window('Melhor Trufa do Mundo Distribuidora LTDA', layout, resizable=True, size=(360, 125))

        event, value = janela_inicio.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            elif event == 'Novo Pedido':
                janela_inicio.close()
                sistema.adicionar_pedido()
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
                  [sg.Button('Registrar Pedido'), sg.Button('Sair')]]

        janela_novo_pedido = sg.Window('Novo Pedido', layout, resizable=True)
        while True:
            event, values = janela_novo_pedido.read()
            if event in (sg.WIN_CLOSED, 'Sair'):
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


sistema.janela_inicio()
