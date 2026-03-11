class TributacaoService:
    """
    Serviço responsável pelos cálculos do Simples Nacional e simulação de Split de Pagamentos,
    baseado no modelo de Eficiência Tributária.
    """

    # Tabela do Simples Nacional mapeada a partir da aba "apoio" (Faturamento Anual)
    TABELA_SIMPLES = [
        {"faixa": 1, "limite": 180000,   "taxas": {"I": 0.040, "II": 0.045, "III": 0.060, "IV": 0.045, "V": 0.155}},
        {"faixa": 2, "limite": 360000,   "taxas": {"I": 0.073, "II": 0.078, "III": 0.112, "IV": 0.090, "V": 0.180}},
        {"faixa": 3, "limite": 720000,   "taxas": {"I": 0.095, "II": 0.100, "III": 0.135, "IV": 0.102, "V": 0.195}},
        {"faixa": 4, "limite": 1800000,  "taxas": {"I": 0.107, "II": 0.112, "III": 0.160, "IV": 0.140, "V": 0.205}},
        {"faixa": 5, "limite": 3600000,  "taxas": {"I": 0.143, "II": 0.147, "III": 0.210, "IV": 0.220, "V": 0.230}},
        {"faixa": 6, "limite": 4800000,  "taxas": {"I": 0.190, "II": 0.300, "III": 0.330, "IV": 0.330, "V": 0.305}},
    ]

    @classmethod
    def obter_aliquota(cls, faturamento_mensal: float, anexo: str) -> float:
        """
        Calcula o faturamento anual projetado e retorna a alíquota correspondente.
        """
        faturamento_anual = faturamento_mensal * 12
        
        for faixa in cls.TABELA_SIMPLES:
            if faturamento_anual <= faixa["limite"]:
                return faixa["taxas"].get(anexo, 0.0)
        
        # Se ultrapassar o teto de 4.8M, aplica a taxa da última faixa
        return cls.TABELA_SIMPLES[-1]["taxas"].get(anexo, 0.0)

    @classmethod
    def simular_eficiencia(cls, faturamento_mensal: float, custo_insumos: float, custo_fornecedores: float, anexo: str = "I") -> dict:
        """
        Gera os dois cenários (Com e Sem Split) espelhando a aba "Inteligência tributária".
        """
        custo_terceiros = custo_insumos + custo_fornecedores
        
        # A alíquota na planilha considera a faixa de enquadramento do faturamento total
        aliquota = cls.obter_aliquota(faturamento_mensal, anexo)
        
        # --- CENÁRIO 1: SEM EFICIÊNCIA TRIBUTÁRIA ---
        imposto_sem_split = faturamento_mensal * aliquota
        lucro_sem_split = faturamento_mensal - custo_terceiros - imposto_sem_split
        
        # --- CENÁRIO 2: COM EFICIÊNCIA TRIBUTÁRIA (SPLIT) ---
        # No split, o faturamento declarado para a Receita desconta a parte dos parceiros/fornecedores
        faturamento_com_split = faturamento_mensal - custo_terceiros
        imposto_com_split = faturamento_com_split * aliquota
        lucro_com_split = faturamento_mensal - custo_terceiros - imposto_com_split
        
        # --- RESULTADOS GLOBAIS ---
        economia_mensal = imposto_sem_split - imposto_com_split
        economia_anual = economia_mensal * 12
        
        aumento_lucro_pct = 0.0
        if lucro_sem_split > 0:
            aumento_lucro_pct = (lucro_com_split / lucro_sem_split) - 1
            
        return {
            "parametros_base": {
                "faturamento_total": faturamento_mensal,
                "custo_terceiros": custo_terceiros,
                "anexo": anexo,
                "aliquota_aplicada": aliquota
            },
            "cenario_1": {
                "nome": "Sem Eficiência Tributária",
                "faturamento_declarado": faturamento_mensal,
                "imposto": imposto_sem_split,
                "lucro": lucro_sem_split
            },
            "cenario_2": {
                "nome": "Com Eficiência Tributária",
                "faturamento_declarado": faturamento_com_split,
                "imposto": imposto_com_split,
                "lucro": lucro_com_split
            },
            "ganhos": {
                "economia_mensal": economia_mensal,
                "economia_anual": economia_anual,
                "aumento_lucro_pct": aumento_lucro_pct
            }
        }

