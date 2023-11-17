# Food Poster Bot
A Discord bot that uses Stable Diffusion AI to generate a picture of food whenever a user with a given role types, with a random chance.

## How To Use

1. Install Stable Diffusion Webui found here https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Create a .env file with the following lines:
DISCORD_TOKEN={Your Bot Token} 
DISCORD_GUILD={Your Server Name}
3. (On Windows) run the Stable Diffusion Webui script webui-user.bat after editing it to place '--api' after COMMANDLINE_ARGS. A webpage will open up: you can ignore it
4. In the command line, run `python bot.py`

To change servers, trigger roles, etc, you must edit the .env file, the bot's discord auth token, etc
