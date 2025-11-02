#from myorm.mybase import mybase;
#from myorm.mycol import mycol;
#from myorm.myvalidator import myvalidator;
#from myorm.myrefcol import myrefcol;
#validates = mycol.validates;
#mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN*, ERROR, or DISABLED.
#now we need a list of the class names
#so we can do class classname(mybase):
#each class needs tablename=None, spot for multiargs mymulticolargs=None, #tableargs=None;
#may also have to_dict, repr, and validator methods
#
#each class will look something like:
#imports here at the top of the file only once needed for all classes
#class classname(mybase):
#    tablename = None;
#
#    #cols here
#
#    mymultiargs = None;#needs to be near cols
#    #tableargs = None;#needs to be near cols
#
#    #everything below this point is optional
#
#    #validator example methods (often a lot of these and they need to be near cols)
#
#    #params comment for to_dict and repr
#    #repr def
#    
#    #todict def
#
#need to get the class names from the user on the command line
#need to know if they just want to add class names only to an existing file or create a new one (default).
#we want the options to tell it to include:
#validatorsonly, repronly, todictonly, or bothreprandtodict or allthreeoptions
#-allopts, -all, -bothbutnovalidators, -repr, -todict, -validators, -reprandv, -todictandv
#
#append options = [-addonly, -add, -a, -append, -appendonly, 1];
#overwrite options = [-overwrite, -writeover, -ow, -write, -w];
#classlist options = [-cl, -classlist, -models, -mdls];
#these are not all of them
#python -m myorm.modelsgenerator newfilename [appendopts] classnameslist [optionslist]
#python -m myorm.modelsgenerator newfilename [overwriteopts] classnameslist [optionslist]
#python -m myorm.modelsgenerator newfilename classnameslist [optionslist]
#python -m myorm.modelsgenerator [appendopts] classnameslist [optionslist]
#python -m myorm.modelsgenerator [overwriteopts] classnameslist [optionslist]
#python -m myorm.modelsgenerator [classlistopts] classnameslist [optionslist]
#on the one only with the class list either create a new file or block.

from myorm.myvalidator import myvalidator;
from myorm.mybase import mybase;
import sys;
import traceback;
def getTopImportLines():
    return ["from myorm.mybase import mybase;", "from myorm.mycol import mycol;",
        "from myorm.myvalidator import myvalidator;", "from myorm.myrefcol import myrefcol;",
        "validates = mycol.validates;",
        "#mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN*, ERROR, or DISABLED."];

def addNumTabsToLine(initline, numtbs):
    myvalidator.varmustbeanumber(numtbs, "numtbs");
    if (initline == None): return addNumTabsToLine("", numtbs);
    if (numtbs < 1): return initline;
    indentstr = "";
    for i in range(numtbs): indentstr += "    ";
    return indentstr + initline;

def addNumTabsToAllLines(numtbs, alines):
    #print(f"numtbs = {numtbs}");
    #print(f"alines = {alines}");
    if (alines == None): return None;
    elif (len(alines) < 1): return [];
    else: return [addNumTabsToLine(oline, numtbs) for oline in alines];

def getReprAndToDictParameterDescriptions(numtbs=0, useboth=False):
    myvalidator.varmustbeboolean(useboth, "useboth");
    toplines = (["#for both to_dict and repr methods:", "#"] if useboth else []);
    initlines = ["#exobjslist is the exclusive object rules list (is a list of strings)",
            "#the usesafelistonly is a boolean variable which tells it if we use the safe list only or",
            "#serialize all attributes on the myattrs list.",
            "#if myattrs is not None IE you provided valid attributes then only these will be included",
            "#otherwise all of them or the only list will be provided.",
            "#lastly the prefix string tracks what object and attribute ... where we are.",
            "#this helps avoid a circular reference error.",
            "#due to the way this method is called, it is best have it declared like this."];
    templines = (["" + line for line in toplines] if 0 < len(toplines) else []);
    for miline in initlines: templines.append("" + miline);
    return addNumTabsToAllLines(numtbs, templines);

def getReprMethodExampleLines(numtbs=0):
    initlines = ["#def __repr__(self, exobjslist=None, usesafelistonly=False):",
            "#   return self.__simplerepr__(displystringsarr,",
            "#                       myattrs=classattributesarruse_valueforcols,",
            "#                       ignoreerr=True, strstarts=True, exobjslist=exobjslist,",
            "#                       usesafelistonly=usesafelistonly);"];
    return addNumTabsToAllLines(numtbs, initlines);

