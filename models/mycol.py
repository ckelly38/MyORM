class mycol:
    @classmethod
    def varmustbethetypeandornull(clsnm, val, tpcls, canbenull, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
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
    def varmustnotbeempty(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return clsnm.varmustnotbeempty(val, "varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None or len(val) < 1): raise ValueError(varnm + " must not be empty!");
        else: return True;


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
        print(f"constraints = {constraints}");#like length or value limits
        #CONSTRAINT CHK_Person CHECK(LENGTH(description) >= 10)
        #THEY NEED A NAME IF YOU WANT TO REMOVE THEM LATER ON

        self.setIsNonNull(isnonnull);
        self.setIsUnique(isunique);
        self.setIsPrimaryKey(isprimarykey);
        self.setIsForeignKey(isforeignkey);
        self.setAutoIncrements(autoincrements);
        
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

    def getIsForeignKey(self): return self._isforeignkey;

    def setIsForeignKey(self, val):
        mycol.varmustbethetypeonly(val, bool, "val");
        self._isforeignkey = val;

    isforeignkey = property(getIsForeignKey, setIsForeignKey);

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