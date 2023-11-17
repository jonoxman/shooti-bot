@echo off

start cmd /k python bot.py
cd ..\stable-diffusion-webui
call webui-user-api-noui.bat
