import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from pytube import YouTube
from config import TOKEN
import unicodedata

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_message(message:types.message):
    chatId = message.chat.id
    await bot.send_message(chatId, "Привет, здесь ты можешь скачать видео из YouTube.\n"
                           "Пришли мне ссылку на видео и его скачаю.\n"
                           "/help - помощь.")
    
@dp.message_handler(commands=['help'])
async def start_message(message:types.message):
    chatId = message.chat.id
    await bot.send_message(chatId, "|Команды:|\n"
                           "/start - начало работы\n"
                           "/help - помощь\n"
                           "/info - информация об обновлениях\n"
                           "/audio - скачать аудио из видео\n"
                           "|Применение:|\n"
                           "Для того чтобы бот скачал видео\n"
                           "нужно прислать ему ссылку на это видео\n"
                           "по которой он и скачает это видео.")
    
@dp.message_handler(commands=['info'])
async def info_message(message:types.message):
    chatId = message.chat.id
    await bot.send_message(chatId, "За последнее время\n"
                           "обновлений нет.")
    
@dp.message_handler()
async def info_message(message:types.Message):
    chatId = message.chat.id
    url = message.text
    yt = YouTube(url)
    if message.text.startswith("https://youtu.be/") or message.text.startswith("https://www.youtube.com/"): 
        await bot.send_message(chatId, f"Запускаю загрузку видео: *{yt.title}*\nКанал: *{yt.author}* -> *{yt.channel_url}*", parse_mode="Markdown") 
        await download_youtube_video(url, message, bot)

async def download_youtube_video(url, message, bot): 
    yt = YouTube(url) 
    stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution() 
    stream.download(f'{message.chat.id}', f'{message.chat.id}+{yt.title}') 
    with open(f'{message.chat.id}/{message.chat.id}+{yt.title}', 'rb') as video: 
        await bot.send_video(message.chat.id, video, caption="*Готово!*", parse_mode="Markdown")
    os.remove(f'{message.chat.id}/{message.chat.id}+{yt.title}')
    


if __name__ == '__main__':
    executor.start_polling(dp)
