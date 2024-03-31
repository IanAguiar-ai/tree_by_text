import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from automatic_graph import criar_diretorios, gerar_grafo
from os import path, mkdir, listdir
from re import sub

texto = {"nome":{"ing":"Graph Assembler","pt":"Montador de Grafos"},
         "aviso":{"ing":"Notice", "pt":"Aviso"},
         "instrucoes":{"ing":"Instructions", "pt":"Instruções"},
         "sua_imagem":{"ing":"Your image is in", "pt":"Sua imagem está em"},
         "exportar":{"ing":"Export", "pt":"Exportar"},
         "importar":{"ing":"Import", "pt":"Importar"},
         "compilar":{"ing":"To compile", "pt":"Compilar"},
         "instrucao_export":{"ing":"In the file on the left (items), put the name of the file, for example, <o_nome_entre_os_simbolos>","pt":"No arquivo da esquerda (itens), coloque o nome do arquivo, por exemplo, <o_nome_entre_os_simbolos>"}}

def suave_desca(inicio:int, fim:int) -> list:
    valores:list = []
    valor:float = inicio
    i = 2.5
    while True:
        #i *= 0.97
        i -= 0.062
        if i < 0.1:
            i = 0.1
        valor += i
        if valor >= fim:
            valores.append(fim)
            return valores
        else:
            valores.append(valor)

def suave_suba(inicio:int, fim:int) -> list:
    valores:list = []
    valor:float = inicio
    i = 0
    while True:
        #i *= 0.97
        i += 0.062
        valor -= i
        if valor <= fim:
            valores.append(fim)
            return valores
        else:
            valores.append(valor)

