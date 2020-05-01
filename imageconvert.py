import glob
import os


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


def process_output(output):
    output = output.replace('\n\n', '\n').split('\n')
    output = [x for x in output if x]
    for i in range(len(output)):
        if output[i]:
            output[i] = output[i].strip()

    output.remove('Name')
    return output


dirlist = glob.glob('*.jpg')
count = len(dirlist)
print('There are %s jpg files to convert' % count)
for img in dirlist:
    process(img)

gpu_cmd_output = os.popen('wmic path win32_VideoController get name').read()
gpu_list = process_output(gpu_cmd_output)
for i in range(len(gpu_list)):
    print(gpu_list[i], '->', i)

index = int(input('Enter the index of the GPU you wish to use: '))
command = 'texconv -m 13 -gpu %s -timing -f BC1_UNORM *.jpg' % index
os.system(command)
dirlist = glob.glob('*.jpg')
for img in dirlist:
    postprocess(img)