def getToDictMethodExampleLines(numtbs=0):
    retsupline = "#    return super().__to_dict__(myattrs=myattrs, exobjslist=nwlist, ";
    retsupline += "usesafelistonly=usesafelistonly,";
    lines = ["#def __to_dict__(self, myattrs=None, exobjslist=None, usesafelistonly=False, prefix=\"\"):",
            "#    nwlist = myvalidator.combineTwoLists(exobjslist, exrules);", retsupline,
            "#                               prefix=prefix);"];
    return addNumTabsToAllLines(numtbs, lines);

def getValidatorsExampleLines(numtbs=0):
    retpt = "): return True;#return False if not valid or error";
    initlines = ["#@validates(\"colname\")",
                "#def isvalidcolname(self, key, val" + retpt,
                "#", "#@validates(\"colnamea\", \"colnameb\", ...)",
                "#def arecolsaandbvalid(self, keys, values" + retpt];
    return addNumTabsToAllLines(numtbs, initlines);

def getOptsFlagsDict():
    #get the option flags lists here then combine them
    usealloptslist = getMyAllOnlyOptsFlags();
    novflagslist = getMyBothNoValidatorFlags();
    myreprflagslist = getMyToDictOrReprOnlyFlags(True);
    mytodictflagslist = getMyToDictOrReprOnlyFlags(False);
    myvflagslist = getMyValidatorsOnlyFlags();
    myreprandvflagslist = getToDictOrReprAndValidatorsFlags(True);
    mytodictandvflagslist = getToDictOrReprAndValidatorsFlags(False);
    
    #start combining the options lists here to make a list that has them all on it
    alloptsandnovflagslist = myvalidator.combineTwoLists(usealloptslist, novflagslist, nodups=True);
    myreprandtodictflagslist = myvalidator.combineTwoLists(myreprflagslist, mytodictflagslist,
                                                            nodups=True);
    alloptwithnovslist = myvalidator.combineTwoLists(novflagslist, myreprandtodictflagslist,
                                                        nodups=True);
    myreprtodictandvflagslist = myvalidator.combineTwoLists(myreprandvflagslist,
                                                            mytodictandvflagslist, nodups=True);
    alloptsnovandmyreprandtodictsonlyflagslist = myvalidator.combineTwoLists(
                                                    alloptsandnovflagslist, myreprandtodictflagslist,
                                                    nodups=True);
    myreprtodictandvflagsandvflagsonlylist = myvalidator.combineTwoLists(myreprtodictandvflagslist,
                                                                            myvflagslist, nodups=True);
    allopts = myvalidator.combineTwoLists(alloptsnovandmyreprandtodictsonlyflagslist,
                                            myreprtodictandvflagsandvflagsonlylist, nodups=True);
    return {"usealloptslist": usealloptslist, "novflagslist": novflagslist,
            "myreprflagslist": myreprflagslist, "mytodictflagslist": mytodictflagslist,
            "myvflagslist": myvflagslist, "myreprandvflagslist": myreprandvflagslist,
            "mytodictandvflagslist": mytodictandvflagslist,
            "alloptsandnovflagslist": alloptsandnovflagslist,
            "myreprandtodictflagslist": myreprandtodictflagslist,
            "alloptwithnovslist": alloptwithnovslist,
            "myreprtodictandvflagslist": myreprtodictandvflagslist,
            "alloptsnovandmyreprandtodictsonlyflagslist": alloptsnovandmyreprandtodictsonlyflagslist,
            "myreprtodictandvflagsandvflagsonlylist": myreprtodictandvflagsandvflagsonlylist,
            "allopts": allopts};

