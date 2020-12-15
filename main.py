from src.bet365Api import Bet365Api
from src.telegramBot import TelegramBot

bot = TelegramBot()
# bot.iniciar()
api = Bet365Api()

while True:
    api.dev()
