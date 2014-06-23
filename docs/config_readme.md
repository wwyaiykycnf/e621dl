## How Do Config File?

You can alter the way **e621dl** runs by enabling or disabling program settings in `config.txt`.  While you are encouraged to modify these options to make **e621dl** work right for you, be careful to set each option to a legal value, or else **e621dl** may not run correctly (or at all).

### Brief Overview
In general, try to match the format of the default `config.txt`, i.e.:

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
The format of this file (familiar to anyone who has used JSON) is:
     
     "name_of_setting" : "value_for_that_setting",

Thus, it should be obvious that in the example above, we are telling **e621dl** to perform 6 downloads at a time, and that our tag file is called `tags.txt`, for example.  

##### When to use quotation marks
Note that for the `cache_size`, `create_subdirectories`, and `parallel_downloads` settings, their values are *not* in quotation marks, but for all others, (which are all strings) quotation marks are used.  Not following this rule will likely cause the program not to run, so in the detailed explanation below, each option lists whether quotes are required. 


### Common Settings

| Option Name           | Quotes? | Acceptable Range            | Description                                                |
| --------------------- | ------- | --------------------------- |----------------------------------------------------------- |
| download_directory    | Yes     | anything                 | path where **e621dl** puts downloads (must end with a `/`)    | 
| create_subdirectories | No      | `true` or `false`           | create a subfolder for each line in tag file if true    |
| last_run              | Yes     | date (format: `YYYY-MM-DD`) | the last day **e621dl** was last run                       |


### Advanced Settings
*(Most users will not need to change the advanced settings.)*

| Option Name           | Quotes? | Acceptable Range            | Description                                                  |
| --------------------- | ------- | --------------------------- |------------------------------------------------------------- |
| tag_file              | Yes     | anything                    | path to the file containing a list of searches to download   |
| parallel_downloads    | No      | 1 to 16                     | the number of simultaneous downloads to perform at once      |
| cache_name            | Yes     | anything                    | path to the file **e621dl** uses to track previous downloads |
| cache_size            | No      | any positive integer        | number of items to keep in the cache.                        |
