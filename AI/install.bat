@echo off

set py=%~dp0.venv\python.exe

%py% -m pip install philh_myftp_biz --ignore-requires-python

%py% -m pip install ollama diffusers transformers accelerate

%py% -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

