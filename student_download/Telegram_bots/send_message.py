#!/usr/bin/python3
from sys import argv, exit, stderr
import os

# based on the useful_instructions_4Telegram:
https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/

# private info needed:
# > /thebotfather:
# Done! Congratulations on your new bot. You will find it at telegram.me/your17bot.
# your17bot
# @your17bot
# Use this token to access the HTTP API:
#    HTTP API='275288481:AAFJM2NWksYKupliFEnJ5QbChv5LatRWP_E'
TOKEN='275288481:AAFJM2NWksYKupliFEnJ5QbChv5LatRWP_E'
phone = '+(39)(351)(8684000)'
# The below information has been obtained from:
# https://my.telegram.org/auth
api_id = 'API_id'
api_hash = 'API_hash'


https://api.telegram.org/bot<yourtoken>/getUpdates
https://api.telegram.org/275288481:AAFJM2NWksYKupliFEnJ5QbChv5LatRWP_E/getUpdates
{"ok":false,"error_code":404,"description":"Not Found"}

# where it was exaplained what is the international phone number format.
# Please make sure you are entering your mobile phone number in the international format.
# I.e.: +(country code)(city or carrier code)(your number)



# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
 
token = f'275288481:{TOKEN}'
message = "Hey mama guarda quanto mi diverto. It works!"
 
  
# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)
  
# connecting and building the session
client.connect()
 
# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
  
    client.send_code_request(phone)
     
    # signing in the client
    client.sign_in(phone, input('Enter the code: '))
  
  
try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
    receiver = InputPeerUser('user_id', 'user_hash')
 
    # sending message using telegram client
    client.send_message(receiver, message, parse_mode='html')
except Exception as e:
     
    # there may be many error coming in while like peer
    # error, wwrong access_hash, flood_error, etc
    print(e);
 
# disconnecting the telegram session
client.disconnect()
