import os.path
import sys
import tempfile
import shutil

virusNodes = {'vaccine_gene', 'breed_gene'}

def sanitize(inpath, outpath):
    handle, temp = tempfile.mkstemp()
    out = os.fdopen(handle, 'w')
    virusDetected = False
    with open(inpath, 'r') as f:
        line = f.readline()
        while True:
            if len(line) == 0:
                break
            lineLower = line.lower()
            if lineLower.startswith('createnode') and len(list(filter(lambda nodeName: lineLower.find(nodeName) >= 0, virusNodes))) > 0:
                print('\tFound virus node: {}'.format(line.strip()))
                virusDetected = True
                while True:
                    line = f.readline()
                    if not line.startswith('\t'):
                        break
            else:
                out.write(line)
                line = f.readline()
        out.close()
    if virusDetected:
        shutil.move(temp, outpath)
    else:
        os.remove(temp)
    return virusDetected