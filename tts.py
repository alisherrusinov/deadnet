import speech_recognition as sr


from pydub import AudioSegment

# Конвертация MP3 в WAV
audio = AudioSegment.from_mp3("trimmed_twitch_audio.mp3")
audio.export("converted_audio.wav", format="wav")

# Создаем экземпляр распознавателя
recognizer = sr.Recognizer()

# Укажите путь к вашему аудиофайлу
audio_file_path = "converted_audio.wav"  # Замените на путь к вашему файлу

# Открываем аудиофайл
with sr.AudioFile(audio_file_path) as source:
    # Считываем аудио
    audio = recognizer.record(source)  # или используйте recognize() для чтения по частям

    try:
        # Используем Google Web Speech API для распознавания речи
        text = recognizer.recognize_google(audio, language='ru-RU')
        print("Распознанный текст: " + text)
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print(f"Ошибка запроса к сервису распознавания речи; {e}")
