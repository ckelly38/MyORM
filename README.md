# MyORM
a new ORM comparable or maybe even a precursor to SQLAlchemy.

## Setup Before Running
As with most ORM libraries like SQLAlchemy, you need to have your DB model classes setup before you can use the ORM or even execute SQL Code for the most part.
This program is no different. To speed setup up I have provided some startup file generators for you to use.

You have a couple of options for setup.
* OPTION A (recommended as this is the easiest):
    1. Run the Config File Generator,
    2. Run the Master Generator.
* OPTION B:
    1. Run the Models File Generator,
    2. Run the Test File Generator,
    3. Run the Class List Startup Generator.

### OVERWRITE WARNING AND DISCLAIMER:
But use caution as **once you have built a huge program and then attempt to make changes using these generators, you may risk overwriting and losing everything. I will not be responsible for lost data due to user error.** So use caution.

### DB Config.py File SETUP:
IMPORTANT NOTE: IF YOUR config.py FILE DOES NOT EXIST or whatever you used for the config module name DOES NOT EXIST, THEN THE TEST FILE WILL NOT RUN.

UNFORTUNATELY, THIS FILE IS HIGHLY VARIABLE DUE TO YOU AS THE USER NEEDING TO PROVIDE:
* THE LIBRARY THIS ORM LIBRARY WILL BE USING.
* A CURSOR AND A WAY TO EXECUTE SQL COMMANDS.
* AN SQL TYPE AND IT MUST BE ONE OF THE SUPPORTED TYPES OTHERWISE IT MAY NOT WORK.
* A MYDB OBJECT CREATED AND INITIALIED. YOUR TEST FILE REFERS TO THIS.

A SAMPLE CONFIG.py file (IE: The DB Config File) looks like this (YOU CAN COPY THIS DIRECTLY):
```
import sqlite3;
from myorm.MyDB import MyDB;
mydb = MyDB.newDBFromNameAndLib("swimleague", sqlite3, "LITE");
print(f"mydb.SQLVARIANT = {mydb.SQLVARIANT}");
```
THE MYDB CLASS HAS THE FOLLOWING CONSTRUCTOR:
```
def__init__(self, mydbname=None, mylibref=None, mysqlvar=None, myconn=None, mycursor=None):
```
This takes in the:
* DB name (mydbname).
* DB library ref (mylibref).
* SQL Variant Type (mysqlvar) like LITE.
* Connection object (myconn).
* Cursor object (mycursor).

The newDBFromNameAndLib static factory method takes in the following
```
MyDB.newDBFromNameAndLib(mydbname, mylibref, mysqlvar);
```
It will create a connection by adding .db to mydbname calling the **connect** method of the library that was given, then it passes that in to the MyDB constructor.

From there it will get the cursor by calling the **cursor** method of the library that was given,
then it passes that in to the MyDB constructor.


## Config File Generator
this generates a generators config file that the master generator then uses to call the other generators.

The config file generator generates a config file that looks like this YOU CAN COPY THIS DIRECTLY:
```
testfile_new_file_name: mystartupscript
testfile_write_mode: b
usedefaultconfigmodulename: false
usenodb: false
usedefaultdbobjname: false
configmodulename: config
dbobjname: mytmpdbobjref

modelsfile_new_file_name: mytempmodels
modelsfile_write_mode: a
models_class_list:
classnamea, tablenamea: -all
classnameb, tablenameb: -validators
classnamec, tablenamec: -repr
classnamed, tablenamed: -to_dict
classnamee, tablenamee: None
```
It can be called whatever you want for the most part, but it will need to have the .txt extension.

**DO NOT CHANGE THE KEY NAMES IN THE FILE!**
IF YOU DO THE MASTER GENERATOR WILL NOT BE ABLE TO USE THAT FILE!


EXECUTE THE CONFIG FILE GENERATOR AS FOLLOWS:
You can call the config file generator as follows (pick one of them):
```
python -m myorm.configfilegenerator filename -notstwmd -nomdlswmd -nodb -usedfltcnfgnm -usedfltdbnm
python -m myorm.configfilegenerator filename ?
python -m myorm.configfilegenerator filename
python -m myorm.configfilegenerator
```

WHAT IT NEEDS:
1. a filename and the path to it like genconfig the .txt extension will automatically be used (so do not include it).
THE FILENAME IS OPTIONAL. A DEFAULT WILL BE USED IF NOT PROVIDED, BUT IT IS REQUIRED IF YOU WANT TO PROVIDE OTHER OPTIONS.
2. Some other options otherwise defaults will be used. These options can be in any order.
Your options that you have are:
    * A: -no test write mode (-notstwmd) specified which does what it says it does not include the testfile_write_mode: line at all in the config file.
    * B: -no models write mode (-nomdlswmd) specified which does what it says it does not include the modelsfile_write_mode: line at all in the config file.
    * C: -no database references (-nodb) specified meaning there are no DB references in the config file
