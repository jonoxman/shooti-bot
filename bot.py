import os
import requests
import io
import base64
from PIL import Image
import random
import discord
import functools
from dotenv import load_dotenv
import ast

#Constants
URL = "http://127.0.0.1:7860"
FOODS = set(['Sushi Rolls', 'Bowl of Ramen', 'Shish Kabob', 'Bowl of Pho', 'Pie', 'Pad Thai', 'Lasagna', 
             'Kimchi', 'Fried Chicken Drumsticks', 'Pepperoni Pizza', 'Burger with Fries', 'Donuts', 'Poutine', 
             'Burrito', 'Mac and Cheese', 'Wonton Soup', 'Chocolate Cake', 'Barbecued Ribs',
               'Sashimi', 'Croissant', 'Tacos', 'Grilled Steak'])
CACHE_SIZE = 7 # Number of images to be stored in the cache at once
BATCH_SIZE = 3 # Number of images to be generated when the cache needs replenishing below a certain threshold

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TARGET_ROLE = os.getenv('TARGET_ROLE')
OUT_OF_IMAGES_MESSAGE = os.getenv('OUT_OF_IMAGES_MESSAGE')
PROMPT_STYLES = os.getenv('PROMPT_STYLES')
PROMPT_SPECIFICS = os.getenv('PROMPT_SPECIFICS')

intents = discord.Intents.default()
intents.members=True
intents.message_content=True

client = discord.Client(intents=intents)

# A global variable to track whether the cache is already being replenished 
currently_generating = False

@client.event
async def on_ready():
    '''On-startup trigger'''
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
@client.event
async def on_message(message):
    '''On-message trigger'''
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.author == client.user:
        return
    role = discord.utils.find(lambda r: r.name == TARGET_ROLE, guild.roles)
    if role in message.author.roles:
        print(f"Targeted role '{role.name}' posted!")
        r = random.random()
        if r < 1:
            options = [name for name in os.listdir('image_cache/')]
            if not options:
                if OUT_OF_IMAGES_MESSAGE: #if the message is empty, don't reply
                    await message.reply(content=OUT_OF_IMAGES_MESSAGE, mention_author=True)
            else: 
                fn = random.choice(options)
                file = discord.File(f'image_cache/{fn}') 
                await message.reply(file=file, mention_author=True)
                os.remove(f'image_cache/{fn}')
                if len([name for name in os.listdir('image_cache/')]) <= CACHE_SIZE - BATCH_SIZE:
                    global currently_generating
                    if not currently_generating:
                        await replenish_cache(3)

def build_payload():
    '''Constructs a payload to be passed into the SD API'''
    object_options = ast.literal_eval
    return {

    }

async def replenish_cache(count):
    '''Input: Number of images to generate
       Sends requests to the stable diffusion webui API to generate the requested number of images in the image_cache directory
       The type of food is chosen at random from the foods constant. 
       '''
    print(f"Began generating a batch of {count} images in the cache")
    global currently_generating
    if currently_generating:
        return
    currently_generating = True
    for i in range(count):
        in_use_foods = [f"{file.split('.')[0]}" for file in os.listdir('image_cache/')]
        food = random.choice(list(FOODS.difference(set(in_use_foods))))
        payload = {
            "prompt": f'RAW photo, {food}, <lora:foodphoto:0.7> foodphoto, dslr, soft lighting, high quality, film grain, Fujifilm XT',
            "negative_prompt": 'worms, disgusting, grotesque, slimy',
            "steps": 50,
            "sampler_name": 'DPM++ 2M Karras',
            "hr_scale": 2,
            "hr_upscaler": 'Latent'
        }
        func = functools.partial(requests.post, url=f'{URL}/sdapi/v1/txt2img', json=payload)
        diffusion_response = await client.loop.run_in_executor(None, func)
        diffusion_response = diffusion_response.json()
        print(f"Generated {diffusion_response['parameters']['prompt'].split(', ')[1]}")
        image = Image.open(io.BytesIO(base64.b64decode(diffusion_response['images'][0])))
        image.save(f'image_cache/{food}.jpg')
    currently_generating = False
client.run(TOKEN)