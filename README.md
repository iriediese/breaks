# breaks
Matrix timer bot telling you to take a break. Uses [simplematrixbotlib](https://github.com/i10b/simplematrixbotlib).
## Usage
if you need a venv, do `python -m venv .` and `source bin/activate`  
install requirements with `pip install -r requirements.txt`          

run `python breaks.py <homeserver> <username> <password>`              

bot commands:
- `!echo [args...]` echoes back the args to you, for debugging 
- `!start <minutes>` starts the timer
- `!stop` stops the timer
  
if the timer is running, the bot will tell you to take a break every `<minutes>` minutes.
