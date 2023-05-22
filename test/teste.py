import operator

# Dicionário com as funções Python correspondentes a cada operador
operadores = {'>': operator.gt, '<': operator.lt, '>=': operator.ge, '<=': operator.le, '==': operator.eq}

# Dicionário com o valor da comparação
indicador1 = {'meta': 10, 'pontuacao': 3, 'comparacao': '>='}

# Selecionar a função correspondente ao operador desejado
operador = operadores[indicador1['comparacao']]

# Fazer a comparação com o valor desejado
valor = 5
if operador(valor, indicador1['meta']):
    print("O valor é maior ou igual à meta.")
else:
    print("O valor é menor do que a meta.")
