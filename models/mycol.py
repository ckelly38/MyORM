from myvalidator import myvalidator;
import sys;
import inspect;
from init import SQLVARIANT;
class mycol:
    #everything to init will need to be removed to solve an import problem between
    #this and the sql generator
    __myclassrefs__ = None;

    @classmethod
    def getMyClassRefs(cls): return cls.__myclassrefs__;
    
    @classmethod
    def setMyClassRefs(cls, val): cls.__myclassrefs__ = val;

    #https://stackoverflow.com/questions/1796180/
    #how-can-i-get-a-list-of-all-classes-within-current-module-in-python
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

    @classmethod
    def getClassFromTableName(cls, tablename):
        myvalidator.varmustnotbeempty(tablename, "tablename");
        for mycls in cls.getMyClassRefsMain(False):
            if (hasattr(mycls, "getTableName") and (mycls.getTableName() == tablename)): return mycls;
        raise ValueError("no class has that (" + tablename + ") as the given tablename!");

    #value needs to be removed because it cannot be stored in a class attribute for multiple objects
    #of the parent (containing) class.
    def __init__(self, colname, datatype, defaultvalue,
                 isprimarykey=False, isnonnull=None, isunique=None, issigned=None,
                 autoincrements=False, isforeignkey=False, foreignClass=None, foreignColNames=None,
                 constraints=None):#value, 
        print("INSIDE OF MY COL CONSTRUCTOR!");
        print(f"colname = {colname}");
        print(f"datatype = {datatype}");
        #print(f"value = {value}");
        print(f"defaultvalue = {defaultvalue}");
        print(f"isnonnull = {isnonnull}");
        print(f"isunique = {isunique}");
        print(f"issigned = {issigned}");
        #datatype if number of some kind will be signed by default
        #datatype if not number of some kind will not be signed by default
        print(f"isprimarykey = {isprimarykey}");
        print(f"autoincrements = {autoincrements}");
        print(f"isforeignkey = {isforeignkey}");
        print(f"foreignClass = {foreignClass}");
        print(f"foreignColNames = {foreignColNames}");
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

        self.setDataType(datatype);
        self.setIsSigned(issigned);
        self.setIsNonNull(isnonnull);
        
        self.setIsUnique(isunique);
        self.setAutoIncrements(autoincrements);
        self.setIsPrimaryKey(isprimarykey);
        self.setForeignClass(foreignClass);
        self.setForeignColNames(foreignColNames);
        self.setIsForeignKey(isforeignkey);
        self.setColName(colname);

        self.setMyClassRefs(None);
        
        #self._value = value;
        self.setDefaultValue(defaultvalue);
        self.constraints = constraints;
        print("DONE WITH MYCOL CONSTRUCTOR!");

    def getDataType(self): return self._datatype;

    #the problem with these two setters are they depend on the SQL variant
    #they need some way inside this class to get the variant by calling a getter.
    #the variant may need to be passed in to the col
    #but the calling class should provide a way to get it?
    #it will be imported or read from some sort of config or passed in as a parameter.
    #
    #there is also another piece of missing data for the default value.

    def setDataType(self, val):
        #get data types for the specific variant
        #if the list is empty or null, then assumed valid
        #if on the list, valid
        #if not on the list and list is not empty, then not valid.
        myvalidator.varmustbethetypeonly(val, str, "val");
        myvalidator.varmustnotbeempty(val, "val");
        varstr = SQLVARIANT;
        mvtpslist = myvalidator.getSQLDataTypesInfo(varstr);
        valhasps = ("(" in val and ")" in val);
        mval = (val[0: val.index("(")].upper() + val[val.index("("):] if (valhasps) else val.upper());
        if (myvalidator.isvaremptyornull(mvtpslist)): self._datatype = mval;
        else:
            if (myvalidator.isValidDataType(mval, varstr)): self._datatype = mval;
            else:
                raise ValueError("invalid data type (" + mval +
                                 ") found and used here for the variant (" + varstr + ")!");

    datatype = property(getDataType, setDataType);

    def getIsSigned(self): return self._issigned;

    #both setIsSigned and setIsNonNull depend on getDataTypeObjectWithNameOnVariant(tp, varstr)
    #this method may at times be unreliable as noted, which may effect these often not the case.
    #types with the same name, tend to have the same nullification defaults and signed defaults.
    #their ranges may differ however, so the issigned may be more likely to be wrong if it varies.

    #if signed is set to None, the default is used or error if no default.
    #if the type can be signed or not, then we take the user's value into account
    #otherwise, we will error out if it does not match the required value
    #somehow get the tpobj from the type.
    def setIsSigned(self, val):
        varstr = SQLVARIANT;
        tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(self.getDataType(), varstr);
        if (tpobj["signedhasadefault"]):
            if (val == None): self._issigned = not(tpobj["useunsigneddefault"]);
            else:
                if (val == (not(tpobj["useunsigneddefault"]))): self._issigned = val;
                else:
                    raise ValueError("invalid value set for signed the type has a default and it is " +
                                     "the opposite of this!");
        else:
            myvalidator.varmustbethetypeandornull(val, bool, True, "val"); 
            self._issigned = val;

    issigned = property(getIsSigned, setIsSigned);

    def getIsNonNull(self): return self._isnonnull;

    #if isnonnull is set to None, then the default for the type will be used
    #else it must be true if the nonnull default is true, otherwise it can be either true or false
    def setIsNonNull(self, val):
        varstr = SQLVARIANT;
        tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(self.getDataType(), varstr);
        if (val == None): self._isnonnull = tpobj["isnonnulldefault"];
        else:
            myvalidator.varmustbethetypeandornull(val, bool, True, "val");
            if (tpobj["isnonnulldefault"]):
                if (val): self._isnonnull = val;
                else:
                    raise ValueError("invalid value set for nonnull the type has a default and it is " +
                                     "the opposite of this!");
            else: self._isnonnull = val;

    isnonnull = property(getIsNonNull, setIsNonNull);

    def getDefaultValue(self): return self._defaultvalue;

    def setDefaultValue(self, val):
        #if we get the type object from the validator, there is a chance the type will provide a default
        #if however the type is signed, and has two different ranges, then we will need to
        #pull the parameter value from the user.
        #myvalidator.isValueValidForDataType(tpnm, val, varstr, useunsigned, isnonnull);
        varstr = SQLVARIANT;
        if (val == None):
            tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(self.getDataType(), varstr);
            mykynm = myvalidator.getDefaultValueKeyNameForDataTypeObj(tpobj, self);
            #print(f"mykynm = {mykynm}");

            self._defaultvalue = myvalidator.getDefaultValueForDataTypeObjWithName(tpobj, mykynm, False);
        else:
            if (myvalidator.isValueValidForDataType(self.getDataType(), val, varstr,
                                                    not(self.getIsSigned()), self.getIsNonNull())):
                self._defaultvalue = val;
            else:
                raise ValueError("invalid default value (" + val + ") for data type (" +
                                 self.getDataType() + ") found and used here for the variant (" +
                                 varstr + ")!");
    
    defaultvalue = property(getDefaultValue, setDefaultValue);

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

    def getIsUnique(self): return self._isunique;

    def setIsUnique(self, val):
        myvalidator.varmustbethetypeandornull(val, bool, True, "val");
        self._isunique = val;

    isunique = property(getIsUnique, setIsUnique);

    def getIsPrimaryKey(self): return self._isprimarykey;

    #if isprimarykey is true, then it must be unique and non-null.
    def setIsPrimaryKey(self, val):
        #if the primary key is multi-column, then we need to look for the specific
        #unique column constraint on our list of constraints
        #if it is present with the columns listed, then this is valid
        #if it is not found, then not valid
        #
        #isnonnull col constraint is single column only
        #a composite key is never null.
        #
        #however, if the primary key is single column only
        #then, we can check the isunique value for the column and the isnonnull values
        #if both are true, then valid; otherwise not valid.
        
        myvalidator.varmustbeboolean(val, "val");
        #not null constraint is single-column only
        #but unique can be one or mulitple-column constraint
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
            #else: raise ValueError("for it to be a primary key, it must be non-null and unique!");
        else:
            if (self.isnonnull == None): self.setIsNonNull(False);
            if (self.isunique == None): self.setIsUnique(False);
        self._isprimarykey = val;

    isprimarykey = property(getIsPrimaryKey, setIsPrimaryKey);

    def primaryKeyInformationMustBeValid(self, myclsref):
        #the fcobj is the calling class's object
        #need to make sure the primary key information is correct.
        #if the primary key is composite:
        #composite keys are never null, so we only need to check to see if there is a multi-col
        #unique constraint with the cols for the primary key
        #if there is, then valid; otherwise not valid so error
        #if the primary key is not composite:
        #make sure that the column is unique and not null
        pkycols = myclsref.getMyPrimaryKeyCols();
        myvalidator.varmustnotbeempty(pkycols, "pkycols");

        if (1 < len(pkycols)):
            #now get the unique constraints and see if one has those exact columns
            #get the colnames from inside of the unique constraint...
            #then check to see if they are the same
            pkycolnames = myclsref.getMyColNames(pkycols);
            mrefallconstraints = myclsref.getAllTableConstraints();
            print(f"pkycolnames = {pkycolnames}");
            print(f"mrefallconstraints = {mrefallconstraints}");
            
            isvalid = False;
            if (myvalidator.isvaremptyornull(mrefallconstraints)): isvalid = False;
            else:
                #the only constraints found on the multi-cols are check and unique
                #get all of the unique constraints, or primary key constraints...
                #then see which columns are on them...
                #if any one that has all of the column names on it matches, then valid
                #if none found, not valid.
                #the unique constraints are in the format: CONSTRAINT name UNIQUE(cols)
                #so we can search for UNIQUE() if that is not there, then ?
                for mcond in mrefallconstraints:
                    if ("UNIQUE(" in mcond):
                        mcolstrincond = mcond[mcond.index("UNIQUE(") + 7: mcond.index(")")]; 
                        print(f"mcolstrincond = {mcolstrincond}");
                        
                        tempcolsarr = mcolstrincond.split(", ");
                        print(f"tempcolsarr = {tempcolsarr}");

                        if (myvalidator.areTwoListsTheSame(tempcolsarr, pkycolnames)):
                            print("match found so valid!");
                            isvalid = True;
                            break;
            if isvalid: pass;
            else:
                raise ValueError("for it to be a primary key, for class(" + myclsref.__name__ +
                                 ") it must be non-null and unique!");
        else:
            if (self.isprimarykey):
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
                else:
                    raise ValueError("for it to be a primary key, for class(" + myclsref.__name__ +
                                     ") it must be non-null and unique!");
            else:
                if (self.isnonnull == None): self.setIsNonNull(False);
                if (self.isunique == None): self.setIsUnique(False);
        return True;

    def getForeignClass(self): return self._foreignClass;

    def setForeignClass(self, val):
        #if (val == None or myvalidator.isClass(val)): pass;
        #else: raise ValueError("val must be a class not an object!");
        self._foreignClass = val;

    foreignClass = property(getForeignClass, setForeignClass);

    def getForeignColNames(self): return self._foreignColNames;

    def setForeignColNames(self, val):#, fcobj
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
            if (self.foreignClass == None): self._foreignColNames = val;
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
            myvalidator.listMustContainUniqueValuesOnly(val);
            self._foreignColNames = val;

    foreignColNames = property(getForeignColNames, setForeignColNames);

    #cannot set is foreign key to be true if the foreign class name is not defined and
    #neither is the foreign col name 
    def getIsForeignKey(self): return self._isforeignkey;

    def setIsForeignKey(self, val):
        myvalidator.varmustbethetypeonly(val, bool, "val");
        if (val):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColNames)):
                raise ValueError("the foreign key needs a reference class and a column name!");
        else:
            if (self.foreignClass == None): pass;
            else: self.setForeignClass(None);
            if (myvalidator.isvaremptyornull(self.foreignColNames)): pass;
            else: self.setForeignColNames(None);
        self._isforeignkey = val;

    isforeignkey = property(getIsForeignKey, setIsForeignKey);

    
    def foreignKeyInformationMustBeValid(self, fcobj):
        #this method takes in the calling class's object and the current column object
        #the goal of this method is to make sure that the foreign key information is valid
        #it will look at the list of cols given and make sure that they are unique (handled by set)
        #it will make sure that the referring class is valid
        #it will make sure that the referring class has those column names on it
        #it will make sure that the referring class has a valid primary key
        #it will make sure that the column names on the link from the calling object
        #are on the referring class and has the unique data enforced.
        
        #has is foreign key
        print("BEGIN FOREIGN KEY VALIDATION METHOD NOW:");
        print(f"self.isforeignkey = {self.isforeignkey}");
        print(f"self.foreignColNames = {self.foreignColNames}");
        print(f"self.foreignClass = {self.foreignClass}");
        
        if (self.isforeignkey):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColNames)):
                raise ValueError("the foreign key needs a reference class and a column name!");
            else:
                #now make sure the column name is on the class as one
                #get the column names from the foreign class
                #once we do that we need to make sure that the column data is unique.
                #then we are sure that the information is valid.
                #self is the column object
                #fcobj is the calling object that contains that column (so this is the real self).
                #foreign class is the string name of the foreign class.
                print("self is the column object.");
                print("the calling object is fcobj which is the class instance that has the column!");
                print(f"fcobj = {fcobj}");
                
                myvalidator.varmustnotbenull(fcobj, "fcobj");
                myclsref = mycol.getMyClassRefFromString(self.foreignClass);
                print(f"myclsref = {myclsref}");

                myfcols = myclsref.getMyCols();
                myfccolnames = myclsref.getMyColNames(myfcols);
                myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                #names referenced by the foreign key
                print(f"self.foreignColNames = {self.foreignColNames}");
                print(f"myfccolnames = {myfccolnames}");#all of the col names in the foreign class
                
                myvalidator.listMustContainUniqueValuesOnly(self.foreignColNames,
                                                            "self.foreignColNames");

                mycolis = [myfccolnames.index(mclnm) for mclnm in self.foreignColNames];
                print(f"mycolis = {mycolis}");

                #now get that column object and check to see if the isunique is set to true?
                #OR is primary key and the only primary key on that table?
                mcolobjs = [myfcols[mycoli] for mycoli in mycolis];
                for mc in mcolobjs:
                    print(f"mc = {mc}");
                    print(f"mc.isunique = {mc.isunique}");
                print(f"myfcols = {myfcols}");

                pkycols = myclsref.getMyPrimaryKeyCols(myfcols);
                print(f"len(pkycols) = {len(pkycols)}");

                if (len(pkycols) < 1):
                    raise ValueError("each table must have at least one primary key, but the class(" +
                                     myclsref.__name__ + ") did not!");
                else:
                    #if there is one column on the foreign key colnames, then if it is unique OR
                    #is the primary key, then it is valid
                    #if there is more than one column on the foreign key colnames, then
                    #-they must either match the primary key colnames OR
                    #-be inside of a UNIQUE constraint with those exact colnames no more no less.
                    #otherwise it is invalid.
                    pkycolnames = myclsref.getMyColNames(pkycols);
                    print(f"pkycolnames = {pkycolnames}");
                    print(f"self.foreignColNames = {self.foreignColNames}");

                    myvalidator.listMustContainUniqueValuesOnly(pkycolnames, "pkycolnames");
                    isvalid = False;
                    if (len(self.foreignColNames) == 1):
                        mc = mcolobjs[0];
                        isvalid = (mc.isunique or (len(pkycols) == 1 and mc.isprimarykey));
                    else:
                        #length is more than one
                        #do they match the primary key column names...?
                        #is there a unique constraint for those exact column names?
                        #If yes to one: valid; if no to both, then not valid.
                        if (myvalidator.areTwoListsTheSame(pkycolnames, self.foreignColNames)):
                            isvalid = True;
                        else:
                            #now get the unique constraints and see if one has those exact columns
                            #get the colnames from inside of the unique constraint...
                            #then check to see if they are the same
                            mrefallconstraints = myclsref.getAllTableConstraints();
                            print(f"mrefallconstraints = {mrefallconstraints}");

                            if (myvalidator.isvaremptyornull(mrefallconstraints)): isvalid = False;
                            else:
                                #the only constraints found on the multi-cols are check and unique
                                #get all of the unique constraints, or primary key constraints...
                                #then see which columns are on them...
                                #if any one that has all of the column names on it matches, then valid
                                #if none found, not valid.
                                #the unique constraints are in the format: CONSTRAINT name UNIQUE(cols)
                                #so we can search for UNIQUE() if that is not there, then ?
                                for mcond in mrefallconstraints:
                                    if ("UNIQUE(" in mcond):
                                        mcolstrincond = mcond[mcond.index("UNIQUE(") + 7:
                                                                        mcond.index(")")]; 
                                        print(f"mcolstrincond = {mcolstrincond}");
                                        
                                        tempcolsarr = mcolstrincond.split(", ");
                                        print(f"tempcolsarr = {tempcolsarr}");

                                        if (myvalidator.areTwoListsTheSame(tempcolsarr,
                                                                           self.foreignColNames)):
                                            print("match found so valid!");
                                            isvalid = True;
                                            break;
                    if isvalid: pass;
                    else:
                        raise ValueError("the foreign key column on class(" + type(fcobj).__name__ +
                                         ") must refer to unique data!");
        else:
            if (self.foreignClass == None): pass;
            else: self.setForeignClass(None);
            if (myvalidator.isvaremptyornull(self.foreignColNames)): pass;
            else: self.setForeignColNames(None);
        print("DONE WITH FOREIGN KEY VALIDATION METHOD NOW!");
        return True;

    #can call in init
    def newForeignKey(self, fkycls, fkycolnm):#, fcobj
        #print(f"self = {self}");
        #print(f"fkycls = {fkycls}");
        #print(f"fkycolnm = {fkycolnm}");
        self.setForeignClass(fkycls);
        self.setForeignColNames(fkycolnm);#, fcobj
        self.setIsForeignKey(True);

    #def __repr__(self):
    #    mystr = f"<MyCol {self.colname} type: {self._datatype} value: {self._value}";
    #    mystr += f" default: {self._defaultvalue} isprimarykey: {self.isprimarykey}";
    #    mystr += f" isnonnull: {self.isnonnull} isunique: {self.isunique}";
    #    mystr += f" autoincrements: {self.autoincrements} isforeignkey: {self.isforeignkey}";
    #    mystr += f" foreignClass: {self.foreignClass} foreignColName: {self.foreignColName}";
    #    mystr += f" constraints: {self._constraints} /MyCol>";
    #    return mystr;
