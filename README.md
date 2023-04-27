MemRat a.k.a MemWare is a quite simple rat designed to be used through a Discord Bot. 

The main functions include:
 - Uploading (and executing) files on the victim's machine
 - Stealing tokens on request
 - Annoying the victim
 - Being remote controlled
 - Controllable file explorer on victim's machine 
 - Downloading files from the victim's machine (handy with the file explorer)
 - Working for multiple machines, and being able to give machines nicknames to recognize them.
 - Streaming service on a simple Flask website
 
The rat IS DETECTABLE by default, you have to obfuscate it yourself if you feel like getting it through AV. This rat is for educational purposes only.

RAT USE AND COMPILING
 - The rat is quite simple to use: Set configs to be the ones you want (startup, bot token, notificationchannel), compile it with a python compiler (such as PyInstaller, not included), done. When someone launches the EXE, you will get a notification in the notification channel you set, and you can start controlling the machine with '(MACHINE'S-IP)+help' on any channel that the discord bot is in. The machine's IP will be included in the start notification.

WIP IDEAS:
 - Keylogger
 - Probably import this to work on the web instead of discord some day
 - In-script obfuscator


The token logger in the rat is taken from: https://github.com/mouadessalim/CookedGrabber (Not mine)

