##### 0 new uploads? How is this even possible?
Remember that **e621dl** downloads anything uploaded since it's **last run**.  The first time you **e621dl**, it doesn't **have** a last run date, so it picks today's date.  So if that's not what you wanted, you'll need to manually change the last run date.  Look in [How Do Config File](docs/config_readme.md) for `"last_run"` for instructions on how to do so. 

Alternatively, if your last run date *is* set properly, this simply means that nothing was uploaded since your last run.

##### Crash prior to downloading, ending with `ValueError: No JSON object could be decoded`
This error, which is currently being researched, is sometimes seen when making large requests to e621.net.  To remedy it, adjust your last run date to a short time ago (the day before yesterday) and see if the issue persists. If it does, your request was probably just too large for the amount of traffic e621.net is currently experiencing.  Decrease your `last_run` date a month or so at a time until you get back as far as you'd like to go.  If the issue persists, please [file a bug report](docs/reporting_bugs.md).  

##### Crash during downloading, ending with `IOError: [Errno 232] The pipe is being closed`
This error, which is currently being researched, is sometimes seen when the site is under high load from other users.  Currently there is no reccomendation to remedy it other than waiting for an hour or so and trying again.  If you see it every single time you run, please [file a bug report](docs/reporting_bugs.md). 

### Other Bugs
If you experience a crash or other unexpected results, please use [the reporting instructions](docs/reporting_bugs.md) for the quickest response.

