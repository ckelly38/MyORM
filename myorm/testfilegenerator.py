#the test file needs to have a few lines of code to launch myorm
#from myorm.myvalidator import myvalidator;#setup line required
#import ?;
#from myorm.mycol import mycol;
#mycol.setUpMyColDBRefAndConfigModule(?);#covers a b and c
#myvalidator.setupConfigModule(?);#setup line required part a
#tmpdbobj = myvalidator.getDBAttrOrValFromConfigModuleNoVars(?, True);#setup line required part b
#mycol.setMyDBRef(tmpdbobj);#setup line required part c
#all other model class imports required now
#from myorm.mybase import mybase;#setup line required
#where your DB model classes are imported here they must be imported before the next line
#mybase.setupMain();#setup line required

from myorm.myvalidator import myvalidator;
from myorm.mybase import mybase;
import sys;
import traceback;
mydfconfigmnm = "configmodulenm";
mydfdbobjrefnm = "tmpdbobj";
mydfscriptnm = "mystartupscript.py";
def genFileLines(confgnm="" + mydfconfigmnm, dbrefnm="" + mydfdbobjrefnm, usenodb=False):
    myvalidator.varmustbeboolean(usenodb, "usenodb");
    errmsgptb = ") must be alpha numeric, but it was not!";
    if (confgnm.isidentifier()): pass;
    else: raise ValueError("the config module name string (" + str(confgnm) + errmsgptb);
    if (dbrefnm.isidentifier()): pass;
    else: raise ValueError("the database object ref name string (" + str(dbrefnm) + errmsgptb); 
    ilinea = "import " + confgnm + ";";
    ilineb = "from myorm.myvalidator import myvalidator;";
    ilinec = "from myorm.mycol import mycol;";
    ilined = "mycol.setUpMyColDBRefAndConfigModule(" + confgnm + ");#covers parts a, b, and c";
    ilinee = "myvalidator.setupConfigModule(" + confgnm + ");#setup part a";
    ilinef = "" + dbrefnm + " = myvalidator.getDBAttrOrValFromConfigModuleNoVars(" + confgnm;
    ilinef += ", True);#setup part b";
    ilineg = "mycol.setMyDBRef(" + dbrefnm + ");#setup part c";
    ilineh = "from myorm.mybase import mybase;";
    ilinei = "#import all of your DB model classes here before you set them up on the next line";
    ilinej = "mybase.setupMain();";
    ilinek = "CURSOR = " + dbrefnm + ".getCursor();";
    ilinel = "CONN = " + dbrefnm + ".getConn();";
    ilinem = "SQLVARIANT = " + dbrefnm + ".getSQLType();";
    mflinesva = [ilinea, ilineb, ilinec, ilined, ilineh, ilinei, ilinej];#no db
    mflinesvb = [ilinea, ilineb, ilinec, ilinee, ilinef, ilineg, ilineh, ilinei, ilinej,
                ilinek, ilinel, ilinem];#with db
    return (mflinesva if usenodb else mflinesvb);

#need to know what to call the new file and which version the user wants with db or not
#https://www.geeksforgeeks.org/python/command-line-arguments-in-python/
#execute it with python -m myorm.testfilegenerator newfilenameandpathtoit configmodulename dbrefnmor0
#execute it with python -m myorm.testfilegenerator
#execute it with python -m myorm.testfilegenerator [-nodb, --nodb, 0]
if __name__ == "__main__":
    #print(f"Total Arguments: {len(sys.argv)}");
    #print(sys.argv[0]);
    #print(sys.argv[1:]);
    #print("the rest of the script!");
    
    #the script we executed is index 0
    #first one is the file name (index 1)
    #second one is the config module name (index 2)
    #third one is either the usenodb value 0 or 1 or the dbname
    #if we give a dbobjrefnm then we are using a db
    merrmsg = "invalid number of arguments! You must have 3 arguments not including the script you ";
    merrmsg += "are executing.\nThey must be as follows:\n1. the new file name (no extension) and ";
    merrmsg += "relative path to it,\n2. the config file/module name,\n3. the db ref object name or a ";
    merrmsg += "0 to indicate not using a db!\n\nAlternatively: ";
    warnmsgapta = "since no arguments were provided, it will use the following:\n";
    warnmsgaptb = "1. the current directory where this command was run and the file will be called ";
    warnmsgaptb += "'" + mydfscriptnm + "'.\n2. the config module name will be: '" + mydfconfigmnm;
    warnmsgaptb += "'.\n";
    warnmsgaptc = "3. the database DB object reference name will be: '" + mydfdbobjrefnm;
    warnmsgaptc += "'. And we will be using the DB.";
    nodboptsstr = "-nodb or --nodb or 0";
    nodboptsprvdstr = "provided and it matches " + nodboptsstr + ", it will use the following:\n";
    warnmsgbpta = "since one argument was " + nodboptsprvdstr;
    warnmsgbptc = "3. No DB or no database ref will be provided because of the " + nodboptsstr;
    warnmsgbptc += "option.";
    merrmsg += "if no arguments are provided, it will use the following:\n" + warnmsgaptb + warnmsgaptc;
    merrmsg += "\n\nAlternatively: if one argument is " + nodboptsprvdstr + warnmsgaptb + warnmsgbptc;
    if (len(sys.argv) == 4):
        tmpdbrefornum = sys.argv[3];
        myusenodb = (tmpdbrefornum == '0');
        mydbrefnm = ("" + mydfdbobjrefnm if myusenodb else "" + tmpdbrefornum);
        mflines = None;
        try:
            mflines = genFileLines(confgnm="" + sys.argv[2], dbrefnm=mydbrefnm, usenodb=myusenodb);
        except Exception as ex:
            traceback.print_exc();
            raise ValueError(merrmsg);
        mybase.blockifmyfileexistswritelines(sys.argv[1] + ".py", mflines, dscptrmsg="test file script");
        print("TEST FILE GENERATED SUCCESSFULLY!");
    elif (len(sys.argv) == 1):
        print(warnmsgapta + warnmsgaptb + warnmsgaptc);
        mflines = genFileLines();
        mybase.blockifmyfileexistswritelines(mydfscriptnm, mflines, dscptrmsg="test file script");
        print("TEST FILE GENERATED SUCCESSFULLY!");
    elif (len(sys.argv) == 2 and sys.argv[1] in ["-nodb", "--nodb", "0"]):
        print(warnmsgbpta + warnmsgaptb + warnmsgbptc);
        mflines = genFileLines(confgnm="" + mydfconfigmnm, dbrefnm="" + mydfdbobjrefnm, usenodb=True);
        mybase.blockifmyfileexistswritelines(mydfscriptnm, mflines, dscptrmsg="test file script");
        print("TEST FILE GENERATED SUCCESSFULLY!");
    else: raise ValueError(merrmsg);
