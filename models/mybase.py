from mycol import mycol;
from mycol import myvalidator;
from init import SQLVARIANT;
class mybase:
    #mytablename = "basetablename";
    #mymulticolargs = None;
    disableconstraintswarning = False;

    def __init__(self, colnames=None, colvalues=None):
        print("INSIDE BASE CLASS CONSTRUCTOR!");
        print(f"type(self) = {type(self)}");
        print(f"mytablename = {type(self).getTableName()}");
        
        if (type(self).isVarPresentOnTableMain("multi_column_constraints_list")): pass;
        else: setattr(type(self), "mymulticolargs", None);
        print(f"multicolconstraints = {type(self).getMultiColumnConstraints()}");
        
        mtargs = type(self).getAllTableConstraints();
        if (type(self).isVarPresentOnTableMain("allconstraints_list")): pass;
        else: setattr(type(self), "tableargs", ([] if (mtargs == None) else mtargs));
        print(f"tableargs = {mtargs}");
        print(f"colnames = {colnames}");
        print(f"colvalues = {colvalues}");
        
        mytempcols = type(self).getMyCols();
        mycolnames = type(self).getMyColNames(mytempcols);
        mycolattrnames = type(self).getMyColAttributeNames();
        print(f"mycolnames = {mycolnames}");
        print(f"mycolattrnames = {mycolattrnames}");

        myvalidator.listMustContainUniqueValuesOnly(mycolnames, "mycolnames");
        myvalidator.listMustContainUniqueValuesOnly(mycolattrnames, "mycolattrnames");
        if (myvalidator.areTwoListsTheSame(mycolnames, mycolattrnames)): pass;
        else: raise ValueError("THE COLUMN ATTRIBUTE NAMES MUST MATCH THE SET COLNAME GIVEN!");
    
        if (type(self).areColsWithIndividualConstraintsValid(mytempcols)): pass;
        else:
            raise ValueError("there exists one column on the class (" + type(self).__name__ +
                             ") that does not have a valid constraint!");

        #the constructor essentially begins here...

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
        print(f"varstr = SQLVARIANT = {varstr}");

        for mc in mytempcols:
            mc.primaryKeyInformationMustBeValid(type(self));
            mc.foreignKeyInformationMustBeValid(self);

        #for each column need to make sure that there is a value if not use the default value
        #how to know which value is for what col?
        #base constructor will take in two parameters, one col names, and one values
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
        
        #do the same for the colnames not in that list
        ocolnms = [mclnm for mclnm in mycolnames
                   if myvalidator.isvaremptyornull(colnames) or mclnm not in colnames];
        print(f"mycolnames = {mycolnames}");
        print(f"colnames = {colnames}");
        print(f"ocolnms = {ocolnms}");
        
        for clnm in ocolnms:
            #the value is the default value for the type for the varaint
            #get the type object for that type for the variant
            mycolobj = mytempcols[mycolnames.index(clnm)];
            fldtnm = mycolobj.getDataType();
            tpobj = myvalidator.getDataTypeObjectWithNameOnVariant(fldtnm, varstr);
            print(f"tpobj = {tpobj}");
            print(f"fldtnm = {fldtnm}");
            
            mykynm = myvalidator.getDefaultValueKeyNameForDataTypeObj(tpobj, mycolobj);
            print(f"mykynm = {mykynm}");

            valcl = myvalidator.getDefaultValueForDataTypeObjWithName(tpobj, mykynm, False);
            print(f"clnm = {clnm}");
            print(f"valcl = {valcl}");

            self.setValueForColName(clnm, valcl, mycolobj);
        
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

    def runGivenValidatorsForClass(self, mvs):
        from mycol import mycol;
        return mycol.runGivenValidatorsForClass(type(self).__name__, self, mvs);

    def runValidatorsByKeysForClass(self, mkys):
        from mycol import mycol;
        return mycol.runValidatorsByKeysForClass(type(self).__name__, self, mkys);

    def runAllValidatorsForClass(self):
        from mycol import mycol;
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
                    #myvalidator.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
                else: return self.setValueForColName(clnm, valcl[0], mycolobj);
            else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);
        else:
            if (myvalidator.isValueValidForDataType(mvaldtp, valcl, varstr, not(mycolobj.getIsSigned()),
                                                    mycolobj.getIsNonNull())):
                print("setting the column to the value here!");
                setattr(self, clnm + "_value", valcl);
                self.runValidatorsByKeysForClass([clnm]);
                #myvalidator.runValidatorsByKeysForClass(type(self).__name__, self, [clnm]);
            else: raise ValueError(errmsgpta + str(valcl) + errptbwithdata + errmsgptc);

    def printValuesForAllCols(self, mycols=None):
        fincols = type(self).getMyColsFromClassOrParam(mycols);
        for mc in self.getMyColNames(fincols):
            print(f"val for colname {mc} is: {self.getValueForColName(mc)}");

    def getKnownAttributeNamesForSerialization(self):
        return [nm for nm in type(self).getKnownAttributeNamesOnTheClass()];

    def __repr__(self):
        mstr = "<" + self.__class__.__name__ + " ";
        nmscls = self.getKnownAttributeNamesForSerialization();
        #print(nmscls);
        
        handleallsame = False;
        for n in range(len(nmscls)):
            attr = nmscls[n];
            if (hasattr(self, attr)):
                if (attr == "all"):
                    if (handleallsame): mstr += attr + ": " + str(getattr(self, attr));
                    else: mstr += "all: [list of all instances of the class]";
                else: mstr += attr + ": " + str(getattr(self, attr));
                if (n + 1 < len(nmscls)): mstr += ", ";
        mstr += " /" + self.__class__.__name__ + ">";
        #print(dir(type(self)));
        #mlist = [{"key": attr, "value": getattr(self, attr)} for attr in dir(type(self))
        #         if not callable(getattr(self, attr) and attr not in
        #                         ["all", "__dict__", "__doc__", "__module__", "__weakref__"])];
        #print(mlist);
        #print(mstr);
        #raise ValueError("NOT DONE YET!");
        return mstr;

    #class methods of the base class, but not constructors.

    @classmethod
    def getMyColsOrMyColAttributeNames(cls, usemycols):
        #print(f"cls = {cls}");
        myvalidator.varmustbeboolean(usemycols, "usemycols");
        return [(getattr(cls, attr) if usemycols else attr)
                for attr in dir(cls) if (type(getattr(cls, attr)) == mycol)];
    @classmethod
    def getMyCols(cls): return cls.getMyColsOrMyColAttributeNames(True);
    @classmethod
    def getMyColAttributeNames(cls): return cls.getMyColsOrMyColAttributeNames(False);

    @classmethod
    def getMyColsFromClassOrParam(cls, mycols=None):
        return (cls.getMyCols() if myvalidator.isvaremptyornull(mycols) else mycols);

    @classmethod
    def getMyColNames(cls, mycols=None):
        return [mclobj.colname for mclobj in cls.getMyColsFromClassOrParam(mycols)];
    
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
    def areColsWithIndividualConstraintsValid(cls, mycols=None):
        for mc in cls.getColumnsWithConstraints(mycols):
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
    def getPossibleTableNames(cls):
        return ["mytablename", "tablename", "table_name", "my_table_name"];

    @classmethod
    def getMultiColumnConstraintVariableNames(cls):
        return ["mymulticolumnconstraints", "mymulticolconstraints", "mcolconstraints",
                "mymulticolumnarguments", "mymulticolarguments", "mcolarguments", "mymulticolumnargs",
                "mymulticolargs", "mcolargs", "my_multi_column_constraints", "my_multicol_constraints",
                "mcol_constraints", "my_multi_column_arguments", "my_multicol_arguments",
                "my_multi_col_arguments", "mcol_arguments", "my_multi_column_args", "my_multicol_args",
                "mcol_args", "my_multi_col_args", "my_multi_col_constraints"];

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
    def getOtherKnownSafeAttributesOnTheClass(cls):
        return [attr for attr in dir(cls)
                if (type(getattr(cls, attr)) in [int, float, str, list, tuple] and
                    attr not in ["__module__", "all"])];
        #mycol could be on the list of stuff to serialize,
        #but there is already a method specifically for that

    @classmethod
    def getKnownAttributeNamesOnTheClass(cls):
        mlist = [item for item in cls.getOtherKnownSafeAttributesOnTheClass()];
        for nm in cls.getMyColAttributeNames():
            mlist.append(nm);
            mlist.append(nm + "_value");
        tnmattrnm = cls.getNameOfVarIfPresentOnTableMain("tablename");
        mcsattrnm = cls.getNameOfVarIfPresentOnTableMain("multi_column_constraints_list");
        acsattrnm = cls.getNameOfVarIfPresentOnTableMain("allconstraints_list");
        if (tnmattrnm not in mlist): mlist.append(tnmattrnm);
        if (mcsattrnm not in mlist): mlist.append(mcsattrnm);
        if (acsattrnm not in mlist): mlist.append(acsattrnm);
        if ("all" not in mlist): mlist.append("all");
        return mlist;

    @classmethod
    def getAllTableConstraints(cls):
        #will have all of the multi-column constraints args list on it
        #plus all of the individual col arguments or constraints on it
        if (cls.isVarPresentOnTableMain("allconstraints_list")):
            valofall = cls.getValueOfVarIfPresentOnTableMain("allconstraints_list");
            if (myvalidator.isvaremptyornull(valofall)): pass;
            else:
                if (cls.disableconstraintswarning): pass;
                else:
                    allattrp = cls.getNameOfVarIfPresentOnTableMain("allconstraints_list");
                    print("");
                    print("WARNING: you provided a " + allattrp + " attribute in the class (" +
                        cls.__name__ + "), the list you provided will be used and not the " +
                        "generated one! If this is not the desired behavior, please remove it! " +
                        "This warning can safely be ignored!");
                    print("");
                    return valofall;

        mclconstraints = cls.getMultiColumnConstraints();
        myiclconstraints = cls.getIndividualColumnConstraints();
        nwlist = myvalidator.combineTwoLists(myiclconstraints, mclconstraints);
        print(f"cls.__name__ = {cls.__name__}");
        print(f"mclconstraints = {mclconstraints}");
        print(f"myiclconstraints = {myiclconstraints}");
        print(f"nwlist = {nwlist}");

        #setattr(cls, "tableargs", ([] if (nwlist == None) else nwlist));
        return nwlist;
