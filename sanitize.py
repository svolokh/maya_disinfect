import os.path
import sys
import tempfile
import shutil

virusNodes = {'vaccine_gene', 'breed_gene'}

if len(sys.argv) <= 1:
    sys.stderr.write('Usage: python {} <input directory> [output directory]\n'.format(sys.argv[0]))
    sys.stderr.write('\t if [output directory] not specified, will just replace files in the same directory\n')
    exit(1)

inputDir = os.path.realpath(sys.argv[1])
if len(sys.argv) > 2:
    outputDir = os.path.realpath(sys.argv[2])
else:
    outputDir = inputDir

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

for dirpath, dirnames, filenames in os.walk(inputDir):
    currentOutputDir = os.path.join(outputDir, dirpath[len(inputDir)+1:])
    if not os.path.exists(currentOutputDir):
        os.mkdir(currentOutputDir)
    for filename in filenames:
        if not filename.lower().endswith('.ma'):
            continue
        inpath = os.path.join(dirpath, filename)
        print('Processing {}'.format(inpath))
        outpath = os.path.join(currentOutputDir, filename)
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