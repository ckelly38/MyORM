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
tstobj = MyTestColsClass();#values of the cols must get past into the constructor...
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

tstobjc = MyModelWithCompPrimaryKey();
tstobjd = MyModelWithCompForeignKey();

print();
print(myvalidator.stringHasAtMaxNumChars("mystr", 0));#false
print(myvalidator.stringHasAtMinNumChars("mystr", 6));#false
print(myvalidator.stringHasAtMaxNumChars("mystr", 5));#true
print(myvalidator.stringHasAtMinNumChars("mystr", 2));#true
#print(myvalidator.stringMustHaveAtMaxNumChars("mystr", 0, "varnm"));#error
print(myvalidator.stringMustHaveAtMaxNumChars("mystr", 5, "varnm"));
#print(myvalidator.stringMustHaveAtMinNumChars("mystr", 6, "varnm"));#error
print(myvalidator.stringMustHaveAtMinNumChars("mystr", 2, "varnm"));
print("is value in range tests:");
print(myvalidator.isValueInRangeWithMaxAndMin(0, 1, 5));#false
print(myvalidator.isValueInRangeWithMaxAndMin(1, 1, 5));#true
print(myvalidator.isValueInRangeWithMaxAndMin(5, 1, 5));#true
print(myvalidator.isValueInRangeWithMaxAndMin(-5, 1, 5));#false
print(myvalidator.isValueInRangeWithMaxAndMin(2.5, 1, 5));#true
print();
print("lite = ", end="");
myvalidator.printSQLDataTypesInfoObj(myvalidator.getSQLDataTypesInfo('LITE'));
print();
print("mysql = ", end="");
myvalidator.printSQLDataTypesInfoObj(myvalidator.getSQLDataTypesInfo('MYSQL'));
print();
print("sqlserver = ", end="");
myvalidator.printSQLDataTypesInfoObj(myvalidator.getSQLDataTypesInfo('SQLSERVER'));
print();
print(myvalidator.isValidDataType("OTHER, VARCHAR(max)", "SQLSERVER"));#false
print(myvalidator.isValidDataType("VARCHAR(max), OTHER", "SQLSERVER"));#false
print(myvalidator.isValidDataType("NUMERIC(p, s)", "SQLSERVER"));#false
print(myvalidator.isValidDataType("VARCHAR(max)", "SQLSERVER"));#true
#need more tests for the isValidDataType method: one with valid numbers for the params, one without
#one with an invalid number of params too
raise ValueError("NEED TO CHECK THE RESULTS HERE...!");
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
#WHAT I STILL NEED TO DO: 2-25-2025
#-CREATE TABLE, INSERT INTO, UPDATE, DELETE, SELECT INTO, INSERT INTO SELECT
#-LEFT JOIN, RIGHT JOIN, INNER JOIN, FULL JOIN, NATURAL JOIN, UNIONS
#-figure out a way to let the user determine what to name the db
#-figure out how to integrate mysql/postgressql...
#-figure out a way to tell the program if using sqllite or sql and
#--if the commands are different from sql to sqllite (JOINS ARE) how they change in the generator
#-figure out where to put the sql generator methods
#-figure out how to enforce the correct data types and the values that can be stored in them (#1)
#-ways to save data, ways to add new data, ways to remove data, ways to update the data, (#2)
#-and ways to remove tables (#3)
#-ways to print out objects via serialization (#4)
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
