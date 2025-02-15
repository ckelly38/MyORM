from init import CURSOR, CONN;
from mycol import mycol;

mynewcol = mycol(colname="mynewcol", datatype="Integer", value=1, defaultvalue=0,
                 isprimarykey=True, isforeignkey=False, isnonnull=True, isunique=True,
                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
print(mynewcol);

#myonewcol = mycol(colname="myonewcol", datatype="Integer", value=1, defaultvalue=0,
#                 isprimarykey=True, isforeignkey=False, isnonnull=False, isunique=False,
#                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
#errors out
#print(myonewcol);

#mybnewcol = mycol(colname="mybnewcol", datatype="Integer", value=1, defaultvalue=0,
#                 isprimarykey=True, isforeignkey=False, isnonnull=True, isunique=True,
#                 autoincrements=True, foreignClass=None, foreignColName=None, constraints=None);
#print(mybnewcol);