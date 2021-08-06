import os
import re
dlfolder="/opt/Download"
ext="/opt/extract"
for root,dirs,files in os.walk(dlfolder):
    for name in files:
        frontname=re.search('.+(?=\.)',name)
        if frontname: print("frontname.group() Found",frontname.group())
        else: print("No archive found")
        extname=re.search('[^.]+$',name)
        if extname: print("extname.group() Found",extname.group())
        else: print("No ext found")
        fullpath=os.path.join(root,name)
        n=re.split(" +",frontname.group(),1)
        np=re.split(" - ?",frontname.group(),1)
        if len(np)!=1:n=np
        n1=n[0]
        n2=n[1]
        n0=re.search("(?<=\[)[^PMGB]*?(?=\])",frontname.group())
        if n0: 
            print("n0.group() Found",n0.group(0))
            n1=n0.group(0)
            n2=(frontname.group()).replace('['+n1+']',"")
        print("Author:",n1)
        print("Name:",n2)
        if n1=="" or n1==" " or n2=="" or n2==" ":
            print ("no author/name detected ,skipped.")
            continue
        extdir=ext+'/'+n1+'/'+n2
        if os.path.isdir(extdir):print("dir already exists.")
        else:os.makedirs(extdir)
        os.environ['ext']=ext
        os.environ['n1']=n1
        os.environ['n2']=n2
        os.environ['fullpath']=fullpath
        if (extname.group()=="zip"): os.system('unzip "$fullpath" -d "$ext/$n1/$n2"')
        elif (extname.group()=="rar"): os.system('unrar x "$fullpath" "$ext/$n1/$n2"')
        elif (extname.group()=="7z"): os.system('7z x "$fullpath" -o"$ext/$n1/$n2"')
        else: print("unsupported archive format.")



