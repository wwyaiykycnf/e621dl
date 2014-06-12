What is `e621dl`?
===============
e621dl is an automated downloader for e621.net, which enables you to keep your 
favorite artists or tags up to date.  

Each time e621dl is run, it will download all files that contain at least one 
tracked tag, that have been uploaded since the last time e621dl was run. 

Getting Started
===============

1. Download or clone this project
2. In the same directory as `e621dl.py`, create a file called `tags.txt`
3. Add tags or artists you wish to download to `tags.txt`.  You may only put
one tag/artist per line.  

example tags.txt:
`
    cat
    dog
`

Running `e621dl`
===============
`e621dl` requires Python 2.7, so make sure you have that. 

Running `e621dl.py` will begin an 'update'.  The tags/artists listed in
`tags.txt` will be checked, one at a time, to see if there are any files that
have been uploaded since the last time `e621dl` was run.

The first time you run e621dl, not much will happen.  When e621dl cannot 
determine the last time it was run (e.g., the first time it is run) the current
date is used.

The last run date may be altered by modifying `.lastrun.txt`, but be sure to 
match the YYYY-MM-DD format present in `.lastrun.txt`
