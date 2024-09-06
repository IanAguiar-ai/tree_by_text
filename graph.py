import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from automatic_graph import criar_diretorios, gerar_grafo, ver_itens, ver_caminhos
from os import path, mkdir, listdir
from re import sub
from time import sleep
import threading

texto = {"nome":{"ing":"Graph Assembler","pt":"Montador de Grafos"},
         "aviso":{"ing":"Notice", "pt":"Aviso"},
         "instrucoes":{"ing":"Instructions", "pt":"Instruções"},
         "sua_imagem":{"ing":"Your image is in", "pt":"Sua imagem está em"},
         "exportar":{"ing":"Export", "pt":"Exportar"},
         "importar":{"ing":"Import", "pt":"Importar"},
         "compilar":{"ing":"To compile", "pt":"Compilar"},
         "salvo":{"ing":"Saved", "pt":"Salvo"},
         "cor":{"ing":"Color", "pt":"Cor"},
         "lingua":{"ing":"Language", "pt":"Lingua"},
         "indefinido":{"ing":"Undefined", "pt":"Indefinido"},
         "definidos":{"ing":"Defined", "pt":"Definidos"},
         "esperando":{"ing":"Waiting...", "pt":"Esperando..."},
         "itens":{"ing":"Itens", "pt":"Itens"},
         "caminhos":{"ing":"Paths", "pt":"Caminhos"},
         "salvar":{"ing":"Save", "pt":"Salvar"},
         "voltar":{"ing":"Back", "pt":"Voltar"},
         "erro_diretorio":{"ing":"First export your project to some folder!", "pt":"Primeiro exporte seu projeto para alguma pasta!"},
         "instrucao_export":{"ing":"In the file on the left (items), put the name of the file, for example, <o_nome_entre_os_simbolos>","pt":"No arquivo da esquerda (itens), coloque o nome do arquivo, por exemplo, <o_nome_entre_os_simbolos>"}}

cores = {"fundo":{"escuro":"#4e4e4e", "claro":"#b5b5b5"},
         "botao":{"escuro":{"bg":"#333333", "fg":"white"}, "claro":{"bg":"#cccccc", "fg":"black"}},
         "?":{"escuro":{"bg":"#8d8d8e", "fg":"white"}, "claro":{"bg":"#898989", "fg":"black"}},
         "popup":{"escuro":"#727271", "claro":"#b1b1b4"}}

def suave_desca(inicio:int, fim:int) -> list:
    valores:list = []
    valor:float = inicio
    i:float = 2.5
    while True:
        #i *= 0.97
        i -= 0.062
        if i < 0.2:
            i = 0.2
        valor += i
        if valor >= fim:
            valores.append(fim)
            return valores
        else:
            valores.append(valor)

def suave_suba(inicio:int, fim:int) -> list:
    valores:list = []
    valor:float = inicio
    i:float = 0
    while True:
        #i *= 0.97
        i += 0.1#0.062
        valor -= i
        if valor <= fim:
            valores.append(fim)
            return valores
        else:
            valores.append(valor)