#classnameslist is a list of class string names
def genFileLines(classlist, optslist, opsflagsinfoobj, tnms=None):
    merrmsgptb = ") must be a valid variable name, but it was not!";
    merrmsgb = "invlaid number of options on the options list! There must be either no options, ";
    merrmsgb += "only one option, or there must be the same number of options as there are classes ";
    merrmsgb += "on the classlist, but this was not the case!";
    merrmsgc = "invlaid number of tablenames on the tablenames list! There must be either no tablenames ";
    merrmsgc += "or there must be the same number of tablenames as there are classes ";
    merrmsgc += "on the classlist, but this was not the case!";
    rkys = ["allopts", "alloptsandnovflagslist", "usealloptslist", "myvflagslist", "alloptwithnovslist",
            "myreprflagslist", "mytodictflagslist"];
    myvalidator.objvarmusthavethesekeysonit(opsflagsinfoobj, rkys, varnm="opsflagsinfoobj");
    if (myvalidator.isvaremptyornull(classlist)): return [];
    else:
        for mc in classlist:
            myvalidator.varmustbethetypeonly(mc, str, "myclassnamestr");
            if (str(mc).isidentifier()): pass;
            else: raise ValueError("the class name (" + mc + merrmsgptb);
        #print(f"classlist = {classlist}");
        #print(f"tnms = {tnms}");
        #print(f"optslist = {optslist}");
        
        usenoopts = myvalidator.isvaremptyornull(optslist);
        notnms = myvalidator.isvaremptyornull(tnms);
        useonlyoneopt = False;
        if (usenoopts): pass;
        elif (len(classlist) == len(optslist)): pass;
        elif (len(optslist) == 1): useonlyoneopt = True;
        else: raise ValueError(merrmsgb);
        if (notnms): pass;
        elif (len(classlist) == len(tnms)): pass;
        else: raise ValueError(merrmsgc);
        #print(f"notnms = {notnms}");
        #print(f"usenoopts = {usenoopts}");
        #print(f"useonlyoneopt = {useonlyoneopt}");

        noneoptslist = ["none", "None", "NONE"];
        if (notnms): pass;
        else: myvalidator.listMustContainUniqueValuesOnly(tnms, ignorelist=noneoptslist, varnm="tnms");
        myvalidator.listMustContainUniqueValuesOnly(classlist, varnm="classlist");

        allopts = opsflagsinfoobj[rkys[0]];
        alloptsandnovflagslist = opsflagsinfoobj[rkys[1]];
        usealloptslist = opsflagsinfoobj[rkys[2]];
        myvflagslist = opsflagsinfoobj[rkys[3]];
        alloptwithnovslist = opsflagsinfoobj[rkys[4]];
        myreprflagslist = opsflagsinfoobj[rkys[5]];
        mytodictflagslist = opsflagsinfoobj[rkys[6]];

        if (usenoopts): pass;
        else:
            for coptstr in optslist:
                if (coptstr in noneoptslist): pass;
                else: myvalidator.itemMustBeOneOf(coptstr, allopts, "coptstr");

        linesperclass = [];
        mynmtbs = 1;
        reprlines = ([] if usenoopts else getReprMethodExampleLines(numtbs=mynmtbs));
        mdictlines = ([] if usenoopts else getToDictMethodExampleLines(numtbs=mynmtbs));
        vldatorlines = ([] if usenoopts else getValidatorsExampleLines(numtbs=mynmtbs));
        #print(f"vldatorlines = {vldatorlines}");
        #print(f"mdictlines = {mdictlines}");
        #print(f"reprlines = {reprlines}");

        for i in range(len(classlist)):
            mc = "" + classlist[i];
            tnm = ("None" if notnms else "" + tnms[i]);
            mclines = ["class " + mc + "(mybase):", "    tablename = " + tnm + ";", "    ",
                       "    #cols here", "    ", "    mymulticolargs = None;", "    #tableargs = None;"];
            #print(f"i = {i}");
            #print(f"mc = {mc}");
            #print(f"tnm = {tnm}");

            copt = (None if (usenoopts) else (optslist[0] if useonlyoneopt else optslist[i]));
            #print(f"copt = {copt}");
            #print(f"allopts = {allopts}");

            if (usenoopts or copt in noneoptslist): pass;
            else:
                usingall = myvalidator.isListAInListB([copt], usealloptslist);
                useboth = myvalidator.isListAInListB([copt], alloptsandnovflagslist);#all, and novs lists
                usingnone = myvalidator.isListAInListB([copt], myvflagslist);#only validators
                usingnovalidators = myvalidator.isListAInListB([copt], alloptwithnovslist);
                initdictmsglines = ([] if usingnone else
                    getReprAndToDictParameterDescriptions(numtbs=mynmtbs, useboth=useboth));
                #print(f"usingall = {usingall}");
                #print(f"useboth = {useboth}");
                #print(f"usingnone = {usingnone}");
                #print(f"usingnovalidators = {usingnovalidators}");
                
                #validator methods, comment for to_dict and repr, then to_dict, then repr
                if (usingnovalidators and not usingall): pass;
                else:
                    mclines.append("");
                    for mline in vldatorlines: mclines.append("" + mline);

                #if using repr, to_dict, both, or all:
                if (usingnone): pass;
                else:
                    #must be using at least one repr or to_dict
                    mclines.append("");
                    for mline in initdictmsglines: mclines.append("" + mline);
                    mclines.append("");
                    if (usingall or useboth or myvalidator.isListAInListB([copt], myreprflagslist)):
                        for mline in reprlines: mclines.append("" + mline);
                        if (usingall or useboth): mclines.append("");
                    if (usingall or useboth or myvalidator.isListAInListB([copt], mytodictflagslist)):
                        for mline in mdictlines: mclines.append("" + mline);
            
            #on the final list we want new lines in between:
            #1. params for, 2. the repr, 3. todict, 4. and the validators
            #print(f"mclines = {mclines}");
            #print("mclines:");
            #for mline in mclines: print(mline);
            #raise ValueError("NOT DONE YET 10-28-2025 10:38 PM MST!");

            if (i + 1 < len(classlist)): mclines.append("");
            linesperclass.append(mclines);
        return ["" + mline for marr in linesperclass for mline in marr];

