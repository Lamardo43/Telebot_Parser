import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

URL = "ЗАПИСАТЬ ЗДЕСЬ URL САЙТА"
API_TOKEN = "ЗАПИСАТЬ ЗДЕСЬ API ТОКЕН БОТА, ПОЛКЧЕННЫЙ С ПОМОЩЬЮ BOT FATHER"

headers = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

previous_status = 0
counter = 0
status = 0

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

begin = 0
end = 0


@dp.message_handler()
async def get_start(message: types.Message):
    async def write_to_file(messages):
        global previous_status
        global status
        global counter
        global begin
        global end
        min = 0
        sec = 0

        if status != previous_status:
            if status == 1:
                begin = time.time()
                await message.answer(messages)
            elif status == 0:
                end = time.time()
                time_online = int((end - begin) - 5 * 60)
                min = time_online // 60
                sec = time_online % 60
                await message.answer(f"{messages} now: {min}m {sec}s")

            with open("log.txt", "a", encoding="utf-8") as file:
                file.write(f"#{counter}\t - [{str(datetime.now())[0:19]}]\t-   {messages} now: {min}m {sec}s \n")

            previous_status = status

    async def get_data(url):
        global status
        global headers
        global counter

        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        # with open("site_code.html", "w", encoding="utf-8") as file:
        #     file.write(src)

        try:
            span = soup.find("span", class_="profile-user__last-visit text-muted small").text
            print(f"-------------------#{counter}\t - [{str(datetime.now())[0:19]}]\t-   {span}")
            counter += 1
            status = 0
            await write_to_file("Off")
        except AttributeError:
            print(f"-------------------#{counter}\t - [{str(datetime.now())[0:19]}]\t-   Online")
            counter += 1
            status = 1
            await write_to_file("On")

    async def startParse(name):
        while True:
            try:
                await get_data(name)
            except():
                await get_data(name)
            time.sleep(10)

    await startParse("")


if __name__ == '__main__':
    executor.start_polling(dp, timeout=1000000000)
