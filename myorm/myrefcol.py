from myorm.myvalidator import myvalidator;
class myrefcol:
    #this creates a link ref to the objects in the given class (classname)
    #the listcolname is given first, then the refclassname.
    #this is not actually a col in the DB it is meant as a simplified link for the classes
    #this also helps bridge the gap for foreign key objects.
    def __init__(self, listcolname, refclassname):
        self.setListColName(listcolname);
        self.setRefClassColName(refclassname);

    #this gets either the listcolname or the refclassname from the properties
    #if uselist is true you get the listcolname otherwise refclassname
    def getListOrRefClassColName(self, uselist):
        myvalidator.varmustbeboolean(uselist, varnm="uselist");
        return (self._listcolname if (uselist) else self._refclassname);
    def getListColName(self): return self.getListOrRefClassColName(True);
    def getRefClassColName(self): return self.getListOrRefClassColName(False);

    #this sets either the listcolname or the refclassname from the properties
    #if uselist is true you get the listcolname otherwise refclassname
    def setListOrRefClassColName(self, val, uselist):
        myvalidator.varmustbeboolean(uselist, varnm="uselist");
        myvarnm = "val (" + ("list" if uselist else "refclass") + "colname)";
        myvalidator.varmustnotbeempty(val, varnm=myvarnm);
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(val, varnm=myvarnm);
        if (uselist): self._listcolname = val;
        else: self._refclassname = val;
    def setListColName(self, val): self.setListOrRefClassColName(val, True);
    def setRefClassColName(self, val): self.setListOrRefClassColName(val, False);

    listcolname = property(getListColName, setListColName);
    refclassname = property(getRefClassColName, setRefClassColName);

    #this returns a string as to what this refcol is supposed to look like
    def __repr__(self):
        return "<RefCol for " + self.listcolname + " = " + self.refclassname + ".all; /RefCol>";