this also means options like: usedefaultdbobjname and dbobjname will not be present in the config file
this option in particular trumps others if there is a contradiction.
    * D: -use default config name (-usedfltcnfgnm) specified meaning that the default config module name will be used instead of you having to provide it. It also means that the configmodulename option line will not be present in the config file.
It also means that the configmodule name will be the default in the test file generator.
    * E: -use default database reference name (-usedfltdbnm) specified meaning the program uses a default DB name in the test file generator.


DEFAULTS:
All of those flags in 2 are optional. Meaning if you do not provide them then defaults will be used to generate the config file.
The config file defaults are set such that:
* a testfile write mode will be provided (block),
* a models file write mode will be provided (append),
* a DB name will be provided but it will be a placeholder name just like for the file names,
* a config module name will be provided but it will be a placeholder name just like for the file names.


### EDIT THE CONFIG FILE BEFORE RUNNING THE MASTER GENERATOR:
You will need to modify these before you can run the Master Generator with it otherwise it will cause some conflicts.


A NOTE ABOUT DB MODEL CLASSES AND OPTIONS:
The config file will not have all of the DB Model Class nor tablenames only filler names and options have been provided.

* The -all option provides sample validators, a repr, and a to_dict method
* The -validators option provides just sample validators
* The -repr option provides just the repr method
* The -to_dict option provides just the to_dict method
* The None option does not provide any of that.
* You can have other options for the model classes.
That combine validators and repr, or validators and to_dict, or just repr and to_dict

The program lists a list of options for you (SEE THE MODELS GENERATOR TO GET AN IDEA).

### Once all of those options are the way you want them:
SAVE the generators config file, and then run the Master Generator.

WARNING:
**DO NOT CHANGE THE KEY NAMES IN THE GENERATORS CONFIG FILE!**
IF YOU DO, THE MASTER GENERATOR WILL NOT BE ABLE TO USE THAT FILE!
SO ONLY CHANGE THE VALUES.


## Master Generator
this take the config file that the Config File Generator made and then executes it.

The config file is not the DB config file (this is provided by the user, which has the libraries imported and the MyDB object created).

The config file that the Master Generator needs is actually a **generators config file.** The generators config file tells the Master Generator how to call the other generators and executes them in a combined order.

EXECUTE THE MASTER GENERATOR AS FOLLOWS:
you can call the program as follows (pick one):
```
python -m myorm.mastergenerator configfilename -tst wtmd -mdls wtmd
python -m myorm.mastergenerator configfilename -mdls wtmd -tst wtmd
python -m myorm.mastergenerator configfilename -tst wtmd
python -m myorm.mastergenerator configfilename -mdls wtmd
python -m myorm.mastergenerator configfilename
```
The only thing that is required on the Master Generator is the generators config filename.
That is the config file that was generated by the Config File Generator.
This filename only needs to be the filename and relative path to it. NO EXTENSION.
THE .txt EXTENSION WILL AUTOMATICALLY BE USED.

THE OTHER OPTIONS:
* -tst is for TEST FILE and this lets you override the write mode given for the test file in the config file.
wtmd is the write mode value or flag.
* -mdls is for MODELS FILE and this lets you override the write mode given for the models file in the config file.

You can specify one or the other or both.

Whichever one you do not speficify, if you do not specify one, the mode in the config file will be used.

If it is not valid, then **block** mode will be used.

SEE **THE MODELS FILE GENERATOR** ON A DESCRIPTION FOR A LIST OF THE OPTIONS.


YOU ARE ALL DONE WITH SETUP NOW EXCEPT FOR ONE THING:

THE MASTER GENERATOR WILL MAKE THE TEST OR STARTUP FILE, AND IT WILL MAKE A MODELS FILE FOR YOU. IT WILL PROVIDE ALL OF THE BOILERPLATE CODE THAT YOU NEED. JUST LIKE THE OTHER GENERATORS DO.

AFTER THIS GENERATOR RUNS, THE TEST OR STARTUP FILE WILL BE READY TO BE EXECUTED. **WELL NOT QUITE SEE THE IMPORTANT NOTE IN THE INITIAL SETUP SECTION ABOUT THE config.py FILE.**

IMPORTANT NOTE: IF YOUR config.py FILE DOES NOT EXIST or whatever you used for the config module name
DOES NOT EXIST, THEN SEE **THE DB Config.py File SETUP** SECTION.

