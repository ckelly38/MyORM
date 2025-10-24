# MyORM
a new ORM comparable or maybe even precursor to SQLAlchemy.

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
