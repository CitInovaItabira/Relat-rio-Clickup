https://citinovaitabira.pythonanywhere.com/

# Relatorio-Clickup
Relatório ClickUp usando o CSV  do Painel de Tempo 

Este é um projeto Flask para processar e gerar relatórios a partir de dados exportados do painél(Relatórios de tempo) do ClickUp  , uma plataforma de gerenciamento de projetos. O aplicativo permite fazer upload de arquivos CSV exportados do ClickUp, processá-los e gerar um relatório em formato Excel (.xlsx) com os dados processados.

Instalação
Antes de executar o aplicativo, é necessário instalar as dependências. Você pode instalar todas as dependências necessárias executando o seguinte comando:pip install -r requirements.txt
Certifique-se de estar no diretório raiz do projeto onde o arquivo requirements.txt está localizado.

Uso
Para executar o aplicativo, use o seguinte comando:
flask run

Isso iniciará o servidor Flask localmente. Você poderá acessar o aplicativo em seu navegador visitando o endereço http://127.0.0.1:5000.

No aplicativo, você poderá fazer upload de um arquivo CSV exportado do ClickUp. O aplicativo processará o arquivo e gerará um arquivo Excel (.xlsx) com os dados processados. Você poderá fazer o download do arquivo gerado.

Estrutura do Projeto
app.py: Este é o arquivo principal do aplicativo Flask. Ele contém as rotas e a lógica para processar os arquivos e gerar os relatórios.
processing.py: Este arquivo contém funções para processar os dados do arquivo CSV e gerar o relatório Excel.
templates/: Esta pasta contém os templates HTML para as páginas web do aplicativo.
uploads/: Esta pasta é usada para armazenar os arquivos CSV enviados pelo usuário.
downloads/: Esta pasta é usada para armazenar os arquivos Excel gerados pelo aplicativo.
Certifique-se de ter as permissões adequadas para gravar em uploads/ e downloads/.

Dependências
Flask: Framework web em Python.
pandas: Biblioteca para manipulação e análise de dados em Python.
xlsxwriter: Biblioteca para escrever arquivos Excel no formato .xlsx.
Certifique-se de ter todas as dependências instaladas antes de executar o aplicativo.

Este é apenas um guia básico sobre como usar o aplicativo. Para mais informações sobre como personalizar ou estender o aplicativo, consulte a documentação do Flask e das bibliotecas usadas.
