import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from repositorio import Repositorio
from deep_translator import GoogleTranslator
from datetime import datetime, timezone, timedelta
from time import sleep
import threading
repo = Repositorio()
cor_fundo = "#117de9"
cor_btn = "#014eb2"
cor_font = "#ffffff"
janela_principal = None
dados = None
tela_carregamento = None
tradutor = GoogleTranslator(source='english', target='portuguese')

# FUNÇÃO VOLTAR PARA JANELA ENTRAR ----------------------
def voltar_op():
    janela_principal.withdraw() # type: ignore
    janela_entrar.deiconify()

# JANELA PRINCIPAL -------------------------------------
def chamar_janela_principal():
    janela_entrar.withdraw()
    global janela_principal
    janela_principal = tk.Toplevel()
    janela_principal.geometry("800x600+300+100")
    janela_principal.title("Principal - Radar do Tempo")
    janela_principal.configure(bg=cor_fundo)
    janela_principal.iconbitmap('imagem/logo_app.ico')
    janela_principal.resizable(0,0) # type: ignore
    
    # INFORMAÇÕES RETIRADAS DA API OPENWEATHER (Repositorio)
    clima_api = dados['weather'][0]['main'] # type: ignore
    cidade_api = dados['name'] #type: ignore
    pais_api = dados['sys']['country'] #type: ignore
    tempMed_api = dados['main']['temp'] # type: ignore
    sensacaoM_api = dados['main']['feels_like'] #type: ignore
    desc_api = dados['weather'][0]['description'] # type: ignore
    tempMin_api = dados['main']['temp_min'] # type: ignore
    tempMax_api = dados['main']['temp_max'] # type: ignore
    umidade_api = dados['main']['humidity'] # type: ignore
    vento_api = dados['wind']['speed'] # type: ignore
    vento_km = vento_api*3.6 # type: ignore
    horario_api = dados['timezone']

    # VALORES QUE APARECEM NA INTERFACE
    data_hora_var = tk.StringVar(janela_principal,value=horario_api)
    cidade_var = tk.StringVar(janela_principal,value=f'{tradutor.translate(cidade_api)}, {pais_api}')
    clima_var = tk.StringVar(janela_principal,value=f'{tradutor.translate(clima_api)}')
    tempMedia_var = tk.StringVar(janela_principal,value=f'{tempMed_api:.1f}°C')
    sensacaoTerm_var = tk.StringVar(janela_principal,value=f'Sensação Térmica: {sensacaoM_api:.1f}°C') # Faz aparece a sensação térmica na interface formatada
    sensTerm_var = tk.StringVar(janela_principal,value=f'{sensacaoM_api:.1f}°C') # Variável para salvar a sensação térmica sem texto, para salvar no registro
    desc_var = tk.StringVar(janela_principal,value=f'{desc_api.title()}')
    tempMin_var = tk.StringVar(janela_principal,value=f'Temp Min: {tempMin_api:.1f}°C')
    tempMax_var = tk.StringVar(janela_principal,value=f'Temp Max: {tempMax_api:.1f}°C')
    umidade_var = tk.StringVar(janela_principal,value=f'Umidade: {umidade_api}%') # Mesmo caso da variável sensacaoTerm_var
    umd_var = tk.StringVar(janela_principal,value=f'{umidade_api}%') # Mesmo caso da variável sensTerm_var
    vento_var = tk.StringVar(janela_principal,value=f'Vento: {vento_km:.1f}km/h')  
    nota_var = tk.StringVar(value="Sem nota")

    # FUNÇÃO ATUALIZAR HORÁRIO ------------------------------
    def atualizar_horario():
        fuso_cidade = timezone(timedelta(seconds=horario_api))
        agora = datetime.now(fuso_cidade)
        hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
        data_hora_var.set(hora_formatada)

        janela_principal.after(1000, atualizar_horario) # type: ignore
    # FUNÇÃO SALVAR REGISTRO --------------------------------
    def salvar_op():
        repo.adicionar(data_hora_var.get(),
                       cidade_var.get(),
                       clima_var.get(),
                       tempMedia_var.get(),
                       sensTerm_var.get(),
                       umd_var.get(),
                       nota_var.get())
        messagebox.showinfo('Aviso', 'Registro salvo com sucesso!')
    # FUNÇÃO ADICIONAR NOTA ---------------------------------
    def adc_nota():
        janela_nota = tk.Toplevel()
        janela_nota.geometry("550x350")
        janela_nota.title("Adicionar nota - Radar do Tempo")
        janela_nota.configure(bg=cor_fundo)
        janela_nota.iconbitmap('imagem/logo_app.ico')
        janela_nota.resizable(0,0) # type: ignore
        # FUNÇÃO CRIAR NOTA
        def confirmar():
            nota = entrada_nota.get("1.0", "end")

            if nota.strip() == "":
                messagebox.showwarning("Aviso", "Digite uma nota!")
                return

            nota_var.set(nota)  # salva a nota
            messagebox.showinfo("Sucesso", "Nota adicionada!")

            janela_nota.destroy()

        # LABELS NOTA
        tk.Label(janela_nota, text="Nota",
                font=("Arial", 30, 'bold'),
                fg='white', bg="#173fa8").place(relx=0.5, y=47, width=180, height=52, anchor='center')

        tk.Label(janela_nota, text="Escreva a nota para a cidade desejada",
                font=("Arial", 16, "bold"),
                fg=cor_font, bg=cor_fundo).place(x=88, y=100)
        
        # ENTRADA NOTA
        entrada_nota = tk.Text(janela_nota, font=("Arial", 14), wrap="word")
        entrada_nota.place(x=110, y=150, width=330, height=100)

        # BUTTON NOTA
        tk.Button(janela_nota, text="Confirmar",
                font=("Arial", 10, "bold"),
                fg=cor_font,
                command=confirmar,
                bg="#0a8f3c").place(x=170, y=280, width=200, height=35)
        
    # Hora
    data_hora = tk.Label(janela_principal,
             font=("Arial", 20, "bold"),
             textvariable=data_hora_var,
             fg="white", bg=cor_fundo)
    data_hora.place(relx=0.5, y=28, anchor='center')
    atualizar_horario()
    # Cidade
    tk.Label(janela_principal,
             font=("Arial", 28, "bold"),
             textvariable=cidade_var,
             fg="white", bg=cor_fundo).place(relx=0.5, y=75, anchor="center")
    # Clima
    tk.Label(janela_principal,
             font=("Arial", 18),
             textvariable=clima_var,
             fg="white", bg=cor_fundo).place(relx=0.5, y=115, anchor='center')
    # Temperatura Média
    tk.Label(janela_principal,
             font=("Arial", 70, "bold"),
             textvariable=tempMedia_var,
             fg="white", bg=cor_fundo).place(relx=0.5, y=190, anchor="center")
    # Sensação Térmica
    tk.Label(janela_principal,
             font=("Arial", 16, "bold"),
             textvariable=sensacaoTerm_var,
             fg="white", bg=cor_fundo).place(relx=0.5, y=322, anchor='center')
    # Descrição
    tk.Label(janela_principal,
             font=("Arial", 20, "bold"),
             textvariable=desc_var,
             fg="white", bg=cor_fundo).place(relx=0.5, y=285, anchor='center')
    # Temperatura min 
    tk.Label(janela_principal,
             font=("Arial", 16, "bold"),
             textvariable=tempMin_var,
             fg=cor_font, bg="#173fa8").place(x=122, y=368, width=250, height=32)
    # Temperatura max
    tk.Label(janela_principal,
             font=("Arial", 16, "bold"),
             textvariable=tempMax_var,
             fg=cor_font, bg="#173fa8").place(x=412, y=368, width=250, height=32)
    # Umidade
    tk.Label(janela_principal, 
             font=("Arial", 18, "bold"),
             textvariable=umidade_var,
             fg="white", bg="#173fa8",
             width=18, height=2).place(x=110, y=420)
    # Vento
    tk.Label(janela_principal,
             font=("Arial", 18, "bold"),
             textvariable=vento_var,
             fg="white", bg="#173fa8",
             width=18, height=2).place(x=400, y=420)
    
    # BUTTONS PRINCIPAL
    tk.Button(janela_principal,
              text="Salvar Registro",
              font=("Arial", 10, "bold"),
              fg="white",
              command=salvar_op,
              bg="#0a8f3c").place(x=300, y=510, width=200, height=35)

    tk.Button(janela_principal,
              text="Voltar",
              font=("Arial", 10, "bold"),
              fg="white",
              command=voltar_op,
              bg=cor_btn).place(x=300, y=555, width=200, height=35)
    
    tk.Button(janela_principal,
              text="Sair",
              font=("Arial", 10, "bold"),
              fg="white",
              command=quit,
              bg='dark red').place(x=100, y=555, width=140, height=35)
    
    tk.Button(janela_principal,
              text="Ver Registros",
              font=("Arial", 10, "bold"),
              fg="white",
              command=abrir_registros,
              bg=cor_btn).place(x=565, y=555, width=140, height=35)
    
    tk.Button(janela_principal,
              text="Adicionar nota",
              font=("Arial", 10, "bold"),
              fg="white",
              command=adc_nota,
              bg=cor_btn).place(x=565, y=505, width=140, height=35)

