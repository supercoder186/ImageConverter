from subprocess import Popen, PIPE
import glob
import os


def isImageValid(file):
    proc = Popen(['identify', '-verbose', file], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return str(exitcode) == '0' and str(err, 'utf-8') == ''


def delete(file):
    os.remove(file)
    print('Discarded', file)


def append_to_list(img_file_name):
    list_file.write(img_file_name)
    list_file.flush()


def process(file):
    ddsfile = file.replace('jpg', 'dds')
    if os.path.isfile(ddsfile):
        if isImageValid(ddsfile):
            delete(file)
        else:
            delete(ddsfile)
            append_to_list(file)
    else:
        append_to_list(file)


list_file = open('file', 'w')
dirlist = glob.glob('*.jpg')
count = len(dirlist)
print(count)
for img in dirlist:
    process(img)

list_file.close()
