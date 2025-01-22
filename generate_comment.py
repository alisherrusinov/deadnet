from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Сгенерируй 5 комментариев к стриму по игре кс го, сделай так чтобы они были более человечными. Вот что сказал стример: может ещё задержка Не сработает 6 Эксклюзив для стрима мяу-мяу мяу-мяу я мяу-мяу"}],
    web_search = False
)
print(response.choices[0].message.content)