### OVERWRITE WARNINGS AND ADDTIONAL MODIFICATIONS:
YOU CAN STILL USE THE MODELS FILE GENERATOR TO **APPEND** NEW CLASSES TO THE MODELS FILE.

YOU COULD ALSO MODIFY THE GENERATORS CONFIG FILE AND REXECUTE **THE MASTER GENERATOR,** BUT BE WARNED **THIS WILL GET RID OF CODE YOU ADDED IN YOURSELF** THAT THE GENERATORS DID NOT.


## Models File Generator
after getting myorm, there is a modelsgenerator.py that is included. This file can be used to generate the database models file where your models classes are kept. We often call this models.py file.

As usual for every model class it will require a few things:
1. that it extends the mybase class.
2. that it has a tablename
3. that it has a multiargs variable to hold the multicolumn args
4. that it has database columns that extend the mycol class
5. you may also have reference columns that hold a list of objects (the foreign key cols will hold the object references or at least be able for my program to create this for you on setup)
6. that it has validators for the columns and it could have multicolumn validators.
7. you may also have a representation method though my program provides a few options for this as well as the to_dict method. Though it is best to not override these unless you follow what I have set out for doing so.

WHAT THE GENERATOR DOES:

Aside from the cols and other unknown variables specific to the class, the models file generator is able to provide:
* a sample single col validator,
* a sample multicol validator,
* a place for the tablename and multiargs variable,
* a placeholder comment for the cols,
* and a sample override for repr and to_dict because these are mostly boilerplate code anyways.

### FILE OVERWRITE WARNING AND DISCLAIMER AND FILE WRITING MODES:
TO AVOID THE OVERWRITE PROBLEM, ALWAYS USE **APPEND** MODE.

**A WORD OF WARNING:
IF THE FILE ALREADY EXISTS, AND YOU CALL IT IN WRITE MODE OR OVERWRITE MODE, IT WILL BE OVERWRITTEN! YOU WILL LOSE EVERYTHING IN THAT FILE!**

**DISCLAIMER:
I, AS THE PROGRAMMER OF MYORM, I, WILL NOT BE RESPONSIBLE FOR LOST DATA DUE TO USER ERROR. SO USE CAUTION.**

FILE WRITING MODES:
YOU ARE ALLOWED TO OPEN THE FILE IF IT EXISTS, IN:
* WRITE, OR
* APPEND, OR
* BLOCK MODES.

The mode you provide to the program tells the program what mode to use **if the file already exists.**
If you pass it anything other than the approved **append** or **overwrite/write** options, then it will open it in **block** mode (in block mode if the file exists, you are not allowed to write and it will crash) or error out.
* **Append** mode will add stuff to the end of the file if it already exists.
* **Write/OverWrite** mode will overwrite the entire file if it already exists starting at the top working its way down.
* **IF THE FILE DOES NOT EXIST**, THEN WRITE/OVERWRITE MODE IS AUTOMATICALLY USED REGARDLESS OF YOUR CHOICE HERE. YOUR CHOICE IS WHAT TO DO IF THE FILE ARLEADY EXISTS!

### WHAT THE models.py FILE LOOKS LIKE:
Your models classes should look something like this YOU CAN COPY THIS DIRECTLY:
```
from myorm.mybase import mybase;
from myorm.mycol import mycol;
from myorm.myvalidator import myvalidator;
from myorm.myrefcol import myrefcol;
validates = mycol.validates;
mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN*, ERROR, or DISABLED.
```
now we need a list of the class names
so we can do class classname(mybase):
each class needs tablename=None, spot for multiargs mymulticolargs=None, #tableargs=None;
may also have to_dict, repr, and validator methods

each class will look something like:
```
#imports here at the top of the file only once needed for all classes
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
```
need to get the class names from the user on the command line
need to know if they just want to add class names only to an existing file or create a new one (default).

### HOW TO CALL THE MODELS FILE GENERATOR:
YOU CAN CALL THE MODELS FILE GENERATOR LIKE SO:

we want the options to tell it to include:
validatorsonly, repronly, todictonly, or bothreprandtodict or allthreeoptions
-allopts, -all, -bothbutnovalidators, -repr, -todict, -validators, -reprandv, -todictandv

append options = [-addonly, -add, -a, -append, -appendonly, 1];
overwrite options = [-overwrite, -writeover, -ow, -write, -w, 0];
classlist options = [-cl, -classlist, -models, -mdls];
these are not all of them
```
python -m myorm.modelsgenerator newfilename appendopts classnameslist optionslist
python -m myorm.modelsgenerator newfilename overwriteopts classnameslist optionslist
python -m myorm.modelsgenerator newfilename classnameslist optionslist
python -m myorm.modelsgenerator appendopts classnameslist optionslist
python -m myorm.modelsgenerator overwriteopts classnameslist optionslist
python -m myorm.modelsgenerator classlistopts classnameslist optionslist
```
on the one only with the class list either create a new file or block.

