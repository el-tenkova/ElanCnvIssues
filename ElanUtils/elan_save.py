from ElanUtils.sent import ElanCnvSent
from ElanUtils.config import ElanCnvConf
from enum import Enum

class ElanCnvSave:
    class stepType(Enum):
        simple = 0
        size = 1

    class refType(Enum):
        words = 0
        homs = 1
        rus = 2
        lemma = 3
        partofspeech = 4
        m_rus = 5
        m_eng = 6

    lvlNames = {}
    lvlExist = {}
    names = {}
    
    def __init__(self, filename, config):
        self.filename = filename
        self.eaf = open(filename, "w+", encoding='utf8')
        for tier in config.config['tiers']:
            ElanCnvSave.lvlNames[tier] = config.config['tiers'][tier]
        
    def writeHeader(self):
        self.eaf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.eaf.write('<ANNOTATION_DOCUMENT AUTHOR="unspecified" DATE="2015-04-09T12:42:10+04:00" FORMAT="2.8" VERSION="2.8" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv2.8.xsd">\n')
        self.eaf.write('<HEADER MEDIA_FILE="" TIME_UNITS="milliseconds">\n')
        self.eaf.write('</HEADER>\n')

    def writeTail(self):
        self.eaf.write('<LINGUISTIC_TYPE GRAPHIC_REFERENCES = "false" LINGUISTIC_TYPE_ID="paragraph" TIME_ALIGNABLE="true" />\n')
        self.eaf.write('<LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Association" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="association" TIME_ALIGNABLE="false" />\n')
        self.eaf.write('<LINGUISTIC_TYPE CONSTRAINTS="Symbolic_Subdivision" GRAPHIC_REFERENCES="false" LINGUISTIC_TYPE_ID="subdivision" TIME_ALIGNABLE="false" />\n')
        self.eaf.write('<CONSTRAINT DESCRIPTION="Time subdivision of parent annotation\'s time interval, no time gaps allowed within this interval\" STEREOTYPE="Time_Subdivision" />\n')
        self.eaf.write('<CONSTRAINT DESCRIPTION="Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered" STEREOTYPE="Symbolic_Subdivision" />\n')
        self.eaf.write('<CONSTRAINT DESCRIPTION="1-1 association with a parent annotation" STEREOTYPE="Symbolic_Association" />\n')
        self.eaf.write('<CONSTRAINT DESCRIPTION="Time alignable annotations within the parent annotation\'s time interval, gaps are allowed" STEREOTYPE="Included_In" />\n')
        self.eaf.write('<LOCALE COUNTRY_CODE="RU" LANGUAGE_CODE="ru"/>\n')
        self.eaf.write('</ANNOTATION_DOCUMENT>\n')
        self.eaf.close()
            
    def writeTimeSlot(self, idx, begin):
        self.eaf.write('<TIME_SLOT TIME_SLOT_ID="ts')
        self.eaf.write(str(idx))
        self.eaf.write('" TIME_VALUE="')
        self.eaf.write(str(begin))
        self.eaf.write('" />\n')

    def writeTierHeader(self, name, tiertype, parent, participant):
        self.eaf.write('<TIER DEFAULT_LOCALE="ru" LINGUISTIC_TYPE_REF="')
        self.eaf.write(tiertype)
        self.eaf.write('" TIER_ID="')
        self.eaf.write(name)
        self.eaf.write('"')
        if (len(parent) > 0):
            self.eaf.write(' PARENT_REF="')
            self.eaf.write(parent)
            self.eaf.write('"')
        if (len(participant) > 0):
            self.eaf.write(' PARTICIPANT="')
            self.eaf.write(participant)
            self.eaf.write('"')
        self.eaf.write(' >\n')

    def writeTierTail(self):
        self.eaf.write('</TIER>\n')

    def writeAnno(self, sent, idx, time1, time2):
        self.eaf.write('<ANNOTATION>\n')
        self.eaf.write('<ALIGNABLE_ANNOTATION ANNOTATION_ID="a');
        self.eaf.write(str(idx))
        self.eaf.write('" TIME_SLOT_REF1="ts')
        self.eaf.write(str(time1))
        self.eaf.write('" TIME_SLOT_REF2="ts')
        self.eaf.write(str(time2))
        self.eaf.write('" >\n')
        self.eaf.write('<ANNOTATION_VALUE>')
        self.eaf.write(sent)
        self.eaf.write('</ANNOTATION_VALUE>\n')
        self.eaf.write('</ALIGNABLE_ANNOTATION>\n')
        self.eaf.write('</ANNOTATION>\n')

    def writeRefAnno(self, sent, idx, refid, previous):
        self.eaf.write('<ANNOTATION>\n')
        self.eaf.write('<REF_ANNOTATION ANNOTATION_ID="a')
        self.eaf.write(str(idx))
        self.eaf.write('" ANNOTATION_REF="a')
        self.eaf.write(str(refid))
        if previous != -1:
            self.eaf.write('" PREVIOUS_ANNOTATION="a')
            self.eaf.write(str(previous))
        self.eaf.write('" >\n')
        self.eaf.write('<ANNOTATION_VALUE>')
        self.eaf.write(sent)
        self.eaf.write('</ANNOTATION_VALUE>\n')
        self.eaf.write('</REF_ANNOTATION>\n')
        self.eaf.write('</ANNOTATION>\n')
        

    def writeTimes(self, sentences):
        idx = 1
        begin = 0
        self.eaf.write('<TIME_ORDER>\n')
        for item in sentences:
            for i in range(0, item.size):
                writeTimeSlot(ef, idx, begin)
                begin += 500;
                idx += 1;
        for i in range(0, 20):
            writeTimeSlot(self, idx, begin)
            begin += 500
            idx += 1
        self.eaf.write('</TIME_ORDER>\n')

    def writeSentOnlyTimes(self, sentences):
        idx = 1
        begin = 0
        self.eaf.write('<TIME_ORDER>\n')
        for item in sentences:
            self.writeTimeSlot(idx, begin);
            idx += 1
            begin += 5000
            self.writeTimeSlot(idx, begin)
            idx += 1
        for i in range(0, 2):
            self.writeTimeSlot(idx, begin)
            begin += 5000
            idx += 1
        self.eaf.write('</TIME_ORDER>\n')
        
    def writeSentOnlyTimesExt(self, sentences):
        idx = 1
        begin = 0
        self.eaf.write('<TIME_ORDER>\n')
        for item in sentences:
            self.writeTimeSlot(idx, item.begin);
            idx += 1
            self.writeTimeSlot(idx, item.end);
            idx += 1
        begin = sentences[len(sentences) -1].end;
        for i in range(0, 2):
            self.writeTimeSlot(idx, begin)
            begin += 5000
            idx += 1
        self.eaf.write('</TIME_ORDER>\n')

    #unsigned long long writeKhakSent(std::wofstream& ef, unsigned long long& id, const stepType timeStep);
    def writeFirstTier(self, id, sentences, cur_name, timeStep):
        time1 = 1;
        time2 = 1;
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Sent]
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            if ElanCnvConf.Transcr in ElanCnvSave.lvlExist:
                lvlName = ElanCnvSave.lvlNames[ElanCnvSave.Transcr]
            elif ElanCnvConf.Rus_Sent in ElanCnvSave.lvlExist:
                lvlName = ElanCnvSent.lvlNames[ElanCnvConf.Rus_Sent]
            else:
                return id
        refLvlName = ""
        lvlName, refLvlName = self.appendName(cur_name, lvlName, refLvlName)
        self.writeTierHeader(lvlName, "paragraph", "", cur_name)

        for item in sentences:
            if timeStep == ElanCnvSave.stepType.simple:
                time2 = time1 + 1
            else:
                time2 = time1 + item.size;
            if item.informant == cur_name:
                if ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
                    self.writeAnno(item.src_sent, id, time1, time2)
                elif ElanCnvConf.Transcr in ElanCnvSave.lvlExist:
                    self.writeAnno(item.transcr, id, time1, time2)
                else:
                    self.writeAnno(item.rus_sent, id, time1, time2)
                item.id = id
                id = id + 1
                item.time1 = time1
                item.time2 = time2
            time1 = time2 + 1
        self.writeTierTail()
        return id
        
    def writeRusSent(self, id, sentences, cur_name):
        if not ElanCnvConf.Rus_Sent in ElanCnvSave.lvlExist:
            return id
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist and not ElanCnvConf.Transcr in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Rus_Sent]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Sent]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "association", khLvlName, cur_name)
        previous = -1
        for sent in sentences:
            if sent.informant == cur_name:
                self.writeRefAnno(sent.rus_sent, id, sent.id, previous)
                id = id + 1
        self.writeTierTail()
        return id
        
    def writeTranscription(self, id, sentences, cur_name):
        print (ElanCnvSave.lvlExist)
        if not ElanCnvConf.Transcr in ElanCnvSave.lvlExist:
            return id
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Transcr]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Sent]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "association", khLvlName, cur_name)

        previous = -1
        for sent in sentences:
            if sent.informant == cur_name:
                self.writeRefAnno(sent.transcr, id, sent.id, previous)
                id = id + 1
        self.writeTierTail()
        return id

    #unsigned long long writeWords(std::wofstream& ef, unsigned long long& id);
    #unsigned long long writeKhakHoms(std::wofstream& ef, unsigned long long& id);
    def writeWordsAsRef(self, id, refid, sentences, cur_name):
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Words]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Sent]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "subdivision", khLvlName, cur_name)
        id = self.writeRefTier(id, refid, ElanCnvSave.refType.words, sentences, None, cur_name)
        self.writeTierTail()
        return id

    def writeKhakHomsAsRef(self, id, refid, sentences, cache, cur_name):
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Homonyms]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Words]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "subdivision", khLvlName, cur_name)
        id = self.writeRefTier(id, refid, ElanCnvSave.refType.homs, sentences, cache, cur_name)
        self.writeTierTail()
        return id

    def writeRefTier(self, id, _refid, reftype, sentences, cache, cur_name):
        sentid = _refid;
        wordid = _refid;
        for sent in sentences:
            if sent.informant == cur_name:
                if reftype == ElanCnvSave.refType.homs:
                    sent.firstHomId = id
                refid = sent.firstHomId
                previous = -1
                for word in sent.words:
                    if reftype == ElanCnvSave.refType.words:
                        self.writeRefAnno(word, id, sentid, previous)
                        previous = id
                        id = id + 1
                        continue
                    if cache == None:
                        continue
                    normWord = sent.keys[word]
                    if normWord in cache:
                        homonyms = cache[normWord][1]
                        for hom in homonyms:
                            if reftype == ElanCnvSave.refType.homs:
                                self.writeRefAnno(hom.src, id, wordid, previous)
                                previous = id
                                id = id + 1
                            elif reftype == ElanCnvSave.refType.rus:
                                self.writeRefAnno(hom.rus, id, refid, previous)
                                id = id + 1
                                refid = refid + 1
                            elif reftype == ElanCnvSave.refType.lemma:
                                self.writeRefAnno(hom.lemma, id, refid, previous)
                                id = id + 1
                                refid = refid + 1
                            elif reftype == ElanCnvSave.refType.partofspeech:
                                self.writeRefAnno(hom.pos, id, refid, previous)
                                id = id + 1
                                refid = refid + 1