def getAppendFlags():
    return ["-addonly", "-AddOnly", "-ADDONLY", "-add", "-ADD", "-a", "-A", "-append", "-Append",
            "-APPEND", "-appendonly", "-AppendOnly", "-APPENDONLY", "1"];

def getOverWriteFlags():
    return ["-overwrite", "-OverWrite", "-OVERWRITE", "-writeover", "-WriteOver", "-WRITEOVER",
            "-ow", "-OW", "-write", "-Write", "-WRITE", "-w", "-W", "0"];

def getClassNamesListFlags():
    return ["-cl", "-CL", "-classlist", "-ClassList", "-CLASSLIST", "-models", "-Models", "-MODELS",
            "-mdls", "-MDLS"];

def getMyAllOnlyOptsFlags():
    return ["-allopts", "-alloptions", "-all", "-allOpts", "-allOptions", "-AllOpts", "-AllOptions",
            "-ALLOPTS", "-ALLOPTIONS", "-a", "-A"];

def getMyBothNoValidatorFlags():
    return ["-bothbutnovalidators", "-bothButNoValidators", "-BothButNoValidators",
            "-BOTHBUTNOVALIDATORS", "-bothnovalidators", "-bothNoValidators", "-BothNoValidators",
            "-BOTHNOVALIDATORS", "-bothnovs", "-bothNoVs", "-BothNoVs", "-BOTHNOVS", "-bothnov",
            "-bothNoV", "-BothNoV", "-BOTHNOV"];

def getMyToDictOrReprOnlyFlags(userepr):
    myvalidator.varmustbeboolean(userepr, "userepr");
    return (["-repr", "-REPR", "-str", "-STR"] if userepr else
            ["-todict", "-toDict", "-ToDict", "-TODICT", "-to_dict", "-to_Dict", "-To_Dict", "-TO_DICT"]);

def getMyValidatorsOnlyFlags(): return ["-validators", "-VALIDATORS", "-v", "-V"];

def getToDictOrReprAndValidatorsFlags(userepr):
    myvalidator.varmustbeboolean(userepr, "userepr");
    todictpostfixs = ["andv", "AndV", "ANDV", "andvalidators", "AndValidators", "ANDVALIDATORS",
                      "v", "V", "validators", "VALIDATORS"];
    reprpostfixs = ["andv", "ANDV", "v", "V", "validators", "VALIDATORS"];
    initmlist = getMyToDictOrReprOnlyFlags(userepr);
    if (userepr):
        #add first to even indexs 0 and 2,
        #add second to odd indexes 1 and 3,
        #add third to even indexes 0 and 2,
        #add fourth to odd indexes 1 and 3.
        return ["" + initmlist[i] + reprpostfixs[ri] for ri in range(len(reprpostfixs))
                    for i in range(len(initmlist)) if (i %2 == ri %2)];
    else:
        return ["" + wda + wdb for wda in initmlist for wdb in todictpostfixs
                if myvalidator.doesCaseMatch(wda, wdb)];

def getOptListStartIndex(margslist, clssi):
    if (myvalidator.isvaremptyornull(margslist)): return -1;
    myvalidator.valueMustBeInMinAndMaxRange(clssi, 2, len(margslist), "clssi");
    #print(f"sindex = {clssi} and args are:");
    #print(margslist);
    
    optsi = -1;
    for i in range(clssi, len(margslist)):
        carg = margslist[i];
        if (carg.startswith("-")):
            optsi = i;
            break;
    #print(f"optsi = {optsi}");
    return optsi;

