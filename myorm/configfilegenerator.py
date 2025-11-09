from myorm.myvalidator import myvalidator;
from myorm.mybase import mybase;
from myorm.modelsgenerator import getOptsFlagsDict;
import sys;

def getTrueFalseString(mval, tp="tf"):
    myvalidator.varmustbeboolean(mval, varnm="mval");
    if (myvalidator.isvaremptyornull(tp)): return getTrueFalseString(mval, tp="tf");
    if (tp == 'tf' or tp == 'TF'): return ("true" if mval else "false");
    elif (tp == 'yn' or tp == 'YN'): return ("yes" if mval else "no");
    elif (tp == '10' or tp == '10'): return ("1" if mval else "0");
    else: raise ValueError("invalid type was used here it must be tf, yn, or 10 only!");

def genFileLines(usetstwmd=True, usemdlswmd=True, nodb=False, usedfltcnfgnm=False, usedfltdbnm=False):
    myvalidator.varmustbeboolean(usetstwmd, varnm="usetstwmd");
    myvalidator.varmustbeboolean(usemdlswmd, varnm="usemdlswmd");
    myvalidator.varmustbeboolean(nodb, varnm="nodb");
    myvalidator.varmustbeboolean(usedfltcnfgnm, varnm="usedfltcnfgnm");
    myvalidator.varmustbeboolean(usedfltdbnm, varnm="usedfltdbnm");

    finusedfltdbnm = (True if nodb else usedfltdbnm);

    #the config file has the following lines
    tstgenlinea = "testfile_new_file_name: the_name_and_loc";
    tstgenlineab = "testfile_write_mode: b";#write mode is optional
    tstgenlineb = "usedefaultconfigmodulename: " + getTrueFalseString(usedfltcnfgnm, tp="tf");
    tstgenlinec = "usenodb: " + getTrueFalseString(nodb, tp="tf");
    tstgenlined = "usedefaultdbobjname: " + getTrueFalseString(finusedfltdbnm, tp="tf");
    #optional if c value is true
    tstgenlinee = "configmodulename: the_name";#optional if b value is true
    tstgenlinef = "dbobjname: the_name";#optional if c or d value is true
    tstflines = [tstgenlinea, tstgenlineab, tstgenlineb, tstgenlinec,
                 tstgenlined, tstgenlinee, tstgenlinef];
    myinctstlines = "1" + ("1" if usetstwmd else "0") + "1" + ("0" if nodb else "1");
    myinctstlines += ("0" if usedfltcnfgnm else "1") + ("0" if finusedfltdbnm else "1");

    merrmsgapta = "the number of ";
    merrmsgaptb = " file lines must be the same as the number of characters on the include ";
    merrmsgaptc = " file lines string length, but they were not!";
    merrmsga = merrmsgapta + "test" + merrmsgaptb + "test" + merrmsgaptc;
    merrmsgb = merrmsgapta + "model" + merrmsgaptb + "model" + merrmsgaptc;
    if (len(myinctstlines) == len(tstflines)): pass;
    else: raise ValueError(merrmsga);

    mdlsgenlinea = "models_class_new_file_name: the_name_and_loc";
    mdlsgenlineab = "modelsfile_write_mode: a";#write mode is optional
    mdlsgenlineb = "models_class_list:";
    mdlsgenlinec = "classnamea, tablenamea: None";
    mdlsgenlined = "classnameb, tablenameb: None";
    mdlsgenlinee = "classnamec, tablenamec: None";
    #...
    mdlsflines = [mdlsgenlinea, mdlsgenlineab, mdlsgenlineb, mdlsgenlinec, mdlsgenlined, mdlsgenlinee];
    myincmdlslines = "1" + ("1" if usemdlswmd else "0") + "1111";

    if (len(myincmdlslines) == len(mdlsflines)): pass;
    else: raise ValueError(merrmsgb);

    mflines = ["" + tstflines[i] for i in range(len(tstflines)) if (myinctstlines[i] == '1')];
    for i in range(len(mdlsflines)):
        if (myincmdlslines[i] == '1'):
            mflines.append("" + mdlsflines[i]);
    return mflines;


#everything is wrong below this point 11-9-2025 4:46 AM MST
#python filename ?
#python filename ?
#python filename ?
#python
if __name__ == "__main__":
    dffnm = "genconfig.txt";
    errmsg = "Please enter a filename no extension and the location to it! If not the default '";
    errmsg += "" + dffnm + "' will be used. This is the only argument accepted! ";
    errmsg += "If you have -? or -help it will also display a message about the model classes options.";
    cfnm = None;
    optsdictobj = getOptsFlagsDict();
    mdlclsoptsmsg = "Note models start options are: " + str(optsdictobj["allopts"]);
    mdlclsoptsmsg += " you may also have None.";
    print(f"Total Arguments: {len(sys.argv)}");
    print(sys.argv[0]);
    print(sys.argv[1:]);
    print("the rest of the script!");
    #print(mdlclsoptsmsg + "\n\n");

    if (len(sys.argv) == 1): cfnm = "" + dffnm;
    elif (len(sys.argv) == 2):
        if (sys.argv[1].startswith("-")): raise ValueError(mdlclsoptsmsg + "\n\n" + errmsg);
        myvalidator.stringMustHaveAtMinNumChars(sys.argv[1], 1, varnm="sys.argv[1]");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(sys.argv[1], varnm="sys.argv[1]");
        cfnm = "" + sys.argv[1] + ".txt";
    else: raise ValueError(errmsg);
    mflines = genFileLines(usetstwmd=True, usemdlswmd=True, nodb=False,
                           usedfltcnfgnm=False, usedfltdbnm=False);
    mybase.blockifmyfileexistswritelines(cfnm, mflines, dscptrmsg="generator config");
