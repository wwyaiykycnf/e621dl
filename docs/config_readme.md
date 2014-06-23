### How Do Config File?

Altering `config.txt` can change the way **e621dl** runs, and enable or disable program options.  While you are encouraged to modify these configuration options, care must be used to make sure you set each option to a legal value, or else **e621dl** may not run correctly (or at all).

##### Brief Overview
In general, try to match the format already present when `config.txt` was created, i.e.:

```JSON
{
    "cache_name": ".cache", 
    "cache_size": 65536,
    "create_subdirectories": false, 
    "download_directory": "downloads/", 
    "last_run": "2014-06-21", 
    "parallel_downloads": 6, 
    "tag_file": "tags.txt"
}
```
The format (familiar to anyone who has used JSON) is:
     "name_of_setting" : "setting_value",

Thus, it should be obvious that in the example above, we are telling **e621dl** to perform 6 downloads at a time, for example. 

**Important:**  Note that quotation marks (`" "`) are used on all lines **except for** `cache_size`, `create_subdirectories`, and `parallel_downloads`.  Those three settings cannot have their values wrapped in quotes, but all other settings **must** have their values wrapped in quotes.

The remainder of this readme is divided up into *common* and *advanced* settings.  Most users will not need to change the advanced settings. 

##### Common Settings

| Option Name           | Quotes? | Acceptable Range            | Description                                                |
| --------------------- | ------- | --------------------------- |----------------------------------------------------------- |
| download_directory    | Yes     | anything, must end with `/` | path where **e621dl** will download files to               | 
| create_subdirectories | No      | true or false               | create a subfolder for each line in tag file if true       |
| last_run              | Yes     | date (format: YYYY-MM-DD)   | the day **e621dl** was last run                            |


##### Advanced Settings

| Option Name           | Quotes? | Acceptable Range            | Description                                                  |
| --------------------- | ------- | --------------------------- |------------------------------------------------------------- |
| tag_file              | Yes     | anything                    | path to the file containing a list of searches to download   |
| parallel_downloads    | No      | 1 to 16                     | the number of simultaneous downloads to perform at once      |
| cache_name            | Yes     | anything                    | path to the file **e621dl** uses to track previous downloads |
| cache_size            | No      | 0 to big                    | number of items to keep in the cache.                        |

