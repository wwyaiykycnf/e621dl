What is **e621dl**?
===============
**e621dl** is an automated downloader for e621.net that keeps your favorite tags, artists, or searches up-to-date.

How does **e621dl** work?
===============
The behavior of e621dl is dependent on two files that tell it two crucial things:

1. ***e621dl*** **has to know what tags, artists, or searches you'd like to track.**  To determine this, it will look for a file called `tags.txt`.  Don't worry about creating this file, **e621dl** will create a blank one with instructions the first time you run it.
2. ***e621dl*** **has to know the last time you ran it.**  To find this, it will look in a file called `config.txt`.  Again, don't create this file yourself, instead just run **e621dl** and it will create a config file for you with default settings.  One of these settings, `"last_run"` tells **e621dl** when the last time it ran was. 

Getting Started
===============
**e621dl** requires Python 2.7, so download and install that first.  Once you have Python installed:

- [Download the latest release] (https://github.com/wwyaiykycnf/e621dl/releases/latest) and unzip it.
- Run `e621dl.py`.  You should see something like:
```
> ./e621dl.py
configfile  ERROR    new default file created: config.txt
configfile  ERROR    verify this new config file and re-run the program
tagfile     ERROR    new default file created: tags.txt
tagfile     ERROR    please add tags you wish to this file and re-run the program
e621dl      ERROR    error(s) encountered during initialization, see above
```
It's not as bad as it looks.  **e621dl** is telling you that it couldn't find a config file or tags file, so it created these files.  Most users will not need to modify `config.txt` but feel free to look at it and see what settings you can change. 

- Add tags or artists you wish to download to `tags.txt`.  There should already be instructions in the `tags.txt` that was created for you.  All lines starting with a `#` are ignored by **e621dl**, so feel free to leave the instructions in the file after adding your tags, if you wish. 

Once you've added a few lines to `tags.txt` and reviewed `config.txt`, you're ready to run **e621dl**!


Running **e621dl**
===============

When you run **e621dl**, it will determine the time it was last run, and then:
- read a line from `tags.txt` 
- perform a search on e621.net using that line
- download all new files matching that search (files uploaded AFTER the last time **e621dl** was run)

This process will be repeated for each line in `tags.txt` until the file has been completely processed.  The last run date will then be set to yesterday's date, and **e621dl** will report the number of total downloads. 

### I did that and not much happened 
The first time you run **e621dl**, its possible that not too much will happen.  Remember when `config.txt` was created and you opened it and saw that the `"last_run"` date was set to yesterday?  **e621dl** does that automatically, and it's set that way intentionally.  **e621dl** might check some old uploads to make sure it didn't miss anything, but it will never re-download old files. 

Anyway, if that's not what you wanted for your very first update, you'll need to:  

### Change the last run date
You can set the last run date to any date that follows the format `YYYY-MM-DD`.  So if you'd like to download EVERYTHING of a given tag from the beginning of time (Ok, the beginning of e621.net) until today, change the `"last_run"` variable in `config.txt` to something old:

    "last_run": "1986-01-01",

Bugs, New Features, and Feedback
=================
If you find something broken or have any ideas about features you'd like to see in the future, please contact me at [wwyaiykycnf@gmail.com].  I read every single email, so even if you think your idea is off-the-wall, or your bug is super-rare, please let me know and I'll see what I can do. 

Donations
===============
If you've benefitted from this *free* project, please consider donating something!  Your support enables bug fixes, new features, and future development!  

[![Wishlist browse button](http://img.shields.io/amazon/wishlist.png?color=blue)](http://amzn.com/w/2F4EC3BPU9JON "Support me by buying something for me on Amazon")
[![BitCoin donate button](http://img.shields.io/bitcoin/donate.png?color=brightgreen)](https://coinbase.com/checkouts/1FZR3iP9zHRqQZeG8zg8Tmx471jP1c8eYe "Make a donation to this project using BitCoin")
[![DogeCoin donate button](http://img.shields.io/dogecoin/donate.png?color=yellow)](README.md#note-dogecoin-donations-may-be-sent-to-dkfycmjxndgaqhq5wdyjlneoqd3xbdygdr "Many donate.  So Project.  Wow.  Very DogeCoin.")

#######Note: *[Dogecoin](http://dogecoin.com) donations may be sent to:* `DKfycmjXNDgaqhQ5wdyJLNEoqd3XBDyGdr`

