# Provisão de Folha de Pagamento

Aplicação web para importação de folha de pagamento e cálculo automático de provisões trabalhistas e encargos sociais.

## Funcionalidades

- **Importação de Arquivos**: Suporta arquivos CSV e Excel (.xlsx, .xls)
- **Cálculos Automáticos**:
  - Encargos Sociais (28,8% sobre o salário)
  - Provisão de 13º Salário
  - Provisão de Férias (com 1/3 constitucional)
  - Provisão de Indenização (5% sobre o salário)
- **Resumo Gerencial**: Dashboard com totalizações
- **Exportação**: Exportar resultados em CSV
- **Interface Responsiva**: Design moderno e adaptável

## Estrutura de Dados

### Entrada (Input)
O arquivo importado deve conter as seguintes colunas:

| Campo | Descrição | Tipo |
|-------|-----------|------|
| `codigo_funcionario` | Código de identificação do funcionário | Alfanumérico |
| `nome_funcionario` | Nome completo do funcionário | Texto |
| `secao` | Departamento ou seção | Texto |
| `funcao` | Cargo ou função | Texto |
| `valor_salario` | Salário base mensal | Numérico |
| `vale_alimentacao` | Valor do benefício Vale Alimentação | Numérico |
| `seguro` | Valor do benefício Seguro | Numérico |

### Saída (Output)
Os dados processados incluem:

| Campo | Descrição |
|-------|-----------|
| `valor_encargos` | Encargos sociais (28,8% do salário) |
| `provisao_13_salario` | Provisão mensal do 13º salário |
| `provisao_ferias` | Provisão mensal de férias |
| `provisao_indenizacao_5pc` | Provisão de indenização (5% do salário) |
| `custo_total_mensal` | Soma de todos os valores |

## Cálculos

### Encargos Sociais
```
Valor Encargos = Valor Salário × 0,288
```
(INSS Patronal 20% + FGTS 8% + RAT/Terceiros 0,8%)

### Provisão de 13º Salário
```
Provisão 13º = (Valor Salário / 12) × (1 + 0,288)
```

### Provisão de Férias
```
Provisão Férias = ((Valor Salário + (Valor Salário / 3)) / 12) × (1 + 0,288)
```

### Provisão de Indenização
```
Provisão Indenização = Valor Salário × 0,05
```

## Instalação e Execução

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Passos

1. **Clonar ou baixar o projeto**
   ```bash
   cd provisao_folha
   ```

2. **Criar um ambiente virtual (opcional, mas recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar a aplicação**
   ```bash
   python app.py
   ```

5. **Acessar a aplicação**
   Abra seu navegador e acesse: `http://localhost:5000`

## Uso

1. **Baixar arquivo de exemplo**: Clique em "Baixar Exemplo" para obter um arquivo CSV de teste
2. **Importar arquivo**: Clique na área de upload ou arraste um arquivo CSV/Excel
3. **Visualizar resultados**: A aplicação processará automaticamente e exibirá:
   - Resumo gerencial com totalizações
   - Tabela detalhada com todos os cálculos
4. **Exportar dados**: Clique em "Exportar para CSV" para baixar os resultados

## Estrutura do Projeto

```
provisao_folha/
├── app.py                 # Aplicação Flask (backend)
├── requirements.txt       # Dependências Python
├── folha_exemplo.csv      # Arquivo de exemplo
├── templates/
│   └── index.html         # Interface web (frontend)
├── uploads/               # Diretório para arquivos enviados
└── README.md              # Este arquivo
```

## Dependências

- **Flask**: Framework web
- **Flask-CORS**: Suporte a CORS
- **pandas**: Processamento de dados
- **openpyxl**: Leitura de arquivos Excel

## Notas Importantes

- Os cálculos de encargos utilizam uma alíquota simplificada de 28,8%
- As provisões são calculadas em regime de competência (mensalmente)
- O arquivo não é persistido no servidor; os dados são processados em memória
- A exportação gera um arquivo CSV com separador ponto-e-vírgula (;) para compatibilidade com Excel português/brasileiro

## Melhorias Futuras

- Suporte a diferentes alíquotas de encargos por região
- Persistência de dados em banco de dados
- Autenticação de usuários
- Histórico de processamentos
- Relatórios em PDF
- Integração com sistemas de RH

## Licença

Este projeto é fornecido como está, sem garantias.

## Suporte

Para dúvidas ou problemas, verifique:
1. Se o arquivo está no formato correto (CSV ou Excel)
2. Se todas as colunas obrigatórias estão presentes
3. Se os valores numéricos estão formatados corretamente
