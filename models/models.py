from mybase import mybase;
from mybase import mycol;
from mycol import myvalidator;
class MyTestColsClass(mybase):
    #def __init__(self):
        #print("INSIDE OF CONSTRUCTOR ON TEST CLASS A!");
        #self.mynewcol.newForeignKey(MyOtherTestClass, ["mynewcol"]);#, self
        #self.mynewcol.newForeignKey(MyOtherTestClass, ["mynewcol"]);#, self
        #super().__init__();

    mynewcol = mycol(colname="mynewcol", datatype="Integer",
                    defaultvalue=1, isprimarykey=True, isnonnull=True, issigned=False,
                    isunique=True, autoincrements=True, constraints=None);# value=None,
    #from testfile import MyOtherTestClass;
    myfkeyid = mycol(colname="myfkeyid", datatype="Integer",
                    defaultvalue=None, isprimarykey=False, isnonnull=True, issigned=False,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyOtherTestClass", foreignColNames=["mynewcol"],
                    constraints=None);# value=None,
    myothervar = 2;
    mymulticolargs = None;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

class MyOtherTestClass(mybase):
    #def __init__(self):
        #print("INSIDE OF CONSTRUCTOR ON TEST CLASS B!");
        #self.mynewcol.newForeignKey(MyTestColsClass, ["mynewcol"]);#, self
        #self.mynewcol.newForeignKey(MyTestColsClass, ["mynewcol"]);#, self
        #self.mynewcol.setMyForeignKeyClassRef(MyTestColsClass);
        #super().__init__();

    mynewcol = mycol(colname="mynewcol", datatype="Integer",
                    defaultvalue=1, isprimarykey=True, isnonnull=True, issigned=False,
                    isunique=True, autoincrements=True, constraints=None);# value=None,
    myfkeyid = mycol(colname="myfkeyid", datatype="Integer",
                    defaultvalue=None, isprimarykey=False, isnonnull=True, issigned=False,
                    isunique=True, autoincrements=False,
                    isforeignkey=True, foreignClass="MyTestColsClass", foreignColNames=["mynewcol"],
                    constraints=None);# value=None,
    mymulticolargs = None;
    myothervar = 2;
    #__mytablename__ = "testtable";
    mytablename = "testtable";

class MyModelWithCompPrimaryKey(mybase):
    #bug with the current setup and storage requirements adjusted. found on 2-24-2025 10 PM
    #
    #some of these col data requirements are constant: like where the foreign keys point to, the
    #datatype of the value stored in it, is it a primary key, etc.
    #a default value can be stored in the mycol class, but not the actual value.
    #but the value of said column must be stored elsewhere because that is object specific.
    #but some of these change with each object: like the value stored in it.
    #the ones that change with each object need to be stored in an object and not in the mycol object
    #either that or the mycol has a list of values for each object that is somehow mapped to the object
    #which is not easy to do. SQLAlchemy makes this easy for some strange reason probably because it
    #has all of these "class attributes" run inside of the init().
    myuvalpkytst = False;
    mynewcola = mycol(colname="mynewcola", datatype="Integer",
                    defaultvalue=1, isprimarykey=True, isnonnull=True, issigned=False,
                    isunique=myuvalpkytst, autoincrements=True, constraints=None);#, value=None
    mynewcolb = mycol(colname="mynewcolb", datatype="Integer",
                    defaultvalue=1, isprimarykey=True, isnonnull=True, issigned=False,
                    isunique=myuvalpkytst, autoincrements=False, constraints=None);#value=None,
    mynewcolc = mycol(colname="mynewcolc", datatype="Integer",
                    defaultvalue=1, isprimarykey=False, isnonnull=True, issigned=False,
                    isunique=False, autoincrements=False, constraints=None);#value=None,
    mymulticolargs = [myvalidator.genUniqueConstraint("mytableuniquecolsconstraint",
                                                      ["mynewcola", "mynewcolb"])];#, "mynewcolc"
    tableargs = None;
    mytablename = "comppkeytable";

    def getKnownAttributeNamesForSerialization(self):
        reslist = ["myuvalpkytst"];
        mlist = super().getKnownAttributeNamesForSerialization();
        for item in mlist: reslist.append(item);
        return reslist;


class MyModelWithCompForeignKey(mybase):
    #foreign key bug found on 3-29-2025 3:26 AM:
    #the data type for a composite foreign key is probably not just one type.

    #also a primary key does not just assign the value...
    #it may increment if auto-increment on an integer is true
    mynewcol = mycol(colname="mynewcol", datatype="Integer",
                    defaultvalue=1, isprimarykey=True, isnonnull=True, issigned=False,
                    isunique=True, autoincrements=True, constraints=None);#value=None,
    mycompfkcolval = mycol(colname="mycompfkcolval", datatype=["Integer", "Integer"],
                    defaultvalue=None, isprimarykey=False, isnonnull=True,
                    isunique=True, autoincrements=False, issigned=False,
                    isforeignkey=True, foreignClass="MyModelWithCompPrimaryKey",
                    foreignColNames=["mynewcola", "mynewcolb"],
                    constraints=None);#, "mynewcolc"#, value=None,
    mymulticolargs = None;
    mytablename = "compfkeytesttable";
