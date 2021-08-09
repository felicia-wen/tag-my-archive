# Extract and sort your archives simply.  
## 原理
通过正则表达式对压缩包名进行分析处理，并将其解压到生成的文件夹中。
## Match
* [] 【】
* ' - ' '-'
* ()  
Folder:`/{Author}/{Work}/{(str)`}

## Depends:
* Packages
    * 7z 
    * if you already have 7z, you don't need the followings:
        * unzip 
        * unrar 
``` Shell
Usages:
        -h|help Display this message.
        -x<ResourceDir> Specify your Resource Dir.
        -o<ExtractTargetDir>    Specify the Output Dir.
        -s      Signal to run.
        --noask Dont Ask [y/n].
        --mvdir Move uncompressed Image/Video to OutputDir.
        --exec<Addtional Args>   Exec Addtional Args in Shell prompt.
Sample: python tagmyarchive.py -s -x <ResourceDir> -o <ExtractTargetDir>
```
#### run with `-s`, set them in .py
``` Python
dlfolder=""  # archives directory
ext=""       # extract directory
```
before | after
-------|------
![before](/before.png) | ![after](after.png)
