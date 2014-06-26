### What is **e621dl**?
**e621dl** is an automated downloader for e621.net that keeps your favorite tags, artists, or searches up-to-date.

### How does **e621dl** work?
The behavior of e621dl is dependent on two files that tell it two crucial things:

1. ***e621dl*** **has to know what tags, artists, or searches you'd like to track.**  To determine this, it will look for a *tag file*.  Don't worry about creating this file, **e621dl** will create a blank one (called `tags.txt`) with instructions the first time you run it.
2. ***e621dl*** **has to know the last time you ran it.**  To find this, it will look in a file called `config.txt`.  Again, don't create this file yourself, instead just run **e621dl** and it will create a config file for you with default settings.  One of these settings, `"last_run"` tells **e621dl** when the last time it ran was. 

### Getting Started
**e621dl** requires Python 2.7, so download and install that first.  [Unless you're using Windows and the **e621dl** Windows Installer, in which case follow these instructions, then skip to step 2 below](https://github.com/wwyaiykycnf/e621dl/releases/tag/v2.4.6). 

1.  [Download the latest release] (https://github.com/wwyaiykycnf/e621dl/releases/latest) and unzip it.
2.  Run `e621dl.py`. (Windows: `e621dl.exe`) You should see something like:
  ```
  > ./e621dl.py
  configfile  ERROR    new default file created: config.txt
  configfile  ERROR    verify this new config file and re-run the program
  tagfile     ERROR    new default file created: tags.txt
  tagfile     ERROR    please add tags you wish to this file and re-run the program
  e621dl      ERROR    error(s) encountered during initialization, see above
  ```
  It's not as bad as it looks.  **e621dl** is telling you that it couldn't find a config file or tags file, so it created these files.  Most users will not need to modify `config.txt` but feel free to look at it and see what settings you can change. 

3. Add tags or artists you wish to download to the newly-created tag file.  There should already be instructions in the `tags.txt` that was created for you.  All lines starting with a `#` are ignored by **e621dl**, so feel free to leave the instructions in the file after adding your tags, if you wish. 

Once you've added a few lines to the tag file and reviewed `config.txt`, you're ready to run **e621dl**!


### Running **e621dl**
When you run **e621dl**, it will determine the time it was last run, and then:
- read a line from the tag file
- perform a search on e621.net using that line
- download all new files matching that search (files uploaded AFTER the last time **e621dl** was run)

This process will be repeated for each line in the tag file, until every line has been checked.  The last run date will then be set to yesterday's date, and **e621dl** will report the number of total downloads. 

**Example Output:**
```
> ./e621dl.py
e621dl      INFO     e621dl was last run on 2014-06-18
e621dl      INFO     Checking for new uploads tagged: cat
e621dl      INFO     10 new uploads for: cat
e621dl      INFO     	will download 10	(cached: 0, existing: 0)

e621dl      INFO     starting download of 10 files

Downloading:        [###################################] 100.00% Done...

e621dl      INFO     successfully downloaded 10 files
e621dl      INFO     last run updated to 2014-06-18
```

### Configuring **e621dl**
Please see [How Do Config File](docs/config_readme.md) to learn more about **e621dl**'s settings and how to change them. 

### Frequently Asked Questions

##### Very few or no downloads
The first time you run **e621dl**, its possible that not too much will happen.  **e621dl** picks yesterday as the `"last_run"` date when it is first run, so if that's not what you wanted, you'll need to manually change the last run date.  Look in [How Do Config File](docs/config_readme.md) for `"last_run"`. 

### Bugs
If you experience a crash or other unexpected results, please use [the reporting instructions](docs/reporting_bugs.md) for the quickest response.

## Feedback and Feature Requests
If you have any ideas for how things might work better, or about features you'd like to see in the future, please send an email to wwyaiykycnf+features@gmail.com.  I read every single email, so even if you think your idea is off-the-wall, please let me know and I'll see what I can do. 

### Donations
If you've benefitted from this *free* project, please consider [buying me something on Amazon](http://amzn.com/w/20RZIUHXLO6R4)!  Your support enables bug fixes, new features, and future development.  Thanks for thinking of me!
