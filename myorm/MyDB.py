#to get access to the properties we need a new db obj and to initialize a db obj
#then we can use it like my_db_obj.CURSOR
from myorm.myvalidator import myvalidator;
class MyDB:
    def __init__(self, mydbname=None, mylibref=None, mysqlvar=None, myconn=None, mycursor=None):
        self.setDBName(mydbname);
        self.setLibRef(mylibref);
        self.setSQLType(mysqlvar);
        self.setConn(myconn);
        self.setCursor(mycursor);
    
    @classmethod
    def newDBFromNameAndLib(cls, mydbname, libtp, sqltp):
        if (mydbname == None or len(mydbname) < 1): raise ValueError("mydbname must not be empty!");
        else:
            if (type(mydbname) == str): pass;
            else: raise ValueError("mydbname must be a non-empty defined string!");
        if (libtp == None): raise ValueError("libtp must not be null or None!");
        tmpconn = libtp.connect(mydbname + ".db");
        return MyDB(mydbname=mydbname, mylibref=libtp, mysqlvar=sqltp,
                    myconn=tmpconn, mycursor=tmpconn.cursor());

    def getLibRef(self): return self._libref;
    def setLibRef(self, val): self._libref = val;
    libref = property(getLibRef, setLibRef);

    def getDBName(self): return self._DB_NAME;
    def setDBName(self, val):
        if (val == None or val == ""): self._DB_NAME = None;
        else:
            if (type(val) == str and 0 < len(val)): self._DB_NAME = "" + val;
            else: raise ValueError("the DB NAME must be a string and not be empty!");
    DB_NAME = property(getDBName, setDBName);

    def getConfigFileName(self): return self._CONFIGFNAME;
    def setConfigFileName(self, val):
        if (val == None or val == ""): self._CONFIGFNAME = None;
        else:
            if (type(val) == str and 0 < len(val)): self._CONFIGFNAME = "" + val;
            else: raise ValueError("the config file name must be a string and not be empty!");
    CONFIGFNAME = property(getConfigFileName, setConfigFileName);

    def getConfigAttrNames(self): return self._CONFIGATTRNAMES;
    def setConfigAttrNames(self, val):
        if (val == None or len(val) < 1): self._CONFIGATTRNAMES = None;
        else:
            for nm in val:
                if (nm == None or len(nm) < 1): raise ValueError("the name must not be empty or null!");
                else:
                    if (type(nm) == str and 0 < len(nm)): pass;
                    else: raise ValueError("the config file attr name must be a string and not empty!");
            self._CONFIGFNAME = ["" + nm for nm in val];
    CONFIGATTRNAMES = property(getConfigAttrNames, setConfigAttrNames);

    def getConfigAttrValues(self): return self._CONFIGATTRVALS;
    def setConfigAttrValues(self, vals): self._CONFIGATTRVALS = vals;
    CONFIGATTRVALUES = property(getConfigAttrValues, setConfigAttrValues);

    def getConfigValueForName(self, attrnm):
        myvalidator.varmustnotbeempty(attrnm, varnm="attrnm");
        myvalidator.twoListsMustBeTheSameSize(self.CONFIGATTRNAMES, self.CONFIGATTRVALUES,
                                              "CONFIGATTRNAMES", "CONFIGATTRVALUES");
        myattrnmi = self.CONFIGATTRNAMES.index(attrnm);
        return self.CONFIGATTRVALUES[myattrnmi];

    def getConfigNamesForValType(self, tpcls):
        myvalidator.twoListsMustBeTheSameSize(self.CONFIGATTRNAMES, self.CONFIGATTRVALUES,
                                              "CONFIGATTRNAMES", "CONFIGATTRVALUES");
        return [self.CONFIGATTRNAMES[i] for i in range(len(self.CONFIGATTRVALUES))
                if (type(self.CONFIGATTRVALUES[i]) == tpcls)];

    def getSQLType(self): return self._SQLVARIANT;
    def setSQLType(self, val):
        if (val == None or val == ""): self._SQLVARIANT = None;
        else:
            if (type(val) == str and 0 < len(val)): self._SQLVARIANT = "" + val;
            else: raise ValueError("val must be a string and not be empty!");
    SQLVARIANT = property(getSQLType, setSQLType);
    
    def getConn(self): return self._CONN;
    def setConn(self, val): self._CONN = val;
    CONN = property(getConn, setConn);
    
    def getCursor(self): return self._CURSOR;
    def setCursor(self, val): self._CURSOR = val;
    CURSOR = property(getCursor, setCursor);
