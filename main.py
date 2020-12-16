import requests
import time
import json
import os
import requests
from requests_html import HTMLSession

body = json.loads('''{
    "filters": {
        "pais": null,
        "tipoEsporte": 1,
        "torneio": null
    },
    "include": [
        "weekdays",
        "sportfilters",
        "cabecalho"
    ],
    "limit": 500,
    "offset": 0,
    "sort": [
        "date-asc"
    ],
    "type": "aovivo"
    }'''
)

baseUrl = 'https://www.betsul.com/web/v2/eventos'
allEvents = requests.post(url=baseUrl, json=body)

print(allEvents.json())

while True:
    token = '1401583441:AAEPwUV3RzQMAtGBsu_0gkju09Nl04YxKkk'
    # Ler mensagens
    url_base = f'https://api.telegram.org/bot{token}/getUpdates'
    # Imprimir Resultados
    time.sleep(10)

class TelegramBot:
    def __init__(self):
        token = '1374813849:AAHauYQ2ikM4E-fTYOsZDNFZ-uOf39TecEM'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(
                        mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Criar uma resposta
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        if eh_primeira_mensagem == True or mensagem in ('menu', 'Menu'):
            return f'''Olá bem vindo a nossa lanchonete Digite o número do hamburguer gostaria de pedir:{os.linesep}1 - Queijo MAX{os.linesep}2 - Duplo Burguer Bacon{os.linesep}3 - Triple XXX'''
        if mensagem == '1':
            return f'''Queijo MAX - R$20,00{os.linesep}Confirmar pedido?(s/n)
            '''
        elif mensagem == '2':
            return f'''Duplo Burguer Bacon - R$25,00{os.linesep}Confirmar pedido?(s/n)
            '''
        elif mensagem == '3':
            return f'''Triple XXX - R$30,00{os.linesep}Confirmar pedido?(s/n)'''

        elif mensagem.lower() in ('s', 'sim'):
            return ''' Pedido Confirmado! '''
        elif mensagem.lower() in ('n', 'não'):
            return ''' Pedido Confirmado! '''
        else:
            return 'Gostaria de acessar o menu? Digite "menu"'

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)


bot = TelegramBot()
bot.Iniciar()