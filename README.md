# Food Poster Bot
A Discord bot that uses Stable Diffusion AI to generate a picture of food whenever a user with a given role types, with a random chance.

## How To Use

1. Install Stable Diffusion Webui found here https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Create a .env file with the following lines:
DISCORD_TOKEN={Your Bot Token} 
DISCORD_GUILD={Your Server Name}
3. (On Windows) edit the script webui-user.bat to place '--api --nowebui' after COMMANDLINE_ARGS. Save it in the same folder as webui-user-api-noui.bat.  
4. (On Windows) run the Stable Diffusion Webui script webui-user-api-noui.bat. Make sure the file structure is correct (the easiest way is to place this repo and the Stable Diffusion Webui repo in the same folder). 

To change servers, trigger roles, etc, you must edit the .env file, the bot's discord auth token, etc
