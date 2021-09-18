import tc.afd as afd

# Recebe um AFD
# Olhe o arquivo unit.py para ter exemplos de entrada e saída da função
def tfa_table(automato): 
    estados = list(automato[0])
    estados.sort()
        
    table = {}

    for i, estado1 in enumerate(estados[:-1]):
        for estado2 in estados[i+1:]:
            table[(estado1, estado2)] = ''
    
    return table

def tfa_fill(automato):
    table = tfa_table(automato)
    table_aux = {}

    for pair in list(table):
        # Se apenas um dos dois estados do par for final, o par é distinguivel
        if (pair[0] in automato[4]) != (pair[1] in automato[4]):
            table[pair] = 'd'
        else:
            table_aux[pair] = table[pair]
    
    achou_novos = True

    while achou_novos:
        # Caso não encontre nenhum par novo que seja distinguivel, o algoritmo chegou ao fim
        achou_novos = False
        for pair in list(table_aux):
            for simbolo in automato[1]:
                r = s = {}
                try:
                    r = afd.delta(automato, pair[0], simbolo)
                    s = afd.delta(automato, pair[1], simbolo)
                except KeyError:
                    continue
                
                pair_aux = None
                if (r, s) in table:
                    pair_aux = (r, s)
                elif (s, r) in table:
                    pair_aux = (s, r)
                else:
                    continue

                if table[pair_aux] == 'd':
                    table[pair] = 'd'
                    if pair in table_aux:
                        del table_aux[pair]
                    achou_novos = True

    # Para cada par que não for distinguivel, marcá-lo como indistinguivel
    for pair in list(table):
        if table[pair] != 'd':
            table[pair] = 'i'

    return table

def tfa(automato):
    table = tfa_fill(automato)
    y = []
    
    for x in list(table):
        if table[x] == 'i':
            y.append(x)

    eq = set(tuple(i) for i in y)
    return eq


#24 AFD produto
#Criar uma função que recebe dois autômatos e retorna o AFD produto entre eles.
#Atenção:
#A assinatura da função deverá ser afd_produto(automato1, automato2).
#Essa função deverá ser criada no arquivo (prop_lr.py).

#Aluno: Matheus Rodrigues Rodrigues

def afd_produto(automato1, automato2):

    estados_automato1 = list(automato1[0])
    estados_automato2 = list(automato2[0])
    dicio_automato1 = automato1(2)
    dicio_automato2 = automato2(2)
    estfinal_automato1 = list(automato1[4])
    estfinal_automato2 = list(automato2[4])

    caracteres = list(automato1(1))

    afd_prod_estados = []
    afd_prod_dicio = {}
    afd_prod_final = []

    #Cria o nome dos novos estados
    for estadocont1 in estados_automato1:

        for estadocont2 in estados_automato2:
            estado1 = estados_automato1(estadocont1)
            estado2 = estados_automato2(estadocont2)
            estado3 = estado1 + "," + estado2
            afd_prod_estados.append(estado3)

            if estado1 in estfinal_automato1 and estado2 not in estfinal_automato2:
                afd_prod_final.append(estado3)

            for caractere in caracteres:
                caractere_atual = caracteres[caractere]
                estado_relacionado1 = dicio_automato1[(estado1, caracteres[caractere])]
                estado_relacionado2 = dicio_automato2[(estado2, caracteres[caractere])]
                estado_afd_prod = estado_relacionado1 + "," + estado_relacionado2
                afd_prod_dicio[(estado3, caractere_atual)] = estado_afd_prod

    afd_produto = {set(afd_prod_estados), set(caracteres), afd_prod_dicio, string(afd_prod_estados[0]), set(afd_prod_final)}

    return afd_produto


def print_table(table, QSet, d_symbol = 'd', i_symbol = 'i'):
    states = list(QSet)
    states.sort()

    col_size = 5                                        # Define o tamanho padrao das colunas da tabela em caracteres
    
    for element in states:                              # Verifica se o tamanho padrao é menor do que o tamanho do maior
        col_size = max(len(element), col_size)          # estado, e caso sim, define o novo tamanho da coluna

    result = ''                                         

    for index, value in enumerate(states[1:]):          # Itera os elementos a partir do segundo, linhas da tabela
        
        result += f'{value}'.ljust(col_size)            # Concatena o estado atual da tabela completando com espacos
                                                        # a direita o tamanho da coluna
        
        for value2 in states[:index + 1]:               # Itera os elementos até o penultimo estado, colunas da tabela
            result += '|'                               # adicionando os elementos no formato da tabela
            result += f'{table[(value2, value)]}' \
                    .rjust(col_size//2 + 1).ljust(col_size)

        result += '|\n'

    result +=''.ljust(col_size)                         # Insere espaços para mostrar os indices das colunas na direcao certa

    for value in states[:-1]:                       
        result += f'{value}'\
            .rjust(col_size//2 + 2)\
            .ljust(col_size + 1)                        # Mostra os indices das colunas

    masked_result = result.replace(' d ', f' {d_symbol} '\
                    .ljust(3))\
                    .replace(' i ', f' {i_symbol} '\
                    .ljust(3))                          # Mascara os marcadores de destinguinvel e indestinguinvel com os simbolos indicados

    return masked_result