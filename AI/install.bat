
git submodule update --init --remote AI/.venv

set py=%~dp0.venv\python.exe

%py% -m pip install --upgrade pip setuptools wheel hatchling hatch-requirements-txt

%py% -m pip install git+https://github.com/MineFartS/Server-PythonPackage --ignore-requires-python --no-build-isolation

%py% -m pip install ollama diffusers transformers accelerate

%py% -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

