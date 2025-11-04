from myorm.myvalidator import myvalidator;
from myorm.mybase import mybase;
from myorm.modelsgenerator import getClassNamesListFlags;
import sys;
import traceback;
#cannot insert None or [] in the middle of a list or at all
#otherwise it inserts it at the index except in one case: 
#if nvals is not empty and mlist is then it ignores the index and returns nvals
def insertListValsToList(mlist, nvals, thei, remi=True):
    myvalidator.varmustbeboolean(remi, "remi");
    if (myvalidator.isvaremptyornull(nvals)):
        if (mlist == None): return None;
        elif (len(mlist) < 1): return [];
        else: return [item for item in mlist];
    if (myvalidator.isvaremptyornull(mlist)):
        if (nvals == None): return None;
        elif (len(nvals) < 1): return [];
        else: return [item for item in nvals];
    myvalidator.valueMustBeInMinAndMaxRange(thei, 0, len(mlist) - 1, "thei");
    nwlist = ([] if (thei < 1) else [mlist[mi] for mi in range(len(mlist)) if mi < thei]);
    for oi in range(len(nvals)): nwlist.append(nvals[oi]);
    nski = (thei + 1 if (remi) else thei);
    for ki in range(nski, len(mlist)): nwlist.append(mlist[ki]);
    return nwlist;

def genClassImportLines(clslist, fnms):
    #from filename import classname;
    myvalidator.varmustnotbeempty(fnms, "fnms");
    myvalidator.varmustnotbeempty(clslist, "clslist");
    errmsg = "the file names list has too many or too few items, it must have at least one name, or ";
    errmsg += "have the same number as classes!";
    if (len(fnms) == 1 or len(fnms) == len(clslist)): pass;
    else: raise ValueError(errmsg);
    for fnm in fnms: myvalidator.stringMustHaveAtMinNumChars(fnm, 1, varnm="fnm");
    for clsnm in clslist: myvalidator.stringMustHaveAtMinNumChars(clsnm, 1, varnm="clsnm");
    baseline = None;
    if (len(fnms) == 1): baseline = "from " + fnms[0] + " import ";
    elif (len(fnms) == len(clslist)): pass;
    else: raise ValueError(errmsg);
    if (myvalidator.isvaremptyornull(baseline)):
        return ["from " + fnms[i] + " import " + clslist[i] + ";" for i in range(len(clslist))];
    else: return [baseline + clsnm + ";" for clsnm in clslist];

def removeNewLineFromEndOfLine(line):
    if (line == None): return None;
    elif (len(line) < 1): return "";
    myvalidator.stringMustHaveAtMinNumChars(line, 1, "line");
    if (line.endswith("\n")): return "" + line[0:len(line) - 1];
    else: return "" + line;

def getLinesFromFile(fnm, noext=True):
    myvalidator.varmustbeboolean(noext, varnm="noext");
    myvalidator.stringMustHaveAtMinNumChars(fnm, 1, varnm="fnm");
    mlines = None;
    finfnm = ("" + fnm + ".py" if noext else "" + fnm);
    with open(finfnm, 'r') as mfile:
        mlines = mfile.readlines();
        mfile.close();
    return [removeNewLineFromEndOfLine(line) for line in mlines];

def getIndexOfOptOnList(argslist, optslist):
    myvalidator.varmustnotbeempty(argslist, "argslist");
    if (len(argslist) < 3): raise ValueError("argslist must have at least 3 items on it!");
    clsi = -1;
    for n in range(2, len(argslist)):
        carg = argslist[n];
        if (myvalidator.isListAInListB([carg], optslist)):
            clsi = n;
            break;
    return clsi;

def getFileNamesFlags():
    return ["-fnms", "-filenames", "-files", "-fns", "-f", "-FNMS", "-fileNames", "-FileNames",
            "-FILENAMES","-FILES", "-FNS", "-F"];

