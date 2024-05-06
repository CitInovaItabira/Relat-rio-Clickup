from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import re
import xlsxwriter
from datetime import datetime
from processing import tratar_arquivo_csv, salvar_em_paginas_separadas, converter_para_horas

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def uploaded_file():
    file = request.files['file']
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df_processed = tratar_arquivo_csv(file_path)
        processed_filename = 'processed_' + filename + '.xlsx'
        processed_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], processed_filename)
        os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
        df_processed['Tempo rastreado'] = df_processed['Tempo rastreado'].apply(converter_para_horas)
        salvar_em_paginas_separadas(df_processed, processed_file_path)
        return send_file(processed_file_path, as_attachment=True)
    return 'Erro ao fazer upload do arquivo'


if __name__ == '__main__':
    app.run(debug=True)
