import os.path
import sys
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..'))
import fileinput
from getopt import getopt
from ElanUtils.elan_save import ElanCnvSave
from ElanUtils.sent import ElanCnvSent
from ElanUtils.config import ElanCnvConf
from ElanUtils.parse import ElanCnvParse

def main(args):
    sentences = []
    confFile = ''
    withTitle = False
    parse = True
    opts, files = getopt(sys.argv[1:], "c:tn")
    if len(opts) == 0 or len(files) == 0:
        print ("Usage: Txt2Elan.py -c configfile [-t] [-n] file")
        print ("Options and arguments:")
        print ("-c     : configuration file")
        print ("-t     : first line in file contains title")
        print ("-n     : don't parse, save to Elan only")
        print ("file   : file to convert to Elan")
        return
    for o, a in opts:
        if o == "-c":
            confFile = a
        elif o == "-t":
            withTitle = True
        elif o == "-n":
            parse = False
            
    config = ElanCnvConf(confFile)
    config.print()
    
    parts = files[0].split('.')
    elanFilename = files[0]
    dictFilename = files[0] + "_dict.txt"
    notFoundFileName = files[0] + "_notfound.txt"
    if len(parts) > 1:
        elanFilename = elanFilename[:len(elanFilename) - len(parts[len(parts) - 1])]
    elanFilename += "eaf"
    print ("output file: " + elanFilename)
    f = open(files[0], "rt", encoding="utf-8-sig")
    lines = [line.strip() for line in f]
    f.close()

    #parse
    titles = {}
    start = 0
    numLine = len(lines)
    delim = config.getDelimeter()
    if withTitle:
        titles = config.getTitlesDic(lines[0])
        ok = False
        for idx in titles:
            if titles[idx] == 'src':
                ok = True
                break
        if ok == False:
            print ("Error: cannot find SRC column")
            exit()
        start = 1
        print (titles)
    else:
        col_num = 0
        for idx in range(start, numLine):
            line = lines[idx].rstrip()
            if not len(line):
                continue
            parts = line.split(delim)
            if len(parts) > col_num:
                col_num = len(parts)
        if col_num > 3:
            print ("Error: too much columns, add title line")
            exit()

        titles = config.getDefaultTitlesDic(col_num)
    if not "name" in titles:
        ElanCnvSave.names[""] = 1
        
    parserReq = config.getParserRequest()
    for idx in range(start, numLine):
        line = lines[idx].rstrip()
        if not len(line):
            continue
    
        item = ElanCnvSent(line, len(sentences), titles, ElanCnvSave.lvlExist, ElanCnvSave.names, delim=delim)
        item.print()
        sentences.append(item)
        #if idx == 4:
        #    break

    empty = {}
    cache = {}
    parser = ElanCnvParse(parserReq)
    for s in sentences:
        for word in s.keys:
            normWord = s.keys[word]
            if normWord in empty:
                empty[normWord] = empty[normWord] + 1
                continue
            if normWord in cache:
                cache[normWord][0] = cache[normWord][0] + 1
                continue
            if parse:
                homonyms = parser.doParse(normWord)
                if not len(homonyms):
                    empty[normWord] = 1
                else:
                    cache[normWord] = [1, homonyms]
                    for hom in homonyms:
                        hom.print()

    #save to eaf
    es = ElanCnvSave(elanFilename, config)
    es.writeHeader()
    es.calcSentTime(sentences)
    if withTitle:
        es.writeSentOnlyTimesExt(sentences)
    else:
        es.writeSentOnlyTimes(sentences)
    
    id = 0
    cur_name = ""
    timeStep = ElanCnvSave.stepType.simple
    for i in range(1, len(ElanCnvSave.names) + 1):
        for name in ElanCnvSave.names:
            if i == ElanCnvSave.names[name]:
                cur_name = name
                break
        refid = id
        id = es.writeFirstTier(id, sentences, cur_name, timeStep)
        id = es.writeTranscription(id, sentences, cur_name)
        refidWords = id
        id = es.writeWordsAsRef(id, refid, sentences, cur_name)
        id = es.writeKhakHomsAsRef(id, refidWords, sentences, cache, cur_name)
        id = es.writeLemma(id, refidWords, sentences, cache, cur_name)
        id = es.writePartOfSpeech(id, refidWords, sentences, cache, cur_name)
        id = es.writeRusHoms(id, refid, sentences, cache, cur_name)
        id = es.writeRusSent(id, sentences, cur_name)
    es.writeTail()

    #save dict and notFound
    dictionary = open(dictFilename, "w+", encoding='utf8')
    keys = sorted(cache, key=lambda key : key)
    for item in keys:
        dictionary.write(item + ":\t" + str(cache[item][0]) + ":\t")
        for hom in cache[item][1]:
            dictionary.write(hom.src + " : " + hom.rus + ";")
        dictionary.write("\n")
    dictionary.close()
    
    notfound = open(notFoundFileName, "w+", encoding='utf8')
    keys = sorted(empty, key=lambda key : key)
    for item in keys:
        notfound.write(item + " : " + str(empty[item]) + "\n")
    notfound.close()                       

main(sys.argv)    
