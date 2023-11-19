# Food Poster Bot
A Discord bot that uses Stable Diffusion AI to generate an image of some random option in some particular style and reply with it whenever a user with a given role types, with a random chance. Images are cached to allow for instant replies - the cache size can be customized based on demand (default is 7).

## How To Use

1. Install Stable Diffusion Webui found here https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Create a .env file with the following lines:
DISCORD_TOKEN={Your Bot Token} 
DISCORD_GUILD={Your Server Name}
TARGET_ROLE={Your Trigger Role}
OUT_OF_IMAGES_MESSAGE={Message To Display When Cache Is Empty.}
PROMPT_STYLE={Prompt Baseline}
PROMPT_SPECIFICS={Specific Objects For Prompt}

### Notes on .env file
- Leave OUT_OF_IMAGES_MESSAGE blank (still include the key) if you want the bot to do nothing when the cache is empty.
- PROMPT_STYLE and PROMPT_SPECIFICS must be given in list format ['A', 'B', 'C']. (If you only want one option, put it in as a single-element list ['A'].) If lists have multiple elements, one will be chosen randomly for each generated image. 

3. (On Windows) edit the script webui-user.bat to place '--api --nowebui --port 7860' after COMMANDLINE_ARGS. If you have an NVidia 10XX series or better GPU, also add '--xformers' to the end fo the line. Save as webui-user-api-noui.bat in the same folder.  
4. (On Windows) run the Stable Diffusion Webui script webui-user-api-noui.bat. Make sure the file structure is correct (the easiest way is to place this repo and the Stable Diffusion Webui repo in the same folder). 

To change servers, trigger roles, etc, you must edit the .env file, the bot's discord auth token, etc
