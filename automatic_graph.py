import os
from graphviz import Digraph
from padroes_base import padrao_h, padrao_c, padrao_pasta

#print(instructions)
def criar_diretorios() -> None:
    """
    Cria diretórios
    """
    dir_ = ("arvores", "backups")
    for _dir_ in dir_:
        if not _dir_ in os.listdir():
            os.mkdir(_dir_)

def ver_caminhos(file:str, normal:bool = True) -> list:
    """
    Trata o arquivo do caminho
    """
    def tratar_caminhos_multiplos(con:list) -> list:
        """
        Trata caminhos maiores que 2, por exemplo:
        c1 -> c2 -{ c3, c4 }- c5, c6 -> c7
        """
        def separar_operadores(texto:str) -> int:
            operadores = ["->", "}-", "-{", "}{", "<>", "<-"]
            posicao:set = set()
            texto_final:str = texto

            for _ in range(10):
                for operador in operadores:
                    if texto_final.find(operador) > -1:
                        pos = texto_final.find(operador)
                        posicao.add(pos)
                        texto_final = texto_final[:pos] + "##" + texto_final[pos+2:]

            if len(posicao) <= 1:
                return [texto]
            else:
                operacoes:list = []
                posicao:list = sorted(list(posicao))
                elementos:list = []
                operadores_achados:list = []
                
                elementos.append(texto[: posicao[0]])
                for i in range(len(posicao) - 1):
                    elementos.append(texto[posicao[i] + 2: posicao[i+1]])
                elementos.append(texto[posicao[-1]+2:])

                for i in posicao:
                    operadores_achados.append(texto[i:i+2])

                for i in range(len(operadores_achados)):
                    operacoes.append(f"{elementos[i]}{operadores_achados[i]}{elementos[i+1]}")

                return operacoes
        
        novo_con:list = []
        for temp in con:
            for operacoes in separar_operadores(temp):
                novo_con.append(operacoes)
        return novo_con

    if normal == True:
        with open("backups/backups/backups.caminhos", "r") as arq:
            con:list = arq.read()
    else:
        con = normal

    con:list = tratar_caminhos_multiplos(con.replace(" ","").split("\n"))
    deletar_pre_tratamento:list = []

    #Pré tratamento:
    for i in range(len(con)):
        if con[i].find("=") > -1:
            abreviacao, significado = con[i].split("=")
            deletar_pre_tratamento.append(i)
            for j in range(i+1, len(con)):
                con[j] = con[j].replace(abreviacao, significado)

    #Deletando pré_tratamento:
    for deleta in sorted(deletar_pre_tratamento, reverse = True):        
        del con[deleta]

    for i in range(len(con)):
        if con[i].find("#") > -1:
            con[i] = ""

        if con[i].find("<-") > -1:
            temp:list = con[i].split("<-")
            con[i] = f"{temp[1]}->{temp[0]}"
        
        #Corrigindo erros no txt:
        if con[i].find("->") > -1 and con[i].find(",") > -1:
            if con[i].find(",") < con[i].find("->") < con[i].rfind(","):
                con[i] = con[i].replace("->", "}{")
            elif con[i].find("->") > con[i].find(","):
                con[i] = con[i].replace("->", "}-")
            elif con[i].find("->") < con[i].find(","):
                con[i] = con[i].replace("->", "-{")

        if -1 < con[i].find("}-") < con[i].rfind(","):
            con[i] = con[i].replace("}-", "}{")

        if -1 < con[i].find(",") < con[i].find("-{"):
            con[i] = con[i].replace("-{", "}{")

        con[i] = con[i].split("->")
        if con[i][0].find("-{") > -1:
            temp = con[i][0].split("-{")
            temp[1] = temp[1].split(",")
            con[i] = [temp[0], temp[1][0]]
            for con_temp in temp[1][1:]:
                con.append([temp[0], con_temp])

        elif con[i][0].find("}-") > -1:
            temp = con[i][0].split("}-")
            temp[0] = temp[0].split(",")
            con[i] = [temp[0][0], temp[1]]
            for con_temp in temp[0][1:]:
                con.append([con_temp, temp[1]])

        elif con[i][0].find("}{") > -1:
            temp = con[i][0].split("}{")
            temp[0] = temp[0].split(",")
            temp[1] = temp[1].split(",")
            con[i] = [""]
            for con_temp_a in temp[0]:
                for con_temp_b in temp[1]:
                    con.append([con_temp_a, con_temp_b])

        elif con[i][0].find("<>") > -1:
            temp = con[i][0].split("<>")
            con[i] = [temp[0], temp[1]]
            con.append([temp[1], temp[0]])


    final_con:list = []
    for i in range(len(con)):
        temp_con:list = []
        if len(con[i]) > 2:
            for k in range(len(con[i]) - 1):
                temp_con.append([con[i][k], con[i][k+1]])
            final_con.extend(temp_con)
        else:
            final_con.append(con[i])

    return final_con

