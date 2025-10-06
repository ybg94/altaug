#read the file and create object

#create Modifier object which has a name and a value ex: modifer="dictator's"
class Modifier:
    def __init__ (self, name: str, affix: str):
        self.name = name
        self.affix = affix