# VERIFICAÇÃO API ----------------------------------
def coletar_cidade():
    global tela_carregamento
    city_escolhida = cidade_escolhida.get().strip()
    if city_escolhida is None:
        messagebox.showerror("Erro", "Digite o nome de uma cidade!")
        return
    # TELA DE CARREGAMENTO -------------------------
    tela_carregamento = tk.Toplevel(janela_entrar)
    tela_carregamento.geometry("340x115+700+600")
    tela_carregamento.title("")
    tela_carregamento.configure(bg=cor_fundo)
    tela_carregamento.resizable(0,0)
    tela_carregamento.configure()
    tela_carregamento.overrideredirect(True)  # Remove a barra de título

    # LABEL E BARRA DE PROGRESSO ------------------
    tk.Label(tela_carregamento,
             text="Buscando cidade...",
             font=("Arial", 13, "bold"),
             fg="white", bg=cor_fundo).place(relx=0.5, rely=0.26, anchor="center")
    tk.Label(tela_carregamento, text="Caso demore, pressione Enter novamente",
             font=("Arial", 12, 'bold'),
             bg=cor_fundo,
             fg='white').place(relx=0.5, rely=0.82, anchor="center")
    barra = ttk.Progressbar(tela_carregamento, mode='indeterminate', length=180)
    barra.place(relx=0.5, rely=0.56, anchor="center")
    barra.start(10)
    tela_carregamento.update()
    def buscar_dados():
        global dados
        dados = repo.coletar_dados(city_escolhida)
        tela_carregamento.after(0, lambda: finalizar(tela_carregamento))
    def finalizar(tela_carregamento):
        if dados is None:
            barra.stop()
            tela_carregamento.destroy()
            messagebox.showerror("Erro", "Cidade não encontrada!")
        else:
            sleep(1)
            chamar_janela_principal()
            barra.stop()
            tela_carregamento.destroy()
    threading.Thread(target=buscar_dados, daemon=True).start()
            
