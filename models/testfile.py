from init import CURSOR, CONN;
from mycol import mycol;

class MyBaseClass:
    #mytablename = "basetablename";

    #it needs an object and its class
    def getMyCols(self):
        return [getattr(self, attr) for attr in dir(type(self))
                if (not attr.startswith("_") and (type(getattr(self, attr)) == mycol))];

    def getTableName(self):
        ptablenames = ["mytablename", "tablename", "table_name", "my_table_name"];
        for attr in dir(type(self)):
            for pnm in ptablenames:
                if (pnm in attr): return getattr(self, attr);
        raise AttributeError("the table must have a tablename in it!");

class MyTestColsClass(MyBaseClass):
    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None, defaultvalue=None,
                    isprimarykey=True, isforeignkey=False, isnonnull=True, isunique=True,
                    autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
    myothervar = 2;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

class MyOtherTestClass(MyBaseClass):
    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None, defaultvalue=None,
                    isprimarykey=True, isforeignkey=False, isnonnull=True, isunique=True,
                    autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
    myothervar = 2;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

#print(mynewcol);
tstobj = MyTestColsClass();
print(tstobj.getMyCols());
print(tstobj.getTableName());
#print(tstobj.mynewcol.value);#error for the moment on this line not done with type enforcement...

tstobjb = MyOtherTestClass();
print(tstobjb.getMyCols());
print(tstobjb.getTableName());

#we can have more than one database open at the same time
#but if the base class has a static list of all of them, then
#some on a different database would share the same names which would be legal as long as
#the same names are not on the same database

#myonewcol = mycol(colname="myonewcol", datatype="Integer", value=1, defaultvalue=0,
#                 isprimarykey=True, isforeignkey=False, isnonnull=False, isunique=False,
#                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
#errors out
#print(myonewcol);

#mybnewcol = mycol(colname="mybnewcol", datatype="Integer", value=1, defaultvalue=0,
#                 isprimarykey=True, isforeignkey=False, isnonnull=True, isunique=True,
#                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
#print(mybnewcol);