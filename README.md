## What is **e621dl**?
**e621dl** is an automated downloader for e621.net.  It can be used to create a local mirror of your favorite searches, and to keep these searches up to date efficiently as new files are uploaded. 

## How does **e621dl** work?
Put very simply, when **e621dl** starts, it determines:
1.  Which searches you would like to perform  (by reading your *tag file*)
2.  When the last time it was run  (by reading `config.txt`)

Once it knows these two things, it goes through the searches one by one, and downloads *only* anything uploaded since the last time it was run.  


## Installing 

There are two methods to install and run **e621dl**, using Python, or (Windows only) as a standalone executable. 

#### Using Python
The standard method works on all platforms. Simply download this repository and run `e621dl.py`.  
- *You must install Python 2.7 first [which you can find here](https://www.python.org/download/releases/2.7.7/).* 
- [Download the latest release of **e621dl**](https://github.com/wwyaiykycnf/e621dl/releases/latest), selecting the  source code (.zip or tarball, **NOT** the .msi)
- Unzip the archive to wherever you wish.
  

#### Windows Executable
This method does not require a Python installation, but only works in Windows.*
- [Download the latest release of **e621dl**](https://github.com/wwyaiykycnf/e621dl/releases/latest), selecting `e621dl-VersionNumber-win32.msi (**NOT** the .zip or tarball)
- Run the installer.  No shortcuts will be created, so remember where you install it (`C:\Program Files (x86)\e621dl\` by default. 

*: This has been tested __only__ in Windows 7.  Users encountering trouble should try the Python method. 

## Running e621dl
How you run **e621dl** depends on which of the above installation methods you selected:

**Python**:  Open the terminal/command line and run `e621dl.py` (you may need to type `python e621dl.py`).  Do not double-click on `e621dl.py`: you __must__ run it from the command line. 

**Windows executable** double click on `Run_e621dl_In_Windows.bat` (**NOT** `e621dl.exe`).  This file will be located in **e621dl**'s install directory. 

#### First-Time Run
The first time you run **e621dl**, you should see something like:
  ```
e621dl      INFO     running e621dl version 2.3.7
configfile  ERROR    new default file created: config.txt
configfile  ERROR    	verify this file and re-run the program
tagfile     ERROR    new default file created: tags.txt
tagfile     ERROR    	add to this file and re-run the program
e621dl      ERROR    error(s) encountered during initialization, see above
  ```
It's not as bad as it looks.  **e621dl** is telling you that it couldn't find *config* or *tags* files, so it created them.  This is totally normal behavior. 

#### Add your searches to the tags file
You must add at least one search you would like to perform to the tags file, so go ahead and open it and... Suprise: there are instructions on how to do this already inside the file!

#### [optional] Modify the config file
Most users will not need to modify the config file, `config.txt`, but feel free to look at it and see what the adjustable settings are.  However, please read [How Do Config File](docs/config_readme.md) to learn more about **e621dl**'s settings **BEFORE** you change any of them.  

#### Nornal Operation
Once you have added to the tags file, you should see something like this when you run **e621dl**:
```
e621dl      INFO     running e621dl version X.X.X
e621dl      INFO     e621dl was last run on 2014-06-25
e621dl      INFO     7 new uploads tagged: shark
e621dl      INFO         3 total (+3 new, 4 existing, 0 cached)

e621dl      INFO     starting download of 3 files

Downloading:        [###################################] 100.00% Done...

e621dl      INFO     successfully downloaded 3 files
e621dl      INFO     last run updated to 2014-06-25
```
There's actually quite a bit of information here.  Since last time **e621dl** was run (2014-06-25) there have been 7 uploads that match the search "shark".  4 of these have been downloaded previously, so they will be skipped.  But 3 are new, and they are downloaded.  Once they have been downloaded, **e621dl** updates its last run date to today (2014-06-26).  

Savvy users should realize at this point that they could simply schedule **e621dl** to run nightly in the wee hours of the morning, and their local collection will always be up-to-date... 

### Frequently Asked Questions
Please see the FAQ for solutions to common problems

## Feedback and Feature Requests
If you have any ideas for how things might work better, or about features you'd like to see in the future, please send an email to wwyaiykycnf+features@gmail.com.  I read every single email, so even if you think your idea is off-the-wall, please let me know and I'll see what I can do. 

### Donations
If you've benefitted from this *free* project, please consider [buying me something on Amazon](http://amzn.com/w/20RZIUHXLO6R4)!  Your support enables bug fixes, new features, and future development.  Thanks for thinking of me!
