from mybase import mybase;
from mybase import mycol;
from mycol import myvalidator;
from myrefcol import myrefcol;
validates = mycol.validates;
mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN, ERROR, or DISABLED.
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
                    isunique=False, autoincrements=False,
                    isforeignkey=True, foreignClass="MyOtherTestClass", foreignColNames=["mynewcol"],
                    foreignObjectName="myotstobj", constraints=None);# value=None,
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
                    isunique=False, autoincrements=False,
                    isforeignkey=True, foreignClass="MyTestColsClass", foreignColNames=["mynewcol"],
                    foreignObjectName="mytstcolsobj", constraints=None);# value=None,
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
                    isunique=False, autoincrements=False, issigned=False,
                    isforeignkey=True, foreignClass="MyModelWithCompPrimaryKey",
                    foreignColNames=["mynewcola", "mynewcolb"],
                    foreignObjectName="mycomppkyobj", constraints=None);#, "mynewcolc"#, value=None,
    mymulticolargs = None;
    mytablename = "compfkeytesttable";

#mycol.getMyClassRefsMain(True);

class Activity(mybase):
    __tablename__ = 'activities'

    #id = db.Column(db.Integer, primary_key=True);
    #name = db.Column(db.String);
    #difficulty = db.Column(db.Integer);
    #
    id = mycol(colname="id", datatype="Integer", defaultvalue=1, isprimarykey=True, isnonnull=True,
               issigned=False, isunique=True, autoincrements=True, constraints=None);
    name = mycol(colname="name", datatype="Text", defaultvalue=None, isprimarykey=False,
                 isnonnull=True, issigned=False, isunique=True, autoincrements=False, constraints=None);
    difficulty = mycol(colname="difficulty", datatype="Integer", defaultvalue=1, isprimarykey=False,
                       isnonnull=True, issigned=False, isunique=False, autoincrements=False,
                       constraints=None);

    # Add relationship
    #signups = db.relationship("Signup", back_populates="activity", cascade="all, delete-orphan");
    signupsinfo = myrefcol(listcolname="signups", refclassname="Signup");
    
    # Add serialization rules
    #serialize_rules = ("-signups",);
    #serialize_rules = ("-signups.activity",);#copied from old code what we used
    #
    ex_rules = ["signups.activity"];
    
    #def __repr__(self):
    #    return f'<Activity {self.id_value}: {self.name_value}>';
    def __repr__(self):
        return self.__simplerepr__(["<Activity ", ": ", " other ", ">"],
                                   ["id_value", "name_value", "signups"],
                                   ignoreerr=True, strstarts=True);

#mycol.getMyClassRefsMain(True);

