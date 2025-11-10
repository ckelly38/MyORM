from myorm.myvalidator import myvalidator;
from myorm.classliststartupgen import getLinesFromFile, genClassImportLines;
from myorm.modelsgenerator import getOptsFlagsDict, getOverWriteFlags, getAppendFlags;
from myorm.modelsgenerator import genFullModelsScriptAndWriteItNow;
from myorm.modelsgenerator import genFileLines as genModelsFileLines;
from myorm.testfilegenerator import genFileLines as genTestFileLines;
from myorm.testfilegenerator import genFullTestFileScriptAndWriteItNow;
import sys;

def getAcceptedTrueOrFalseAnswers():
    return ["false", "False", "FALSE", "NO", "no", "0", "true", "True", "TRUE", "YES", "Yes", "yes", "1"];

def getTrueOrFalseBoolFromString(mval):
    tfans = getAcceptedTrueOrFalseAnswers();
    myvalidator.itemMustBeOneOf(mval, tfans, varnm="mval");
    mytfi = tfans.index(mval);
    return (False if mytfi < 6 else True);

def getValPartOfString(lnum, flines):
    myvalidator.varmustnotbeempty(flines, varnm="flines");
    myvalidator.valueMustBeInMinAndMaxRange(lnum, 0, len(flines) - 1, varnm="lnum");
    return "" + flines[lnum][flines[lnum].index(": ")+2:];

def boolValIsValidForLine(lnum, flines):
    tfans = getAcceptedTrueOrFalseAnswers();
    tmpsecpt = getValPartOfString(lnum, flines);
    myvnm = "the second part of line " + str(lnum + 1);
    omerrmsg = "config file was wrong on " + myvnm + " because it was not a true or false value!";
    if (tmpsecpt.isalpha()):
        myvalidator.itemMustBeOneOf(tmpsecpt, tfans, varnm=myvnm);
        return True;
    else: raise ValueError(omerrmsg);

def getValAsBoolPartOfString(lnum, flines):
    return getTrueOrFalseBoolFromString(getValPartOfString(lnum, flines));

def stringValMustBeAlnumOrUnderscores(lnum, flines):
    secptofline = getValPartOfString(lnum, flines);
    myvnm = "line " + str(lnum + 1) + " on config file";
    myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(secptofline, varnm=myvnm);
    return True;

def areLinesInModelFormatAndGetInfoObj(flines, si, optsdictobj):
    #now the rest must meet the following format:
    #classnamea, tablenamea: opt or None
    myvalidator.varmustnotbeempty(flines, varnm="flines");
    myvalidator.objvarmusthavethesekeysonit(optsdictobj, ["allopts"], varnm="optsdictobj");
    mdlsfnm = getValPartOfString(si - 2, flines);
    myopts = optsdictobj["allopts"];
    myarrstrsarr = [];
    mdlsflines = [];
    for n in range(si, len(flines)):
        cline = flines[n];
        myvnm = "second part of the line num: " + str(n + 1);
        mstrs = myvalidator.mysplitWithLen(cline, [cline.index(", "), cline.index(": ")], 2, offset=0);
        for cstr in mstrs:
            tmpstr = (cstr[1:] if (cstr[0] == "-") else "" + cstr);
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tmpstr, varnm="cstr");
        if (mstrs[2] == "None"): pass;
        else: myvalidator.itemMustBeOneOf(mstrs[2], myopts, varnm=myvnm);
        myarrstrsarr.append(mstrs);
        mdlsflines.append(cline);
    return {"result": True, "mdlsfname": mdlsfnm, "origsi": si, "mysplitstrsarrs": myarrstrsarr,
            "mdlsflines": mdlsflines};

