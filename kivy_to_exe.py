# -*- coding: utf-8 -*-
"""
Created on Fri May 14 06:47:43 2021

@author: shane
"""
import os
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
        x=subprocess.Popen(["python","-m","PyInstaller","--name",name,icon,fileloc],cwd=directory)
    else:
        x=subprocess.Popen(["python","-m","PyInstaller","--name",name,fileloc],cwd=directory)
    comms_list.append(x.communicate())
    return(True)


def file_rewrite(filename):
    with open(filename,'r') as f:
            lines=f.readlines()
    lines[1]="from kivy_deps import sdl2, glew"
    for ix,line in enumerate(lines):
        if line=="          [],":
            lines[ix]=="          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],"
    with open(filename,'w') as f:
        f.writelines(lines)
def end_exe(file,directory):
    comms_list=[]
    x=subprocess.Popen(["python","-m","PyInstaller",file],cwd=directory)
    comms_list.append(x.communicate())
    return(True)


def main(directory=None):
    if directory:
        directory=directory
    else:
        directory=os.getcwd()
    start_exe(directory)
    #assumes that the spec file has been generated at this point
    file=[f for f in os.listdir(directory) if '.spec' in f][0]
    file_rewrite(os.path.join(directory,file))
    end_exe(file,directory)