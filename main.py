import json
from telethon import TelegramClient, events
from pytesseract import image_to_string
from PIL import Image
import requests
from decouple import config

api_id = config('API_ID')
api_hash = config('API_HASH')

client = TelegramClient('anon', api_id, api_hash)

headers = {
    'Content-Type': 'application/json'
}


async def read_image():
    print('reading image')
    return image_to_string(Image.open('images/image.png'))


async def send_text(text):
    data = dict(
        text=text,
        img=False
    )

    data = json.dumps(data)

    requests.post('http://localhost:5000/binance', headers=headers, data=data)


@client.on(events.NewMessage(chats='testalv'))
async def my_event_handler(msg):
    # If the message has a media, it downloads it
    if msg.media is not None:
        await client.download_media(msg.media, 'images/image.png')
        print('Image saved')
        text = await read_image()
    else:
        text = msg.message.message

    await send_text(text)


client.start()
client.run_until_disconnected()