# JANELA ENTRAR ----------------------------------
janela_entrar = tk.Tk()
janela_entrar.geometry("350x280+300+200")
janela_entrar.title("Entrar - Radar do Tempo")
janela_entrar.configure(bg=cor_fundo)
janela_entrar.iconbitmap('imagem/logo_app.ico')
janela_entrar.resizable(0,0) # type: ignore

img_entrar = PhotoImage(file='imagem/logo_app.png') # Logo usada na janela entrar

# LABELS ENTRAR
tk.Label(janela_entrar, text="Bem-Vindo(a) ao\nRadar do Tempo",
         font=("Arial", 14, "bold"),
         fg=cor_font, bg=cor_fundo).place(x=95, y=30)

tk.Label(janela_entrar, text="Escolha uma cidade\npara ver o clima:",
         font=("Arial", 13, "bold"),
         fg=cor_font, bg=cor_fundo).place(x=92, y=115)

#LOGO ENTRAR
tk.Label(janela_entrar,
         image=img_entrar,
         bg=cor_fundo).place(x=25, y=20)

#ENTRY ENTRAR
cidade_escolhida = tk.Entry(janela_entrar,
                            font=('Arial', 12),
                            relief='solid'
                            )
cidade_escolhida.place(x=80, y=176, width=185, height=28)
cidade_escolhida.bind("<Return>", lambda event: coletar_cidade())

