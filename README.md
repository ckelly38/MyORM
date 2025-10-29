# MyORM
a new ORM comparable or maybe even a precursor to SQLAlchemy.

## Test File Generator
after getting myorm, there is a testfilegenerator.py that is included. This file can be used to generate a setup or seed script so you can start executing it.
You will need the following command:

python -m myorm.testfilegenerator newfilenameandpathtoit configmodulename dbrefnmor0
python -m myorm.testfilegenerator
python -m myorm.testfilegenerator [-nodb, --nodb, 0]

A WORD OF WARNING: IF THE FILE ALREADY EXISTS, IT WILL BE OVERWRITTEN!
YOU WILL LOSE EVERYTHING IN THAT FILE!
DISCLAIMER:
I, AS THE PROGRAMMER OF MYORM, I, WILL NOT BE RESPONSIBLE FOR LOST DATA DUE TO USER ERROR. SO USE CAUTION.

NOTE if you choose to provide no arguments after calling the script all defaults will be used.
It will create the test file with whatever the default file name is with the .py extension
and it will have a default config module name,
and it will have a default DB ref name (you will be using the DB).

NOTE if you choose to provide 1 argument it must be one of the following: -nodb, --nodb, or 0
In this case that command will look like: python -m myorm.testfilegenerator --nodb
It will create the test file with whatever the default file name is with the .py extension
and it will have a default config module name,
and it will not be using the DB and will not provide a DB ref name.

IF YOU DO NOT LIKE THE DEFAULT NAMES PROVIDED, YOU CAN USE FIND AND REPLACE ALL ON THE FILE OR
USE THE MAIN COMMAND TO CALL THE GENERATOR WITH ALL 3 ARGUMENTS:

1. The new file name and relative path to it (no extension because that will be given to you).
2. The config module or file name again no extension just the name.
3. This is the name of the database DB object that holds the ref in the config file. This is important because the setup script that gets run once you run this file will setup the myorm so it can be used.
If you do not want to have a DB object ref, just provide a 0 here.

The generator will generate a file like this YOU CAN COPY THIS DIRECTLY:

import config;
from myorm.myvalidator import myvalidator;
from myorm.mycol import mycol;
mycol.setUpMyColDBRefAndConfigModule(config);#covers parts a, b, and c
from myorm.mybase import mybase;
#import all of your DB model classes here before you set them up on the next line
mybase.setupMain();

OR

import config;
from myorm.myvalidator import myvalidator;
from myorm.mycol import mycol;
myvalidator.setupConfigModule(config);#setup part a
tmpdbref = myvalidator.getDBAttrOrValFromConfigModuleNoVars(config, True);#setup part b
mycol.setMyDBRef(tmpdbref);#setup part c
from myorm.mybase import mybase;
#import all of your DB model classes here before you set them up on the next line
mybase.setupMain();
CURSOR = tmpdbref.getCursor();
CONN = tmpdbref.getConn();
SQLVARIANT = tmpdbref.getSQLType();

OF COURSE YOU EXECUTE THAT GENERATED STARTUP FILE AS YOU WOULD ANY OTHER PYTHON FILE WITH:
python filename.py

ONE OTHER THING, YOU CANNOT EXECUTE IT DIRECTLY WITHOUT HAVING MODEL FILES...
THAT IS TO SAY THAT IF THERE ARE NO MODEL DB CLASSES,
THEN THERE IS A CHANCE SOME OF THE METHODS WILL NOT RUN OR WILL ERROR OUT
PROBABLY DUE TO A MISSING TABLE NAME.


## Models File Generator
after getting myorm, there is a modelsgenerator.py that is included. This file can be used to generate
the database models file where your models classes are kept.
We often call this models.py file. As usual for every model class it will require a few things:
1. that it extends the mybase class.
2. that it has a tablename
3. that it has a multiargs variable to hold the multicolumn args
4. that it has database columns that extend the mycol class
5. you may also have reference columns that hold a list of objects (the foreign key cols will hold the object references or at least be able for my program to create this for you on setup)
6. that it has validators for the columns and it could have multicolumn validators.
7. you may also have a representation method though my program provides a few options for this as well as the to_dict method. Though it is best to not override these unless you follow what I have set out for doing so.