def lineMustHaveTheExpectedPartAtTheSpotAndBeBoolOrAString(lnum, explinestr, expi, flines,
                                                           useblvlisvld):
    myvalidator.varmustnotbeempty(flines, varnm="flines");
    myvalidator.valueMustBeInMinAndMaxRange(lnum, 0, len(flines) - 1, varnm="lnum");
    myvalidator.stringMustHaveAtMinNumChars(explinestr, 1, varnm="explinestr");
    myvalidator.varmustbeboolean(useblvlisvld, "useblvlisvld");
    if (flines[lnum].index(explinestr) == expi):
        if (useblvlisvld): boolValIsValidForLine(lnum, flines);
        else: stringValMustBeAlnumOrUnderscores(lnum, flines);
    else: raise ValueError("config file was wrong on line " + str(lnum + 1) + "!");
def lineMustHaveTheExpectedPartAtTheSpotAndBeABool(lnum, explinestr, expi, flines):
    return lineMustHaveTheExpectedPartAtTheSpotAndBeBoolOrAString(lnum, explinestr, expi, flines, True);
def lineMustHaveTheExpectedPartAtTheSpotAndBeAString(lnum, explinestr, expi, flines):
    return lineMustHaveTheExpectedPartAtTheSpotAndBeBoolOrAString(lnum, explinestr, expi, flines, False);