def ver_itens(file:str, normal:bool = True) -> dict:
    """
    Trata o arquivo do iten
    """
    if normal == True:
        with open("backups/backups/backups.itens", "r") as arq:
            iten:list = arq.read()
    else:
        iten = normal

    iten:list = iten.replace(" ","").split("\n")
    deletar_pre_tratamento = []

    #Pré tratamento:
    for i in range(len(iten)):
        if iten[i].find("=") > -1:
            abreviacao, significado = iten[i].split("=")
            deletar_pre_tratamento.append(i)
            for j in range(i+1, len(iten)):
                iten[j] = iten[j].replace(abreviacao, significado)
        if -1 < iten[i].find("#") < 5:
            deletar_pre_tratamento.append(i)

    #Deletando pré_tratamento:
    for deleta in sorted(deletar_pre_tratamento, reverse = True):        
        del iten[deleta]

    for i in range(len(iten)):
        iten[i] = iten[i].split(",")

    lens:list = list(map(len, iten))
    itens_for_del:list = []
    if max(lens) != min(lens):
        for i in range(len(lens)):
            if lens[i] != max(lens):
                itens_for_del.append(i)

    for i in sorted(itens_for_del, reverse = True):
        del iten[i]
        
    itens = {}
    for i in iten:
        if not i[0] in itens:
            itens[i[0]] = {"color":i[1],
                           "shape":i[2],
                           "style":i[3]}

    return itens

def ver_arquivo_texto(arq:str) -> list:
    """
    Lê arquivos de texto
    """
    with open(file, "r") as arq:
        file:list = arq.read()

    return file.replace(" ","").split("\n")

def tratar_itens(itens, caminhos) -> (dict, list):
    if type(caminhos) == str:
        caminhos:list = ver_caminhos(caminhos)
    if type(itens) == str:
        itens:dict = ver_itens(itens)
    return itens, caminhos

def todos_pontos(itens:dict, caminhos:list) -> dict:
    for ponto in caminhos:
        if ponto != [""]:
            if not ponto[0] in itens:
                itens[ponto[0]] = {"shape":"*",
                                   "color":"*",
                                   "style":"*"}

            if not ponto[1] in itens:
                itens[ponto[1]] = {"shape":"*",
                                   "color":"*",
                                   "style":"*"}
    return itens

def montar_grafo(itens:dict, caminhos:list, _montar_grafo_) -> None:
    """
    Monta o grafo
    """
    itens:dict
    caminhos:list
    itens, caminhos = tratar_itens(itens, caminhos)

    itens = todos_pontos(itens, caminhos)

    for iten in itens.keys():
        if itens[iten]["shape"] == "*" and itens[iten]["color"] == "*" and itens[iten]["style"] == "*":
            if iten.find(".h") > -1:
                _montar_grafo_.node(iten,
                                    shape = padrao_h["shape"],
                                    color = padrao_h["color"],
                                    style = padrao_h["style"])

            elif iten.find(".c") > -1:
                _montar_grafo_.node(iten,
                                    shape = padrao_c["shape"],
                                    color = padrao_c["color"],
                                    style = padrao_c["style"])

            elif iten.find("/") > -1:
                _montar_grafo_.node(iten,
                                    shape = padrao_pasta["shape"],
                                    color = padrao_pasta["color"],
                                    style = padrao_pasta["style"])
        else:
            _montar_grafo_.node(iten,
                         shape = itens[iten]["shape"],
                         color = itens[iten]["color"],
                         style = itens[iten]["style"])

    connection:list
    for connection in caminhos:
        try:
            _montar_grafo_.edge(connection[0], connection[1])
        except IndexError:
            pass

    return None

def captar_arquivos() -> (list, list, list):
    """
    No arquivo gerar.txt,
    ele pega os arquivos que estão na pasta 'arquivos' e foram apontados,
    na ordem:
        nome itens caminhos
    e gera o grafo    
    """
    with open("gerar.txt", "r") as arq:
        arquivos = arq.read()

    todos_nomes:list = []
    todos_itens:list = []
    todos_caminhos:list = []
    arquivos:list = arquivos.split("\n")
    for procurar in arquivos:
        if procurar.find("#") == -1:
            if len(procurar.split(" ")) == 3:
                nomes:str
                itens:str
                caminhos:str
                nome, iten, caminho = procurar.split(" ")

                todos_nomes.append(nome)
                todos_itens.append(iten)
                todos_caminhos.append(caminho)
            else:
                if procurar != "":
                    pass
    return todos_nomes, todos_itens, todos_caminhos

def gerar_grafo(itens:str, caminhos:str, nome:str, pasta:str) -> None:
    """
    Gera o grafo de maneira rápida
    """    
    grafo = Digraph(nome, format='png')
    montar_grafo(itens, caminhos, grafo)
    grafo.render(filename = os.path.join(pasta, nome), cleanup = True, format = 'png', engine = 'dot')

criar_diretorios()
if __name__ == "__main__":    
    nome:list
    itens:list
    caminhos:list
    nomes, itens, caminhos = captar_arquivos()

    for i in range(len(nomes)):
        nome:str = nomes[i]
        iten:dict = itens[i]
        caminho:list = caminhos[i]

        grafo = Digraph(nome, format='png')
        montar_grafo(iten, caminho, grafo)
        grafo.render(filename = f'arvores§/{nome}', cleanup = True, format = 'png', engine = 'dot')
