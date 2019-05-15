# Quote-bot
A discord bot that can store quotes/messages from users in a database which can be called at any time.

## Requirements
```
Python 3.5+
discord.py
```

## How to run
1. Install the discord.py package.
```
pip install discord.py
```
2. Create a bot application [here](https://discordapp.com/developers/applications/) and get a discord token/secret key.

4. Create a file named config.vars and put the following line in it: `export DISCORD_SECRET=xxxx` where `xxxx` is your token/secret key.

3. To add the bot to your server find your client ID from the page above and replace it in X's in the link below.
```
https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXXXXX&scope=bot
```
5. Finally run:
```
./run.sh
```
## Commands
%qsave [user] [message] - stores a quote by the user.  
%getq [user] - gets a users quote.  
%qhelp - shows a list of commands and syntax.   
%qrand - gets a random quote from a random user.

## FAQ
* The program has checks to stop people adding the same quote to a given person.

* Check your python version if you have async problems.