IF YOU DO NOT PROVIDE THE OPTIONS LIST, THEN YOU CAN GET A FILE ONLY WITH THE REQUIRED STUFF.

* THERE IS CURRENTLY **NO WAY TO HAVE NO OPTIONS ON ONE CLASS, BUT HAVE OPTIONS ON OTHERS.** YOU CANNOT PICK AND CHOOSE WITH THIS.
* YOU DO HOWEVER HAVE THE ABILITY TO **NOT PROVIDE AN OPTIONSLIST AT ALL**, BUT IF YOU DO NOT PROVIDE AN OPTIONSLIST, **THEN FOR ALL OF THOSE CLASSES NO OPTIONS WILL BE USED.** YOU CANNOT PICK AND CHOOSE WITH THIS.
* THE MASTER GENERATOR ACCEPTS NONE OPTION AS AN OPTION FOR THESE ON THE GENERATORS CONFIG FILE. YOU ARE STRONGLY ENCOURAGED TO USE THE MASTER GENERATOR.
* BUT A BYPASS EXISTS, THE **APPEND** MODE FOR THE FILE CAN BE USED TO GENERATE (A) DB MODEL CLASS(ES) WITH NO OPTIONS. FROM THERE YOU CAN REARRANGE SAID CLASSES IN A DIFFERENT EDITOR.

### OVERWRITE WARNING AND DISCLAIMER:
TO AVOID THE OVERWRITE PROBLEM, ALWAYS USE **APPEND** MODE.

WARNING AND DISCLAIMER:
BUT IF YOU ACCIDENTLY OPEN IT IN **WRITE/OVERWRITE** MODE TO DO THIS, **YOU WILL LOSE EVERYTHING IN THAT FILE**. I WILL NOT BE HELD RESPONSIBLE FOR USER ERROR.


## Test File Generator
after getting myorm, there is a testfilegenerator.py that is included. This file can be used to generate a setup or seed script so you can start executing it.

nodbopts = [-nodb, --nodb, 0]

You will need the following command:
```
python -m myorm.testfilegenerator newfilenameandpathtoit configmodulename dbrefnmor0
python -m myorm.testfilegenerator nodbopts
python -m myorm.testfilegenerator
```

### OVERWRITE WARNING AND DISCLAIMER:
A WORD OF WARNING: **IF THE FILE ALREADY EXISTS, IT WILL BE OVERWRITTEN!
YOU WILL LOSE EVERYTHING IN THAT FILE!**
**DISCLAIMER:
I, AS THE PROGRAMMER OF MYORM, I, WILL NOT BE RESPONSIBLE FOR LOST DATA DUE TO USER ERROR.** SO USE CAUTION.

### Your options how you call it:
* OPTION A: NO ARGUMENTS:
    * NOTE if you choose to provide no arguments after calling the script all defaults will be used.
    * It will create the test file with whatever the default file name is with the .py extension
    * and it will have a default config module name,
    * and it will have a default DB ref name (you will be using the DB).

* OPTION B: NODB (1) ARGUMENT:
    * NOTE if you choose to provide 1 argument it must be one of the following:
    * -nodb, --nodb, or 0

    * In this case, that command will look like:
    ```
    python -m myorm.testfilegenerator --nodb
    ```
    
    * It will create the test file with whatever the default file name is with the .py extension
    * and it will have a default config module name,
    * and it will not be using the DB and will not provide a DB ref name.

* OPTION C: THE MAIN COMMAND: 
* IF YOU DO NOT LIKE THE DEFAULT NAMES PROVIDED, YOU CAN USE FIND AND REPLACE ALL ON THE FILE OR
USE THE MAIN COMMAND TO CALL THE GENERATOR WITH ALL 3 ARGUMENTS:

    1. The new file name and relative path to it (no extension because that will be given to you).
    2. The config module or file name again no extension just the name.
    3. This is the name of the database DB object that holds the ref in the config file. This is important because the setup script that gets run once you run this file will setup the myorm so it can be used.
    If you do not want to have a DB object ref, just provide a 0 here.

### WHAT THE GENERATED FILE LOOKS LIKE:
The generator will generate a file like this YOU CAN COPY THIS DIRECTLY:
```
import config;
from myorm.myvalidator import myvalidator;
from myorm.mycol import mycol;
mycol.setUpMyColDBRefAndConfigModule(config);#covers parts a, b, and c
from myorm.mybase import mybase;
#import all of your DB model classes here before you set them up on the next line
mybase.setupMain();
```
OR
```
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
```

