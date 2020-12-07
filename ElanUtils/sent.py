import string
import re
from ElanUtils.config import ElanCnvConf

class ElanCnvSent:
    repl = {ord('a')      : '\u0430',
            ord('c')      : '\u0441',
            ord('e')      : '\u0435',
            ord('i')      : '\u0456',
            ord('o')      : '\u043E',
            ord('p')      : '\u0440',
            ord('x')      : '\u0445',
            ord('y')      : '\u0443',
            ord('\xF6')   : '\u04E7',
            ord('\xFF')   : '\u04F1',
            ord('\u04B7') : '\u04CC' }

    rgx = re.compile('[%s]' % ',|\.|\:|\;|\!|\?|\'|\"|-|\“|\”|\(|\)|\{|\}|\<|\>|=|_|\+|…|–')

    def __init__(self, line, sentencesSize, titles, lvlExist, names, begin=0, end=0, delim="\x01"):
        self.size = 0 # суммарное количество омонимов в предложении (если слово не парсировано +1)
        self.src_sent = '' # предложение на языке источника
        self.rus_sent = '' # русское предложение
        self.transcr = '' # транскрипция
        self.words = []
        self.keys = {}
        self.informant = '' # имя участника разговора
        self.begin = begin # время начала предложения
        self.end = end # время конца предложения
        self.id = 0 # индекс хакасского предложения
        self.firstHomId = 0 # индекс первого омонима (для соотв. русских ref)
        self.time1 = 0 # начало разговора
        self.time2 = 0 # конец разговора
        parts = line.split(delim)
        if len(titles):
            for title in titles:
                if titles[title] == 'src':
                    self.src_sent = parts[title].strip()
                    lvlExist[ElanCnvConf.Src_Sent] = 1
                elif titles[title] == 'rus':
                    self.rus_sent = parts[title].strip()
                    lvlExist[ElanCnvConf.Rus_Sent] = 1
                elif titles[title] == 'time':
                    time = parts[title].strip()
                    minutes = int(time[:time.find('.')])
                    seconds = int(time[time.find('.') + 1:])
                    self.begin = (minutes * 60 + seconds) * 1000
                elif titles[title] == 'name':
                    self.informant = parts[title].strip()
                    if not self.informant in names:
                        names[self.informant] = len(names) + 1
                elif titles[title] == 'transcription':
                    self.transcr = parts[title].strip()
                    lvlExist[ElanCnvConf.Transcr] = 1
            
        if self.begin == 0 and sentencesSize > 0:
            self.begin = sentencesSize * 5000;
        self.src_sent.replace('\x1f', "")
        self.splitSent()

    def splitSent(self):
        # разбить на слова
        words = self.src_sent.split(" ")
        for word in words:
            word = ElanCnvSent.rgx.sub("", word)
            if "-" in word:
                subwords = word.split("-")
                for item in subwords:
                    self.words.append(item)
                    normWord = self.normalizeWord(item)
            else:
                self.words.append(word)
                normWord = self.normalizeWord(word)

    def normalizeWord(self, word):
        normWord = word.lower()
        normWord = normWord.translate(ElanCnvSent.repl)
        if not word in self.keys:
            self.keys[word] = normWord
        return normWord

    def print(self):
        print(self.size)
        print(self.src_sent)
        print(self.rus_sent)
        print(self.transcr)
        print(self.words)
        print(self.keys)
        print(self.informant)
        print(self.begin)
        print(self.end)
        print(self.id)
        print(self.firstHomId)
        print(self.time1)
        print(self.time2)

        
