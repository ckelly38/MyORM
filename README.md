# MyORM
a new ORM comparable to SQLAlchemy.

## Test File Generator
after getting myorm, there is a testfilegenerator.py that is included. This file can be used to generate a setup or seed script so you can start executing it.
You will need the following command:

python -m myorm.testfilegenerator newfilenameandpathtoit configmodulename dbrefnmor0

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
