from myvalidator import myvalidator;
class myrefcol:
    def __init__(self, listcolname, refclassname):
        self.setListColName(listcolname);
        self.setRefClassColName(refclassname);

    def getListOrRefClassColName(self, uselist):
        myvalidator.varmustbeboolean(uselist, "uselist");
        return (self._listcolname if (uselist) else self._refclassname);
    def getListColName(self): return self.getListOrRefClassColName(True);
    def getRefClassColName(self): return self.getListOrRefClassColName(False);

    def setListOrRefClassColName(self, val, uselist):
        myvalidator.varmustbeboolean(uselist, "uselist");
        myvalidator.varmustnotbeempty(val, "val (" + ("list" if uselist else "refclass") + "colname)");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(val, "val");
        if (uselist): self._listcolname = val;
        else: self._refclassname = val;
    def setListColName(self, val): self.setListOrRefClassColName(val, True);
    def setRefClassColName(self, val): self.setListOrRefClassColName(val, False);

    listcolname = property(getListColName, setListColName);
    refclassname = property(getRefClassColName, setRefClassColName);

    def __repr__(self):
        return "<RefCol for " + self.listcolname + " = " + self.refclassname + ".all; /RefCol>";
