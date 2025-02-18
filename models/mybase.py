from mycol import mycol;
from mycol import myvalidator;
class mybase:
    #mytablename = "basetablename";

    def __init__(self):
        print("INSIDE BASE CLASS CONSTRUCTOR!");
        print(f"self = {self}");
        print(f"mytablename = {self.getTableName()}");
        
        mytempcols = self.getMyCols();
        mycolnames = self.getMyColNames(mytempcols);
        print(f"mycolnames = {mycolnames}");

        #for each column if it is a foreign key, now need to evaluate the class string
        #but need and the link col name
        #over here call the validation method for the new foreign key...
        #colname is already set we need to validate it.
        #we also need the class reference for validation purposes.
        #USING GLOBALS DOES NOT WORK IN THIS CASE SO CANNOT DO STRING TO REF CONVERSION.

        for mc in mytempcols:
            mc.foreignKeyInformationMustBeValid(self);
        
        myvalidator.listMustContainUniqueValuesOnly(mycolnames, "mycolnames");

    #it needs an object and its class
    def getMyCols(self):
        #print(f"self = {self}");
        return [getattr(self, attr) for attr in dir(type(self))
                if (not attr.startswith("_") and (type(getattr(self, attr)) == mycol))];

    def getMyColNames(self, mycols=None):
        finmycols = (self.getMyCols() if myvalidator.isvaremptyornull(mycols) else mycols);
        return [mclobj.colname for mclobj in finmycols];

    def getMyPrimaryKeyCols(self, mycols=None):
        finmycols = (self.getMyCols() if myvalidator.isvaremptyornull(mycols) else mycols);
        return [mclobj for mclobj in finmycols if mclobj.isprimarykey];

    def getTableName(self):
        ptablenames = ["mytablename", "tablename", "table_name", "my_table_name"];
        for attr in dir(type(self)):
            for pnm in ptablenames:
                if (pnm in attr): return getattr(self, attr);
        raise AttributeError("the table must have a tablename in it!");
