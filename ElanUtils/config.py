import fileinput
class ElanCnvConf:

    Src_Sent = "Src_Sent"
    Transcr = "Transcr"
    Src_Words = "Src_Words"
    Src_Homonyms = "Src_Homonyms"
    Src_Lemma = "Src_Lemma"
    Src_PartOfSpeech = "Src_PartOfSpeech"
    Src_Morphems = "Src_Morphems"
    Rus_Morphems = "Rus_Morphems"
    Eng_Morphems = "Eng_Morphems"
    Rus_Homonyms = "Rus_Homonyms"
    Eng_Homonyms = "Eng_Homonyms"
    Rus_Sent = "Rus_Sent"

    tiers = {Src_Sent : 1,
             Transcr : 1,
             Src_Words : 1,
             Src_Homonyms : 1,
             Src_Lemma : 1,
             Src_PartOfSpeech : 1,
             Src_Morphems : 1,
             Rus_Morphems : 1,
             Eng_Morphems : 1,
             Rus_Homonyms : 1,
             Eng_Homonyms : 1,
             Rus_Sent : 1}
    columns = {'src' : 1,
               'rus' : 1,
               'time' : 1,
               'name' : 1,
               'transcription' : 1}
    parameters = {'request' : 1,
                  'delim' : 1}
    
    def __init__(self, conffile):
        self.config = {'tiers' : {}, 'columns' : {}, 'parameters' : {}}
        self.setDefault()
        if len(conffile) > 0:
            for line in fileinput.input(conffile):
                line = line.rstrip()
                parts = line.split(":")
                if len(parts) != 2:
                    continue
                key = parts[0].rstrip().lstrip()
                value = parts[1].rstrip().lstrip()
                if key in ElanCnvConf.parameters:
                    self.config['parameters'][key] = value
                elif key in ElanCnvConf.tiers:
                    self.config['tiers'][key] = value
                elif key in ElanCnvConf.columns:
                    if key == 'src':
                        langs = value.split(',')
                        if len(langs) > 0:
                             self.config['columns']['src'] = []
                        for lang in langs:
                            lang = lang.strip()
                            self.config['columns']['src'].append(lang)
                    else:
                        self.config['columns'][key] = value

    def setDefault(self):
        # названия слоёв
        self.config['tiers'][ElanCnvConf.Src_Sent] = 'Transcription-txt-src'
        self.config['tiers'][ElanCnvConf.Transcr] = 'Phonetic-txt-src'
        self.config['tiers'][ElanCnvConf.Src_Words] = 'Words-txt-src'
        self.config['tiers'][ElanCnvConf.Src_Homonyms] = 'Morph-txt-src'
        self.config['tiers'][ElanCnvConf.Src_Lemma] = 'Lemma-txt-src'
        self.config['tiers'][ElanCnvConf.Src_PartOfSpeech] = 'POS-txt-en'
        self.config['tiers'][ElanCnvConf.Src_Morphems] = 'mb'
        self.config['tiers'][ElanCnvConf.Rus_Morphems] = 'gr'
        self.config['tiers'][ElanCnvConf.Eng_Morphems] = 'ge'
        self.config['tiers'][ElanCnvConf.Rus_Homonyms] = 'Gloss-txt-rus'
        self.config['tiers'][ElanCnvConf.Eng_Homonyms] = 'Gloss-txt-en'
        self.config['tiers'][ElanCnvConf.Rus_Sent] = 'Translation-gls-rus'
        # название колонок входного файла
        self.config['columns']['src'] = ['src']
        self.config['columns']['rus'] = 'rus'
        self.config['columns']['time'] = 'time'
        self.config['columns']['name'] = 'name'
        self.config['columns']['transcription'] = 'transcription'
        # настройки
        self.config['parameters']['request'] = 'https://khakas.altaica.ru/suddenly/?parse='
        self.config['parameters']['delim'] = '|' # разделитель по умолчанию

    def print(self):
        print ()
        print ("current configuration:")
        for key in self.config:
            print ("=========",key,"=========")
            maxl = len(max(self.config[key], key=len))
            fmt = "{:<" + str(maxl) + "}"
            for key1 in self.config[key]:
                print (fmt.format(key1), ":", self.config[key][key1])
        print ()

    def getTitlesDic(self, line):
        titles = {}
        parts = line.split(self.config['parameters']['delim'])
        if len(parts) > 1:
            idx = 0
            for part in parts:
                part = part.strip()
                if not len(part):
                    continue
                for name in self.config['columns']:
                    if self.config['columns'][name] == part:
                        titles[idx] = name
                    elif name == 'src':
                        if part in self.config['columns']['src']:
                             titles[idx] = name
                idx = idx + 1
        return titles

    def getDefaultTitlesDic(self, col_num):
        titles = {}
        if col_num == 1:
            titles[0] = 'src'
        elif col_num == 2:
            titles[0] = 'src'
            titles[1] = 'rus'
        elif col_num == 3:
            titles[0] = 'name'
            titles[1] = 'src'
            titles[2] = 'rus'
        return titles
        
    def getDelimeter(self):
        return self.config['parameters']['delim']

    def getParserRequest(self):
        return self.config['parameters']['request']
