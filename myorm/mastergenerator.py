from myorm.myvalidator import myvalidator;
from myorm.classliststartupgen import getLinesFromFile, genClassImportLines;
from myorm.modelsgenerator import getOptsFlagsDict, genFullModelsScriptAndWriteItNow;
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
    origtstkys = ["testfile_new_file_name", "usedefaultconfigmodulename", "usenodb",
                  "usedefaultdbobjname", "configmodulename", "dbobjname"];
    tstgenlinea = "" + origtstkys[0] + ": ";
    tstgenlineb = "" + origtstkys[1] + ": ";
    tstgenlinec = "" + origtstkys[2] + ": ";
    tstgenlined = "" + origtstkys[3] + ": ";
    tstgenlinee = "" + origtstkys[4] + ": ";
    tstgenlinef = "" + origtstkys[5] + ": ";

    mdlsgenlinea = "modelsfile_new_file_name: ";
    mdlsgenlineb = "models_class_list:";
    #mdlsgenlinec = "classnamea, tablenamea: None";#included this line to show formatting
    
    isblkys = "011100";
    fintstkys = ["tstfname", "usedfltcnfgmdlname", "nodb", "usedfltdbobjname", "cnfgmdlname",
                 "dbojbname"];
    #skpkys = "000111";

    merrmsgblvl = "since we are not using a database, the default name must be used, but it was not ";
    merrmsgblvl += "therefore there is a problem with config line 4!";
    
    lineMustHaveTheExpectedPartAtTheSpotAndBeAString(0, tstgenlinea, 0, flines);
    lineMustHaveTheExpectedPartAtTheSpotAndBeABool(1, tstgenlineb, 0, flines);
    lineMustHaveTheExpectedPartAtTheSpotAndBeABool(2, tstgenlinec, 0, flines);
    usdfltmdlcnfgnm = getValAsBoolPartOfString(1, flines);
    undbval = getValAsBoolPartOfString(2, flines);
    offset = 0;
    if (undbval):
        #we do not need line d and f to be present, but they still can be
        #however if usedefaultdbobjname: is present then it must be true.
        if (tstgenlined in flines[3]):
            boolValIsValidForLine(3, flines);
            mbval = getValAsBoolPartOfString(3, flines);
            if (mbval):
                if (tstgenlinee in flines[4] and flines[4].index(tstgenlinee) == 0):
                    stringValMustBeAlnumOrUnderscores(4, flines);
                else: raise ValueError("config file was wrong on line 5!");
                if (tstgenlinef in flines[5] and flines[5].index(tstgenlinef) == 0):
                    stringValMustBeAlnumOrUnderscores(5, flines);
                else: raise ValueError("config file was wrong on line 6!");
            else: raise ValueError(merrmsgblvl);
        elif (tstgenlinee in flines[3]):
            stringValMustBeAlnumOrUnderscores(3, flines);
            offset = -2;
        elif (usdfltmdlcnfgnm and len(flines[3]) < 1): offset = -3;
        else: raise ValueError("config file was wrong on line 4!");
    else:
        lineMustHaveTheExpectedPartAtTheSpotAndBeABool(3, tstgenlined, 0, flines);
        lineMustHaveTheExpectedPartAtTheSpotAndBeAString(4, tstgenlinee, 0, flines);
        lineMustHaveTheExpectedPartAtTheSpotAndBeAString(5, tstgenlinef, 0, flines);
    if (len(flines[6 + offset]) < 1): pass;
    else: raise ValueError("config file was wrong on line " + str(7 + offset) + "!");
    lineMustHaveTheExpectedPartAtTheSpotAndBeAString(7 + offset, mdlsgenlinea, 0, flines);
    if (flines[8 + offset] == mdlsgenlineb): pass;
    else: raise ValueError("config file was wrong on line " + str(9 + offset) + "!");
    mdlsresobj = areLinesInModelFormatAndGetInfoObj(flines, 9 + offset, optsdictobj);
    
    #get the values from the config and split them...
    tstmstrs = [myvalidator.mysplitWithDelimeter(flines[n], ": ", offset=0) for n in range(len(flines))
                if n < 6 + offset];
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
    myobj["offset"] = offset;
    myobj["listlinesi"] = 9 + offset;
    myobj["mdlsresobj"] = mdlsresobj;
    return myobj;

if __name__ == "__main__":
    #make sure the config file is valid
    #then call the other generators
    fnm = sys.argv[1];
    flines = getLinesFromFile(fnm, noext=False);
    print("config file lines are:");
    for cline in flines: print(cline);
    
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
    myusedfltdbnm = (True if myusenodb else resdict["usedefaultdbobjname"]);
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
    
    mytstusewrite = False;
    mdlswrtmd = 'b';

    #genFullModelsScriptAndWriteItNow(nwmdlsfnm, mdlswrtmd, nmdlsfilelines);
    #genFullTestFileScriptAndWriteItNow(nwtstfnm, nwtstfilelines, useovrwrte=mytstusewrite);
    raise ValueError("NOT DONE YET 11-3-2025 10:27 PM MST!");