### EXECUTING THE TEST FILE:
OF COURSE YOU EXECUTE THAT GENERATED STARTUP FILE AS YOU WOULD ANY OTHER PYTHON FILE WITH:
```
python filename.py
```
* ONE OTHER THING, YOU CANNOT EXECUTE IT DIRECTLY WITHOUT HAVING **MODEL FILES...**
* THAT IS TO SAY THAT IF THERE ARE **NO MODEL DB CLASSES**,
THEN THERE IS A CHANCE **SOME OF THE METHODS WILL NOT RUN OR WILL ERROR OUT** PROBABLY DUE TO A **MISSING TABLENAME**.

**WELL NOT QUITE SEE THE IMPORTANT NOTE IN THE INITIAL SETUP SECTION ABOUT THE config.py FILE.**

IMPORTANT NOTE: IF YOUR config.py FILE DOES NOT EXIST or whatever you used for the config module name
DOES NOT EXIST, THEN SEE **THE DB Config.py File SETUP** SECTION.


## Class List Startup Generator
after running the test or startup or seed file generator, you will have noticed that there is a line on that file that says:

```
#import all of your DB model classes here before you set them up on the next line
```

the idea with the class list startup generator is that **it finds the line like this and replaces it with the model class import lines.** Like 
```
from models import myclassnamea; ...
```
for each of the classes for example. Only it is more like:
```
from models import myclassnamea;
from otherfile import myotherclassnamea;
...
```
for each of the classes on each of the files.

### EXECUTION ORDER MATTERS:
This Class List Generator is obviously intended to be run **after the Models Generator and after the Test File Generator has run.**
**IF you run it before the Test File Generator has generated that file, it will not work at all.**

You can run it before the Models File Generator, **the only thing that it needs are the file names and the class names. It does not need the actual files to exist**, so the Models File Generator does not need to actually have been run.

However, if the Models File Generator has not been run yet and you run this after running the Test File Generator, and then **try to execute that newly modified test file, the test file will not run because the
models files and classes do not exist yet.**

**WELL NOT QUITE SEE THE IMPORTANT NOTE IN THE INITIAL SETUP SECTION ABOUT THE config.py FILE.**

IMPORTANT NOTE: IF YOUR config.py FILE DOES NOT EXIST or whatever you used for the config module name
DOES NOT EXIST, THEN SEE **THE DB Config.py File SETUP** SECTION.

### OVERWRITE WARNING AND DISCLAIMER:
OVERWRITE WARNING:
**It obviously OVERWRITES and saves that given test file, so be careful.**

A WORD OF WARNING: **IF THE FILE ALREADY EXISTS, AND YOU CALL IT IN WRITE/OVERWRITE MODE, IT WILL BE OVERWRITTEN!
YOU WILL LOSE EVERYTHING IN THAT FILE!**

DISCLAIMER:
I, AS THE PROGRAMMER OF MYORM, **I, WILL NOT BE RESPONSIBLE FOR LOST DATA DUE TO USER ERROR.** SO USE CAUTION.

### YOU CAN CALL THE CLASS LIST STARTUP GENERATOR AS FOLLOWS:
You can call the program as follows:
```
python -m myorm.addclasslisttotestfile testfile searchstrorflgorindex classlistflags classlist filenameflags fnms
python -m myorm.addclasslisttotestfile testfile classlistflags classlist filenameflags fnms
```
It needs:
1. the testfile name and relative path to it no extension.
2. the search string or line index (file line number - 1) to replace. SO DO NOT GET THIS WRONG. IF THE NUMBER IS CORRECT, YOU MIGHT ACCIDENTALLY OVERWRITE A LINE YOU NEEDED, SO BE CAREFUL.
Ideally this string is inside of "" properly escaped.
3. the indicator that you are begining the class list next.
4. the list of class names each separated by a space.
5. the indicator that you are begining the file list next.
6. the list of file names each separated by a space.

NOTE: 2. is optional, it will search for the default string that the test file generated added if you
do not provide this.

After this generator runs, the test or startup or seed file will be ready to be executed.

**WELL NOT QUITE SEE THE IMPORTANT NOTE IN THE INITIAL SETUP SECTION ABOUT THE config.py FILE.**

IMPORTANT NOTE: IF YOUR config.py FILE DOES NOT EXIST or whatever you used for the config module name
DOES NOT EXIST, THEN SEE **THE DB Config.py File SETUP** SECTION.
