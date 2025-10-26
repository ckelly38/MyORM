slines = ["from myorm.mybase import mybase;", "from myorm.mycol import mycol;",
    "from myorm.myvalidator import myvalidator;", "from myorm.myrefcol import myrefcol;",
    "validates = mycol.validates;",
    "#mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN*, ERROR, or DISABLED."];
#now we need a list of the class names
#so we can do class classname(mybase):
#each class needs tablename=None, spot for multiargs mymulticolargs=None, #tableargs=None;
#need to get the class names from the user on the command line
#need to know if they just want to add class names only to an existing file or create a new one (default).
#python -m myorm.modelsgenerator newfilename [-addonly, -add, -a, -append, -appendonly, 1] classnameslist
#python -m myorm.modelsgenerator newfilename [-overwrite, -writeover, -ow, -write, -w] classnameslist
#python -m myorm.modelsgenerator newfilename classnameslist
#python -m myorm.modelsgenerator [-addonly, -add, -a, -append, -appendonly, 1] classnameslist
#python -m myorm.modelsgenerator [-overwrite, -writeover, -ow, -write, -w] classnameslist
#python -m myorm.modelsgenerator classnameslist
#on the one only with the class list either create a new file or block.
