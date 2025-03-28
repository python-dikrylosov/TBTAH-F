#-*- coding: utf-8 -*-
#8/03 Были добавлены коды телеграм-бота
#9/03 Добавлена текстовая и голосовая обработка , в итоге получается TEXT т.к. аудио преобразуется в текст, а текст он и есть текст
#10/03 Проработка текстового запроса по всем классификаторам      
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
    
'''
- Zero-shot classification
from transformers import pipeline

classifier = pipeline("zero-shot-classification")
classifier(
"This is a course about the Transformers library",
candidate_labels=["education", "politics", "business"],
)
- Генерация текста
from transformers import pipeline

generator = pipeline("text-generation")
generator("In this course, we will teach you how to")
- Использование произвольной модели из Hub в пайплайне
from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")
generator(
"In this course, we will teach you how to",
max_length=30,
num_return_sequences=2,
)
- Распознавание именованных сущностей (NER)
from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")
- Вопросно-ответные системы
from transformers import pipeline

question_answerer = pipeline("question-answering")
question_answerer(
question="Where do I work?",
context="My name is Sylvain and I work at Hugging Face in Brooklyn",
)
-Автоматическое реферирование (саммаризация)
from transformers import pipeline

summarizer = pipeline("summarization")
summarizer(
"""
America has changed dramatically during recent years. Not only has the number of
graduates in traditional engineering disciplines such as mechanical, civil,
electrical, chemical, and aeronautical engineering declined, but in most of
the premier American universities engineering curricula now concentrate on
and encourage largely the study of engineering science. As a result, there
are declining offerings in engineering subjects dealing with infrastructure,
the environment, and related issues, and greater concentration on high
technology subjects, largely supporting increasingly complex scientific
developments. While the latter is important, it should not be at the expense
of more traditional engineering.

Rapidly developing economies such as China and India, as well as other
industrial countries in Europe and Asia, continue to encourage and advance
the teaching of engineering. Both China and India, respectively, graduate
six and eight times as many traditional engineers as does the United States.
Other industrial countries at minimum maintain their output, while America
suffers an increasingly serious decline in the number of engineering graduates
and a lack of well-educated engineers.
"""
)
- Перевод
from transformers import pipeline

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
translator("Ce cours est produit par Hugging Face.")
- Классификация
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")
'''
    

print('Запуск бота')
bot.infinity_polling(none_stop=True, interval=0)
