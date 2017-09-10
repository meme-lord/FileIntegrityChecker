# Simple script to get hashes for one or more files
# For directories the script will get checksums for
# all files in subdirectories also.
import hashlib, os, threading
from sys import argv

try:
	script,path = argv
except:
	exit("Usage: python %s FILE_OR_FOLDER" % argv[0])
	
def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return (hasher.hexdigest() if ashexstr else hasher.hexdigest())

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

file_list = []

for root, dirs, files in os.walk(".\\" + path, topdown=False):
	for name in files:
		file_list.append(os.path.join(root, name))

output = []
class myThread(threading.Thread):
	def __init__ (self):
		threading.Thread.__init__(self)
	def run(self):
		while len(file_list)>0:
			fname = file_list.pop(0)
			output.append("%s:%s" % (fname,hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha1())))

threads = []
for i in range(0,10):
	thread = myThread()
	thread.start()
	threads.append(thread)

for thread in threads:
    thread.join()
	
output.sort()
for x in output:
	print(x)
