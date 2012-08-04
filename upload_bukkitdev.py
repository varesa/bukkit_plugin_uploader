#!/bin/env python
# Tool to copy given files to specific folder

## Conf

dp_dir='/home/tomcat/Dropbox/bukkit_plugins'

##

from sys import argv, exit
from lxml import etree
import re
from os import sep, makedirs
from os.path import dirname, basename, exists, isdir, join
from shutil import copy2


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



pom = etree.parse(pomfile)
pomroot = pom.getroot()

roottag = pomroot.tag
nms = re.match("({.*})", roottag).group()

print(etree.tostring(pomroot))

version  = pomroot.find(nms + "version").text
groupid  = pomroot.find(nms + "groupId").text
artifact = pomroot.find(nms + "artifactId").text

package = groupid + "." + artifact

string = """
File    : {file}
Version : {ver}
Package : {pkg}
GroupID : {group}
Artifact: {artifact}
""".format(file=path, ver=version, pkg=package, group=groupid, artifact=artifact)
print(string)




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
