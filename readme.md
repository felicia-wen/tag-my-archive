# Extract and sort your archives simply.  
## Depends:
* Unix-like shell environment
* Packages
    * 7z 
    * if you already have 7z, you don't need the followings:
        * unzip 
        * unrar 
``` Shell
Usages:
-h|help Display this message.
-x      Specify your Resource Dir.
-o      Specify the Output Dir.
-s      Use Pre-Defined Dir.
--noask Dont Ask [y/n].
Sample: python tagmyarchive.py -x <ResourceDir> -o <ExtractTargetDir>
```
#### run with `-s`, set them in .py
``` Python
dlfolder=""  # archives directory
ext=""       # extract directory
```
before | after
-------|------
![before](/before.png) | ![after](after.png)
