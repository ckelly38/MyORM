from mybase import MyBaseClass;
from mybase import mycol;
class MyTestColsClass(MyBaseClass):
    #def __init__(self):
        #print("INSIDE OF CONSTRUCTOR ON TEST CLASS A!");
        #self.mynewcol.newForeignKey(MyOtherTestClass, "mynewcol", self);
        #self.mynewcol.newForeignKey(MyOtherTestClass, "mynewcol", self);

    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    #from testfile import MyOtherTestClass;
    myfkeyid = mycol(colname="myfkeyid", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyOtherTestClass", foreignColName="mynewcol",
                    constraints=None);
    myothervar = 2;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

class MyOtherTestClass(MyBaseClass):
    def __init__(self):
        print("INSIDE OF CONSTRUCTOR ON TEST CLASS B!");
        #self.mynewcol.newForeignKey(MyTestColsClass, "mynewcol", self);
        #self.mynewcol.newForeignKey(MyTestColsClass, "mynewcol", self);
        #self.mynewcol.setMyForeignKeyClassRef(MyTestColsClass);

    mynewcol = mycol(colname="mynewcol", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=True, isnonnull=True,
                    isunique=True, autoincrements=True, constraints=None);
    myfkeyid = mycol(colname="myfkeyid", datatype="Integer", value=None,
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyTestColsClass", foreignColName="mynewcol",
                    constraints=None);
    myothervar = 2;
    #__mytablename__ = "testtable";
    mytablename = "testtable";
