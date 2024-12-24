# MemRat
MemRat is a quite simple rat designed to be used through a Discord Bot. 

The main functions include:
 - Uploading (and executing) files on the target's machine
 - Taking the target's tokens
 - Annoying the target
 - Being remote controlled
 - Controllable file explorer on target's machine 
 - Downloading files from the target's machine (handy with the file explorer)
 - Working for multiple machines at once, and being able to give machines nicknames to recognize them.
 - Streaming service on a simple Flask website (a bit broken currently)

## RAT USE AND COMPILING
 - To use the rat, you might want to compile your python code first. You can do this with whatever compiler you want (such as PyInstaller). Then after that, the target has to run the file once, the rat should move into a startup directrory, so it should start up automatically when the computer is started. After the target runs the rat for the first time, you will get a notification in the channel you provided, including the machine's IP and the command used to control the machine. 
