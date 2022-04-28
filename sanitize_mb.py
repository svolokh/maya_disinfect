import maya.standalone
import os
import os.path
import sys
from san_common import sanitize

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

maya.standalone.initialize(name='python')

from maya import cmds

for dirpath, dirnames, filenames in os.walk(inputDir):
    currentOutputDir = os.path.join(outputDir, dirpath[len(inputDir)+1:])
    if not os.path.exists(currentOutputDir):
        os.mkdir(currentOutputDir)
    for filename in filenames:
        if not filename.lower().endswith('.mb'):
            continue
        print('Processing {}'.format(filename))
        inpath = os.path.join(dirpath, filename)
        mapath = os.path.join(currentOutputDir, os.path.splitext(filename)[0] + '.ma')
        cmds.file(inpath, open=True, executeScriptNodes=False) # prevent any malicious code from running on load by setting executeScriptNodes=False
        cmds.file(rename=mapath)
        cmds.file(save=True, type='mayaAscii')
        if not sanitize(mapath, mapath):
            os.remove(mapath)