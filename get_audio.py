import subprocess
import streamlink

# URL трансляции Twitch
url = "https://www.twitch.tv/poisonalixir"

# Получаем список доступных потоков со стрима
streams = streamlink.streams(url)
print(streams)
input()
# Выбираем наиболее подходящий по качеству поток
best = streams["audio_only"]

# Получаем ссылку на поток
stream_url = best.url

# Определяем имя файла, в который будем записывать звук
filename = "twitch_audio.mp3"
trimmed_filename = "trimmed_twitch_audio.mp3"

# Команда для записи потока в файл на 30 секунд
cmd_record = ["ffmpeg", "-i", stream_url, "-vn", "-c:a", "libmp3lame", "-q:a", "0", "-t", "30", filename]

# Запускаем процесс записи звука
subprocess.call(cmd_record)

print(f"Запись завершена. Аудиофайл сохранен как: {filename}")

# Команда для обрезки первых 10 секунд
cmd_trim = ["ffmpeg", "-i", filename, "-ss", "12", "-c", "copy", trimmed_filename]

# Запускаем процесс обрезки
subprocess.call(cmd_trim)

print(f"Обрезка завершена. Новый аудиофайл сохранен как: {trimmed_filename}")
