#!/usr/bin/env python3
import os,re,sys,stat,getopt,datetime,shutil
dlfolder="/opt/Download"
ext="/opt/extract"
noask=0
mvdir=0
# SGR color constants
# rene-d 2018
class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
def Shell(t,*r):
    r=''.join(r)
    print(Colors.GREEN+"Shell:\t"+Colors.LIGHT_GREEN+t+Colors.CYAN+r+Colors.END)
def Skip(t,*r):
    r=''.join(r)
    print(Colors.FAINT+Colors.CYAN+"Skip:\t"+Colors.LIGHT_CYAN+t+Colors.LIGHT_WHITE+r+Colors.END)
def Info(t,*r):
    r=''.join(r)
    print(Colors.BLUE+"Info:\t"+Colors.LIGHT_BLUE+t+Colors.LIGHT_PURPLE+r+Colors.END)
def Warn(t,*r):
    r=''.join(r)
    print(Colors.NEGATIVE+Colors.BROWN+"Warning:\t"+Colors.YELLOW+t+Colors.LIGHT_WHITE+r+Colors.END)
def Error(t,*r):
    r=''.join(r)
    print(Colors.NEGATIVE+Colors.RED+"Error:\t"+Colors.BLINK+t+Colors.END+Colors.UNDERLINE+Colors.LIGHT_RED+r+Colors.END)

def start():
    edit=0
    mv=0
    Info("ExtractTarget Dir:\t",ext)
    Info("Resource Dir:\t",dlfolder)
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
        Info("Current Dir:\t",os.getcwd())
        if '7z' in avlstr:
            p7zip='7z'
            Shell("7z/p7zip detected.")
        elif 'unzip' in avlstr: 
            zip_only='zip'
            Shell("UnZip detected.")
            if 'unrar' in avlstr: 
                rar_only='rar'
                Shell("unRAR detected.")
        else: 
            shellNone=1
            Shell("None of shell way extract method available.\a")
            sys.exit()
        Shell("available extract method:",avlstr)
        if noask!=1:
            y=input("Continue?\n[y/n]:")
            Info(y)
            if y!="y":sys.exit()
    for root,dirs,files in os.walk(dlfolder):
        for name in files:
            if os.path.isfile(ext+'/done')==False:
                f=open(ext+'/done','x')
                f.close
            f=open(ext+'/done','r+')
            frs=f.readlines()
            skip=1
            for fr in frs:
                if name+'\n'==fr:
                    Skip(f"Recorded File:{name},Skipping.")
                    f.close
                    break
            else:skip=0
            if skip!=0:
                Skip("Skipped.")
                continue
            fullpath=os.path.join(root,name)
            frontname=re.search('.+(?=\.)',name)
            if frontname: 
                fname=frontname.group()
                Info("archive found.",fname)
            else: 
                Skip("archive not found.")
                continue
            extname=re.search('[^.]+$',name)
            if extname: 
                ename=extname.group()
                Info("Extentions Found:",ename)
                if ename not in ['rar','zip','7z']:
                    Skip("Not an archive format.")
                    if ename in ['jpg','png','mp4','avi']:
                        Info(ename,"detected.")
                        if os.path.isdir(root) and mvdir==1 and root!=dlfolder:
                            mv=1
                            edit=1
                    else:continue
            else: 
                Skip("Extentions Not Found,Skipped.")
                continue
            if (ename=='zip' and zip_only=="zip") or (ename=='rar' and rar_only=='rar') and mv!=1:
                _un=ename
                Info(f"Extract {fname} using un{ename}.")
            elif p7zip=='7z':
                Info(f'Extract {fname} using p7zip.')
                _7z=1
            else: 
                Skip("Unsupported Extention.")
                continue
            Shell("environment checked.")
            if mv==1:
                fname=re.search("[^/]*$",root).group()
                Info("fname changed to:",fname)
            e2=re.split(" +",fname,1)
            e1=re.split("-+",fname,1)
            e=""
            _match=0
            if len(e1)!=1:
                Info("Using fitter='-'")
                e=e1
                n1=e[0]
                n2=e[1]
                _match=1
            elif len(e2)!=1:
                Info("Using fitter=' '")
                e=e2
                n1=e[0]
                n2=e[1]
                _match=1
            ns=re.search("(?<=\[)[^PMGB]*?(?=\])|(?<=【)[^PMGB]*?(?=】)",fname)
            n3=re.search("(?<=[(]).*?(?=[)])|(?<=[（]).*?(?=[）])",fname)
            if ns: 
                Info("Special Matching triggered,Overwrite.",ns.group())
                n1=ns.group()
                n2=fname.replace(f"[{n1}]","")
                n2=n2.replace(f"【{n1}】","")
                _match=1
            for by in (" by "," By "):
                if by in fname:
                    Info("by_string detected,Overwrite.")
                    n1=re.split(by,fname,1)[1]
                    n2=re.split(by,fname,1)[0]
                    _match=1
            if n3 and _match==1:
                Info("Extended Matching triggered.")
                n3=n3.group(0)
                n2=n2.replace(f"({n3})","")
                n1=n1.replace(f"({n3})","")
                n3=re.sub("^(\s*_*)*|(\s*_*)*$","",n3)
            n1=re.sub("^(\s*_*)*|(\s*_*)*$","",n1)
            n2=re.sub("^(\s*_*)*|(\s*_*)*$","",n2)
            Info("Author:",n1)
            Info("Name:",n2)
            if n3 and _match==1:extdir=f"{ext}/{n1}/{n2}/{n3}"
            else: extdir=f"{ext}/{n1}/{n2}"
            if _match==0:
                Skip("No Author/Name Detected ,Skipped.")
                continue
            if n3:Info('Extented String=',n3)
            if os.path.isdir(extdir):Warn("dir already exists.")
            else:os.makedirs(extdir),Info("mkdir:",extdir)
            if mv==1:
                Warn(f"MvDir:\t--mvdir given,move directory:{fullpath} to {extdir}")
                shutil.move(fullpath,extdir)
                continue
            Info(f"Extracting {name} to {extdir}")
            os.environ['n1']=n1
            os.environ['n2']=n2
            os.environ['fullpath']=fullpath
            os.environ['extdir']=extdir
            edit=1
            if os.name=='nt':
                if _7z==1: osret=os.system('7z x "%fullpath%" -o"%extdir%" -y %arg%')
                if _un=='zip': osret=os.system('unzip "%fullpath%" -d "%extdir%" -o %arg%')
                if _un=='rar': osret=os.system('unrar x "%fullpath%" "%extdir%" y %arg%')
                os.system('chmod -R 775 "%extdir%"')
            else:
                if _7z==1: osret=os.system('7z x "$fullpath" -o"$extdir" -mmt1 -y $arg')
                if _un=='zip': osret=os.system('unzip "$fullpath" -d "$extdir" -o $arg')
                if _un=='rar': osret=os.system('unrar x "$fullpath" "$extdir" y $arg')
                os.system('chmod -R 775 "$extdir"')
            if osret==0:
                f.write(name+'\n')
                Info("History Recorded.")
            else:Error("Encountered with error:",str(osret))
            f.close
    f.close
    if os.path.isfile('available_ext'):os.remove('available_ext')
    
