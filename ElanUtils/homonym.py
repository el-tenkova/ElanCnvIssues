import string

class ElanCnvHom:
    repl = {"\x1d62" : "",
            "\x1d63" : "",
            "\x2090" : "",
            "\x2080" : "",
            "Ass\x2082" : "Ass2" ,
            "i\x2081" : "i1" ,
            "Gen\x2081" : "Gen1" ,
            "\x2081" : "",
            "\x2082" : "",
            "\x2083" : ""}

    def __init__(self, stem, headWord, meaning, affixes, posPoss, form, pos):
        if len(stem) and stem[0] != '-':
            self.src = stem
        elif len(stem) and stem[0] == '-':
            self.src = "stem"
        else:
            self.src = headWord

        self.rus = meaning
        if posPoss != -1:
            self.rus = self.rus + ".3pos"
        form = self.removeSymbols(form)
        if len(form):
            self.rus = self.rus + '-' + form
        
        self.lemma = headWord
        self.pos = self.removeSymbols(pos)
        self.morphems = []
        self.morphems.append(self.src)
        self.morphems = self.getMorphems(affixes, self.morphems, '-')
        if len(affixes):
            self.src = self.src + '-' + affixes

        self.r_morphems = []
        self.r_morphems.append(meaning)
        self.r_morphems = self.getMorphems(form, self.r_morphems, '-')
    
    def removeSymbols(self, fromStr):
        for item in ElanCnvHom.repl:
            fromStr = fromStr.replace(item, ElanCnvHom.repl[item])
        return fromStr

    def getMorphems(self, fromStr, morphems, delim): 
        pos = fromStr.find(delim)
        if pos == -1:
            return morphems
        morphems = morphems + fromStr.split(delim)
        return morphems

    def print(self):
        print("------homonym------")
        print(self.src)
        print(self.rus)
        print(self.lemma)
        print(self.pos)
        print(self.morphems)
        print(self.r_morphems)
        
        
