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

#mycol.getMyClassRefsMain(True);

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

#mycol.getMyClassRefsMain(True);

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

    #note the user can override this method here and the string representation
    #will use this list instead
    #def getKnownAttributeNamesForSerialization(self):
    #    reslist = ["myuvalpkytst"];
    #    mlist = super().getKnownAttributeNamesForSerialization();
    #    for item in mlist: reslist.append(item);
    #    return reslist;

#mycol.getMyClassRefsMain(True);

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

#mycol.getMyClassRefsMain(True);

class Activity(mybase):
    __tablename__ = 'activities'

    #id = db.Column(db.Integer, primary_key=True);
    #name = db.Column(db.String);
    #difficulty = db.Column(db.Integer);
    id = mycol(colname="id", datatype="Integer", defaultvalue=1, isprimarykey=True, isnonnull=True,
               issigned=False, isunique=True, autoincrements=True, constraints=None);
    name = mycol(colname="name", datatype="Text", defaultvalue=None, isprimarykey=False,
                 isnonnull=True, issigned=False, isunique=True, autoincrements=False, constraints=None);
    difficulty = mycol(colname="difficulty", datatype="Integer", defaultvalue=1, isprimarykey=False,
                       isnonnull=True, issigned=False, isunique=False, autoincrements=False,
                       constraints=None);

    # Add relationship
    #signups = db.relationship("Signup", back_populates="activity", cascade="all, delete-orphan");
    #?
    
    # Add serialization rules
    #serialize_rules = ("-signups",);
    #serialize_rules = ("-signups.activity",);#copied from old code what we used
    
    def __repr__(self):
        return f'<Activity {self.id_value}: {self.name_value}>';

#mycol.getMyClassRefsMain(True);

class Camper(mybase):
    __tablename__ = 'campers';

    #validations and constraints bug problem 4-3-2025 4 AM MST:
    #
    #most of the constraints use the table name to look up the class
    #the problem is the class does not exist yet, so the look up errors out
    #we can do so without verification that it is on the table name.
    #if we could get the init to run, then the class would be defined.
    #then we could assign all of these.
    #but I want it assigned before an object is created if possible.
    #if there was only one way to verify that the column name given to a constraint was on the table
    #we could do that after the classes are defined...
    #some methods assume that the calling class is the class that has the table name...
    #we already have a method that checks to see if a column name is on a table.
    #but that is the method we cannot call without the class being defined.


    #id = db.Column(db.Integer, primary_key=True);
    #name = db.Column(db.String, nullable=False);
    #age = db.Column(db.Integer);
    id = mycol(colname="id", datatype="Integer", defaultvalue=1, isprimarykey=True, isnonnull=True,
               issigned=False, isunique=True, autoincrements=True, constraints=None);
    name = mycol(colname="name", datatype="Text", defaultvalue=None, isprimarykey=False,
                 isnonnull=True, issigned=False, isunique=True, autoincrements=False,
                 constraints=[myvalidator.genCheckConstraint("namelencheck",
                                                             myvalidator.genLengthCol("name",
                                                                                      __tablename__) +
                                                                                      " >= 1")]);
    age = mycol(colname="age", datatype="Integer", defaultvalue=1, isprimarykey=False, isnonnull=True,
                issigned=False, isunique=False, autoincrements=False,
                constraints=[myvalidator.genCheckConstraint("agecheck", "age >= 8 AND age <= 18")]);

    # Add relationship
    #signups = db.relationship("Signup", back_populates="camper", cascade="all, delete-orphan");
    #?
    
    # Add serialization rules
    #serialize_rules = ("-signups",);
    #serialize_rules = ("-signups.camper",);#copied from old code what we used
    
    # Add validation
    #@validates("name")
    #def isvalidname(self, key, val):
    #    nmvld = mv.strValHasAtMinXChars(val, 1);
    #    if (nmvld): return val;
    #    else: raise ValueError("the camper must have a name!");

    #@validates("age")
    #def isvalidage(self, key, val):
    #    return mv.intValIsAtMinXAndAtMaxY(val, 8, 18, "age");
    
    
    def __repr__(self):
        return f'<Camper {self.id_value}: {self.name_value}>';

#mycol.getMyClassRefsMain(True);

class Signup(mybase):
    __tablename__ = 'signups';

    #id = db.Column(db.Integer, primary_key=True);
    #time = db.Column(db.Integer);
    id = mycol(colname="id", datatype="Integer", defaultvalue=1, isprimarykey=True, isnonnull=True,
               issigned=False, isunique=True, autoincrements=True, constraints=None);
    time = mycol(colname="time", datatype="Integer", defaultvalue=0, isprimarykey=False, isnonnull=True,
                issigned=False, isunique=False, autoincrements=False,
                constraints=[myvalidator.genCheckConstraint("timecheck", "time >= 0 AND age <= 23")]);

    # Add relationships
    #camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"));
    #activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"));
    camper_id = mycol(colname="camper_id", datatype="Integer", defaultvalue=None, isprimarykey=False,
                      isnonnull=True, isunique=True, autoincrements=False, issigned=False,
                      isforeignkey=True, foreignClass="Camper", foreignColNames=["id"],
                      constraints=None);
    activity_id = mycol(colname="activity_id", datatype="Integer", defaultvalue=None, isprimarykey=False,
                        isnonnull=True, isunique=True, autoincrements=False, issigned=False,
                        isforeignkey=True, foreignClass="Activity", foreignColNames=["id"],
                        constraints=None);

    #camper = db.relationship("Camper", back_populates="signups");
    #activity = db.relationship("Activity", back_populates="signups");
    #?
    #?
    
    # Add serialization rules
    #serialize_rules = ("-camper", "-activity");
    #serialize_rules = ("-campers.signups", "-activity.signups");#copied from old code what we used
    
    # Add validation
    #@validates("time")
    #def isvalidtime(self, key, val):
    #    return mv.intValIsAtMinXAndAtMaxY(val, 0, 23, "time");
    
    def __repr__(self):
        return f'<Signup {self.id_value}>';

#mycol.getMyClassRefsMain(True);
