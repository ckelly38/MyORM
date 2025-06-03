from init import SQLVARIANT, CURSOR, CONN;
from models import mycol;
from mycol import myvalidator;
#from myvalidator import myvalidator;
from mybase import mybase;
from models import MyTestColsClass;
from models import MyOtherTestClass;
from models import MyModelWithCompPrimaryKey;
from models import MyModelWithCompForeignKey;
from models import Activity;
from models import Camper;
from models import Signup;
#from models import *;
#these imports are no longer needed
#import sys;
#import inspect;

print();
print("INSIDE OF TEST FILE!");
#print("list of system modules:");
#print(sys.modules[__name__]);
#print(inspect.getmembers(sys.modules[__name__], myvalidator.isClass));#list of tuples
#myclasses = [MyOtherTestClass, MyTestColsClass];
#mycol.setMyClassRefs(myclasses);
#mycol.getMyClassRefsMain(True);#will force the fetch of the new list if it has changed by now
#print(issubclass(mybase, mybase));
mybase.setupMain();

print();
#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

runresviapscpttsta = False;
if (runresviapscpttsta):
      mybase.restoreDBFromPyFile("./bkscrpt.py");
      raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

rungensqlfromscrpttst = False;
if (rungensqlfromscrpttst):
    with open("bkscrpt.py", "r") as mfile:
      scrptflines = mfile.readlines();
      mfile.close();
    sqlines = mybase.genSQLFileLinesFromScriptFileLines(scrptflines);
    for line in sqlines: print(line[0:len(line) - 1]);
    raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

#print(mynewcol);
#tstobj = MyTestColsClass(colnames=["mynewcol"], colvalues=[1]);
#values of the cols must get past into the constructor...
tstobj = MyTestColsClass(["mynewcol", "myfkeyid"], [1, 1]);
tstobjcols = tstobj.getMyCols();
print(f"\nPRINTING THE COLS AND TABLE NAME TO VERIFY THAT THE VALUES WERE SET CORRECTLY:\n");
print(tstobjcols);
print(tstobj.getTableName());
print("\nvalues for tstobj: via key name subscripted almost via getattr:");
tstobj.printValuesForAllCols(tstobjcols);
print("\nsome values for tstobj printed out via property:");
print(f"tstobj.mynewcol_value = {tstobj.mynewcol_value}");
print(f"tstobj.myfkeyid_value = {tstobj.myfkeyid_value}");
#context will be set in the constructor unless the user overrides it
#context should not be relied on and these methods are strongly subjective to it.
#tstobj.mynewcol.setContainer(tstobj);
print(tstobj.mynewcol.value);#no error if context is tstobj
#tstobj.mynewcol.setContainer(None);#error because context is not allowed to be null!
#tstobj.mynewcol.setContainer(tstobj.mynewcol);
#error because context must be an instance of a subclass of mybase
#print(tstobj.mynewcol.value);#errors out if one of the two immediately above setContexts are run.
#print(myvalidator.listMustContainUniqueValuesOnly(
#    ["colnamea", "colnameb", "colnamea"], "nonucolnames"));#also errors out
print(tstobj);
print(f"\ntstobj.myotstobj = {tstobj.myotstobj}\n");
#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

print("\nBEGIN CREATING OUR NEW OBJECT HERE NOW:\n");

tstobjb = MyOtherTestClass(["mynewcol", "myfkeyid"], [1, 1]);
#print(f"\n{tstobjb.getMyCols()}");
#print(tstobjb.getTableName());
print("\nvalues for tstobjb:");
tstobjb.printValuesForAllCols();
print(f"\n{tstobjb}\n");
print(f"tstobjb.mytstcolsobj = {tstobjb.mytstcolsobj}\n");
print(f"\ntstobj.myotstobj = {tstobj.myotstobj}\n");

#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

#the question is how can we get it so the user does not have to create an init?
#if we assign the foreign key col name in the col constructor,
#we cannot validate it until later on, but will have access to it.
#if we assign the class string name, we can get the class reference from the globals() list later on.


#question on the foreign key col, should the value of the key be assigned and stored in mycol or not?
#we ideally do not want to store it mycol because it suggests
#that we should be able to for others but we cannot.
#we also want to assign all of the other properties in the classes in the base class constructor
#on self of those class objects (not the references).
#a foreign key refers to a specific row on the data table,
#so I think it must be set when the object is initialized.
#SO ALL VALUES MUST BE SET WHEN THE OBJECT IS INITIALIZED.
#
#THEY CAN OF COURSE CHANGE LATER ON (BE UPDATED).
#
#SOME CHANGES MAY FORCE A BACKUP OF THE ENTIRE DATABASE,
#SUBSEQUENT DELETION, SOME RESTORATION, AND THEN ADDITION OF NEW DATA.

#foreign keys values match data problem bug 3-30-2025 4 AM

#if we can, we need to make sure the values for the foreign keys match too.
#or at least are valid. This might be a timing issue though.
#That is assuming we can get the values here.
#we have access to the calling class object here the class that has the
#foreign key on it
#however depending on the timing, the value may not be set yet...
#so we have access to one side of the values, what about the other side?
#we would need to know all objects created of the type.
#then we could see if one of them have it where the column values match.
#but the method that checks to see if the foreign key data types are valid
#runs in the base class constructor. So this is not necessarily guaranteed
#that all of the objects needed have been created even yet.
#So maybe this part needs to be separate.
#but even then this depends on the order the objects are created in.
#either that or the order the objects are saved in.
#this also depends on if the object lists have been synced up with the database or not.

#needs to be called on a column and needs the calling class object
#for mfcl in tstobjd.getMyForeignKeyCols():
#      print(mfcl.doesOrGetObjectThatHasTheForeignKeyValues(tstobjd, useget));
#      print(mfcl.doesForeignKeyValuesExistOnObjectsList(tstobjd));
#      print(mfcl.getObjectThatHasTheForeignKeyValues(tstobjd));



#we can have more than one database open at the same time
#but if the base class has a static list of all of them, then
#some on a different database would share the same names which would be legal as long as
#the same names are not on the same database

#myonewcol = mycol(colname="myonewcol", datatype="Integer", defaultvalue=0,
#                 isprimarykey=True, isforeignkey=False, isnonnull=False, isunique=False,
#                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
#errors out
#print(myonewcol);#value=1, 

#mybnewcol = mycol(colname="mybnewcol", datatype="Integer", defaultvalue=0,
#                 isprimarykey=True, isforeignkey=False, isnonnull=True, isunique=True,
#                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
#print(mybnewcol);# value=1, 

#tstobjc = MyModelWithCompPrimaryKey();
tstobjc = MyModelWithCompPrimaryKey.newBase([1, 1, 1]);
print("\nvalues for tstobjc:");
tstobjc.printValuesForAllCols();
print();

#tstobjd = MyModelWithCompForeignKey(["mynewcol", "mycompfkcolval"], [1, [1, 1]]);
tstobjd = MyModelWithCompForeignKey.newBase([[1, 1], 1]);#uses alphabetic order
#tstobjd = MyModelWithCompForeignKey.newBaseFromObjsList([{"mynewcol": 1}, {"mycompfkcolval": [1, 1]}]);
#tstobjd = MyModelWithCompForeignKey.newBaseFromListOfLists([["mynewcol", 1],
#                                                             ["mycompfkcolval", [1, 1]]]);
#tstobjd = MyModelWithCompForeignKey.newBaseFromListOfLists([("mynewcol", 1),
#                                                             ("mycompfkcolval", [1, 1])]);
#tstobjd = MyModelWithCompForeignKey.newBaseFromDataObj({"mynewcol": 1, "mycompfkcolval": [1, 1]});
print(tstobjc);
print("\nvalues for tstobjc:");
tstobjc.printValuesForAllCols();
print(f"\n{tstobjd}");
print("\nvalues for tstobjd:");
tstobjd.printValuesForAllCols();
print();

