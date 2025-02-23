from init import CURSOR, CONN;
from models import mycol;
from mycol import myvalidator;
from models import MyTestColsClass;
from models import MyOtherTestClass;
from models import MyModelWithCompPrimaryKey;
from models import MyModelWithCompForeignKey;
#import sys;
#import inspect;

#print("");
#print("INSIDE OF TEST FILE!");
#print("list of system modules:");
#print(sys.modules[__name__]);
#print(inspect.getmembers(sys.modules[__name__], myvalidator.isClass));#list of tuples
#myclasses = [MyOtherTestClass, MyTestColsClass];
#mycol.setMyClassRefs(myclasses);
mycol.getMyClassRefsMain(True);#will force the fetch of the new list if it has changed by now

#print(mynewcol);
tstobj = MyTestColsClass();
print(tstobj.getMyCols());
print(tstobj.getTableName());
#print(tstobj.mynewcol.value);#error for the moment on this line not done with type enforcement...
#print(myvalidator.listMustContainUniqueValuesOnly(
#    ["colnamea", "colnameb", "colnamea"], "nonucolnames"));

tstobjb = MyOtherTestClass();
print(tstobjb.getMyCols());
print(tstobjb.getTableName());

#the question is how can we get it so the user does not have to create an init?
#if we assign the foreign key col name in the col constructor,
#we cannot validate it until later on, but will have access to it.
#if we assign the class string name, we can get the class reference from the globals() list later on.


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

tstobjc = MyModelWithCompPrimaryKey();
tstobjd = MyModelWithCompForeignKey();

print();
print("SQL GEN TESTS:");
print(myvalidator.genUniqueConstraint("constraintname", ["itema", "itemb", "itemc"]));
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
#WHAT I STILL NEED TO DO: 2-23-2025
#-ORDER BY, CREATE TABLE, INSERT INTO, UPDATE, DELETE, SELECT INTO, INSERT INTO SELECT
#-LEFT JOIN, RIGHT JOIN, INNER JOIN, FULL JOIN, NATURAL JOIN, UNIONS
#-OTHER STUFF LIKE: MAX(), MIN(), SUM(), AVG(), CURSTOM PROCEDURES, SWITCH CASES
#-figure out a way to let the user determine what to name the db
#-figure out how to integrate mysql/postgressql...
#-figure out a way to tell the program if using sqllite or sql and
#--if the commands are different from sql to sqllite how they change in the generator
#-figure out where to put the sql generator methods
#-figure out how to enforce the correct data types and the values that can be stored in them
#-ways to save data, ways to add new data, ways to remove data, ways to update the data,
#-and ways to remove tables
#-ways to print out objects via serialization
#-ways to back up the database

#these two lines will be printed on the same line
#print("this is part ", end="");
#print("of the sentence!");
#other print statements will be on their own lines unless end=""