WHAT THE GENERATOR DOES:

Aside from the cols and other unknown variables specific to the class, the models file generator is able
to provide a sample single col validator a sample multicol validator, a place for the tablename and multiargs variable, a placehold for the cols, and a sample override for repr and to_dict because these are mostly boilerplait code anyways.

TO AVOID THE OVERWRITE PROBLEM, ALWAYS USE APPEND MODE.

A WORD OF WARNING: IF THE FILE ALREADY EXISTS, AND YOU CALL IT IN WRITE MODE OR OVERWRITE MODE, IT WILL BE OVERWRITTEN!
YOU WILL LOSE EVERYTHING IN THAT FILE!
DISCLAIMER:
I, AS THE PROGRAMMER OF MYORM, I, WILL NOT BE RESPONSIBLE FOR LOST DATA DUE TO USER ERROR. SO USE CAUTION.

FILE WRITING MODES: YOU ARE ALLOWED TO OPEN THE FILE IF IT EXISTS, IN WRITE, OR APPEND MODES.
The mode you provide to the program tells the program what mode to use if the file already exists.
If you pass it anything other than the approved append or overwrite options, then it will open it in block mode (block mode if the file exists, you are not allowed to write and it will crash) or error out.

Your models classes should look something like this:

from myorm.mybase import mybase;
from myorm.mycol import mycol;
from myorm.myvalidator import myvalidator;
from myorm.myrefcol import myrefcol;
validates = mycol.validates;
mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN*, ERROR, or DISABLED.

now we need a list of the class names
so we can do class classname(mybase):
each class needs tablename=None, spot for multiargs mymulticolargs=None, #tableargs=None;
may also have to_dict, repr, and validator methods

each class will look something like:
imports here at the top of the file only once needed for all classes
class classname(mybase):
    tablename = None;

    #cols here

    mymultiargs = None;#needs to be near cols
    #tableargs = None;#needs to be near cols

    #everything below this point is optional

    #validator example methods (often a lot of these and they need to be near cols)

    #params comment for to_dict and repr
    #repr def
    
    #todict def

need to get the class names from the user on the command line
need to know if they just want to add class names only to an existing file or create a new one (default).

YOU CAN CALL THE MODELS FILE GENERATOR LIKE SO:

we want the options to tell it to include:
validatorsonly, repronly, todictonly, or bothreprandtodict or allthreeoptions
-allopts, -all, -bothbutnovalidators, -repr, -todict, -validators, -reprandv, -todictandv

append options = [-addonly, -add, -a, -append, -appendonly, 1];
overwrite options = [-overwrite, -writeover, -ow, -write, -w, 0];
classlist options = [-cl, -classlist, -models, -mdls];
these are not all of them

python -m myorm.modelsgenerator newfilename [appendopts] classnameslist [optionslist]
python -m myorm.modelsgenerator newfilename [overwriteopts] classnameslist [optionslist]
python -m myorm.modelsgenerator newfilename classnameslist [optionslist]
python -m myorm.modelsgenerator [appendopts] classnameslist [optionslist]
python -m myorm.modelsgenerator [overwriteopts] classnameslist [optionslist]
python -m myorm.modelsgenerator [classlistopts] classnameslist [optionslist]

on the one only with the class list either create a new file or block.

IF YOU DO NOT PROVIDE THE OPTIONS LIST, THEN YOU CAN GET A FILE ONLY WITH THE REQUIRED STUFF.

THERE IS CURRENTLY NO WAY TO HAVE NO OPTIONS ON ONE CLASS, BUT HAVE OPTIONS ON OTHERS.
BUT A BYPASS EXISTS, THE APPEND MODE FOR THE FILE CAN BE USED TO GENERATE A MODELS CLASS WITH NO OPTIONS.

WARNING AND DISCLAIMER:
BUT IF YOU ACCIDENTLY OPEN IT IN WRITE OR OVERWRITE MODE TO DO THIS, YOU WILL LOSE EVERYTHING IN THAT FILE. I WILL NOT BE HELD RESPONSIBLE FOR THAT.

TO AVOID THE OVERWRITE PROBLEM, ALWAYS USE APPEND MODE.