#needs to be called on a column and needs the calling class object
for mfcl in tstobjd.getMyForeignKeyCols():
      print(mfcl.doesForeignKeyValuesExistOnObjectsList(tstobjd));
      print(mfcl.getObjectThatHasTheForeignKeyValues(tstobjd));

runvdtorstst = True;
if (runvdtorstst):
      print("\nBEGIN GETTING ALL VALIDATORS TESTS:\n");
      print(mycol.getAllValidators());
      print(myvalidator.getAllValidators());
      #print(mycol.getMyClassRefsMain(False));
      for mv in myvalidator.getAllValidators():
            if mv["classname"] not in [mcref.__name__ for mcref in mycol.getMyClassRefsMain(False)]:
                  raise ValueError("classname " + mv['classname'] + " not found on list of classes!");
      print("\nDONE TESTING GET ALL VALIDATORS!\n");

#mcmpr = Camper(["name", "age"], ["Sydney", 20]);#error invalid age out of 8 to 18 inclusive range
#print(mcmpr);
#omcmpr = Camper(["name", "age"], ["", 9]);#error name cannot be empty!
#print(omcmpr);
vcmpr = Camper(["id", "name", "age"], [1, "Chris", 18]);
print(vcmpr);
ovcmpr = Camper(["id", "name", "age"], [2, "Sean", 16]);
print(ovcmpr);
print(ovcmpr.getMyRefCols());
print(ovcmpr.getMyRefColNames());
#when printed out the ID shows NONE because this will be pulled from the DB.
#until then the ID = NONE.

#add some activities here too
dball = Activity(["id", "name", "difficulty"], [1, "dodgeball", 5]);
prgmng = Activity(["id", "name", "difficulty"], [2, "programming", 10]);
print(dball);
print(prgmng);
print();
print("\nBEGIN CREATING SOME SIGNUPS HERE:\n");

#add some signups here for the campers, and maybe IDs for the campers
sa = None;
tstwithusrpid = False;
if (tstwithusrpid): sa = Signup(["id", "time", "camper_id", "activity_id"], [1, 8, 1, 2]);
else: sa = Signup(["time", "camper_id", "activity_id"], [8, 1, 2]);
sb = Signup(["id", "time", "camper_id", "activity_id"], [2, 9, 2, 1]);
sc = Signup(["id", "time", "camper_id", "activity_id"], [3, 9, 1, 1]);
print();

if (len(Signup.all) == 3): pass;
else: raise ValueError("there must be 3 signups, but there was not!");

#now recheck the signups to see if the lists are accurate...
runlinkreftests = False;
if (runlinkreftests):
      print("\nSIGNUPS:");
      print(Signup.all);
      print();
      print("CAMPER SIGNUPS:");
      print(ovcmpr.signups);
      print();
      print("ACTIVITY SIGNUPS:");
      print(dball.signups);
      print();

#after this build a better test and then do serialization.
runserializationtests = False;
if (runserializationtests):
      mysclslist = [Signup, Camper, Activity];
      for mycls in mysclslist:
            for item in mycls.all:
                  print(item.__to_dict__());
                  
                  hasonlyrules = True;
                  myonlyrules = None;
                  try:
                        myonlyrules = mycls.getSerializeOnlyRules();
                  except Exception as ex:
                        hasonlyrules = False;
                  hasexrules = True;
                  myexrules = None;
                  try:
                        myexrules = mycls.getExclusiveSerializeRules();
                  except Exception as ex:
                        hasexrules = False;
                  if (hasonlyrules): print(f"item.only_rules = {myonlyrules}");
                  if (hasexrules): print(f"item.ex_rules = {myexrules}");
            print("\nDONE WITH THE SERIALIZATION FOR " + mycls.__name__ + "!\n");
            #mybase.mcntr = 0;
      #for item in Signup.all:
      #      print(item.__to_dict__());
            #print(f"item.only_rules = {item.only_rules}");
      #      print(f"item.ex_rules = {item.ex_rules}");
      #print("\nDONE WITH THE SERIALIZATION FOR SIGNUPS!\n");
      #for item in Camper.all: print(item.__to_dict__());
      #print("\nDONE WITH THE SERIALIZATION FOR CAMPER!\n");
      #for item in Activity.all: print(item.__to_dict__());
      #print("\nDONE WITH THE SERIALIZATION FOR ACTIVITY!\n");

#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

#need to attempt to create the data tables if have not already and save the new objects to it
#if the ID is not assigned, let the DB put it on there....

tstnotablesbfrcreatecmd = False;
mysclslist = [MyModelWithCompPrimaryKey, Signup, Camper, Activity];
if (tstnotablesbfrcreatecmd):
      for mycls in mysclslist: mycls.dropTable(onlyifnot=True, runbkbfr=False, runbkaftr=False);

#test create table query only here
runtstctbleqry = False;
if (runtstctbleqry):
      varstr = "" + SQLVARIANT;
      for mycls in mysclslist:
            print(f"\nGen CREATE TABLE command for class ({mycls.__name__})!");
            print(f"\n{mycls.genSQLCreateTableFromRef(varstr=varstr, onlyifnot=True, isinctable=True)}");

#test remove all tables
tstnotables = True;
if (tstnotablesbfrcreatecmd): pass;
else:
      if (tstnotables):
            for mycls in mysclslist: mycls.dropTable(onlyifnot=True, runbkbfr=False, runbkaftr=False);

print("\nattempting to save data!\n");
print(f"tstnotablesbfrcreatecmd = {tstnotablesbfrcreatecmd}");
print(f"tstnotables = {tstnotables}");
print("no tables with save test (if one or both of the above is true, then true): " +
      f"{(tstnotablesbfrcreatecmd or tstnotables)}");
print(f"tstwithusrpid = {tstwithusrpid}");

#mybase.backupDB();

sa.save(runbkbfr=False, runbkaftr=False);
#vcmpr.save(runbkbfr=False, runbkaftr=False);
sb.save(runbkbfr=False, runbkaftr=False);

#sa = Signup(["id", "time", "camper_id", "activity_id"], [1, 8, 1, 2]);
sa.setValueForColumn("id", 4);
sa.setValueForColumn("time", 11);
sa.setValueForColumn("camper_id", 2);
sa.setValueForColumn("activity_id", 1);

print("\nattempting to update the data now!\n");

sa.save(runbkbfr=False, runbkaftr=False);

#need to test saving values with strings missing quotes and with null values.
#?;

#check to see if there is a base class property access problem
runbsclspropacsststs = False;
if (runbsclspropacsststs):
      print(f"sa last synced vals dict = {sa.getLastSyncedValsDict()}");#defined if saved else not
      print(f"sb last synced vals dict = {sb.getLastSyncedValsDict()}");
      print(f"vcmpr last synced vals dict = {vcmpr.getLastSyncedValsDict()}");#should not be defined

#need to sync the DB at the start...
#mybase.syncDB();

#need to run a backup of data on the DB...
mybase.backupDB();