#python -m myorm.addclasslisttotestfile testfile searchstrorflgusedefault classlistflags
# classlist filenameflags fnms
#python -m myorm.addclasslisttotestfile testfile classlistflags classlist filenameflags fnms
if __name__ == "__main__":
    #print(f"Total Arguments: {len(sys.argv)}");
    #print(sys.argv[0]);
    #print(sys.argv[1:]);
    #print("the rest of the script!");

    #print(genClassImportLines(["game", "user", "info"], ["models"]));
    #print(genClassImportLines(["game", "user", "info"], ["game", "user", "info"]));
    #print(genClassImportLines(["game", "user", "info"], ["game", "user"]));#error out

    #print(insertListValsToList(None, ["otherthing1", "otherthing2", "otherthing4", "otherthing3"], 1));
    #print(insertListValsToList(["item1", "item2", "item3"], None, 1));
    #print(insertListValsToList(["item1", "item2", "item3"],
    #                    ["otherthing1", "otherthing2", "otherthing4", "otherthing3"], 1));
    clsopts = getClassNamesListFlags();
    fmnsopts = getFileNamesFlags();
    print(clsopts);
    print(fmnsopts);

    fnmargmsg = "1. file name (no extension) where the generated test file or startup script is ";
    fnmargmsg += "located.\n";

    mnerrmsg = "invalid number of arguments! You must call this program as follows: ";
    mnerrmsg += "" + fnmargmsg + "2. the line to search for and to replace with the generated list of ";
    mnerrmsg += "imports OR the line index to replace.\n3. this is a class list indicator and must be ";
    mnerrmsg += "on the following list and only one of them: " + str(clsopts) + ".\n";
    mnerrmsg += "4. the list of DB model classes each separated by a space. There must be at least ";
    mnerrmsg += "one.\n5. the file names indicator option and must be on the following list and only ";
    mnerrmsg += "one of them: " + str(fmnsopts) + ".\n6. and finally the list of file names. There ";
    mnerrmsg += "must be at least one file name.\nAlternatively it must have the following arguments:\n";
    mnerrmsg += "" + fnmargmsg + "2. this is a class list indicator and must be on the following list ";
    mnerrmsg += "and only one of them: " + str(clsopts) + ".\n";
    mnerrmsg += "3. the list of DB model classes each separated by a space. There must be at least ";
    mnerrmsg += "one.\n4. the file names indicator option and must be on the following list and only ";
    mnerrmsg += "one of them: " + str(fmnsopts) + ".\n5. and finally the list of file names. There ";
    mnerrmsg += "must be at least one file name.\nOtherwise this will not work!";
    if (len(sys.argv) < 6): raise ValueError(mnerrmsg);

    dfline = "#import all of your DB model classes here before you set them up on the next line";
    fnm = sys.argv[1];
    
    mclerrmsg = "missing class list indicator " + str(clsopts) + " it must be found at or after the ";
    mclerrmsg += "test file name, but it was not!";
    mfnmserrmsg = "missing file names list indicator " + str(fmnsopts) + " it must be found after the ";
    mfnmserrmsg += "class list indicator and after the class list, but it was not!";
    
    mlnierrmsg = "negative line index not allowed here!\n\n" + mnerrmsg;

    clsi = getIndexOfOptOnList(sys.argv, clsopts);
    if (clsi < 2): raise ValueError(mclerrmsg + "\n\n" + mnerrmsg);
    fnmsi = getIndexOfOptOnList(sys.argv, fmnsopts);
    if (fnmsi < clsi or fnmsi < 3): raise ValueError(mfnmserrmsg + "\n\n" + mnerrmsg);
    clslist = sys.argv[clsi + 1:fnmsi];
    fnms = sys.argv[fnmsi + 1:];
    print(f"clslist = {clslist}");
    print(f"fnms = {fnms}");

    finsrchstr = ("" + dfline if (clsi == 2) else myvalidator.myjoin(" ", sys.argv[2:clsi])); 
    mlines = getLinesFromFile(fnm);
    print(f"finsrchstr = {finsrchstr}");
    #print(f"mlines = {mlines}");
    
    slni = -1;
    if (str(finsrchstr).isnumeric()): slni = int(finsrchstr);
    elif (str(finsrchstr)[0] == '-' and str(finsrchstr)[1:].isnumeric()): raise ValueError(mlnierrmsg);
    else:
        try:
            slni = mlines.index(finsrchstr + "\n");
        except Exception as ex:
            traceback.print_exc();
            raise ValueError(mnerrmsg);
    print(f"slni = {slni}");

    nilines = None;
    try:
        nilines = genClassImportLines(clslist, fnms);
    except Exception as ex:
        traceback.print_exc();
        raise ValueError(mnerrmsg);
    finlines = insertListValsToList(mlines, nilines, slni, remi=True);
    mybase.overwriteifmyfileexistswritelines(fnm + ".py", finlines, dscptrmsg="test file script");
    print("DONE SUCCESSFULLY GENERATED THE FULL TEST FILE SCRIPT!");
