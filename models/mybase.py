from mycol import mycol;
from mycol import myvalidator;
from myrefcol import myrefcol;
from init import SQLVARIANT;
import traceback;
class mybase:
    #mytablename = "basetablename";
    #mymulticolargs = None;
    #disableconstraintswarning = False;

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

        print(f"DONE WITH THE SETUP METHOD FOR {cls.__name__}!\n");
    
    #depends on the all list existing and being set for all of the classes that is a subclass of mybase
    #and not mybase before this runs.
    #this method sets up the refcols here.
    @classmethod
    def setupPartB(cls, calledinmain=False):
        myvalidator.varmustbeboolean(calledinmain, "calledinmain");
        if (issubclass(cls, mybase) and not (cls == mybase)):
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
    @classmethod
    def updateAllLinkRefsForMyClass(cls): cls.setupPartB(True);

    @classmethod
    def setupMain(cls):
        mlist = mycol.getMyClassRefsMain(True);
        isempty = myvalidator.isvaremptyornull(mlist);
        if (isempty): pass;
        else:
            for mclsref in mlist:
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)): mclsref.setupPartA();
            
            #due to a dependency on the all list existing and being set for all of the classes
            #(that are a subclass of mybase and not mybase),
            #we need to set the refcols here essentially after the setup method has run.
            #therefore it must be done in a separate loop after all of partA has finished running.

            for mclsref in mlist:
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)): mclsref.setupPartB(True);
        mycol.setRanSetup(not isempty);

    def __init__(self, colnames=None, colvalues=None):
        print("INSIDE BASE CLASS CONSTRUCTOR CALLING SETUP IF NEEDED FIRST!");
        #print(f"mycol.hasRunSetupYet() = {mycol.hasRunSetupYet()}");
        if (not mycol.hasRunSetupYet()): type(self).setupMain();
        mytempcols = type(self).getMyCols();
        mycolnames = type(self).getMyColNames(mytempcols);
        print("INSIDE BASE CLASS CONSTRUCTOR AFTER SETUP CALL!");
        print(f"type(self) = {type(self)}");
        print(f"mytablename = {type(self).getTableName()}");
        print(f"mycolnames = {mycolnames}");
        print(f"colnames = {colnames}");
        print(f"colvalues = {colvalues}");

        #for each column if it is a foreign key, now need to evaluate the class string
        #but need and the link col name
        #over here call the validation method for the new foreign key...
        #colname is already set we need to validate it.
        #we also need the class reference for validation purposes.
        #USING GLOBALS DOES NOT WORK IN THIS CASE SO CANNOT DO STRING TO REF CONVERSION.

        varstr = "" + SQLVARIANT;
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
            mc.primaryKeyInformationMustBeValid(type(self));
            mc.foreignKeyInformationMustBeValid(self);

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
                print(f"clnm = {clnm}");
                print(f"valcl = {valcl}");

                if (clnm in mycolnames):
                    mycolobj = mytempcols[mycolnames.index(clnm)];
                    print(f"mycolobj = {mycolobj}");

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

                    #they either all agree or the computed num holds the coorect value now
                    valcl = mynum;
                else:
                    print("TYPE IS NOT AN INTEGER!");
                    valcl = (deftpvalcl if (defvaloncl == None) else defvaloncl);
            
            if (getfromdb): setattr(self, clnm + "_value", valcl);
            else: self.setValueForColName(clnm, valcl, mycolobj);
        
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
        mybase.updateAllForeignKeyObjectsForAllClasses();
        mybase.updateAllLinkRefsForAllClasses();

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

    def getValueForColName(self, clnm):
        myvalidator.stringMustHaveAtMinNumChars(clnm, 1, "clnm");
        return getattr(self, clnm + "_value");

    def setValueForColName(self, clnm, valcl, mycolobj=None):
        myvalidator.stringMustHaveAtMinNumChars(clnm, 1, "clnm");
        if (mycolobj == None):
            return self.setValueForColName(clnm, valcl, type(self).getMyColObjFromName(clnm));
        else: myvalidator.varmustnotbenull(mycolobj, "mycolobj");
        varstr = "" + SQLVARIANT;
        errmsgpta = "invalid value (";
        errmsgptb = ") used here for the data type (";
        mvaldtp = mycolobj.getDataType();
        errptbwithdata = errmsgptb + (mvaldtp if (type(mvaldtp) == str) else str(mvaldtp));
        errmsgptc = ") for the variant (" + varstr + ")!";
        print(f"clnm = {clnm}");
        print(f"valcl = {valcl}");
        print(f"mycolobj = {mycolobj}");

        if (type(valcl) == list):
            if (mycolobj.isforeignkey):
                if (1 < len(valcl)):
                    #get the foreign col object now
                    
                    #in order for this method below to work it requires that the:
                    #self is the column object
                    #fcobj is the calling object that contains that column (so this is the real self).
                    #foreign class is the string name of the foreign class.
                    myfcoldatainfoobj = mycolobj.genForeignKeyDataObjectInfo(self);
                    #print();
                    #print(f"myfcoldatainfoobj = {myfcoldatainfoobj}");
                    #print();

                    myclsref = myfcoldatainfoobj["fclassref"];
                    myfcols = myfcoldatainfoobj["myfcols"];
                    myfccolnames = myfcoldatainfoobj["myfccolnames"];
                    mycolis = myfcoldatainfoobj["mycolis"];
                    mcolobjs = myfcoldatainfoobj["mcolobjs"];
                    myvalidator.varmustnotbenull(self, "self");
                    myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                    #names referenced by the foreign key
                    print(f"mycolobj.foreignColNames = {mycolobj.foreignColNames}");
                    print(f"myfccolnames = {myfccolnames}");#all of the col names in the foreign class
                    
                    myvalidator.listMustContainUniqueValuesOnly(mycolobj.foreignColNames,
                                                                "mycolobj.foreignColNames");

                    print(f"mycolis = {mycolis}");

                    #now get that column object and check to see if the isunique is set to true?
                    #OR is primary key and the only primary key on that table?
                    print(f"mcolobjs = {mcolobjs}");

                    for n in range(len(valcl)):
                        itemval = valcl[n];
                        dtpval = mvaldtp[n];
                        print(f"itemval = {itemval}");
                        print(f"dtpval = {dtpval}");
                        print(f"mcolobjs[{n}].getColName() = {mcolobjs[n].getColName()}");
                        print(f"mycolobj.foreignColNames[{n}] = {mycolobj.foreignColNames[n]}");
                        print(f"issigned = {mcolobjs[n].getIsSigned()}");
                        print(f"isnonnull = {mcolobjs[n].getIsNonNull()}");

                        if (mcolobjs[n].getColName() == mycolobj.foreignColNames[n]): pass;
                        else: raise ValueError("the col names must match, but they did not!");

                        if (myvalidator.isValueValidForDataType(dtpval, itemval, varstr,
                                                                not(mcolobjs[n].getIsSigned()),
                                                                mcolobjs[n].getIsNonNull())):
                            pass;
                        else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
                    
                    print("setting the column to the value here!");
                    setattr(self, clnm + "_value", valcl);
                    self.runValidatorsByKeysForClass([clnm]);
                    #mycol.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                    #myvalidator.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                else: return self.setValueForColName(clnm, valcl[0], mycolobj);
            else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
        else:
            if (myvalidator.isValueValidForDataType(mvaldtp, valcl, varstr, not(mycolobj.getIsSigned()),
                                                    mycolobj.getIsNonNull())):
                print("setting the column to the value here!");
                setattr(self, clnm + "_value", valcl);
                self.runValidatorsByKeysForClass([clnm]);
                #mycol.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                #myvalidator.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
            else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
        if (mycolobj.isforeignkey): mybase.updateAllForeignKeyObjectsForAllClasses();

    #returns None if not found instead of throwing an error
    @classmethod
    def getObjectFromGivenKeysAndValues(cls, mlist, keys, values):
        print(f"mlist = {mlist}");
        print(f"keys = {keys}");
        print(f"values = {values}");

        tperrmsg = "invalid data type found and used here for the values! There are multiple keys, ";
        tperrmsg += "so there must be multiple values!";
        if (myvalidator.isvaremptyornull(mlist)): return None;
        else:
            klen = len(keys);
            isvalslist = (type(values) in [list, tuple]);
            print(f"klen = {klen}");
            print(f"isvalslist = {isvalslist}");

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
                    print(f"mattr = {mattr}");
                    print(f"mval = {mval}");

                    if (hasattr(mobj, mattr + "_value")):
                        if (mval == getattr(mobj, mattr + "_value")): pass;
                        else:
                            print("not found on this object moving on to the next one!");
                            fndallvals = False;
                            break;
                    else: return None;
                if (fndallvals): return mobj;
        
            print("the object with those values for those columns was not found on the list!");
            return None;

    def getForeignKeyObjectFromCol(self, mc):
        print(f"mc = {mc}");
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
            print("WE NEED TO CREATE AN OBJECT FOR THE COLUMN HERE!");
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
            print(f"GOT THE REFERENCE CLASS NAME {mcref.__name__}!");
            print(f"foreign col names = {mc.getForeignColNames()}");
            print(f"my col name = {mc.getColName()}");
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
        print(f"mobjnms = {mobjnms}");

        mobjs = self.getForeignKeyObjectsFromCols(mycols);
        print(f"mobjs = {mobjs}");

        myvalidator.listMustContainUniqueValuesOnly(mobjnms, "mobjnms");
        myvalidator.twoArraysMustBeTheSameSize(mobjnms, mobjs);

        for n in range(len(mobjnms)):
            mobj = mobjs[n];
            mnm = mobjnms[n];
            print(f"mobj = {mobj}");
            print(f"mnm = {mnm}");
            
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
            
            
            print("val of the new attribute should be the initial value!");
            print(getattr(self, mnm));
            #print(getattr(self, mnm).fget(self));
            
            print("now setting the value here.");
            #getattr(self, mnm).fset(self, mobj);
            setattr(self, mnm, mobj);
            print("val of the property should now be the object!");
            print(getattr(self, mnm));
            #raise ValueError("NOT DONE YET 4-15-2025 10:44 PM MST!");
        return mobjs;

    #update all foreign key objects methods:
    
    @classmethod
    def updateAllForeignKeyObjectsForMyClass(cls):
        #from mybase import mybase;
        if (issubclass(cls, mybase)):
            if (myvalidator.isvaremptyornull(cls.all)): pass;
            else:
                print(f"\nBEGIN WORKING ON THOSE FOR {cls.__name__}!");
                for mobj in cls.all: mobj.getAndSetForeignKeyObjectsFromCols(cls.getMyCols());
                print(f"\nDONE WITH THOSE FOR {cls.__name__}!");

    @classmethod
    def updateAllForeignKeyObjectsForAllClasses(cls):
        print("\nUPDATING ALL OBJECT REFS FROM FOREIGN KEYS NOW:\n");
        mlist = mycol.getMyClassRefsMain(True);
        if (myvalidator.isvaremptyornull(mlist)): pass;
        else:
            for mclsref in mlist:
                #from mybase import mybase;
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)):
                    mclsref.updateAllForeignKeyObjectsForMyClass();   
        print("DONE UPDATING ALL OBJECT REFS FROM FOREIGN KEYS NOW!");

    @classmethod
    def updateAllLinkRefsForAllClasses(cls):
        print("\nUPDATING ALL LINK REFS FROM FOREIGN KEYS NOW:\n");
        mlist = mycol.getMyClassRefsMain(True);
        if (myvalidator.isvaremptyornull(mlist)): pass;
        else:
            for mclsref in mlist:
                #from mybase import mybase;
                if (issubclass(mclsref, mybase) and not (mclsref == mybase)):
                    mclsref.updateAllLinkRefsForMyClass();#mclsref.setupPartB(True);
        print("DONE UPDATING ALL LINK REFS FROM FOREIGN KEYS NOW!");

    def printValuesForAllCols(self, mycols=None):
        fincols = type(self).getMyColsFromClassOrParam(mycols);
        for mc in self.getMyColNames(fincols):
            print(f"val for colname {mc} is: {self.getValueForColName(mc)}");

    def getKnownAttributeNamesForRepresentation(self):
        return [nm for nm in type(self).getKnownAttributeNamesOnTheClass()];

    def __myrepr__(self, exobjslist=None, usesafelistonly=False):
        myvalidator.varmustbeboolean(usesafelistonly, "usesafelistonly");
        mstr = "<" + self.__class__.__name__ + " ";
        unsafelist = type(self).getForeignKeyObjectNamesFromCols();
        nmscls = self.getKnownAttributeNamesForRepresentation();
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

    #def __to_dict(self):
    #    raise ValueError("NOT DONE YET 4-19-2025 1:20 AM MST!");
        

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
        return [(mc.constraints if (useclist) else mc) for mc in cls.getMyColsFromClassOrParam(mycols)
                if not myvalidator.isvaremptyornull(mc.constraints)];
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
    def getListOfPossibleNamesForVariable(cls, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)): return cls.varMustBePresentOnTable("varnm");
        if (varnm == "tablename"): return cls.getPossibleTableNames();
        elif (varnm == "multi_column_constraints_list"):
            return cls.getMultiColumnConstraintVariableNames();
        elif (varnm == "allconstraints_list"): return cls.getAllConstraintVariableNames();
        else:
            raise ValueError("variable name " + varnm +
                             " not recognized or is not associated with a list!");

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

    @classmethod
    def getNameOrValueOfVarIfPresentOnTable(cls, usename, ilist=None, varnm="varnm"):
        myvalidator.varmustbeboolean(usename, "usename");
        myresobj = cls.getValObjectIfPresent(ilist, varnm);
        if (myvalidator.isvaremptyornull(myresobj)):
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

    @classmethod
    def getAndSetMultiColumnConstraints(cls):
        mlist = cls.getMultiColumnConstraints();
        setattr(cls, "mymulticolargs", mlist);

    @classmethod
    def getOtherKnownSafeAttributesOnTheClass(cls):
        return [attr for attr in dir(cls)
                if (type(getattr(cls, attr)) in [int, float, str, list, tuple] and
                    attr not in ["__module__", "all"])];
        #mycol could be on the list of stuff to serialize,
        #but there is already a method specifically for that

    @classmethod
    def getKnownAttributeNamesOnTheClass(cls):
        mycols = cls.getMyCols();
        safelist = cls.getOtherKnownSafeAttributesOnTheClass();
        unsafelist = cls.getForeignKeyObjectNamesFromCols(mycols);
        mlist = myvalidator.combineTwoLists(safelist, unsafelist);
        myvalidator.varmustnotbeempty(mlist, "mlist");
        for nm in cls.getMyColAttributeNames():
            mlist.append(nm);
            mlist.append(nm + "_value");
        myrefcols = cls.getMyRefCols();
        for nm in cls.getMyRefColAttributeNames(): mlist.append(nm);
        for nm in cls.getMyRefColNames(myrefcols): mlist.append(nm);
        tnmattrnm = cls.getNameOfVarIfPresentOnTableMain("tablename");
        mcsattrnm = cls.getNameOfVarIfPresentOnTableMain("multi_column_constraints_list");
        acsattrnm = cls.getNameOfVarIfPresentOnTableMain("allconstraints_list");
        if (tnmattrnm not in mlist): mlist.append(tnmattrnm);
        if (mcsattrnm not in mlist): mlist.append(mcsattrnm);
        if (acsattrnm not in mlist): mlist.append(acsattrnm);
        if ("all" not in mlist): mlist.append("all");
        return mlist;

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
        print(f"cls.__name__ = {cls.__name__}");
        print(f"mclconstraints = {mclconstraints}");
        print(f"myiclconstraints = {myiclconstraints}");
        print(f"nwlist = {nwlist}");

        #setattr(cls, "tableargs", ([] if (nwlist == None) else nwlist));
        return nwlist;

    @classmethod
    def getAndSetAllTableConstraints(cls, fetchnow=False):
        nwlist = cls.getAllTableConstraints(fetchnow);
        setattr(cls, "tableargs", ([] if (nwlist == None) else nwlist));