#need to test deleting values or clearing entire DB tables...
rundeltests = True;
if (rundeltests):
      print(f"all items on the signups DB table are: {Signup.getAllItemsOnTable()}");
      #sa.deleteMyRowFromTable(onlyifnot=True, runbkbfr=False, runbkaftr=False);
      Signup.deleteARowFromTable(Signup.getMyColNames(Signup.getMyPrimaryKeyCols()), [4],
            onlyifnot=True, runbkbfr=False, runbkaftr=False);
      print(f"all items on the signups DB table are AFTER DELETING ONE: {Signup.getAllItemsOnTable()}");
      Signup.clearTable(onlyifnot=True, runbkbfr=False, runbkaftr=False);
      print("all items on the signups DB table are AFTER CLEARING THE TABLE: " +
            f"{Signup.getAllItemsOnTable()}\n");

runresviasqlfiletst = False;
#test restore DB from SQL file here
if (runresviasqlfiletst):
      mybase.restoreDBFromSQLFile("./bkcmdsonly.sql");
      #raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

runresviapscpttst = False;
if (runresviapscpttst):
      #the init import line may cause this to fail
      mybase.restoreDBFromPyFile("./bkscrpt.py");
      raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

runresviadatfiletst = False;
if (runresviadatfiletst):
      mybase.restoreDBFromDatOnlyFile("./bkdatonly.txt");
      raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

#still have a problem with multi-column and single column constraints adding or removing them
#need a good test case, but as of yet do not have a great one 5-13-2025 9:11 PM MST
#
#remove the agecheck constraint from Camper
#myvalidator.genSQLCheck("agecheck", "age >= 8 AND age <= 18")
#
#mybasesubclass.getMyColObjFromName(cls, mcnm, mycols=None);
#
#mycolobj.removeConstraint(self, mval, isinctable=False);
#mycolobj.removeAConstraintByName(self, mcnstnm, isinctable=False);
#mybasesubclass.removeAMultiColumnConstraintByName(cls, cnstnm);
#
runremsgcolcnsttst = True;
if (runremsgcolcnsttst):
      runtstnocmprtble = False;
      if (runtstnocmprtble): pass;
      else: Camper.createTable();#fails because not done yet
      print("CAMPER CONSTRAINTS BEFORE:");
      print(Camper.getMyColObjFromName("age", mycols=None).getConstraints());
      Camper.getMyColObjFromName("age", mycols=None).removeAConstraintByName("agecheck",
                                                                             isinctable=False);
      print("CAMPER CONSTRAINTS AFTER:");
      print(Camper.getMyColObjFromName("age", mycols=None).getConstraints());

runremmulcolcnsttst = True;
if (runremmulcolcnsttst):
      #runtstnocmprtble = True;
      #if (runtstnocmprtble): pass;
      #else: Camper.createTable();#fails because not done yet
      #print("CAMPER CONSTRAINTS BEFORE:");
      #print(Camper.getMultiColumnConstraints());
      #Camper.removeAMultiColumnConstraintByName(cnstnm);
      #print("CAMPER CONSTRAINTS AFTER:");
      #print(Camper.getMultiColumnConstraints());
      pass;

raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

print("IS VALUE IN RANGE OR STRING HAS AT MOST OR AT MIN AMOUNT OF CHARS TESTS:");
print();
print("mystr has at max 0 characters: " + str(myvalidator.stringHasAtMaxNumChars("mystr", 0)));#false
print("mystr has at min 6 characters: " + str(myvalidator.stringHasAtMinNumChars("mystr", 6)));#false
print("mystr has at max 5 characters: " + str(myvalidator.stringHasAtMaxNumChars("mystr", 5)));#true
print("mystr has at min 2 characters: " + str(myvalidator.stringHasAtMinNumChars("mystr", 2)));#true
#print(myvalidator.stringMustHaveAtMaxNumChars("mystr", 0, "varnm"));#error
print(myvalidator.stringMustHaveAtMaxNumChars("mystr", 5, "varnm"));
#print(myvalidator.stringMustHaveAtMinNumChars("mystr", 6, "varnm"));#error
print(myvalidator.stringMustHaveAtMinNumChars("mystr", 2, "varnm"));
print("is value in range tests:");
print("value 0, min 1, max 5 is value in range: " +
      str(myvalidator.isValueInRangeWithMaxAndMin(0, 1, 5)));#false
print("value 1, min 1, max 5 is value in range: " +
      str(myvalidator.isValueInRangeWithMaxAndMin(1, 1, 5)));#true
print("value 5, min 1, max 5 is value in range: " +
      str(myvalidator.isValueInRangeWithMaxAndMin(5, 1, 5)));#true
print("value -5, min 1, max 5 is value in range: " +
      str(myvalidator.isValueInRangeWithMaxAndMin(-5, 1, 5)));#false
print("value 2.5, min 1, max 5 is value in range: " +
      str(myvalidator.isValueInRangeWithMaxAndMin(2.5, 1, 5)));#true
print();

print("MY JOIN AND SPLIT METHOD (NOT SQL JOINS) TESTS:");
print();
print(myvalidator.myjoin("", ["some", " text", "with ", "other", "stuff"]));
print();
print(myvalidator.myjoin("\n", ["some", " text", "with ", "other", "stuff"]));
print();
print("\n".join(["some", " text", "with ", "other", "stuff"]));
print();
print(myvalidator.mysplitWithLen("the funny string", None, 2, 0));
#print(myvalidator.mysplitWithLen("the funny string", [3, 8, 12], [2, 4], 0));#error
#print(myvalidator.mysplit("the funny string", [3, 8, 12], [2, 4], 0));#error
print(myvalidator.mysplit("the funny string", [3, 8, 12], [2, 4, 1], 0));#["the", "unn", "", "ing"]
#the funny string
#01234567890123456 indexes
#          1
#   ^    ^   ^
#   ^^   ^^^^^
#   ^^   ^^
print(myvalidator.mysplitWithLen("the funny string", [3, 8], 2, 0));#["the", "unn", "string"];
print(myvalidator.mysplitWithDelimeter("the funny string", "", 0));
print();

print("BEGIN DATE AND TIME METHODS TESTS:");
print();
print(myvalidator.getMonthNames());
for n in range(12): print(myvalidator.getMonthNameFromNum(n + 1));
print();
print("MONTH ABBREVIATION TESTS:");
print(myvalidator.getAllThreeLetterAbbreviationsForMonthNames());
print(myvalidator.getAllFourLetterAbbreviationsForMonthNames());
for tltrabr in myvalidator.getAllThreeLetterAbbreviationsForMonthNames():
      print(myvalidator.getFullMonthNameFromAbreviation(tltrabr));
for frltrabr in myvalidator.getAllThreeLetterAbbreviationsForMonthNames():
      print(myvalidator.getFullMonthNameFromAbreviation(frltrabr));
for mnthnm in myvalidator.getMonthNames(): print(myvalidator.getMonthNumFromName(mnthnm));
print();
print("GET NUM DAYS IN THE MONTH TESTS:");
for n in range(12):
      if (n == 1):
            print("FEB NORMAL: " + str(myvalidator.getNumDaysInMonth(n + 1, False)) + " LEAP YEAR: " +
                  str(myvalidator.getNumDaysInMonth(n + 1, True)));
      else: print(myvalidator.getNumDaysInMonth(n + 1, False));
