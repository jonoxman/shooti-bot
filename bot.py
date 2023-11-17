import os
import json
import requests
import io
import base64
from PIL import Image
import random
import discord
from dotenv import load_dotenv

url = "http://127.0.0.1:7860"
foods = ['Sushi', 'Ramen', 'Kebab', 'Pho', 'Pie', 'Pad Thai', 'Lasagna', 'Kimchi', 'Fried Chicken', 'Pizza', 'Burger', 'Donuts', 'Poutine', 'Burrito', 'Mac and Cheese', 'Wonton Soup', 'Chocolate Cake', 'Barbecued Ribs', 'Sashimi', 'Croissant', 'Tacos']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members=True
intents.message_content=True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
@client.event
async def on_message(message):
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.author == client.user:
        return

    role = discord.utils.find(lambda r: r.name == 'Above Faust NPC', guild.roles)
    
    if role in message.author.roles:
        r = random.random()
        if r < 0.05:
            food = random.choice(foods)
            payload = {
                "prompt": f'RAW photo, {food}, <lora:foodphoto:1> foodphoto, dslr, soft lighting, high quality, film grain, Fujifilm XT',
                "steps": 20,
                "sampler_name": 'DPM++ 2M Karras'
            }
            diffusion_response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
            diffusion_response = diffusion_response.json()
            print(diffusion_response)
            image = Image.open(io.BytesIO(base64.b64decode(diffusion_response['images'][0])))
            image.save('nux.jpg')
            file = discord.File("nux.jpg")
            await message.reply(file=file, mention_author=True)

client.run(TOKEN)