from wand import image
from subprocess import Popen, PIPE
import glob
import os
import queue
import threading


def isImageValid(file):
    proc = Popen(['identify', '-verbose', file], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return str(exitcode) == '0' and str(err, 'utf-8') == ''


def delete(file):
    os.remove(file)
    print('Discarded', file)


def doConvert(file):
    global write_q, q, write_lock
    ddsfile = file.replace('jpg', 'dds')
    img = image.Image(filename=file)
    img.compression = "dxt3"
    write_lock.acquire()
    write_q.put((ddsfile, img))
    write_lock.release()
    print('Converted', file)
    delete(file)
    print("Number of files left:", q.qsize())


def process(file):
    ddsfile = file.replace('jpg', 'dds')
    if os.path.isfile(ddsfile):
        if isImageValid(ddsfile):
            delete(file)
        else:
            delete(ddsfile)
            doConvert(file)
    else:
        doConvert(file)


def process_data(id):
    global q
    while not exit:
        if not q.empty():
            qLock.acquire()
            file = q.get()
            qLock.release()
            print("Thread #%s processing %s" % (id, file))
            process(file)


def write_data():
    global write_q, write_lock
    while not exit:
        if not write_q.empty():
            write_lock.acquire()
            file, img = write_q.get()
            write_lock.release()
            print("Writing file %s" % file)
            img.save(filename=file)


class converter(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        print("Starting thread #%s" % self.id)
        process_data(self.id)
        print("Closing Thread #%s" % self.id)


class writer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Starting write thread')
        write_data()
        print('Closing write thread')


exit = 0
dir = glob.glob('*.jpg')
count = len(dir)
print(count)
q = queue.Queue()
write_q = queue.Queue()
qLock = threading.Lock()
write_lock = threading.Lock()
qLock.acquire()
threads = []

for f in dir:
    q.put(f)

qLock.release()

thread_count_s = input('Number of threads (default 1): ')
if thread_count_s:
    thread_count = int(thread_count_s)
else:
    thread_count = 1

for i in range(thread_count):
    thread = converter(i)
    thread.start()
    threads.append(thread)

writer = writer()
writer.start()
threads.append(writer)

while not (q.empty() and write_q.empty()):
    pass

exit = 1
for t in threads:
    t.join()

print("Batch convert completed")
