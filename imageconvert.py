import glob
import os
from subprocess import Popen, PIPE


def isImageValid(file):
    return os.stat(file).st_size == 11184952


def delete(file):
    os.remove(file)
    print('Discarded', file)


def process(file):
    ddsfile = file.replace('jpg', 'dds')
    if os.path.isfile(ddsfile):
        if isImageValid(ddsfile):
            delete(file)
        else:
            delete(ddsfile)


def postprocess(file):
    ddsfile = file.replace('jpg', 'dds')
    if os.path.isfile(ddsfile):
        if isImageValid(ddsfile):
            delete(file)
        else:
            print(file, 'failed to convert properly')
    else:
        print(file, 'didn\'t convert at all')


dirlist = glob.glob('*.jpg')
count = len(dirlist)
print(count)
for img in dirlist:
    process(img)

command = 'texconv -m 13 -gpu 1 -timing -f BC1_UNORM *.jpg'
print(command)
os.system(command)
dirlist = glob.glob('*.jpg')
for img in dirlist:
    postprocess(img)
