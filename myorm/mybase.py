from myorm.mycol import mycol;
from myorm.myvalidator import myvalidator;
from myorm.myrefcol import myrefcol;
from myorm.MyDB import MyDB;
#from init import *;#SQLVARIANT, CURSOR, CONN
import traceback;
from pathlib import Path;#needed for checking if files exit if not using os or try catch
class mybase:
    #mytablename = "basetablename";
    #mymulticolargs = None;
    #disableconstraintswarning = False;
    
    @classmethod
    def getMyDBRef(cls): return mycol.getMyDB();
    @classmethod
    def setMyDB(cls, val): mycol.setMyDB(val);
    @classmethod
    def getMyLibRefClass(cls): return mycol.getMyLibRefClass();
    @classmethod
    def setMyLibRefClass(cls, val): mycol.setMyLibRefClass(val);
    @classmethod
    def getMyDBName(cls): return mycol.getMyDBName();
    @classmethod
    def setMyDBName(cls, val): mycol.setMyDBName(val);
    @classmethod
    def getMyDBConfigFileName(cls): return mycol.getMyDBConfigFileName();
    @classmethod
    def setMyDBConfigFileName(cls, val): mycol.setMyDBConfigFileName(val);
    @classmethod
    def getMySQLType(cls): return mycol.getMySQLType();
    @classmethod
    def setMySQLType(cls, val): mycol.setMySQLType(val);
    @classmethod
    def getMyCursor(cls): return mycol.getMyCursor();
    @classmethod
    def setMyCursor(cls, val): mycol.setMyCursor(val);
    @classmethod
    def getMyConn(cls): return mycol.getMyConn();
    @classmethod
    def setMyConn(cls, val): return mycol.setMyConn(val);

    @classmethod
    def setupPartA(cls):
        print("\nINSIDE BASE SETUP CLASS METHOD!");
        print(f"cls = {cls}");
        print(f"mytablename = {cls.getTableName()}");
        
        if (cls.isVarPresentOnTableMain("multi_column_constraints_list")): pass;
        else: setattr(cls, "mymulticolargs", None);
        #multiclcnsts = cls.getAndSetAllMultiColumnConstraints();
        multiclcnsts = cls.getMultiColumnConstraints();
        print(f"multicolconstraints = {multiclcnsts}");
        
        mtargs = cls.getAllTableConstraints();#bool fetchnow=False
        if (cls.isVarPresentOnTableMain("allconstraints_list")): pass;
        else: setattr(cls, "tableargs", ([] if (mtargs == None) else mtargs));
        #mtargs = cls.getAndSetAllTableConstraints();#bool fetchnow=False
        print(f"tableargs = {mtargs}");
        
        mytempcols = cls.getMyCols();
        mycolnames = cls.getMyColNames(mytempcols);
        mycolattrnames = cls.getMyColAttributeNames();
        myrefcols = cls.getMyRefCols();
        myrefcolnames = cls.getMyRefColNames(myrefcols);
        myrefcolattrnames = cls.getMyRefColAttributeNames();
        print(f"mycolnames = {mycolnames}");
        print(f"mycolattrnames = {mycolattrnames}");
        print(f"myrefcolattrnames = {myrefcolattrnames}");
        print(f"myrefcolnames = {myrefcolnames}");

        myvalidator.listMustContainUniqueValuesOnly(mycolnames, "mycolnames");
        myvalidator.listMustContainUniqueValuesOnly(mycolattrnames, "mycolattrnames");
        myvalidator.listMustContainUniqueValuesOnly(myrefcolattrnames, "myrefcolattrnames");
        myvalidator.listMustContainUniqueValuesOnly(myrefcolnames, "myrefcolnames");
        if (myvalidator.areTwoListsTheSame(mycolnames, mycolattrnames)): pass;
        else: raise ValueError("THE COLUMN ATTRIBUTE NAMES MUST MATCH THE SET COLNAME GIVEN!");
        if (myvalidator.areTwoListsTheSameSize(myrefcolnames, myrefcolattrnames)): pass;
        else: raise ValueError("THE REF COLUMN ATTRIBUTE NAMES MUST BE THE SAME SIZE AS THE COLNAMES!");
    
        colinverrmsg = "there exists at least one column on the class (" + cls.__name__;
        colinverrmsg += ") that does not have a valid constraint! The invalid colnames are: ";
        if (cls.areColsWithIndividualConstraintsValid(mytempcols)): pass;
        else:
            errmsgptc = myvalidator.myjoin(", ", cls.getMyColNames(
                cls.getColumnsWithIndividualInvalidConstraints(mytempcols)));
            raise ValueError(colinverrmsg + errmsgptc);

        #make sure all gets added.
        if (hasattr(cls, "all")): pass;
        else: setattr(cls, "all", None);

        print(f"DONE WITH THE SETUP PART A METHOD FOR {cls.__name__}!\n");
    
    #depends on the all list existing and being set for all of the classes that is a subclass of mybase
    #and not mybase before this runs.
    #this method sets up the refcols here.
    @classmethod
    def setupPartB(cls, calledinmain=False):
        myvalidator.varmustbeboolean(calledinmain, "calledinmain");
        if (issubclass(cls, mybase) and not (cls == mybase)):
            #print(f"BEGIN THE SETUP PART B METHOD FOR {cls.__name__}!\n");
            for myrefcolobj in cls.getMyRefCols():
                mynwattrnm = myrefcolobj.getListColName();
                myrefclsnm = myrefcolobj.getRefClassColName();
                
                #if we outright call it before setupPartA has run,
                #then there is a chance that the class instance will not have been defined yet.
                #the error is not fatal yet. Though it should be.
                #it is when it is called in the main setup then it is fatal.
                myrefclsref = None;
                try:
                    myrefclsref = mycol.getMyClassRefFromString(myrefclsnm);
                except Exception as ex:
                    #traceback.print_exc();
                    print(f"class name {myrefclsnm} was not found (so setup exited prematurely)!");
                    if (calledinmain): raise ex;
                    else: return None;
                
                callset = True;
                if (hasattr(cls, mynwattrnm)):
                    mval = getattr(cls, mynwattrnm);
                    if (mval == myrefclsref.all): callset = False;
                if (callset): setattr(cls, mynwattrnm, myrefclsref.all);
            #print(f"DONE WITH THE SETUP PART B METHOD FOR {cls.__name__}!\n");
    @classmethod
    def updateAllLinkRefsForMyClass(cls): cls.setupPartB(True);

    @classmethod
    def setupPartC(cls):
        if (issubclass(cls, mybase) and not (cls == mybase)):
            print(f"BEGIN THE SETUP PART C METHOD FOR {cls.__name__}!\n");
            for mc in cls.getMyCols():
                mc.setContainingClassName(cls.__name__);
                mc.primaryKeyInformationMustBeValid(cls);
                if (mc.isForeignKey()):
                    if (mc.foreignKeyInformationMustBeValid(fcobj=None, usenoclassobj=True)): pass;
                    else: raise ValueError("the foreign key column information must be valid!");
            print(f"DONE WITH THE SETUP PART C METHOD FOR {cls.__name__}!\n");

    @classmethod
    def setupMain(cls):
        mlist = mycol.getMyClassRefsMain(True);
        isempty = myvalidator.isvaremptyornull(mlist);
        if (isempty): pass;
        else:
            mbclses = [];
            mtnms = [];
            for mclsref in mlist:
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)):
                    mbclses.append(mclsref);
                    mtnms.append(mclsref.getTableName());
                    mclsref.setupPartA();
            myvalidator.listMustContainUniqueValuesOnly(mtnms, "the list of table names");
            
            #due to a dependency on the all list existing and being set for all of the classes
            #(that are a subclass of mybase and not mybase),
            #we need to set the refcols here essentially after the setup method has run.
            #therefore it must be done in a separate loop after all of partA has finished running.

            for mclsref in mbclses:
                #if (issubclass(mclsref, mybase) and not (mclsref == mybase)):
                    mclsref.setupPartB(True);
                    mclsref.setupPartC();
        mycol.setRanSetup(not isempty);


    #DEPENDS ON THE SQL VARIANT
    def __init__(self, colnames=None, colvalues=None, **kwargs):
        print("INSIDE BASE CLASS CONSTRUCTOR CALLING SETUP IF NEEDED FIRST!");
        #print(f"mycol.hasRunSetupYet() = {mycol.hasRunSetupYet()}");
        if (not mycol.hasRunSetupYet()): type(self).setupMain();
        mytempcols = type(self).getMyCols();
        mycolnames = type(self).getMyColNames(mytempcols);
        print("INSIDE BASE CLASS CONSTRUCTOR AFTER SETUP CALL!");
        print(f"type(self) = {type(self)}");
        print(f"mytablename = {type(self).getTableName()}");
        print(f"mycolnames = {mycolnames}");
        print(f"colnames = {colnames}");#user provided
        print(f"colvalues = {colvalues}");#user provided
        print(f"kwargs = {kwargs}");
        
        mkwdargslist = list(kwargs.keys());
        if (myvalidator.isvaremptyornull(mkwdargslist)): pass;
        else:
            #if the user provides both the colnames and colvalues and keywordargs
            #with contradicting values kill the program here because the call is invalid
            #otherwise ignore them after copying them to the colvalues and colnames lists and recall
            if (myvalidator.isvaremptyornull(colnames)):
                ncolnames = myvalidator.combineTwoLists(colnames, mkwdargslist, nodups=True);
                ncolvalues = [kwargs[ky] for ky in mkwdargslist];
                #print(f"ncolnames = {ncolnames}");
                #print(f"ncolvalues = {ncolvalues}");
                
                return self.__init__(colnames=ncolnames, colvalues=ncolvalues);
            else:
                #cmnkys = [ky for ky in mkwdargslist if ky in colnames];
                #uargkys = [ky for ky in mkwdargslist if ky not in cmnkys];
                cmnkys = [];
                uargkys = [];
                for ky in mkwdargslist:
                    if (ky in colnames): cmnkys.append(ky);
                    else: uargkys.append(ky);
                cmnkyindxs = [colnames.index(ky) for ky in cmnkys];
                #print(f"uargkys = {uargkys}");
                #print(f"cmnkys = {cmnkys}");
                #print(f"cmnkyindxs = {cmnkyindxs}");
                
                lstbadkynmvals = [];
                for n in range(len(cmnkys)):
                    ky = cmnkys[n];
                    #print(f"argval = {kwargs[ky]}");
                    #print(f"colval = {colvalues[cmnkyindxs[n]]}");

                    if (kwargs[ky] == colvalues[cmnkyindxs[n]]): pass;
                    else: lstbadkynmvals.append(ky);
                
                if (myvalidator.isvaremptyornull(lstbadkynmvals)):
                    #no bad keys where there were contradicting values
                    #but we may have different keys on both lists
                    #so add the kywargs keys and values to the col lists
                    ncolnames = myvalidator.combineTwoLists(colnames, mkwdargslist, nodups=True);
                    ncolvalues = [val for val in colvalues];
                    kyarglist = (mkwdargslist if (myvalidator.isvaremptyornull(cmnkys)) else uargkys);
                    for ky in kyarglist: ncolvalues.append(kwargs[ky]);
                    #print(f"kyarglist = {kyarglist}");
                    #print(f"ncolnames = {ncolnames}");
                    #print(f"ncolvalues = {ncolvalues}");
                    
                    return self.__init__(colnames=ncolnames, colvalues=ncolvalues);
                else:
                    errmsg = "all of the keys should agree on the values or the keys ";
                    errmsg += "should be different, but they were not!\n";
                    errmsg += "The following key(s) have two different values for them:\n";
                    errmsg += str(lstbadkynmvals) + "!";
                    raise TypeError(errmsg);

        self.setLastSyncedValsDict(None);
        self.setUserProvidedColNames(colnames);

        #for each column if it is a foreign key, now need to evaluate the class string
        #but need and the link col name
        #over here call the validation method for the new foreign key...
        #colname is already set we need to validate it.
        #we also need the class reference for validation purposes.
        #USING GLOBALS DOES NOT WORK IN THIS CASE SO CANNOT DO STRING TO REF CONVERSION.

        varstr = "" + mybase.getMySQLType();#SQLVARIANT
        if (hasattr(type(self), "all")):
            if (type(self).all == None): type(self).all = [self];
            else: type(self).all.append(self);
        else: setattr(type(self), "all", [self]);

        #provide the context to the cols for the object here...
        #get my cols, then for each col, call setContext with the current object.
        for mc in self.getMyCols(): mc.setContext(self);
        
        print(f"varstr = SQLVARIANT = {varstr}");
        print("\nNOW VERIFYING THE FOREIGN AND PRIMARY KEY INFORMATION IN BASE CLASS CONSTRUCTOR:\n");
        
        for mc in mytempcols:
            #mc.setContainingClassName(type(self).__name__);
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(
                mc.getContainingClassName(), "containing class name");
            mc.primaryKeyInformationMustBeValid(type(self));
            mc.foreignKeyInformationMustBeValid(fcobj=self, usenoclassobj=False);

        print("\nDONE VERIFYING THE FOREIGN AND PRIMARY KEY INFORMATION IN BASE CLASS CONSTRUCTOR!");
        
        #for each column need to make sure that there is a value if not use the default value
        #how to know which value is for what col?
        #base constructor will take in two parameters, one col names, and one values

        print("\nBEGIN ASSIGNING GIVEN VALUES FOR THE COLUMNS IN THE BASE CLASS CONSTRUCTOR:");

        if myvalidator.isvaremptyornull(colnames): pass;
        else:
            for n in range(len(colnames)):
                clnm = colnames[n];
                valcl = colvalues[n];
                #print(f"clnm = {clnm}");
                #print(f"valcl = {valcl}");

                if (clnm in mycolnames):
                    mycolobj = mytempcols[mycolnames.index(clnm)];
                    #print(f"mycolobj = {mycolobj}");

                    self.setValueForColName(clnm, valcl, mycolobj);
                print();
        
        print("DONE ASSIGNING GIVEN VALUES FOR THE COLUMNS IN THE BASE CLASS CONSTRUCTOR!");
        

        #get the col names not in that list and then compute the default values that can be used
        #for those columns here and below

        #do the same for the colnames not in that list
        ocolnms = [mclnm for mclnm in mycolnames
                   if myvalidator.isvaremptyornull(colnames) or mclnm not in colnames];
        print();
        print(f"mycolnames = {mycolnames}");
        print(f"colnames = {colnames}");
        print(f"ocolnms = {ocolnms}");
        
        print("\nBEGIN ASSIGNING REMAINING COLUMNS WITH DEFAULT VALUES IN BASE CLASS CONSTRUCTOR:");

        clvalsfromdb = [];
        clvalsdftsused = [];
        for clnm in ocolnms:
            #the value is the default value for the type for the varaint
            #get the type object for that type for the variant
            mycolobj = mytempcols[mycolnames.index(clnm)];
            fldtnm = mycolobj.getDataType();
            tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(fldtnm, varstr);
            print(f"tpobj = {tpobj}");
            print(f"fldtnm = {fldtnm}");
            print(f"mycolobj = {mycolobj}");
            
            mykynm = myvalidator.getDefaultValueKeyNameForDataTypeObj(tpobj, mycolobj);
            print(f"mykynm = {mykynm}");

            #default value from the data type
            deftpvalcl = myvalidator.getDefaultValueForDataTypeObjWithName(tpobj, mykynm, False);
            print(f"clnm = {clnm}");
            print(f"deftpvalcl = {deftpvalcl}");

            #default value from the col from the user (assuming not NONE)
            defvaloncl = mycolobj.getDefaultValue();
            print(f"defvaloncl = {defvaloncl}");

            #if the type is an integer of some kind,
            #then get the maximum value used on the object list (excluding self)
            #then add 1 if autoincrement.
            #if no autoincrement, then what?
            #if the type is not an integer of some kind, then skip
            tpisintnum = False;
            for nm in tpobj["names"]:
                if ("INT" in nm):
                    tpisintnum = True;
                    break;
            print(f"tpisintnum = {tpisintnum}");

            #if they all agree, just use it
            #if they do not all agree, then we need to pick one of them:
            #if there is only one instance (the self), then the defaults can be used in this order:
            #-the column default provided by the user, if not provided then:
            #-the default for the data type will be used.
            #if there is more than one instance (other than self), then we need to pick one of them.
            #-we cannot use the type default. we may be able to use the user provided default,
            #but the computed value should be used.
            #unless the user explicitly wants this to come from the DB.
            
            #if the user wants it to come from the DB, then do a special set
            #else compute the value from the defaults below.
            #if it is a primary key and not provided by the user and not a multi-col primary key,
            #then get from DB else the user will provide it or it will be computed.
            #if it is the only primary key column and some sort of integer, then for sure get from DB.
            #but if it is some other type, then cannot get from DB
            #unless it is some sort of default like the current date or the current time.
            #NOT SURE ON THE OTHER STUFF 4-12-2025 2:48 AM MST???
            mypkycols = type(self).getMyPrimaryKeyCols(mytempcols);
            getfromdb = ((mycolobj.getIsPrimaryKey() and len(mypkycols) == 1) and (tpisintnum));
            print(f"getfromdb = {getfromdb}");
            
            if (getfromdb): valcl = None;
            else:
                if (tpisintnum):
                    mynum = 0;
                    fnditemotherthanself = False;
                    for mobj in type(self).all:
                        if (mobj == self): pass;
                        else:
                            if (not fnditemotherthanself): fnditemotherthanself = True;
                            tmpobjval = mobj.getValueForColName(clnm);
                            if (mynum < tmpobjval): mynum = tmpobjval;
                    print(f"fnditemotherthanself = {fnditemotherthanself}");

                    if (fnditemotherthanself): pass;
                    else: mynum = (deftpvalcl if (defvaloncl == None) else defvaloncl);
                    print(f"mycolobj.getAutoIncrements() = {mycolobj.getAutoIncrements()}");
                    
                    if (fnditemotherthanself and mycolobj.getAutoIncrements()): mynum += 1;
                    #else do nothing do not auto-increment on the foreign key for example.
                    #computed default value
                    print(f"mynum = {mynum}");

                    #they either all agree or the computed num holds the correct value now
                    valcl = mynum;
                else:
                    print("TYPE IS NOT AN INTEGER!");
                    valcl = (deftpvalcl if (defvaloncl == None) else defvaloncl);
            
            if (getfromdb):
                clvalsfromdb.append(clnm);
                setattr(self, clnm + "_value", valcl);
            else:
                clvalsdftsused.append(clnm);
                self.setValueForColName(clnm, valcl, mycolobj);
        self.setColNamesWithDefaultsUsed(clvalsdftsused);
        self.setColNamesWithDBValsUsed(clvalsfromdb);
        
        print("DONE ASSIGNING REMAINING COLUMNS WITH DEFAULT VALUES IN BASE CLASS CONSTRUCTOR!");
        
        #set the objects for the foreign key object cols here...
        #IE say we have a SignUps DB table and it has a reference to a Camper object called camper
        #we also have the ID of the Camper in the foreign key column.
        #so we can look up the correct camper from our list.
        #this list assumes it has been synced with the DB.
        #now this adds a new property called camper and sets it equal to the object with the given ID.
        #note if the other class's objects were not created yet due to sequencing, then this will say
        #camper = None; or null for example.
        #this information will need to be refetched in that case before a save is done.
        #if the user tries to access it, and the object exists, but did not before,
        #we may want to refetch then instead of just before save.
        self.getAndSetForeignKeyObjectsFromCols(mytempcols);

        #update them all here...
        print();
        type(self).updateAllForeignKeyObjectsForAllClasses(not mycol.hasRunSetupYet());
        type(self).updateAllLinkRefsForAllClasses(not mycol.hasRunSetupYet());

        #do something here...
        print("DONE WITH THE BASE CONSTRUCTOR!\n");
    

    #uses alphabetic order for colnames
    @classmethod
    def newBase(cls, myvals):
        myvalidator.varmustnotbeempty(myvals, "myvals");
        return cls(cls.getMyColNames(cls.getMyCols()), myvals);
    
    #note can also pass in a list of tuples in here without a problem
    @classmethod
    def newBaseFromObjsOrListOfLists(cls, mlistofobjsorlists, useobjs):
        myvalidator.varmustbeboolean(useobjs, "useobjs");
        myvalidator.varmustnotbeempty(mlistofobjsorlists, "mlistofobjsorlists");
        #although we could use a list comprehension here, this is more efficient.
        clnms = [];
        clvls = [];
        for mobjorlist in mlistofobjsorlists:
            if (useobjs):
                clnms.append(list(mobjorlist.keys())[0]);
                clvls.append(list(mobjorlist.values())[0]);
            else:
                clnms.append(mobjorlist[0]);
                clvls.append(mobjorlist[1]);
        return cls(clnms, clvls);
    @classmethod
    def newBaseFromObjsList(cls, myobjslist):
        return cls.newBaseFromObjsOrListOfLists(myobjslist, True);
    @classmethod
    def newBaseFromListOfLists(cls, mytupslist):
        return cls.newBaseFromObjsOrListOfLists(mytupslist, False);

    @classmethod
    def newBaseFromDataObj(cls, mydataobj):
        myvalidator.varmustnotbenull(mydataobj, "mydataobj");
        return cls(list(mydataobj.keys()), list(mydataobj.values()));
    
    #constructor methods above up to and including __init__


    #individual object class methods below here

    #validator convenience methods here
    #(actual validator methods are stored in mycol, but data type validations are done in myvalidator)

    #This is a decorator. This actually calls a decorator.
    #https://www.datacamp.com/tutorial/decorators-python
    #@classmethod
    def validates(*args): return mycol.validates(args);#cls, 

    def runGivenValidatorsForClass(self, mvs):
        return mycol.runGivenValidatorsForClass(type(self).__name__, self, mvs);

    def runValidatorsByKeysForClass(self, mkys):
        return mycol.runValidatorsByKeysForClass(type(self).__name__, self, mkys);

    def runAllValidatorsForClass(self):
        return mycol.runAllValidatorsForClass(type(self).__name__, self);


    #get and set column and update object references

    def getValueForColName(self, clnm):
        myvalidator.stringMustHaveAtMinNumChars(clnm, 1, "clnm");
        return getattr(self, clnm + "_value");
    def getValueForColumn(self, clnm): return self.getValueForColName(clnm);
    def getValueForCol(self, clnm): return self.getValueForColName(clnm);
    def getColValue(self, clnm): return self.getValueForColName(clnm);
    def getColumnValue(self, clnm): return self.getValueForColName(clnm);

    #DEPENDS ON THE SQL VARIANT
    def setValueForColName(self, clnm, valcl, mycolobj=None):
        myvalidator.stringMustHaveAtMinNumChars(clnm, 1, "clnm");
        if (mycolobj == None):
            return self.setValueForColName(clnm, valcl, type(self).getMyColObjFromName(clnm));
        else: myvalidator.varmustnotbenull(mycolobj, "mycolobj");
        varstr = "" + mybase.getMySQLType();#SQLVARIANT;
        errmsgpta = "invalid value (";
        errmsgptb = ") used here for the data type (";
        mvaldtp = mycolobj.getDataType();
        errptbwithdata = errmsgptb + (mvaldtp if (type(mvaldtp) == str) else str(mvaldtp));
        errmsgptc = ") for the variant (" + varstr + ")!";
        #print(f"clnm = {clnm}");
        #print(f"valcl = {valcl}");
        #print(f"mycolobj = {mycolobj}");

        if (type(valcl) == list):
            if (mycolobj.isforeignkey):
                if (1 < len(valcl)):
                    #get the foreign col object now
                    
                    #in order for this method below to work it requires that the:
                    #self is the column object
                    #fcobj is the calling object that contains that column (so this is the real self).
                    #foreign class is the string name of the foreign class.
                    myfcoldatainfoobj = mycolobj.genForeignKeyDataObjectInfo(self);
                    #print(f"\nmyfcoldatainfoobj = {myfcoldatainfoobj}\n");

                    myclsref = myfcoldatainfoobj["fclassref"];
                    myfcols = myfcoldatainfoobj["myfcols"];
                    myfccolnames = myfcoldatainfoobj["myfccolnames"];
                    mycolis = myfcoldatainfoobj["mycolis"];
                    mcolobjs = myfcoldatainfoobj["mcolobjs"];
                    myvalidator.varmustnotbenull(self, "self");
                    myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                    #names referenced by the foreign key
                    #print(f"mycolobj.foreignColNames = {mycolobj.foreignColNames}");
                    #print(f"myfccolnames = {myfccolnames}");#all of the col names in the foreign class
                    
                    myvalidator.listMustContainUniqueValuesOnly(mycolobj.foreignColNames,
                                                                "mycolobj.foreignColNames");

                    #print(f"mycolis = {mycolis}");

                    #now get that column object and check to see if the isunique is set to true?
                    #OR is primary key and the only primary key on that table?
                    #print(f"mcolobjs = {mcolobjs}");

                    for n in range(len(valcl)):
                        itemval = valcl[n];
                        dtpval = mvaldtp[n];
                        #print(f"itemval = {itemval}");
                        #print(f"dtpval = {dtpval}");
                        #print(f"mcolobjs[{n}].getColName() = {mcolobjs[n].getColName()}");
                        #print(f"mycolobj.foreignColNames[{n}] = {mycolobj.foreignColNames[n]}");
                        #print(f"issigned = {mcolobjs[n].getIsSigned()}");
                        #print(f"isnonnull = {mcolobjs[n].getIsNonNull()}");

                        if (mcolobjs[n].getColName() == mycolobj.foreignColNames[n]): pass;
                        else: raise ValueError("the col names must match, but they did not!");

                        if (myvalidator.isValueValidForDataType(dtpval, itemval, varstr,
                                                                not(mcolobjs[n].getIsSigned()),
                                                                mcolobjs[n].getIsNonNull())):
                            pass;
                        else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
                    
                    #print("setting the column " + clnm + " to the value " + str(valcl) + " here!");
                    setattr(self, clnm + "_value", valcl);
                    self.runValidatorsByKeysForClass([clnm]);
                    #mycol.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                    #myvalidator.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                    #print("value set successfully!");
                else: return self.setValueForColName(clnm, valcl[0], mycolobj);
            else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
        else:
            if (myvalidator.isValueValidForDataType(mvaldtp, valcl, varstr, not(mycolobj.getIsSigned()),
                                                    mycolobj.getIsNonNull())):
                #print("setting the column " + clnm + " to the value " + str(valcl) + " here!");
                setattr(self, clnm + "_value", valcl);
                self.runValidatorsByKeysForClass([clnm]);
                #mycol.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                #myvalidator.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                #print("value set successfully!");
            else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
        if (mycolobj.isforeignkey): mybase.updateAllForeignKeyObjectsForAllClasses(False);
    def setValueForColumn(self, clnm, valcl, mycolobj=None):
        self.setValueForColName(clnm, valcl, mycolobj=mycolobj);
    def setValueForCol(self, clnm, valcl, mycolobj=None):
        self.setValueForColName(clnm, valcl, mycolobj=mycolobj);
    def setColValue(self, clnm, valcl, mycolobj=None):
        self.setValueForColName(clnm, valcl, mycolobj=mycolobj);
    def setColumnValue(self, clnm, valcl, mycolobj=None):
        self.setValueForColName(clnm, valcl, mycolobj=mycolobj);
    
    def genValsListForColNames(self, colnames):
        #get a list of values for colnames then return tuple of it
        myvalidator.varmustnotbeempty(colnames, "colnames");
        return [self.getValueForColName(cnm) for cnm in colnames];

    def genValsTupleForColNames(self, colnames):
        #get a list of values for colnames then return tuple of it
        myvalidator.varmustnotbeempty(colnames, "colnames");
        return tuple(self.genValsListForColNames(colnames));

    def genSimpleValsDict(self, mycols=None):
        mdict = {};
        for ky in type(self).getValueColNames(mycols=mycols): mdict[ky] = getattr(self, ky);
        return mdict;
    
    
    #properties of the base class, but the self type should not be mybase

    def getLastSyncedValsDict(self): return self._lastsyncedvalsdict;

    def setLastSyncedValsDict(self, mval): self._lastsyncedvalsdict = mval;

    lastsyncedvalsdict = property(getLastSyncedValsDict, setLastSyncedValsDict);

    def getUserProvidedColNames(self): return self._userprovidedcolnames;

    def setUserProvidedColNames(self, mval):
        myvalidator.varMustBeAListOfColNameStringsOrEmpty(mval, "userprovidedcolnames");
        self._userprovidedcolnames = mval;

    userprovidedcolnames = property(getUserProvidedColNames, setUserProvidedColNames);

    def getColNamesWithDefaultsUsed(self): return self._colnmswdefaultsused;

    def setColNamesWithDefaultsUsed(self, mval):
        myvalidator.varMustBeAListOfColNameStringsOrEmpty(mval, "colnmswdefaultsused");
        self._colnmswdefaultsused = mval;

    colnmswdefaultsused = property(getColNamesWithDefaultsUsed, setColNamesWithDefaultsUsed);
    
    def getColNamesWithDBValsUsed(self): return self._colnmswdbvalsused;

    def setColNamesWithDBValsUsed(self, mval):
        myvalidator.varMustBeAListOfColNameStringsOrEmpty(mval, "colnmswdbvalsused");
        self._colnmswdbvalsused = mval;

    colnmswdbvalsused = property(getColNamesWithDBValsUsed, setColNamesWithDBValsUsed);

    
    #returns None if not found instead of throwing an error
    @classmethod
    def getObjectFromGivenKeysAndValues(cls, mlist, keys, values):
        #print(f"mlist = {mlist}");
        #print(f"keys = {keys}");
        #print(f"values = {values}");

        tperrmsg = "invalid data type found and used here for the values! There are multiple keys, ";
        tperrmsg += "so there must be multiple values!";
        if (myvalidator.isvaremptyornull(mlist)): return None;
        else:
            klen = len(keys);
            isvalslist = (type(values) in [list, tuple]);
            #print(f"klen = {klen}");
            #print(f"isvalslist = {isvalslist}");

            if (klen == 1): pass;
            elif (1 < klen):
                if (type(values) in [list, tuple]): pass;
                else: raise TypeError(tperrmsg);
            if (isvalslist): pass;
            else:
                if (klen == 1): pass;
                else: raise TypeError(tperrmsg + " BUT the values was not a list!");
            
            for mobj in mlist:
                fndallvals = True;
                for n in range(klen):
                    mattr = keys[n];
                    mval = (values[n] if (isvalslist) else values);
                    #print(f"mattr = {mattr}");
                    #print(f"mval = {mval}");

                    if (hasattr(mobj, mattr + "_value")):
                        if (mval == getattr(mobj, mattr + "_value")): pass;
                        else:
                            #print("not found on this object moving on to the next one!");
                            fndallvals = False;
                            break;
                    else: return None;
                if (fndallvals): return mobj;
        
            #print("the object with those values for those columns was not found on the list!");
            return None;

    def getForeignKeyObjectFromCol(self, mc):
        #print(f"mc = {mc}");
        myvalidator.varmustnotbenull(mc, "mc");
        #using the foreign key column information stored in the column,
        #we can get attributes like foreignClass="Camper", foreignColNames=["id"], and
        #our colname="camper_id"
        #we can then notice that the object will be called the classname but lower case first letter
        #if it is the same case as the letter it will be the opposite case.
        #or we can force the case here...
        #now we know what to call it (varname in the setattr call).
        #the value is what we need
        #first of all, if it exists on the list of objects, then we can return the object
        #if it does not exist on the list of objects, then we can return None or attempt
        #to get it from the DB. or force resync then do it here...
        #if not found, return None. Either the user entered invalid information or it does not exist.
        #setattr(self, nm, val);
        #What if there are multiple foreign key columns that refer to the same class?
        #There may be two objects that are different.
        #The two objects supposedly created should not be named the same.
        #Therefore, the foreign key object name should be required,
        #or specified by the user that the user does not want an object created for one or the other.
        #stringMustContainOnlyAlnumCharsIncludingUnderscores(cls, mstr, varnm="varnm");
        #stringContainsOnlyAlnumCharsIncludingUnderscores(cls, mstr)
        #fkyobjname from col
        if (type(self).needToCreateAnObjectForCol(mc)):
            #print("WE NEED TO CREATE AN OBJECT FOR THE COLUMN HERE!");
            #fkyobjnmfromcl = mc.getForeignObjectName();
            #we depend on it, but do not need it here if not calling setattr
            #using the foreign class and the attributes and values specified in the column
            #look up the object from the list...
            mcnm = mc.getForeignClass();
            mcref = None;
            try:
                mcref = mycol.getMyClassRefFromString(mcnm);
            except Exception as ex:
                #traceback.print_exc();
                print(f"class name {mcnm} not found!");
                return None;
            #print(f"GOT THE REFERENCE CLASS NAME {mcref.__name__}!");
            #print(f"foreign col names = {mc.getForeignColNames()}");
            #print(f"my col name = {mc.getColName()}");
            mval = None;
            try:
                mval = self.getValueForColName(mc.getColName());
            except Exception as ex:
                #traceback.print_exc();
                print(f"col name {str(mc.getColName() + '_value')} not found!");
                return None;
            #get the object here...
            mobj = type(self).getObjectFromGivenKeysAndValues(mcref.all, mc.getForeignColNames(), mval);
            #now we can maybe call setattr here... or just return...
            return mobj;
        else: return None;

    @classmethod
    def needToCreateAnObjectForCol(cls, mc):
        myvalidator.varmustbethetypeonly(mc, mycol, "mc");
        fobjnm = mc.getForeignObjectName();
        if (myvalidator.isvaremptyornull(fobjnm)): return False;
        else:
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(fobjnm, "fobjnm");
            return True;

    def getForeignKeyObjectsFromCols(self, mycols=None):
        #get the foreign key cols
        #then for each col
        return [self.getForeignKeyObjectFromCol(mc) for mc in type(self).getMyForeignKeyCols(mycols)
                if (type(self).needToCreateAnObjectForCol(mc))];

    
    #dynamic properties for class objects from the foreign keys set here

    #these links were not that helpful, but did provide some insight into the problem:
    #https://stackoverflow.com/questions/60686572/dynamic-property-getter-and-setter
    #https://stackoverflow.com/questions/10967551/how-do-i-dynamically-create-properties-in-python
    #https://stackoverflow.com/questions/37869030/how-to-programmatically-define-properties-in-python
    
    #remember in Python properties have the normal property name and the private name
    #remember to set the private name initially to an initial value first to prevent not found
    #remember to get from the private name to prevent an infinite loop
    #remember to set both the private name and public name property to the new value.
    #when I say public name think camper.
    #when I say private name think _camper.
    #one other thing, for the dynamic property to work, your getters and setters must return a function.
    #therefore these getters and setters are kind of like decorators.
    #keep in mind you can also use a property decorator like this:
    #@property
    #def prop(self): return self._name;
    #
    #@property.setter
    #def prop(self, val): self._name = val;
    #
    #the normal example is:
    #def mygettername(self): return self._name;
    #
    #def mysettername(self, val): self._name = val;
    #
    #name = property(mygettername, mysettername);

    def myObjectGet(self, attrnm):
        def fget(self):
            #print("INSIDE GET!");
            #print(f"attrnm = {attrnm}");
            myattval = getattr(self, "_" + attrnm);
            #myattval = __getattr__(self, attrnm);
            #print(f"myattval = {myattval}");
            return myattval;
        return fget;

    def myObjectSet(self, attrnm):
        def fset(self, val):
            #print("INSIDE SET!");
            #print(f"attrnm = {attrnm}");
            #print(f"val = {val}");
            myattval = getattr(self, attrnm);
            myattval = val;
            #myattval.value = val;
            setattr(self, "_" + attrnm, val);
            #print("DONE WITH SET!");
        return fset;

    def getAndSetForeignKeyObjectsFromCols(self, mycols=None):
        mobjnms = self.getForeignKeyObjectNamesFromCols(mycols);
        #print(f"mobjnms = {mobjnms}");

        mobjs = self.getForeignKeyObjectsFromCols(mycols);
        #print(f"mobjs = {mobjs}");

        myvalidator.listMustContainUniqueValuesOnly(mobjnms, "mobjnms");
        myvalidator.twoArraysMustBeTheSameSize(mobjnms, mobjs);

        for n in range(len(mobjnms)):
            mobj = mobjs[n];
            mnm = mobjnms[n];
            #print(f"mobj = {mobj}");
            #print(f"mnm = {mnm}");
            
            #setattr(self, mnm, mobj);
            setattr(type(self), mnm, property(self.myObjectGet(mnm), self.myObjectSet(mnm)));
            setattr(self, "_" + mnm, mobj);
            
            #properties need a get, set functions as well as a name
            #properties are applied to the class only not just the self object...
            #but you cannot only do it on self, otherwise the access methods will not be enforced.
            #properties have a certain name like camper
            #but to access it you need to do self._camper ...
            #
            #so first you need to create the property
            #then you need to set the private value
            #now you can try getting the value, but the getter needs to pull it from the private value
            #then you can officially attempt to set the value using the property
            #this will then tell the setter to get the current value of the property and say it is val
            #then set the private value
            
            
            #print("val of the new attribute should be the initial value!");
            #print(getattr(self, mnm));
            #print(getattr(self, mnm).fget(self));#does not work now
            
            #print("now setting the value here.");
            #getattr(self, mnm).fset(self, mobj);#does not work now
            setattr(self, mnm, mobj);
            #print("val of the property should now be the object!");
            #print(getattr(self, mnm));
        return mobjs;

    #update all foreign key objects methods:
    
    @classmethod
    def updateAllForeignKeyObjectsForMyClass(cls):
        #from myorm.mybase import mybase;
        if (issubclass(cls, mybase)):
            if (myvalidator.isvaremptyornull(cls.all)): pass;
            else:
                #print(f"\nBEGIN WORKING ON THOSE FOR {cls.__name__}!");
                for mobj in cls.all: mobj.getAndSetForeignKeyObjectsFromCols(cls.getMyCols());
                #print(f"\nDONE WITH THOSE FOR {cls.__name__}!");

    @classmethod
    def updateAllForeignKeyObjectsForAllClasses(cls, ftchnw=False):
        print("\nUPDATING ALL OBJECT REFS FROM FOREIGN KEYS NOW:\n");
        myvalidator.varmustbeboolean(ftchnw, "ftchnw");
        mlist = mycol.getMyClassRefsMain(ftchnw);
        if (myvalidator.isvaremptyornull(mlist)): pass;
        else:
            for mclsref in mlist:
                #from myorm.mybase import mybase;
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)):
                    mclsref.updateAllForeignKeyObjectsForMyClass();   
        print("DONE UPDATING ALL OBJECT REFS FROM FOREIGN KEYS NOW!");

    @classmethod
    def updateAllLinkRefsForAllClasses(cls, ftchnw=False):
        print("\nUPDATING ALL LINK REFS FROM FOREIGN KEYS NOW:\n");
        myvalidator.varmustbeboolean(ftchnw, "ftchnw");
        mlist = mycol.getMyClassRefsMain(ftchnw);
        if (myvalidator.isvaremptyornull(mlist)): pass;
        else:
            for mclsref in mlist:
                #from myorm.mybase import mybase;
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)):
                    mclsref.updateAllLinkRefsForMyClass();#mclsref.setupPartB(True);
        print("DONE UPDATING ALL LINK REFS FROM FOREIGN KEYS NOW!");

    def printValuesForAllCols(self, mycols=None):
        fincols = type(self).getMyColsFromClassOrParam(mycols);
        for mc in self.getMyColNames(fincols):
            print(f"val for colname {mc} is: {self.getValueForColName(mc)}");
    
    
    @classmethod
    def getTableAndClassNameString(cls):
        return "the table " + cls.getTableName() + " on class " + cls.__name__;


    #database CRUD methods section may depend on which database itself you are using.

    #NOT DONE YET WITH ALL OF THESE 4-30-2025 9:30 PM MST

    #depends on the table name
    #convenience method that calls the method in the myvalidator for generating the
    #CREATE TABLE SQL query.
    #
    #DEPENDS ON THE SQL VARIANT or SQLVARIANT.
    @classmethod
    def genSQLCreateTableFromRef(cls, varstr=None, onlyifnot=True, isinctable=True):
        if (myvalidator.isvaremptyornull(varstr)):
            return cls.genSQLCreateTableFromRef(varstr="" + mybase.getMySQLType(),
                                                onlyifnot=onlyifnot, isinctable=isinctable);
        return myvalidator.genSQLCreateTable(cls.getTableName(), varstr, cls.getMyCols(),
                                             cls.getMultiColumnConstraints(),
                                             cls.getAllTableConstraints(), onlyifnot=onlyifnot,
                                             isinctable=isinctable);
    #DEPENDS ON THE SQL VARIANT or SQLVARIANT.
    @classmethod
    def createTable(cls):
        #if the table exists and onlyifnot is False, then it will fail because the table already exists
        #if the table exists and onlyifnot is True, then it will not create a new table,
        #and essentially do nothing
        #it may still fail due to another reason, but this is not my fault unless it is a bad query.
        
        for mc in cls.getMyCols():
            mc.primaryKeyInformationMustBeValid(cls);
            mc.foreignKeyInformationMustBeValid(fcobj=None, usenoclassobj=True);
        
        qry = cls.genSQLCreateTableFromRef(varstr="" + mybase.getMySQLType(), onlyifnot=False,
                                           isinctable=True);
        print(f"\nCREATE TABLE qry = {qry}\n");
        
        #this either failed because the table already exists or fails for some other reason
        #the user should be informed because it means there is a problem with the user's program
        res = mybase.getMyCursor().execute(qry);
        mybase.getMyConn().commit();
        print("created " + cls.getTableAndClassNameString() + " on the DB successfully!\n");
        return True;

    @classmethod
    def tableExists(cls, pqry=True):
        #some databases do not support the PRAGMA command.
        #in fact PRAGMA is only supported by SQL LITE. SQL has some other ways and it depends on the DB.
        #however, if the SELECT fails, that means that the table does not exist.
        #all databases and dialects of SQL support SELECT so, the SELECT command of SQL will be used.
        myvalidator.varmustbeboolean(pqry, "pqry");
        qry = myvalidator.genSelectAllOnlyOnTables([cls.getTableName()], useseldistinct=False);
        qry += " " + myvalidator.genSQLimit(1, offset=0);
        if (pqry): print(f"\nTABLE EXISTS qry = {qry}\n");
        
        exists = True;
        try:
            res = mybase.getMyCursor().execute(qry).fetchall();
            mybase.getMyConn().commit();
        except Exception as ex:
            #if (pqry): print(f"\nTABLE EXISTS qry = {qry}\n");
            #traceback.print_exc();
            exists = False;
        
        if (pqry):
            print(f"\nTHE TABLE " + ("EXISTS" if (exists) else "DOES NOT EXIST") + " ON THE DB!\n");

        return exists;

    @classmethod
    def genSQLInsertIntoFromRef(cls, vals=None):
        return myvalidator.genSQLInsertInto(cls.getTableName(), cls.getMyColNames(), vals);
    

    #BACKUP AND RESTORE METHODS NOT DONE YET 5-25-2025 12:04 AM MST
    
    #NEED A METHOD TO ATTEMPT TO ADD DATA BACK AFTER A NEW COL IS ADDED
    # OR A NEW CONSTRAINT OR A NEW TABLE NAME, ETC.

    #https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python
    @classmethod
    def restoreDBFromSQLFile(cls, filepathandnm):
        myvalidator.stringMustHaveAtMinNumChars(filepathandnm, 4, "filepathandnm");
        myvalidator.stringMustEndWith(filepathandnm, ".sql", "filepathandnm");
        mscrpt = None;
        with open(filepathandnm, "r") as mfile:
            mscrpt = mfile.read();
            mfile.close();
        mybase.getMyCursor().executescript(mscrpt);
        mybase.getMyConn().commit();
        print("DB SUCCESSFULLY RESTORED!");
    
    @classmethod
    def restoreDBFromPyFile(cls, filepathandnm):
        #this method is a possible security problem.
        myvalidator.stringMustHaveAtMinNumChars(filepathandnm, 3, "filepathandnm");
        myvalidator.stringMustEndWith(filepathandnm, ".py", "filepathandnm");
        import os;
        os.system("python " + filepathandnm);
        print("DONE EXECUTING THE RESTORE FILE!");
    
    @classmethod
    def dataOnlyFileMustBeInTheCorrectFormat(cls, mlines):
        lineswithclsonthem = myvalidator.getLineIndexesWithStringOnIt("class", mlines);
        ctbllines = myvalidator.getLineIndexesWithStringOnIt("and the create table statement is:",
                                                             mlines);
        dtaline = myvalidator.getLineIndexesWithStringOnIt("and the data: [", mlines);
        print("\nbegin make sure that the backup data file is in the correct format now:");
        print(f"lineswithclsonthem = {lineswithclsonthem}");
        print(f"ctbllines = {ctbllines}");
        print(f"dtaline = {dtaline}\n");
        
        mxitems = len(lineswithclsonthem);
        for n in range(mxitems):
            bglineindx = lineswithclsonthem[n];
            exptctblindx = bglineindx + 2;
            actctblindx = ctbllines[n];
            clstbleexists = ("EXISTS" in mlines[bglineindx]);
            print(f"clstbleexists = {clstbleexists}");
            print(f"exptctblindx = {exptctblindx}");
            print(f"actctblindx = {actctblindx}");
            
            if (exptctblindx == actctblindx): pass;
            else: raise ValueError("(1A) backup file is in the wrong format!");
            if (clstbleexists):
                if (1 < len(mlines[actctblindx + 1])): pass;
                else: raise ValueError("(1B) backup file is in the wrong format!");
            else:
                if (1 < len(mlines[actctblindx + 1])):
                    raise ValueError("(1C) backup file is in the wrong format!");
            exptdtlindx = exptctblindx + 2;
            actdtlindx = dtaline[n];
            print(f"exptdtlindx = {exptdtlindx}");
            print(f"actdtlindx = {actdtlindx}");
            
            if (exptdtlindx == actdtlindx): pass;
            else: raise ValueError("(2) backup file is in the wrong format!");
            nxtbglineindx = (lineswithclsonthem[n + 1] if (n + 1 < mxitems) else len(mlines));
            diffnxtclsdatline = nxtbglineindx - actdtlindx;
            print(f"nxtbglineindx = {nxtbglineindx}");
            print(f"(must be at least 1) diffnxtclsdatline = {diffnxtclsdatline}");
            
            if (0 < diffnxtclsdatline): pass;
            else: raise ValueError("(3A) backup file is in the wrong format!");
            if (clstbleexists): pass;
            else:
                if (diffnxtclsdatline == 1): pass;
                else: raise ValueError("(3B) backup file is in the wrong format!");
            diffnxtclslineandprev = nxtbglineindx - bglineindx;
            print(f"(must be at least 5) diffnxtclslineandprev = {diffnxtclslineandprev}");
            
            if (4 < diffnxtclslineandprev): pass;
            else: raise ValueError("(4) backup file is in the wrong format!");

        print("\nbackup data only file is in the correct format!\n");
        return True;

    @classmethod
    def restoreDBFromDatOnlyFile(cls, filepathandnm):
        #this method is a possible security problem.
        #dat only file is in the following format (this may change):
        #class classname EXISTS/DOES NOT EXIST and has colnames:\n
        #[colnames for the class here in the list of strings]\n
        #and the create table statement is:\n
        #(line will be empty if table does not exist
        # otherwise this line has the entire create table statement)
        #and the data: []\n or ends after [\n
        #and then prints one row of each table here... as tuples\n
        #...\n
        #]\n
        #this line will have the next class on it or will be blank
        myvalidator.stringMustHaveAtMinNumChars(filepathandnm, 5, "filepathandnm");
        myvalidator.stringMustEndWith(filepathandnm, ".txt", "filepathandnm");
        mlines = None;
        with open(filepathandnm, "r") as mfile:
            mlines = mfile.readlines();
            mfile.close();
        print("BEGIN PRINTING THE FILE LINES HERE:");
        #print(f"mlines = {mlines}");
        for line in mlines: print(line[0:len(line) - 1]);
        
        #first we need to know where our bounds are for each class...
        lineswithclsonthem = myvalidator.getLineIndexesWithStringOnIt("class", mlines);
        ctbllines = myvalidator.getLineIndexesWithStringOnIt("and the create table statement is:",
                                                             mlines);
        dtaline = myvalidator.getLineIndexesWithStringOnIt("and the data: [", mlines);
        cls.dataOnlyFileMustBeInTheCorrectFormat(mlines);

        #we care if the table exists...
        #we care about the create table statement...
        #we care about the data lines if there is data...
        #we care what the data is...
        mxitems = len(lineswithclsonthem);
        for n in range(mxitems):
            bglineindx = lineswithclsonthem[n];
            ctblineindx = ctbllines[n];#execute directly
            dtlindx = dtaline[n];#look at first line
            nxtbglineindx = (lineswithclsonthem[n + 1] if (n + 1 < mxitems) else len(mlines));
            diffnxtclsdatline = nxtbglineindx - dtlindx;
            bgline = mlines[bglineindx];
            clstbleexists = ("EXISTS" in bgline);
            tnmindx = bgline.index("with tablename: ");
            tnmnxtspcindx = -1;
            for i in range(tnmindx + 16, len(bgline)):
                if (bgline[i] == ' '):
                    tnmnxtspcindx = i;
                    break;
            myvalidator.valueMustBeInRange(tnmnxtspcindx, tnmindx + 17, len(bgline) - 1,
                                           True, True, "tnmnxtspcindx");
            tname = bgline[tnmindx + 16:tnmnxtspcindx];
            print(f"tname = {tname}");
            #print(f"len(tname) = {len(tname)}");
            #add a drop table if exists and then execute it
            #then execute the create table statement
            #then add the data
            dpqry = myvalidator.genSQLDropTable(tname, True);
            print(f"DROP TABLE QUERY dpqry = {dpqry}");

            try:
                mybase.getMyCursor().execute(dpqry);
                mybase.getMyConn().commit();
            except Exception as ex:
                print("either the table already does not exist or problem connecting with the DB!");
                traceback.print_exc();
            
            if (clstbleexists):
                if (len(mlines[ctblineindx + 1]) == 1): pass;#no create table statement
                else:
                    #there is a create table statement
                    ctbleqry = mlines[ctblineindx + 1][0:len(mlines[ctblineindx + 1]) - 1];
                    print(f"CREATE TABLE QUERY: {ctbleqry}");
                    
                    try:
                        mybase.getMyCursor().execute(ctbleqry);
                        mybase.getMyConn().commit();
                    except Exception as ex:
                        print("either the table already exists or problem connecting to the DB!");
                        raise ex;
                if (diffnxtclsdatline == 1): pass;#no data on the table
                else:
                    #the diff is more than 1
                    #either subtract 1 or 2 lines depending on how it is generated
                    #need to start 1 more than the data only line start indicator.
                    #line 2 is the colnames ,s cannot be in them neither can quotes we can use split
                    cnmsline = mlines[bglineindx + 1];
                    mycnmsstr = cnmsline[2:len(cnmsline) - 3];
                    mcnms = myvalidator.mysplitWithDelimeter(mycnmsstr, "', '");
                    print(f"cnmsline = {cnmsline}");
                    print(f"mycnmsstr = {mycnmsstr}");
                    print(f"mcnms = {mcnms}");
                    
                    #https://stackoverflow.com/questions/8494514/converting-string-to-tuple
                    from ast import literal_eval;#this is a possible security problem.
                    for k in range(diffnxtclsdatline - 2):
                        #need to convert the string to a tuple
                        #then this will be the vals tuple passed in to the query method
                        myiline = mlines[dtlindx + 1 + k][0:len(mlines[dtlindx + 1 + k]) - 1];
                        mtp = tuple(literal_eval(myiline));
                        print(f"myiline = {myiline}");
                        print(f"mtp = {mtp}");
                        
                        mnwdatqry = myvalidator.genSQLInsertInto(tname, mcnms, vals=None);
                        print(f"mnwdatqry = {mnwdatqry}");
                        
                        mybase.getMyCursor().execute(mnwdatqry, mtp);
                        mybase.getMyConn().commit();
        print("DB successfully restored from the backup data only file!");
        return True;

    #NOT DONE YET RESTORING THE DB 5-29-2025 8:56 PM

    #old data 0
    #old data and new names only 1
    #new data only 2
    #old data and new data 3
    @classmethod
    def getIfLineRequiresNewOldOrBothData(cls, cloglines):
        if (myvalidator.isvaremptyornull(cloglines)): return [];
        else:
            #print("\nThe CHANGE LOG HAS:\n");
            #for line in cloglines: print(line);
            #print();
            
            #determining if we need new data or just the old or both:
            #
            #if [a col, a table, a constraint] was renamed what the old name was and
            # what the new name is
            #-we need the old data only.
            #-renaming all of these effects the create table statement
            #--when it is a constraint that is the only thing that got changed though
            #--we can get the new name from the class file in this case
            #-renaming a table or a col on a table effects everything that refers to it
            #--like foreign keys on other tables might no longer be valid until they are changed
            #
            #if [a col, a table, a constraint] was added or removed (the count will be different)
            #-for removal we only need the old data only;
            #-for addition we need the new data only
            #--(except for the constraint, but this will change what old data is legal).
            #if some other property of a col or a constraint was changed like data type,
            # we need new data
            #-ideally we treat this as creating something new; new data only.
            #
            #rnm table from old_name to new_name
            #rnm col from old_name to new_name on table_name
            #rnm cons from old_name to new_name on table_name
            #del/add col col_name on table_name
            #del/add table table_name
            #del/add cons cons_name on table_name
            #del/add icolcons type from col_name on table_name
            
            #old data 0
            #old data and new names only 1
            #new data only 2
            #old data and new data 3
            #print("old data is 0\nold data new names only is 1\nnew data only 2");
            #print("old and new data is 3");
            mlist = [];
            for line in cloglines:
                #if (myvalidator.lineHasStringOnItAtIndex("rnm", line, 0))
                if ("rnm" in line and line.index("rnm") == 0):
                    #old data and the new names only
                    mlist.append(1);
                elif ("del" in line and line.index("del") == 0):
                    #removing something here, old data only
                    mlist.append(0);
                elif ("add" in line and line.index("add") == 0):
                    #if adding a new table we need new data
                    #if adding a new col on a table we need new data and old data
                    #if adding a new constraint we need old data
                    #if adding a new individual col constraint (changing data type) new data
                    if ("table" in line and line.index("table") == 4): mlist.append(2);
                    elif ("col" in line and line.index("col") == 4): mlist.append(3);
                    elif ("cons" in line and line.index("cons") == 4): mlist.append(0);
                    elif ("icolcons" in line and line.index("icolcons") == 4): mlist.append(3);
                    else: raise ValueError("the change log added and invalid type of something to it!");
                else: raise ValueError("the change log line started with something invalid!");

            #mlist = [(1 if ("rnm" in line and line.index("rnm") == 0) else
            #         (0 if ("del" in line and line.index("del") == 0) else
            #          ((2 if ("table" in line and line.index("table") == 4) else
            # (3 if ("col" in line and line.index("col") == 4) else 
            # (0 if ("cons" in line and line.index("cons") == 4) else
            # (3 if ("icolcons" in line and line.index("icolcons") == 4) else -1))))
            # if ("add" in line and line.index("add") == 0) else -1))) for line in cloglines];
            #for num in mlist: myvalidator.valueMustBeInMinAndMaxRange(num, 0, 3, "num");
            return mlist;

    @classmethod
    def restoreDBFromDatFileAndChangeLog(cls, filepathandnm, cloglines, newdatarr=None):
        #at any rate, we need to:
        #1. back up the data (if that has not already been done so),
        #-but the backup files will have the OLD create table statement and all old data
        #--even the insert into commands will be different.
        #-when we restore the data, we want to use the NEW create table statement
        #-we also want to use the NEW insert into statements
        #-we may also need the user to provide new information if the cols have changed
        #-if the col names got renamed, then the restore will need to know what the
        #--old col names were and will need to map it with the new ones
        #-if new cols are added or are totally different,
        #--then the restore will need to know the new data...
        #-the backup methods do not change the existing objects in memory
        #--the user might be able to take advantage of this and update the data this way.
        #--however if the objects did not exist when running the restore,
        #---the user may not have access to them.
        #
        #if we just added or dropped a constraint only the old data will be used.
        #--(if added a constraint some of the old data might not get restored).
        #if we added a new column entirely, we need new data and the old data.
        #if we change data types for one col, we need new data for that col and the old data.
        #if we just renamed column names, then we only need old data with the new names.
        #if we just deleted a column entirely, we need the old data new names.
        #if we just renamed a table name, then we need the old name and the one.
        #if we just deleted an entire table, then only the old data will be used.
        #if a combination is used it depends on what changes were made will determine
        #-if we need new only or old only or both old and new data.
        #
        #2. get rid of the current table,
        #3. then add the new constraint
        #4. then create the new table
        #5. then attempt to restore the old data
        

        #we may just want to backup only a specific table and not all of them to save space
        #this may be a good idea, but it can bite you in the ass when you go to restore it...
        

        #-new_data object or list of objects or something like that
        #-old_data from one of the restore files methods and we want to know which one
        #--the file will probably be the SQL file or the data only file,
        #---not the script unless it was custom built for this
        #-change log either file or data object that the user provides
        #--(the mapping from the old data to the new data...)
        

        #determining if we need new data or just the old or both:
        #
        #if [a col, a table, a constraint] was renamed what the old name was and what the new name is
        #-we need the old data only.
        #-renaming all of these effects the create table statement
        #--when it is a constraint that is the only thing that got changed though
        #--we can get the new name from the class file in this case
        #-renaming a table or a col on a table effects everything that refers to it
        #--like foreign keys on other tables might no longer be valid until they are changed
        #
        #if [a col, a table, a constraint] was added or removed (the count will be different)
        #-for removal we only need the old data only;
        #-for addition we need the new data only
        #--(except for the constraint, but this will change what old data is legal).
        #if some other property of a col or a constraint was changed like data type, we need new data
        #-ideally we treat this as creating something new; new data only.
        
        #the old and new data need to be formatted the same.
        #in that the old data is a list of tuples for a list of tables
        #with a list of colnames for those tables.
        
        #what needs to be on the change log after said table exists?
        #when does the change log need to start tracking changes?
        #when should the change log be cleared?
        #
        #rnm table from old_name to new_name
        #rnm col from old_name to new_name from table_name
        #rnm cons from old_name to new_name from table_name
        #del/add col col_name from table_name
        #del/add table table_name
        #del/add cons cons_name from table_name
        #del/add icolcons type from col_name from table_name
        
        #which file is best to get the data from? We have the datonly, the sqlcmdsonly, scrpt file.
        #A: the script file is a small short script that executes the sql commands stored in it.
        #B: the sql file which has all of the sql commands only.
        #C: the data only file has the class name, table name, col names, create table statement,
        #-and the data
        #-it may or may not have the create table statement if the table was never on the DB
        #
        #if we use the datonly file, we can match it via classname or tablename
        #if the cols have changed we just subsitute the new cols for the old ones
        #then pull the old data
        #but we still need the new data in some cases
        #
        #we will use the data only file as it is the most complete...
        myvalidator.stringMustHaveAtMinNumChars(filepathandnm, 5, "filepathandnm");
        myvalidator.stringMustEndWith(filepathandnm, ".txt", "filepathandnm");
        if (myvalidator.isvaremptyornull(cloglines)):
            return cls.restoreDBFromDatOnlyFile(filepathandnm);
        #if above only has 0s the other method will work fine.
        dtrequsrnumslist = mybase.getIfLineRequiresNewOldOrBothData(cloglines);
        hasnummorethanzero = False;
        hasnummorethanone = False;
        for n in dtrequsrnumslist:
            if (n == 0): pass;
            elif (0 < n and n < 4):
                if (hasnummorethanzero): pass;
                else: hasnummorethanzero = True;
                #break;
                if (1 < n and n < 4):
                    if (hasnummorethanone): pass;
                    else: hasnummorethanone = True;
            else: raise ValueError("invalid number found and use here!");
        mlines = None;
        with open(filepathandnm, "r") as mfile:
            mlines = mfile.readlines();
            mfile.close();
        print("BEGIN PRINTING THE FILE LINES HERE:");
        #print(f"mlines = {mlines}");
        for line in mlines: print(line[0:len(line) - 1]);
        
        #first we need to know where our bounds are for each class...
        lineswithclsonthem = myvalidator.getLineIndexesWithStringOnIt("class", mlines);
        ctbllines = myvalidator.getLineIndexesWithStringOnIt("and the create table statement is:",
                                                             mlines);
        dtaline = myvalidator.getLineIndexesWithStringOnIt("and the data: [", mlines);
        cls.dataOnlyFileMustBeInTheCorrectFormat(mlines);

        #what to do if the table already exists on the DB?
        #what do we do if the table does not exist on the DB?
        #how do we know if a table has changes or not?
        #what to do if we have no changes for the table?
        #what to do if we have changes for the table? well this depends on what they are.
        
        #determine if each change requires new data etc (dtrequsrnumslist has that info)
        print("\nThe CHANGE LOG HAS:\n");
        allfintnmsflines = [];
        allprevtnms = [];
        mydeltablenms = [];#list will contain duplicates
        myaddtlinenums = [];
        mydeltlinenums = [];
        myaddtablenms = [];#list will contain duplicates
        isatleastoneprevnm = False;
        for n in range(len(cloglines)):
            line = cloglines[n];
            #there are only two or three commands that will not have it like this that is
            #when we are:
            #add/del table table_name or
            #rnm table oldtnm to newtnm
            #we want the last index of on table_name
            hasprevnm = False;
            #mydeltnm = myvalidator.lineHasMSTROnItAtIndex("del table", line, 0);
            mydeltnm = ("del table " in line and line.index("del table ") == 0);
            myaddtnm = ("add table " in line and line.index("add table ") == 0);
            if (myaddtnm or mydeltnm): si = 10;
            elif ("rnm table " in line and line.index("rnm table ") == 0 and " to " in line):
                si = line.rindex(" to ") + 4;
                oldnmsi = 15;#ignore the from space part (5) and ignore the rnm table part (10)
                oldnmei = si - 4;
                oldtnm = line[oldnmsi:oldnmei];
                hasprevnm = True;
                if (isatleastoneprevnm): pass;
                else: isatleastoneprevnm = True;
                allprevtnms.append(oldtnm);
            elif (" on " in line): si = line.rindex(" on ") + 4;
            else: raise ValueError("the change log line was in the wrong format!");
            tnmfline = line[si:];
            allfintnmsflines.append(tnmfline);
            if (myaddtnm):
                myaddtablenms.append(tnmfline);
                myaddtlinenums.append(n); 
            if (mydeltnm):
                mydeltablenms.append(tnmfline);
                mydeltlinenums.append(n);
            if (hasprevnm): pass;
            else: allprevtnms.append("");#tnmfline
            print(str(dtrequsrnumslist[n]) + " | " + line);
        print();
        print("the numbers on the left of the | mean:");
        print("old data is 0\nold data new names only is 1\nnew data only 2");
        print("old and new data is 3\n");
        print(f"hasnummorethanzero = {hasnummorethanzero}");
        print(f"hasnummorethanone = {hasnummorethanone}\n");

        #we need the highest number for each table...
        #we need to know the old name and the new name of the col for each table...
        utnms = myvalidator.removeDuplicatesFromList(allfintnmsflines);
        uprevtnms = [];#not sure if this should be a list of lists or not...
        allnumsoneachtble = [];#list of lists
        allrnmcolobjsoneachtble = [];#list of lists
        isarnmcoltble = False;
        alltblshasrnmcols = [];
        for utnm in utnms:
            numsftble = [];
            rnmcolobjsftble = [];
            hasprevnm = False;
            for n in range(len(cloglines)):
                line = cloglines[n];
                tnmfline = allfintnmsflines[n];
                numfline = dtrequsrnumslist[n];
                if (tnmfline == utnm):
                    numsftble.append(numfline);
                    if ("rnm table " in line and line.index("rnm table ") == 0 and " to " in line):
                        oldnmsi = 15;
                        oldnmei = line.rindex(" to ");
                        oldtnm = line[oldnmsi:oldnmei];
                        hasprevnm = True;
                        uprevtnms.append(oldtnm);
                    trnmcol = myvalidator.lineHasMSTROnItAtIndex("rnm col from ", line, 0);
                    if (trnmcol and " to " in line and " on " in line):
                        #if the table has renamed cols, then get it
                        toindx = line.index(" to ");
                        onindx = line.index(" on ");
                        oldclnm = line[13:toindx];
                        nwcolnm = line[toindx + 4:onindx];
                        myvalidator.valueMustBeInMinAndMaxRange(toindx, 14, len(line) - 1,
                                                                varnm="toindx");
                        myvalidator.valueMustBeInMinAndMaxRange(toindx, 14, onindx, varnm="toindx");
                        if (isarnmcoltble): pass;
                        else: isarnmcoltble = True;
                        #print(f"line = {line}");
                        #print(f"tnmfline = {tnmfline}");
                        #print(f"oldclnm = {oldclnm}");
                        #print(f"nwcolnm = {nwcolnm}");
                        
                        rnmcolobjsftble.append({"oldcolname": oldclnm, "newcolname": nwcolnm,
                                                "tablenamefromline": tnmfline, "linenum": n});
            if (hasprevnm): pass;
            else: uprevtnms.append("");
            alltblshasrnmcols.append(not myvalidator.isvaremptyornull(rnmcolobjsftble));
            allrnmcolobjsoneachtble.append(rnmcolobjsftble);
            allnumsoneachtble.append(numsftble);
        mxnumoneachtble = [];
        mnnumoneachtble = [];
        for mlist in allnumsoneachtble:
            mxnumoneachtble.append(max(mlist));
            mnnumoneachtble.append(min(mlist));
        isadeltble = not(myvalidator.isvaremptyornull(mydeltablenms));
        
        #need to get all numbers for each table on the unique list
        uaddtblnms = myvalidator.removeDuplicatesFromList(myaddtablenms);
        udeltblnms = myvalidator.removeDuplicatesFromList(mydeltablenms);
        cmnuaddanddeltnms = [nm for nm in uaddtblnms if (nm in udeltblnms)];
        umyaddtblelinenums = [[myaddtlinenums[n] for n in range(len(myaddtablenms))
                               if (myaddtablenms[n] == nm)] for nm in uaddtblnms];
        umydeltblelinenums = [[mydeltlinenums[n] for n in range(len(mydeltablenms))
                               if (mydeltablenms[n] == nm)] for nm in udeltblnms];
        #we need to know if it ends with add or delete
        #we want the order...
        cmnnmsisaddedordellast = [];
        for nm in cmnuaddanddeltnms:
            addi = uaddtblnms.index(nm);
            deli = udeltblnms.index(nm);
            addlnumlist = umyaddtblelinenums[addi];
            dellnumlist = umydeltblelinenums[deli];
            mxaddnum = (-1 if (myvalidator.isvaremptyornull(addlnumlist)) else max(addlnumlist));
            mxdelnum = (-1 if (myvalidator.isvaremptyornull(dellnumlist)) else max(dellnumlist));
            print(f"mxaddnum = {mxaddnum}");
            print(f"mxdelnum = {mxdelnum}");
            
            mydatobj = myvalidator.compareTwoArraysItemByItemInfoObj(addlnumlist, dellnumlist);
            srtedarr = mydatobj["sortedarr"];
            myresarr = mydatobj["resarr"];
            print(f"mydatobj = {mydatobj}");
            print(f"srtedarr = {srtedarr}");
            print(f"myresarr = {myresarr}");

            #0 means on first array add; 1 means on delete only; 2 means on both
            #the line numbers themselves give us the order...

            if (myresarr[len(myresarr) - 1] == 0):
                cmnnmsisaddedordellast.append(True);
                print("added it last!");
            elif (myresarr[len(myresarr) - 1] == 1):
                cmnnmsisaddedordellast.append(False);
                print("deleted it last!");
            #elif (myresarr[len(myresarr) - 1] == 2): print("did both to it last!");
            else:
                raise ValueError("invalid value found for the last item on the resarr! " +
                                 "It must be one of the following: 0, 1, or 2, but it was not!");
        
        #nwdatmustbeempty = True;
        #for num in mxnumoneachtble:
        #    if (1 < num):
        #        nwdatmustbeempty = False;
        #        break;
        nwdatmustbeempty = not(any(1 < num for num in mxnumoneachtble));

        #print all of the data from the above loops up to this point
        print(f"allfintnmsflines = {allfintnmsflines}");
        print(f"allprevtnms = {allprevtnms}");
        print(f"isatleastoneprevnm = {isatleastoneprevnm}");
        print(f"myaddtablenms = {myaddtablenms}");
        print(f"mydeltablenms = {mydeltablenms}");
        print(f"myaddtlinenums = {myaddtlinenums}");
        print(f"mydeltlinenums = {mydeltlinenums}");
        print(f"uaddtblnms = {uaddtblnms}");
        print(f"udeltblnms = {udeltblnms}");
        print(f"umyaddtblelinenums = {umyaddtblelinenums}");
        print(f"umydeltblelinenums = {umydeltblelinenums}");
        print(f"cmnuaddanddeltnms = {cmnuaddanddeltnms}");
        print(f"cmnnmsisaddedordellast = {cmnnmsisaddedordellast}");
        print(f"isadeltble = {isadeltble}");
        print(f"isarnmcoltble = {isarnmcoltble}");
        print(f"utnms = {utnms}");
        print(f"uprevtnms = {uprevtnms}");
        print(f"allnumsoneachtble = {allnumsoneachtble}");
        print(f"allrnmcolobjsoneachtble = {allrnmcolobjsoneachtble}");
        print(f"alltblshasrnmcols = {alltblshasrnmcols}");
        print(f"mnnumoneachtble = {mnnumoneachtble}");
        print(f"mxnumoneachtble = {mxnumoneachtble}");
        print(f"nwdatmustbeempty = {nwdatmustbeempty}");
        print(f"newdatarr = {newdatarr}\n");
        #if (isadeltble): raise ValueError("NEED TO DO SOMETHING HERE...!");

        if (nwdatmustbeempty): myvalidator.varmustbeemptyornull(newdatarr, "newdatarr");
        else: myvalidator.varmustnotbeempty(newdatarr, "newdatarr");


        tnmserrmsgpta = "a table must have at most one previous name and at most one current ";
        tnmserrmsgpta += "name, but one table with a prevname (";
        tnmserrmsgptb = ") has a table name that is both previous and current, which is illegal! ";
        tnmserrmsgptb += "Some effected line numbers in the change log are: ";
        for prevtnm in allprevtnms:
            if (myvalidator.isvaremptyornull(prevtnm)): pass;
            else:
                if (prevtnm in allfintnmsflines):
                    mclglinenums = [i + 1 for i in range(len(allfintnmsflines))
                                    if (allfintnmsflines[i] == prevtnm)];
                    olinenums = [prevtnmi + 1 for i in range(len(allfintnmsflines))
                                 for prevtnmi in range(len(allprevtnms))
                                    if (not(myvalidator.isvaremptyornull(allprevtnms[prevtnmi])) and
                                        allfintnmsflines[i] == allprevtnms[prevtnmi])];
                    finclgproblnums = myvalidator.combineTwoLists(mclglinenums, olinenums, nodups=True);
                    raise ValueError(tnmserrmsgpta + prevtnm + tnmserrmsgptb + str(finclgproblnums));


        #we care if the table exists...
        #we care about the create table statement...
        #we care about the data lines if there is data...
        #we care what the data is...
        mxitems = len(lineswithclsonthem);
        datrejlistftbles = [];
        clogtnmdatreglist = [];
        mtnms = [];
        for n in range(mxitems):
            bglineindx = lineswithclsonthem[n];
            ctblineindx = ctbllines[n];#execute directly
            dtlindx = dtaline[n];#look at first line
            nxtbglineindx = (lineswithclsonthem[n + 1] if (n + 1 < mxitems) else len(mlines));
            diffnxtclsdatline = nxtbglineindx - dtlindx;
            bgline = mlines[bglineindx];
            clstbleexists = ("EXISTS" in bgline);
            tnmindx = bgline.index("with tablename: ");
            tnmnxtspcindx = -1;
            for i in range(tnmindx + 16, len(bgline)):
                if (bgline[i] == ' '):
                    tnmnxtspcindx = i;
                    break;
            myvalidator.valueMustBeInRange(tnmnxtspcindx, tnmindx + 17, len(bgline) - 1,
                                           True, True, "tnmnxtspcindx");
            tname = bgline[tnmindx + 16:tnmnxtspcindx];
            mtnms.append(tname);
            print("\nBEGIN WORKING ON THE TABLE NOW:");
            print(f"tname = {tname}");
            #print(f"len(tname) = {len(tname)}");

            #tname comes from the bkupdat file
            #but the unique table name utnms comes from the change log and
            #if the table was renamed this would be the new name and not the old
            #which will result in a mismatch so we included a check against previous names
            #we also need to know the names of tables that got renamed and what their old name was.
            
            #according to the backup data file and change log is the current table name current or
            #is it a previous name?
            #if the answer is yes, then we know we are working with old and new data
            #if the answer is no, then we know we are working with old data only.
            tnmiscurrentnm = (tname in utnms);
            tnmisprevnm = (isatleastoneprevnm and tname in uprevtnms);
            utnmi = (utnms.index(tname) if (tnmiscurrentnm) else -1);
            prvnmi = (uprevtnms.index(tname) if (tnmisprevnm) else -1);
            usenwnmsordataftble = (tnmiscurrentnm or tnmisprevnm);
            tnmisascrrnt = ((tnmiscurrentnm == tnmisprevnm) and not(tnmiscurrentnm));
            if (tnmiscurrentnm == tnmisprevnm):
                if (tnmiscurrentnm):
                    myvalidator.twoBoolVarsMustBeDifferentOrEqual(tnmiscurrentnm, tnmisprevnm, True,
                                                                "tnmiscurrentnm", "tnmisprevnm");
            mtnmfref = ("" + tname if (tnmiscurrentnm or tnmisascrrnt) else "" + utnms[prvnmi]);
            #is the previous or current tname on the mydeltablenms list
            tnmdeltble = (isadeltble and ((tname in mydeltablenms) or
                                          (tnmisprevnm and (utnms[prvnmi] in mydeltablenms))));
            #is the tname deleted last or not
            tnmisdellast = (isadeltble and ((tnmiscurrentnm and tname in cmnuaddanddeltnms and
                            not(cmnnmsisaddedordellast[cmnuaddanddeltnms.index(tname)])) or
                            (tnmisprevnm and (utnms[prvnmi] in cmnuaddanddeltnms and
                            not(cmnnmsisaddedordellast[cmnuaddanddeltnms.index(utnms[prvnmi])])))));
            #is the tname added last or not
            tnmisaddlast = (isadeltble and ((tnmiscurrentnm and tname in cmnuaddanddeltnms and
                            cmnnmsisaddedordellast[cmnuaddanddeltnms.index(tname)]) or
                            (tnmisprevnm and (utnms[prvnmi] in cmnuaddanddeltnms and
                            cmnnmsisaddedordellast[cmnuaddanddeltnms.index(utnms[prvnmi])]))));
            #is the tname on the rename col list
            tnmhasarnmcol = (isarnmcoltble and ((tnmiscurrentnm and alltblshasrnmcols[utnmi]) or
                                                (tnmisprevnm and alltblshasrnmcols[prvnmi])));
            print(f"tnm in utnms = tname on change log = tnmiscurrentnm = {tnmiscurrentnm}");
            print("NOTE: the table name even if it is not on the change log may still be current!");
            print(f"tnmisascrrnt = {tnmisascrrnt}");#if true, not on change log so assumed true.
            print(f"tnmisprevnm = {tnmisprevnm}");
            print(f"prvnmi = {prvnmi}");
            if (prvnmi in range(len(utnms))):
                print(f"current table name, since tname is previous, is: {utnms[prvnmi]}");
            print("NOTE: when we say it is a previous name, the table name was changed and " +
                  "both are present on the change log, but only the old one will be present " +
                  "on the data file.");
            print(f"current table name is mtnmfref = {mtnmfref}");
            print(f"usenwnmsordataftble = {usenwnmsordataftble}");
            print(f"isadeltble = {isadeltble}");
            print(f"tnmdeltble = {tnmdeltble}");
            print(f"tnmisdellast = {tnmisdellast}");
            print(f"tnmisaddlast = {tnmisaddlast}");
            print(f"isarnmcoltble = {isarnmcoltble}");
            print(f"tnmhasarnmcol = {tnmhasarnmcol}");
            
            if (usenwnmsordataftble and isarnmcoltble):
                #usenwnmsordataftble or isadeltble, or tnmisaddlast
                print("WE NEED TO DO A LOT HERE...!");
                #for line in cloglines:
                #    print(myvalidator.lineHasMSTROnItAtIndex("del table " + tname, line, 0));
                #raise ValueError("NOT DONE YET RESTORING THE DATA 5-29-2025 8:56 PM MST!");
            else: print("WE USE THE OLD DATA ONLY HERE!");

            #add a drop table if exists and then execute it
            #then execute the create table statement
            #then add the data
            #
            #if using the all of the old data only, then we do not need to drop the tables...
            #we also do not need to create the tables either...
            #we just need to restore the data on the one...
            #if some of the data was not on the backup file, then it might be there we can keep it...

            #QUESTIONS ON THE PROCEDURE ASKED ON 6-13-2025 2:49 AM MST
            #
            #what does the user expect to happen if we call this method with
            #a change log and the datfile and the log says to use the old data?
            #
            #-what if the change requires a new create table statement?
            #--deleting a table does not. (only one that does not)
            #--the others do (and the other tables that refer to the deleted tables).
            #--if the change requires a new create table statement,
            #then we need the new one and we need to drop the old one and restore data from the file.
            #
            #when we need a create table statement do we use the one in the backup file or
            #do we generate a new one for the table?
            #what if the table was deleted?
            #
            #if the change requires a new create table statement, then we must build it.
            #if it does not we can use the one from the file.
            #
            #-what if the change does not require a new create table statement?
            #--IE we deleted a table?
            #--drop it if the old one exists and that is it
            #--however it is possible that the older tables refer to it
            #--in this case we probably want new create table statements for all if this is found
            #
            #given that we are using the old data only:
            #-do we drop all of the data and restore it from the datfile OR
            #-should we not change the DB (not remove the table and then restore it back from datfile)
            #and add the old data back if possible?
            #
            #given that we are using old data only and the new names from the change log:
            #-we will need the new create table statement and not the one on the datfile though
            #-we should probably drop all of the data and restore it from the datfile.
            #
            #given that we need new data for the table:
            #-we will need the new create table statement and not the one on the datfile though
            #-we should probably drop all of the data and restore it from the datfile.
            #-but we will also need the new data here from the user
            
            datrejlistftble = [];
            if (usenwnmsordataftble):
                dpqry = myvalidator.genSQLDropTable(tname, onlyifnot=True);
                print(f"DROP TABLE QUERY dpqry = {dpqry}");

                try:
                    mybase.getMyCursor().execute(dpqry);
                    mybase.getMyConn().commit();
                except Exception as ex:
                    print("either the table already does not exist or problem connecting with the DB!");
                    traceback.print_exc();
            
            #if we deleted a table, regardless of if it exists on the data file,
            #we should only drop it here, in this case the user does not want the data.
            #
            #IF DELETED AND THEN ADDED BACK LATER ON, ORDER MATTERS
            if (tnmisdellast):#tnmdeltble 
                print(f"\nWE DO NOT WANT A TABLE NOR THE DATA FOR tname = {tname}!");
                datrejlistftbles.append(datrejlistftble);
                clogtnmdatreglist.append(tname);
                continue;
            
            if (clstbleexists):
                if (len(mlines[ctblineindx + 1]) == 1): pass;#no create table statement
                else:
                    #there is a create table statement
                    if (usenwnmsordataftble):
                        #in order for tname to be the correct name to use it must be in the utnms list
                        #if it is in the unique previous names list we can assume
                        #that it corresponds with a unique table name that got renamed
                        #if this is not the case we are screwed this will crash...
                        
                        mclsref = mycol.getClassFromTableName(mtnmfref);#need the current table name
                        #raise ValueError("NOT DONE YET RESTORING THE DATA 5-29-2025 8:56 PM MST!");
                        #DEPENDS ON THE SQL VARIANT or SQLVARIANT.
                        ctbleqry = mclsref.genSQLCreateTableFromRef(varstr="" + mybase.getMySQLType(),
                                                                   onlyifnot=False, isinctable=True);
                        #ctbleqry = mlines[ctblineindx + 1][0:len(mlines[ctblineindx + 1]) - 1];
                        print(f"CREATE TABLE QUERY: {ctbleqry}");
                        
                        try:
                            mybase.getMyCursor().execute(ctbleqry);
                            mybase.getMyConn().commit();
                        except Exception as ex:
                            print("either the table already exists or problem connecting to the DB!");
                            raise ex;
                        print("created " + mclsref.getTableAndClassNameString() +
                              " on the DB successfully!\n");

                #if table is not a del last table,
                #then what do we do with the data on the database or on the file?
                #we deleted then added the table back after the data from the file what data do we want?
                #do we just want to create the table, but abandon the data? WE ONLY CREATE THE TABLE.
                #possible problem here 7-1-2025 2:36 AM MST
                if (tnmisaddlast):
                    print(f"\nWE ONLY WANT THE TABLE BUT NOT THE DATA FOR tname = {tname}!");
                    datrejlistftbles.append(datrejlistftble);
                    clogtnmdatreglist.append(tname);
                    #PROBLEM HERE AND BELOW IF THERE IS NEW DATA FOR THIS TABLE AND IF WE WANT IT.
                    continue;

                if (diffnxtclsdatline == 1): pass;#no data on the table
                else:
                    #the diff is more than 1
                    #either subtract 1 or 2 lines depending on how it is generated
                    #need to start 1 more than the data only line start indicator.
                    #line 2 is the colnames ,s cannot be in them neither can quotes we can use split
                    cnmsline = mlines[bglineindx + 1];
                    mycnmsstr = cnmsline[2:len(cnmsline) - 3];
                    mcnms = myvalidator.mysplitWithDelimeter(mycnmsstr, "', '");
                    print(f"cnmsline = {cnmsline}");
                    print(f"mycnmsstr = {mycnmsstr}");
                    print(f"mcnms = {mcnms}");#old col names
                    
                    finclnms = None;
                    if (tnmhasarnmcol):
                        #need to identify what col names stay the same and which get changed...
                        #look at the col objects list for the table...
                        #we want the current column names, but keep the old order...
                        
                        if (tnmiscurrentnm):
                            print(f"allrnmcolobjsoneachtble[utnmi] = {allrnmcolobjsoneachtble[utnmi]}");
                            print(f"alltblshasrnmcols[utnmi] = {alltblshasrnmcols[utnmi]}");
                        else:
                            #table name is a previous table name
                            print("allrnmcolobjsoneachtble[prvnmi] = " +
                                  f"{allrnmcolobjsoneachtble[prvnmi]}");
                            print(f"alltblshasrnmcols[prvnmi] = {alltblshasrnmcols[prvnmi]}");
                        
                        myustindx = (utnmi if (tnmiscurrentnm) else prvnmi);
                        myodclnms = [mobj["oldcolname"] for mobj in allrnmcolobjsoneachtble[myustindx]];
                        mynwclnms = [mobj["newcolname"] for mobj in allrnmcolobjsoneachtble[myustindx]];
                        nwclnms = [(mynwclnms[myodclnms.index(nm)] if (nm in myodclnms) else nm)
                                    for nm in mcnms];
                        finclnms = ["" + nm for nm in nwclnms];
                        print(f"nwclnms = {nwclnms}");
                    else: finclnms = ["" + nm for nm in mcnms];
                    print(f"finclnms = {finclnms}");

                    #https://stackoverflow.com/questions/8494514/converting-string-to-tuple
                    from ast import literal_eval;#this is a possible security problem.
                    for k in range(diffnxtclsdatline - 2):
                        #need to convert the string to a tuple
                        #then this will be the vals tuple passed in to the query method
                        myiline = mlines[dtlindx + 1 + k][0:len(mlines[dtlindx + 1 + k]) - 1];
                        mtp = tuple(literal_eval(myiline));
                        print(f"myiline = {myiline}");
                        print(f"mtp = {mtp}");
                        
                        mnwdatqry = myvalidator.genSQLInsertInto(mtnmfref, finclnms, vals=None);
                        print(f"mnwdatqry = {mnwdatqry}");
                        
                        try:
                            mybase.getMyCursor().execute(mnwdatqry, mtp);
                            mybase.getMyConn().commit();
                        except Exception as ex:
                            datrejlistftble.append(mtp);
                            print("either the data could not be added if it violates a newly " +
                                  "added constraint or if it is not in the correct format or " +
                                  "the table does not exist or if the data was already on the table " +
                                  "or there was a problem contacting the DB.");
                            traceback.print_exc();
            datrejlistftbles.append(datrejlistftble);
        print("\nDB successfully restored from the backup data only file!");
        print("the data rejection list for each table is as follows:");
        for n in range(len(datrejlistftbles)):
            mlist = datrejlistftbles[n];
            print("the table name is: " + mtnms[n] + ("*" if (mtnms[n] in clogtnmdatreglist) else ""));
            for item in mlist: print(item);
        #print(datrejlistftble);
        #possible problem here 7-1-2025 2:36 AM MST
        print("NOTE: the * next to the name means that if there was data it was ignored due " +
              "to the change log and not due to errors!");
        print("end of data rejection list!\n");
        return True;

    #depends on the config file and what the DB variable name is called
    @classmethod
    def genpscrptfromsqlines(cls, msqlines):
        #generate the python script file lines here...
        #we need to be able to call our methods to add the data.
        #do we want to do this via objects or directly?
        #the objects currently exist in this program...
        #so this may be a problem when generating the new script.
        #keep in mind the new script may be executed on a completely different machine
        #after this program has closed and the objects probably will not be in memory.
        #?;
        #we want to drop all of the tables
        #we can use the command or current classes
        #dropTable(cls, onlyifnot=False, runbkbfr=False, runbkaftr=False)
        #(above depends on the class being the same and that the table names are the same)
        #or we can write one that does not...
        #or we can store the sql queries in it and just run all of the queries...
        #take the above...
        #copy the array into the file...
        #need to import the CURSOR and CONN from the config or init...
        myvalidator.varmustnotbeempty(msqlines, "msqlines");
        mbfnm = mybase.getMyDBConfigFileName();
        myvalidator.varmustnotbeempty(mbfnm, "mbfnm");
        dbrefnm = mybase.getMyDB().getConfigNamesForValType(MyDB)[0];

        #use the config file to get the attribute name that is the instance of MyDB class.
        #when we have that attribute name, we can proceed.

        #iline = "from init import CURSOR, CONN;";
        ilinea = "from " + mbfnm + " import " + dbrefnm + ";";
        ilineb = "CURSOR = " + dbrefnm + ".getCursor();";
        ilinec = "CONN = " + dbrefnm + ".getConn();";
        qline = "mqries = " + str(msqlines) + ";";
        nxtline = "for qry in mqries:";
        bnxtline = "    CURSOR.execute(qry);";#\t instead of 4 spaces on these lines
        cnxtline = "    CONN.commit();";#\t instead of 4 spaces on these lines
        fline = "print('DB RESTORED SUCCESSFULLY!');"
        
        #have a leveling algorithmn go over the qline...
        #enmbasestr = "ENUM('something, other', 'some ofht', 'this, some, other, else', 'else', ";
        #enmodptstr = "'something else, other', 'last'";
        #finenmstr = enmbasestr + "'mychar\\\'s poses)sive', " + enmodptstr;
        #oenumpstr = enmbasestr + "'mychar\'s poses)sive', " + enmodptstr + ")";
        #myindxstr = "CONSTRAINT individualcoliduniqueconstraint";
        #tmpindx = qline.index(myindxstr);
        #tmpqline = qline[0:tmpindx] + oenumpstr + ", " + qline[tmpindx:];
        #print(myvalidator.getLevelsForValStr(oenumpstr));
        #print(myvalidator.getLevelsForValStr(qline));
        #print(myvalidator.oLevelsAlgorithm(qline));
        #print(myvalidator.oLevelsAlgorithm(tmpqline));

        #if is quote and level is 2 and prev level is 3
        #if next character is a comma insert the newline here...
        mlvlsobj = myvalidator.oLevelsAlgorithm(qline);
        #print(mlvlsobj);

        cmais = [];
        for i in range(len(mlvlsobj['finlvs'])):
            clvl = mlvlsobj['finlvs'][i];
            mc = mlvlsobj['val'][i];
            plvl = (1 if (i == 0) else mlvlsobj['finlvs'][i - 1]);
            if (clvl == 2 and plvl == 3):
                if (i + 1 < len(mlvlsobj['finlvs'])):
                    nxtmc = mlvlsobj['val'][i + 1];
                    if (nxtmc == ','): cmais.append(i + 2);#i+2 where we want to put the newline
        tmparr = myvalidator.mysplitWithLen(qline, cmais, 1, offset=0);
        #nwlinestr = myvalidator.myjoin("\n", tmparr);
        #print(f"nwlinestr = {nwlinestr}");

        #mflines = [iline, qline, nxtline, bnxtline, cnxtline, fline];
        mflines = [ilinea, ilineb, ilinec];
        for n in range(len(tmparr)):
            cline = tmparr[n];
            fincline = ("          " + cline if (0 < n) else "" + cline);
            mflines.append(fincline);
        mflines.append(nxtline);
        mflines.append(bnxtline);
        mflines.append(cnxtline);
        mflines.append(fline);
        return mflines;

    @classmethod
    def getTableClasses(cls, ftchnow=False):
        myvalidator.varmustbeboolean(ftchnow, "ftchnow");
        return [mclsref for mclsref in mycol.getMyClassRefsMain(ftchnw=ftchnow)
                     if (issubclass(mclsref, mybase) and not (mclsref == mybase))];

    @classmethod
    def getExistsCreateTableStatementsAndDataForAllTablesObject(cls, mtblclses):
        mtexistsdata = [];
        mdataforalltbls = [];
        ctblstmnts = [];
        #from models import Signup;#bug here 5-21-2025 4 AM MST
        for mclsref in mtblclses:
            texists = mclsref.tableExists(pqry=False);
            #run the select all query here...
            if (texists):# or (mclsref == Signup) bug here 5-21-2025 4 AM MST
                #if (mclsref == Signup): mdataforalltbls.append([]);
                #else:
                mitemlist = mclsref.getAllItemsOnTable(pqry=False);
                mdataforalltbls.append(mitemlist);
                #DEPENDS ON THE SQL VARIANT or SQLVARIANT.
                ctblqry = mclsref.genSQLCreateTableFromRef(varstr="" + mybase.getMySQLType(),
                                                            onlyifnot=False, isinctable=True);
                                                            #the create table statement
                ctblstmnts.append(ctblqry);
                #print("all items on DB for class " + mclsref.__name__ + " are: ");
                #print(f"all colnames are: {mclsref.getMyColNames()}");
                #for item in mitemlist: print(item);
            else:
                mdataforalltbls.append([]);
                ctblstmnts.append("");
            mtexistsdata.append(texists);
            #else not sure what to do if the table does not exist on the DB
        return {"tsexists": mtexistsdata, "ctbls": ctblstmnts, "dataftbles": mdataforalltbls};
    def getExistsCreateTableStatementAndDataForAllTablesObjectAfterClasses(cls, ftchnow=False):
        mtclses = cls.getTableClasses(ftchnow=ftchnow);
        return cls.getExistsCreateTableStatementsAndDataForAllTablesObject(mtclses);

    @classmethod
    def genSQLFileLines(cls, mtexistsdata, ctblstmnts, mdataforalltbls):
        mtblclses = cls.getTableClasses(ftchnow=False);
        myvalidator.twoListsMustBeTheSameSize(mtexistsdata, mtblclses, "mtexistsdata", "mtblclses");
        myvalidator.twoListsMustBeTheSameSize(ctblstmnts, mtblclses, "ctblstmnts", "mtblclses");
        myvalidator.twoListsMustBeTheSameSize(mdataforalltbls, mtblclses,
                                              "mdataforalltbls", "mtblclses");
        mysqlfilelines = [mclsref.genSQLDropTableFromClass(onlyifnot=True) for mclsref in mtblclses];
        for n in range(len(mtblclses)):
            #create table if exists else do nothing, then generate the statements to insert the data.
            mclsref = mtblclses[n];
            if (mtexistsdata[n]):# or (mclsref == Signup) bug here 5-21-2025 4 AM MST
                mysqlfilelines.append(ctblstmnts[n]);
                #take the data then generate the insert into table statements here...
                for item in mdataforalltbls[n]:
                    nwvqry = mclsref.genSQLInsertIntoFromRef(vals=item);
                    mysqlfilelines.append(nwvqry);
        return mysqlfilelines;
    @classmethod
    def genSQLFileFromTExistsCTAndDataObj(cls, mdataobj):
        myvalidator.objvarmusthavethesekeysonit(mdataobj, ["tsexists", "ctbls", "dataftbles"],
                                                varnm="mdataobj");
        mtexistsdata = mdataobj["tsexists"];
        ctblstmnts = mdataobj["ctbls"];
        mdataforalltbls = mdataobj["dataftbles"];
        return cls.genSQLFileLines(mtexistsdata, ctblstmnts, mdataforalltbls);
    @classmethod
    def genSQLFileLinesFromTExistsCTAndDataForTFromObjFromClses(cls, mclses):
        mdatobj = cls.getExistsCreateTableStatementsAndDataForAllTablesObject(mclses);
        return cls.genSQLFileFromTExistsCTAndDataObj(mdatobj);
    @classmethod
    def genSQLFileLinesFromTExistsCTAndDataForTFromObjAfterClasses(cls, ftchnow=False):
        mtclses = cls.getTableClasses(ftchnow=ftchnow);
        return cls.genSQLFileLinesFromTExistsCTAndDataForTFromObjFromClses(mtclses);

    @classmethod
    def genSQLFileLinesFromScriptFileLines(cls, scrptflines):
        #qline = "mqries = " + str(msqlines) + ";";
        #nxtline = "for qry in mqries:";
        #         01234567890
        #https://stackoverflow.com/questions/8494514/converting-string-to-tuple
        #from ast import literal_eval;#this is a possible security problem.
        
        #si = 1;
        ei = -1;
        for n in reversed(range(len(scrptflines))):
            #print(f"cscrptfline = {scrptflines[n]}");
            if ("for qry in mqries:" in scrptflines[n]):
                ei = n;
                break;
        #print(f"ei = {ei}");
        myvalidator.valueMustBeInRange(ei, 2, len(scrptflines) - 4, True, True, "ei");
        #mstr = scrptflines[1][9:len(scrptflines[1]) - 1];
        #print(f"mstr = {mstr}");
        mlist = [(scrptflines[i][11:len(scrptflines[i]) - 3] if (i + 1 == ei) else
                  scrptflines[i][11:len(scrptflines[i]) - 2])
                 for i in range(len(scrptflines)) if (0 < i and i < ei)];
        #print(mlist);
        return mlist;


    @classmethod
    def myfilewritelinesmethod(cls, fnmandpth, flines, baowiffexists="b", dscptrmsg=""):
        #actually write the stuff here...
        #we need to know what to call the new files and where to save them...
        #note opening in write mode if the file does not exist will create it
        #modes are read, write, append
        #if the file exists, do we block or append or overwrite?
        #if the file does not exist, then we write.
        myvalidator.stringMustHaveAtMinNumChars(fnmandpth, 3, "fnmandpth");
        boremds = ["b", "B", "e", "E", "block", "BLOCK", "error", "ERROR"];
        ovrwmds = ["o", "O", "w", "W", "ow", "OW", "OVER-WRITE", "over-write", "overwrite", "OVERWRITE"];
        apndmds = ["a", "A", "append", "APPEND"];
        worapndmds = myvalidator.combineTwoLists(apndmds, ovrwmds, nodups=True);
        allfmds = myvalidator.combineTwoLists(boremds, worapndmds, nodups=True);
        myvalidator.itemMustBeOneOf(baowiffexists, allfmds, varnm="on_file_exists_action_policy");
        if (myvalidator.isvarnull(dscptrmsg)):
            return cls.myfilewritelinesmethod(fnmandpth, flines,
                baowiffexists=baowiffexists, dscptrmsg="");
        if (myvalidator.isvarnull(flines)):
            return cls.myfilewritelinesmethod(fnmandpth, [],
                baowiffexists=baowiffexists, dscptrmsg=dscptrmsg);
        tmpfile = None;
        tmpfile = Path(fnmandpth);
        exists = tmpfile.is_file();
        #exists = False;
        #try:
        #    tmpfile = open(fnmandpth, "r");
        #    exists = True;
        #    tmpfile.close();
        #except FileNotFoundError as fnfe:
        #    exists = False;
        wfmd = "w";
        if (exists):
            if (myvalidator.isListAInListB([baowiffexists], boremds)):
                raise ValueError("the file (" + fnmandpth + ") already exists!");
            elif (myvalidator.isListAInListB([baowiffexists], apndmds)): wfmd = "a";
            else: wfmd = "w";
        with open(fnmandpth, wfmd) as mfile:
            for line in flines:
                mfile.write(line);
                mfile.write("\n");
            print(dscptrmsg + (" " if (not(dscptrmsg.endswith(" "))) else "") +
                  "file written successfully!");
            mfile.close();
        return True;
    @classmethod
    def blockifmyfileexistswritelines(cls, fnmandpth, flines, dscptrmsg=""):
        return cls.myfilewritelinesmethod(fnmandpth, flines, baowiffexists="b", dscptrmsg=dscptrmsg);
    @classmethod
    def appendifmyfileexistswritelines(cls, fnmandpth, flines, dscptrmsg=""):
        return cls.myfilewritelinesmethod(fnmandpth, flines, baowiffexists="a", dscptrmsg=dscptrmsg);
    @classmethod
    def overwriteifmyfileexistswritelines(cls, fnmandpth, flines, dscptrmsg=""):
        return cls.myfilewritelinesmethod(fnmandpth, flines, baowiffexists="o", dscptrmsg=dscptrmsg);

    @classmethod
    def backupDB(cls):
        #the backup entails everything that is on the DB...
        #may need a new location set...
        #we want to create a list of the SQL commands run
        #we want all of the data on the DB...
        #we also need to know the sequence of the backups like a date and time stamp...
        #
        #maybe what triggered it? User, or adding, removeing or changing a constraint,
        #or adding, deleting, or changing column names or other column properties,
        #or saving, updating data, or deleting data (row or rows),
        #or deleting, adding, or changing tables (like the name, constraints)
        #
        #USER, constraint, table, data
        #
        #what if there are multiple differences? like data, constraints, tables
        #(in this case, it would have been triggered by the USER)
        #adding and dropping contsraints after the table exists
        #causes a problem for saving the data later on (needs backed up immediately).
        #
        #most changes you make are readily apparent execpt one: renaming of existing tables or cols.
        #since the data only file will include the classname and the tablename,
        #this will be apparent there that is unless you changed the class name too.
        #
        #if you did not change the class name, but changed the table name,
        #you can tell in the file that you just changed the table name
        #
        #if you changed both the class name and the table name, among other changes,
        #then it will look like an entirely different table (when comparing these, so be careful).
        #
        #we need to know where to save the different types of files.
        #
        #we need to make the following files:
        #-a python script to execute
        #-an SQL file of commands to execute
        #-a data only file
        #
        #we need to select all from all tables that this program knows of...
        mtblclses = cls.getTableClasses(ftchnow=False);
        mdatobj = cls.getExistsCreateTableStatementsAndDataForAllTablesObject(mtblclses);
        mtexistsdata = mdatobj["tsexists"];
        ctblstmnts = mdatobj["ctbls"];
        mdataforalltbls = mdatobj["dataftbles"];
        
        #print the data and other results here...
        datflines = [];
        for n in range(len(mtblclses)):
            mclsref = mtblclses[n];
            clsexiststr = "class " + mclsref.__name__ + " ";
            clsexiststr += ("EXISTS" if (mtexistsdata[n]) else "DOES NOT EXIST");
            clsexiststr += " with tablename: " + mclsref.getTableName();
            clsexiststr += " and has colnames: ";
            datflines.append(clsexiststr);
            clnmsstr = str(mclsref.getMyColNames());
            datflines.append(clnmsstr);
            ctranstr = "and the create table statement is:";
            datflines.append(ctranstr);
            datflines.append(ctblstmnts[n]);
            dattranstr = "and the data: [";
            if (myvalidator.isvaremptyornull(mdataforalltbls[n])): dattranstr += "]"; 
            datflines.append(dattranstr);
            print("\n" + clsexiststr + "\n" + clnmsstr + "\n" + ctranstr + "\n\n" + ctblstmnts[n]);
            print("\n\n" + dattranstr);
            if (myvalidator.isvaremptyornull(mdataforalltbls[n])): pass;
            else:
                for item in mdataforalltbls[n]:
                    datflines.append(str(item));
                    print(item);
                datflines.append("]");
                print("]");
        #print("\nPRINTING THE DATA ONLY FILE LINES HERE:");
        #for line in datflines: print(line);

        print("\nBEGIN GENERATING THE SQL COMMAND FILE ONLY HERE:");

        mysqlfilelines = cls.genSQLFileLines(mtexistsdata, ctblstmnts, mdataforalltbls);
        for line in mysqlfilelines: print(line);
        
        #generate the python script file here
        mflines = cls.genpscrptfromsqlines(mysqlfilelines);

        print("\nBEGIN GENERATING THE PYTHON FILE ONLY HERE:");
        for line in mflines: print(line);

        #actually write the stuff here...
        #we need to know what to call the new files and where to save them...
        #note opening in write mode if the file does not exist will create it
        #modes are read, write, append
        cls.blockifmyfileexistswritelines("bkdatonly.txt", datflines, dscptrmsg="data only");
        cls.blockifmyfileexistswritelines("bkcmdsonly.sql", mysqlfilelines, dscptrmsg="sql");
        cls.blockifmyfileexistswritelines("bkscrpt.py", mflines, dscptrmsg="script");
        print("SUCCESSFULLY CREATED THE BACKUP FILES AND FINISHED THE BACKUP!");
        #raise ValueError("NEED TO DO THE BACKUP HERE, BUT NOT DONE YET 5-8-2025 12:04 AM MST!");
    
    @classmethod
    def genSQLDropTableFromClass(cls, onlyifnot=False):
        return myvalidator.genSQLDropTable(cls.getTableName(), onlyifnot=onlyifnot);

    @classmethod
    def dropTable(cls, onlyifnot=False, runbkbfr=False, runbkaftr=False):
        myvalidator.varmustbeboolean(runbkbfr, "runbkbfr");
        myvalidator.varmustbeboolean(runbkaftr, "runbkaftr");
        if (runbkbfr): cls.backupDB();

        tnmonclsnmstr = "" + cls.getTableAndClassNameString();
        qry = cls.genSQLDropTableFromClass(onlyifnot=onlyifnot);
        print(f"\nDROP TABLE qry = {qry}\n");
        
        try:
            res = mybase.getMyCursor().execute(qry);
            mybase.getMyConn().commit();
        except Exception as ex:
            #print(f"\nDROP TABLE qry = {qry}\n");
            print("either " + tnmonclsnmstr + " already does not exist, or problem " +
                  "connecting with the DB!");
            traceback.print_exc();

        print("deleted " + tnmonclsnmstr + " on the DB successfully!\n");

        if (runbkaftr): cls.backupDB();
        return True;
    
    @classmethod
    def deleteTable(cls, onlyifnot=False, runbkbfr=False, runbkaftr=False):
        return cls.dropTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def delTable(cls, onlyifnot=False, runbkbfr=False, runbkaftr=False):
        return cls.dropTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeTable(cls, onlyifnot=False, runbkbfr=False, runbkaftr=False):
        return cls.dropTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def remTable(cls, onlyifnot=False, runbkbfr=False, runbkaftr=False):
        return cls.dropTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    

    #WE CANNOT ADD IF EXISTS TO THE TRUNCATE NOR TO THE DELETE COMMANDS.
    @classmethod
    def genSQLTruncateTableFromRef(cls): return myvalidator.genSQLTruncateTable(cls.getTableName());
    @classmethod
    def genSQLDeleteFromRef(cls, colnms=None):
        finclnms = (cls.getMyColNames(cls.getMyPrimaryKeyCols())
                    if (myvalidator.isvaremptyornull(colnms)) else ["" + item for item in colnms]);
        return myvalidator.genSQLDelete(cls.getTableName(), finclnms);
    @classmethod
    def genSQLDeleteNoWhereFromRef(cls): return myvalidator.genSQLDeleteNoWhere(cls.getTableName());
    @classmethod
    def genSQLClearTableFromRef(cls): return cls.genSQLDeleteNoWhereFromRef();

    #SQLite does support the DELETE command and if no where is provided, then it acts as a truncate.
    #THE DELETE command is implemented on most DBs.
    @classmethod
    def truncateTable(cls, onlyifnot=True, runbkbfr=False, runbkaftr=False):
        myvalidator.varmustbeboolean(onlyifnot, "onlyifnot");
        myvalidator.varmustbeboolean(runbkbfr, "runbkbfr");
        myvalidator.varmustbeboolean(runbkaftr, "runbkaftr");
        tnmandclsnmstr = "" + cls.getTableAndClassNameString();
        errmsg = tnmandclsnmstr + " must exist in order for it to be truncated or cleared.";
        if (cls.tableExists()):
            if (runbkbfr): cls.backupDB();

            truncqry = cls.genSQLDeleteNoWhereFromRef() + ";";
            print("\nbegin truncating the data on " + tnmandclsnmstr + " on the DB now!");
            print(f"TRUNCATE TABLE truncqry = {truncqry}");

            res = mybase.getMyCursor().execute(truncqry);
            mybase.getMyConn().commit();

            print("truncated the data on " + tnmandclsnmstr + " on the DB successfully!\n");

            if (runbkaftr): cls.backupDB();
        else: 
            if (onlyifnot): pass;
            else: raise ValueError(errmsg);
        return True;
    @classmethod
    def clearTable(cls, onlyifnot=True, runbkbfr=False, runbkaftr=False):
        return cls.truncateTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);

    @classmethod
    def clearThenDropTable(cls, onlyifnot=True, runbkbfr=False, runbkaftr=False):
        cls.truncateTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=False);
        return cls.dropTable(onlyifnot=onlyifnot, runbkbfr=False, runbkaftr=runbkaftr);
    @classmethod
    def clearAndDropTable(cls, onlyifnot=True, runbkbfr=False, runbkaftr=False):
        return cls.clearThenDropTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);

    def deleteMyRowFromTable(self, onlyifnot=True, runbkbfr=False, runbkaftr=False):
        myvalidator.varmustbeboolean(onlyifnot, "onlyifnot");
        myvalidator.varmustbeboolean(runbkbfr, "runbkbfr");
        myvalidator.varmustbeboolean(runbkaftr, "runbkaftr");
        tnmandclsnmstr = "" + type(self).getTableAndClassNameString();
        errmsg = tnmandclsnmstr + " must exist in order for it to be removed or deleted.";
        if (type(self).tableExists()):
            if (runbkbfr): type(self).backupDB();

            mpkycols = type(self).getMyPrimaryKeyCols();
            mdelcrowqry = type(self).genSQLDeleteFromRef(colnms=None);
            #pkeycola = ?, colb = ? ...
            #need to get the values for the primary key cols only.
            mvals = tuple(self.genValsListForColNames(type(self).getMyColNames(mpkycols)));
        
            print("\nbegin removing the row on " + tnmandclsnmstr + " from the DB now!");
            print(f"DELETE ROW mdelcrowqry = {mdelcrowqry}");
            print(f"mvals = {mvals}");

            res = mybase.getMyCursor().execute(mdelcrowqry, mvals);
            mybase.getMyConn().commit();

            print("removed the data on " + tnmandclsnmstr + " from the DB successfully!\n");

            if (runbkaftr): type(self).backupDB();
        else: 
            if (onlyifnot): pass;
            else: raise ValueError(errmsg);
        return True;
    
    @classmethod
    def deleteARowFromTable(cls, colnms, colvals, onlyifnot=True, runbkbfr=False, runbkaftr=False):
        myobj = cls.getObjectFromGivenKeysAndValues(cls.all, colnms, colvals);
        myvalidator.varmustnotbenull(myobj, "myobj");
        return myobj.deleteMyRowFromTable(onlyifnot=onlyifnot, runbkbfr=runbkbfr, runbkaftr=runbkaftr);


    #despite implying that it would return it returns a list from the fetchall method on the DB.
    #if the list is empty, you still get an empty list, but no item.
    #otherwise the DB method throws an error.
    #however the list will have either 1 or no items on it.
    @classmethod
    def getFirstOrLastItemOnTable(cls, usefirst):
        pkycolnms = cls.getMyColNames(cls.getMyPrimaryKeyCols());
        myselqry = myvalidator.genSelectAllOnlyOnTables([cls.getTableName()], useseldistinct=False);
        ordrbypt = myvalidator.genOrderByOneTableOneVal(pkycolnms, cls.getTableName(),
                                                        False, usefirst);#singleinctname, boolval
        #srdrvals = myvalidator.genSortOrderByAscVal(len(pkycolnms), False);
        #ordrbypt = myvalidator.genOrderBy(pkycolnms, [cls.getTableName()], False, sorder=srdrvals);
        limpt = myvalidator.genSQLimit(1, offset=0);
        myfinselqry = myselqry + " " + ordrbypt + " " + limpt;
        #print(srdrvals);
        #print(f"myselqry = {myselqry}");
        #print(f"ordrbypt = {ordrbypt}");
        #print(f"limpt = {limpt}");
        print(f"SELECT QUERY myfinselqry = {myfinselqry}");

        myores = mybase.getMyCursor().execute(myfinselqry).fetchall();
        mybase.getMyConn().commit();
        print("successfully got the item from the DB (stored in a list as the only item)!");
        return myores;
    @classmethod
    def getFirstItemOnTable(cls): return cls.getFirstOrLastItemOnTable(True);
    @classmethod
    def getLastItemOnTable(cls): return cls.getFirstOrLastItemOnTable(False);

    @classmethod
    def getAllItemsOnTable(cls, pqry=True):
        myvalidator.varmustbeboolean(pqry, "pqry");
        myselqry = myvalidator.genSelectAllOnlyOnTables([cls.getTableName()], useseldistinct=False);
        if (pqry): print(f"SELECT QUERY myselqry = {myselqry}");

        myores = mybase.getMyCursor().execute(myselqry).fetchall();
        mybase.getMyConn().commit();
        if (pqry): print("successfully got the items from the DB!");
        return myores;

    @classmethod
    def printUniqueForeignKeyWarning(cls, pstack=True):
        myfkycols = cls.getMyForeignKeyCols();
        ufkycolnms = [fcol.getColName() for fcol in myfkycols if (fcol.getIsUnique())];
        if (myvalidator.isvaremptyornull(ufkycolnms)): pass;
        else:
            print("WARNING: the following columns for the class " + cls.__name__ +
                  f" have unique foreign keys: {ufkycolnms}");
            print(mycol.getUniqueForeignKeyWarningMessage());
            if (pstack):
                traceback.print_stack();
                print();
            else:
                print("NOTE: THE ABOVE WARNING MAY NOT BE RELATED TO THE ERROR! " +
                      "CHECK THE TRACE BELOW:\n");


    #NOT DONE YET AND NOT WELL TESTED YET 5-8-2025 4:21 AM MST

    #possible bug found: no access to old values or not storing the old values...
    #if we are not storing the old values, then when we try to run update, we do not really
    #have access to what we need especially when we change everything.
    #
    #for example: assume a person has an ID, a first name, and a last name
    #let us assume a major problem occured or that this person committed something illegal
    #so they got a new ID number, a new first name, and a new last name
    #
    #but the DB still has all of the old information in there.
    #if the class does not store the old values somehow, we cannot get access to it to change it.
    #
    #so either we store a previous version of the values...
    #or we insert or update the new values immediately when set is called in the column class.
    #the only problem with the other is what happens if the attribute does not exist?
    #what happens if it does, but was added on setup not when a value was set?
    #it seems storing a previous version of the values is a better solution.
    #
    #currently implemented solution is to store the old values (last synced values)
    #but there is an issue of this not being accurate on start up...
    #due to syncing not set to automatically run yet.

    #this either saves or updates the DB
    #this method determines which of two SQL commands to execute here
    #INSERT INTO tname (colnamea, colnameb, ...) VALUES (?, ...);
    #OR
    #UPDATE tname SET colname = ?, ... WHERE pkycolname = ?, ...
    #oldvalues for the primary key cols are used to look up the row in the DB
    #which are pulled from the last synced values 
    #the values before that are the new values.
    #Of course a values tuple (generated by the program) will be passed in along with the command.
    #in order to decide what to do, the program needs the last synced values for each object to
    #be stored in each object (results in duplicate data, but updates are faster and more convenient)
    #
    #DEPENDS ON THE SQL VARIANT.
    def save(self, runbkbfr=False, runbkaftr=False):
        #if the table does not exist, create it first.
        #if the table exists do nothing.
        #then proceed to save the data.
        #we may need to add new data onto the database, or update data if it is on the DB.
        #depending on what we need to do, the commands could change.
        #may want to backup the OLD data before we do this.
        #may want to run a backup of NEW data after we do this.
        print("\nBEGIN SAVE():\n");
        myvalidator.varmustbeboolean(runbkbfr, "runbkbfr");
        myvalidator.varmustbeboolean(runbkaftr, "runbkaftr");        

        fkydataerrmsg = "the foreign key data is wrong, the columns were found, ";
        fkydataerrmsg += "but no object was found with the given values!";
        for mc in type(self).getMyCols():
            mc.primaryKeyInformationMustBeValid(type(self));
            mc.foreignKeyInformationMustBeValid(fcobj=self, usenoclassobj=False);
            if (mc.isForeignKey()):
               if (mc.doesForeignKeyValuesExistOnObjectsList(self)): pass;
               else: raise ValueError(fkydataerrmsg);

        print(f"\nINSIDE SAVE() for class {type(self).__name__}:");

        #may want to run a backup of the OLD DATA ON THE DB here
        if (runbkbfr): type(self).backupDB();

        texists = type(self).tableExists();
        if (texists): pass;
        else: type(self).createTable();
            

        #need to determine the proper SQL command to execute here...
        #since the object contains the new data already, in order to update it:
        #we need to know a value of the data or have a way to get the row specifically uniquely.
        #maybe by an ID.

        #if the table exists, then we could do either update or add new data to it
        #but if the table did not exist until create was called in this method,
        #then adding new data only.

        #if the lastsyncedvalsdict exists and is not None, then we have already put data on the DB
        #for this object, so updating it not saving it.

        prevvdict = self.getLastSyncedValsDict();
        print(f"lastsyncedvalsdict = {prevvdict}");

        pkycolnms = type(self).getMyColNames(type(self).getMyPrimaryKeyCols());
        print(f"pkycolnms = {pkycolnms}");

        useupdate = ((not (myvalidator.isvaremptyornull(prevvdict))) if (texists) else False);
        
        if (useupdate):
            #get the data uniquely then generate the update DB command
            #UPDATE tablename SET colnamea = newvalue, colnameb = newvalue, ...
            # WHERE colnamea = oldvalue; (or just use the primary key to access it).
            
            print("\nwe are updating the data here now!\n");

            simpvdict = self.genSimpleValsDict(mycols=None);
            print(f"simpvdict = {simpvdict}\n");

            #the col names will be the same...
            diffkys = [mky for mky in list(simpvdict.keys()) if not (simpvdict[mky] == prevvdict[mky])];
            mcnms = [mky[0:mky.rindex("_value")] for mky in diffkys];
            #print(f"diffkys = {diffkys}");
            #print(f"mcnms = {mcnms}");

            #if we are using the primary key arbitrarily, what should we use when one or all of the
            #primary key columns are being updated?
            #A: We should use a UNIQUE key col assuming it is not being updated.
            #What if all unique column data is being updated including the primary key?
            #if we do not have access to what the old value was: we are screwed.
            #if we do just use the old primary key or one unique key col to access the data
            #if we have to provide multiple values we can.

            wrval = myvalidator.genColNameEqualsValString(pkycolnms, nvals=None);#primarykey col = ?;
            #print(f"wrval = {wrval}");
            
            #if the primary key is composed of multiple columns then all of their values will need
            #to be pulled here in order.
            upqry = myvalidator.genSQLUpdate(type(self).getTableName(), mcnms, wrval, nvals=None);
            print(f"\nUPDATE QUERY upqry = {upqry}");

            #if the pkycolnames are not included in the colnames that got modified, then add them here
            tmpvalslist = self.genValsListForColNames(mcnms);
            oldpkyvalslist = [prevvdict[pkclnm + "_value"] for pkclnm in pkycolnms];
            mvals = tuple(myvalidator.combineTwoLists(tmpvalslist, oldpkyvalslist));
            #print(f"tmpvalslist = {tmpvalslist}");
            #print(f"oldpkyvalslist = {oldpkyvalslist}");
            print(f"mvals = {mvals}\n");

            res = None;
            try:
                #just if the update succeeded or not!
                res = mybase.getMyCursor().execute(upqry, mvals).fetchone();
                mybase.getMyConn().commit();
            except Exception as ex:
                print("----------------------------------------------------------------------------");
                print("ERROR: UPDATE FAILED!\n");
                type(self).printUniqueForeignKeyWarning(pstack=False);
                raise ex;
            
            print("\ndata successfully updated on the DB!\n");

            print(f"simpvdict = {simpvdict}");
            self.setLastSyncedValsDict(simpvdict);
        else:
            #we are putting the data on the DB for the first time generate the INSERT INTO command
            #INSERT INTO tablename (colnamea, colnameb, ...) VALUES (values_tuple);
            #however when calling the cursor method we need ?s in for the values and a values tuple
            #to be past in. The number of ?s will match the number of colnames given...
            
            print("\nputting the data on the table for the first time!\n");
            
            #if the user provided the col names in the constructor, we need it
            #if the user set column values after, and not a value like None, but before calling save, 
            #we need it

            dbcolnames = self.getColNamesWithDBValsUsed();

            #print(f"userpcolnames = {self.getUserProvidedColNames()}");#list for sure includes these
            #print(f"dftcolnames = {self.getColNamesWithDefaultsUsed()}");#list may include these or not
            print(f"dbcolnames = {dbcolnames}");#list for sure excludes these

            allcolnames = type(self).getMyColNames();
            mcnms = [item for item in allcolnames if item not in dbcolnames];
            print(f"allcolnames = {allcolnames}");
            print(f"colnames to be saved = mcnms = {mcnms}");
            
            nwvqry = myvalidator.genSQLInsertInto(type(self).getTableName(), mcnms, vals=None);
            print(f"\nSAVE QUERY nwvqry = {nwvqry}");

            mvals = self.genValsTupleForColNames(mcnms);
            print(f"mvals = {mvals}\n");

            res = None;
            try:
                #just if the save succeeded or not!
                res = mybase.getMyCursor().execute(nwvqry, mvals).fetchone();
                mybase.getMyConn().commit();
            except Exception as ex:
                print("----------------------------------------------------------------------------");
                print("ERROR: SAVE FAILED!\n");
                type(self).printUniqueForeignKeyWarning(pstack=False);
                raise ex;

            print("\nthe new data was successfully added onto the DB!\n");

            myores = type(self).getLastItemOnTable();
            print(f"myores = {myores}");

            #returns list of items in the order in which the colums were created in...
            #the list also has the order in which the items were created in
            #unless the query is different

            finitem = myores[len(myores) - 1];
            #cols are in allcols order...
            finitemdict = {};
            for n in range(len(finitem)):
                clnm = allcolnames[n];
                finitemdict[clnm + "_value"] = finitem[n];
            print(f"finitemdict = {finitemdict}");

            #need to get the values for the columns that were not passed in and set those
            for clnm in allcolnames:
                if (clnm in dbcolnames):
                    self.setValueForCol(clnm, finitemdict[clnm + "_value"], mycolobj=None);

            print("\ndata successfully added onto the DB and new object values were set!\n");

            #create a last synced vals dict...
            #add onto previous vals on DB or the last synced vals
            #the values are from the the get it...
            #and if the result provided values they should be set here and included in this.
            mdict = self.genSimpleValsDict(mycols=None);
            print(f"mdict = {mdict}");
            self.setLastSyncedValsDict(mdict);

        #may want to run a backup of the NEW DATA ON THE DB here
        if (runbkaftr): type(self).backupDB();

        print("\nDONE WITH THE SAVE() NOW!\n");
        #raise ValueError("NOT DONE YET 4-30-2025 9:33 PM MST!");


    #begin serialization and representation methods here

    def getKnownAttributeNamesForRepresentation(self, useserial=False):
        return [nm for nm in type(self).getKnownAttributeNamesOnTheClass(useserial)];
    def getKnownAttributeNamesForSerialization(self):
        return self.getKnownAttributeNamesForRepresentation(useserial=True);

    
    def __simplerepr__(self, mystrs, myattrs=None, ignoreerr=True, strstarts=True,
                       exobjslist=None, usesafelistonly=False):
        myvalidator.varmustbeboolean(strstarts, "strstarts");
        myvalidator.varmustbeboolean(ignoreerr, "ignoreerr");
        myvalidator.varmustbeboolean(usesafelistonly, "usesafelistonly");
        if (myvalidator.isvaremptyornull(myattrs)): return myvalidator.myjoin("", mystrs);
        else:
            #they alternate starting with one or other other
            #when one runs out, just put the other
            #when the attributes runs out and the strings are left we can join the remaining strings.
            #we cannot do the same for the attributes.
            #if the attributes are on the unsafelist, copy how it is handled in myrepr
            #if the attribute does not exist, then either
            #-add None to the string and ignore the error OR kill it.
            myvalidator.listMustContainUniqueValuesOnly(myattrs, "myattrs");
            #print(f"my class name = {self.__class__.__name__}");

            fobjnames = type(self).getForeignKeyObjectNamesFromCols();
            refcolnames = type(self).getMyRefColNames();
            unsafelist = myvalidator.combineTwoLists(fobjnames, refcolnames);
            #print(f"unsafelist = {unsafelist}");
            #print(type(self).getMyRefColAttributeNames());
            #safe to serialize and represent, but not really needed
            #what they refer to absolutely is not safe

            mstr = "";
            maxlen = max(len(mystrs), len(myattrs));
            nostrsleft = False;
            for n in range(maxlen):
                #get the first item
                #now attempt to get the other item...
                cstr = None;
                if (n < len(mystrs)): cstr = mystrs[n];
                else: nostrsleft = True;
                cattr = None;
                if (n < len(myattrs)): cattr = myattrs[n];
                else:
                    #strings only but no attributes... we want n<=x not: x<n;
                    return mstr + myvalidator.myjoin("", [mystrs[x] for x in range(len(mystrs))
                                                          if(not (x < n))]);
                #we want to add both if we have them here...
                #the question is what order:
                #print(f"cstr = {cstr}");
                #print(f"cattr = {cattr}");

                if (strstarts and not nostrsleft): mstr += "" + cstr;
                if (hasattr(self, cattr)):
                    #need to get the attribute from the object, but also need to be careful...
                    #if our attribute is on the unsafe list, we need to be really careful
                    #if our attribute is on the safe list, we are safe.
                    #print("the attribute was found!");

                    if (cattr in unsafelist):
                        #print("the attribute is on the unsafe list!");
                        #print(f"cattr = {cattr}");
                        #print(f"usesafelistonly = {usesafelistonly}");
                        #print(f"current class is = {type(self).__name__}");

                        if (usesafelistonly): pass;
                        else:
                            mval = getattr(self, cattr);
                            if (mval == None): mstr += "None";
                            else:
                                #if item is on the exclusion object list, just say self reference
                                #to stop the infinite recursion otherwise.
                                isexcluded = (False if (myvalidator.isvaremptyornull(exobjslist))
                                            else (mval in exobjslist));
                                if (isexcluded):
                                    #we can have it do the safe list only here
                                    dispsafelist = True;
                                    if (dispsafelist):
                                        #not sure which one to use:
                                        mstr += cattr + " (self): ";
                                        try:
                                            mstr += mval.__repr__(exobjslist=exobjslist,
                                                                usesafelistonly=True);
                                        except Exception as ex:
                                            traceback.print_exc();
                                            mstr += mval.__repr__();
                                        #mstr += cattr + " (self): " +
                                        #mval.__simplerepr__(mystrs, myattrs=None, ignoreerr=True,
                                        #                    strstarts=True, exobjslist=None,
                                        #                    usesafelistonly=False);
                                        #mval.__myrepr__(exobjslist=exobjslist, usesafelistonly=True);
                                        #raise ValueError("NOT DONE YET 4-19-2025 11 PM MST!");
                                    else: mstr += "self";
                                else:
                                    #if item is a list of unsafe objects, then what?
                                    #like for example signups in a different class like Activity
                                    #if we just let it run it will be infinite,
                                    #so we can try generating it ourselves, then...
                                    if (type(mval) in [list, tuple]):
                                        mstr += "[";
                                        for k in range(len(mval)):
                                            item = mval[k];
                                            #print(f"class of item = {type(item).__name__}");
                                            try:
                                                mstr += item.__repr__(exobjslist=exobjslist,
                                                                    usesafelistonly=True);
                                            except Exception as ex:
                                                traceback.print_exc();
                                                mstr += item.__repr__();
                                            if (k + 1 < len(mval)): mstr += ", ";
                                        mstr += "]";
                                    else:
                                        #print(f"cattr = {cattr}");
                                        try:
                                            mstr += mval.__repr__(exobjslist=exobjslist,
                                                                  usesafelistonly=True);
                                        except Exception as ex:
                                            traceback.print_exc();
                                            mstr += mval.__repr__();
                                        #raise ValueError("NOT DONE YET 4-19-2025 11 PM MST!");
                    else: mstr += "" + str(getattr(self, cattr));
                    #mstr += "" + cattr;
                else:
                    if (ignoreerr): mstr += "None";
                    else: raise AttributeError(f"'{type(self).__name__}' has no attribute '{cattr}'");
                if (not strstarts and not nostrsleft): mstr += "" + cstr;
            return mstr;
                    

    def __myrepr__(self, exobjslist=None, usesafelistonly=False):
        myvalidator.varmustbeboolean(usesafelistonly, "usesafelistonly");
        mstr = "<" + self.__class__.__name__ + " ";
        unsafelist = type(self).getForeignKeyObjectNamesFromCols();
        nmscls = self.getKnownAttributeNamesForRepresentation(useserial=False);
        pinforefcols = False;#if this is false, col info is not printed to the user, if true, it is
        tmpnmscls = [nm for nm in nmscls if (pinforefcols or
                                             (nm not in type(self).getMyRefColAttributeNames()))];
        allsafelist = [nm for nm in tmpnmscls if nm not in unsafelist];
        finlist = (allsafelist if (usesafelistonly) else tmpnmscls);
        #print(finlist);
        #print(f"my class name = {self.__class__.__name__}");
        #print(f"usesafelistonly = {usesafelistonly}");
        
        handleallsame = False;
        previscol = False;
        for n in range(len(finlist)):
            attr = finlist[n];
            addnl = False;
            #print(f"attr = {attr}");

            if (hasattr(self, attr)):
                if (attr == "all" and not handleallsame):
                    mstr += "all: [list of all instances of the class]";
                else:
                    mval = getattr(self, attr);
                    #if item is on the exclusion object list, just say self reference to stop
                    #the infinite recursion otherwise.
                    isexcluded = (myvalidator.isvaremptyornull(exobjslist) or (mval in exobjslist));
                    if (isexcluded):
                        #we can have it do the safe list only here
                        dispsafelist = False;
                        if (dispsafelist):
                            mstr += attr + " (self): " + mval.__myrepr__(exobjslist, True);
                        else: mstr += attr + ": self";
                    else:
                        ciscol = (False if (attr == "all") else (type(mval) == mycol));
                        ciscol = (ciscol or ((attr in unsafelist) and not (mval == None)));
                        if ((not (attr == "all")) and ciscol and not previscol): mstr += "\n";
                        #print("calling to string of the item!");
                        #if attribute name is on the unsafelist,
                        #then need to call myrepr but with the exlist;
                        if (attr in unsafelist):
                            if (mval == None): mstr += attr + ": None";
                            else:
                                nwexlist = [self];
                                for item in exobjslist: nwexlist.append(item);
                                mstr += attr + ": " + mval.__myrepr__(nwexlist, False);
                                #print(f"back in calling class {self.__class__.__name__}!");
                        else: mstr += attr + ": " + str(mval);
                        previscol = ciscol;
                        if (previscol): addnl = True;
                if (n + 1 < len(finlist)):
                    if (addnl):
                        mstr += ",\n";
                        addnl = False;
                    else: mstr += ", ";
        mstr += " /" + self.__class__.__name__ + ">";
        #print(dir(type(self)));
        #mlist = [{"key": attr, "value": getattr(self, attr)} for attr in dir(type(self))
        #         if not callable(getattr(self, attr) and attr not in
        #                         ["all", "__dict__", "__doc__", "__module__", "__weakref__"])];
        #print(mlist);
        #print(mstr);
        #raise ValueError("NOT DONE YET!");
        return mstr;
    def __repr__(self): return self.__myrepr__([self]);

    
    def __to_dict__(self, myattrs=None, exobjslist=None, usesafelistonly=False, prefix=""):
        myvalidator.varmustbeboolean(usesafelistonly, "usesafelistonly");

        if (prefix == None):
            return self.__to_dict__(myattrs=myattrs, exobjslist=exobjslist,
                                    usesafelistonly=usesafelistonly, prefix="");
        
        #this method serialized and makes a dict of the given object for its given
        #attributes or properties.
        #
        #not sure what to exclude.
        #we know that some attributes are always safe and some are unsafe
        #the unsafe stuff may be excluded or included but how?
        #we need some kind of list to determine what gets excluded...
        #we also may only want to serialize certain items and ignore the rest...
        #but we do not really want that to depend on the context.
        #
        #if we are in the Signups class for example:
        #when we go to something unsafe like activity or camper, we need to exclude at minimum:
        #-our current signup object (self)
        #-we also need to exclude camper.signups and activity.signups or *.signups
        #-but really it is a reference to the starting class or the classes used.
        #for example:
        #signups has a camper object and an activity object
        #the camper and activity objects both have a list of signup objects that must be excluded
        #Class order: Signup, Camper, List<Signup>, Signup (if not excluded) or Activity, List<Signup> 
        #if we assume that the lists are all of the same type then we can get the type of the first
        #item or all items assuming non-null and if it refers to an already used class
        #exclude altogether or serialize safe items only or just exclude that...
        #
        #sometimes in the camper, we want the signups and other times we do not.
        #so we need to be able to specify that we do not want something...
        #we also need some way of saying we only want these...
        #the only is myattrs provided list.
        #
        #do we want to include stuff like the tablename and the constraints that are common for the
        #whole class or not? For serialization it seems pointless to include this stuff.
        #That kind of stuff is not included now.

        #make sure the self object is always excluded.
        noexobjs = myvalidator.isvaremptyornull(exobjslist);#no original exobjs
        #if (noexobjs):
        #    return self.__to_dict__(myattrs=myattrs, exobjslist=[self],
        #       usesafelistonly=usesafelistonly, prefix=prefix);

        fobjnames = type(self).getForeignKeyObjectNamesFromCols();
        refcolnames = type(self).getMyRefColNames();
        unsafelist = myvalidator.combineTwoLists(fobjnames, refcolnames);
        if (unsafelist == None): unsafelist = ["all"];
        elif ("all" not in unsafelist): unsafelist.append("all");
        nmscls = self.getKnownAttributeNamesForSerialization();
        
        hasonlyrules = True;
        myonlyrules = None;
        try:
            myonlyrules = type(self).getSerializeOnlyRules();
        except Exception as ex:
            hasonlyrules = False;
        hasexrules = True;
        myexrules = None;
        try:
            myexrules = type(self).getExclusiveSerializeRules();
        except Exception as ex:
            hasexrules = False;
        
        if (hasexrules):
            if (myvalidator.isvaremptyornull(myexrules)): pass;
            else:
                #noorigexrules = noexobjs = myvalidator.isvaremptyornull(exobjslist);
                nwlist = [mxrule for mxrule in myexrules if (noexobjs or mxrule not in exobjslist)];
                if (myvalidator.isvaremptyornull(nwlist)): pass;
                else:
                    finxlist = myvalidator.combineTwoLists(exobjslist, nwlist);
                    return self.__to_dict__(myattrs=myattrs, exobjslist=finxlist,
                                        usesafelistonly=usesafelistonly, prefix=prefix);
        nogivenrules = myvalidator.isvaremptyornull(myattrs);
        if (hasonlyrules and nogivenrules):
            if (myvalidator.isvaremptyornull(myonlyrules)): pass;
            else:
                #noorigexrules = myvalidator.isvaremptyornull(myattrs);
                #nwlist = [mxrule for mxrule in myonlyrules if (noorigexrules
                #                                             or mxrule not in myattrs)];
                nwlist = [mxrule for mxrule in myonlyrules];
                if (myvalidator.isvaremptyornull(nwlist)): pass;
                else:
                    finxlist = myvalidator.combineTwoLists(myattrs, nwlist);
                    return self.__to_dict__(myattrs=finxlist, exobjslist=exobjslist,
                                        usesafelistonly=usesafelistonly, prefix=prefix);


        print("\nINSIDE TO_DICT():");
        print(f"current class is {type(self).__name__}");
        print(f"myattrs = {myattrs}");
        print(f"unsafelist = {unsafelist}");
        print(f"all list = nmscls = {nmscls}");
        print(f"exlistforserialization = {type(self).getTheExclusionListForSerialization()}");
        print(f"exobjslist = {exobjslist}");
        print(f"hasonlyrules = {hasonlyrules}");
        print(f"myonlyrules = {myonlyrules}");
        print(f"hasexrules = {hasexrules}");
        print(f"myexrules = {myexrules}");
        print(f"prefix = {prefix}");

        usealist = (myvalidator.isvaremptyornull(myattrs));#use_all_list or included attribute list
        safelist = [item for item in nmscls if (item not in unsafelist)];
        myfinlist = ((safelist if (usesafelistonly) else nmscls) if (usealist) else myattrs);
        print(f"usealist = {usealist}");
        print(f"usesafelistonly = {usesafelistonly}");
        print(f"safelist = {safelist}");
        print(f"myfinlist = {myfinlist}");

        hasnvals = False;
        mynlist = [];
        for attr in myfinlist:
            if (attr in safelist): pass;
            else:
                if ("." in attr):
                    mysubattrstrs = myvalidator.mysplitWithDelimeter(attr, ".", 0);
                    hasnvals = True;
                    print(f"attr = {attr}");
                    print(f"mysubattrstrs = {mysubattrstrs}");

                    if (mysubattrstrs[0] not in mynlist): mynlist.append(mysubattrstrs[0]);
                    #print(f"mynlist = {mynlist}");
                    
        if (hasnvals):
            print(f"mynlist = {mynlist}");
            
            myfinruleslist = [item for item in myfinlist];
            ndsnwlist = False;
            for item in mynlist:
                if (item not in myfinruleslist):
                    if (ndsnwlist): pass;
                    else: ndsnwlist = True;
                    myfinruleslist.append(item);
            if (ndsnwlist):
                print("calling to_dict again!");
                return self.__to_dict__(myattrs=myfinruleslist, exobjslist=exobjslist,
                                        usesafelistonly=usesafelistonly, prefix=prefix);
            else:
                print("\noriginal rules myfinlist will be used!\n");
                print(f"myfinlist = {myfinlist}");

        
        #serialization does not care about the order
        #so handle everything that is safe before we even both to deal with the hard stuff
        mdict = {};
        for attr in myfinlist:
            if (attr in safelist): mdict[attr] = getattr(self, attr);
            else:
                if ("." in attr): pass;
                else:
                    mval = getattr(self, attr);
                    if (mval == None): mdict[attr] = mval;
                    elif ((type(mval) in [list, tuple]) and myvalidator.isvaremptyornull(mval)):
                        mdict[attr] = mval;
                    #else handle unsafe list in other loop below
        print(f"\nsafedict = {mdict}\n");

        
        #need to check the prefix for circles
        #activity.signups.activity.signups
        #if a part of the prefix is contained inside it other than itself we have a circle...
        if (myvalidator.isvaremptyornull(prefix)): pass;
        else:
            #split the string at the .
            #combine a few with the .s until a circle is produced or not possible.
            mysubstrs = myvalidator.mysplitWithDelimeter(prefix, ".", 0);
            print(f"mysubstrs = {mysubstrs}");

            frqsingles = [];
            for mystr in mysubstrs:
                cnt = prefix.count(mystr);
                if (1 < cnt): raise RecursionError("prefix string contains a circle!");
                else: frqsingles.append(cnt);
            print(f"frqsingles = {frqsingles}");
        

        #signups has unsafe stuff like:
        #activity object (signups list and some other stuff)
        #camper object (signups list and some other stuff)
        #all signups list (camper and activity and all models include all list on theirs too)
        #
        #when we have to serialize stuff like camper, what do we do?
        #first we serialize the safe stuff, but we also need to exclude signups class as a whole.
        #or do we exclude the class as a whole or just everything on the signups...

        if (usesafelistonly): pass;
        else:
            for attr in myfinlist:
                if (attr in safelist): pass;
                else:
                    if ("." in attr): pass;#not handled here or above, but handled below.
                    else:
                        mval = getattr(self, attr);
                        if (mval == None): pass;
                        elif ((type(mval) in [list, tuple]) and myvalidator.isvaremptyornull(mval)):
                            pass;
                        else:
                            #if on the exclusion list, exclude it; if not, add it to the dict.
                            #isonexlist = (False if (noexobjs) else (mval in exobjslist));
                            fulnm = (attr if (myvalidator.isvaremptyornull(prefix)) else
                                    prefix + "." + attr);
                            print("attr is in the unsafe list!");
                            print(f"attr = {attr}");
                            print(f"fulnm = {fulnm}");
                            
                            isonexlist = (False if (noexobjs) else (fulnm in exobjslist));
                            if (isonexlist or noexobjs): pass;
                            else:
                                for exrule in exobjslist:
                                    print(f"exrule = {exrule}");
                                    ptinrule = ("." in exrule);
                                    attrinexrule = (exrule[exrule.rindex(".") + 1:] if (ptinrule) else
                                                    "" + exrule);
                                    print(f"attrinexrule = {attrinexrule}");

                                    if (attr == attrinexrule):
                                        print("the attributes match!");

                                        if (exrule == "*." + attr):
                                            print("the rule excludes the attribute!");
                                            isonexlist = True;
                                            break;
                            #isonexlist = False;
                            
                            print(f"isonexlist = {isonexlist}");
                            print(f"calling class is {type(self).__name__}");
                            
                            if (isonexlist): pass;
                            else:
                                print("item is not excluded!");
                                
                                #for the unsafe item that is not excluded,
                                #do we have other special serialization rules that will apply to it?
                                #if so, we cannot just use the myattrs list...
                                #it will be on the myattrs list or on the myfinlist with .s in it
                                otherruleslist = [item for item in myfinlist if "." in item];
                                print(f"myattrs = {myattrs}");
                                print(f"myfinlist = {myfinlist}");
                                print(f"otherruleslist = {otherruleslist}");
                                
                                #if any of the otherrules start with our attr, then these rules apply
                                #to our object...
                                #if not, then safe to proceed
                                nwattrslist = [myotrrule[len(attr) + 1:]
                                               for myotrrule in otherruleslist
                                               if myotrrule.startswith(attr + ".")];
                                print(f"nwattrslist = {nwattrslist}");
                                
                                no_orules = myvalidator.isvaremptyornull(otherruleslist);
                                innwattrlist = (myattrs if (no_orules) else nwattrslist);
                                print(f"innwattrlist = {innwattrlist}");
                                #raise ValueError("NOT DONE YET!");

                                if (type(mval) in [list, tuple]):
                                    print("item is a list of unsafe objects!");

                                    #mybase.mcntr += 1;
                                    mdict[attr] = [item.__to_dict__(myattrs=innwattrlist,
                                                                    exobjslist=exobjslist,
                                                                    #exobjslist=[exitem for exitem in
                                                                    #            exobjslist].append(
                                                                    # item),
                                                                usesafelistonly=False, prefix=fulnm)
                                                                for item in mval];
                                    #pass;
                                else:
                                    print("this is just an unsafe item!");
                                    
                                    #add the self object to the new exclusive object list
                                    #nwlist = ([] if (myvalidator.isvaremptyornull(exobjslist)) else
                                    #          [item for item in exobjslist]);
                                    #nwlist.append(mval);
                                    #print(f"nwlist = {nwlist}");
                                    print(f"innwattrlist = {innwattrlist}");
                                    
                                    #mybase.mcntr += 1;
                                    mdict[attr] = mval.__to_dict__(myattrs=innwattrlist,
                                                                   exobjslist=exobjslist,
                                                                usesafelistonly=False, prefix=fulnm);
                                #raise ValueError("NOT DONE YET WITH THE UNSAFE LIST STUFF YET " +
                                #                "4-24-2025 2 AM MST!");
        print(f"\nFINAL mdict = {mdict}\n");
        return mdict;
        

    #class methods of the base class, but not constructors.

    @classmethod
    def getMyColsOrRefColsOrMyColAttributeNames(cls, retobjs, usemycols):
        #print(f"cls = {cls}");
        myvalidator.varmustbeboolean(usemycols, "usemycols");
        myvalidator.varmustbeboolean(retobjs, "retobjs");
        return [(getattr(cls, attr) if retobjs else attr)
                for attr in dir(cls) if (type(getattr(cls, attr)) ==
                                         (mycol if (usemycols) else myrefcol))];
    @classmethod
    def getMyColObjects(cls, usemycols):
        return cls.getMyColsOrRefColsOrMyColAttributeNames(True, usemycols);
    @classmethod
    def getMyAttributeNamesForColsOrRefCols(cls, usemycols):
        return cls.getMyColsOrRefColsOrMyColAttributeNames(False, usemycols);
    @classmethod
    def getMyCols(cls): return cls.getMyColObjects(True);
    @classmethod
    def getMyRefCols(cls): return cls.getMyColObjects(False);
    @classmethod
    def getMyColAttributeNames(cls): return cls.getMyAttributeNamesForColsOrRefCols(True);
    @classmethod
    def getMyRefColAttributeNames(cls): return cls.getMyAttributeNamesForColsOrRefCols(False);

    @classmethod
    def getMyOrRefColsFromClassOrParam(cls, usemycols, mycols=None):
        myvalidator.varmustbeboolean(usemycols, "usemycols");
        return (cls.getMyColObjects(usemycols) if myvalidator.isvaremptyornull(mycols) else mycols);
    @classmethod
    def getMyColsFromClassOrParam(cls, mycols=None):
        return cls.getMyOrRefColsFromClassOrParam(True, mycols);
    @classmethod
    def getMyRefColsFromClassOrParam(cls, mycols=None):
        return cls.getMyOrRefColsFromClassOrParam(False, mycols);

    @classmethod
    def getMyOrRefColNames(cls, usemycols, mycols=None):
        return [(mclobj.colname if (usemycols) else mclobj.listcolname) for mclobj in
                 cls.getMyOrRefColsFromClassOrParam(usemycols, mycols)];
    #the colnames for mycol object match the attribute names for it so you may use this method or
    #getMyColAttributeNames(cls) since they both return the same result
    @classmethod
    def getMyColNames(cls, mycols=None): return cls.getMyOrRefColNames(True, mycols);
    #returns the value colnames for the refcols
    #if this is not what you want use: getMyRefColAttributeNames(cls)
    @classmethod
    def getMyRefColNames(cls, mycols=None): return cls.getMyOrRefColNames(False, mycols);
    
    @classmethod
    def getValueColNames(cls, mycols=None): return [nm + "_value" for nm in cls.getMyColNames(mycols)];

    @classmethod
    def getMyColObjFromName(cls, mcnm, mycols=None):
        mclist = cls.getMyColsFromClassOrParam(mycols);
        if (myvalidator.isvaremptyornull(mclist)): pass;
        else:
            for mclobj in mclist:
                if (mclobj.colname == mcnm): return mclobj;
        errmsg = "col object with name (" + mcnm + ") and class name (" + cls.__name__ + ") not found!";
        raise ValueError(errmsg);
    @classmethod
    def getColObjFromName(cls, mcnm, mycols=None): return cls.getMyColObjFromName(mcnm, mycols=mycols);
    @classmethod
    def getColObjectFromName(cls, mcnm, mycols=None):
        return cls.getMyColObjFromName(mcnm, mycols=mycols);
    @classmethod
    def getMyColumnObjectFromName(cls, mcnm, mycols=None):
        return cls.getMyColObjFromName(mcnm, mycols=mycols);
    @classmethod
    def getMyColumnObjFromName(cls, mcnm, mycols=None):
        return cls.getMyColObjFromName(mcnm, mycols=mycols);

    @classmethod
    def areGivenColNamesOnTable(cls, mlist, mycols=None):
        if (myvalidator.isvaremptyornull(mlist)): return False;
        fincolnms = cls.getMyColNames(cls.getMyColsFromClassOrParam(mycols));
        for mitem in mlist:
            if (mitem in fincolnms): pass;
            else: return False;
        return True;

    @classmethod
    def getMyPrimaryOrForeignKeyCols(cls, usepkys, mycols=None):
        myvalidator.varmustbeboolean(usepkys, "usepkys");
        return [mclobj for mclobj in cls.getMyColsFromClassOrParam(mycols)
                if (mclobj.isprimarykey if (usepkys) else mclobj.isforeignkey)];
    @classmethod
    def getMyPrimaryKeyCols(cls, mycols=None): return cls.getMyPrimaryOrForeignKeyCols(True, mycols);
    @classmethod
    def getMyForeignKeyCols(cls, mycols=None): return cls.getMyPrimaryOrForeignKeyCols(False, mycols);
    
    @classmethod
    def getForeignKeyObjectNamesFromCols(cls, mycols=None):
        return [mc.getForeignObjectName() for mc in cls.getMyForeignKeyCols(mycols)
                if (cls.needToCreateAnObjectForCol(mc))];

    @classmethod
    def getIndividualColumnConstraintsOrColsWithConstraints(cls, useclist, mycols=None):
        myvalidator.varmustbeboolean(useclist, "useclist");
        return [(mc.getConstraints() if (useclist) else mc)
                for mc in cls.getMyColsFromClassOrParam(mycols)
                if not myvalidator.isvaremptyornull(mc.getConstraints())];
    @classmethod
    def getIndividualColumnConstraints(cls, mycols=None):
        return cls.getIndividualColumnConstraintsOrColsWithConstraints(True, mycols);
    @classmethod
    def getColumnsWithConstraints(cls, mycols=None):
        return cls.getIndividualColumnConstraintsOrColsWithConstraints(False, mycols);

    @classmethod
    def isColWithConstraintsValid(cls, mc):
        myvalidator.varmustnotbenull(mc, "mc");
        if (myvalidator.isvaremptyornull(mc.constraints)): pass;
        else:
            for thecnst in mc.constraints:
                if (myvalidator.isvaremptyornull(thecnst)): return False;
                else:
                    if (" CHECK(" in thecnst):
                        ci = thecnst.index(" CHECK(");
                        aindxsofnm = [n for n in range(len(thecnst))
                                    if thecnst[n:].startswith(mc.getColName())];
                        isvld = False;
                        if (0 < len(aindxsofnm)):
                            for i in aindxsofnm:
                                if (ci < i):
                                    isvld = True;
                                    break;
                        if (isvld): pass;
                        else: return False;
                    else: return False;
        return True;

    @classmethod
    def getColumnsWithIndividualInvalidConstraints(cls, mycols=None):
        return [mc for mc in cls.getColumnsWithConstraints(mycols)
                if (not cls.isColWithConstraintsValid(mc))];

    @classmethod
    def areColsWithIndividualConstraintsValid(cls, mycols=None):
        for mc in cls.getColumnsWithConstraints(mycols):
            if (cls.isColWithConstraintsValid(mc)): pass;
            else: return False;
        return True;
    
    @classmethod
    def getPossibleTableNames(cls):
        return ["mytablename", "tablename", "table_name", "my_table_name"];

    @classmethod
    def getMultiColumnConstraintVariableNames(cls):
        return ["mymulticolumnconstraints", "mymulticolconstraints", "mcolconstraints",
                "mymulticolumnarguments", "mymulticolarguments", "mcolarguments", "mymulticolumnargs",
                "mymulticolargs", "multicolargs", "mcolargs", "my_multi_column_constraints",
                "my_multicol_constraints", "mcol_constraints", "my_multi_column_arguments",
                "my_multicol_arguments", "my_multi_col_arguments", "multi_col_arguments",
                "mcol_arguments", "my_multi_column_args", "my_multicol_args",
                "mcol_args", "my_multi_col_args", "multi_col_args", "my_multi_col_constraints"];

    @classmethod
    def getAllConstraintVariableNames(cls):
        return ["allconstraints", "allcolumnconstraints", "allcolconstraints", "alltableconstraints",
                "alltablecolconstraints", "all_constraints", "all_column_constraints",
                "all_col_constraints", "all_table_constraints", "all_table_col_constraints",
                "allarguments", "allcolumnarguments", "allcolarguments", "alltablearguments",
                "alltablecolarguments", "all_arguments", "all_column_arguments", "all_col_arguments",
                "all_table_arguments", "all_table_col_arguments", "all_tablecol_arguments",
                "allargs", "allcolumnargs", "allcolargs", "alltableargs", "alltablecolargs",
                "all_args", "all_column_args", "all_col_args", "all_table_args", "all_table_col_args",
                "all_tablecol_args", "tableargs", "tablecolargs", "table_args", "table_col_args",
                "tablecol_args"];

    @classmethod
    def getAllExclusiveSerializeRuleNames(cls):
        return ["ex_rules", "exclusive_rules", "exrules", "exclusiverules", "exclusionrules",
                "serialize_exclusive_rules", "serialize_ex_rules", "serialize_exclusion_only_rules",
                "serializeexclusion_only_rules", "serializeexclusiononly_rules",
                "serializeexclusiononlyrules", "exclusion_rules", "serialize_exclusive_only_rules",
                "serializeexclusive_only_rules", "serializeexclusiveonly_rules",
                "serializeexclusiveonlyrules"];
    @classmethod
    def getAllGeneralSerializeRuleNames(cls):
        return ["serialize_rules", "serializerules", "serialize_only", "only_rules", "onlyrules",
                "serialize_only_rules", "serializeonly", "serializeonlyrules"];

    @classmethod
    def getListOfPossibleNamesForVariable(cls, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)): return cls.varMustBePresentOnTable("varnm");
        errmsg = "variable name " + varnm + " not recognized or is not associated with a list!";
        if (varnm == "tablename"): return cls.getPossibleTableNames();
        elif (varnm == "multi_column_constraints_list"):
            return cls.getMultiColumnConstraintVariableNames();
        elif (varnm == "allconstraints_list"): return cls.getAllConstraintVariableNames();
        elif (varnm == "allexrules"): return cls.getAllExclusiveSerializeRuleNames();
        elif (varnm == "allonlyrules"): return cls.getAllGeneralSerializeRuleNames();
        elif (varnm == "allserializerules"):
            mlist = [item for item in cls.getAllGeneralSerializeRuleNames()];
            for item in cls.cls.getAllExclusiveSerializeRuleNames(): mlist.append(item);
            return mlist;
        else: raise ValueError(errmsg);

    @classmethod
    def getValObjectIfPresent(cls, ilist=None, varnm="varnm"):
        if (myvalidator.isvaremptyornull(ilist)):
            mylist = cls.getListOfPossibleNamesForVariable(varnm);
        else: mylist = ilist;
        for attr in dir(cls):
            for pnm in mylist:
                if (pnm in attr): return {"value": getattr(cls, attr), "name": attr};
        return None;
    @classmethod
    def getValObjectIfPresentMain(cls, varnm="varnm"): return cls.getValObjectIfPresent(None, varnm);

    @classmethod
    def isVarPresentOnTable(cls, ilist=None, varnm="varnm"):
        return (not myvalidator.isvaremptyornull(cls.getValObjectIfPresent(ilist, varnm)));
    @classmethod
    def isVarPresentOnTableMain(cls, varnm="varnm"): return cls.isVarPresentOnTable(None, varnm);

    @classmethod
    def varMustBePresentOnTable(cls, ilist=None, varnm="varnm"):
        if (cls.isVarPresentOnTable(ilist, varnm)): return True;
        else: raise AttributeError("the table must have a(n) " + varnm + " in it!");
    @classmethod
    def varMustBePresentOnTableMain(cls, varnm="varnm"):
        return cls.varMustBePresentOnTable(None, varnm);

    
    #possible bug found 5-4-2025 12:29 AM maybe we can return null if the name is not found?
    #if the name is not present, what should we do? should we return null for the name or error out?

    @classmethod
    def getNameOrValueOfVarIfPresentOnTable(cls, usename, ilist=None, varnm="varnm"):
        myvalidator.varmustbeboolean(usename, "usename");
        myresobj = cls.getValObjectIfPresent(ilist, varnm);
        if (myvalidator.isvaremptyornull(myresobj)):
            #if (usename): return None;
            #else:
                raise AttributeError("the table must have a(n) " + varnm + " in it!");
        else: return myresobj[("name" if usename else "value")];
    @classmethod
    def getNameOrValueOfVarIfPresentOnTableMain(cls, usename, varnm="varnm"):
        return cls.getNameOrValueOfVarIfPresentOnTable(usename, None, varnm);
    
    @classmethod
    def getNameOfVarIfPresentOnTable(cls, ilist=None, varnm="varnm"):
        return cls.getNameOrValueOfVarIfPresentOnTable(cls, True, ilist, varnm);
    @classmethod
    def getNameOfVarIfPresentOnTableMain(cls, varnm="varnm"):
        return cls.getNameOrValueOfVarIfPresentOnTableMain(True, varnm);
    
    @classmethod
    def getValueOfVarIfPresentOnTable(cls, ilist=None, varnm="varnm"):
        return cls.getNameOrValueOfVarIfPresentOnTable(cls, False, ilist, varnm);
    @classmethod
    def getValueOfVarIfPresentOnTableMain(cls, varnm="varnm"):
        return cls.getNameOrValueOfVarIfPresentOnTableMain(False, varnm);
    
    @classmethod
    def getTableName(cls): return cls.getValueOfVarIfPresentOnTableMain("tablename");
    @classmethod
    def getMultiColumnConstraints(cls):
        return cls.getValueOfVarIfPresentOnTableMain("multi_column_constraints_list");
    

    #most serialization methods are here

    #the two immediately below are convenience methods based on the above functions

    #this gets the rules that the user has defined in their class which extends mybase class
    #in the event that the user did not define it, it throws an attribute error
    #this does not get all attributes that will be serialized
    @classmethod
    def getSerializeOnlyORExclusiveSerializeRules(cls, useexrules):
        myvalidator.varmustbeboolean(useexrules, varnm="useexrules");
        mky = ("allexrules" if (useexrules) else "allonlyrules");
        return cls.getValueOfVarIfPresentOnTableMain(mky);
    @classmethod
    def getSerializeOnlyRules(cls): return cls.getSerializeOnlyORExclusiveSerializeRules(False);
    @classmethod
    def getExclusiveSerializeRules(cls): return cls.getSerializeOnlyORExclusiveSerializeRules(True);



    @classmethod
    def getOtherKnownSafeAttributesOnTheClass(cls):
        return [attr for attr in dir(cls)
                if (type(getattr(cls, attr)) in [int, float, str, list, tuple] and
                    attr not in ["__module__", "all"])];
        #mycol could be on the list of stuff to serialize,
        #but there is already a method specifically for that

    @classmethod
    def getKnownAttributeNamesOnTheClass(cls, useserial=False):
        myvalidator.varmustbeboolean(useserial, "useserial");
        mycols = cls.getMyCols();
        safelist = cls.getOtherKnownSafeAttributesOnTheClass();
        unsafelist = cls.getForeignKeyObjectNamesFromCols(mycols);
        mlist = myvalidator.combineTwoLists(safelist, unsafelist);
        #print(f"safelist = {safelist}");
        #print(f"unsafelist = {unsafelist}");
        #print(f"init mlist = {mlist}");
        
        myvalidator.varmustnotbeempty(mlist, "mlist");
        mxlist = [];#exclusion list for serialization
        for nm in cls.getMyColAttributeNames():
            if (useserial): mxlist.append(nm);
            else:
                if (nm not in mlist): mlist.append(nm);
            if (nm + "_value" not in mlist): mlist.append(nm + "_value");
        #print(f"NEW mlist = {mlist}");
        
        myrefcols = cls.getMyRefCols();
        for nm in cls.getMyRefColAttributeNames():
            if (useserial): mxlist.append(nm);
            else:
                if (nm not in mlist): mlist.append(nm);
        for nm in cls.getMyRefColNames(myrefcols):
            if (nm not in mlist): mlist.append(nm);
        #print(f"NEW mlist = {mlist}");
        
        tnmattrnm = cls.getNameOfVarIfPresentOnTableMain("tablename");
        mcsattrnm = cls.getNameOfVarIfPresentOnTableMain("multi_column_constraints_list");
        acsattrnm = cls.getNameOfVarIfPresentOnTableMain("allconstraints_list");
        
        exrulesnm = None;
        hasexrules = True;
        try:
            exrulesnm = cls.getNameOfVarIfPresentOnTableMain("allexrules");
        except Exception as ex:
            hasexrules = False;
        onlyrulesnm = None;
        hasonlyrules = True;
        try:
            onlyrulesnm = cls.getNameOfVarIfPresentOnTableMain("allonlyrules");
        except Exception as ex:
            hasonlyrules = False;
        
        if (useserial):
            mxlist.append(tnmattrnm);
            mxlist.append(mcsattrnm);
            mxlist.append(acsattrnm);
            if (hasexrules): mxlist.append(exrulesnm);
            if (hasonlyrules): mxlist.append(onlyrulesnm);
        else:
            if (tnmattrnm not in mlist): mlist.append(tnmattrnm);
            if (mcsattrnm not in mlist): mlist.append(mcsattrnm);
            if (acsattrnm not in mlist): mlist.append(acsattrnm);
            if (hasexrules and exrulesnm not in mlist): mlist.append(exrulesnm);
            if (hasonlyrules and onlyrulesnm not in mlist): mlist.append(onlyrulesnm);
        if (useserial): mxlist.append("all");
        elif ("all" not in mlist): mlist.append("all");
        #print(f"FINAL mlist = {mlist}");
        
        myretlist = [item for item in mlist if item not in mxlist];
        #print(f"myretlist = {myretlist}");
        
        myvalidator.listMustContainUniqueValuesOnly(myretlist, "myretlist");
        return myretlist;
    @classmethod
    def getAllKnownAttributeNamesOnTheClass(cls): return cls.getKnownAttributeNamesOnTheClass(False);
    @classmethod
    def getKnownAttributeNamesOnTheClassForSerialization(cls):
        return cls.getKnownAttributeNamesOnTheClass(True);
    @classmethod
    def getTheExclusionListForSerialization(cls):
        alllist = cls.getAllKnownAttributeNamesOnTheClass();
        serlist = cls.getKnownAttributeNamesOnTheClassForSerialization();
        if (myvalidator.isvaremptyornull(serlist)): return alllist;
        else: return [item for item in alllist if item not in serlist];


    #constraint methods here

    @classmethod
    def getAndSetMultiColumnConstraints(cls):
        mlist = None;
        try:
            mlist = cls.getMultiColumnConstraints();
        except Exception as ex:
            setattr(cls, "mymulticolargs", mlist);
    

    #possible bug found 5-4-2025 12:29 AM MISSING METHOD
    #NEED TO MAKE A METHOD TO ADD OR REMOVE A MULTI-COLUMN CONSTRAINT...
    #ONE OTHER THING, THIS METHOD MAY BE DEPENDENT ON HOW AND WHEN THE TABLE WAS CREATED...
    #REMOVING THESE CONSTRAINTS CAN HAVE NASTY CONSEQUENCES AND SO CAN ADDING THEM
    #AFTER THE TABLE WAS CREATED.

    #NOT DONE YET HERE 5-6-2025 6:56 PM MST

    @classmethod
    def addOrDropAConstraintAfterTableExists(cls, mval, useadd, runbkbfr=False, runbkaftr=False,
                                             mcolobj=None):
        myvalidator.varmustbeboolean(useadd, "useadd");
        myvalidator.varmustbeboolean(runbkbfr, "runbkbfr");
        myvalidator.varmustbeboolean(runbkaftr, "runbkaftr");
        #at any rate, we need to:
        #1. back up the data (if that has not already been done so),
        #-but the backup files will have the OLD create table statement and all old data
        #--even the insert into commands will be different.
        #-when we restore the data, we want to use the NEW create table statement
        #-we also want to use the NEW insert into statements
        #-we may also need the user to provide new information if the cols have changed
        #-if the col names got renamed, then the restore will need to know what the
        #--old col names were and will need to map it with the new ones
        #-if new cols are added or are totally different,
        #--then the restore will need to know the new data...
        #-the backup methods do not change the existing objects in memory
        #--the user might be able to take advantage of this and update the data this way.
        #--however if the objects did not exist when running the restore,
        #---the user may not have access to them.
        #
        #if we just added or dropped a constraint only the old data will be used.
        #--(if added a constraint some of the old data might not get restored).
        #if we added a new column entirely, we need new data and the old data.
        #if we change data types for one col, we need new data for that col and the old data.
        #if we just renamed column names, then we only need old data with the new names.
        #if we just deleted a column entirely, we need the old data new names.
        #if we just renamed a table name, then we need the old name and the one.
        #if we just deleted an entire table, then only the old data will be used.
        #if a combination is used it depends on what changes were made will determine
        #-if we need new only or old only or both old and new data.
        #
        #2. get rid of the current table,
        #3. then add the new constraint
        #4. then create the new table
        #5. then attempt to restore the old data
        #
        #we may just want to backup only a specific table and not all of them to save space
        #this may be a good idea, but it can bite you in the ass when you go to restore it...
        #
        print("BEFORE ATTEMPTING TO ADD OR DROP THE CONSTRAINT AFTER DROPPING THE TABLE!");
        print(f"OLD mval = {mval}");
        usecolobj = (not myvalidator.varisnull(mcolobj));
        if (usecolobj): print(f"OLD mcolobj.getConstraints() = {mcolobj.getConstraints()}");
        else: print(f"OLD cls.getMultiColumnConstraints() = {cls.getMultiColumnConstraints()}");

        cls.clearThenDropTable(onlyifnot=True, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
        if (cls.tableExists()): raise ValueError("failed to drop the table!");
        else:
            #mycolobj and the other just needs to know the class
            if (usecolobj): mcolobj.addOrRemoveConstraint(mval, useadd, isinctable=False);
            else: cls.addOrRemoveMultiColumnConstraint(mval, useadd);
        cls.createTable();

        #now attempt to restore the data
        raise ValueError("NEED TO DO A LOT HERE TO ADD THE CONSTRAINT SINCE THE " +
                                    "TABLE ALREADY EXISTS!");
        #raise ValueError("NOT DONE YET 5-28-2025 10:37 PM MST!");

    @classmethod
    def addOrRemoveMultiColumnConstraint(cls, mval, useadd, runbkbfr=False, runbkaftr=False):
        myvalidator.varmustbeboolean(useadd, "useadd");
        myvalidator.varmustbeboolean(runbkbfr, "runbkbfr");
        myvalidator.varmustbeboolean(runbkaftr, "runbkaftr");
        if (myvalidator.isvaremptyornull(mval)): pass;
        else:
            #if the table already exists on the DB, then we have a problem...
            #as changing the constraints may cause serious needs
            #alter table command is not always supported and varies significantly...
            #if the constraint is already present on the list of constraints, then do not add it
            myvalidator.varmustbethetypeonly(mval, str, "mval");
            mlist = cls.getAndSetMultiColumnConstraints();
            isonlist = (False if (myvalidator.isvaremptyornull(mlist)) else (mval in mlist));
            if (isonlist == useadd): pass;
            else:
                if (cls.tableExists()):
                    cls.addOrDropAConstraintAfterTableExists(mval, useadd, runbkbfr=runbkbfr,
                                                             runbkaftr=runbkaftr, mcolobj=None);
                else:
                    #safe to add it...
                    #get the attribute name
                    #get the old value (mlist)
                    #add the new value to the old value...
                    nlist = None;
                    if (useadd):
                        nlist = ([mval] if (myvalidator.isvaremptyornull(mlist)) else
                                 ([item for item in mlist] if (mval in mlist) else
                                  [item for item in mlist].append(mval)));
                    else:
                        premex = False;
                        if (myvalidator.isvaremptyornull(mlist)):
                            if (mlist == None): pass;
                            else: nlist = [];
                            premex = True;
                        else:
                            if (mval in mlist): pass;
                            else: premex = True;
                            nlist = [item for item in mlist if not item == mval];
                        if (premex):
                            print("WARNING: you attempted to remove mval = " + mval +
                                  ", but it was not on the list!");
                            traceback.print_stack();
                    setattr(cls, cls.getNameOfVarIfPresentOnTableMain("multi_column_constraints_list"),
                            nlist);
    #add a multi-column constraint convenience methods here
    @classmethod
    def addMultiColumnConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.addOrRemoveMultiColumnConstraint(mval, True, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def addMultiColConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.addMultiColumnConstraint(mval, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def addAMultiColConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.addMultiColumnConstraint(mval, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def addAMultiColumnConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.addMultiColumnConstraint(mval, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    #remove a multi-column constraint convenience methods here
    @classmethod
    def removeMultiColumnConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.addOrRemoveMultiColumnConstraint(mval, False, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeMultiColConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.removeMultiColumnConstraint(mval, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeAMultiColConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.removeMultiColumnConstraint(mval, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeAMultiColumnConstraint(cls, mval, runbkbfr=False, runbkaftr=False):
        cls.removeMultiColumnConstraint(mval, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    
    @classmethod
    def getAMultiColumnConstraintByName(cls, cnstnm):
        mcnstsbynm = [cnst for cnst in cls.getMultiColumnConstraints()
                      if myvalidator.getNameFromConstraint(cnst) == cnstnm];
        return (None if (myvalidator.isvaremptyornull(mcnstsbynm)) else mcnstsbynm[0]);
    @classmethod
    def getAMultiColConstraintByName(cls, cnstnm): return cls.getAMultiColumnConstraintByName(cnstnm);
    @classmethod
    def getMultiColumnConstraintByName(cls, cnstnm): return cls.getAMultiColumnConstraintByName(cnstnm);
    @classmethod
    def getMultiColConstraintByName(cls, cnstnm): return cls.getAMultiColumnConstraintByName(cnstnm);

    @classmethod
    def removeAMultiColumnConstraintByName(cls, cnstnm, runbkbfr=False, runbkaftr=False):
        cls.removeAMultiColumnConstraint(cls.getAMultiColConstraintByName(cnstnm),
                                         runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeAMultiColConstraintByName(cls, cnstnm, runbkbfr=False, runbkaftr=False):
        cls.removeAMultiColumnConstraintByName(cnstnm, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeMultiColConstraintByName(cls, cnstnm, runbkbfr=False, runbkaftr=False):
        cls.removeAMultiColumnConstraintByName(cnstnm, runbkbfr=runbkbfr, runbkaftr=runbkaftr);
    @classmethod
    def removeMultiColumnConstraintByName(cls, cnstnm, runbkbfr=False, runbkaftr=False):
        cls.removeAMultiColumnConstraintByName(cnstnm, runbkbfr=runbkbfr, runbkaftr=runbkaftr);


    @classmethod
    def getAllTableConstraints(cls, fetchnow=False):
        #will have all of the multi-column constraints args list on it
        #plus all of the individual col arguments or constraints on it
        myvalidator.varmustbeboolean(fetchnow, "fetchnow");
        if (cls.isVarPresentOnTableMain("allconstraints_list")):
            valofall = cls.getValueOfVarIfPresentOnTableMain("allconstraints_list");
            if (myvalidator.isvaremptyornull(valofall)): pass;
            else:
                # if (cls.disableconstraintswarning): pass;
                # else:
                #     allattrp = cls.getNameOfVarIfPresentOnTableMain("allconstraints_list");
                #     print("");
                #     print("WARNING: you provided a " + allattrp + " attribute in the class (" +
                #         cls.__name__ + "), the list you provided will be used and not the " +
                #         "generated one! If this is not the desired behavior, please remove it! " +
                #         "This warning can safely be ignored!");
                #     print("");
                if (fetchnow): pass;
                else: return valofall;

        mclconstraints = cls.getMultiColumnConstraints();
        myiclconstraints = cls.getIndividualColumnConstraints();
        nwlist = myvalidator.combineTwoLists(myiclconstraints, mclconstraints);
        #print(f"cls.__name__ = {cls.__name__}");
        #print(f"mclconstraints = {mclconstraints}");
        #print(f"myiclconstraints = {myiclconstraints}");
        #print(f"nwlist = {nwlist}");

        #setattr(cls, "tableargs", ([] if (nwlist == None) else nwlist));
        return nwlist;

    @classmethod
    def getAndSetAllTableConstraints(cls, fetchnow=False):
        nwlist = cls.getAllTableConstraints(fetchnow);
        setattr(cls, "tableargs", ([] if (nwlist == None) else nwlist));
