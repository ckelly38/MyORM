from mycol import mycol;
from mycol import myvalidator;
from init import SQLVARIANT;
class mybase:
    #mytablename = "basetablename";
    #mymulticolargs = None;
    disableconstraintswarning = False;

    def __init__(self, colnames=None, colvalues=None):
        print("INSIDE BASE CLASS CONSTRUCTOR!");
        print(f"self = {self}");
        print(f"mytablename = {self.getTableName()}");
        print(f"multicolconstraints = {self.getMultiColumnConstraints()}");
        print(f"tableargs = {self.getAllTableConstraints()}");
        print(f"colnames = {colnames}");
        print(f"colvalues = {colvalues}");
        
        mytempcols = self.getMyCols();
        mycolnames = self.getMyColNames(mytempcols);
        mycolattrnames = self.getMyColAttributeNames();
        varstr = "" + SQLVARIANT;
        print(f"mycolnames = {mycolnames}");
        print(f"mycolattrnames = {mycolattrnames}");
        print(f"varstr = SQLVARIANT = {varstr}");

        myvalidator.listMustContainUniqueValuesOnly(mycolnames, "mycolnames");
        myvalidator.listMustContainUniqueValuesOnly(mycolattrnames, "mycolattrnames");
        if (myvalidator.areTwoListsTheSame(mycolnames, mycolattrnames)): pass;
        else: raise ValueError("THE COLUMN ATTRIBUTE NAMES MUST MATCH THE SET COLNAME GIVEN!");

        #for each column if it is a foreign key, now need to evaluate the class string
        #but need and the link col name
        #over here call the validation method for the new foreign key...
        #colname is already set we need to validate it.
        #we also need the class reference for validation purposes.
        #USING GLOBALS DOES NOT WORK IN THIS CASE SO CANNOT DO STRING TO REF CONVERSION.

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
        print("DONE WITH THE BASE CONSTRUCTOR!");
    
    def getValueForColName(self, clnm):
        myvalidator.stringMustHaveAtMinNumChars(clnm, 1, "clnm");
        return getattr(self, clnm + "_value");

    def setValueForColName(self, clnm, valcl, mycolobj):
        varstr = "" + SQLVARIANT;
        myvalidator.stringMustHaveAtMinNumChars(clnm, 1, "clnm");
        myvalidator.varmustnotbenull(mycolobj, "mycolobj");
        if (myvalidator.isValueValidForDataType(mycolobj.getDataType(), valcl, varstr,
                                                not(mycolobj.getIsSigned()), mycolobj.getIsNonNull())):
             print("setting the column to the value here!");
             setattr(self, clnm + "_value", valcl);
        else:
            raise ValueError("invalid value (" + str(valcl) + ") used here for the data type (" +
                             mycolobj.getDataType() + ") for the variant (" + varstr + ")!");

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
    def areGivenColNamesOnTable(cls, mlist, mycols=None):
        if (myvalidator.isvaremptyornull(mlist)): return False;
        fincolnms = cls.getMyColNames(cls.getMyColsFromClassOrParam(mycols));
        for mitem in mlist:
            if (mitem in fincolnms): pass;
            else: return False;
        return True;

    @classmethod
    def getMyPrimaryKeyCols(cls, mycols=None):
        return [mclobj for mclobj in cls.getMyColsFromClassOrParam(mycols) if mclobj.isprimarykey];
    
    @classmethod
    def getIndividualColumnConstraints(cls, mycols=None):
        return [mc.constraints for mc in cls.getMyColsFromClassOrParam(mycols)
                if not myvalidator.isvaremptyornull(mc.constraints)];
    
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
                if (pnm in attr):
                    return {"value": getattr(cls, attr), "name": attr};
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

        return nwlist;
