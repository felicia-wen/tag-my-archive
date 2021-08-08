#!/usr/bin/env python3
import os,re,sys,stat,getopt,datetime,shutil
dlfolder="/opt/Download"
ext="/opt/extract"
noask=0
def start():
    edit=0
    print("ExtractTarget Dir:\t",ext)
    print("Resource Dir:\t",dlfolder)
    p7zip,zip_only,rar_only=0,0,0
    _7z,_un=0,0
    os.environ['ext']=ext
    if os.path.isdir(ext):os.chdir(ext)
    else: os.makedirs(ext),os.chdir(ext)
    if os.name=='nt':  
        os.system('echo $(which 7z unzip unrar | grep -E -o "7z$|unzip$|unrar$") > %ext%/available_ext')
    else:
        os.system('echo $(which 7z unzip unrar | grep -E -o "7z$|unzip$|unrar$") > $ext/available_ext')
    with open("available_ext",'r') as avl:
        avlstr=avl.read()
        print( "Current Dir:\t",os.getcwd(),"\nShell:\tavailable extract method:",avlstr)
        if '7z' in avlstr:
            p7zip='7z'
            print("Shell:\t7z detected.")
        elif 'unzip' in avlstr: 
            zip_only='zip'
            print("Shell:\tunzip detected.")
            if 'unrar' in avlstr: 
                rar_only='rar'
                print("Shell:\tunrar detected.")
        else: 
            shellNone=1
            print("Shell:\tNone of shell way extract method available.\a")
            sys.exit()
        if noask!=1:
            y=input("Continue?\n[y/n]:")
            print(y)
            if y!="y":sys.exit()
    for root,dirs,files in os.walk(dlfolder):
        for name in files:
            if os.path.isfile(ext+'/done')==False:
                f=open(ext+'/done','x')
                f.close()
            f=open(ext+'/done','r+')
            if name in f.read():
                print(f"Recorded File:{name},Skipped.")
                
                continue
            
            f.write(name+'\n')
            f.close
            fullpath=os.path.join(root,name)
            frontname=re.search('.+(?=\.)',name)
            if frontname: 
                fname=frontname.group()
                print("archive found.",fname)
            else: 
                print("archive not found.")
                
                continue
            
            extname=re.search('[^.]+$',name)
            if extname: 
                ename=extname.group()
                print("Extentions Found:",ename)
                if ename not in ['rar','zip','7z']:
                    print("Not archive format.")
                    if ename in ['jpg','png','mp4','avi']:
                        print(ename,"detected.")
                        if os.path.isdir(root) and mvdir==1 and root!=dlfolder:
                            print(f"\t--mvdir given,move directory:{root} to {ext}")
                            shutil.move(root,ext)
                            edit=1
                        continue
                    else:continue
            else: 
                print("Extentions Not Found.")
                
                continue
            
            if (ename=='zip' and zip_only=="zip") or (ename=='rar' and rar_only=='rar'):
                _un=ename
                print(f"Extract {fname} using un{ename}.")
            elif p7zip=='7z':
                print(f'Extract {fname} using p7zip.')
                _7z=1
            else: 
                print("Shell:\tUnsupported Extention.")
                
                continue
            
            print("shell environment checked.")
            n=re.split(" +",fname,1)
            np=re.split(" - ?",fname,1)
            if len(np)!=1:n=np
            n1=n[0]
            n2=n[1]
            n0=re.search("(?<=\[)[^PMGB]*?(?=\])",fname)
            if n0: 
                print("Special Matching triggered.",n0.group(0))
                n1=n0.group(0)
                n2=(fname).replace(f"[{n1}]","")
            print("Author:",n1)
            print("Name:",n2)
            if n1=="" or n1==" " or n2=="" or n2==" ":
                print ("No Author/Name Detected ,Skipped.")
                
                continue
            
            extdir=f"{ext}/{n1}/{n2}"
            if os.path.isdir(extdir):print("dir already exists.\n",extdir)
            else:os.makedirs(extdir)
            os.environ['n1']=n1
            os.environ['n2']=n2
            os.environ['fullpath']=fullpath
            edit=1
            if os.name=='nt':
                if _7z==1: os.system('7z x "%fullpath%" -o"%ext%/%n%/%n2%" -y')
                if _un=='zip': os.system('unzip "%fullpath%" -d "%ext%/%n1%/%n2%"')
                if _un=='rar': os.system('unrar x "%fullpath%" "%ext%/%n1%/%n2%"')
            else:
                if _7z==1: os.system('7z x "$fullpath" -o"$ext/$n1/$n2" -y')
                if _un=='zip': os.system('unzip "$fullpath" -d "$ext/$n1/$n2" -n')
                if _un=='rar': os.system('unrar x "$fullpath" "$ext/$n1/$n2" y')
    if edit==1:
        os.chmod(extdir,stat.S_IROTH)
        os.chmod(extdir,stat.S_IRWXG)
        os.chmod(extdir,stat.S_IRWXU)
    if os.path.isfile('available_ext'):os.remove('available_ext')
help="""
Usages:
\t-h|help\tDisplay this message.
\t-x\tSpecify your Resource Dir.
\t-o\tSpecify the Output Dir.
\t-s\tSignal to run.
\t--noask\tDont Ask [y/n].
\t--mvdir\tmove uncompressed Image/Video to OutputDir directly. 
Sample:\tpython tagmyarchive.py -x <ResourceDir> -o <ExtractTargetDir>
"""
print(datetime.datetime.now(),"Start.")
try:
    options,otheropts=getopt.getopt(sys.argv[1:],"sx:o:h",['noask','mvdir'])
except getopt.GetoptError:
    print("Type 'python tagmyarchive.py -h' for usages.")
    sys.exit(2)
for option,argument in options:
    if option=='-h':print(help),sys.exit()
    if option=='-x':
        dlfolder=argument
        _x=1
    if option=='-o':
        ext=argument
        _o=1
    if option=='--noask':
        print("NoAsking...")
        noask=1
    if option=='--mvdir':
        print("Warning:\t--mvdir given,this may cause system impact.")
        mvdir=1
    if option=='-s':sta=1
for otheropt in otheropts:
    if otheropt=='help':print(help),sys.exit()
    else:print("Type 'python tagmyarchive.py -h' for usages.")
if os.name=='nt':
    print("System:\t",os.name)
try:
    if sta==1 or (_x==1 and _o==1):start()
except NameError:print("Type 'python tagmyarchive.py -h' for usages.")