print(myvalidator.getDelimeterIndexesForDateStrings(True));
print(myvalidator.getDelimeterIndexesForDateStrings(False));
print();
print("GEN DATE STRING TESTS:");
print(myvalidator.genDateString(2, 29, 2024, True, True));#02-29-2024
print(myvalidator.genDateString(2, 29, 2024, True, False));#02/29/2024
print(myvalidator.genDateString(2, 29, 2024, False, True));#2024-02-29
print(myvalidator.genDateString(2, 29, 2024, False, False));#2024/02/29
#print(myvalidator.genDateString(2, 29, 2025, True, True));#error invalid date
print();
print("IS VALID DATE TESTS:");
print(myvalidator.isValidDate(2, 29, 2024));#true
print(myvalidator.isValidDate(2, 29, 2025));#false
#print(myvalidator.getMonthDayYearFromDateString("202afdssa2asdf"));#error
print(myvalidator.isValidDateFromString("202afdssa2asdf"));#false
print();
print("GET MONTH DAY YEAR FROM DATE STRING AND REVERSE TESTS:");
print(myvalidator.getMonthDayYearFromDateString("02-29-2024"));
print(myvalidator.getMonthDayYearFromDateString("2024-02-29"));
print(myvalidator.getMonthDayYearFromDateString("02-29-2025"));#may error due to it being invalid
print(myvalidator.getMonthDayYearFromDateString("2025-02-29"));#may error due to it being invalid
#print(myvalidator.getMonthDayYearFromDateString("2024-02-29-2024"));#error
print(myvalidator.isValidDateFromObj(myvalidator.getMonthDayYearFromDateString("02-29-2024")));#true
print(myvalidator.isValidDateFromObj(myvalidator.getMonthDayYearFromDateString("02-29-2025")));#false
print(myvalidator.genDateStringFromObj(myvalidator.getMonthDayYearFromDateString("02-29-2024"), True));
print(myvalidator.genDateStringFromObj(myvalidator.getMonthDayYearFromDateString("02-29-2024"), False));
print();
print("GEN TIME STRING TESTS:");
#print(myvalidator.genTimeString(23, 59, "a", True, True, True));#error on seconds
#print(myvalidator.genTimeString(23, 59, 59.99999999, True, True, True));#error on seconds
#print(myvalidator.genTimeString(23, 59, 60, True, True, True));#error on seconds
#print(myvalidator.genTimeString(23, 59, -1, True, True, True));#error on seconds
#print(myvalidator.genTimeString(23, 60, 59.99999999, True, True, True));#error on minutes
#print(myvalidator.genTimeString(23, -1, 59.99999999, True, True, True));#error on minutes
#print(myvalidator.genTimeString(839, 59, 59.9999999, True, True, True));#error on hours
print(myvalidator.genTimeString(838, 59, 59.9999999, True, True, True));#838:59:59.9999999
print(myvalidator.genTimeString(23, 59, 59.9999999, True, True, True));#23:59:59.9999999
print();
print("GET TIME OBJECT FROM TIME STRING AND REVERSE TESTS:");
print(myvalidator.getTimeObject("838:59:59.9999999", True));
print(myvalidator.getTimeObject("838:59", True));
print(myvalidator.getTimeObject("59:59.9999999", False));
#print(myvalidator.getTimeObject("59:59.9999999", True));#error invalid string given the parameters
#print(myvalidator.getTimeObject(" ", True));#error invalid characters found on this
print(myvalidator.getTimeObject("", True));
print(myvalidator.getTimeObject(None, True));
print(myvalidator.genTimeStringFromObj({}));
print(myvalidator.genTimeStringFromObj(None));
print(myvalidator.genTimeStringFromObj(myvalidator.getTimeObject("838:59", True)));
print();
#"1753-01-01 00:00:00.000"
dtstrb = myvalidator.genDateString(1, 1, 1, False, True);#usemonthdayyear, usedashes
dtstra = myvalidator.genDateString(1, 1, 1753, False, True);#usemonthdayyear, usedashes
tmstra = myvalidator.genTimeString(0, 0, 0, True, True, True);#inchr, incmin, incsec
tmstrb = myvalidator.genTimeString(838, 59, 59.9999999, True, True, True);#inchr, incmin, incsec
tmstrc = myvalidator.genTimeString(838, 59, 0, True, True, False);
tmstrd = myvalidator.genTimeString(0, 59, 59.9999999, False, True, True);
print(myvalidator.compareTwoDateTimeStrs(dtstra + " " + tmstra, dtstrb + " " + tmstra, True, True));
#b has numbers all less than a expected value is 1.
print(myvalidator.compareTwoDateTimeStrs(dtstrb + " " + tmstra, dtstra + " " + tmstra, True, True));
#a has numbers all less than b expected value is -1.
print(myvalidator.compareTwoDateTimeStrs(dtstrb + " " + tmstra, dtstrb + " " + tmstra, True, True));
#a and b are the same expected value is 0.
print(myvalidator.compareTwoDateTimeStrs(dtstra + " " + tmstrc, dtstrb + " " + tmstrd, True, False));
#b has numbers all less than a expected value is 1.
print(myvalidator.compareTwoDateTimeStrs(dtstrb + " " + tmstrd, dtstra + " " + tmstrc, False, True));
#a has numbers all less than b expected value is -1.
print(myvalidator.compareTwoDateTimeStrs(dtstrb + " " + tmstra, dtstrb + " " + tmstra, True, True));
#0 same string
#two dates only
print(myvalidator.compareTwoDateTimeStrs(dtstra, dtstrb, False, False));#1 see above
print(myvalidator.compareTwoDateTimeStrs(dtstrb, dtstra, False, False));#-1 see above
print(myvalidator.compareTwoDateTimeStrs(dtstrb, dtstrb, False, False));#0 same string
#two times only
print(myvalidator.compareTwoDateTimeStrs(tmstra, tmstrb, True, True));#-1
print(myvalidator.compareTwoDateTimeStrs(tmstrb, tmstra, True, True));#1
print(myvalidator.compareTwoDateTimeStrs(tmstra, tmstra, True, True));#0 same string
print(myvalidator.compareTwoDateTimeStrs(tmstrc, tmstrd, True, False));#1
print(myvalidator.compareTwoDateTimeStrs(tmstrd, tmstrc, False, True));#-1
print(myvalidator.compareTwoDateTimeStrs(tmstra, tmstra, True, True));#0 same string
#time string and date string only
print(myvalidator.compareTwoDateTimeStrs(dtstrb, tmstra, False, True));#1
#the no date or no time will be first b will be less than a expected value is 1
print(myvalidator.compareTwoDateTimeStrs(tmstra, dtstrb, True, False));#-1
#the no date or no time will be first a will be less than b expected value is -1
print("DONE WITH DATE AND TIME METHODS TESTS:");
print();
#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");


print("MY SQL VARIANT DATA TYPE INFO OBJECTS TESTS:");
print();
print("lite = ", end="");
liteinfoobjlist = myvalidator.getSQLDataTypesInfo('LITE');
myvalidator.printSQLDataTypesInfoObj(liteinfoobjlist);
print();
print("mysql = ", end="");
mysqlinfoobjlist = myvalidator.getSQLDataTypesInfo('MYSQL');
myvalidator.printSQLDataTypesInfoObj(mysqlinfoobjlist);
print();
print("sqlserver = ", end="");
sqlsrvrinfoobjlist = myvalidator.getSQLDataTypesInfo('SQLSERVER');
myvalidator.printSQLDataTypesInfoObj(sqlsrvrinfoobjlist);
print();
print("ALL:");
print();
print(myvalidator.getValidSQLDataTypesFromInfoList(liteinfoobjlist));
print(myvalidator.getValidSQLDataTypesFromInfoList(mysqlinfoobjlist));
print(myvalidator.getValidSQLDataTypesFromInfoList(sqlsrvrinfoobjlist));
print();
print("NO PARAMETERS ONLY (NOPSONLY):");
print();
print(myvalidator.getValidSQLDataTypesWithNoParametersOnlyFromInfoList(liteinfoobjlist));
print(myvalidator.getValidSQLDataTypesWithNoParametersOnlyFromInfoList(mysqlinfoobjlist));
print(myvalidator.getValidSQLDataTypesWithNoParametersOnlyFromInfoList(sqlsrvrinfoobjlist));
print();
print("PARAMETERS ONLY (PSONLY):");
print();
psonlylite = myvalidator.getValidSQLDataTypesWithParametersOnlyFromInfoList(liteinfoobjlist);
psonlymysql = myvalidator.getValidSQLDataTypesWithParametersOnlyFromInfoList(mysqlinfoobjlist);
psonlysqlsrvr = myvalidator.getValidSQLDataTypesWithParametersOnlyFromInfoList(sqlsrvrinfoobjlist);
print(psonlylite);
print(psonlymysql);
print(psonlysqlsrvr);

