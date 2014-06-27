## Frequently Asked Questions

##### When I run e621dl, there are 0 new uploads... How is this even possible?
Remember that **e621dl** downloads anything uploaded since it's **last run**.  The first time you **e621dl**, it doesn't **have** a last run date, so it picks today's date.  So if that's not what you wanted, you'll need to manually change the last run date.  Look in [How Do Config File](docs/config_readme.md) for `"last_run"` for instructions on how to do so. 

Alternatively, if your last run date *is* set properly, this simply means that nothing was uploaded since your last run.

##### e621dl crashes immediately, and an error is displayed ending with `ValueError: Invalid control character at: line X column Y (char Z)`

(wherein X, Y, and Z are arbitrary numbers).  There's something wrong with your config file. Read [How Do Config File](docs/config_readme.md) for formatting information-- e621dl is **very** particular about how this file is formatted.  Remember that you can always simply delete `config.txt` and a new one with correct formatting will be created.

##### e621dl crashes prior to downloading, and an error is displayed ending with `ValueError: No JSON object could be decoded`
This error, which is currently being researched, is sometimes seen when making large requests to e621.net.  To remedy it, adjust your last run date to a short time ago (the day before yesterday) and see if the issue persists. If it does, your request was probably just too large for the amount of traffic e621.net is currently experiencing.  Decrease your `last_run` date a month or so at a time until you get back as far as you'd like to go.  If the issue persists, please [file a bug report](docs/reporting_bugs.md).  

##### e621dl crashes during downloading, and an error is displayed ending with `IOError: [Errno 232] The pipe is being closed`
This error, which is currently being researched, is sometimes seen when the site is under high load from other users.  Currently there is no reccomendation to remedy it other than waiting for an hour or so and trying again.  If you see it every single time you run, please [file a bug report](docs/reporting_bugs.md). 

## Something else is broken
Don't hesitate to contact me if you experience a crash or other unexpected results not listed above, but please use [the reporting instructions](docs/reporting_bugs.md) for the quickest response and highest likelihood of me being able to figure out what's wrong.

