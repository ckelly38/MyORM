from mycol import mycol;
from mycol import myvalidator;
class mybase:
    #mytablename = "basetablename";
    mymulticolargs = None;

    def __init__(self):
        print("INSIDE BASE CLASS CONSTRUCTOR!");
        print(f"self = {self}");
        print(f"mytablename = {self.getTableName()}");
        print(f"multicolconstraints = {self.getMultiColumnConstraints()}");
        #print(f"tableargs = {self.getAllTableConstraints()}");#NOT DONE YET...
        
        mytempcols = self.getMyCols();
        mycolnames = self.getMyColNames(mytempcols);
        print(f"mycolnames = {mycolnames}");

        myvalidator.listMustContainUniqueValuesOnly(mycolnames, "mycolnames");

        #for each column if it is a foreign key, now need to evaluate the class string
        #but need and the link col name
        #over here call the validation method for the new foreign key...
        #colname is already set we need to validate it.
        #we also need the class reference for validation purposes.
        #USING GLOBALS DOES NOT WORK IN THIS CASE SO CANNOT DO STRING TO REF CONVERSION.

        for mc in mytempcols:
            mc.foreignKeyInformationMustBeValid(self);

        #do something here...
        print("DONE WITH THE BASE CONSTRUCTOR!");

    @classmethod
    def getMyCols(cls):
        #print(f"cls = {cls}");
        return [getattr(cls, attr) for attr in dir(cls) if (type(getattr(cls, attr)) == mycol)];

    @classmethod
    def getMyColNames(cls, mycols=None):
        finmycols = (cls.getMyCols() if myvalidator.isvaremptyornull(mycols) else mycols);
        return [mclobj.colname for mclobj in finmycols];

    @classmethod
    def getMyPrimaryKeyCols(cls, mycols=None):
        finmycols = (cls.getMyCols() if myvalidator.isvaremptyornull(mycols) else mycols);
        return [mclobj for mclobj in finmycols if mclobj.isprimarykey];
    
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
    def varMustBePresentOnTable(cls, ilist=None, varnm="varnm"):
        if (myvalidator.isvaremptyornull(ilist)):
            mylist = cls.getListOfPossibleNamesForVariable(varnm);
        else: mylist = ilist;
        for attr in dir(cls):
            for pnm in mylist:
                if (pnm in attr): return getattr(cls, attr);
        raise AttributeError("the table must have a(n) " + varnm + " in it!");
    @classmethod
    def varMustBePresentOnTableMain(cls, varnm="varnm"):
        return cls.varMustBePresentOnTable(None, varnm);
    @classmethod
    def getTableName(cls): return cls.varMustBePresentOnTableMain("tablename");
    @classmethod
    def getMultiColumnConstraints(cls):
        return cls.varMustBePresentOnTableMain("multi_column_constraints_list");
    
    #NOT DONE YET...2-19-2025!
    @classmethod
    def getAllTableConstraints(cls):
        #will have all of the multi-column constraints args list on it
        #plus all of the individual col arguments or constraints on it
        mclconstraints = cls.getMultiColumnConstraints();
        myiclconstraints = [mc.constraints for mc in cls.getMyCols()
                            if not myvalidator.isvaremptyornull(mc.constraints)];
        print(f"cls.__name__ = {cls.__name__}");
        print(f"mclconstraints = {mclconstraints}");
        print(f"myiclconstraints = {myiclconstraints}");
        
        #if (myvalidator.isvaremptyornull(myiclconstraints)):
        #    return (None if myvalidator.isvaremptyornull(mclconstraints) else mclconstraints);
        #else:
            #if (myvalidator.isvaremptyornull(mclconstraints)): return myiclconstraints;
            #else:
                #combine both of the lists...
                #pass;
        return cls.varMustBePresentOnTableMain("allconstraints_list");
