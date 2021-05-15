# -*- coding: utf-8 -*-
"""
Created on Fri May 14 06:47:43 2021

@author: shane
"""
import string
import os
import shutil
import subprocess
import kivy
import PyInstaller

def start_exe(directory):
    name=directory.split('\\')[-1]
    fileloc=os.path.join(directory,'main.py')
    icon=''
    for dir,subdir,files in os.walk(directory):
        for file in files:
            if '.ico' in file:
                icon=" "+os.path.join(dir,file)
    comms_list=[]
    if icon!='':
        x=subprocess.Popen(["python","-m","PyInstaller","--onefile","--noconfirm","--name",name,icon,fileloc],cwd=directory)
    else:
        x=subprocess.Popen(["python","-m","PyInstaller","--noconfirm","--name",name,fileloc],cwd=directory)
    comms_list.append(x.communicate())
    return(True)


def file_rewrite(filename):
    with open(filename,'r') as f:
            lines=f.readlines()
    if "/" in filename:
        name=filename.split('/')[-1].split('.')[0]
    else:
        name=filename.split('\\')[-1].split('.')[0]
    if filename.count(name)>1:
        filepath=os.path.join(filename.split(name)[0],name)
    else:
        filepath=filename.split(name)[0]
    if "\\\\" not in filepath:
        filepath=filepath.encode('unicode_escape').decode()
    exclusion="             excludes=['tkinter','sklearn','sqlite3'],\n"
    position=[ix for ix,i in enumerate(lines) if ' excludes=[]' in i][0]
    lines[position]=exclusion
    lines[1]="from kivy_deps import sdl2, glew"
    newlines=[f"exe = EXE(pyz, Tree('{filepath}'),\n",
                         '               a.scripts,\n',
                         '               a.binaries,\n',
                         '               a.zipfiles,\n',
                         '               a.datas,\n',
                         '               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],\n',
                         '               upx=True,\n',
                         f"               name='{name}')\n"]
    start=[ix for ix,i in enumerate(lines) if "exe = EXE" in i][0]
    stop=[ix for ix,i in enumerate(lines) if "coll = COLLECT" in i][0]
    lines=lines[:start]+newlines+lines[stop:]
    with open(filename,'w') as f:
        f.writelines(lines)
def end_exe(file,directory):
    deletions=[fle for fle in os.listdir(directory) if '.' not in fle]
    for delete in deletions:
        delete=os.path.join(directory,delete)
        shutil.rmtree(delete)
    comms_list=[]
    
    x=subprocess.Popen(["python","-m","PyInstaller","--noconfirm",file],cwd=directory)
    comms_list.append(x.communicate())
    return(True)


def main(directory=None):
    if directory:
        directory=directory
    else:
        directory=os.getcwd()
    print("Getting started setting up executable")
    start_exe(directory)
    #assumes that the spec file has been generated at this point
    file=[f for f in os.listdir(directory) if '.spec' in f][0]
    print(f"Rewriting {file} now")
    file_rewrite(os.path.join(directory,file))
    print("Attempting to write standalone executable")
    end_exe(file,directory)
    
if __name__=="__main__":
    main()