help="""
Sample:\tpython tagmyarchive.py -s -x <ResourceDir> -o <ExtractTargetDir>
Usages:
\t-h                       Display this message.
\t-x <ResourceDir>         Specify your Resource Dir.
\t-o <ExtractTargetDir>    Specify the Output Dir.
\t-s                       Signal to run.
\t--noask                  Dont Ask [y/n].
\t--mvdir                  Move uncompressed Image/Video to OutputDir. 
\t--exec <Addtional Args>  Exec Addtional Args in Shell prompt.
"""
print(datetime.datetime.now(),Colors.BOLD+"Start.")
try:
    options,otheropts=getopt.getopt(sys.argv[1:],"sx:o:h",['noask','mvdir','exec='])
except getopt.GetoptError:
    Info("Type 'python tagmyarchive.py -h' for usages.")
    sys.exit(2)
sta,_x,_o=0,0,0
for option,argument in options:
    if option=='-h':print(help),sys.exit()
    if option=='-x':
        dlfolder=argument
        _x=1
    if option=='-o':
        ext=argument
        _o=1
    if option=='--noask':
        Info("NoAsking...")
        noask=1
    if option=='--mvdir':
        Warn("\t--mvdir given,this may cause system impact.")
        mvdir=1
    if option=='-s':sta=1
    if option=='--exec':os.environ['arg']=argument
    else:os.environ['arg']=''
for otheropt in otheropts:
    if otheropt=='help':Info(help),sys.exit()
    else:Info("Type 'python tagmyarchive.py -h' for usages.") 
if os.name=='nt':
    Info("System:\t",os.name)
try:
    if sta==1 or (_x==1 and _o==1):start()
except NameError:Info("Type 'python tagmyarchive.py -h' for usages.")