class Camper(mybase):
    __tablename__ = 'campers';

    #validations and constraints bug problem 4-3-2025 4 AM MST: (bug is fixed)
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
    #
    #if the individual column has a constraint in the list and it is not empty or null,
    #then we check to see if the column name is found somewhere after the word CHECK(.
    #if it is found, then assumed valid, otherwise not valid.


    #id = db.Column(db.Integer, primary_key=True);
    #name = db.Column(db.String, nullable=False);
    #age = db.Column(db.Integer);
    #
    id = mycol(colname="id", datatype="Integer", defaultvalue=1, isprimarykey=True, isnonnull=True,
               issigned=False, isunique=True, autoincrements=True, constraints=None);
    name = mycol(colname="name", datatype="Text", defaultvalue=None, isprimarykey=False,
                 isnonnull=True, issigned=False, isunique=True, autoincrements=False,
                 constraints=[myvalidator.genSQLCheck("namelencheck",
                                                      myvalidator.genSQLLength("name") + " >= 1")]);
    age = mycol(colname="age", datatype="Integer", defaultvalue=1, isprimarykey=False, isnonnull=True,
                issigned=False, isunique=False, autoincrements=False,
                constraints=[myvalidator.genSQLCheck("agecheck", "age >= 8 AND age <= 18")]);

    # Add relationship
    #signups = db.relationship("Signup", back_populates="camper", cascade="all, delete-orphan");
    signupsinfo = myrefcol(listcolname="signups", refclassname="Signup");
    #
    #want it to refer to Signup.all.
    #we can add it once the class becomes defined
    #how do we know what the user wants to call it? colname
    #how do we know what class the users wants to reference? foreignclass name
    #maybe make it a mycol object that holds the information we need for this...
    #we could use some sort of colname
    #we could set the foreignClass
    #but this is not a foreign key. This is not a DB column at all.
    
    # Add serialization rules
    #serialize_rules = ("-signups",);
    #serialize_rules = ("-signups.camper",);#copied from old code what we used
    #
    ex_rules = ["signups.camper"];
    
    # Add validation
    #@validates("name")
    #def isvalidname(self, key, val):
    #    nmvld = mv.strValHasAtMinXChars(val, 1);
    #    if (nmvld): return val;
    #    else: raise ValueError("the camper must have a name!");
    #@validates(["name"])
    @validates("name")
    def isvalidname(self, key, val): return myvalidator.stringHasAtMinNumChars(val, 1);

    #@validates("age")
    #def isvalidage(self, key, val): return mv.intValIsAtMinXAndAtMaxY(val, 8, 18, "age");
    #@mycol.validates(["age"])#this is the same as #mycol.addValidator("Camper", "isvalidage", ["age"]);
    #@myvalidator.validates(["age"])
    #@mybase.validates(["age"])
    #@validates(["age"])
    #@validates("name", "age")#use for multi-column validator (will cause an error)
    @validates("age")
    def isvalidage(self, key, val): return myvalidator.isValueInRangeWithMaxAndMin(val, 8, 18);

    #myvalidator.addValidator("Camper", "isvalidage", ["age"]);

    #a little note on debugging validation methods:
    #if you register a multi-column validator for a method that only is supposed to do
    #single column validation, due to a timing issue, you may see an
    #AttributeError: 'classname' object has no attribute 'colname_value'
    #AttributeError: 'Camper' object has no attribute 'age_value'
    #check the validates call first before you check the method.
    #The validates call probably has mulitple columns on a single column validator method.
    #This could be causing your bug.
    #Also, you could add a print statement to see the key and the values.
    #If said print statements never fire, the bug is in validates call.
    #This could also cause a TypeError. You were expecting the keys or values to only be a string,
    #but it was a list for example.
    #again check the validates call first. If you gave it a multi-column validator for a single
    #column validation method, the validates call is your problem.
    #if not, your validation method is probably wrong.
    
    
    
    #a little note on debugging toString() or __repr__(self) or __str__(self):
    #the colname_value s may not be added yet unless explicitly set by you.
    #it is wise to check to see if they exist using hasattr(obj, "colname_value")
    #so if the crash is in the constructor of an object, then it is due to a timing issue.
    #there was not a fault of the user other than not explicitly setting all of them to None or null.
    #then the user tried using it, which is why it crashed with an attribute error.
    #AttributeError: 'classname' object has no attribute 'colname_value'
    #AttributeError: 'Camper' object has no attribute 'age_value'
    #
    #you could also not bother, and just use the __repr__ method in mybase class.
    #but if you want to only have certain attributes, then you can:
    #override the getKnownAttributeNamesForRepresentation(self) method
    #and put your own return of a list of strings for the attribute names you want.
    #the representation will get these attributes and build a string with them and
    #their values in that order.
    #but you may accidentally exclude information you wanted...
    #getOtherKnownSafeAttributesOnTheClass(cls) this returns a list of names of attributes on the class
    #that is of one of the following types: int, float, str, list, tuple
    #you may miss stuff that is easy to get like the:
    #tablename, multi_column_constraints_list, allconstraints_list
    #we can easily get those names by calling: cls.getNameOfVarIfPresentOnTableMain("tablename")
    #that returns the tablename var that the class has for example.
    #but if order matters, you are better off doing it yourself otherwise
    #most of these return in alphabetical order.
    #if you want just the col value names: getValueColNames(cls, mycols=None)
    #if you want just the col names: getMyColNames(cls, mycols=None) or getMyColAttributeNames(cls)
    #to get all of the cols colnames with their values we use:
    #for nm in cls.getMyColAttributeNames():
    #    mlist.append(nm);
    #    mlist.append(nm + "_value");
    #all is a reserved attribute name for a list of all instances of the class

    #def getKnownAttributeNamesForRepresentation(self):
    #    return ["id_value", "name_value", "age_value"];
    #    #return type(self).getValueColNames();#uses abc order of the above list

    #def __repr__(self):
        #mystr = "<Camper ";
        #mystr += (str(self.id_value) + ": " if (hasattr(self, "id_value")) else "None: ");
        #mystr += (str(self.name_value) if (hasattr(self, "name_value")) else "None") + " is ";
        #mystr += (str(self.age_value) if (hasattr(self, "age_value")) else "None");
        #mystr += " years old>";
        #return mystr;
        #return f'<Camper {self.id_value}: {self.name_value}>';
    
    def __repr__(self, exobjslist=None, usesafelistonly=False):
        return self.__simplerepr__(["<Camper ", ": ", " is ", " years old>"],
                                   myattrs=["id_value", "name_value", "age_value", "signups"],
                                   ignoreerr=True, strstarts=True, exobjslist=exobjslist,
                                   usesafelistonly=usesafelistonly);

