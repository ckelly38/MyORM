from myorm.myvalidator import myvalidator;
from myorm.mybase import mybase;
from myorm.modelsgenerator import getOptsFlagsDict;
from myorm.testfilegenerator import getNoDBFlags;
from myorm.mastergenerator import getTestFileFlags, getModelsFileFlags;
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
    myinctstlines = "1" + ("1" if usetstwmd else "0") + "11" + ("0" if nodb else "1");
    myinctstlines += ("0" if usedfltcnfgnm else "1") + ("0" if finusedfltdbnm else "1");

    mdlsgenlinea = "models_class_new_file_name: the_name_and_loc";
    mdlsgenlineab = "modelsfile_write_mode: a";#write mode is optional
    mdlsgenlineb = "models_class_list:";
    mdlsgenlinec = "classnamea, tablenamea: -all";
    mdlsgenlined = "classnameb, tablenameb: -validators";
    mdlsgenlinee = "classnamec, tablenamec: -repr";
    mdlsgenlinef = "classnamed, tablenamed: -to_dict";
    mdlsgenlineg = "classnamee, tablenamee: None";
    #...
    mdlsflines = [mdlsgenlinea, mdlsgenlineab, mdlsgenlineb, mdlsgenlinec, mdlsgenlined, mdlsgenlinee,
                  mdlsgenlinef, mdlsgenlineg];
    myincmdlslines = "1" + ("1" if usemdlswmd else "0") + "111111";

    #assertions to see if the config file will be generated correctly
    merrmsgapta = "the number of ";
    merrmsgaptb = " file lines must be the same as the number of characters on the include ";
    merrmsgaptc = " file lines string length, but they were not!";
    merrmsga = merrmsgapta + "test" + merrmsgaptb + "test" + merrmsgaptc;
    merrmsgb = merrmsgapta + "model" + merrmsgaptb + "model" + merrmsgaptc;
    if (len(myinctstlines) == len(tstflines)): pass;
    else: raise ValueError(merrmsga);

    if (len(myincmdlslines) == len(mdlsflines)): pass;
    else: raise ValueError(merrmsgb);

    mflines = ["" + tstflines[i] for i in range(len(tstflines)) if (myinctstlines[i] == '1')];
    mflines.append("");
    for i in range(len(mdlsflines)):
        if (myincmdlslines[i] == '1'):
            mflines.append("" + mdlsflines[i]);
    return mflines;

def getDefaultNames():
    return ["-usedfltname", "-usedefaultname", "-dfltname", "-defaultname",
            "-usedfltnm", "-usedefaultnm", "-dfltnm", "-defaultnm",
            "-useDFLTName", "-useDefaultName", "-useDFLTNM", "-useDefaultNM",
            "-DFLTName", "-defaultName", "-UseDFLTName", "-UseDefaultName", "-DefaultName",
            "-defaultNM", "-UseDFLTNM", "-UseDefaultNM", "-DefaultNM",
            "-DFLTNAME", "-USEDFLTNAME", "-USEDEFAULTNAME", "-DEFAULTNAME",
            "-USEDFLTNM", "-DFLTNM", "-USEDEFAULTNM", "-DEFAULTNM"];

def getCaseNumForStr(mstr):
    myvalidator.varmustnotbeempty(mstr, varnm="mstr");
    if (mstr.islower()): return 0;
    elif (mstr.isupper()): return 1;
    else: return 2;

def getMyLenEndDiffForName(mstr):
    if (myvalidator.isvaremptyornull(mstr)): return 0;
    if (mstr.endswith("name") or mstr.endswith("Name") or mstr.endswith("NAME")): return 4;
    elif (mstr.endswith("nm") or mstr.endswith("NM")): return 2;
    else: return 0;

def getDefaultConfigOrDBNameFlags(usedb):
    myvalidator.varmustbeboolean(usedb, "usedb");
    dfltnms = getDefaultNames();
    dfltnmslendiffs = [getMyLenEndDiffForName(nm) for nm in dfltnms];
    #len(dfltnms[n]) - dfltnmslendiffs[n] - 1 on first index old value
    #len(dfltnms[n]) - dfltnmslendiffs[n] + 2 on second index old value
    dfltnmcs = [getCaseNumForStr(dfltnms[n][1:]) for n in range(len(dfltnms))];
    dbopts = ["db", "DB"];
    cnfgopts = ["cnfg", "config", "Config", "CONFIG", "CNFG"];
    dbcs = "01";#0 all lowercase 1 all uppercase 2 snake
    cnfgcs = "00211";
    mlist = ["" + item for item in (dbopts if usedb else cnfgopts)];
    mycs = ("" + dbcs if usedb else "" + cnfgcs);
    if (len(mlist) == len(mycs)): pass;
    else: raise ValueError("the options list and the case strings must both be the same length!");
    #print(f"dfltnms = {dfltnms}");
    #print(f"dfltnmcs = {dfltnmcs}");
    #print(f"dfltnmslendiffs = {dfltnmslendiffs}");
    #we put the option insert it the index calculated
    rlist = [dfltnms[n][0:len(dfltnms[n]) - dfltnmslendiffs[n]] + mlist[ci] +
             dfltnms[n][len(dfltnms[n]) - dfltnmslendiffs[n]:]
             for n in range(len(dfltnms)) for ci in range(len(mlist)) if (int(mycs[ci]) == dfltnmcs[n])];
    #rlist = [];
    #for n in range(len(dfltnms)):
    #    cnm = dfltnms[n];
    #    spi = len(cnm) - dfltnmslendiffs[n];#split index
    #    for ci in range(len(mlist)):
    #        if (int(mycs[ci]) == dfltnmcs[n]): rlist.append(cnm[0:spi] + mlist[ci] + cnm[spi:]);
    #print(f"rlist = {rlist}");
    return rlist;
