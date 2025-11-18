"""
Aplicação Flask para Provisão de Folha de Pagamento
"""
import os
import json
from io import StringIO
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_provisions(salary):
    """
    Calcula as provisões e encargos com base no salário.
    
    Parâmetros:
    - salary: Valor do salário base
    
    Retorna:
    - Dicionário com todos os valores calculados
    """
    # Alíquota de encargos sociais (INSS Patronal + FGTS + RAT)
    ENCARGO_RATE = 0.288
    
    # Cálculos
    valor_encargos = salary * ENCARGO_RATE
    
    # Provisão de 13º Salário (com encargos)
    provisao_13_salario = (salary / 12) * (1 + ENCARGO_RATE)
    
    # Provisão de Férias (1/3 constitucional + encargos)
    provisao_ferias = ((salary + (salary / 3)) / 12) * (1 + ENCARGO_RATE)
    
    # Provisão de Indenização (5% sobre o salário)
    provisao_indenizacao_5pc = salary * 0.05
    
    return {
        'valor_encargos': round(valor_encargos, 2),
        'provisao_13_salario': round(provisao_13_salario, 2),
        'provisao_ferias': round(provisao_ferias, 2),
        'provisao_indenizacao_5pc': round(provisao_indenizacao_5pc, 2)
    }

def process_payroll(df):
    """
    Processa a folha de pagamento e calcula as provisões.
    
    Parâmetros:
    - df: DataFrame com os dados da folha de pagamento
    
    Retorna:
    - DataFrame com os cálculos adicionados
    """
    # Normalizar nomes de colunas (remover espaços, converter para minúsculas)
    df.columns = df.columns.str.strip().str.lower()
    
    # Validar colunas obrigatórias
    required_columns = [
        'codigo_funcionario',
        'nome_funcionario',
        'secao',
        'funcao',
        'valor_salario',
        'vale_alimentacao',
        'seguro'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Colunas obrigatórias faltando: {', '.join(missing_columns)}")
    
    # Converter valores numéricos
    df['valor_salario'] = pd.to_numeric(df['valor_salario'], errors='coerce')
    df['vale_alimentacao'] = pd.to_numeric(df['vale_alimentacao'], errors='coerce')
    df['seguro'] = pd.to_numeric(df['seguro'], errors='coerce')
    
    # Remover linhas com valores nulos em salário
    df = df.dropna(subset=['valor_salario']).reset_index(drop=True)
    
    # Preencher valores nulos em benefícios com 0
    df['vale_alimentacao'] = df['vale_alimentacao'].fillna(0)
    df['seguro'] = df['seguro'].fillna(0)
    
    # Aplicar cálculos para cada funcionário
    for idx, row in df.iterrows():
        salary = row['valor_salario']
        provisions = calculate_provisions(salary)
        
        # Adicionar cálculos ao dicionário
        for key, value in provisions.items():
            df.at[idx, key] = value
        
        # Calcular custo total mensal
        custo_total = (
            salary +
            row['vale_alimentacao'] +
            row['seguro'] +
            provisions['valor_encargos'] +
            provisions['provisao_13_salario'] +
            provisions['provisao_ferias'] +
            provisions['provisao_indenizacao_5pc']
        )
        df.at[idx, 'custo_total_mensal'] = round(custo_total, 2)
    
    return df

@app.route('/')
def index():
    """Página inicial da aplicação."""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Endpoint para upload e processamento de arquivo de folha de pagamento.
    """
    try:
        # Validar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Arquivo não selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido. Use CSV ou Excel'}), 400
        
        # Ler arquivo
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Processar folha de pagamento
        df_processed = process_payroll(df)
        
        # Preparar dados para resposta - converter NaN para None (que vira null em JSON)
        result_data = df_processed.where(pd.notna(df_processed), None).to_dict('records')
        
        # Calcular resumo gerencial
        summary = {
            'total_funcionarios': len(df_processed),
            'total_salarios': round(df_processed['valor_salario'].sum(), 2),
            'total_beneficios': round(
                df_processed['vale_alimentacao'].sum() + 
                df_processed['seguro'].sum(), 
                2
            ),
            'total_encargos': round(df_processed['valor_encargos'].sum(), 2),
            'total_provisoes': round(
                df_processed['provisao_13_salario'].sum() +
                df_processed['provisao_ferias'].sum() +
                df_processed['provisao_indenizacao_5pc'].sum(),
                2
            ),
            'custo_total_mensal': round(df_processed['custo_total_mensal'].sum(), 2)
        }
        
        return jsonify({
            'success': True,
            'data': result_data,
            'summary': summary
        })
    
    except Exception as e:
        print(f"Erro ao processar arquivo: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500

@app.route('/api/export', methods=['POST'])
def export_data():
    """
    Endpoint para exportar dados processados em CSV.
    """
    try:
        data = request.json.get('data', [])
        
        if not data:
            return jsonify({'error': 'Nenhum dado para exportar'}), 400
        
        # Converter para DataFrame
        df = pd.DataFrame(data)
        
        # Criar arquivo CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, decimal=',', sep=';')
        
        # Preparar resposta
        csv_string = csv_buffer.getvalue()
        
        return jsonify({
            'success': True,
            'csv': csv_string,
            'filename': f'provisao_folha_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        })
    
    except Exception as e:
        print(f"Erro ao exportar dados: {str(e)}")
        return jsonify({'error': f'Erro ao exportar dados: {str(e)}'}), 500

@app.route('/api/example', methods=['GET'])
def get_example():
    """
    Endpoint para baixar arquivo de exemplo.
    """
    try:
        # Criar DataFrame de exemplo
        example_data = {
            'codigo_funcionario': ['001', '002', '003'],
            'nome_funcionario': ['João Silva', 'Maria Santos', 'Pedro Oliveira'],
            'secao': ['TI', 'RH', 'Financeiro'],
            'funcao': ['Desenvolvedor', 'Gerente', 'Analista'],
            'valor_salario': [5000.00, 6000.00, 4500.00],
            'vale_alimentacao': [500.00, 500.00, 500.00],
            'seguro': [100.00, 100.00, 100.00]
        }
        
        df = pd.DataFrame(example_data)
        
        # Salvar como Excel
        filename = 'folha_exemplo.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, sheet_name='Folha de Pagamento')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    except Exception as e:
        print(f"Erro ao gerar arquivo de exemplo: {str(e)}")
        return jsonify({'error': f'Erro ao gerar arquivo de exemplo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
