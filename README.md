What is **e621dl**?
===============
**e621dl** is an automated downloader for e621.net, which enables you to keep your
favorite artists or tags up to date.

Each time **e621dl** is run, it will download all files that contain at least one
tracked tag, that have been uploaded since the last time **e621dl** was run.

Getting Started
===============

1. Download or clone this project
2. In the same directory as `e621dl.py`, create a file called `tags.txt`
3. Add tags or artists you wish to download to `tags.txt`, one tag per line.

example `tags.txt`:
```
    cat
    dog
```

*Note: e621dl has only been tested with a single per line, but may work with more.*

Running **e621dl**
===============
**e621dl** requires Python 2.7, so make sure you have that.

Running `e621dl.py` will begin an 'update'.  The tags/artists listed in
`tags.txt` will be checked, one at a time, to see if there are any files that
have been uploaded since the last time **e621dl** was run.

The first time you run **e621dl**, not much will happen.  When **e621dl** cannot
determine the last time it was run (e.g., the first time it is run) the current
date is used.

The last run date may be altered by modifying `.lastrun.txt`, but be sure to
match the YYYY-MM-DD format present in `.lastrun.txt`

Donations
===============
Help support future development of this project!

[![BitCoin donate button](http://img.shields.io/bitcoin/donate.png?color=brightgreen)](https://coinbase.com/checkouts/1FZR3iP9zHRqQZeG8zg8Tmx471jP1c8eYe "Make a donation to this project using BitCoin")
[![DogeCoin donate button](http://img.shields.io/dogecoin/donate.png?color=yellow)](README.md#note-dogecoin-donations-may-be-sent-to-dkfycmjxndgaqhq5wdyjlneoqd3xbdygdr "Many donate.  So Project.  Wow.  Very DogeCoin.")
[![Wishlist browse button](http://img.shields.io/amazon/wishlist.png?color=blue)](http://amzn.com/w/2F4EC3BPU9JON "Support me by buying something for me on Amazon")

#######Note: *[Dogecoin](http://dogecoin.com) donations may be sent to:* `DKfycmjXNDgaqhQ5wdyJLNEoqd3XBDyGdr`