def getDefaultConfigNameFlags(): return getDefaultConfigOrDBNameFlags(False);
def getDefaultDBNameFlags(): return getDefaultConfigOrDBNameFlags(True);

def getNoWriteModeFlags():
    return ["-nowritemode", "-nowritemd", "-nowmd", "-noWriteMode", "-NoWriteMode",
            "-noWriteMD", "-NoWriteMD", "-noWMD", "-NoWMD",  "-NOWWRITEMODE", "-NOWRITEMD", "-NOWMD"];

def getTestOrModelsNoWriteModeFlags(usetsts):
    myvalidator.varmustbeboolean(usetsts, "usetsts");
    tstslist = getTestFileFlags();
    mdlslist = getModelsFileFlags();
    mlist = ["" + item for item in (tstslist if usetsts else mdlslist)];
    mycsnums = [getCaseNumForStr(mlist[n][1:]) for n in range(len(mlist))];
    tstomdlsc = myvalidator.myjoin("", mycsnums);
    #tstslist = ["-tst", "-test", "-Test", "-TST", "-TEST"];
    #mdlslist = ["-mdls", "-models", "-Models", "-MDLS", "-MODELS"];
    #tstomdlsc = "00211";#0 all lowercase 1 all uppercase 2 snake
    merrmsga = "the test or models lists and the string dictating the case must be the same length!";
    if (len(mlist) == len(tstomdlsc)): pass;
    else: raise ValueError(merrmsga);

    #we want to insert our selected option after the first 3 characters.
    #we want the case to match IE if the w is lowercase then the t or the m must be lowercase
    #if it is all caps, we want our option to be all caps.
    #if it is all lowercase, then we want it all lowercase.
    #
    #on the no write mode options list: the first 3 are all lowercase, the last 3 are all uppercase
    #the middle are midcase.
    wmdopts = getNoWriteModeFlags();
    wmdlwropts = "000222222111";#0 all lowercase 1 all uppercase 2 snake
    merrmsgb = "the write mode options list and the string dictating the case must be the same length!";
    if (len(wmdopts) == len(wmdlwropts)): pass;
    else: raise ValueError(merrmsgb);

    #item at index 0 and 1 on the mlist goes into the ones with 0s only on the opts list
    finlst = [wmdopts[n][0:3] + mlist[i][1:] + wmdopts[n][3:]
              for n in range(len(wmdopts)) for i in range(len(mlist)) if (tstomdlsc[i] == wmdlwropts[n])];
    #print(f"finlst = {finlst}");
    return finlst;
def getTestNoWriteModeFlags(): return getTestOrModelsNoWriteModeFlags(True);
def getModelsNoWriteModeFlags(): return getTestOrModelsNoWriteModeFlags(False);


