#-*- coding: utf-8 -*-
#8/03 Были добавлены коды телеграм-бота
#9/03 Добавлена текстовая и голосовая обработка , в итоге получается TEXT т.к. аудио преобразуется в текст, а текст он и есть текст


import telebot
import librosa
import keygen
import soundfile as sf
from gtts import gTTS
import speech_recognition as sr
bot = telebot.TeleBot(keygen.telegram_TOKEN)
@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    # Получаем информацию о голосовом сообщении
    voice = message.voice
    print(voice)
    file_id = voice.file_id
    print(file_id)
    duration = voice.duration
    print(duration)
    # Загружаем аудиофайл
    file_info = bot.get_file(file_id)
    print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    print(downloaded_file)
    # Сохраняем аудиофайл на диск
    with open("voice_message.ogg", 'wb') as f:
        f.write(downloaded_file)
    # загрузка аудиофайла
    audio_data, sample_rate = librosa.load("voice_message.ogg")
    # конвертация в одноканальный формат
    mono_audio_data = librosa.to_mono(audio_data)
    # применение обработки сигналов для удаления фонового шума (при необходимости)
    # сохранение очищенного аудиофайла на диск
    sf.write("mono_voice_message.wav", mono_audio_data, sample_rate)
    sf.write(file_id + "mono_voice_message.wav", mono_audio_data, sample_rate)
    # Теперь ваша модель обучена на голосовом файле и может классифицировать новые голосовые сегменты по их классам
    
    # Отправляем сообщение с ответом
    bot.reply_to(message, "Голосовое сообщение получено и обработано")
    
    # Создание экземпляра распознавателя
    recognizer = sr.Recognizer()
    # Открытие аудиофайла
    audio_file = sr.AudioFile("mono_voice_message.wav")
    # Чтение аудиофайла
    with audio_file as source:
        audio = recognizer.record(source)
    # Распознавание речи
    text = recognizer.recognize_google(audio, language="ru-RU")
    print(text)
    print("Распознанный текст: ", text)
    
    bot.send_massage(message.chat.id,text)

@bot.message_handler(content_types=["text"])
def handle_voice(message):
    
    bot.send_massage(message.chat.id,message.text)
    

print('Запуск бота')
bot.infinity_polling(none_stop=True, interval=0)
