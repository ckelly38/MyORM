from myorm.myvalidator import myvalidator;
from myorm.classliststartupgen import getLinesFromFile;
from myorm.modelsgenerator import getOptsFlagsDict;
import sys;

def getAcceptedTrueOrFalseAnswers():
    return ["false", "False", "FALSE", "NO", "no", "0", "true", "True", "TRUE", "YES", "Yes", "yes", "1"];

def getTrueOrFalseBoolFromString(mval):
    tfans = getAcceptedTrueOrFalseAnswers();
    myvalidator.itemMustBeOneOf(mval, tfans, varnm="mval");
    mytfi = tfans.index(mval);
    return (False if mytfi < 6 else True);

def boolValIsValidForLine(lnum, flines):
    myvalidator.varmustnotbeempty(flines, varnm="flines");
    myvalidator.valueMustBeInMinAndMaxRange(lnum, 0, len(flines) - 1, varnm="lnum");
    tfans = getAcceptedTrueOrFalseAnswers();
    tmpsecpt = flines[lnum][flines[lnum].index(": ")+2:];
    myvnm = "the second part of line " + str(lnum + 1);
    omerrmsg = "config file was wrong on " + myvnm + " because it was not a true or false value!";
    if (tmpsecpt.isalpha()):
        myvalidator.itemMustBeOneOf(tmpsecpt, tfans, varnm=myvnm);
        return True;
    else: raise ValueError(omerrmsg);

def stringValMustBeAlnumOrUnderscores(lnum, flines):
    myvalidator.varmustnotbeempty(flines, varnm="flines");
    myvalidator.valueMustBeInMinAndMaxRange(lnum, 0, len(flines) - 1, varnm="lnum");
    secptofline = flines[lnum][flines[lnum].index(": ")+2:];
    myvnm = "line " + str(lnum + 1) + " on config file";
    myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(secptofline, varnm=myvnm);
    return True;

def areLinesInModelFormat(flines, si):
    #now the rest must meet the following format:
    #classnamea, tablenamea: opt or None
    myvalidator.varmustnotbeempty(flines, varnm="flines");
    myvalidator.valueMustBeInMinAndMaxRange(si, 0, len(flines) - 1, varnm="si");
    optsdictobj = getOptsFlagsDict();
    myopts = optsdictobj["allopts"];
    for n in range(si, len(flines)):
        cline = flines[n];
        myvnm = "second part of the line num: " + str(n + 1);
        mstrs = myvalidator.mysplitWithLen(cline, [cline.index(", "), cline.index(": ")], 2, offset=0);
        for cstr in mstrs:
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(cstr, varnm="cstr");
        if (mstrs[2] == "None"): pass;
        else: myvalidator.itemMustBeOneOf(mstrs[2], myopts, varnm=myvnm);
    return True;

def configFileMustBeValid(flines):
    tstgenlinea = "testfile_new_file_name: ";
    tstgenlineb = "usedefaultconfigmodulename: ";
    tstgenlinec = "usenodb: ";
    tstgenlined = "usedefaultdbobjname: ";
    tstgenlinee = "configmodulename: ";
    tstgenlinef = "dbobjname: ";

    mdlsgenlinea = "models_class_new_file_name: ";
    mdlsgenlineb = "models_class_list:";
    mdlsgenlinec = "classnamea, tablenamea: None";

    merrmsgblvl = "since we are not using a database, the default name must be used, but it was not ";
    merrmsgblvl += "therefore there is a problem with config line 4!";
    
    if (flines[0].index(tstgenlinea) == 0): stringValMustBeAlnumOrUnderscores(0, flines);
    else: raise ValueError("config file was wrong on line 1!");
    if (flines[1].index(tstgenlineb) == 0): boolValIsValidForLine(1, flines);
    else: raise ValueError("config file was wrong on line 2!");
    if (flines[2].index(tstgenlinec) == 0): boolValIsValidForLine(2, flines);
    else: raise ValueError("config file was wrong on line 3!");
    undbval = getTrueOrFalseBoolFromString(flines[2][flines[2].index(": ")+2:]);
    offset = 0;
    if (undbval):
        #we do not need line d and f to be present, but they still can be
        #however if usedefaultdbobjname: is present then it must be true.
        if (tstgenlined in flines[3]):
            boolValIsValidForLine(3, flines);
            mbval = getTrueOrFalseBoolFromString(flines[3][flines[3].index(": ")+2:]);
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
        else: raise ValueError("config file was wrong on line 4!");
    else:
        if (flines[3].index(tstgenlined) == 0): boolValIsValidForLine(3, flines);
        else: raise ValueError("config file was wrong on line 4!");
        if (flines[4].index(tstgenlinee) == 0): stringValMustBeAlnumOrUnderscores(4, flines);
        else: raise ValueError("config file was wrong on line 5!");
        if (flines[5].index(tstgenlinef) == 0): stringValMustBeAlnumOrUnderscores(5, flines);
        else: raise ValueError("config file was wrong on line 6!");
    if (len(flines[6 + offset]) < 1): pass;
    else: raise ValueError("config file was wrong on line " + str(7 + offset) + "!");
    if (flines[7 + offset].index(mdlsgenlinea) == 0):
        stringValMustBeAlnumOrUnderscores(7 + offset, flines);
    else: raise ValueError("config file was wrong on line " + str(8 + offset) + "!");
    if (flines[8 + offset] == mdlsgenlineb): pass;
    else: raise ValueError("config file was wrong on line " + str(9 + offset) + "!");
    areLinesInModelFormat(flines, 9 + offset);
    return True;

if __name__ == "__main__":
    #make sure the config file is valid
    #then call the other generators
    fnm = sys.argv[1];
    flines = getLinesFromFile(fnm);
    configFileMustBeValid(flines);
    #generate the files...