#python filename -notstwmd -nomdlswmd -nodb -usedfltcnfgnm -usedfltdbnm
#python filename ?
#python filename
#python
if __name__ == "__main__":
    dffnm = "genconfig.txt";
    optsdictobj = getOptsFlagsDict();
    nodbopts = getNoDBFlags();
    tstnowmdopts = getTestNoWriteModeFlags();
    mdlsnowmdopts = getModelsNoWriteModeFlags();
    dfltcnfgnmflgs = getDefaultConfigNameFlags();
    dfltdbnmflgs = getDefaultDBNameFlags();
    
    errmsg = "invalid number of arguments used! You must use the program as follows:\n";
    errmsg += "1. Please enter a filename no extension and the location to it! If not the default '";
    errmsg += "" + dffnm + "' will be used.\nAfter that you have options and the order does not matter.";
    errmsg += " 2. Your next parameters must of course be either a: no test write mode option: ";
    errmsg += "" + str(tstnowmdopts) + "\nor it could be a no models write mode option: ";
    errmsg += "" + str(mdlsnowmdopts) + "\nor it could be a no db option: " + str(nodbopts);
    errmsg += "\nor it could be a use default config module name option: " + str(dfltcnfgnmflgs);
    errmsg += "\nor it could be a use default DB object name option: " + str(dfltdbnmflgs);
    errmsg += ".\nNOTE: You do not have to have any of them and the defaults will be used!";
    errmsg += "The defaults are to include the write modes, to have a non-default DB name, and a ";
    errmsg += "non-default config module name. BUT if you want to have the options, then you must ";
    errmsg += "include a filename before those options.\nAlternatively you could have no parameters and";
    errmsg += " all defaults will be used.\nBUT IF YOU HAVE MORE THAN 7 ARGUMENTS, THEN IT WILL ERROR ";
    errmsg += "OUT. OR IF YOU HAVE A DUPLICATE OPTION IT WILL ALSO ERROR OUT.\n\n";
    errmsg += "YOUR models start options are: " + str(optsdictobj["allopts"]);
    errmsg += " you may also have None.\nYou can also type -? or -help to see this message again.";
    
    print(f"Total Arguments: {len(sys.argv)}");
    print(sys.argv[0]);
    print(sys.argv[1:]);
    print("the rest of the script!");
    
    cfnm = None;
    myutstwmd = True;
    myumdlswmd = True;
    myunodb = False;
    myudfltcnfgnm = False;
    myudfltdbnm = False;
    if (len(sys.argv) == 1): cfnm = "" + dffnm;
    elif (1 < len(sys.argv) < 8):
        if (sys.argv[1].startswith("-")): raise ValueError(errmsg);
        myvalidator.stringMustHaveAtMinNumChars(sys.argv[1], 1, varnm="sys.argv[1]");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(sys.argv[1], varnm="sys.argv[1]");
        cfnm = "" + sys.argv[1] + ".txt";
        if (2 < len(sys.argv)):
            merrmsgpta = "the arguments sys.argv[";
            merrmsgptb = " must be on one of the options lists (and not already used), but it was not!";
            for n in range(2, len(sys.argv)):
                mderrmsg = "" + str(n) + "]=" + str(sys.argv[n]);
                if (myvalidator.isListAInListB([sys.argv[n]], nodbopts) and not myunodb): myunodb = True;
                elif (myvalidator.isListAInListB([sys.argv[n]], tstnowmdopts) and myutstwmd):
                    myutstwmd = False;
                elif (myvalidator.isListAInListB([sys.argv[n]], mdlsnowmdopts) and myumdlswmd):
                    myumdlswmd = False;
                elif (myvalidator.isListAInListB([sys.argv[n]], dfltcnfgnmflgs) and not myudfltcnfgnm):
                  myudfltcnfgnm = True;
                elif (myvalidator.isListAInListB([sys.argv[n]], dfltdbnmflgs) and not myudfltdbnm):
                  myudfltdbnm = True;
                else: raise ValueError(merrmsgpta + mderrmsg + merrmsgptb + "\n\n" + errmsg);
    else: raise ValueError(errmsg);
    print(f"myutstwmd = {myutstwmd}");
    print(f"myumdlswmd = {myumdlswmd}");
    print(f"myunodb = {myunodb}");
    print(f"myudfltcnfgnm = {myudfltcnfgnm}");
    print(f"myudfltdbnm = {myudfltdbnm}");

    mflines = genFileLines(usetstwmd=myutstwmd, usemdlswmd=myumdlswmd, nodb=myunodb,
                           usedfltcnfgnm=myudfltcnfgnm, usedfltdbnm=myudfltdbnm);
    print("\nnew config file lines are:");
    for mline in mflines: print(mline);
    print("");
    
    mybase.blockifmyfileexistswritelines(cfnm, mflines, dscptrmsg="generator config");
    
    print("SUCCESSFULLY GENERATED THE CONFIG FILE!");
    print("THIS CONFIG FILE IS THE FILE YOU CAN USE TO GENERATE THE MODELS AND TEST FILE STARTER CODE" +
          " VIA THE MASTER GENERATOR.");
    print("YOU SHOULD OPEN UP THE CONFIG FILE AND EDIT IT THE WAY YOU WANT IT LIKE THE ACTUAL NAMES " +
          "OF THE NEW FILES FOR EXAMPLE,\nTHE ACTUAL NAMES OF TABLES AND MODEL CLASSES,\n" +
          "AND MAKE SURE THAT THE METHOD OPTIONS ARE WHAT YOU WANT FOR THE MODELS!");
    print("THE WRITE MODE FOR THE FILE IS WHAT HAPPENS WHEN THE FILE EXISTS!");
    print("THE MASTER GENERATOR TAKES THE CONFIG FILE AND A FEW OTHER INPUTS AND CALLS THE OTHER " +
          "GENERATORS (testfilegenerator, modelsgenerator, classliststartupgen) FOR YOU!");