#mycol.getMyClassRefsMain(True);

class Signup(mybase):
    __tablename__ = 'signups';

    #id = db.Column(db.Integer, primary_key=True);
    #time = db.Column(db.Integer);
    #
    id = mycol(colname="id", datatype="Integer", defaultvalue=1, isprimarykey=True, isnonnull=True,
               issigned=False, isunique=True, autoincrements=True, constraints=None);
    time = mycol(colname="time", datatype="Integer", defaultvalue=0, isprimarykey=False, isnonnull=True,
                issigned=False, isunique=False, autoincrements=False,
                constraints=[myvalidator.genCheckConstraint("timecheck", "time >= 0 AND time <= 23")]);

    # Add relationships
    #camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"));
    #activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"));
    #
    camper_id = mycol(colname="camper_id", datatype="Integer", defaultvalue=None, isprimarykey=False,
                      isnonnull=True, isunique=False, autoincrements=False, issigned=False,
                      isforeignkey=True, foreignClass="Camper", foreignColNames=["id"],
                      foreignObjectName="camper", constraints=None);
    activity_id = mycol(colname="activity_id", datatype="Integer", defaultvalue=None, isprimarykey=False,
                        isnonnull=True, isunique=False, autoincrements=False, issigned=False,
                        isforeignkey=True, foreignClass="Activity", foreignColNames=["id"],
                        foreignObjectName="activity", constraints=None);

    #camper = db.relationship("Camper", back_populates="signups");
    #activity = db.relationship("Activity", back_populates="signups");
    #
    #? = get the Camper object by id look up for each signup object...
    #? = get the Activity object by id look up for each signup object...
    #we can get these from the database using some sort of get from db method
    #OR we can get these from the object list that we have like Camper.all then find it on there...
    #these will be added and assigned in the constructor for the mybase class.
    #that assumes that:
    #-the user actually entered valid foreign key information and
    #-that the class where the foreign key links to is already instantiated and
    #-that the object exists, if it does not None will be returned
    #
    #we can create an object of class A, that refers to Class B,
    #but if the class B has not been instantiated yet, you cannot get the reference yet.
    #if the class has been instantiated, then the object with those specific values may not exist yet.
    #we will need to keep updating this until it is not None or null.
    #
    #the user will specify the vales for the foreign keys when they create the objects
    #then something will take those values and look it up...
    #if the class is not instantiated or the values are not found, then None
    #if found it gets returned.
    #if not found, we need to keep doing the look up on them each time a new object is created or
    #when the foreign key values change
    
    # Add serialization rules
    #serialize_rules = ("-camper", "-activity");
    #serialize_rules = ("-campers.signups", "-activity.signups");#copied from old code what we used
    #
    ex_rules = ["*.signups"];#["camper.signups", "activity.signups"];
    #only_rules = ["id_value", "time_value", "camper_id_value", "activity_id_value",
    #              "camper.name_value", "camper.id_value", "activity.name_value", "activity.id_value"];
    
    # Add validation
    #@validates("time")
    #def isvalidtime(self, key, val): return mv.intValIsAtMinXAndAtMaxY(val, 0, 23, "time");
    #@validates(["time"])
    @validates("time")
    def isvalidtime(self, key, val): return myvalidator.isValueInRangeWithMaxAndMin(val, 0, 23);
    
    #def __repr__(self):
    #    return f'<Signup {self.id_value}>';

    def __repr__(self, exobjslist=None, usesafelistonly=False):
        return self.__simplerepr__(["<Signup ", "other ", "stuff", ">"],
                                   ["id_value", "camper", "activity"],
                                   ignoreerr=True, strstarts=True, exobjslist=exobjslist,
                                   usesafelistonly=usesafelistonly);

    #def __to_dict__(self, myattrs=None, exobjslist=None, usesafelistonly=False, prefix=""):
    #    #nwlist = myvalidator.combineTwoLists(exobjslist, ["activity.signups", "camper.signups"]);
    #    nwlist = myvalidator.combineTwoLists(exobjslist, ["*.signups"]);
    #    return super().__to_dict__(myattrs=myattrs, exobjslist=nwlist, usesafelistonly=usesafelistonly,
    #                               prefix=prefix);

#mycol.getMyClassRefsMain(True);
