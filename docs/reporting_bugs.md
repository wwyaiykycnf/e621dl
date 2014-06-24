## So bug. Much Broken. Wow.  Very crash. 

Well... shit.  I'm sorry that you're here.  Unfortunately its impossible to test everything, but if you're willing to follow the steps below, I'll do my best to fix the problem for you and anyone else who has it.

This system is a little clunky, but bear with me for now until I get something more formal in place.


### Windows Users
1. navigate to the folder where e621dl.py is located on your computer
2. [click on the address bar of windows explorer and type: cmd](http://lifehacker.com/5989434/quickly-open-a-command-prompt-from-the-windows-explorer-address-bar)
3. a command prompt should open in the folder where e621dl.py is located. 
4. type/paste the following, one line at a time: 
```
echo %PROCESSOR_ARCHITECTURE% >> output.txt
systeminfo | findstr /C:"OS" >> output.txt
python.exe --version >> output.txt 2>&1
python.exe e621dl.py -v >> output.txt 2>&1
```
5. This will send your processor architecture, version of windows, version to python, and **debug output of e621dl** to a file called output.txt.    

6. Send an email to wwyaiykycnf+bugs@gmail.com, and attach output.txt, config.txt, and tags.txt to the email. 

### OSX/Linux/Unix
1. open a terminal and navigate to where e621dl.py is located on your computer
2. run the following:

```ShellSession
uname -a >> output.txt; python --version >> output.txt 2>&1; ./e621dl.py -v >> output.txt 2>&1
```

3. Send an email to wwyaiykycnf+bugs@gmail.com, and attach output.txt, config.txt, and tags.txt to the email. 

