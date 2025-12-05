#to get access to the properties we need a new db obj and to initialize a db obj
#then we can use it like my_db_obj.CURSOR
from myorm.myvalidator import myvalidator;
class MyDB:
    #this creates a new MyDB object with information about the DB and how to access library methods
    #this takes in the DB Name (mydbname),
    #the library ref class that was imported itself (mylibref),
    #the SQL VARIANT (mysqlvar), the connection to it (myconn),
    #and the cursor to do operations on it (mycursor)
    def __init__(self, mydbname=None, mylibref=None, mysqlvar=None, myconn=None, mycursor=None):
        self.setDBName(mydbname);
        self.setLibRef(mylibref);
        self.setSQLType(mysqlvar);
        self.setConn(myconn);
        self.setCursor(mycursor);
    
    #this creates a new MyDB object with information about the DB and how to access library methods
    #this takes in the DB Name (mydbname),
    #the library ref class that was imported itself (mylibref),
    #the SQL VARIANT (mysqlvar or sqltp)
    #it first creates a conn by calling libtp or libref.connect(mydbname + ".db");
    #it then gets the cursor via the cursor() method on the conn
    #it then calls the main constructors
    @classmethod
    def newDBFromNameAndLib(cls, mydbname, libtp, sqltp):
        myvalidator.varmustbethetypeonly(mydbname, str, varnm="mydbname");
        myvalidator.stringMustHaveAtMinNumChars(mydbname, 1, varnm="mydbname");
        if (libtp == None): raise ValueError("libtp must not be null or None!");
        tmpconn = libtp.connect(mydbname + ".db");
        return MyDB(mydbname=mydbname, mylibref=libtp, mysqlvar=sqltp,
                    myconn=tmpconn, mycursor=tmpconn.cursor());

    #this returns the libref class that was imported
    def getLibRef(self): return self._libref;
    def setLibRef(self, val): self._libref = val;
    libref = property(getLibRef, setLibRef);

    #this method returns either the DB_NAME, CONFIGFNAME, or the SQLVARIANT property values
    def getMyStrType(self, tpstr):
        myvalidator.varmustbethetypeonly(tpstr, str, varnm="tpstr");
        if (tpstr == "DB_NAME"): return self._DB_NAME;
        elif (tpstr == "CONFIGFNAME"): return self._CONFIGFNAME;
        elif (tpstr == "SQLVARIANT"): return self._SQLVARIANT;
        else:
            raise ValueError("the tpstr must be one of the following: " +
                             "[DB_NAME, CONFIGFNAME, SQLVARIANT], but it was not!");
    def getDBName(self): return self.getMyStrType("DB_NAME");
    def getConfigFileName(self): return self.getMyStrType("CONFIGFNAME");
    def getSQLType(self): return self.getMyStrType("SQLVARIANT");
    
    #this sets the value of either the DB_NAME, CONFIGFNAME, or the SQLVARIANT properties
    #to the given value.
    def setMyStrTypeVal(self, val, tpstr):
        myvalidator.varmustbethetypeonly(tpstr, str, varnm="tpstr");
        finvarnm = None;
        if (tpstr == "DB_NAME"): finvarnm = "DB NAME";
        elif (tpstr == "CONFIGFNAME"): finvarnm = "config file name";
        elif (tpstr == "SQLVARIANT"): finvarnm = "val (nwSQLType)";
        else:
            raise ValueError("the tpstr must be one of the following: " +
                             "[DB_NAME, CONFIGFNAME, SQLVARIANT], but it was not!");
        if (myvalidator.isvaremptyornull(val)):
            if (finvarnm == "DB NAME"): self._DB_NAME = None;
            elif (finvarnm == "config file name"): self._CONFIGFNAME = None;
            else: self._SQLVARIANT = None;
        else:
            myvalidator.varmustbethetypeonly(val, str, varnm=finvarnm);
            myvalidator.stringMustHaveAtMinNumChars(val, 1, varnm=finvarnm);
            if (finvarnm == "DB NAME"): self._DB_NAME = "" + val;
            elif (finvarnm == "config file name"): self._CONFIGFNAME = "" + val;
            else: self._SQLVARIANT = "" + val;
    def setDBName(self, val): self.setMyStrTypeVal(val, "DB_NAME");
    def setConfigFileName(self, val): self.setMyStrTypeVal(val, "CONFIGFNAME");
    def setSQLType(self, val): self.setMyStrTypeVal(val, "SQLVARIANT");
    
    DB_NAME = property(getDBName, setDBName);
    CONFIGFNAME = property(getConfigFileName, setConfigFileName);
    SQLVARIANT = property(getSQLType, setSQLType);

    #this gets the attribute names from the DB config file
    #well actually this does not interact with the DB config file at all,
    #but the setup method handles setting this information
    def getConfigAttrNames(self): return self._CONFIGATTRNAMES;
    def setConfigAttrNames(self, val):
        if (myvalidator.isvaremptyornull(val)): self._CONFIGATTRNAMES = None;
        else:
            for nm in val:
                myvalidator.varmustbethetypeonly(nm, str, varnm="config file attr name");
                myvalidator.stringMustHaveAtMinNumChars(nm, 1, varnm="config file attr name");
            self._CONFIGFNAME = ["" + nm for nm in val];
    CONFIGATTRNAMES = property(getConfigAttrNames, setConfigAttrNames);

    #this gets the attribute values from the DB config file
    #well actually this does not interact with the DB config file at all,
    #but the setup method handles setting this information
    def getConfigAttrValues(self): return self._CONFIGATTRVALS;
    def setConfigAttrValues(self, vals): self._CONFIGATTRVALS = vals;
    CONFIGATTRVALUES = property(getConfigAttrValues, setConfigAttrValues);

    def getConn(self): return self._CONN;
    def setConn(self, val): self._CONN = val;
    CONN = property(getConn, setConn);
    
    def getCursor(self): return self._CURSOR;
    def setCursor(self, val): self._CURSOR = val;
    CURSOR = property(getCursor, setCursor);

    #this gets the value for a given attribute name from the DB config file
    #well actually this does not interact with the DB config file at all,
    #but the setup method handles setting this information
    def getConfigValueForName(self, attrnm):
        myvalidator.varmustnotbeempty(attrnm, varnm="attrnm");
        myvalidator.twoListsMustBeTheSameSize(self.CONFIGATTRNAMES, self.CONFIGATTRVALUES,
                                              arranm="CONFIGATTRNAMES", arrbnm="CONFIGATTRVALUES");
        myattrnmi = self.CONFIGATTRNAMES.index(attrnm);
        return self.CONFIGATTRVALUES[myattrnmi];

    #this gets the DB config attribute names for the given value type
    #well actually this does not interact with the DB config file at all,
    #but the setup method handles setting this information
    def getConfigNamesForValType(self, tpcls):
        myvalidator.twoListsMustBeTheSameSize(self.CONFIGATTRNAMES, self.CONFIGATTRVALUES,
                                              arranm="CONFIGATTRNAMES", arrbnm="CONFIGATTRVALUES");
        return [self.CONFIGATTRNAMES[i] for i in range(len(self.CONFIGATTRVALUES))
                if (type(self.CONFIGATTRVALUES[i]) == tpcls)];
