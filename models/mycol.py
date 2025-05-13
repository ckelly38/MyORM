from myvalidator import myvalidator;
import sys;
import inspect;
import traceback;
import functools;
from init import SQLVARIANT;
class mycol:
    #everything to init will need to be removed to solve an import problem between
    #this and the sql generator
    __myclassrefs__ = None;
    __ucconscntr__ = 0;
    __ccconscntr__ = 0;
    __all_validators__ = None;
    __ransetup__= False;

    #constraint counter methods

    @classmethod
    def getMyUniqueOrCheckConstraintCounter(cls, useuctr):
        myvalidator.varmustbeboolean(useuctr, "useuctr");
        return (cls.__ucconscntr__ if (useuctr) else cls.__ccconscntr__);

    @classmethod
    def setMyUniqueOrCheckConstraintCounter(cls, nval, useuctr):
        myvalidator.varmustbeboolean(useuctr, "useuctr");
        myvalidator.varmustbethetypeonly(nval, int, "nval");
        myvalidator.valueMustBeInRange(nval, 0, 0, True, False, "nval");
        if (useuctr): cls.__ucconscntr__ = nval;
        else: cls.__ccconscntr__ = nval;
    @classmethod
    def setMyUniqueConstraintCounter(cls, nval):
        cls.setMyUniqueOrCheckConstraintCounter(nval, True);
    @classmethod
    def setMyCheckConstraintCounter(cls, nval):
        cls.setMyUniqueOrCheckConstraintCounter(nval, False);
    
    @classmethod
    def incrementAndGetUniqueOrCheckConstraintCounterBy(cls, useuctr, intval=1):
        myvalidator.varmustbethetypeonly(intval, int, "intval");
        cls.setMyUniqueOrCheckConstraintCounter(cls.getMyUniqueOrCheckConstraintCounter(useuctr) +
                                                intval, useuctr);
        return cls.getMyUniqueOrCheckConstraintCounter(useuctr);
    @classmethod
    def incrementAndGetUniqueConstraintCounterBy(cls, intval=1):
        return cls.incrementAndGetUniqueOrCheckConstraintCounterBy(True, intval);
    @classmethod
    def incrementAndGetCheckConstraintCounterBy(cls, intval=1):
        return cls.incrementAndGetUniqueOrCheckConstraintCounterBy(False, intval);

    @classmethod
    def decrementAndGetUniqueOrCheckConstraintCounterBy(cls, useuctr, intval=1):
        myvalidator.varmustbethetypeonly(intval, int, "intval");
        cls.setMyUniqueOrCheckConstraintCounter(cls.getMyUniqueOrCheckConstraintCounter(useuctr) -
                                                intval, useuctr);
        return cls.getMyUniqueOrCheckConstraintCounter(useuctr);
    @classmethod
    def decrementAndGetUniqueConstraintCounterBy(cls, intval=1):
        return cls.decrementAndGetUniqueOrCheckConstraintCounterBy(True, intval);
    @classmethod
    def decrementAndGetCheckConstraintCounterBy(cls, intval=1):
        return cls.decrementAndGetUniqueOrCheckConstraintCounterBy(False, intval);

    
    #validator methods

    @classmethod
    def getAllValidators(cls): return cls.__all_validators__;

    @classmethod
    def getMyValidators(cls, mcnm):
        myvalidator.stringHasAtMinNumChars(mcnm, 1);
        myvalidator.stringContainsOnlyAlnumCharsIncludingUnderscores(mcnm);
        return [item for item in cls.getAllValidators() if (item["classname"] == mcnm)];

    @classmethod
    def getMyValidatorsThatContainKeys(cls, mcnm, mkys):
        return [item for item in cls.getMyValidators(mcnm)
                if (myvalidator.isListAInListB(mkys, item["keys"]))];

    @classmethod
    def getMyIndividualOrMultiColumnValidators(cls, mcnm, useindiv):
        myvalidator.varmustbeboolean(useindiv, "useindiv");
        return [item for item in cls.getMyValidators(mcnm)
                if ((len(item["keys"]) < 2 and useindiv) or (1 < len(item["keys"]) and not useindiv))];
    @classmethod
    def getMyIndividualColumnValidators(cls, mcnm):
        return cls.getMyIndividualOrMultiColumnValidators(mcnm, True);
    @classmethod
    def getMyMultiColumnValidators(cls, mcnm):
        return cls.getMyIndividualOrMultiColumnValidators(mcnm, False);

    @classmethod
    def setAllValidators(cls, vlist):
        #myvalidator.addValidator("Camper", isvalidage, ["age"]);
        #[{classname: "Camper", methodnameorref: isvalidage, colnames: ["age"]}, ...];
        cls.__all_validators__ = vlist;#might be a memory leak here

    #https://www.datacamp.com/tutorial/decorators-python
    #https://stackoverflow.com/questions/961048/get-class-that-defined-method
    #
    #this is a decorator whos only purpose is to register the validator method
    #this does not actually call it.
    #the run methods below call the validator after it is registered.
    #@classmethod
    def validates(*args):#cls, 
        #print();
        #print(f"cls = {cls}");
        #print(f"keys = {args}");

        def myAddVDator(myvfunc):
            #print(f"funcname = {myvfunc.__name__}");
            #print(dir(myvfunc));
            #print(dir(myvfunc.__code__));
            #print(f"funcclassfullname = myvfunc.__qualname__ = {myvfunc.__qualname__}");
            #print(f"keys = {args}");

            mkys = [];
            for ky in args:
                if (type(ky) in [list, tuple]):
                    if (len(args) == 1):
                        for item in ky:
                            if (type(item) == str): mkys.append(item);
                            else: raise TypeError("the type of item on keys must be a string!");
                    else: raise ValueError("args must only have the list of keys on it!");
                elif (type(ky) == str): mkys.append(ky);
                else: raise TypeError("each key must be a list a tuple or a string");
            #print(f"mkys = {mkys}");
            
            #the code for this will be different if using under version 3 of Python.
            mcnm = myvfunc.__qualname__[0: myvfunc.__qualname__.index(myvfunc.__name__) - 1];
            #print(f"mcnm = {mcnm}");
            #print();

            mycol.addValidator(mcnm, myvfunc.__name__, mkys);
            
            #because this is a decorator and not actually calling the function we need to return it
            #this also prevents getattr seeing the function name and thinking that it is None.
            return myvfunc;
        return myAddVDator;

    @classmethod
    def addValidator(cls, classname, methodref, keys):
        #mycol.addValidator("Camper", isvalidage, ["age"]);
        print(f"classname = {classname}");
        print(f"methodref = {methodref}");
        print(f"keys = {keys}");
        myvalidator.varmustnotbeempty(keys, "keys");
        myvalidator.stringHasAtMinNumChars(classname, 1);
        myvalidator.stringContainsOnlyAlnumCharsIncludingUnderscores(classname);
        mlist = cls.getAllValidators();
        clist = ([] if (myvalidator.isvaremptyornull(mlist)) else [item for item in mlist]);
        clist.append({"classname": classname, "methodref": methodref, "keys": keys});
        cls.setAllValidators(clist);
    
    @classmethod
    def removeValidator(cls, classname, keys):
        myvalidator.stringHasAtMinNumChars(classname, 1);
        myvalidator.stringContainsOnlyAlnumCharsIncludingUnderscores(classname);
        if (myvalidator.isvaremptyornull(keys)): return None;
        nlist = [item for item in cls.getAllValidators()
                 if (item["classname"] == classname and myvalidator.doTwoListsContainTheSameData(
                     keys, item["keys"]))];
        cls.setAllValidators(nlist);
    
    @classmethod
    def runGivenValidatorsForClass(cls, mcnm, mobj, mvs):
        nmerrmsg = "the class name of the object (" + type(mobj).__name__ + ") and the given ";
        nmerrmsg += "classname (" + mcnm + ") must match, but they did not!";
        if (type(mobj).__name__ == mcnm): pass;
        else: raise ValueError(nmerrmsg);
        if (myvalidator.isvaremptyornull(mvs)): pass;
        else:
            errmsgpta = "invalid value for the col";
            errmsgptb = ") used for class (" + mcnm + ")!";
            #print(f"mobj = {mobj}");#may error out due to a timing issue if the method is overridden.
            for mv in mvs:
                klist = mv["keys"];
                vlist = [getattr(mobj, ky + "_value") for ky in mv["keys"]];
                errptasornot = "";
                if (1 < len(klist)): errptasornot = "s";
                else:
                    klist = klist[0];
                    vlist = vlist[0];
                myfunc = getattr(mobj, mv["methodref"]);
                finerrmsgpta = errmsgpta + errptasornot + " (";
                if (myfunc(klist, vlist)): pass;
                else: raise ValueError(finerrmsgpta + (", ".join(mv["keys"])) + errmsgptb);
        return True;

    @classmethod
    def runValidatorsByKeysForClass(cls, mcnm, mobj, mkys):
        #if mkys has multiple items on it, then just stick it as is into the runValidators method.
        #if mkys has one item on it, then the given results could have multiple validators which
        #need sorted to run individuals first.
        #if empty skip execution altogether.
        if (myvalidator.isvaremptyornull(mkys)): return True;
        initmvs = cls.getMyValidatorsThatContainKeys(mcnm, mkys);
        finmvslist = None;
        if (len(mkys) == 1):
            #split the validators list into individuals if any and then those with multiple
            #then combine the lists to produce the final list of course.
            #micvs = [vobj for vobj in initmvs if (len(vobj["keys"]) == 1)];
            #mmcvs = [vobj for vobj in initmvs if (1 < len(vobj["keys"]))];
            micvs = [];
            mmcvs = [];
            for vobj in initmvs:
                myvalidator.varmustnotbeempty(vobj["keys"], "vobj[keys]");
                if (len(vobj["keys"]) == 1): micvs.append(vobj);
                else: mmcvs.append(vobj);
            finmvslist = myvalidator.combineTwoLists(micvs, mmcvs);
        else: finmvslist = initmvs;
        return cls.runGivenValidatorsForClass(mcnm, mobj, finmvslist);

    @classmethod
    def runAllValidatorsForClass(cls, mcnm, mobj):
        micvs = cls.getMyIndividualColumnValidators(mcnm);
        mmcvs = cls.getMyMultiColumnValidators(mcnm);
        return cls.runGivenValidatorsForClass(mcnm, mobj, myvalidator.combineTwoLists(micvs, mmcvs));

    
    #has setup run yet methods

    @classmethod
    def hasRunSetupYet(cls): return cls.__ransetup__;

    @classmethod
    def setRanSetup(cls, val):
        myvalidator.varmustbeboolean(val);
        cls.__ransetup__ = val;


    #my class ref methods

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
        for mycls in cls.getMyClassRefsMain(False):
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
                 foreignObjectName=None, constraints=None):#value, 
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
        print(f"foreignObjectName = {foreignObjectName}");
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

        self.setIsInitialized(False);
        self.setForeignClass(foreignClass);
        self.setForeignColNames(foreignColNames);
        self.setIsForeignKey(isforeignkey);
        
        self.setDataType(datatype);
        self.setIsSigned(issigned);
        self.setIsNonNull(isnonnull);
        
        self.setIsUnique(isunique);
        self.setAutoIncrements(autoincrements);
        self.setIsPrimaryKey(isprimarykey);
        self.setColName(colname);
        self.setForeignObjectName(foreignObjectName);

        self.setContext(None);
        self.setMyClassRefs(None);
        self.setContainingClassName(None);
        
        #self._value = value;
        self.setDefaultValue(defaultvalue);
        self.setConstraints(constraints);
        self.setIsInitialized(True);
        print("DONE WITH MYCOL CONSTRUCTOR!");
    
    @classmethod
    def genFKeyDict(cls, fclsnm=None, objname=None, refcolnms=None):
        isfkey = True;
        errmsg = "you provided referenced column names, therefore you must provide the class name, ";
        errmsg += "but you did not!";
        if (myvalidator.isvaremptyornull(refcolnms)):
            if (myvalidator.isvaremptyornull(fclsnm)):
                isfkey = False;
                if (myvalidator.isvaremptyornull(objname)): pass;
                else: return cls.genFKeyDict(fclsnm=fclsnm, objname=None, refcolnms=refcolnms);
            else: return cls.genFKeyDict(fclsnm=None, objname=objname, refcolnms=refcolnms);
        else:
            if (myvalidator.isvaremptyornull(fclsnm)): raise ValueError(errmsg);
            #else: pass;#valid
        return {"isfkey": isfkey, "classname": fclsnm, "objectname": objname, "refcolnames": refcolnms};

    @classmethod
    def newColFromFKeyDict(cls, colname, datatype, defaultvalue, isprimarykey=False, isnonnull=None,
                           isunique=None, issigned=None, autoincrements=False, fkeydict=None,
                           constraints=None):
        if (myvalidator.isvaremptyornull(fkeydict)):
            return cls.newColFromFKeyDict(colname, datatype, defaultvalue, isprimarykey=isprimarykey,
                                          isnonnull=isnonnull, isunique=isunique, issigned=issigned,
                                          autoincrements=autoincrements, fkeydict=cls.genFKeyDict(),
                                          constraints=constraints);
        return mycol(colname, datatype, defaultvalue, isprimarykey=isprimarykey, isnonnull=isnonnull,
                     isunique=isunique, issigned=issigned, autoincrements=autoincrements,
                     isforeignkey=fkeydict["isfkey"], foreignClass=fkeydict["classname"],
                     foreignColNames=fkeydict["refcolnames"], foreignObjectName=fkeydict["objectname"],
                     constraints=constraints);


    #non-constructor methods are below this point

    #if you want to do mycolobj.value, then the context must be set correctly:
    #
    #you must first call mycolobj.setContext or setContainer(containerobj);
    #with the container object.
    #for example if you have a tstclassobj that is an instance of a subclass of the mybase class,
    #then you can use this as the context object.
    #this will of course contain columns like ID for example.
    #tstclassobj.myidcol.setContext(tstclassobj);
    #then you can use the value like so:
    #print(tstclassobj.myidcol.value);#calls the get
    #tstclassobj.myidcol.value = newval;#calls the set
    #because now the value property has the context it needs.
    #the get and set value methods actually call it on the object.
    #so the get and set value methods must be an instance of a subclass of the mybase class.
    #
    #context should not be relied on and these methods are strongly subjective to it.
    #the context is set in the mybase constructor, but it can be overridden by the user.
    #because the cols are class attributes, one cannot assume the context is correct.

    def getIsInitialized(self): return self.__isinitialized;
    def setIsInitialized(self, mval):
        myvalidator.varmustbeboolean(mval, "mval");
        self.__isinitialized = mval;
    
    _isinitialialized = property(getIsInitialized, setIsInitialized);

    def getContext(self): return self._context;
    def getContainer(self): return self.getContext();

    def setContext(self, val): self._context = val;
    def setContainer(self, val): self.setContext(val);

    context = property(getContext, setContext);

    def getValue(self, mobj):
        myvalidator.varmustnotbenull(mobj, "mobj (aka the context object)");
        from mybase import mybase;
        if (issubclass(type(mobj), mybase)): return mobj.getValueForColName(self.getColName());
        else: raise ValueError("mobj must be a subclass of mybase class!");

    def setValue(self, mobj, val):
        myvalidator.varmustnotbenull(mobj, "mobj (aka the context object)");
        from mybase import mybase;
        if (issubclass(type(mobj), mybase)): mobj.setValueForColName(self.getColName(), val, self);
        else: raise ValueError("mobj must be a subclass of mybase class!");

    def getValueFromContext(self): return self.getValue(self.getContext());

    def setValueFromContext(self, val): self.setValue(self.getContext(), val);

    value = property(getValueFromContext, setValueFromContext);

    def getContainingClassNameFromSelf(self): return self._containingclassname;
    def getContainingClassNameFromContext(self):
        cntxt = self.getContext();
        return (None if (cntxt == None) else cntxt.__class__.__name__);
    def getContainingClassName(self, usecntxt=False):
        myvalidator.varmustbeboolean(usecntxt, "usecntxt");
        if (usecntxt): return self.getContainingClassNameFromContext();
        else: return self.getContainingClassNameFromSelf();

    def setContainingClassName(self, mval):
        #mval can be empty or null or it must follow the requirements...
        if (myvalidator.isvaremptyornull(mval)): pass;
        else:
            mvnm = "the containing class name";
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mval, mvnm);
        self._containingclassname = mval;

    containingclassname = property(getContainingClassName, setContainingClassName);

    def getConstraints(self): return self._constraints;

    def setConstraints(self, mlist):
        if (myvalidator.isvaremptyornull(mlist)): pass;
        else:
            for mval in mlist:
                myvalidator.stringMustHaveAtMinNumChars(mval, 1, "mval");
                if (myvalidator.isConstraintValid(mval)): pass;
                else: raise ValueError("the constraint must be valid, but it was not!");
        self._constraints = mlist;
    
    
    #NEED TO ADD A REMOVE CONSTRAINT METHOD
    #BUT THESE METHODS ARE ALSO SOMEWHAT DEPENDENT ON IF THE TABLE EXISTS IN THE DB.
    #-if we go via class name stored on the mycol object (first we need to store it),
    #second we need to be aware that there might be a timing issue
    #where the class may not be fully initialized yet
    #-if we go via context object, there is the problem where the context can easily be changed
    #therefore due to this being a class attribute it is considdered not reliable,
    #but is a good indicator that the classes may already be fully initialized if not null.
    #
    #NOT DONE YET 5-6-2025 9:57 PM MST

    def addOrRemoveConstraint(self, mval, useadd, isinctable=False):
        myvalidator.varmustbeboolean(useadd, "useadd");
        if (myvalidator.isvaremptyornull(mval)): pass;
        else:
            if (myvalidator.isConstraintValid(mval)): pass;
            else: raise ValueError("the constraint must be valid, but it was not!");

            #exit if no work needs to be done
            mlist = self.getConstraints();
            isonlist = (False if (myvalidator.isvaremptyornull(mlist)) else (mval in mlist));
            if (useadd == isonlist):
                #no work is true;
                if (useadd): pass;
                else:
                    premex = True;
                    if (premex):
                        print("WARNING: you attempted to remove mval = " + mval +
                                ", but it was not on the list!");
                        traceback.print_stack();
                return None;
        

            callset = True;
            myclsref = None;
            usecntxt = False;
            #get the class ref from the context object if usecntxt is true
            #get the class ref from class name stored on mycol here if false
            mycntxt = self.getContext();
            if (usecntxt):
                if (mycntxt == None): usecntxt = False;
            if (usecntxt): myclsref = mycntxt.__class__;
            else: myclsref = mycol.getMyClassRefFromString(self.getContainingClassNameFromSelf());
            if (not isinctable and myclsref.tableExists()):
                #if it is not on our list and not called from createTable,
                #then we assume it is not on the DB.
                #if (useadd):
                #    ?;
                #else:
                #    ?;
                print(f"mval = {mval}");
                print(f"self.getConstraints() = {self.getConstraints()}");
                raise ValueError("NEED TO DO A LOT HERE TO ADD THE CONSTRAINT SINCE THE " +
                                 "TABLE ALREADY EXISTS!");
            else:
                #now add or remove it to or from the constraints list.
                #get the current list for this, create an exact copy of it,
                #then add this to the new list
                retlist = None;
                premex = False;
                if (mlist == None):
                    if (useadd): retlist = [mval];
                    else: raise ValueError("this should have already been taken care of above!");
                    #    callset = False;#no need to call set...
                    #    premex = True;
                else:
                    if (useadd):
                        retlist = ["" + cnst for cnst in mlist];
                        if (mval not in retlist): retlist.append(mval);
                        else:
                            #callset = False;
                            raise ValueError("this should have already been taken care of above!");
                    else:
                        if (myvalidator.isvaremptyornull(mlist)):
                            #retlist = [];
                            #premex = True;
                            raise ValueError("this should have already been taken care of above!");
                        else:
                            retlist = ["" + cnst for cnst in mlist if not cnst == mval];
                            if (mval not in mlist):
                                #premex = True;
                                raise ValueError("this should have already been taken care of above!");
                if (premex):
                    print("WARNING: you attempted to remove mval = " + mval +
                            ", but it was not on the list!");
                    traceback.print_stack();
            if (callset): self.setConstraints(retlist);
    def addConstraint(self, mval, isinctable=False):
        self.addOrRemoveConstraint(mval, True, isinctable=isinctable);
    def addAConstraint(self, mval, isinctable=False): self.addConstraint(mval, isinctable=isinctable);
    def removeConstraint(self, mval, isinctable=False):
        self.addOrRemoveConstraint(mval, False, isinctable=False);
    def removeAConstraint(self, mval, isinctable=False):
        self.removeConstraint(mval, isinctable=isinctable);

    constraints = property(getConstraints, setConstraints);


    def getDefaultValueKeyNameForDataTypeObj(self, tpobj):
        return myvalidator.getDefaultValueKeyNameForDataTypeObj(tpobj, self);

    def getDataType(self): return self._datatype;

    #the problem with these two setters are they depend on the SQL variant
    #they need some way inside this class to get the variant by calling a getter.
    #the variant may need to be passed in to the col
    #but the calling class should provide a way to get it?
    #it will be imported or read from some sort of config or passed in as a parameter.
    #
    #there is also another piece of missing data for the default value.

    #the type of val can be a string or a list
    def setDataType(self, val):
        #get data types for the specific variant
        #if the list is empty or null, then assumed valid
        #if on the list, valid
        #if not on the list and list is not empty, then not valid.
        varstr = SQLVARIANT;
        mvtpslist = myvalidator.getSQLDataTypesInfo(varstr);
        mval = None;
        if (type(val) == list):
            valhaspslist = [("(" in item and ")" in item) for item in val];
            mval = [(val[i][0: val[i].index("(")].upper() + val[i][val[i].index("("):]
                    if (valhaspslist[i]) else val[i].upper()) for i in range(len(val))
                    if (myvalidator.stringMustHaveAtMinNumChars(val[i], 1, "val[" + str(i) + "]"))];
        elif (type(val) == str):
            myvalidator.stringMustHaveAtMinNumChars(val, 1, "val");
            valhasps = ("(" in val and ")" in val);
            mval = (val[0: val.index("(")].upper() + val[val.index("("):]
                    if (valhasps) else val.upper());
        else: raise TypeError("the data type of data type must be either a string or a list!");
        if (myvalidator.isvaremptyornull(mvtpslist)): self._datatype = mval;
        else:
            errmsgptone = "invalid data type (";
            errmsgpttwo = ") found and used here for the variant (" + varstr + ")!";
            if (type(val) == str):
                if (myvalidator.isValidDataType(mval, varstr)): self._datatype = mval;
                else: raise ValueError(errmsgptone + mval + errmsgpttwo);
            else:#this is a list
                for item in mval:
                    if (myvalidator.isValidDataType(item, varstr)): pass;
                    else: raise ValueError(errmsgptone + item + errmsgpttwo);
                self._datatype = mval;

    datatype = property(getDataType, setDataType);

    def getIsSigned(self): return self._issigned;
    def isSigned(self): return self.getIsSigned();

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
        errmsg = "invalid value set for signed the type has a default and it is the opposite of this!";
        if (type(self.getDataType()) == list):
            if (val == None): self._issigned = False;
            else:
                myvalidator.varmustbethetypeandornull(val, bool, True, "val"); 
                if (val): raise ValueError(errmsg);
                else: self._issigned = val;
        else:
            tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(self.getDataType(), varstr);
            if (tpobj["signedhasadefault"]):
                if (val == None): self._issigned = not(tpobj["useunsigneddefault"]);
                else:
                    if (val == (not(tpobj["useunsigneddefault"]))): self._issigned = val;
                    else: raise ValueError(errmsg);
            else:
                myvalidator.varmustbethetypeandornull(val, bool, True, "val"); 
                self._issigned = val;

    issigned = property(getIsSigned, setIsSigned);

    def getIsNonNull(self): return self._isnonnull;
    def isNonNull(self): return self.getIsNonNull();

    #if isnonnull is set to None, then the default for the type will be used
    #else it must be true if the nonnull default is true, otherwise it can be either true or false
    def setIsNonNull(self, val):
        varstr = SQLVARIANT;
        errmsg = "invalid value set for nonnull the type has a default and it is the opposite of this!";
        if (type(self.getDataType()) == list):
            if (val == None): self._isnonnull = True;
            else:
                myvalidator.varmustbethetypeandornull(val, bool, True, "val"); 
                if (val): self._isnonnull = val;
                else: raise ValueError(errmsg);
        else:
            tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(self.getDataType(), varstr);
            if (val == None): self._isnonnull = tpobj["isnonnulldefault"];
            else:
                myvalidator.varmustbethetypeandornull(val, bool, True, "val");
                if (tpobj["isnonnulldefault"]):
                    if (val): self._isnonnull = val;
                    else: raise ValueError(errmsg);
                else: self._isnonnull = val;

    isnonnull = property(getIsNonNull, setIsNonNull);

    def getDefaultValue(self): return self._defaultvalue;

    def setDefaultValue(self, val):
        #if we get the type object from the validator, then maybe the type will provide a default
        #if however the type is signed, and has two different ranges, then we will need to
        #pull the parameter value from the user.
        #myvalidator.isValueValidForDataType(tpnm, val, varstr, useunsigned, isnonnull);
        varstr = SQLVARIANT;
        valerrmsgptc = ") found and used here for the variant (" + varstr + ")!";
        if (val == None):
            if (type(self.getDataType()) == list): self._defaultvalue = None;
            else:
                tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(self.getDataType(), varstr);
                mykynm = self.getDefaultValueKeyNameForDataTypeObj(tpobj);
                #print(f"mykynm = {mykynm}");

                self._defaultvalue = myvalidator.getDefaultValueForDataTypeObjWithName(tpobj,
                                                                                       mykynm, False);
        else:
            if (myvalidator.isValueValidForDataType(self.getDataType(), val, varstr,
                                                    not(self.getIsSigned()), self.getIsNonNull())):
                self._defaultvalue = val;
            else:
                valerrmsgptb = ") for data type (" + self.getDataType();
                raise ValueError("invalid default value (" + str(val) + valerrmsgptb + valerrmsgptc);
    
    defaultvalue = property(getDefaultValue, setDefaultValue);

    def getColName(self): return self._colname;
    def getColumnName(self): return self.getColName();

    def setColName(self, val):
        #the colname must be unique on each table
        #(CANNOT BE ENFORCED HERE, BUT WHEN A NEW OBJECT IS CREATED AND SAVED, ETC)
        #the colname cannot be null or empty
        #myvalidator.varmustnotbeempty(val, "val");
        #myvalidator.varmustbethetypeonly(val, str, "val");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(val, "val");
        self._colname = val;
    
    def setColumnName(self, val): self.setColName(val);
    
    colname = property(getColName, setColName);

    def getForeignObjectName(self): return self._foreignobjectname;

    def setForeignObjectName(self, val):
        if (myvalidator.isvaremptyornull(val)): pass;
        else: myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(val, "val");
        self._foreignobjectname = val;

    foreignobjectname = property(getForeignObjectName, setForeignObjectName);


    def getAutoIncrements(self): return self._autoincrements;
    def autoIncrements(self): return self.getAutoIncrements();

    def setAutoIncrements(self, val):
        myvalidator.varmustbethetypeonly(val, bool, "val");
        self._autoincrements = val;

    autoincrements = property(getAutoIncrements, setAutoIncrements);

    def getIsUnique(self): return self._isunique;
    def isUnique(self): return self.getIsUnique();

    def setIsUnique(self, val):
        myvalidator.varmustbethetypeandornull(val, bool, True, "val");
        self._isunique = val;

    isunique = property(getIsUnique, setIsUnique);

    def getIsPrimaryKey(self): return self._isprimarykey;
    def isPrimaryKey(self): return self.getIsPrimaryKey();

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

        pkyerrmsg = "for it to be a primary key, for class(" + myclsref.__name__ ;
        pkyerrmsg += ") it must be non-null and unique!";
        if (1 < len(pkycols)):
            #now get the unique constraints and see if one has those exact columns
            #get the colnames from inside of the unique constraint...
            #then check to see if they are the same
            pkycolnames = myclsref.getMyColNames(pkycols);
            mrefallconstraints = myclsref.getAllTableConstraints();
            #print(f"pkycolnames = {pkycolnames}");
            #print(f"mrefallconstraints = {mrefallconstraints}");
            
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
                        #print(f"mcolstrincond = {mcolstrincond}");
                        
                        tempcolsarr = mcolstrincond.split(", ");
                        #print(f"tempcolsarr = {tempcolsarr}");

                        if (myvalidator.areTwoListsTheSame(tempcolsarr, pkycolnames)):
                            #print("match found so valid!");
                            isvalid = True;
                            break;
            if isvalid: pass;
            else: raise ValueError(pkyerrmsg);
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
                else: raise ValueError(pkyerrmsg);
            else:
                if (self.isnonnull == None): self.setIsNonNull(False);
                if (self.isunique == None): self.setIsUnique(False);
        return True;

    def getForeignClass(self): return self._foreignClass;

    def setForeignClass(self, val):
        #if (val == None or myvalidator.isClass(val)): pass;
        #else: raise ValueError("val must be a class not an object!");
        self._foreignClass = val;
        from mybase import mybase;
        mybase.updateAllForeignKeyObjectsForAllClasses(not self.getIsInitialized());

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
        from mybase import mybase;
        mybase.updateAllForeignKeyObjectsForAllClasses(not self.getIsInitialized());

    foreignColNames = property(getForeignColNames, setForeignColNames);

    #cannot set is foreign key to be true if the foreign class name is not defined and
    #neither is the foreign col name 
    def getIsForeignKey(self): return self._isforeignkey;
    def isForeignKey(self): return self.getIsForeignKey();

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
        from mybase import mybase;
        mybase.updateAllForeignKeyObjectsForAllClasses(not self.getIsInitialized());

    isforeignkey = property(getIsForeignKey, setIsForeignKey);

    
    #these methods for getting the foreign key information and then checking it
    #take in a context object called fcobj
    #
    #if the context object fcobj is None, then we attempt to get the context from our variable
    #called context via self.getContext();
    #
    #if that is still None, now it is an error because the context object is not allowed to be null.
    #
    #a word of warning: the context is set in the mybase class constructor
    #however, this should not be relied on as being correct.
    #because the mycol object is a class attribute to many classes that extend mybase class.

    def genForeignKeyDataObjectInfo(self, fcobj=None, usenoclassobj=False):
        myvalidator.varmustbeboolean(usenoclassobj, "usenoclassobj");
        if (fcobj == None):
            if (usenoclassobj): pass;
            else:
                cntxt = self.getContext();
                myvalidator.varmustnotbenull(cntxt, "cntxt or fcobj (aka the context object)");
                return self.genForeignKeyDataObjectInfo(cntxt);

        #print("\nGET FOREIGN KEY DATA OBJECT METHOD NOW:");
        #print(f"self.isforeignkey = {self.isforeignkey}");
        #print(f"self.foreignColNames = {self.foreignColNames}");
        #print(f"self.foreignClass = {self.foreignClass}");

        if (self.isforeignkey):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColNames)):
                raise ValueError("the foreign key needs a reference class and a column name!");
            else:
                #print("self is the column object.");
                #print("the calling object is fcobj which is the class instance that has the column!");
                #print(f"fcobj = {fcobj}");

                #check to see if the foreign key values on the column exist on the foreign key class
                
                #self is the column object
                #fcobj is the calling object that contains that column (so this is the real self).
                #foreign class is the string name of the foreign class.
                if (usenoclassobj): pass;
                else: myvalidator.varmustnotbenull(fcobj, "fcobj");
                myclsref = mycol.getMyClassRefFromString(self.foreignClass);
                #print(f"myclsref = {myclsref}");

                myfcols = myclsref.getMyCols();
                myfccolnames = myclsref.getMyColNames(myfcols);
                myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                #names referenced by the foreign key
                #print(f"self.foreignColNames = {self.foreignColNames}");
                #print(f"myfccolnames = {myfccolnames}");#all of the col names in the foreign class
                
                myvalidator.listMustContainUniqueValuesOnly(self.foreignColNames,
                                                            "self.foreignColNames");

                mycolis = [myfccolnames.index(mclnm) for mclnm in self.foreignColNames];
                #print(f"mycolis = {mycolis}");

                #now get that column object and check to see if the isunique is set to true?
                #OR is primary key and the only primary key on that table?
                mcolobjs = [myfcols[mycoli] for mycoli in mycolis];
                #print(f"mcolobjs = {mcolobjs}");
                
                return {"initcolobj": self, "initclassobj": fcobj, "fclassref": myclsref,
                        "myfcols": myfcols, "myfccolnames": myfccolnames, "mycolis": mycolis,
                        "mcolobjs": mcolobjs};
        print(self);
        raise ValueError("the col must be a foreign key, but it was not!");

    
    #NOT DONE YET ENFORCING FOREIGN KEY DATA TYPES bug found 3-29-2025 3:26 AM
    #
    #NOT SURE WHEN THIS METHOD BELOW SHOULD BE RUN...
    
    #this checks to see if the values for the foreign key column (self) on the containing object (fcobj)
    #is on the foreign key reference class list of objects for that class.
    #
    #note: if the database and the class lists of objects have not synced up the item might be on the
    #database, but not on the list of objects for that class.
    #
    #for validation purposes the foreign key object with data must be found on the
    #foreign class list of objects. However, if the object has not been created before this is run,
    #then it also will not be on that list.
    #
    #this method is really sensitive as to when it is run.
    def doesOrGetObjectThatHasTheForeignKeyValues(self, useget, fcobj=None):
        myvalidator.varmustbeboolean(useget, "useget");

        if (fcobj == None):
            cntxt = self.getContext();
            myvalidator.varmustnotbenull(cntxt, "cntxt or fcobj (aka the context object)");
            return self.doesOrGetObjectThatHasTheForeignKeyValues(useget, cntxt);

        #print("BEGIN FOREIGN KEY DATA VALIDATION METHOD NOW:");
        #print(f"self.isforeignkey = {self.isforeignkey}");
        #print(f"self.foreignColNames = {self.foreignColNames}");
        #print(f"self.foreignClass = {self.foreignClass}");
        #print(f"self.getColName() = {self.getColName()}");

        if (self.isforeignkey):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColNames)):
                print(self);
                raise ValueError("the foreign key needs a reference class and a column name!");
            else:
                #print("self is the column object.");
                #print("the calling object is fcobj which is the class instance that has the column!");
                #print(f"fcobj = {fcobj}");

                #check to see if the foreign key values on the column exist on the foreign key class
                
                #self is the column object
                #fcobj is the calling object that contains that column (so this is the real self).
                #foreign class is the string name of the foreign class.
                myfcoldatainfoobj = self.genForeignKeyDataObjectInfo(fcobj);
                #print(f"\nmyfcoldatainfoobj = {myfcoldatainfoobj}\n");

                myclsref = myfcoldatainfoobj["fclassref"];
                myfcols = myfcoldatainfoobj["myfcols"];
                myfccolnames = myfcoldatainfoobj["myfccolnames"];
                mycolis = myfcoldatainfoobj["mycolis"];
                mcolobjs = myfcoldatainfoobj["mcolobjs"];
                myvalidator.varmustnotbenull(fcobj, "fcobj");
                myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                #names referenced by the foreign key
                #print(f"self.foreignColNames = {self.foreignColNames}");
                #print(f"myfccolnames = {myfccolnames}");#all of the col names in the foreign class
                
                myvalidator.listMustContainUniqueValuesOnly(self.foreignColNames,
                                                            "self.foreignColNames");

                #print(f"mycolis = {mycolis}");

                #now get that column object and check to see if the isunique is set to true?
                #OR is primary key and the only primary key on that table?
                #print(f"mcolobjs = {mcolobjs}");

                #need to get the values of each column from an object from
                #the list of objects for that class
                #
                #the comparison values will come from the fcobj
                #we want the values for the foreign key columns specifically the ones pointing
                #to this foreign class.
                #
                valfcrefcol = fcobj.getValueForColName(self.getColName());
                #print(f"colname = {self.getColName()}");
                #print(f"valfcrefcol = {valfcrefcol}");
                #val is either a list or a number
                
                for mobj in myclsref.all:
                    #print(f"mobj = {mobj}");

                    clvals = [mobj.getValueForColName(mc.getColName()) for mc in mcolobjs];
                    #print(f"clvals = {clvals}");

                    ismatch = True;
                    for n in range(len(mcolobjs)):
                        mc = mcolobjs[n];
                        #print(f"colnm = {mc.getColName()}");
                        #print(f"clval = {clvals[n]}");

                        if (mc.getColName() == self.foreignColNames[n]): pass;
                        else:
                            print(f"self = {self}");
                            print(f"mc = {mc}");
                            print(f"mc.getColName() = {mc.getColName()}");
                            print(f"self.foreignColNames[{n}] = {self.foreignColNames[n]}");
                            raise ValueError("the column names must match, but they did not!");

                        ismatch = ((type(valfcrefcol) == list and (valfcrefcol[n] == clvals[n])) or
                                   ((not (type(valfcrefcol) == list)) and (valfcrefcol == clvals[n])));
                        if (ismatch): pass;
                        else:
                            #print("not a match!");
                            #ismatch = False;
                            break;
                    #print(f"ismatch = {ismatch}");
                    
                    if (ismatch): return (mobj if (useget) else True);
        return (None if (useget) else False);
    def getObjectThatHasTheForeignKeyValues(self, fcobj=None):
        return self.doesOrGetObjectThatHasTheForeignKeyValues(True, fcobj);
    def doesForeignKeyValuesExistOnObjectsList(self, fcobj=None):
        return self.doesOrGetObjectThatHasTheForeignKeyValues(False, fcobj);

    
    def foreignKeyInformationMustBeValid(self, fcobj=None, usenoclassobj=True):
        #this method takes in the calling class's object and the current column object
        #the goal of this method is to make sure that the foreign key information is valid
        #it will look at the list of cols given and make sure that they are unique (handled by set)
        #it will make sure that the referring class is valid
        #it will make sure that the referring class has those column names on it
        #it will make sure that the referring class has a valid primary key
        #it will make sure that the column names on the link from the calling object
        #are on the referring class and has the unique data enforced.
        #
        #this method only checks the columns and does not check the values used for the foreign key
        #and sees if a corresponding object exists that is the
        #doesForeignKeyValuesExistOnObjectsList(self, fcobj=None) that does that.
        #
        #we do not call that in here either, due to a timing issue as the above requires the objects to
        #actually exist in memory with the links more or less, AND the current method is actually
        #called before that had a chance to be true.

        myvalidator.varmustbeboolean(usenoclassobj, "usenoclassobj");
        if (fcobj == None):
            if (usenoclassobj): pass;
            else:
                cntxt = self.getContext();
                myvalidator.varmustnotbenull(cntxt, "cntxt or fcobj (aka the context object)");
                return self.foreignKeyInformationMustBeValid(fcobj=cntxt);
        
        #has is foreign key
        #print("\nBEGIN FOREIGN KEY VALIDATION METHOD NOW:");
        #print(f"self.isforeignkey = {self.isforeignkey}");
        #print(f"self.foreignColNames = {self.foreignColNames}");
        #print(f"self.foreignClass = {self.foreignClass}");
        
        if (self.isforeignkey):
            if (self.foreignClass == None or myvalidator.isvaremptyornull(self.foreignColNames)):
                print(f"self = {self}");
                print(f"self.foreignClass = {self.foreignClass}");
                print(f"self.foreignColNames = {self.foreignColNames}");
                raise ValueError("the foreign key needs a reference class and a column name!");
            else:
                #now make sure the column name is on the class as one
                #get the column names from the foreign class
                #once we do that we need to make sure that the column data is unique.
                #then we are sure that the information is valid.
                #self is the column object
                #fcobj is the calling object that contains that column (so this is the real self).
                #foreign class is the string name of the foreign class.
                #print("self is the column object.");
                #print("the calling object is fcobj which is the class instance that has the column!");
                #print(f"fcobj = {fcobj}");
                
                myfcoldatainfoobj = self.genForeignKeyDataObjectInfo(fcobj=fcobj,
                                                                     usenoclassobj=usenoclassobj);
                #print(f"\nmyfcoldatainfoobj = {myfcoldatainfoobj}\n");

                myclsref = myfcoldatainfoobj["fclassref"];
                myfcols = myfcoldatainfoobj["myfcols"];
                myfccolnames = myfcoldatainfoobj["myfccolnames"];
                mycolis = myfcoldatainfoobj["mycolis"];
                mcolobjs = myfcoldatainfoobj["mcolobjs"];
                if (usenoclassobj): pass;
                else: myvalidator.varmustnotbenull(fcobj, "fcobj");
                myvalidator.varmustnotbeempty(myfccolnames, "myfccolnames");
                #names referenced by the foreign key
                #print(f"self.foreignColNames = {self.foreignColNames}");
                #print(f"myfccolnames = {myfccolnames}");#all of the col names in the foreign class
                
                myvalidator.listMustContainUniqueValuesOnly(self.foreignColNames,
                                                            "self.foreignColNames");

                #print(f"mycolis = {mycolis}");

                #now get that column object and check to see if the isunique is set to true?
                #OR is primary key and the only primary key on that table?
                #print(f"mcolobjs = {mcolobjs}");

                myfcdtps = [mc.getDataType() for mc in mcolobjs];
                #for mc in mcolobjs:
                #    print(f"mc = {mc}");
                #    print(f"mc.isunique = {mc.isunique}");
                #print(f"myfcols = {myfcols}");

                pkycols = myclsref.getMyPrimaryKeyCols(myfcols);
                #print(f"len(pkycols) = {len(pkycols)}");

                #if is a multi-column foreign key, then multi-values and multiple types...
                #we need to make sure that the foreign key column data types match here
                #the data type value might be an array for multi-column data types
                #the data type might be a string for single types or an array.
                
                #print(f"self.datatype = {self.datatype}");
                #print(f"myfcdtps = {myfcdtps}");
                #print(type(myfcdtps));
                #print(type(self.datatype));

                if (1 < len(self.foreignColNames)):
                    myvalidator.varmustbethetypeonly(self.datatype, list, "self.datatype");

                    for mc in mcolobjs:
                        fndmatch = False;
                        for i in range(len(self.foreignColNames)):
                            nm = self.foreignColNames[i];
                            dtp = self.datatype[i];
                            #print(f"nm = {nm}");
                            #print(f"dtp = {dtp}");
                            #print(f"mc.getColName() = {mc.getColName()}");
                            #print(f"mc.getDataType() = {mc.getDataType()}");

                            if (nm == mc.getColName()):
                                if (dtp == mc.getDataType()):
                                    fndmatch = True;
                                    break;
                                else:
                                    print(f"mc = {mc}");
                                    print(f"self = {self}");
                                    print(f"nm = {nm}");
                                    print(f"mc.getColName() = {mc.getColName()}");
                                    print(f"dtp = {dtp}");
                                    print(f"mc.getDataType() = {mc.getDataType()}");
                                    raise ValueError("the column names were the same, but the " +
                                                     "data types did not match for the foreign key!");
                        if (fndmatch): pass;
                        else:
                            print(f"mc = {mc}");
                            print(f"self = {self}");
                            raise ValueError("one of the column names were not found for the " +
                                             "foreign key!");
                else:
                    if (self.datatype == myfcdtps[0]): pass;
                    else:
                        print(f"self = {self}");
                        print(f"mcolobjs = {mcolobjs}");
                        print(f"self.datatype = {self.datatype}");
                        print(f"myfcdtps[0] = {myfcdtps[0]}");
                        raise ValueError("the foreign key col data types must match!");

                
                if (len(pkycols) < 1):
                    raise ValueError("each table must have at least one primary key, but the class(" +
                                     myclsref.__name__ + ") did not have one at all!");
                else:
                    #if there is one column on the foreign key colnames, then if it is unique OR
                    #is the primary key, then it is valid
                    #if there is more than one column on the foreign key colnames, then
                    #-they must either match the primary key colnames OR
                    #-be inside of a UNIQUE constraint with those exact colnames no more no less.
                    #otherwise it is invalid.
                    pkycolnames = myclsref.getMyColNames(pkycols);
                    #print(f"pkycolnames = {pkycolnames}");
                    #print(f"self.foreignColNames = {self.foreignColNames}");

                    myvalidator.listMustContainUniqueValuesOnly(pkycolnames, "pkycolnames");
                    isvalid = False;
                    merrmsgpta = "the foreign key column";
                    merrmsgptb = ("" if (fcobj == None) else " on class(" + type(fcobj).__name__ + ")");
                    merrmsgptc = " must refer to unique data!";
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
                            #print(f"mrefallconstraints = {mrefallconstraints}");

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
                                        #print(f"mcolstrincond = {mcolstrincond}");
                                        
                                        tempcolsarr = mcolstrincond.split(", ");
                                        #print(f"tempcolsarr = {tempcolsarr}");

                                        if (myvalidator.areTwoListsTheSame(tempcolsarr,
                                                                           self.foreignColNames)):
                                            #print("match found so valid!");
                                            isvalid = True;
                                            break;
                    if isvalid: pass;
                    else: raise ValueError(merrmsgpta + merrmsgptb + merrmsgptc);
        else:
            if (self.foreignClass == None): pass;
            else: self.setForeignClass(None);
            if (myvalidator.isvaremptyornull(self.foreignColNames)): pass;
            else: self.setForeignColNames(None);
        #print("DONE WITH FOREIGN KEY VALIDATION METHOD NOW!");
        return True;

    #can call in init
    def newForeignKey(self, fkycls, fkycolnm):#, fcobj
        #print(f"self = {self}");
        #print(f"fkycls = {fkycls}");
        #print(f"fkycolnm = {fkycolnm}");
        self.setForeignClass(fkycls);
        self.setForeignColNames(fkycolnm);#, fcobj
        self.setIsForeignKey(True);

    def __repr__(self):
        mystr = f"<MyCol {self.colname} type: {self._datatype}";#" value: {self._value}"
        mystr += f" default: {self._defaultvalue} isprimarykey: {self.isprimarykey}";
        mystr += f" isnonnull: {self.isnonnull} isunique: {self.isunique} issigned: {self.issigned}";
        mystr += f" containingclassname: {self.containingclassname}";
        mystr += f" autoincrements: {self.autoincrements} isforeignkey: {self.isforeignkey}";
        mystr += f" foreignClass: {self.foreignClass} foreignColNames: {self.foreignColNames}";
        mystr += f" foreignobjectname: {self.foreignobjectname} constraints: {self.constraints}";
        mystr += " /MyCol>";
        return mystr;