def configFileMustBeValidAndGetInfoObj(flines, optsdictobj):
    origtstkys = ["testfile_new_file_name", "testfile_write_mode", "usedefaultconfigmodulename",
                  "usenodb", "usedefaultdbobjname", "configmodulename", "dbobjname"];
    tstgenlinea = "" + origtstkys[0] + ": ";
    tstgenlineab = "" + origtstkys[1] + ": ";
    tstgenlineb = "" + origtstkys[2] + ": ";
    tstgenlinec = "" + origtstkys[3] + ": ";
    tstgenlined = "" + origtstkys[4] + ": ";
    tstgenlinee = "" + origtstkys[5] + ": ";
    tstgenlinef = "" + origtstkys[6] + ": ";

    mdlsgenlinea = "modelsfile_new_file_name: ";
    mdlsgenlineab = "modelsfile_write_mode: ";
    mdlsgenlineb = "models_class_list:";
    #mdlsgenlinec = "classnamea, tablenamea: None";#included this line to show formatting
    
    isblkys = "0011100";
    fintstkys = ["tstfname", "tstfwmd", "usedfltcnfgmdlname", "nodb", "usedfltdbobjname", "cnfgmdlname",
                 "dbojbname"];
    #skpkys = "0100111";

    wrteflgs = getOverWriteFlags();
    apndflgs = getAppendFlags();
    blkflgs = ['b'];
    wrteblkflgs = myvalidator.combineTwoLists(wrteflgs, blkflgs, nodups=True);
    allwrteflgs = myvalidator.combineTwoLists(wrteflgs, apndflgs, nodups=True);
    allflgs = myvalidator.combineTwoLists(allwrteflgs, blkflgs, nodups=True);

    merrmsgblvl = "since we are not using a database, the default name must be used, but it was not ";
    merrmsgblvl += "therefore there is a problem with config line 4!";

    merrmsgblkyslen = "the number of is bool keys must be the same as the number of orig test keys, ";
    if (len(isblkys) == len(origtstkys)): pass;
    else: raise ValueError(merrmsgblkyslen + "but they were not!");
    
    lineMustHaveTheExpectedPartAtTheSpotAndBeAString(0, tstgenlinea, 0, flines);
    inito = 0;
    if (tstgenlineab in flines[1]):
        lineMustHaveTheExpectedPartAtTheSpotAndBeAString(1, tstgenlineab, 0, flines);
        tstwmdarr = myvalidator.mysplitWithDelimeter(flines[1], ": ", offset=0);
        tstwmdval = tstwmdarr[1];
        inito = 1;
        myvarnm = "tstwmdval=flines[1]=config file line 2";
        myvalidator.itemMustBeOneOf("-" + tstwmdval, wrteblkflgs, varnm=myvarnm);
    lineMustHaveTheExpectedPartAtTheSpotAndBeABool(1 + inito, tstgenlineb, 0, flines);
    lineMustHaveTheExpectedPartAtTheSpotAndBeABool(2 + inito, tstgenlinec, 0, flines);
    usdfltmdlcnfgnm = getValAsBoolPartOfString(1 + inito, flines);
    undbval = getValAsBoolPartOfString(2 + inito, flines);
    offset = 0;
    if (undbval):
        #we do not need line d and f to be present, but they still can be
        #however if usedefaultdbobjname: is present then it must be true.
        if (tstgenlined in flines[3 + inito]):
            boolValIsValidForLine(3 + inito, flines);
            mbval = getValAsBoolPartOfString(3 + inito, flines);
            if (mbval):
                if (tstgenlinee in flines[4 + inito] and flines[4 + inito].index(tstgenlinee) == 0):
                    stringValMustBeAlnumOrUnderscores(4 + inito, flines);
                else: raise ValueError("config file was wrong on line " + str(5 + inito) + "!");
                if (tstgenlinef in flines[5 + inito] and flines[5 + inito].index(tstgenlinef) == 0):
                    stringValMustBeAlnumOrUnderscores(5 + inito, flines);
                else: raise ValueError("config file was wrong on line " + str(6 + inito) + "!");
            else: raise ValueError(merrmsgblvl);
        elif (tstgenlinee in flines[3 + inito]):
            stringValMustBeAlnumOrUnderscores(3 + inito, flines);
            offset = -2;
        elif (usdfltmdlcnfgnm and len(flines[3 + inito]) < 1): offset = -3;
        else: raise ValueError("config file was wrong on line " + str(6 + inito) + "!");
    else:
        lineMustHaveTheExpectedPartAtTheSpotAndBeABool(3 + inito, tstgenlined, 0, flines);
        lineMustHaveTheExpectedPartAtTheSpotAndBeAString(4 + inito, tstgenlinee, 0, flines);
        lineMustHaveTheExpectedPartAtTheSpotAndBeAString(5 + inito, tstgenlinef, 0, flines);
    tstttloffst = offset + inito;
    if (len(flines[6 + tstttloffst]) < 1): pass;
    else: raise ValueError("config file was wrong on line " + str(7 + tstttloffst) + "!");
    lineMustHaveTheExpectedPartAtTheSpotAndBeAString(7 + tstttloffst, mdlsgenlinea, 0, flines);
    mdlswmdval = None;
    mdlso = 0;
    if (mdlsgenlineab in flines[8 + tstttloffst]):
        lineMustHaveTheExpectedPartAtTheSpotAndBeAString(8 + tstttloffst, mdlsgenlineab, 0, flines);
        mdlso = 1;
        mdlswmdarr = myvalidator.mysplitWithDelimeter(flines[8 + tstttloffst], ": ", offset=0);
        mdlswmdval = mdlswmdarr[1];
        tmplni = 8 + tstttloffst;
        myvarnm = "mdlswmdval=flines[" + str(tmplni) + "]=config file line " + str(tmplni + 1);
        myvalidator.itemMustBeOneOf("-" + mdlswmdval, allflgs, varnm=myvarnm);
    if (flines[8 + tstttloffst + mdlso] == mdlsgenlineb): pass;
    else: raise ValueError("config file was wrong on line " + str(9 + tstttloffst + mdlso) + "!");
    mdlsresobj = areLinesInModelFormatAndGetInfoObj(flines, 9 + tstttloffst + mdlso, optsdictobj);
    
    #get the values from the config and split them...
    tstmstrs = [myvalidator.mysplitWithDelimeter(flines[n], ": ", offset=0) for n in range(len(flines))
                if n < 6 + tstttloffst];
    #print(tstmstrs);
    
    myobj = {"result": True};
    for n in range(len(tstmstrs)):
        myarr = tstmstrs[n];
        mky = myarr[0];
        mval = myarr[1];
        mki = origtstkys.index(mky);
        finky = fintstkys[mki];
        finval = (getTrueOrFalseBoolFromString(mval) if (bool(int(isblkys[mki]))) else "" + mval);
        myobj[finky] = finval;
    myobj["initoffset"] = inito;
    myobj["offset"] = offset;
    myobj["fulltestoffset"] = tstttloffst;
    myobj["listlinesi"] = 9 + tstttloffst;
    if (mdlso == 1): myobj["mdlsfwmd"] = "" + mdlswmdval;
    myobj["mdlsresobj"] = mdlsresobj;
    return myobj;