print();
print("BEGIN TYPES WITH PARAMETERS CLASSIFICATIONS:");
print();
print("1. SET TOTAL AMOUNT OF DIGITS AND SET AMOUNT AFTER THE DECIMAL POINT:");
print();
#None is not needed but will not crash this method
#print(myvalidator.getAllDataTypesWithASetAmountOfDigitsAndAfterDecimalPoint(None));
tdgtsandadptlite = myvalidator.getAllDataTypesWithASetAmountOfDigitsAndAfterDecimalPoint("LITE");
tdgtsandadptmysql = myvalidator.getAllDataTypesWithASetAmountOfDigitsAndAfterDecimalPoint("MYSQL");
tdgtsandadptsqlsrvr = myvalidator.getAllDataTypesWithASetAmountOfDigitsAndAfterDecimalPoint("SQLSERVER");
print(tdgtsandadptlite);
print(tdgtsandadptmysql);
print(tdgtsandadptsqlsrvr);
print();
print("2. SET AMOUNT OF DIGITS AFTER THE DECIMAL POINT ONLY:");
print();
#None is not needed but will not crash this method
#print(myvalidator.getAllDataTypesWithASetAmountOfDigitsAfterTheDecimalPointOnly(None));
dgtsadptonlylite = myvalidator.getAllDataTypesWithASetAmountOfDigitsAfterTheDecimalPointOnly("LITE");
dgtsadptonlymysql = myvalidator.getAllDataTypesWithASetAmountOfDigitsAfterTheDecimalPointOnly("MYSQL");
dgtsadptonlysqlsrvr = myvalidator.getAllDataTypesWithASetAmountOfDigitsAfterTheDecimalPointOnly(
      "SQLSERVER");
print(dgtsadptonlylite);
print(dgtsadptonlymysql);
print(dgtsadptonlysqlsrvr);
print();
print("3. HAS A LIST AS THE ONLY PARAMETER:");
print();
listasonlyplite = myvalidator.getAllDataTypesWithAListAsTheParameter("LITE");
listasonlypmysql = myvalidator.getAllDataTypesWithAListAsTheParameter("MYSQL");
listasonlypsqlsrvr = myvalidator.getAllDataTypesWithAListAsTheParameter("SQLSERVER");
print(listasonlyplite);
print(listasonlypmysql);
print(listasonlypsqlsrvr);
print();
print("4. HAS A DISPLAY WIDTH AS THE ONLY PARAMETER:");
print();
dpwdthasonlyplite = myvalidator.getTypesThatHaveADisplayWidthParam("LITE");
dpwdthasonlypmysql = myvalidator.getTypesThatHaveADisplayWidthParam("MYSQL");
dpwdthasonlypsqlsrvr = myvalidator.getTypesThatHaveADisplayWidthParam("SQLSERVER");
print(dpwdthasonlyplite);
print(dpwdthasonlypmysql);
print(dpwdthasonlypsqlsrvr);
print();
print("5. HAS A LENGTH AS THE ONLY PARAMETER:");
print();
lenasonlyplite = myvalidator.getTypesThatHaveLengthAsTheParam("LITE");
lenasonlypmysql = myvalidator.getTypesThatHaveLengthAsTheParam("MYSQL");
lenasonlypsqlsrvr = myvalidator.getTypesThatHaveLengthAsTheParam("SQLSERVER");
print(lenasonlyplite);
print(lenasonlypmysql);
print(lenasonlypsqlsrvr);
print();
print("6. HAS A BYTE RELATED LENGTH AS THE ONLY PARAMETER:");
print();
lenrbtsasonlyplite = myvalidator.getTypesThatHaveAByteRelatedLengthAsTheParam("LITE");
lenrbtsasonlypmysql = myvalidator.getTypesThatHaveAByteRelatedLengthAsTheParam("MYSQL");
lenrbtsasonlypsqlsrvr = myvalidator.getTypesThatHaveAByteRelatedLengthAsTheParam("SQLSERVER");
print(lenrbtsasonlyplite);
print(lenrbtsasonlypmysql);
print(lenrbtsasonlypsqlsrvr);
print();
#if on one of the lists, the type name matches, and number of parameters implied matches
#then not remaining
print("WHAT I STILL HAVE REMAINING TO DO:");
print();
numreqpsarr = [2, 1, 1, 1, 1, 1];
myliteusedlist = [tdgtsandadptlite, dgtsadptonlylite, listasonlyplite, dpwdthasonlyplite,
                  lenasonlyplite, lenrbtsasonlyplite];
mysqlusedlist = [tdgtsandadptmysql, dgtsadptonlymysql, listasonlypmysql, dpwdthasonlypmysql,
                 lenasonlypmysql, lenrbtsasonlypmysql];
sqlsrvrusedlist = [tdgtsandadptsqlsrvr, dgtsadptonlysqlsrvr, listasonlypsqlsrvr, dpwdthasonlypsqlsrvr,
                   lenasonlypsqlsrvr, lenrbtsasonlypsqlsrvr];
rempsonlite = myvalidator.getRemainingParameters(psonlylite, myliteusedlist, numreqpsarr);
rempsonmysql = myvalidator.getRemainingParameters(psonlymysql, mysqlusedlist, numreqpsarr);
rempsonsqlsrvr = myvalidator.getRemainingParameters(psonlysqlsrvr, sqlsrvrusedlist, numreqpsarr);
print(rempsonlite);
print(rempsonmysql);
print(rempsonsqlsrvr);
print();
print("DONE WITH TYPES WITH PARAMETERS CLASSIFICATIONS TESTS!");
print();
raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

myreslist = myvalidator.getCompleteSetListFromList(["a", "b", "c", "d", "e", "f"]);
print(myreslist);
print("b,d,e" in myreslist);
print();
#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

