import os,re,sys,stat,getopt,datetime
dlfolder="/opt/Download"
ext="/opt/extract"
p7zip,zip_only,rar_only,noask=0,0,0,0
def start():
    print("ExtractTarget Dir:\t",ext)
    print("Resource Dir:\t",dlfolder)
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
        print("available_ext:\t",avlstr, "\nCurrent Dir:\t",os.getcwd())
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
        if noask!="y":
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
                print("Extentions Found:",ename,end=" ")
            else: 
                print("Extentions Not Found.")
                continue
            if ename==f"{ename}_only":
                _un=ename
                print(f"Extract {fname} using un{ename}.")
            elif p7zip=='7z':
                print(f'Extract {fname} using p7zip.')
                _7z=1
            else: 
                print("Unsupported Extention.")
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
            if os.name=='nt':
                if _7z==1: os.system('7z x "%fullpath%" -o"%ext%/%n%/%n2%"')
                if _un=='zip': os.system('unzip "%fullpath%" -d "%ext%/%n1%/%n2%"')
                if _un=='rar': os.system('unrar x "%fullpath%" "%ext%/%n1%/%n2%"')
            else:
                if _7z==1: os.system('7z x "$fullpath" -o"$ext/$n1/$n2"')
                if _un=='zip': os.system('unzip "$fullpath" -d "$ext/$n1/$n2"')
                if _un=='rar': os.system('unrar x "$fullpath" "$ext/$n1/$n2"')
        os.remove('available_ext')
    os.chmod(ext,stat.S_IRWXO)
help="""
Usages:
\t-h|help\tDisplay this message.
\t-x\tSpecify your Resource Dir.
\t-o\tSpecify the Output Dir.
\t-s\tUse Pre-Defined Dir.
\t--noask\tDont Ask [y/n].
\tSample:\tpython tagmyarchive.py -x <ResourceDir> -o <ExtractTargetDir>
"""
if sys.argv[1:]:
    print(datetime.datetime.now(),"Start.")
else:
    print("Type 'python tagmyarchive.py -h' for usages.")
try:
    options,otheropts=getopt.getopt(sys.argv[1:],"sx:o:h",['noask'])
except getopt.GetoptError:
    print("Type 'python tagmyarchive.py -h' for usages.")
    sys.exit(2)
for option,argument in options:
    if option=='-h':print(help),sys.exit()
    if option=='-x':dlfolder,xg=argument,"passed"
    if option=='-o':ext,og=argument,"passed"
    if option=='-s':print("no args given,using defaults in script."),start()
    if option=='--noask':noask="y"
for otheropt in otheropts:
    if otheropt=='help':print(help),sys.exit()
    else:print("Type 'python tagmyarchive.py -h' for usages.")
if os.name=='nt':
    print("System:\t",os.name)
try:
    if og=="passed" and xg=="passed" :start()
except NameError:print("Finished without specify PATH args.")