class Aplicativo(tk.Tk):
    def __init__(self):
        self.__animacao = False
        self.__instrucoes = None
        self.__cor = "escuro"
        self.__idioma = "ing"
        self.__tamanho = 14
        self.__memoria = 16
        self.__memoria_caixa_1 = [" ", " "]
        self.__memoria_caixa_2 = [" ", " "]
        self.__diretorio_salvar = None
        self.__nome_conteudo = None
        
        super().__init__()
        self.title(texto["nome"][self.__idioma])
        self.configure(bg = cores["fundo"][self.__cor])
        self.geometry("700x500")

        #Caixa de animação:
        self.caixa_animacao = tk.Label(self, text = texto["salvo"][self.__idioma], bg = cores["popup"][self.__cor], fg = "White", bd = 1, relief = "solid", font = ("Times", 20))
        self.caixa_animacao.place(x = 20, y= -32)
    
        # Criando as caixas de texto
        self.caixa_texto1 = tk.Text(self, width = 40, height = 30, font = f"Times {self.__tamanho}", borderwidth = 5, relief = "sunken")
        self.caixa_texto2 = tk.Text(self, width = 40, height = 30, font = f"Times {self.__tamanho}", borderwidth = 5, relief = "sunken")
        self.caixa_texto3 = tk.Text(self, width = 25, height = 30, font = f"Times {self.__tamanho}", borderwidth = 5, relief = "sunken")
    
        # Posicionando as caixas de texto usando grid
        self.caixa_texto1.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "nsew")
        self.caixa_texto2.grid(row = 0, column = 2, columnspan = 2, padx = 5, pady = 5, sticky = "nsew")
        self.caixa_texto3.grid(row = 0, column = 4, columnspan = 3, padx = 5, pady = 5, sticky = "nsew")
    
        # Criando os botões
        self.botao_duvida = tk.Button(self, font = f"Times {self.__tamanho}", text = "?", command = self.duvida, bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_exportar = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["exportar"][self.__idioma], command = self.exportar, bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_importar = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["importar"][self.__idioma], command = self.importar, bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_compilar = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["compilar"][self.__idioma], command = self.compilar, bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_cor = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["cor"][self.__idioma], command = self.mudar_cor, bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_linguagem = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["lingua"][self.__idioma], command = self.mudar_lingua, bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_aumentar = tk.Button(self, font = f"Times {self.__tamanho}", text = "+", command = self.aumentar_letra, bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_diminuir = tk.Button(self, font = f"Times {self.__tamanho}", text = "-", command = self.diminuir_letra, bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_memoria_caixa_1 = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["voltar"][self.__idioma], command = self.voltar_caixa_1, bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_memoria_caixa_2 = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["voltar"][self.__idioma], command = self.voltar_caixa_2, bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_salvar = tk.Button(self, font = f"Times {self.__tamanho}", text = texto["salvar"][self.__idioma], command = self.salvar_rapido, bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])


        # Posicionando os botões usando grid
        self.botao_duvida.grid(row = 2, column = 4, columnspan = 1, padx = 10, pady = 0, sticky = "ew")
        self.botao_exportar.grid(row = 2, column = 3, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_importar.grid(row = 2, column = 2, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_compilar.grid(row = 2, column = 0, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_cor.grid(row = 2, column = 5, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_linguagem.grid(row = 1, column = 4, columnspan = 2, padx = 10, pady = 10, sticky = "ew")
        self.botao_aumentar.grid(row = 1, column = 6, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_diminuir.grid(row = 2, column = 6, columnspan = 1, padx = 10, pady = 10, sticky = "ew")
        self.botao_memoria_caixa_1.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = "ew")
        self.botao_memoria_caixa_2.grid(row = 1, column = 2, columnspan = 2, padx = 10, pady = 10, sticky = "ew")
        self.botao_salvar.grid(row = 2, column = 1, columnspan = 1, padx = 10, pady = 10, sticky = "ew")

        # Configurando a geometria da janela para redimensionamento
        self.grid_columnconfigure(0, weight = 1) #Janela 1 em 0, com tamanho 2
        self.grid_columnconfigure(1, weight = 1) #Botões em 0 e 1
        self.grid_columnconfigure(2, weight = 1) #Janela 2 em 2, com tamanho 2
        self.grid_columnconfigure(3, weight = 1) #Botões em 2 e 3
        self.grid_rowconfigure(0, weight = 1)
        self.resizable(True, True)       

        # Atualizar a altura das caixas de texto ao redimensionar
        self.bind("<Configure>", self.atualizar_altura_caixas_texto)

        # Iniciar a thread
        threading.Thread(target = self.atualizar_caixa).start()
        threading.Thread(target = self.memoria_caixas).start()
  
    def atualizar_altura_caixas_texto(self, event) -> None:
        """
        Ajustas os limites das caixas dependendo do tamanho da tela
        """
        altura = event.height // 25 
        self.caixa_texto1.config(height = altura)
        self.caixa_texto2.config(height = altura)

    def mudar_lingua(self) -> None:
        """
        Muda a lingua
        """
        if self.__idioma == "ing":
            self.__idioma = "pt"
        else:
            self.__idioma = "ing"

        self.botao_exportar.config(text = texto["exportar"][self.__idioma])
        self.botao_importar.config(text = texto["importar"][self.__idioma])
        self.botao_compilar.config(text = texto["compilar"][self.__idioma])
        self.botao_cor.config(text = texto["cor"][self.__idioma])
        self.botao_linguagem.config(text = texto["lingua"][self.__idioma])
        self.botao_memoria_caixa_1.config(text = texto["voltar"][self.__idioma])
        self.botao_memoria_caixa_2.config(text = texto["voltar"][self.__idioma])
        self.botao_salvar.config(text = texto["salvar"][self.__idioma])
        self.title(texto["nome"][self.__idioma])

    def mudar_cor(self) -> None:
        """
        Muda entre o modo claro e escuro
        """
        if self.__cor == "escuro":
            self.__cor = "claro"
        else:
            self.__cor = "escuro"

        self.configure(bg = cores["fundo"][self.__cor])
        self.botao_duvida.config(bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_exportar.config(bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_importar.config(bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_compilar.config(bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_cor.config(bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_linguagem.config(bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])
        self.botao_aumentar.config(bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_diminuir.config(bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_memoria_caixa_1.config(bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_memoria_caixa_2.config(bg = cores["?"][self.__cor]["bg"], fg = cores["?"][self.__cor]["fg"])
        self.botao_salvar.config(bg = cores["botao"][self.__cor]["bg"], fg = cores["botao"][self.__cor]["fg"])

    def mudar_tamanho(self) -> None:
        """
        Configura fonte
        """
        self.botao_exportar.config(font = f"Times {self.__tamanho}")
        self.botao_importar.config(font = f"Times {self.__tamanho}")
        self.botao_compilar.config(font = f"Times {self.__tamanho}")
        self.botao_cor.config(font = f"Times {self.__tamanho}")
        self.botao_linguagem.config(font = f"Times {self.__tamanho}")
        self.botao_aumentar.config(font = f"Times {self.__tamanho}")
        self.botao_diminuir.config(font = f"Times {self.__tamanho}")
        self.botao_duvida.config(font = f"Times {self.__tamanho}")
        self.caixa_texto1.config(font = f"Times {self.__tamanho}")
        self.caixa_texto2.config(font = f"Times {self.__tamanho}")
        self.caixa_texto3.config(font = f"Times {self.__tamanho}")
        self.botao_memoria_caixa_1.config(font = f"Times {self.__tamanho}")
        self.botao_memoria_caixa_2.config(font = f"Times {self.__tamanho}")
        self.botao_salvar.config(font = f"Times {self.__tamanho}")

    def aumentar_letra(self) -> None:
        """
        Aumenta a letra
        """
        self.__tamanho += 1
        if self.__tamanho > 36:
            self.__tamanho = 36
        self.mudar_tamanho()

    def diminuir_letra(self) -> None:
        """
        Diminue a letra
        """
        self.__tamanho -= 1
        if self.__tamanho < 6:
            self.__tamanho = 6
        self.mudar_tamanho()

    def atualizar_caixa(self) -> None:
        """
        Atualiza o contador de caracteres na caixa_texto3 a cada 5 segundos
        """
        try:
            texto1:str = " "
            texto2:str = " "
            while True:
                if texto1 != self.caixa_texto1.get("1.0", "end-1c") or texto2 != self.caixa_texto2.get("1.0", "end-1c"):
                    complemento_1, complemento_2, complemento_3, nome_conteudo = self.obter_complementos()
                    texto1:str = self.caixa_texto1.get("1.0", "end-1c")
                    texto2:str = self.caixa_texto2.get("1.0", "end-1c")

                    self.__nome_conteudo = nome_conteudo
                    self.atualizar_caixa_texto3(texto1, texto2, nome_conteudo, complemento_1, complemento_2, complemento_3)
                    delay = 0
                sleep(min(0.25 + delay * 0.05, 1))
                delay += 1
        except RuntimeError:
            pass

    def memoria_caixas(self) -> None:
        while True:
            if self.caixa_texto1.get("1.0", "end-1c") != self.__memoria_caixa_1[-1]:
                self.__memoria_caixa_1.append(self.caixa_texto1.get("1.0", "end-1c"))
                if len(self.__memoria_caixa_1) > self.__memoria:
                    self.__memoria_caixa_1 = self.__memoria_caixa_1[-self.__memoria//2:]
            if self.caixa_texto2.get("1.0", "end-1c") != self.__memoria_caixa_2[-1]:
                self.__memoria_caixa_2.append(self.caixa_texto2.get("1.0", "end-1c"))
                if len(self.__memoria_caixa_2) > self.__memoria:
                    self.__memoria_caixa_2 = self.__memoria_caixa_2[-self.__memoria//2:]
            sleep(10)

    def voltar_caixa_1(self) -> None:
        """
        Volta o estado anterior da caixa 1
        """
        #print(self.__memoria_caixa_1)
        if len(self.__memoria_caixa_1) >= 3 and self.__memoria_caixa_1[-1] == self.caixa_texto1.get("1.0", "end-1c"):
            self.caixa_texto1.delete("1.0", "end")
            self.caixa_texto1.insert("1.0", self.__memoria_caixa_1[-2])
            self.__memoria_caixa_1 = self.__memoria_caixa_1[:-2]
        elif len(self.__memoria_caixa_1) >= 2:
            self.caixa_texto1.delete("1.0", "end")
            self.caixa_texto1.insert("1.0", self.__memoria_caixa_1[-1])
            self.__memoria_caixa_1 = self.__memoria_caixa_1[:-1]

    def voltar_caixa_2(self) -> None:
        """
        Volta o estado anterior da caixa 2
        """
        #print(self.__memoria_caixa_2)
        if len(self.__memoria_caixa_2) >= 3 and self.__memoria_caixa_2[-1] == self.caixa_texto2.get("1.0", "end-1c"):
            self.caixa_texto2.delete("1.0", "end")
            self.caixa_texto2.insert("1.0", self.__memoria_caixa_2[-2])
            self.__memoria_caixa_2 = self.__memoria_caixa_2[:-2]
        elif len(self.__memoria_caixa_2) >= 2:
            self.caixa_texto2.delete("1.0", "end")
            self.caixa_texto2.insert("1.0", self.__memoria_caixa_2[-1])
            self.__memoria_caixa_2 = self.__memoria_caixa_2[:-1]

    def obter_complementos(self) -> (str, str, str, str):
        """
        Obtém os complementos para exibir na caixa_texto3
        """
        complemento_1:str = texto["esperando"][self.__idioma]
        complemento_2:str = ""
        complemento_3:str = ""
        nome_conteudo:str = ""

        try:
            conteudo1:str = self.caixa_texto1.get("1.0", tk.END)
            if conteudo1.find("<") != -1 and conteudo1.find(">") != -1:
                nome_conteudo:str = conteudo1[conteudo1.find("<")+1: conteudo1.find(">")]

            itens:dict = ver_itens("", conteudo1)
            complemento_1:str = f"{texto['definidos'][self.__idioma]}:\n"
            n:int = 1
            caminhos_conhecidos:set = set(itens.keys())
            for i in itens:
                complemento_1 += f"  ({n:02}) {i}\n"
                n += 1
        except Exception as ex:
            print(ex)

        try:
            caminhos:list = ver_caminhos("", self.caixa_texto2.get("1.0", tk.END))
            todos_caminhos:set = set()
            variaveis:dict = {}
            for a in caminhos:
                if len(a) == 2:
                    todos_caminhos.add(a[0])
                    todos_caminhos.add(a[1])
                    if not a[0] in variaveis:
                        variaveis[a[0]]:set = {a[1]}
                    else:
                        variaveis[a[0]].add(a[1])
            #print(variaveis)
            
            for var in sorted(variaveis):
                complemento_3 += f"\n{var}:\n"
                n = 1
                for individual in variaveis[var]:
                    complemento_3 += f" ({n:02}) {individual}\n"
                    n += 1

            if len(caminhos_conhecidos) > 0:
                faltantes:set = todos_caminhos.difference(caminhos_conhecidos)
    
            if "faltantes" in locals():
                if len(faltantes) != 0:
                    complemento_2 = f"{texto['indefinido'][self.__idioma]}:\n"

            n:int = 1    
            for falta in sorted(faltantes):
                complemento_2 += f"  ({n:02}) {falta}\n"
                n += 1
        except Exception as ex:
            print(ex)

        return complemento_1, complemento_2, complemento_3, nome_conteudo

    def atualizar_caixa_texto3(self, texto1, texto2, nome_conteudo, complemento_1, complemento_2, complemento_3) -> None:
        """
        Atualiza o texto na caixa_texto3
        """
        self.caixa_texto3.config(state = "normal")
        self.caixa_texto3.delete("1.0", "end")
        self.caixa_texto3.insert("1.0", f"{texto['itens'][self.__idioma]}: {len(texto1)} chr\n{texto['caminhos'][self.__idioma]}: {len(texto2)} chr\nNome: {nome_conteudo}\n\n{complemento_1}\n{complemento_2}\n{complemento_3}")
        self.caixa_texto3.config(state = "disabled")

    def duvida(self) -> None:
        """
        Mostra uma série de instruções para o uso do programa
        """
        if self.__instrucoes == None:
            self.__instrucoes = _instrucoes_(self.__idioma)
            self.__instrucoes.mainloop()
            return

        try:
            if not self.__instrucoes.winfo_exists():
                self.__instrucoes = _instrucoes_(self.__idioma)
                self.__instrucoes.mainloop()
                return
        except:
            self.__instrucoes = _instrucoes_(self.__idioma)
            self.__instrucoes.mainloop()
            return

    def exibir_popup_salvo(self) -> None:
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
                f.write(conteudo1) #Escreve o conteúdo das caixas de texto no arquivo
            with open(path.join(pasta_escolhida, nome_conteudo, f"{nome_conteudo}.caminhos"), "w") as f:
                f.write(conteudo2) #Escreve o conteúdo das caixas de texto no arquivo

            threading.Thread(target = self.exibir_popup_salvo).start()
            #self.exibir_popup_salvo()
            return True
        return False

    def capturar_conteudo(self) -> (str, str):
        """
        Captura o conteudo atual nas caixas
        """
        conteudo1:str = self.caixa_texto1.get("1.0", tk.END) #Obtém todo o texto da caixa de texto 1
        conteudo2:str = self.caixa_texto2.get("1.0", tk.END) #Obtém todo o texto da caixa de texto 2
        return conteudo1, conteudo2

    def exportar(self) -> None:
        """
        Função que exporta os textos atuais para arquivos .itens e .caminho na pasta selecionada
        """
        conteudo1, conteudo2 = self.capturar_conteudo()

        if conteudo1.find("<") != -1 and conteudo1.find(">") != -1:
            nome_conteudo:str = conteudo1[conteudo1.find("<")+1: conteudo1.find(">")]
        else:
            messagebox.showwarning(texto["aviso"][self.__idioma], texto["instrucao_export"][self.__idioma])
            return

        pasta_escolhida:str = filedialog.askdirectory()
        self.salvar(pasta_escolhida, nome_conteudo, conteudo1, conteudo2)

        self.__diretorio_salvar = pasta_escolhida #Memoriza o diretório para salvar rapidamente
        self.__nome_conteudo = nome_conteudo

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

        self.__diretorio_salvar = pasta_escolhida #Memoriza o diretório para salvar rapidamente

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
            messagebox.showwarning(texto["aviso"][self.__idioma], f"{texto['sua_imagem'][self.__idioma]} '{pasta_escolhida}/{nome_conteudo}'")

    def salvar_rapido(self) -> None:
        if self.__diretorio_salvar == None or self.__nome_conteudo == None:
            messagebox.showwarning(texto["aviso"][self.__idioma], f"{texto['erro_diretorio'][self.__idioma]}'")
            return None
        conteudo1, conteudo2 = self.capturar_conteudo()
        self.salvar(self.__diretorio_salvar, self.__nome_conteudo, conteudo1, conteudo2)

class _instrucoes_(tk.Tk):
    def __init__(self, _idioma_ = "ing"):
        super().__init__()
        self.title(texto["instrucoes"][_idioma_])
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
    app = Aplicativo()
    app.mainloop()
