from mybase import mybase;
from mybase import mycol;
#MAY NEED TO CHANGE FOREIGN KEYS 2-18-2025
class MyTestColsClass(mybase):
    def __init__(self):
        print("INSIDE OF CONSTRUCTOR ON TEST CLASS A!");
        #self.mynewcol.newForeignKey(MyOtherTestClass, ["mynewcol"]);#, self
        #self.mynewcol.newForeignKey(MyOtherTestClass, ["mynewcol"]);#, self
        super().__init__();

    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    #from testfile import MyOtherTestClass;
    myfkeyid = mycol(colname="myfkeyid", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyOtherTestClass", foreignColNames=["mynewcol"],
                    constraints=None);
    myothervar = 2;
    mymulticolargs = None;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

class MyOtherTestClass(mybase):
    def __init__(self):
        print("INSIDE OF CONSTRUCTOR ON TEST CLASS B!");
        #self.mynewcol.newForeignKey(MyTestColsClass, ["mynewcol"]);#, self
        #self.mynewcol.newForeignKey(MyTestColsClass, ["mynewcol"]);#, self
        #self.mynewcol.setMyForeignKeyClassRef(MyTestColsClass);
        super().__init__();

    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    myfkeyid = mycol(colname="myfkeyid", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyTestColsClass", foreignColNames=["mynewcol"],
                    constraints=None);
    mymulticolargs = None;
    myothervar = 2;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

class MyModelWithCompPrimaryKey(mybase):
    #bug in is primary key: the primary key must be unique and non-null
    #a composite primary key can be null, but not likely.
    #also need some column for multi-column-constraints...
    #probably need a way to get all of the constraints for a table too.
    #need to verify that the colname saved in the col object and the attribute name for it must match

    mynewcola = mycol(colname="mynewcola", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    mynewcolb = mycol(colname="mynewcolb", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    mynewcolc = mycol(colname="mynewcolc", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=False, autoincrements=True, constraints=None);
    mymulticolargs = None;
    mytablename = "comppkeytable";

class MyModelWithCompForeignKey(mybase):
    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    mycompfkcolval = mycol(colname="mycompfkcolval", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyModelWithCompPrimaryKey",
                    foreignColNames=["mynewcola", "mynewcolb", "mynewcolc"],
                    constraints=None);
    mymulticolargs = None;
    mytablename = "compfkeytesttable";