# BUTTON ENTRAR
tk.Button(janela_entrar, text="Entrar",
          font=("Arial", 10, "bold"),
          fg="white", bg=cor_btn,
          command=coletar_cidade).place(x=122, y=215, width=100, height=30)

# FUNÇÂO EDITAR NOTA -----------------------------
def editar_nota(tree):
    item_selecionado = tree.selection()

    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro!")
        return

    item = tree.item(item_selecionado)
    valores = list(item["values"])

    # índice da nota (última coluna)
    nota_atual = valores[6]
    # JANELA EDITAR ------------------------------
    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Nota")
    janela_editar.geometry("400x300")
    janela_editar.iconbitmap('imagem/logo_app.ico')
    janela_editar.resizable(0,0) # type: ignore

    entrada = tk.Text(janela_editar, font="Arial 16", wrap="word")
    entrada.insert("1.0", nota_atual)
    entrada.pack(expand=True, fill="both", padx=10, pady=10)
    # FUNÇÃO SALVAR EDIÇÃO -----------------------
    def salvar_edicao():
        nova_nota = entrada.get("1.0", "end").strip()

        if nova_nota == "":
            messagebox.showwarning("Aviso", "Nota vazia!")
            return

        # atualiza na lista
        valores[6] = nova_nota
        tree.item(item_selecionado, values=valores)
        repo.editar(valores[0], valores[1], nova_nota)

        messagebox.showinfo("Sucesso", "Nota atualizada!")
        janela_editar.destroy()
    # BUTTON EDITAR
    tk.Button(janela_editar,
              text="Salvar",
              font="Arial 12",
              command=salvar_edicao,
              fg="white",
              bg="#0a8f3c").place(x=100, y=250, width=200, height=35)
    
# FUNÇÃO EXCLUIR NOTA --------------------------
def excluir_nota(tree):
    item_selecionado = tree.selection()

    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro!")
        return

    item = tree.item(item_selecionado)
    valores = list(item["values"])

    # índice da nota (última coluna)
    valores[6] = "Sem nota"

    tree.item(item_selecionado, values=valores)
    repo.editar(valores[0], valores[1], "Sem nota")

    messagebox.showinfo("Sucesso", "A nota foi excluída!")

# JANELA DOS REGISTROS --------------------------
def abrir_registros():
    janela_registros = tk.Toplevel()
    janela_registros.title("Registros Salvos")
    janela_registros.geometry("1000x410")
    janela_registros.resizable(0,0)
    janela_registros.maxsize(width=1500, height=410)
    janela_registros.iconbitmap('imagem/logo_app.ico')

    colunas = ("Data/Horário","Cidade","Clima","Temperatura Média","Sensação Term.","Umidade","Nota") # Tupla com o nome das colunas
    
    frame_registros = tk.Frame(janela_registros)
    frame_registros.pack(fill="both", expand=True, pady=(0, 50))

    scrollbar_y = tk.Scrollbar(frame_registros, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    tree = ttk.Treeview(frame_registros, columns=colunas, show="headings",
                        displaycolumns=colunas,
                        yscrollcommand=scrollbar_y.set)

    scrollbar_y.config(command=tree.yview)
   
    for col in colunas: # Cria as colunas de forma simples e padronizada
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=125)

    tree.pack(fill="both", expand=True)

    # Inserindo dados
    for registro in repo.listar():
        tree.insert("", "end", values=(
            registro.data_horario,
            registro.cidade,
            registro.clima,
            registro.temperatura_media,
            registro.sensacaoM,
            registro.umidade,
            registro.nota
        ))
    # BUTTONS
    tk.Button(janela_registros,
          text="Editar Nota",
          command=lambda: editar_nota(tree),
          fg='white',
          bg=cor_btn).place(x=250, y=368, width=200, height=35)
    
    tk.Button(janela_registros,
          text="Excluir Nota",
          command=lambda: excluir_nota(tree),
          compound="left",
          fg='white',
          bg='dark red').place(x=500, y=368, width=200, height=35)
try:    
    janela_entrar.mainloop()
except KeyboardInterrupt:
    if tela_carregamento and tela_carregamento.winfo_exists():
        tela_carregamento.destroy()
