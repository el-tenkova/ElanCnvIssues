import string
import requests
import re
from ElanUtils.homonym import ElanCnvHom

class ElanCnvParse:

    rgx = re.compile('%s' % '-+')
    
    def __init__(self, parserReq):
        self.request = parserReq

    def doParse(self, normWord):
        print (self.request + normWord)
        r = requests.get(self.request + normWord)
        if r.status_code == 200:
            #print (r.text)
            resp = r.text
            foundStem = "FOUND STEM: "
            homonyms = []
            #hom homonym;
            pos = resp.find(foundStem)
            while pos != -1:
                resp = resp[pos + len(foundStem):]
                # grammatics
                form = self.getDetails(resp, ' ')
                print ("form = ", form)
                # affixes
                affixes = self.getDetails(resp[resp.find(' '):], chr(0xA))
                print ("affixes =", affixes)
                # part of speech
                pos = resp.find(chr(0xA))
                if pos == -1:
                    continue
                resp = resp[pos + 1:]
                ps = self.getSubstr(resp, ' ')
                print ("part of speech =", ps)
                # headword
                pos = resp.find(' ')
                if pos == -1:
                    continue
                resp = resp[pos + 1:]
                headword = self.getSubstr(resp, ' ')
                print ("headword =", headword)
                # meaning
                posPoss = resp.find("<+poss>")
                pos = resp.find(chr(0x201B))
                if pos == -1:
                    continue
                if posPoss != -1 and posPoss > pos:
                    posPoss = -1
                resp = resp[pos + 1:]
                meaning = self.getSubstr(resp, chr(0x2019))
                print ("meaning =", meaning)
                pos = resp.find(chr(0x2019))
                resp = resp[pos + 1:]
                stem = self.getSubstr(resp, chr(0xA))
                if len(stem) > 0 and (str(stem[0])).isdigit():
                    stem = ""
                if len(stem) > 0:
                    posSpace = stem.find(' ')
                    if posSpace != -1:
                        stem = stem[:posSpace]
                print ("stem =", stem)
                hom = ElanCnvHom(stem, headword, meaning, affixes, posPoss, form, ps)
                homonyms.append(hom)
                pos = resp.find(foundStem)
        return homonyms
    
    def getDetails(self, fromStr, endCh):
        pos = fromStr.find(endCh)
        if pos == -1:
            return ""
        aff = fromStr[:pos]
        aff = aff.strip(' ')
        aff = ElanCnvParse.rgx.sub("-", aff)
        aff = aff.strip('-')
        return aff

    def getSubstr(self, fromStr, endCh):
        headWord = fromStr.lstrip(' ')
        pos = headWord.find(endCh)
        if pos == -1:
            return "-"
        return headWord[:pos]
    