#                            case m_eng:
#                            case m_rus:
#                            {
#                                for (auto mit = vt->r_morphems.begin(); mit != vt->r_morphems.end(); ++mit) {
#                                    writeRefAnno(ef, (*mit), id, refid, previous);
#                                    id++;
#                                    refid++;
#                                }
#                                break;
#                            }
                    wordid = wordid + 1
                    previous = -1
                sentid = sentid + 1
        return id
        
    
    def writeRusHoms(self, id, refid, sentences, cache, cur_name):
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Rus_Homonyms]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Homonyms]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "association", khLvlName, cur_name)
        id = self.writeRefTier(id, refid, ElanCnvSave.refType.rus, sentences, cache, cur_name)
        self.writeTierTail()
        return id

    #unsigned long long writeEngHoms(std::wofstream& ef, unsigned long long& id, unsigned long long& refid);
    def writeLemma(self, id, refid, sentences, cache, cur_name):
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Lemma]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Homonyms]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "association", khLvlName, cur_name)
        id = self.writeRefTier(id, refid, ElanCnvSave.refType.lemma, sentences, cache, cur_name)
        self.writeTierTail()
        return id

    def writePartOfSpeech(self, id, refid, sentences, cache, cur_name):
        if not ElanCnvConf.Src_Sent in ElanCnvSave.lvlExist:
            return id
        lvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_PartOfSpeech]
        khLvlName = ElanCnvSave.lvlNames[ElanCnvConf.Src_Homonyms]
        lvlName, khLvlName = self.appendName(cur_name, lvlName, khLvlName)
        self.writeTierHeader(lvlName, "association", khLvlName, cur_name)
        id = self.writeRefTier(id, refid, ElanCnvSave.refType.partofspeech, sentences, cache, cur_name)
        self.writeTierTail()
        return id

    #unsigned long long writeKhakMorphems(std::wofstream& ef, unsigned long long& id);
    #unsigned long long writeRusMorphems(std::wofstream& ef, unsigned long long& id, unsigned long long& refid);
    #unsigned long long writeEngMorphems(std::wofstream& ef, unsigned long long& id, unsigned long long& refid);
    def appendName(self, cur_name, lvlName, refLvlName):
        if len(cur_name) != 0:
            lvlName = cur_name + "_" + lvlName;
            if len(refLvlName) != 0:
                refLvlName = cur_name + "_" + refLvlName
        return lvlName, refLvlName
    
    def calcSentTime(self, sentences):
        for name in ElanCnvSave.names:
            idx = 0
            prevIdx = len(sentences)
            for sent in sentences:
                if sent.informant != name:
                    idx = idx + 1
                    continue
                if idx != prevIdx and prevIdx != len(sentences):
                    if sent.begin == sentences[prevIdx].begin:
                        sent.begin = sent.begin + 300
                    sentences[prevIdx].end = sent.begin;
                    if sentences[prevIdx].end - sentences[prevIdx].begin > 10000:
                        sentences[prevIdx].end = sentences[prevIdx].begin + 10000
                prevIdx = idx
                idx = idx + 1
            if prevIdx != len(sentences):
                sentences[prevIdx].end = sentences[prevIdx].begin + 10000;

