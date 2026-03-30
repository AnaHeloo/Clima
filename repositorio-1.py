from classe import Registro
import requests
from tkinter import messagebox

API_KEY = '706060739e7265e2bbf5092a4198c23b'

class Repositorio: 
    def __init__(self):
        self.lista = []
        
    def adicionar(self,data_horario,cidade,clima,temperatura_media,sensacao_t,umidade,nota):
        registros = Registro(data_horario,cidade,clima,temperatura_media,sensacao_t,umidade,nota)
        self.lista.append(registros)

    def buscar(self,id):
        for registro in self.lista:
            if registro.id == id:
                return registro

    def listar(self):
        return self.lista

    def editar(self, data_horario, cidade, nova_nota):
        for registro in self.lista:
            if registro.data_horario == data_horario and registro.cidade == cidade:
                registro.nota = nova_nota
                break

    def deletar(self,id):
        registro = self.buscar(id)
        self.lista.remove(registro)
    
    def coletar_dados(self, cidade):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br'
        # Adicionei &units=metric para receber a temperatura em Celsius
        resposta = requests.get(url, timeout=10)  # timeout de 10 segundos
        dados = resposta.json()
        if dados['cod'] != 200:
            return None
        else:
            return dados


repo = Repositorio()