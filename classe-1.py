class Registro:
    def __init__(self,data_horario,cidade,clima,temperatura_media,sensacaoM,umidade,nota=''):
        self.data_horario = data_horario
        self.cidade = cidade
        self.clima = clima
        self.temperatura_media = temperatura_media
        self.sensacaoM = sensacaoM
        self.umidade = umidade
        self.nota = nota
    def para_treeview(self):
        return (
            self.cidade,
            self.data_horario,
            self.clima,
            self.temperatura_media,
            self.umidade,
            self.nota
        )