<h1> ⚒️ Installation </h1>

## 1. Prerequisites 

  * Install FFMPEG from [FFMPEG builds](https://www.gyan.dev/ffmpeg/builds), extract it and add it to your path [How to add FFMPEG to Path](https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10#:~:text=Add%20FFmpeg%20to%20Windows%20path%20using%20Environment%20variables&text=In%20the%20Environment%20Variables%20window,bin%5C%E2%80%9D%20and%20click%20OK.)

## 2. Running Code

First, clone the repository and cd into the folder:

```
$ git clone https://github.com/rohit-sram/Enigma.git
```

Alternatively, clone repo using SSH keys,
  ```
  $ git clone git@github.com:rohit-sram/Enigma.git
  ```
```
$ cd Enigma
```

### Create a .env file for Discord token: 
Use the following format `DISCORD_TOKEN=#SECRET_TOKEN#`
<!-- ### Join the discord channel of the bot [Discord Channel of bot](https://discord.com/channels/1017135653315686490/1017135653789646850) and connect to the voice channel. -->

Install requirements 
```
$ pip install -r requirements.txt
```
Start the bot
```
$ python bot.py
```

You can now use the discord bot to give music recommendations! Use `]help` to see all functionalities of bot.


#### Note: Make sure the bot has the role `bot` and the user has the role `DJ` 
