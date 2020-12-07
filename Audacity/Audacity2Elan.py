import sys
sys.path.append('../')
import fileinput
from getopt import getopt
from ElanUtils.elan_save import ElanCnvSave
from ElanUtils.sent import ElanCnvSent
from ElanUtils.config import ElanCnvConf

def main(args):
    sentences = []
    confFile = ''
    opts, files = getopt(sys.argv[1:], "c:")
    if len(opts) == 0 or len(files) == 0:
        print ("Usage: Audacity2Elan.py -c configfile file")
        print ("Options and arguments:")
        print ("-c     : configuration file")
        print ("file   : file to convert to Elan")
        return
    for o, a in opts:
        if o == "-c":
            confFile = a
            
    config = ElanCnvConf(confFile)
    config.print()
    
    parts = files[0].split('.')
    elanFilename = files[0]
    if len(parts) > 1:
        elanFilename = elanFilename[:len(elanFilename) - len(parts[len(parts) - 1])]
    elanFilename += "eaf"
    print ("output file: " + elanFilename)
    ElanCnvSave.names[""] = 1
    titles = config.getDefaultTitlesDic(1)
    delim = '\t'
    for line in fileinput.input(files[0]):
        line = line.rstrip()
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        mark = parts[2]
        begin = round(float(parts[0].replace(',','.'))*1000)
        end = round(float(parts[1].replace(',','.'))*1000)

        item = ElanCnvSent(mark, len(sentences), titles, ElanCnvSave.lvlExist, ElanCnvSave.names, begin=begin, end=end)
        sentences.append(item)

    print ("count:", len(sentences))
    es = ElanCnvSave(elanFilename, config)
    es.writeHeader()
    es.writeSentOnlyTimesExt(sentences)
    id = 0
    cur_name = ""
    timeStep = ElanCnvSave.stepType.simple
    id = es.writeFirstTier(id, sentences, cur_name, timeStep)
    es.writeTail()

main(sys.argv)    
