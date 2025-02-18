from init import CURSOR, CONN;
from models import mycol;
from mycol import myvalidator;
from models import MyTestColsClass;
from models import MyOtherTestClass;
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