class Aplicativo(tk.Tk):
    def __init__(self):
        cores = {"fundo":"#4e4e4e",
                 "botao":{"bg":"#333333", "fg":"white"},
                 "?":{"bg":"#8d8d8e", "fg":"white"},
                 "popup":"#8d8d8e"}
        self.__animacao = False
        self.__instrucoes = None
        
        super().__init__()
        self.title(texto["nome"][idioma])
        self.configure(bg = cores["fundo"])
        self.geometry("600x400")

        #Caixa de animação:
        self.caixa_animacao = tk.Label(self, text = "Salvo", bg = cores["popup"], bd = 1, relief = "solid", font = ("Times", 20))
        self.caixa_animacao.place(x = 20, y= -32)
    
        # Criando as caixas de texto
        self.caixa_texto1 = tk.Text(self, width = 40, height = 30, font = "Times 12", borderwidth = 2, relief = "sunken")
        self.caixa_texto2 = tk.Text(self, width = 40, height = 30, font = "Times 12", borderwidth = 2, relief = "sunken")
    
        # Posicionando as caixas de texto usando grid
        self.caixa_texto1.grid(row = 0, column = 0, columnspan = 1, padx = 10, pady = 10, sticky = "nsew")
        self.caixa_texto2.grid(row = 0, column = 1, columnspan = 3, padx = 10, pady = 10, sticky = "nsew")
    
        # Criando os botões
        self.botao_duvida = tk.Button(self, text = "?", command = self.duvida, bg = cores["?"]["bg"], fg = cores["?"]["fg"])
        self.botao_exportar = tk.Button(self, text = texto["exportar"][idioma], command = self.exportar, bg = cores["botao"]["bg"], fg = cores["botao"]["fg"])
        self.botao_importar = tk.Button(self, text = texto["importar"][idioma], command = self.importar, bg = cores["botao"]["bg"], fg = cores["botao"]["fg"])
        self.botao_compilar = tk.Button(self, text = texto["compilar"][idioma], command = self.compilar, bg = cores["botao"]["bg"], fg = cores["botao"]["fg"])
    
        # Posicionando os botões usando grid
        self.botao_duvida.grid(row = 1, column = 3, columnspan = 1, padx = 5, pady = 0, sticky = "ew")
        self.botao_exportar.grid(row = 1, column = 1, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_importar.grid(row = 1, column = 0, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_compilar.grid(row = 2, column = 0, columnspan = 4, padx = 10, pady = 10, sticky = "ew")

        # Configurando a geometria da janela para redimensionamento
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.resizable(True, True)       

        # Atualizar a altura das caixas de texto ao redimensionar
        self.bind("<Configure>", self.atualizar_altura_caixas_texto)
  
    def atualizar_altura_caixas_texto(self, event) -> None:
        """
        Ajustas os limites das caixas dependendo do tamanho da tela
        """
        altura = event.height // 25 
        self.caixa_texto1.config(height = altura)
        self.caixa_texto2.config(height = altura)

    def duvida(self) -> None:
        """
        Mostra uma série de instruções para o uso do programa
        """
        if self.__instrucoes == None:
            self.__instrucoes = _instrucoes_()
            self.__instrucoes.mainloop()
            return 

        try:
            if not self.__instrucoes.winfo_exists():
                self.__instrucoes = _instrucoes_()
                self.__instrucoes.mainloop()
                return
        except:
            self.__instrucoes = _instrucoes_()
            self.__instrucoes.mainloop()
            return

    def exibir_popup_salvo(self):
        if not self.__animacao:
            self.caixa_animacao.lift()  # Eleva a caixa acima de outros widgets
            self.__animacao = True
            for i in suave_desca(-32, 20):
                self.caixa_animacao.place(y = int(i))  # Nova posição absoluta em pixels
                self.update()
                self.after(17)
            self.after(500)
            for i in suave_suba(20, -32):
                self.caixa_animacao.place(y = i)  # Nova posição absoluta em pixels
                self.update()
                self.after(17)
            self.__animacao = False

    def salvar(self, pasta_escolhida:str, nome_conteudo:str, conteudo1:str, conteudo2:str) -> bool:
        """
        Salva os arquivos
        """
        if pasta_escolhida and nome_conteudo.replace(" ","") != "":
            if not nome_conteudo in listdir(pasta_escolhida):
                mkdir(path.join(pasta_escolhida, nome_conteudo)) #Criando a pasta para salvar o arquivo:
            with open(path.join(pasta_escolhida, nome_conteudo, f"{nome_conteudo}.itens"), "w") as f:
                f.write(conteudo1) # Escreve o conteúdo das caixas de texto no arquivo
            with open(path.join(pasta_escolhida, nome_conteudo, f"{nome_conteudo}.caminhos"), "w") as f:
                f.write(conteudo2) # Escreve o conteúdo das caixas de texto no arquivo
            self.exibir_popup_salvo()
            return True
        return False

    def exportar(self) -> None:
        """
        Função que exporta os textos atuais para arquivos .itens e .caminho na pasta selecionada
        """
        conteudo1:str = self.caixa_texto1.get("1.0", tk.END) # Obtém todo o texto da caixa de texto 1
        conteudo2:str = self.caixa_texto2.get("1.0", tk.END) # Obtém todo o texto da caixa de texto 2

        if conteudo1.find("<") != -1 and conteudo1.find(">") != -1:
            nome_conteudo:str = conteudo1[conteudo1.find("<")+1: conteudo1.find(">")]
        else:
            messagebox.showwarning(texto["aviso"][idioma], texto["instrucao_export"][idioma])
            return

        pasta_escolhida:str = filedialog.askdirectory()
        self.salvar(pasta_escolhida, nome_conteudo, conteudo1, conteudo2)        

    def importar(self) -> None:
        """
        Importa uma pasta com arquivos .itens e .caminhos e joga para as caixas
        """
        pasta_escolhida:str = filedialog.askdirectory()

        if pasta_escolhida:
            diretorio_escolhido:str = path.basename(pasta_escolhida) #Também será o nome dos arquivos
            
            if f"{diretorio_escolhido}.itens" in listdir(pasta_escolhida):
                with open(path.join(pasta_escolhida, f"{diretorio_escolhido}.itens"), "r") as arquivo:
                    conteudo1_novo:str = arquivo.read()
                self.caixa_texto1.delete("1.0", tk.END) # Apagando o texto antigo da caixa de texto 1
                self.caixa_texto1.insert(tk.END, conteudo1_novo) # Adicionando novo texto à caixa de texto 1
                
            if f"{diretorio_escolhido}.caminhos" in listdir(pasta_escolhida):
                with open(path.join(pasta_escolhida, f"{diretorio_escolhido}.caminhos"), "r") as arquivo:
                    conteudo2_novo:str = arquivo.read()
                self.caixa_texto2.delete("1.0", tk.END) # Apagando o texto antigo da caixa de texto 2
                self.caixa_texto2.insert(tk.END, conteudo2_novo) # Adicionando novo texto à caixa de texto 2

    def compilar(self) -> None:
        conteudo1:str = self.caixa_texto1.get("1.0", tk.END) # Obtém todo o texto da caixa de texto 1
        nome_conteudo:str = conteudo1[conteudo1.find("<")+1: conteudo1.find(">")]
        conteudo1:str = sub(r"<.*?>", "",conteudo1)
        conteudo2:str = self.caixa_texto2.get("1.0", tk.END) # Obtém todo o texto da caixa de texto 2

        pasta_escolhida:str = filedialog.askdirectory() #Pasta onde será salvo o grafo
        if pasta_escolhida:
            if not "backups" in listdir():
                criar_diretorios()
            self.salvar("backups", "backups", conteudo1, conteudo2)   
            gerar_grafo(conteudo1, conteudo2, nome_conteudo, pasta_escolhida)
            messagebox.showwarning(texto["aviso"][idioma], f"{texto['sua_imagem'][idioma]} '{pasta_escolhida}/{nome_conteudo}'")

class _instrucoes_(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(texto["instrucoes"][idioma])
        self.geometry("500x400")

        self.texto_instrucoes = ("""
#Templates:
[pasta] = orange, folder, filled
[variavel_1] = red, box, dotted
[variavel_2] = orange, doubleoctagon, dotted

#Pastas:
pasta_1, [pasta]
pasta_2, [pasta]
pasta_3, [pasta]

#Variaveis:
var_1, [variavel_1]
var_2, [variavel_1]
var_3, [variavel_1]
var_4, [variavel_2]

#Resumos:
variaveis_indiretas = var_10.c, var_11.h, var_ 12

#Caminho de pastas:
pasta_1 -{ pasta_2, pasta_3
pasta_2 -> /pasta_4 -> /pasta_5

#Caminho das variáveis:
pasta_3 -{ /pasta_6, var_1, var_2
var_2, var_3 }{ variaveis_indiretas, var_7

#Dependencia:
a <> b

Um exemplo do arquivo de itens é:
{exemplo_itens}
-----------------------------------------------------------

Onde existir '#' o programa ignora a leitura desta linha.

Um exemplo do arquivo de caminhos:
{exemplo_caminho}
-----------------------------------------------------------

'->' Faz uma ligação um a um;
'<-' Faz uma ligação um a um invertido;
'-{chr(123)}' Faz uma ligação um para varios;
'{chr(125)}-' Faz uma ligação varios para um;
'{chr(125)}{chr(123)}' Faz uma ligação varios para varios;
'=' Define uma variável como vários itens;
'<>' Ligação dupla, por exemplo, a <> b é a mesma coisa que a -> b + b -> a;


Formato do arquivo com os itens:
\tname, color, shape, style

colors:
    blue
    red
    yellow
    green
    lightblue

shapes:
    folder
    rectangle
    parallelogram
    trapezium
    doublecircle
    diamond
    oval
    box
    plaintext
    doubleoctagon

style:
    filled
    solid
    dashed
    dotted
    invisible
""")

        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.texto = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD)
        self.texto.pack(fill=tk.BOTH, expand=True)
        self.texto.insert(tk.END, self.texto_instrucoes)

if __name__ == "__main__":
    idioma = messagebox.askquestion("Language selection", "Do you want to run the program in English?",
                                      icon='info', 
                                      type='yesno')
    if idioma == "yes":
        idioma = "ing"
    else:
        idioma = "pt"
    app = Aplicativo()
    app.mainloop()