if __name__ == "__main__":
    #print(f"Total Arguments: {len(sys.argv)}");
    #print(sys.argv[0]);
    #print(sys.argv[1:]);
    #print("the rest of the script!");
    #if arg[2] is a flag startswith -, then this is in the format:
    #newfile [append or overwrite flag] classlist [optional options_for_each_class_or_all_classes]
    #if arg[1] is a flag startswith -, then this is in the format:
    #[append, overwrite, or classlist flag] classlist [optional options_for_each_class_or_all_classes]
    #otherwise in the format: newfile classlist [optional options_for_each_class_or_all_classes]
    #print(getToDictOrReprAndValidatorsFlags(True));
    #print(getToDictOrReprAndValidatorsFlags(False));
    apndflgs = getAppendFlags();
    wrteflgs = getOverWriteFlags();
    clsnmslistflgs = getClassNamesListFlags();
    apndwrteflgs = myvalidator.combineTwoLists(apndflgs, wrteflgs, nodups=True);
    allflgs = myvalidator.combineTwoLists(apndwrteflgs, clsnmslistflgs, nodups=True);
    optsdictobj = getOptsFlagsDict();
    nwdffnm = "mymodels";
    optsmsg = "you give it at least no options, or give it only one, or one per class name, and ";
    optsmsg += "your option must be on the following list: " + str(optsdictobj["allopts"]) + "!\n";
    altermsg = "Alternatively: the following arguments are required:\n";

    merrmsg = "invalid number of arguments! This program needs at least one class name!\n";
    merrmsg += "the following arguments are required:\n1. new file name (no extension).\n";
    merrmsg += "2. you need to give it one of the append " + str(apndflgs) + " or overwrite flags ";
    merrmsg += str(wrteflgs) + ".\n";
    merrmsg += "3. now you start giving it the name of classes using space as the delimeter ";
    merrmsg += "(assume in a list already)!\n4. " + optsmsg + altermsg;
    merrmsg += "1. new file name (no extension).\n";
    merrmsg += "2. now you start giving it the name of classes using space as the delimeter ";
    merrmsg += "(assume in a list already)!\n3. " + optsmsg + altermsg;
    merrmsg += "1. you need to give it one of the append or overwrite or class names or models list ";
    merrmsg += "flags " + str(clsnmslistflgs) + ".\n2. now you start giving it the name of ";
    merrmsg += "classes using space as the delimeter (assume in a list already)! (since no file name ";
    merrmsg += "was given '" + nwdffnm + "' will be used)!\n3. " + optsmsg;
    merrmsg += "Otherwise it will not work!";
    
    wrtemd = None;
    newfnm = None;
    clsi = -1;
    if (4 < len(sys.argv) and sys.argv[2].startswith("-")):
        myvalidator.itemMustBeOneOf(sys.argv[2], apndwrteflgs, "the flag sys.argv[2]");
        useappendflg = (myvalidator.isListAInListB([sys.argv[2]], apndflgs));   
        clsi = 3;
        wrtemd = ("a" if useappendflg else "w");
        newfnm = "" + sys.argv[1];
    elif (3 < len(sys.argv) and sys.argv[1].startswith("-")):
        myvalidator.itemMustBeOneOf(sys.argv[1], allflgs, "the flag sys.argv[1]");
        useappendflg = (myvalidator.isListAInListB([sys.argv[1]], apndflgs));
        useowriteflg = (myvalidator.isListAInListB([sys.argv[1]], wrteflgs));
        wrtemd = ("a" if useappendflg else ("w" if useowriteflg else "b"));
        clsi = 2;
        newfnm = "" + nwdffnm;
    elif (3 < len(sys.argv)):
        clsi = 2;
        newfnm = "" + sys.argv[1];
        wrtemd = "b";
    else: raise ValueError(merrmsg);

    optsi = getOptListStartIndex(sys.argv, clsi);
    classlist = (sys.argv[clsi:] if optsi < clsi else sys.argv[clsi:optsi]);
    optslist = (None if optsi < clsi else sys.argv[optsi:]);
    
    clslines = None;
    try:
        clslines = genFileLines(classlist, optslist, optsdictobj, tnms=None);
    except Exception as ex:
        traceback.print_exc();
        raise ValueError(merrmsg);
    
    mflines = (clslines if (wrtemd == "a") else
               myvalidator.combineTwoLists(getTopImportLines(), clslines, nodups=False));
    myfunc = (mybase.appendifmyfileexistswritelines if (wrtemd == "a") else
              (mybase.overwriteifmyfileexistswritelines if (wrtemd == "w") else
               mybase.blockifmyfileexistswritelines));
    myfunc(newfnm + ".py", mflines, dscptrmsg="models file script");
    print("DONE SUCCESSFULLY GENERATED THE MODELS FILE SCRIPT!");