#this determines the write mode to use if given two options the commandline option and the config option
#if they are the same, it returns it.
#if they are different, the difftp if a returns the first option, if b returns the second, else errors.
#it will only return one of 3 values: 'a', 'w', or 'b' for append, write, or block.
def getFinalWriteMode(cmdmd, cnfgmd, difftp="a"):
    if (myvalidator.isvaremptyornull(cmdmd)): return getFinalWriteMode('b', cnfgmd, difftp=difftp);
    elif (myvalidator.isvaremptyornull(cnfgmd)): return getFinalWriteMode(cmdmd, 'b', difftp=difftp);
    elif (myvalidator.isvaremptyornull(difftp)): return getFinalWriteMode(cmdmd, cnfgmd, difftp='a');
    isdiff = False;
    if (cmdmd == 'a' or cmdmd == 'A'):
        if (cnfgmd == 'a' or cnfgmd == 'A'): return 'a';
        else: isdiff = True;
    elif (cmdmd == 'w' or cmdmd == 'W'):
        if (cnfgmd == 'w' or cnfgmd == 'W'): return 'w';
        else: isdiff = True;
    else:
        #cmdmd = 'b';
        if (cnfgmd in ['a', 'A', 'w', 'W']): isdiff = True;
        else: return 'b';
    if (isdiff):
        errmsg = "the config file write mode and the commandline arguments must be the same!";
        if (difftp == 'a' or difftp == 'A'):
            if (cmdmd == 'a' or cmdmd == 'A'): return 'a';
            elif (cmdmd == 'w' or cmdmd == 'W'): return 'w';
            else: return 'b';
        elif (difftp == 'b' or difftp == 'B'):
            if (cnfgmd == 'a' or cnfgmd == 'A'): return 'a';
            elif (cnfgmd == 'w' or cnfgmd == 'W'): return 'w';
            else: return 'b';
        else: raise ValueError(errmsg);
    else: raise ValueError("the same modes case should have been handled already!");
#this prioritizes the option we gave it. If we the write mode came in on the command line (usecmd=True),
#it says use the first option and if they are different return the first option.
#if we told it to use the write mode from the file (usecmd=False), then it says us the second option
#and if they are different return the second option.
def getFinalWriteModeCMDOrConfigOnly(wmd, usecmd):
    myvalidator.varmustbeboolean(usecmd, varnm="usecmd");
    if (usecmd): return getFinalWriteMode(wmd, 'b', difftp='a');
    else: return getFinalWriteMode('b', wmd, difftp='b');
def getFinalWriteCMDModeOnly(wmd): return getFinalWriteModeCMDOrConfigOnly(wmd, True);
def getFinalWriteConfigModeOnly(wmd): return getFinalWriteModeCMDOrConfigOnly(wmd, False);

def getWriteModeFromFlag(wmdflg):
    wrteflgs = getOverWriteFlags();
    apndflgs = getAppendFlags();
    return ('w' if (myvalidator.isListAInListB([wmdflg], wrteflgs)) else
            ('a' if (myvalidator.isListAInListB([wmdflg], apndflgs)) else 'b'));

def getModelsFileFlags():
    return ["-models", "-Models", "-MODELS", "-mdls", "-MDLS", "-modelsfile", "-modelsFile",
            "-ModelsFile", "-MODELSFILE"];

def getTestFileFlags():
    return ["-test", "-tst", "-testfile", "-testFile", "-TestFile", "-TESTFILE"];