#quote did not actually get escaped
enmbasestr = "ENUM('something, other', 'some ofht', 'this, some, other, else', 'else', ";
enmodptstr = "'something else, other', 'last'";
finenmstr = enmbasestr + "'mychar\\\'s poses)sive', " + enmodptstr;
print(myvalidator.getLevelsForValStr(enmbasestr + "'mychar\'s poses)sive', " + enmodptstr + ")"));
print(myvalidator.getLevelsForValStr(finenmstr + ")"));
print(myvalidator.getParamsFromValType(finenmstr + ")"));
print();
print(myvalidator.getDataTypeObjectWithNameOnVariant(finenmstr + ")", "MYSQL"));
print(myvalidator.getDataTypeObjectWithNameOnVariant("NUMERIC(1)", "SQLSERVER"));
print(myvalidator.getDataTypeObjectWithNameOnVariant("DATETIME2", "SQLSERVER"));
print(myvalidator.getDataTypeObjectWithNameOnVariant("NUMERIC(1, 38)", "SQLSERVER"));
print();
print(myvalidator.getDataTypesObjsFromTypeName("FLOAT", "MYSQL"));
print();
#print(myvalidator.isValidDataType(finenmstr, "MYSQL"));#false
print(myvalidator.isValidDataType(finenmstr + ")", "MYSQL"));#true
print(myvalidator.isValidDataType("ENUM('vala', 'vala', 'valb', 'my val')", "MYSQL"));
#false duplicate values
print(myvalidator.isValidDataType("SET('vala', 'vala', 'valb', 'my val')", "MYSQL"));
#false duplicate values
print();
print(myvalidator.isValidDataType("OTHER, VARCHAR(max)", "SQLSERVER"));#false
print(myvalidator.isValidDataType("VARCHAR(max), OTHER", "SQLSERVER"));#false
print(myvalidator.isValidDataType("NUMERIC(p, s)", "SQLSERVER"));#false
print(myvalidator.isValidDataType("NUMERIC(1, 39, 20)", "SQLSERVER"));#false#too many parameters
print(myvalidator.isValidDataType("NUMERIC(39, 1)", "SQLSERVER"));#false#38 or less for both
print(myvalidator.isValidDataType("NUMERIC(1, 39)", "SQLSERVER"));#false#38 or less for both
print(myvalidator.isValidDataType("NUMERIC(39)", "SQLSERVER"));#false#38 or less for both
print(myvalidator.isValidDataType("NUMERIC(1)", "SQLSERVER"));#true
print(myvalidator.isValidDataType("VARCHAR(max)", "SQLSERVER"));#true
print(myvalidator.isValidDataType("DATETIME2", "SQLSERVER"));#true
print();
raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

print(myvalidator.isValueValidForDataType("TINYINT", "a", "SQLSERVER", True, True));#false not a number
print(myvalidator.isValueValidForDataType("TINYINT", "adsfsad203e4", "SQLSERVER", True, True));
#false not a number
print(myvalidator.isValueValidForDataType("TINYINT", 256, "SQLSERVER", True, True));#false 255 max
print(myvalidator.isValueValidForDataType("TINYINT(4)", 256, "MYSQL", True, True));
#false 255 max and invalid size
print(myvalidator.isValueValidForDataType("TINYINT(3)", 256, "MYSQL", True, True));
#false 255 max and invalid size
print(myvalidator.isValueValidForDataType("TINYINT(3)", 1000, "MYSQL", True, True));
#false 255 max size disagreement
print(myvalidator.isValueValidForDataType("TINYINT(2)", 255, "MYSQL", True, False));
#false null cannot be allowed for this data type.
#
#display width type class test here:
#
#size problem is not tested for because the value is out of range and the range is checked first.
print(myvalidator.isValueValidForDataType("TINYINT(2)", 255, "MYSQL", True, True));#true valid
#false value is outside of display size range, but the type can still store it. so returns true valid.

print(myvalidator.isValueValidForDataType("TINYTEXT",
                                          myvalidator.genStringWithNumberText(255), "MYSQL"));#true
print(myvalidator.isValueValidForDataType("TINYTEXT",
                                          myvalidator.genStringWithNumberText(256), "MYSQL"));#false
#above test is out side of the 255 charcters that that can store so not valid
#but I will note that although a range of values is not technically given, a range on the length is.
#this type however has no parameters, so it is not exactly what I am looking for for the test.

#there is another note-worthy bug I need to check for, if non-null values are properly enforced.
#the type may allow null values as a default, but if non-null is selected,
#null should not be used or is not valid.
print(myvalidator.isValueValidForDataType("TINYTEXT", "NULL", "MYSQL", True, False));#true
print(myvalidator.isValueValidForDataType("TINYTEXT", "NULL", "MYSQL", True, True));#false

#I need a test where the value is in the required range, but not when dictated by the parameters
#to produce the test case the variant is probably MYSQL.
#although we could use display width as the parameter to dictate that the value is out of range for
#testing I want an example that does not use this as the parameter.
#I should be able to get it with something like DECIMAL or NUMERIC or FLOAT or REAL ...

#parameters limit the length of the value and
#how many digits can be stored after the decimal point class tests:

#useunsigned, isnonnull
print(myvalidator.isValueValidForDataType("DECIMAL(3, 1)", 312.5, "SQLSERVER", False, True));#false
print(myvalidator.isValueValidForDataType("NUMERIC(3, 1)", 312.5, "SQLSERVER", False, True));#false
print(myvalidator.isValueValidForDataType("DECIMAL(3, 1)", 12.5, "SQLSERVER", False, True));#true
print(myvalidator.isValueValidForDataType("NUMERIC(3, 1)", 12.5, "SQLSERVER", False, True));#true

#the number is in the really big range of -10^38 to 10^38,
#but according to the parameters the total number of digits should be 3,
#and 1 should be after the decimal point which is not the case. Both paremeters should be less than 38.

#length test class tests:

print(myvalidator.isValueValidForDataType("CHAR(255)", myvalidator.genStringWithNumberText(255),
                                          "MYSQL"));#true
print(myvalidator.isValueValidForDataType("CHAR(255)", myvalidator.genStringWithNumberText(256),
                                          "MYSQL"));#false
print(myvalidator.isValueValidForDataType("BIT(2)", "01", "MYSQL"));#true
print(myvalidator.isValueValidForDataType("BIT(64)", myvalidator.genStringWithNumberText(65),
                                          "MYSQL"));#false
#invalid length and invalid data stored on a bit
print(myvalidator.isValueValidForDataType("BIT(64)", myvalidator.genStringWithNumberText(64),
                                          "MYSQL"));#false
#invalid data stored on a bit

#length byte related test class tests

#BINARY(255) and TINYBLOB tests for mysql here
btbinnum=2040;#255*8
btnumpone = btbinnum + 1;
for tpnm in ["BINARY(255)", "TINYBLOB"]:
      print(myvalidator.isValueValidForDataType(tpnm, myvalidator.genStringWithNumberText(btbinnum, 10),
                                                "MYSQL"));#false invalid data
      print(myvalidator.isValueValidForDataType(tpnm, myvalidator.genStringWithNumberText(btbinnum, 2),
                                                "MYSQL"));#true
      print(myvalidator.isValueValidForDataType(tpnm, myvalidator.genStringWithNumberText(btnumpone, 2),
                                                "MYSQL"));#false invalid length

#param is a list test class tests here

print(myvalidator.isValueValidForDataType("ENUM('vala', 'other', 'else')", "'vala,other'", "MYSQL"));
#false invalid if not on the list
print(myvalidator.isValueValidForDataType("ENUM('vala', 'other', 'else')", "'other'", "MYSQL"));#true
print(myvalidator.isValueValidForDataType("SET('vala', 'other', 'else')", "'something'", "MYSQL"));
#false invalid if not on the list and cannot be made by a combination of the elements
print(myvalidator.isValueValidForDataType("SET('vala', 'other', 'else')", "'other'", "MYSQL"));#true
#direct match
print(myvalidator.isValueValidForDataType("SET('vala', 'other', 'else')", "'vala,other'", "MYSQL"));
#true because you can take the values on the list and make this one
#or true because it is a direct match


