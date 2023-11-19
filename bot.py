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
CACHE_SIZE = 6 # Number of images to be stored in the cache at once
BATCH_SIZE = 3 # Number of images to be generated when the cache needs replenishing below a certain threshold
TRIGGER_PROBABILITY = 0.05 #Probability to send an image when triggered

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TARGET_ROLE = os.getenv('TARGET_ROLE')
OUT_OF_IMAGES_MESSAGE = os.getenv('OUT_OF_IMAGES_MESSAGE')
PROMPT_STYLES = os.getenv('PROMPT_STYLES')
PROMPT_SPECIFICS = os.getenv('PROMPT_SPECIFICS')
NEG_PROMPT = os.getenv('NEG_PROMPT')

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
        if r < TRIGGER_PROBABILITY:
            options = [name for name in os.listdir('image_cache/')][1:] # Don't put prompts that start with "." into the objects - this could break
            if not options:
                if OUT_OF_IMAGES_MESSAGE: #if the message is empty, don't reply
                    await message.reply(content=OUT_OF_IMAGES_MESSAGE, mention_author=True)
            else: 
                fn = random.choice(options)
                file = discord.File(f'image_cache/{fn}') 
                await message.reply(file=file, mention_author=True)
                os.remove(f'image_cache/{fn}')
                if len([name for name in os.listdir('image_cache/')][1:]) <= CACHE_SIZE - BATCH_SIZE:
                    global currently_generating
                    if not currently_generating:
                        await replenish_cache(3)

def build_payload():
    '''Constructs a payload to be passed into the SD API. Ensures the cache will not have duplicates of the same object.'''
    style_options = ast.literal_eval(PROMPT_STYLES) #This and the below PROMPT_SPECIFICS are lists
    style = random.choice(style_options)
    object_options = set(ast.literal_eval(PROMPT_SPECIFICS))
    in_use_objects = [f"{file.split('.')[0]}" for file in os.listdir('image_cache/')]
    obj = random.choice(list(object_options.difference(set(in_use_objects))))
    prompt = f"{obj}, {style}"
    return ({
        'prompt': prompt,
        'negative_prompt': NEG_PROMPT,
        'steps': 50,
        'sampler_name': 'DPM++ 2M Karras',
        'hr_scale': 2,
        'hr_upscaler': 'Latent'
    }, obj)

async def replenish_cache(count):
    '''Input: Number of images to generate
       Sends requests to the stable diffusion webui API to generate the requested number of images in the image_cache directory.
       Each file is named based on a randomly chosen object to be placed in the image, generated within 
       '''
    global currently_generating
    if currently_generating:
        return
    currently_generating = True
    print(f"Began generating a batch of {count} images in the cache")
    for i in range(count):
        payload, obj = build_payload()
        func = functools.partial(requests.post, url=f'{URL}/sdapi/v1/txt2img', json=payload)
        diffusion_response = await client.loop.run_in_executor(None, func)
        diffusion_response = diffusion_response.json()
        print(f"Generated '{diffusion_response['parameters']['prompt'].split(', ')[0]}'") #Log the object that was supposed to be generated
        print(f"Prompt: '{diffusion_response['parameters']['prompt']}'") # Print the complete prompt (the object is the first input)
        image = Image.open(io.BytesIO(base64.b64decode(diffusion_response['images'][0])))
        image.save(f'image_cache/{obj}.jpg')
    currently_generating = False
client.run(TOKEN)