#0       1              2   3     4    5 (arg indexes)
#python configfilename -tst wtmd -mdls wtmd
#python configfilename -mdls wtmd -tst wtmd
#python configfilename -tst wtmd
#python configfilename -mdls wtmd
#python configfilename
#note replace python with: python -m myorm.mastergenerator
if __name__ == "__main__":
    #make sure the config file is valid
    #then call the other generators
    wrteflgs = getOverWriteFlags();
    apndflgs = getAppendFlags();
    allflgs = myvalidator.combineTwoLists(wrteflgs, apndflgs, nodups=True);
    mdlsflgs = getModelsFileFlags();
    tstflgs = getTestFileFlags();
    allfileflgs = myvalidator.combineTwoLists(mdlsflgs, tstflgs, nodups=True);
    optabc = "1. the filename with the extension.\n2. the file type test or models here.\n";
    optabc += "3. the write mode for the file type given in 2 here.\n";
    misdismsg = " NOTE: for the others not given they will come in as block mode if needed unless ";
    misdismsg += "they are in the config file.";
    apndmderrmsg = "the append mode is not supported for the test file only write or block modes ";
    apndmderrmsg += "are allowed!";
    
    merrmsg = "invalid number of arguments! You must have 5 arguments as follows:\n" + optabc;
    merrmsg += "4. the file type test or models the other one that you did not use in 2.\n";
    merrmsg += "5. the write mode for the file type given in 4 here.\nAlternatively you must have 3 ";
    merrmsg += "arguments as follows:\n" + optabc + misdismsg;
    merrmsg += "\nAlternatively you must have one argument:\n1. the filename with the extension.\n";
    merrmsg += "" + misdismsg + "\nOtherwise it will not work!";

    print(f"Total Arguments: {len(sys.argv)}");
    print(sys.argv[0]);
    print(sys.argv[1:]);
    print("the rest of the script!");
    
    if (len(sys.argv) in [2, 4, 6]): pass;
    else: raise ValueError(merrmsg);

    fnm = sys.argv[1];
    flines = getLinesFromFile(fnm, noext=False);
    print("config file lines are:");
    for n in range(len(flines)): print(str(n + 1) + ": " + flines[n]);
    
    optsdictobj = getOptsFlagsDict();
    resdict = configFileMustBeValidAndGetInfoObj(flines, optsdictobj);
    print("\nconfig file is valid!\n");
    print(resdict, end="\n\n");

    #get the information about the test file here now
    #get the information about the models file here now
    nwtstfnm = resdict["tstfname"];
    myusenodb = resdict["nodb"];
    nwmdlsfnm = resdict["mdlsresobj"]["mdlsfname"];
    myusedfltcnfgmdlnm = resdict["usedfltcnfgmdlname"];
    
    #optional if the lines are even in the config file
    cnfgmdlnm = (None if myusedfltcnfgmdlnm else resdict["cnfgmdlname"]);
    mydbrefnm = (None if myusenodb else resdict["dbojbname"]);
    myusedfltdbnm = (True if myusenodb else resdict["usedfltdbobjname"]);
    print(f"nwtstfnm = {nwtstfnm}");
    print(f"myusenodb = {myusenodb}");
    print(f"myusedfltcnfgmdlnm = {myusedfltcnfgmdlnm}");
    print(f"nwmdlsfnm = {nwmdlsfnm}");
    print(f"cnfgmdlnm = {cnfgmdlnm}");
    print(f"mydbrefnm = {mydbrefnm}");
    print(f"myusedfltdbnm = {myusedfltdbnm}");

    #get the information from the models results object
    mdlsclslist = [];
    mdlsoptslist = [];
    mdlstnmslist = [];
    for myarr in resdict["mdlsresobj"]["mysplitstrsarrs"]:
        #print(myarr);
        mdlsclslist.append("" + myarr[0]);
        mdlstnmslist.append("" + myarr[1]);
        mdlsoptslist.append("" + myarr[2]);
    print(f"mdlsclslist = {mdlsclslist}");
    print(f"mdlstnmslist = {mdlstnmslist}");
    print(f"mdlsoptslist = {mdlsoptslist}");

    myimprtlines = genClassImportLines(mdlsclslist, [nwmdlsfnm]);
    print("\nimport lines for the new test file are:");
    for cline in myimprtlines: print(cline);
    
    #generate the files...
    #call the models file generator correctly
    #then call the test file generator correctly with the given information using the model
    #information as well
    nmdlsfilelines = genModelsFileLines(mdlsclslist, mdlsoptslist, optsdictobj, tnms=mdlstnmslist);
    print("\nlines in the new models file to be generated are:");
    for cline in nmdlsfilelines: print(cline);

    nwtstfilelines = genTestFileLines(confgnm=cnfgmdlnm, dbrefnm=mydbrefnm,
                                      imprtlines=myimprtlines, usenodb=myusenodb);
    print("\nlines in the new startup file to be generated are:");
    for cline in nwtstfilelines: print(cline);

    #if the test file exists, it is either overwritten or blocked (no append mode for this)
    #if the models file exists, it could be overwritten or appended or blocked.
    #RULE: if a write mode is not provided for either file, the one missing will use block mode.
    #RULE: if only one mode is provided for a file no matter how, it will be used.
    #RULE: if two are provided, but they mean the same thing, treat it as if only one was provided.
    #
    #In the models case it left off the top import lines (in order to support append mode),
    #but the method below takes care of that.
    #
    #how does the user tell the program what write mode to use for what file?
    #does it include this information in the generators config file as well? or via command?
    #do we just arbitrarily say block, overwrite, or append if one exists? NO.
    #if two different write modes are provided (one on command and one in the genconfig file)
    #which one has higher priority or which one will be used OR does it error out?
    #
    #getFinalWriteMode(cmdmd, cnfgmd, difftp="a");
    #
    #the last one is higher priority: a, b, or error if different
    #if only one provided, set the provided one as the priority
    #if two are provided, unless it is specified the program may let the user override.
    
    myresdictkys = list(resdict.keys());
    tstwmdincnfgfile = ("tstfwmd" in myresdictkys);
    mdlswmdincnfgfile = ("mdlsfwmd" in myresdictkys);
    #if (tstwmdincnfgfile): print("test file write mode is present!");
    #else: print("test file write mode is not present!");
    #if (mdlswmdincnfgfile): print("models file write mode is present!");
    #else: print("models file write mode is not present!");
    
    tmptstwmdfile = (resdict["tstfwmd"] if tstwmdincnfgfile else 'b');
    tmpmdlswmdfile = (resdict["mdlsfwmd"] if mdlswmdincnfgfile else 'b');
    #print(f"tmptstwmdfile = {tmptstwmdfile}");
    #print(f"tmpmdlswmdfile = {tmpmdlswmdfile}");

    #if the write mode flag is present, or w, a, or b then we are good.
    #otherwise this is illegal
    fintstwmdfile = getWriteModeFromFlag("-" + tmptstwmdfile);
    finmdlswmdfile = getWriteModeFromFlag("-" + tmpmdlswmdfile);
    #print(f"fintstwmdfile = {fintstwmdfile}");
    #print(f"finmdlswmdfile = {finmdlswmdfile}");

    #now attempt to get it from the command line here...
    #need to know if one or both or none is present on the command line
    tstwmdincmd = False;
    mdlswmdincmd = False;
    inittstwmdcmdval = None;
    initmdlswmdcmdval = None;
    if (len(sys.argv) == 4 or len(sys.argv) == 6):
        #2 and 4 indicate type and cannot be the same (needs validated)
        #3 and 5 are the write mode values given on the command prompt (needs validated)
        #if it is in the write or append list, this is good
        #else set the write mode to be block.
        tpa = sys.argv[2];
        wmda = (sys.argv[3] if (myvalidator.isListAInListB([sys.argv[3]], allflgs)) else 'b');
        #print(f"tpa = sys.argv[2] = {tpa}");
        #print(f"wmda = sys.argv[3] = {wmda}");
        
        #if type is in the test file, then the write mode is only allowed to be write or block
        #it cannot be on the append list
        myvalidator.itemMustBeOneOf(tpa, allfileflgs, varnm="tpa=sys.argv[2]");
        if (myvalidator.isListAInListB([tpa], tstflgs)):
            tstwmdincmd = True;
            if (myvalidator.isListAInListB([wmda], apndflgs)): raise ValueError(apndmderrmsg);
            inittstwmdcmdval = ('w' if (myvalidator.isListAInListB([wmda], wrteflgs)) else 'b');
        else: #if (myvalidator.isListAInListB([tpa], mdlsflgs)):
            mdlswmdincmd = True;
            initmdlswmdcmdval = getWriteModeFromFlag(wmda);

        if (len(sys.argv) == 6):
            tpb = sys.argv[4];
            wmdb = (sys.argv[5] if (myvalidator.isListAInListB([sys.argv[5]], allflgs)) else 'b');
            #print(f"tpb = sys.argv[4] = {tpb}");
            #print(f"wmdb = sys.argv[5] = {wmdb}");

            #if type is in the test file, then the write mode is only allowed to be write or block
            #it cannot be on the append list
            myvalidator.itemMustBeOneOf(tpb, allfileflgs, varnm="tpa=sys.argv[4]");
            if (myvalidator.isListAInListB([tpb], tstflgs)):
                tstwmdincmd = True;
                if (myvalidator.isListAInListB([wmdb], apndflgs)): raise ValueError(apndmderrmsg);
                inittstwmdcmdval = ('w' if (myvalidator.isListAInListB([wmdb], wrteflgs)) else 'b');
            else: #if (myvalidator.isListAInListB([tpb], mdlsflgs)):
                mdlswmdincmd = True;
                initmdlswmdcmdval = getWriteModeFromFlag(wmdb);
    #print(f"tstwmdincmd = {tstwmdincmd}");
    #print(f"mdlswmdincmd = {mdlswmdincmd}");
    #print(f"inittstwmdcmdval = {inittstwmdcmdval}");
    #print(f"initmdlswmdcmdval = {initmdlswmdcmdval}");
    
    tmptstwmdcmdval = (inittstwmdcmdval if tstwmdincmd else 'b');
    tmpmdlswmdcmdval = (initmdlswmdcmdval if mdlswmdincmd else 'b');
    #print(f"tmptstwmdcmdval = {tmptstwmdcmdval}");
    #print(f"tmpmdlswmdcmdval = {tmpmdlswmdcmdval}");

    #print(f"tstwmdincnfgfile = {tstwmdincnfgfile}");
    #print(f"mdlswmdincnfgfile = {mdlswmdincnfgfile}");
    #print(f"fintstwmdfile = {fintstwmdfile}");
    #print(f"finmdlswmdfile = {finmdlswmdfile}");

    fintstwmd = None;
    if (tstwmdincnfgfile and tstwmdincmd):
        fintstwmd = getFinalWriteMode(tmptstwmdcmdval, fintstwmdfile, difftp="a");
    elif (tstwmdincnfgfile and not tstwmdincmd): fintstwmd = "" + fintstwmdfile;
    elif (tstwmdincmd and not tstwmdincnfgfile): fintstwmd = "" + tmptstwmdcmdval;
    else: fintstwmd = 'b';
    print(f"fintstwmd = {fintstwmd}");

    finmdlswmd = None;
    if (mdlswmdincnfgfile and mdlswmdincmd):
        finmdlswmd = getFinalWriteMode(tmpmdlswmdcmdval, finmdlswmdfile, difftp="a");
    elif (mdlswmdincnfgfile and not mdlswmdincmd): finmdlswmd = "" + finmdlswmdfile;
    elif (mdlswmdincmd and not mdlswmdincnfgfile): finmdlswmd = "" + tmpmdlswmdcmdval;
    else: finmdlswmd = 'b';
    print(f"finmdlswmd = {finmdlswmd}");

    mytstusewrite = (fintstwmd == 'w');
    print(f"mytstusewrite = {mytstusewrite}");

    genFullModelsScriptAndWriteItNow(nwmdlsfnm, finmdlswmd, nmdlsfilelines);
    genFullTestFileScriptAndWriteItNow(nwtstfnm, nwtstfilelines, useovrwrte=mytstusewrite);
    print("DONE WITH THE MASTER GENERATOR! PROGRAM FINISHED SUCCESSFULLY!");