#need a test for FLOAT(p) or figure out what test class to put it in
myofltval = 1.8*(10**38);#NOT SURE ON THESE TESTS AND ON THE RANGE HERE.
print(myvalidator.isValueValidForDataType("FLOAT(54)", myofltval, "MYSQL"));#false invalid type
print(myvalidator.isValueValidForDataType("FLOAT(53)", myofltval, "MYSQL", True, False));
#false signed only and cannot be null
print(myvalidator.isValueValidForDataType("FLOAT(53)", myofltval, "MYSQL", True, True));
#false signed only
print(myvalidator.isValueValidForDataType("FLOAT(53)", myofltval, "MYSQL", False, False));
#false cannot be null
#not entirely sure on the values that can and cannot be stored depending on the p value.
#the tests may need to change.
#so the below 2 tests will return true if the number is in the given range.
#I am also not that confident on the range used.
print(myvalidator.isValueValidForDataType("FLOAT(24)", myofltval, "MYSQL", False, True));
#false too small
print(myvalidator.isValueValidForDataType("FLOAT(53)", myofltval, "MYSQL", False, True));#true
#raise ValueError("NEED TO CHECK THE RESULTS HERE...!");

#these conduct some other tests on the method and for the data type.

#parameter limits the number of digits after the decimal point class tests:

myfltval = 1234.567890123;
print(myvalidator.isValueValidForDataType("FLOAT(3, 1)", myfltval, "SQLSERVER"));#false invalid type
print(myvalidator.isValueValidForDataType("FLOAT(53)", myfltval, "SQLSERVER", True, False));
#false signed only and cannot be null
print(myvalidator.isValueValidForDataType("FLOAT(53)", myfltval, "SQLSERVER", True, True));
#false signed only
print(myvalidator.isValueValidForDataType("FLOAT(53)", myfltval, "SQLSERVER", False, False));
#false cannot be null
print(myvalidator.isValueValidForDataType("FLOAT(24)", myfltval, "SQLSERVER", False, True));
#false too small
print(myvalidator.isValueValidForDataType("FLOAT(53)", myfltval, "SQLSERVER", False, True));#true

#MYSQL TIME RANGE IS: "-838:59:59.000000", "838:59:59.999999"
print(myvalidator.isValueValidForDataType("TIME(0)", "24:59:59.999999", "MYSQL"));#false
print(myvalidator.isValueValidForDataType("TIME(0)", "24:59.999999:59", "MYSQL"));#false minutes invalid
print(myvalidator.isValueValidForDataType("TIME(6)", "24:59:59.999999", "MYSQL"));#true

#tests on string types:

#I need a test where the value in the required range, but it is specifically formated like a date.
print(myvalidator.isValueValidForDataType("DATE", "2029-02-28", "SQLSERVER"));#true

#tests where data in the wrong format goes into a type with formatted data.
#like text into numbers or
#text like a numbers and or other characters into something like a date for example.
print(myvalidator.isValueValidForDataType("DATE", "202afdssa2asdf", "SQLSERVER"));#false not a date.
print(myvalidator.isValueValidForDataType("DATE", "202afdssa2", "SQLSERVER"));#false not a date.
print(myvalidator.isValueValidForDataType("DATE", "2029302329", "SQLSERVER"));#false not a date.
#also a test where the value is in the required range, but not actually valid like a date.
print(myvalidator.isValueValidForDataType("DATE", "2029-02-29", "SQLSERVER"));#false not a valid date.


#some date time formats do not allow fractional seconds or minutes to not be an integer, etc.
#but these formatting constraints are not actually enforced yet (3-25-2025 4:30 AM MST):
#need to make tests to check for this problem on all of those formats.

#SQLSERVER:
#
#DATETIME YYYY-MM-DD HH:MM:SS[.NNN] from 1753-01-01 to 9999-12-31
# with an accuracy of 3.33 miliseconds.
#DATETIME2 YYYY-MM-DD HH:MM:SS[.NNNNNNN] from 0001-01-01 to 9999-12-31
# with an accuracy of 100 nanoseconds.
#SMALLDATETIME YYYY-MM-DD HH:MM:SS from 1900-01-01 to 2079-06-06 with an accuracy of 1 minute.
#DATE YYYY-MM-DD 0001-01-01 to 9999-12-31.
#TIME HH:MM:SS[.NNNNNNN] store a time only with an accuracy of 100 nanoseconds.
#DATETIMEOFFSET YYYY-MM-DD HH:MM:SS[.NNNNNNN] [+|-] HH:MM (in UTC)


#"SMALLDATETIME" min "1900-01-01 00:00:00" max "2079-06-06 23:59:59"
print(myvalidator.isValueValidForDataType("SMALLDATETIME", "2080-02-29 23:59:59", "SQLSERVER"));#false
#out of range for the type
print(myvalidator.isValueValidForDataType("SMALLDATETIME", "2076-02-29 23:59:59", "SQLSERVER"));#true
print(myvalidator.isValueValidForDataType("SMALLDATETIME", "2076-02-29 23:59:59.999999", "SQLSERVER"));
#false fractionalseconds not allowed to be stored on this format

print(myvalidator.isValueValidForDataType("DATETIME", "2076-02-29 23:59:59.999999", "SQLSERVER"));
#false too many decimal place digits for the format only 3 allowed max

print(myvalidator.isValueValidForDataType("DATETIME2", "2076-02-29 23:59:59.9999999", "SQLSERVER"));
#true

print(myvalidator.isValueValidForDataType("DATETIME2", "2076-02-29 23:59:59.99999999", "SQLSERVER"));
#false too many decimal place digits for the format only 7 allowed max

print(myvalidator.isValueValidForDataType("TIME", "23:59:59.99999999", "SQLSERVER"));
#false too many decimal place digits for the format only 7 allowed max

print(myvalidator.isValueValidForDataType("DATETIMEOFFSET", "9998-12-31 23:59:59.99999999 + 23:59",
                                          "SQLSERVER"));
#false too many decimal place digits for the format only 7 allowed max

#"DATETIMEOFFSET" min "0001-01-01 00:00:00.0000000 - 23:59"
# max "9999-12-31 23:59:59.9999999 + 23:59"
print(myvalidator.isValueValidForDataType("DATETIMEOFFSET", "0002-01-01 00:00:00.0000000 - 23:59",
                                          "SQLSERVER"));#true
print(myvalidator.isValueValidForDataType("DATETIMEOFFSET", "9998-12-31 23:59.99999:59.9 + 23:59",
                                          "SQLSERVER"));#false minutes must be an integer
print(myvalidator.isValueValidForDataType("DATETIMEOFFSET", "9998-12-31 23:59.99999:59.9999999 + 23:59",
                                          "SQLSERVER"));#false minutes must be an integer
print(myvalidator.isValueValidForDataType("DATETIMEOFFSET", "9998-12-31 23:59:59.9999999 + 23:59.99999",
                                          "SQLSERVER"));#false minutes must be an integer
print();
raise ValueError("NEED TO CHECK THE RESULTS HERE...!");


print("SQL GEN TESTS:");
print(myvalidator.genUniqueConstraint("constraintname", ["itema", "itemb", "itemc"]));
print(myvalidator.genUniqueConstraint("", ["itema", "itemb", "itemc"]));
print(myvalidator.genCheckConstraint("constraintname", "itema >= 2"));
print(myvalidator.genCheckConstraint("", "itema >= 2"));

#passes because not from table, from table only passes now because now the class is defined...
print(myvalidator.genLengthCol("name", "campers"));
print(myvalidator.genSQLMinOrMax(True, "name"));
print(myvalidator.genSQLMinOrMax(True, "campers.name"));

