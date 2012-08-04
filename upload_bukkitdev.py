#!/bin/env python
# Tool to copy given files to specific folder

## CONFIGURATION

dp_dir='/home/tomcat/Dropbox/bukkit_plugins'
bukkitdev_en = True

## IMPORTS

from sys import argv, exit
from lxml import etree
import re
from os import sep, makedirs
from os.path import dirname, basename, exists, isdir, join
from shutil import copy2


## CHECK ARGUMENT VALIDITY

try:
    path = argv[1]
except IndexError:
    print('Give a filename as first argument') 
    exit(-1)

if not exists(path) or isdir(path):
    print("File {path} does not exist\n".format(path=path))
    exit(-1)

pomfile = path.replace('.jar','.pom')

if not exists(pomfile) or isdir(pomfile):
    print("Pomfile {pom} does not exist\n".format(pom=pomfile))
    exit(-1)


## PARSE POM

pom = etree.parse(pomfile)
pomroot = pom.getroot()

roottag = pomroot.tag
nms = re.match("({.*})", roottag).group()

#print(etree.tostring(pomroot))

version  = pomroot.findtext(nms + "version")
groupid  = pomroot.findtext(nms + "groupId")
artifact = pomroot.findtext(nms + "artifactId")

package = groupid + "." + artifact

'''
string = """
File    : {file}
Version : {ver}
Package : {pkg}
GroupID : {group}
Artifact: {artifact}
""".format(file=path, ver=version, pkg=package, group=groupid, artifact=artifact)
print(string)
'''


dependencies = pomroot.find(nms + "dependencies")
for dependency in dependencies.findall(nms + "dependency"):
    print(etree.tostring(dependency))
    if dependency.findtext(nms + "groupId") == "org.bukkit" and dependency.findtext(nms + "artifactId") == "bukkit":
	bukkitver = dependency.findtext(nms + "version")

if not bukkitver:
    bukkitdev_en = false
    print("Can not find bukkit version form pom file, not uploading to bukkitdev")


## DO OTHER STUFF

if file == '' or version == '' or package == '':
    print('Path is not correctly formated')
    exit(-1)

#dir = join(dp_dir,package,version)
#
#if not exists(dir) or not isdir(dir):
#    makedirs(dir)
#
#if not exists(join(dir,file)):
#    copy2(path, dir)
#    print("Copied " + file)
