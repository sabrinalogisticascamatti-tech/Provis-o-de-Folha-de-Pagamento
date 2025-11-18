# Prompt de Desenvolvimento: Aplicação Web de Provisão de Folha de Pagamento

## Objetivo
Desenvolver uma **Aplicação Web Full-Stack** que permita ao usuário importar dados de uma folha de pagamento e, automaticamente, calcular as provisões trabalhistas e encargos sociais associados, apresentando um relatório detalhado por funcionário e um resumo gerencial.

## Requisitos Funcionais

### 1. Importação de Dados
*   A aplicação deve fornecer uma interface para o usuário **importar um arquivo** (preferencialmente CSV ou Excel) contendo os dados da folha de pagamento.
*   O sistema deve validar a estrutura do arquivo e os tipos de dados.

### 2. Estrutura de Dados (Input)
A tabela de dados importada deve conter, no mínimo, os seguintes campos por funcionário:

| Campo | Descrição | Tipo de Dado |
| :--- | :--- | :--- |
| `codigo_funcionario` | Código de identificação único do funcionário. | Alfanumérico |
| `nome_funcionario` | Nome completo do funcionário. | Texto |
| `secao` | Departamento ou seção do funcionário. | Texto |
| `funcao` | Cargo ou função do funcionário. | Texto |
| `valor_salario` | Salário base mensal do funcionário. | Numérico (Moeda) |
| `vale_alimentacao` | Valor fixo mensal do benefício Vale Alimentação. | Numérico (Moeda) |
| `seguro` | Valor fixo mensal do benefício Seguro (ex: Seguro de Vida). | Numérico (Moeda) |

### 3. Cálculos Automáticos (Provisões e Encargos)

O sistema deve realizar os seguintes cálculos automaticamente para cada funcionário, com base no `valor_salario`:

#### A. Encargos Sociais (Valor Encargos)
O sistema deve calcular um valor de encargos sociais (INSS Patronal, FGTS, etc.) como uma **porcentagem fixa** sobre o `valor_salario`. Para fins de desenvolvimento inicial, utilize a alíquota de **28,8%** (20% INSS Patronal + 8% FGTS + 0,8% Terceiros/RAT, como um valor simplificado e ilustrativo).

*   **Fórmula Simplificada:** `Valor Encargos = Valor Salário * 0.288`

#### B. Provisões Trabalhistas
O sistema deve calcular as seguintes provisões mensais (em regime de competência):

1.  **Provisão de 13º Salário:**
    *   **Fórmula:** `Provisão 13º = (Valor Salário / 12) * (1 + 0.288)`
    *   *Nota:* O encargo social (28,8%) deve ser provisionado sobre o 13º salário.

2.  **Provisão de Férias:**
    *   **Fórmula:** `Provisão Férias = ((Valor Salário + (Valor Salário / 3)) / 12) * (1 + 0.288)`
    *   *Nota:* A provisão de férias inclui o adicional de 1/3 constitucional e o encargo social (28,8%) sobre o total.

3.  **Provisão de Indenização (5% sobre o Salário):**
    *   **Fórmula:** `Provisão Indenização = Valor Salário * 0.05`
    *   *Nota:* Esta provisão é um valor fixo de 5% sobre o salário, conforme solicitado.

### 4. Estrutura de Dados (Output/Relatório)
O resultado final deve apresentar uma tabela com os dados de entrada mais os campos calculados:

| Campo | Descrição |
| :--- | :--- |
| `codigo_funcionario` | (Input) |
| `nome_funcionario` | (Input) |
| `secao` | (Input) |
| `funcao` | (Input) |
| `valor_salario` | (Input) |
| `vale_alimentacao` | (Input) |
| `seguro` | (Input) |
| **`valor_encargos`** | (Calculado - 28,8% sobre o salário) |
| **`provisao_13_salario`** | (Calculado) |
| **`provisao_ferias`** | (Calculado) |
| **`provisao_indenizacao_5pc`** | (Calculado - 5% sobre o salário) |
| **`custo_total_mensal`** | Soma de todos os valores acima. |

### 5. Interface do Usuário (UI/UX)
*   **Página Inicial:** Formulário simples para upload do arquivo de folha de pagamento.
*   **Página de Resultados:**
    *   Tabela interativa (filtrável e ordenável) com o detalhamento do Output/Relatório.
    *   **Resumo Gerencial (Dashboard):** Cartões de resumo com o **Custo Total da Folha (Salários + Benefícios + Encargos + Provisões)**, e o **Total de Provisões Mensais**.
    *   Opção para **Exportar** o relatório final (tabela de Output) para CSV/Excel.

## Requisitos Técnicos
*   **Tecnologia:** Aplicação Web Full-Stack (sugestão: Python/Flask/FastAPI para o backend e HTML/CSS/JavaScript para o frontend, ou um framework moderno como React/Vue/Svelte se o agente preferir).
*   **Persistência:** Não é necessário banco de dados persistente para a primeira versão. Os dados podem ser processados em memória após a importação.
*   **Estilo:** Design limpo e profissional, focado na usabilidade e clareza dos dados financeiros.

## Entregáveis
1.  Código-fonte completo da aplicação web.
2.  Instruções claras sobre como rodar a aplicação.
3.  Um arquivo de exemplo (`folha_exemplo.csv`) para teste.
4.  A aplicação rodando em um link público temporário para demonstração.

---
**Fim do Prompt**
