from myvalidator import myvalidator;
import sys;
import inspect;
class mycol:
    __myclassrefs__ = None;

    @classmethod
    def getMyClassRefs(cls): return cls.__myclassrefs__;
    
    @classmethod
    def setMyClassRefs(cls, val): cls.__myclassrefs__ = val;

    #https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    #gets and sets the class ref list if fetchnow is True or the current list (above) is empty
    #if the current list is not empty and fetchnow is False, it returns the current list.
    #if it gets the new list, then the class refs list is updated.
    @classmethod
    def getMyClassRefsMain(cls, ftchnw=False):
        myvalidator.varmustbeboolean(ftchnw, "ftchnw");
        mycrefs = cls.getMyClassRefs();
        if (ftchnw or myvalidator.isvaremptyornull(mycrefs)):
            print("INSIDE OF MYCOL:");
            print("list of system modules:");
            #mymodnm = __name__;
            mymodnm = "__main__";
            mymods = sys.modules[mymodnm];
            print(mymods);

            #mysrclistcrefs = inspect.getmembers(mymods, myvalidator.isClass);
            #print(mysrclistcrefs);
            
            #since the inspect method gives me a list of tuples, I just want the classes, I need to:
            myfincrefs = [item[1] for item in inspect.getmembers(mymods, myvalidator.isClass)];
            print(myfincrefs);

            cls.setMyClassRefs(myfincrefs);
            return myfincrefs;
        else: return mycrefs;

    @classmethod
    def getMyClassRefFromString(cls, nmstr):
        #print(f"nmstr = {nmstr}");
        myvalidator.varmustnotbeempty(nmstr, "nmstr");
        for mycls in cls.getMyClassRefsMain():
            #print(f"mycls = {mycls}");
            #print(f"mycls.__name__ = {mycls.__name__}");
            if (mycls.__name__ == nmstr): return mycls;
        raise ValueError(f"NAME {nmstr} NOT FOUND!");

    #NEEDS TO CHANGE 2-18-2025
    def __init__(self, colname, datatype, value, defaultvalue,
                 isprimarykey=False, isnonnull=None, isunique=None,
                 autoincrements=False, isforeignkey=False, foreignClass=None, foreignColName=None,
                 constraints=None):
        print("INSIDE OF MY COL CONSTRUCTOR!");
        print(f"colname = {colname}");
        print(f"datatype = {datatype}");
        print(f"value = {value}");
        print(f"defaultvalue = {defaultvalue}");
        print(f"isnonnull = {isnonnull}");
        print(f"isunique = {isunique}");
        print(f"isprimarykey = {isprimarykey}");
        print(f"autoincrements = {autoincrements}");
        print(f"isforeignkey = {isforeignkey}");
        print(f"foreignClass = {foreignClass}");
        print(f"foreignColName = {foreignColName}");
        print(f"constraints = {constraints}");#like length or value limits
        #CONSTRAINT CHK_Person CHECK(LENGTH(description) >= 10)
        #THEY NEED A NAME IF YOU WANT TO REMOVE THEM LATER ON

        #if the default value was given as an option, then its data type must match
        #the column's data type. SAME FOR VALUE.
        #
        #it is important to note, that to start off VALUE will not be assigned.
        #ideally once it is saved on the database, then the value is assigned...
        #but once assigned the value's datatype must match the required data type.
        #
        #the foreign key data type on the corresponding table must be the same type as on this col
        #if is foreign key is true, then the foreign class name and col name must also be defined
        #with the class name and the col name we can get the column and check its data type.
        #
        #when the foreign key is composite, then the value holds the values for those columns.
        #I guess in that case the invalid data type array/tuple could be assigned.
        #
        #a note about unique constraints: you can create multi-column-unique-constraints at the
        #table level only, but in that case you do not want the isunique to be true on the
        #single column if it is not guranteed to be unique

        self.setIsNonNull(isnonnull);
        self.setIsUnique(isunique);
        self.setAutoIncrements(autoincrements);
        self.setIsPrimaryKey(isprimarykey);
        self.setForeignClass(foreignClass);
        self.setForeignColName(foreignColName);#MAY NEED TO CHANGE 2-18-2025
        self.setIsForeignKey(isforeignkey);
        self.setColName(colname);
        #self.setMyClassRefs(None);
        
        self._datatype = datatype;
        self._value = value;
        self._defaultvalue = defaultvalue;
        self._constraints = constraints;

    def getColName(self): return self._colname;

    def setColName(self, val):
        #the colname must be unique on each table
        #(CANNOT BE ENFORCED HERE, BUT WHEN A NEW OBJECT IS CREATED AND SAVED, ETC)
        #the colname cannot be null or empty
        myvalidator.varmustnotbeempty(val, "val");
        self._colname = val;
    
    colname = property(getColName, setColName);

    def getAutoIncrements(self): return self._autoincrements;

    def setAutoIncrements(self, val):
        myvalidator.varmustbethetypeonly(val, bool, "val");
        self._autoincrements = val;

    autoincrements = property(getAutoIncrements, setAutoIncrements);

    def getIsNonNull(self): return self._isnonnull;

    def setIsNonNull(self, val):
        myvalidator.varmustbethetypeandornull(val, bool, True, "val");
        self._isnonnull = val;

    isnonnull = property(getIsNonNull, setIsNonNull);

    def getIsUnique(self): return self._isunique;

    def setIsUnique(self, val):
        myvalidator.varmustbethetypeandornull(val, bool, True, "val");
        self._isunique = val;

    isunique = property(getIsUnique, setIsUnique);

    def getIsPrimaryKey(self): return self._isprimarykey;

    #if isprimarykey is true, then it must be unique and non-null.
    def setIsPrimaryKey(self, val):
        myvalidator.varmustbeboolean(val, "val");
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
        self._isprimarykey = val;

    isprimarykey = property(getIsPrimaryKey, setIsPrimaryKey);

    def getForeignClass(self): return self._foreignClass;

    def setForeignClass(self, val):
        #if (val == None or myvalidator.isClass(val)): pass;
        #else: raise ValueError("val must be a class not an object!");
        self._foreignClass = val;

    foreignClass = property(getForeignClass, setForeignClass);

    def getForeignColName(self): return self._foreignColName;

    #NOT CORRECT 2-18-2025
    def setForeignColName(self, val):#, fcobj
        #officially this must be one of the columns on the list of the calling class's columns
        #get the foreign class, then get the cols for that foreign class
        #
        #1. although I could add a calling class parameter for the column class and
        #I could create a list and add the each col to a list of them, this LIST COULD BE VERY BIG!
        #
        #2. I could store the list on the calling class.
        #BUT I DO NOT WANT TO MAKE TOO MUCH WORK FOR THE USER. (USED METHOD IN BASE CLASS)
        #
        #the data the foreign keys link back to must be unique.
        #the column must be the whole primary key for the table OR
        #the unique constraint applied to this column
        #
        if (myvalidator.isvaremptyornull(val)):
            if (self.foreignClass == None): self._foreignColName = val;
            else: raise ValueError("foreign class must be null because the colname was empty!");
        else:
            #print(f"self.foreignClass = {self.foreignClass}");
            #print(f"fcobj = {fcobj}");
            #myvalidator.varmustnotbenull(fcobj, "fcobj");
            #myfccolnames = self.foreignClass.getMyColNames(fcobj);
            #myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
            #print(f"val = {val}");
            #print(f"myfccolnames = {myfccolnames}");
            #if (val in myfccolnames): self._foreignColName = val;
            #else: raise ValueError(f"invalid column name ({val})!");
            self._foreignColName = val;

    foreignColName = property(getForeignColName, setForeignColName);

    #cannot set is foreign key to be true if the foreign class name is not defined and
    #neither is the foreign col name 
    def getIsForeignKey(self): return self._isforeignkey;

    #may need to change 2-18-2025
    def setIsForeignKey(self, val):
        myvalidator.varmustbethetypeonly(val, bool, "val");
        if (val):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColName)):
                raise ValueError("the foreign key needs a reference class and a column name!");
        else:
            if (self.foreignClass == None): pass;
            else: self.setForeignClass(None);
            if (myvalidator.isvaremptyornull(self.foreignColName)): pass;
            else: self.setForeignColName(None);
        self._isforeignkey = val;

    isforeignkey = property(getIsForeignKey, setIsForeignKey);

    #NOT SURE IF THE ENDING CONDITION FOR DETERMINGING IF THE DATA THAT
    #THE FOREIGN KEY REFERS TO IS UNIQUE OR NOT IS CORRECT
    #NOT DONE YET AND IT IS NOT CORRECT!

    def foreignKeyInformationMustBeValid(self, fcobj):
        #has is foreign key
        print(f"self.isforeignkey = {self.isforeignkey}");
        print(f"self.foreignColName = {self.foreignColName}");
        print(f"self.foreignClass = {self.foreignClass}");
        
        if (self.isforeignkey):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColName)):
                raise ValueError("the foreign key needs a reference class and a column name!");
            else:
                #now make sure the column name is on the class as one
                #get the column names from the foreign class
                #once we do that we need to make sure that the column data is unique.
                #then we are sure that the information is valid.
                print(f"self.foreignClass = {self.foreignClass}");
                print(f"fcobj = {fcobj}");
                myvalidator.varmustnotbenull(fcobj, "fcobj");
                myclsref = mycol.getMyClassRefFromString(self.foreignClass);
                myfcols = myclsref.getMyCols(fcobj);
                myfccolnames = myclsref.getMyColNames(fcobj, myfcols);
                myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                print(f"self.foreignColName = {self.foreignColName}");
                print(f"myfccolnames = {myfccolnames}");
                
                mycoli = myfccolnames.index(self.foreignColName);
                print(f"mycoli = {mycoli}");

                #now get that column object and check to see if the isunique is set to true?
                #OR is primary key and the only primary key on that table?
                mc = myfcols[mycoli];
                print(f"mc = {mc}");
                print(f"mc.isunique = {mc.isunique}");
                print(f"myfcols = {myfcols}");

                pkycols = myclsref.getMyPrimaryKeyCols(fcobj, myfcols);
                print(f"len(pkycols) = {len(pkycols)}");

                if (len(pkycols) < 1):
                    raise ValueError("each table must have at least one primary key!");
                else:
                    if (mc.isunique or (len(pkycols) == 1 and mc.isprimarykey)): pass;
                    else: raise ValueError("the foreign key column must refer to unique data!");
        else:
            if (self.foreignClass == None): pass;
            else: self.setForeignClass(None);
            if (myvalidator.isvaremptyornull(self.foreignColName)): pass;
            else: self.setForeignColName(None);
        return True;

    #can call in init NOT DONE YET...
    def newForeignKey(self, fkycls, fkycolnm):#, fcobj
        #print(f"self = {self}");
        #print(f"fkycls = {fkycls}");
        #print(f"fkycolnm = {fkycolnm}");
        self.setForeignClass(fkycls);
        self.setForeignColName(fkycolnm);#, fcobj
        self.setIsForeignKey(True);

    #def __repr__(self):
    #    mystr = f"<MyCol {self.colname} type: {self._datatype} value: {self._value}";
    #    mystr += f" default: {self._defaultvalue} isprimarykey: {self.isprimarykey}";
    #    mystr += f" isnonnull: {self.isnonnull} isunique: {self.isunique}";
    #    mystr += f" autoincrements: {self.autoincrements} isforeignkey: {self.isforeignkey}";
    #    mystr += f" foreignClass: {self.foreignClass} foreignColName: {self.foreignColName}";
    #    mystr += f" constraints: {self._constraints} /MyCol>";
    #    return mystr;
