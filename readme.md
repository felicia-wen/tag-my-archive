# TagMyArchive! 
>Extract and sort your archives simply.
## Matching
```Python
class Match:
    def All(str=".*"): return f"(?<=(?:\[|【|\(|（)){str}(?=(?:\]|】|\)|）))"
    def inBrackets(str="[^PMGB\W]+"):return f"(?<=(?:\[|【)){str}(?=(?:\]|】))"
    def inParentheses(str=".*"):return f"(?<=(?:\(|（)){str}(?=(?:\)|）))"
    def withBrackets(str="[^PMGB\W]+"):return f"(?:\[|【){str}(?:\]|】)"
    def withParentheses(str=".*"):return f"(?:\(|（){str}(?:\)|）)"
class Quirk:    
    def SplitMinus(str):return re.split("-+",str,1)
    def SplitSpace(str):return re.split(" +",str,1)
    def SplitBy(str):
        for by in (" by "," By "):
            if by in str:
                _case=1
                Info(f"{by}_string detected.")
                n1=re.split(by,str,1)[1]
                n2=re.split(by,str,1)[0]
                return _case,n1,n2
            else:return 1
    def Cleanup(str):return re.sub("^(\s*_*)*|(\s*_*)*$","",str)
```
## Depends:
* Packages
    * 7z 
    * if you already have 7z, you don't need the followings:
        * unzip 
        * unrar 
## Usage
```
Sample: python tagmyarchive.py -s -x <ResourceDir> -o <ExtractTargetDir>
Usages:
        -h                                 Display this message.
        -x <ResourceDir>                   Specify your Resource Dir.
        -o <ExtractTargetDir>              Specify the Output Dir.
        -s                                 Signal to run.
        --noask                            Dont Ask [y/n].
        --mvdir                            Move uncompressed Image/Video to OutputDir. 
        --exec<7z|Ur|Uz> <Addtional Args>  Execute Addtional Arguments in 7z,UnRAR,UnZip prompts.
```
### run without `-x -o`
``` Python
./tagmyarchive.py

dlfolder=""  # archives directory
ext=""       # extract directory
```
BEFORE | AFTER
-------|------
![before](/before.png) | ![after](after.png)
