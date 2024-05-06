import pandas as pd
import re
from datetime import datetime

def tratar_arquivo_csv(file_path):
    # Colunas para remover
    colunas_para_remover = ['Horário', 'User ID', 'Time Tracked', 'Time Entry ID', 'Description', 'Billable',
                            'Time Labels', 'Start', 'Stop', 'Time Tracked', 'Space ID', 'Folder ID', 'List ID',
                            'Task ID', 'Due Date', 'Due Date Text', 'Start Date', 'Start Date Text',
                            'Task Time Estimated', 'Task Time Estimated Text', 'Task Time Spent',
                            'Task Time Spent Text', 'User Total Time Estimated', 'User Total Time Estimated Text',
                            'User Total Time Tracked', 'User Total Time Tracked Text', 'Tags', 'Checklists',
                            'User Period Time Spent', 'User Period Time Spent Text', 'Date Created',
                            'Date Created Text', 'Custom Task ID', 'Parent Task ID', 'Progresso']

    # Ler o arquivo CSV
    df = pd.read_csv(file_path)
    
    # Remover colunas
    df = df.drop(columns=colunas_para_remover)

    # Renomear colunas
    df = df.rename(columns={
        'Username': 'Nome',
        'Start Text': 'Tempo de rastreio inicial',
        'Stop Text': 'Tempo de rastreio final',
        'Time Tracked Text': 'Tempo rastreado',
        'Space Name': 'Espaço',
        'Folder Name': 'Pasta',
        'List Name': 'Lista',
        'Task Name': 'Tarefa',
        'Task Status': 'Status'
    })

    # Expressão regular para extrair data e hora
    regex = r"(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}:\d{2} [AP]M)"

    # Função para extrair data e hora e ajustar o formato
    def extrair_data_hora(text):
        match = re.search(regex, str(text))
        if match:
            return match.group(1)
        return None

    # Aplicar a função nas colunas "Tempo de rastreio inicial" e "Tempo de rastreio final"
    df['Tempo de rastreio inicial'] = df['Tempo de rastreio inicial'].apply(extrair_data_hora)
    df['Tempo de rastreio final'] = df['Tempo de rastreio final'].apply(extrair_data_hora)

    return df

def extrair_mes_ano(text):
    if text:
        date_time_obj = datetime.strptime(text, '%m/%d/%Y, %I:%M:%S %p')
        return date_time_obj.strftime('%B %Y')
    return None

def converter_para_horas(hora_str):
    try:
        if isinstance(hora_str, str):
            match = re.match(r'(\d+)\s*h\s*(\d*)', hora_str)
            if match:
                horas = int(match.group(1))
                minutos = int(match.group(2)) if match.group(2) else 0
                return horas + minutos / 60
            else:
                match_minutos = re.match(r'(\d+)\s*m', hora_str)
                if match_minutos:
                    minutos = int(match_minutos.group(1))
                    return minutos / 60
                else:
                    return float(hora_str.split()[0])
        else:
            return 0
    except ValueError:
        return 0


def salvar_em_paginas_separadas(df, file_path):
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    workbook = writer.book

    title_page_format = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
    })

    header_format = workbook.add_format({'bold': True, 'align': 'center'})

    geral_data = []

    for nome, data in df.groupby('Nome'):
        soma = data['Tempo rastreado'].sum()

        # Pegar o valor único da coluna "Espaço" e colocá-lo ao lado do nome na linha 1
        espaco_value = data['Espaço'].iloc[0]

        # Extrair mês e ano
        data['Mês e Ano'] = data['Tempo de rastreio inicial'].apply(extrair_mes_ano)

        nova_linha = {'Nome': nome, 'Total tempo rastreado': soma, 'Mês e Ano': data['Mês e Ano'].unique()}
        geral_data.append(nova_linha)

        # Adicionar os dados à planilha individual
        data_final = data.drop(columns=['Nome', 'Espaço'])  # Removendo as colunas 'Nome' e 'Espaço'

        worksheet = writer.sheets.get(nome)  # Verifica se a planilha já existe

        if not worksheet:  # Se a planilha não existe, cria ela
            data_final.to_excel(writer, sheet_name=nome, index=False, startrow=3)  # Começar a escrever a partir da linha 4
            worksheet = writer.sheets[nome]

            worksheet.write('A1', nome, title_page_format)  # Escrevendo o nome como título na parte superior
            worksheet.write('B1', espaco_value, title_page_format)  # Escrevendo o valor da coluna "Espaço"
            worksheet.write_row('A4', data_final.columns, header_format)  # Escrevendo os cabeçalhos a partir da linha 5

            # Escrevendo a soma do tempo rastreado
            worksheet.write('A2', f'Total Tempo Rastreado: {soma}', title_page_format)

            for idx, col in enumerate(data_final.columns):
                worksheet.set_column(idx, idx, max(len(str(val)) for val in data_final[col]) + 2)

        else:  # Se a planilha já existe, apenas anexa os dados
            row = len(worksheet.colnames) + 3
            data_final.to_excel(writer, sheet_name=nome, index=False, startrow=row)

    # Adicionar página "Geral"
    geral_df = pd.DataFrame(geral_data)
    geral_df.to_excel(writer, sheet_name='Geral', index=False)

    writer.close()