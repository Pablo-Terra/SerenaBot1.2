#Módulo: Telebot1.2.py
#Autor: Pablo Terra G. Vieira
#Descrição: Robô que aceita pagamentos e envia infoconteudo.



#BIBLIOTECAS DO SCRIPT
import telebot, csv
from decouple import config
from telebot.types import LabeledPrice
from datetime import datetime
#Biblioteca dos Botões
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#Token em um arquivo .ENV separado por questão de segurança
token = config('TOKEN_BOT')


bot = telebot.TeleBot(token)
#Token do gateway
token_provider = config('TOKEN_PROVIDER')

#Possíveis respostas ao usuário que o Rôbo está programado para entregar 
respostas = {'oi': 'Oi, em que posso ajudar ?\n Digite /start para iniciar', 'ola': 'Ola, em que posso ajudar ?\n Digite /start para iniciar'}
#Preço defeinido para o infoproduto
precos = [
    LabeledPrice(label='Segredos do bot', amount=500)
]

def salvar(arquivo_destino, dados: list):
    with open(arquivo_destino, 'a') as ids:
        e = csv.writer(ids)
        e.writerow(dados)
#Comando de inicio
@bot.message_handler(commands=['start', 'inicio'])
def start(message):
    salvar('ids_telegram.csv', [message.from_user.id])
    bot.send_message(message.chat.id, 'Olá, tudo bom ?\nEstou disponibilizando o meu material em PDF OU MP3\nClick e selecione o formato desejado.')
    # botoes
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("PDF", callback_data="opcao1")
    button2 = InlineKeyboardButton("MP3", callback_data="opcao2")
    keyboard.row(button1, button2)
    bot.send_message(message.chat.id, "Escolha uma opção:", reply_markup=keyboard)
#Botões
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "opcao1":
        bot.send_message(call.message.chat.id, '/comprarpdf')
    elif call.data == "opcao2":
        bot.send_message(call.message.chat.id, '/comprarmp3')

#PDF
@bot.message_handler(commands=['comprarpdf'])
def comprar(message):
    bot.send_invoice(
        message.from_user.id,
        title='Robo pdf',
        description='Conteúdo detalhado de como possuir um robô totalmente automatizado no formato PDF',
        provider_token=token_provider,
        currency='BRL',
        photo_url=config('IMG_PRODUTO'),
        photo_height=512,
        photo_size=512,
        photo_width=512,
        is_flexible=False,
        prices=precos,
        start_parameter='serena-robot',
        invoice_payload='PDF'
    )
#MP3
@bot.message_handler(commands=['comprarmp3'])
def comprar(message):
    bot.send_invoice(
        message.from_user.id,
        title='Robo mp3',
        description='Escute o manual detalhado de como possuir um robô totalmente automatizado no formato MP3',
        provider_token=token_provider,
        currency='BRL',
        photo_url=config('IMG_PRODUTO'),
        photo_height=512,
        photo_size=512,
        photo_width=512,
        is_flexible=False,
        prices=precos,
        start_parameter='serena-robot',
        invoice_payload='MP3'
    )
#Mensagem em caso de falha na compra
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message="Houve uma falha na compra, tente mais tarde por gentileza.")

#PDF ENVIO
@bot.message_handler(content_types=['successful_payment']) 
def pagou(message): #Envio caso de pdf
    if message.successful_payment.invoice_payload == 'PDF':
        salvar('ids_telegram_compra_ok.csv', [message.from_user.id, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
        doc = open('C:\\Users\\Terra\\Documents\\codigo\\tcc\\bot1.2\\teste.pdf', 'rb')
        bot.send_document(message.chat.id, doc)
        bot.send_message(message.from_user.id, 'Muito obrigado pela confiança e preferencia, segue o pdf para download')
    elif message.successful_payment.invoice_payload == 'MP3': #Envio caso de mp3
        audio = open('C:\\Users\\Terra\\Documents\\codigo\\tcc\\bot1.2\\audio.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        bot.send_message(message.from_user.id, 'Muito obrigado pela confiança e preferência, segue o áudio em formato MP3 para download')

#Função que testa se robô envia pdfs
@bot.message_handler(commands=['download'])
def download(message):
    doc = open('teste.pdf', 'rb')
    bot.send_document(message.chat.id, doc)
#Função de registro de conversas com o bot - apenas o que é digitado no chat
@bot.message_handler(func=lambda m: True)
def tudo(message):
    print("Mensagem: ", message.text)
    salvar('historico_chat_telegram_.csv', [message.from_user.id, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    resp = respostas.get(str(message.text).lower(), 'Não entendi o que quiz dizer, tente novamete')
    bot.send_message(message.from_user.id, resp)

# botões

bot.skip_pending = True
bot.polling(none_stop=True, interval=0)

