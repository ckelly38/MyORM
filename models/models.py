from mybase import mybase;
from mybase import mycol;
from mycol import myvalidator;
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
    myuvalpkytst = False;
    mynewcola = mycol(colname="mynewcola", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=myuvalpkytst, autoincrements=True, constraints=None);
    mynewcolb = mycol(colname="mynewcolb", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=myuvalpkytst, autoincrements=False, constraints=None);
    mynewcolc = mycol(colname="mynewcolc", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=False, autoincrements=False, constraints=None);
    mymulticolargs = [myvalidator.genUniqueConstraint("mytableuniquecolsconstraint",
                                                      ["mynewcola", "mynewcolb"])];#, "mynewcolc"
    tableargs = None;
    mytablename = "comppkeytable";

class MyModelWithCompForeignKey(mybase):
    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    mycompfkcolval = mycol(colname="mycompfkcolval", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyModelWithCompPrimaryKey",
                    foreignColNames=["mynewcola", "mynewcolb"],
                    constraints=None);#, "mynewcolc"
    mymulticolargs = None;
    mytablename = "compfkeytesttable";
