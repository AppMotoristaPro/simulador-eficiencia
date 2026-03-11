from flask import Blueprint, render_template, request, jsonify
from app.services.tributacao_service import TributacaoService

# Cria o Blueprint do simulador
simulador_bp = Blueprint('simulador', __name__)

@simulador_bp.route('/', methods=['GET'])
def index():
    # Renderiza a página principal com o formulário
    return render_template('simulador/novo.html')

@simulador_bp.route('/regras', methods=['GET'])
def regras():
    # Renderiza a página explicativa do Simples Nacional e Split
    return render_template('simulador/regras.html')

@simulador_bp.route('/calcular', methods=['POST'])
def calcular():
    # Rota que recebe os dados do frontend e devolve o cálculo
    try:
        # Suporta tanto requisições via API (JSON) quanto envio de formulário tradicional
        dados = request.get_json() if request.is_json else request.form
        
        faturamento_mensal = float(dados.get('faturamento_mensal', 0))
        custo_insumos = float(dados.get('custo_insumos', 0))
        custo_fornecedores = float(dados.get('custo_fornecedores', 0))
        anexo = dados.get('anexo', 'I')

        # Aciona o motor de cálculo que espelha a sua planilha
        resultado = TributacaoService.simular_eficiencia(
            faturamento_mensal=faturamento_mensal,
            custo_insumos=custo_insumos,
            custo_fornecedores=custo_fornecedores,
            anexo=anexo
        )

        # Se a requisição veio via JavaScript (Fetch API), devolve um JSON limpo
        if request.is_json:
            return jsonify(resultado)
        
        # Se for um envio de form padrão, renderiza a tela de resultado
        return render_template('simulador/resultado.html', resultado=resultado)

    except Exception as e:
        return jsonify({"erro": "Erro ao processar os dados: " + str(e)}), 400