print(myvalidator.genSQLMinOrMax(True, [10, 20, 40, 30, 80, 50]));
print(myvalidator.genSQLMinOrMax(False, [10, 20, 40, 30, 80, 50]));
#counts
print(myvalidator.genCount(["mynewcola", "mynewcolb"], [tstobjc.getTableName()], False, False));
print(myvalidator.genCount(["mynewcola", "mynewcolb"], [tstobjc.getTableName()], True, False));
print(myvalidator.genCount(["mynewcola", "mynewcolb"], [tstobjc.getTableName()], False, True));
print(myvalidator.genCount(["mynewcola", "mynewcolb"], [tstobjc.getTableName()], True, True));
print(myvalidator.genCountAll(False));
print(myvalidator.genCountAll(True));
#selects
print(myvalidator.genCustomSelect("1", "mytablename", False));
print(myvalidator.genCustomSelect("1", "mytablename", True));
#still a select all method
#useselonly, useseldistinct, usecntdistinct
print(myvalidator.genSelectAllAndOrCountOnTables(
    [tstobjb.getTableName(), tstobjc.getTableName(), tstobjd.getTableName()],
    None, None, True, True, False));
print(myvalidator.genSelectAllAndOrCountOnTables(
    [tstobjb.getTableName(), tstobjc.getTableName(), tstobjd.getTableName()],
    ["mynewcol", "mynewcola", "mynewcolb"],
    [tstobjb.getTableName(), tstobjc.getTableName(), tstobjc.getTableName()], False, False, True));
#ERRORS OUT BECAUSE SELECT DISTINCT COUNT(DISTINCT *) FROM wherever IS ILLEGAL.
#ERRORS OUT BECAUSE SELECT DISTINCT *, COUNT(DISTINCT *) FROM wherever IS ILLEGAL.
#print(myvalidator.genSelectAllAndCountAllOnTables([tstobjb.getTableName()], True, True));#error
#print(myvalidator.genCustomSelect("COUNT(DISTINCT *)", tstobjc.getTableName(), True));#error
#print(myvalidator.genSelectCountOnlyOnTables([tstobjc.getTableName()], None, None, True, True));#error

#useselonly, usecntonly, useseldistinct, usecntdistinct
print(myvalidator.genSelectSomeAndOrCountOnTables(["mynewcol", "mynewcola", "mynewcolb"],
                                              [tstobjb.getTableName(), tstobjc.getTableName(),
                                               tstobjc.getTableName()],
                                              ["mynewcol", "myfkeyid"],
                                              [tstobjb.getTableName(), tstobjb.getTableName()],
                                              False, False, True, True));
#usedistinct
print(myvalidator.genSelectSomeOnlyOnTables(["mynewcol", "mynewcola", "mynewcolb"],
                                            [tstobjb.getTableName(), tstobjc.getTableName(),
                                             tstobjc.getTableName()], True));
print(myvalidator.genSelectSomeOnlyOnTables(["mynewcol", "mynewcola", "mynewcolb"],
                                            [tstobjb.getTableName(), tstobjc.getTableName(),
                                             tstobjc.getTableName()], False));
#useseldistinct, usecntdistinct
print(myvalidator.genSelectCountOnlyOnTables([tstobjb.getTableName(), tstobjc.getTableName(),
                                              tstobjc.getTableName()], ["mynewcol", "myfkeyid"],
                                              [tstobjb.getTableName(), tstobjb.getTableName()],
                                              True, True));
print(myvalidator.genSQLIn([None, "something", "other"], False));#will include null
print(myvalidator.genWhere("age > 9"));
print(myvalidator.genHaving("COUNT(personID) > 9"));
print(myvalidator.genBetween("vala", "valb"));
print(myvalidator.genGroupBy("age"));
print(myvalidator.genLengthCol("mynewcol", tstobjb.getTableName()));
print(myvalidator.genSQLimit(4, 10));
print(myvalidator.genSQLimit(4, 0));
print(myvalidator.genCheckConstraint("checkage", "age > 18"));
print(myvalidator.genSQLSwitchCase(["Quantity > 30", "Quantity = 30"],
                                   ["'The quantity is greater than 30.'", "'The quantity equals 30.'"],
                                   "'The quantity is less than 30.'", "QuantityText"));
print(myvalidator.genSQLSwitchCase(["Quantity > 30", "Quantity = 30"],
                                   ["'The quantity is greater than 30.'", "'The quantity equals 30.'"],
                                   "'The quantity is less than 30.'", None));
print(myvalidator.genSQLSwitchCase(["Quantity > 30", "Quantity = 30"],
                                   ["'The quantity is greater than 30.'", "'The quantity equals 30.'"],
                                   None, None));
print(myvalidator.genSortOrderByAscVal(4, False));
print(myvalidator.genSortOrderByAscVal(4, True));
print(myvalidator.genOrderBy(["mynewcol", "mynewcola", "mynewcolb"],
                             [tstobjb.getTableName(), tstobjc.getTableName(), tstobjc.getTableName()],
                             True, [True, False, False]));
print(myvalidator.genOrderBy(["mynewcol", "mynewcola", "mynewcolb"],
                             [tstobjb.getTableName(), tstobjc.getTableName(), tstobjc.getTableName()],
                             True, [False, False]));
print(myvalidator.genOrderBy(["mynewcol", "mynewcola", "mynewcolb"],
                             [tstobjb.getTableName(), tstobjc.getTableName(), tstobjc.getTableName()],
                             True, None));
print(myvalidator.genSQLMin("mynewcol", tstobjb.getTableName(), True));
print(myvalidator.genSQLMax("mynewcola", tstobjc.getTableName(), False));
print(myvalidator.genSQLAvg("price", True));
print(myvalidator.genSQLAvg("price", False));
print(myvalidator.genSQLSum("price", True));
print(myvalidator.genSQLSum("price", False));

#each database has its own way to do custom procedures, so this program will not provide a generic way.
#
#WHAT I STILL NEED TO DO: 4-30-2025
#-CREATE TABLE, INSERT INTO, UPDATE, DELETE, SELECT INTO, INSERT INTO SELECT
#-LEFT JOIN, RIGHT JOIN, INNER JOIN, FULL JOIN, NATURAL JOIN, UNIONS
#--note: some of these are different from LITE to normal SQL.
#-figure out a way to let the user determine what to name the db
#-figure out how to integrate mysql/postgressql/sqlserver/oracle...
#-figure out a way to tell the program if using sqllite or sql and
#--if the commands are different from sql to sqllite (JOINS ARE) how they change in the generator
#-figure out where to put the sql generator methods
#-ways to save data, ways to add new data, ways to remove data, ways to update the data, (#2)
#-and ways to remove tables (#3)
#-ways to back up the database (#5)

#some data types have the same names, but the parameters for max and min sizes depend on the variant.
#we can use the biggest max and the smallest min for them,
#but this may allow some invalid values to slip in (without accounting for the variant)
#the good news is time it right in the validator and we will have easy access to the vairiant type.
#but this should still be set in some sort of config.
#no idea how to use something else other than a db saved in sqllite on the computer at the moment.
#perhaps the CURSOR class documentation or some research will provide some answers on that.
#
#we can make sure that the type is on a given list of names for valid types
#we can make sure that the value initially looks valid independently of the variant
#then once we take into account the variant, then we can do further validation on the size
#
#for example: varchar, varchar(n), varchar(max)
#varchar is not the same as varchar(max) which is not the same as varchar(n)
#I guess I could make the varchar default to varchar(max), but again this depends on the variant.

#these two lines will be printed on the same line
#print("this is part ", end="");
#print("of the sentence!");
#other print statements will be on their own lines unless end=""
