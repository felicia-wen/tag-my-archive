# Extract and sort your archives simply.  
## Depends:
* Unix-like shell environment
* Packages
    * 7z 
    * if you already have 7z, you don't need the followings:
        * unzip 
        * unrar 
``` Shell
Type 'python tagmyarchive.py -h' for usages.
python tagmyarchive.py -x <ResourceDir> -o <ExtractTargetDir>
```
### OR 
#### run with `-s`, set them in .py
``` Python
dlfolder=""  # archives directory
ext=""       # extract directory
```
before | after
-------|------
![before](/before.png) | ![after](after.png)
