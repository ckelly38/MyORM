class mycol:
    @classmethod
    def varmustbethetypeandornull(clsnm, val, tpcls, canbenull, varnm="varname"):
        if (varnm == None or (type(varnm) == str and len(varnm) < 1)):
            return clsnm.varmustbethetypeornull(val, tpcls, "varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None):
            if (canbenull): return True;
            else: raise TypeError(varnm + " was not the correct type!");
        else:
            if (type(val) == tpcls): return True;
            else: raise TypeError(varnm + " was not the correct type!");
    @classmethod
    def varmustbethetypeonly(clsnm, val, tpcls, varnm="varname"):
        return clsnm.varmustbethetypeandornull(val, tpcls, False, varnm);
    @classmethod
    def varmustbeboolean(clsnm, val, varnm="varname"):
        return clsnm.varmustbethetypeonly(val, bool, varnm);
    
    @classmethod
    def varmustnotbenull(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return clsnm.varmustnotbenull(val, "varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None): raise ValueError(varnm + " must not be null!");
        else: return True;

    @classmethod
    def isvaremptyornull(clsnm, val): return (val == None or len(val) < 1);

    @classmethod
    def varmustnotbeempty(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return clsnm.varmustnotbeempty(val, "varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None or len(val) < 1): raise ValueError(varnm + " must not be empty!");
        else: return True;

    @classmethod
    def isClass(clsnm, val): return (type(val) == type);

    def __init__(self, colname, datatype, value, defaultvalue,
                 isprimarykey=False, isforeignkey=False, isnonnull=None, isunique=None,
                 autoincrements=False, foreignClass=None, foreignColName=None, constraints=None):
        print("INSIDE OF MY COL CONSTRUCTOR!");
        print(f"colname = {colname}");
        print(f"datatype = {datatype}");
        print(f"value = {value}");
        print(f"defaultvalue = {defaultvalue}");
        print(f"isprimarykey = {isprimarykey}");
        print(f"isforeignkey = {isforeignkey}");
        print(f"autoincrements = {autoincrements}");
        print(f"isnonnull = {isnonnull}");
        print(f"isunique = {isunique}");
        print(f"foreignClass = {foreignClass}");
        print(f"foreignColName = {foreignColName}");
        print(f"constraints = {constraints}");#like length or value limits
        #CONSTRAINT CHK_Person CHECK(LENGTH(description) >= 10)
        #THEY NEED A NAME IF YOU WANT TO REMOVE THEM LATER ON

        #the default value must be the same data type.
        #the foreign key data type on the corresponding table must be the same type as on this col
        #if is foreign key is true, then the foreign class name and col name must also be defined
        #with the class name and the col name we can get the column and check its data type.

        self.setIsNonNull(isnonnull);
        self.setIsUnique(isunique);
        self.setAutoIncrements(autoincrements);
        self.setIsPrimaryKey(isprimarykey);
        self.setForeignClass(foreignClass);
        self.setForeignColName(foreignColName);
        self.setIsForeignKey(isforeignkey);
        
        mycol.varmustnotbeempty(colname, "colname");
        self._colname = colname;
        
        self._datatype = datatype;
        self._value = value;
        self._defaultvalue = defaultvalue;
        self._constraints = constraints;

    def getAutoIncrements(self): return self._autoincrements;

    def setAutoIncrements(self, val):
        mycol.varmustbethetypeonly(val, bool, "val");
        self._autoincrements = val;

    autoincrements = property(getAutoIncrements, setAutoIncrements);

    def getIsNonNull(self): return self._isnonnull;

    def setIsNonNull(self, val):
        mycol.varmustbethetypeandornull(val, bool, True, "val");
        self._isnonnull = val;

    isnonnull = property(getIsNonNull, setIsNonNull);

    def getIsUnique(self): return self._isunique;

    def setIsUnique(self, val):
        mycol.varmustbethetypeandornull(val, bool, True, "val");
        self._isunique = val;

    isunique = property(getIsUnique, setIsUnique);

    def getIsPrimaryKey(self): return self._isprimarykey;

    #if isprimarykey is true, then it must be unique and non-null.
    def setIsPrimaryKey(self, val):
        mycol.varmustbeboolean(val, "val");
        if (val):
            isvalid = False;
            if (self.isnonnull == None):
                if (self.isunique == None): isvalid = True;
                else: isvalid = self.isunique;
            else:
                if (self.isnonnull):
                    if (self.isunique == None): isvalid = True;
                    else: isvalid = self.isunique;
                else: isvalid = False;
            if (isvalid):
                if (self.isnonnull == None or self.isunique == None):
                    self.setIsNonNull(True);
                    self.setIsUnique(True);
            else: raise ValueError("for it to be a primary key, it must be non-null and unique!");
        else:
            if (self.isnonnull == None): self.setIsNonNull(False);
            if (self.isunique == None): self.setIsUnique(False);

    isprimarykey = property(getIsPrimaryKey, setIsPrimaryKey);

    def getForeignClass(self): return self._foreignClass;

    def setForeignClass(self, val):
        if (val == None or mycol.isClass(val)): self._foreignClass = val;
        else: raise ValueError("val must be a class not an object!");

    foreignClass = property(getForeignClass, setForeignClass);

    def getForeignColName(self): return self._foreignColName;

    def setForeignColName(self, val):
        #officially this must be one of the columns on the list of the calling class's columns
        #get the foreign class, then get the cols for that foreign class
        #
        #1. although I could add a calling class parameter for the column class and
        #I could create a list and add the each col to a list of them, this LIST COULD BE VERY BIG!
        #
        #2. I could store the list on the calling class.
        #BUT I DO NOT WANT TO MAKE TOO MUCH WORK FOR THE USER. (USED METHOD IN BASE CLASS)
        #
        if (mycol.isvaremptyornull(val)):
            if (self.foreignClass == None): self._foreignColName = val;
            else: raise ValueError("foreign class must be null because the colname was empty!");
        else:
            mycol.varmustnotbeempty(self.foreignClass, "self.foreignClass");
            if (val in self.foreignClass.getMyCols()): self._foreignColName = val;
            else: raise ValueError(f"invalid column name ({val})!");

    foreignColName = property(getForeignColName, setForeignColName);

    #cannot set is foreign key to be true if the foreign class name is not defined and
    #neither is the foreign col name 
    def getIsForeignKey(self): return self._isforeignkey;

    def setIsForeignKey(self, val):
        mycol.varmustbethetypeonly(val, bool, "val");
        if (val):
            if (self.foreignClass == None or mycol.isvaremptyornull(self.foreignColName)):
                raise ValueError("the foreign key needs a reference class and a column name!");
        else:
            if (self.foreignClass == None): pass;
            else: self.setForeignClass(None);
            if (mycol.isvaremptyornull(self.foreignColName)): pass;
            else: self.setForeignColName(None);
        self._isforeignkey = val;

    isforeignkey = property(getIsForeignKey, setIsForeignKey);
