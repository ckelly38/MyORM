#from myorm.mybase import mybase;
#from myorm.mycol import mycol;
#from myorm.myvalidator import myvalidator;
#from myorm.myrefcol import myrefcol;
#validates = mycol.validates;
#mycol.setWarnUniqueFKeyMethod('WARN');#user warning of a problem WARN*, ERROR, or DISABLED.
#now we need a list of the class names
#so we can do class classname(mybase):
#each class needs tablename=None, spot for multiargs mymulticolargs=None, #tableargs=None;
#need to get the class names from the user on the command line
#need to know if they just want to add class names only to an existing file or create a new one (default).
#python -m myorm.modelsgenerator newfilename [-addonly, -add, -a, -append, -appendonly, 1] classnameslist
#python -m myorm.modelsgenerator newfilename [-overwrite, -writeover, -ow, -write, -w] classnameslist
#python -m myorm.modelsgenerator newfilename classnameslist
#python -m myorm.modelsgenerator [-addonly, -add, -a, -append, -appendonly, 1] classnameslist
#python -m myorm.modelsgenerator [-overwrite, -writeover, -ow, -write, -w] classnameslist
#python -m myorm.modelsgenerator [-cl, -classlist, -models, -mdls] classnameslist
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

#classnameslist is a list of class string names
def genFileLines(classlist):
    merrmsgptb = ") must be a valid variable name, but it was not!";
    if (myvalidator.isvaremptyornull(classlist)): return [];
    else:
        for mc in classlist:
            myvalidator.varmustbethetypeonly(mc, str, "myclassnamestr");
            if (str(mc).isidentifier()): pass;
            else: raise ValueError("the class name (" + mc + merrmsgptb);
        linesperclass = [];
        for i in range(len(classlist)):
            mc = "" + classlist[i];
            mclines = ["class " + mc + "(mybase):", "    tablename=None;",
                          "    mymulticolargs=None;", "    #tableargs=None;"];
            #if (useopts):
            #add repr method
            #def __repr__(self, exobjslist=None, usesafelistonly=False):
            #   return self.__simplerepr__(["<Camper ", ": ", " is ", " years old>"],
            #                       myattrs=["id_value", "name_value", "myage_value", "signups"],
            #                       ignoreerr=True, strstarts=True, exobjslist=exobjslist,
            #                       usesafelistonly=usesafelistonly);
            
            #add to_dict method
            #exobjslist is the exclusive object rules list (is a list of strings)
            #the usesafelistonly is a boolean variable which tells it if we use the safe list only or
            #serialize all attributes on the myattrs list.
            #if myattrs is not None IE you provided valid attributes then only these will be included
            #otherwise all of them or the only list will be provided.
            #lastly the prefix string tracks what object and attribute ... where we are.
            #this helps avoid a circular reference error.
            #due to the way this method is called, it is best have it declared like this.
            #def __to_dict__(self, myattrs=None, exobjslist=None, usesafelistonly=False, prefix=""):
            #    #nwlist = myvalidator.combineTwoLists(exobjslist, ["activity.signups", "camper.signups"]);
            #    nwlist = myvalidator.combineTwoLists(exobjslist, ["*.signups"]);
            #    return super().__to_dict__(myattrs=myattrs, exobjslist=nwlist, usesafelistonly=usesafelistonly,
            #                               prefix=prefix);

            #add multicol validator and single col validator method
            #    ?;
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

if __name__ == "__main__":
    #print(f"Total Arguments: {len(sys.argv)}");
    #print(sys.argv[0]);
    #print(sys.argv[1:]);
    #print("the rest of the script!");
    #if arg[2] is a flag startswith -, then this is in the format:
    #newfile [append or overwrite flag] classlist
    #if arg[1] is a flag startswith -, then this is in the format:
    #[append, overwrite, or classlist flag] classlist
    #otherwise in the format: newfile classlist
    apndflgs = getAppendFlags();
    wrteflgs = getOverWriteFlags();
    clsnmslistflgs = getClassNamesListFlags();
    apndwrteflgs = myvalidator.combineTwoLists(apndflgs, wrteflgs, nodups=True);
    allflgs = myvalidator.combineTwoLists(apndwrteflgs, clsnmslistflgs, nodups=True);
    nwdffnm = "mymodels";
    merrmsg = "invalid number of arguments! This program needs at least one class name!\n";
    merrmsg += "the following arguments are required:\n1. new file name (no extension).\n";
    merrmsg += "2. you need to give it one of the append " + str(apndflgs) + " or overwrite flags ";
    merrmsg += str(wrteflgs) + ".\n";
    merrmsg += "3. now you start giving it the name of classes using space as the delimeter ";
    merrmsg += "(assume in a list already)!\nAlternatively: the following arguments are required:\n";
    merrmsg += "1. new file name (no extension).\n";
    merrmsg += "2. now you start giving it the name of classes using space as the delimeter ";
    merrmsg += "(assume in a list already)!\nAlternatively: the following arguments are required:\n";
    merrmsg += "1. you need to give it one of the append or overwrite or class names or models list ";
    merrmsg += "flags " + str(clsnmslistflgs) + ".\n2. now you start giving it the name of ";
    merrmsg += "classes using space as the delimeter (assume in a list already)! (since no file name ";
    merrmsg += "was given '" + nwdffnm + "' will be used)!\nOtherwise it will not work!";
    classlist = None;
    wrtemd = None;
    newfnm = None;
    if (3 < len(sys.argv) and sys.argv[2].startswith("-")):
        myvalidator.itemMustBeOneOf(sys.argv[2], apndwrteflgs, "the flag sys.argv[2]");
        useappendflg = (myvalidator.isListAInListB([sys.argv[2]], apndflgs));   
        classlist = sys.argv[3:];
        wrtemd = ("a" if useappendflg else "w");
        newfnm = "" + sys.argv[1];
    elif (2 < len(sys.argv) and sys.argv[1].startswith("-")):
        myvalidator.itemMustBeOneOf(sys.argv[1], allflgs, "the flag sys.argv[1]");
        useappendflg = (myvalidator.isListAInListB([sys.argv[1]], apndflgs));
        useowriteflg = (myvalidator.isListAInListB([sys.argv[1]], wrteflgs));
        wrtemd = ("a" if useappendflg else ("w" if useowriteflg else "b"));
        classlist = sys.argv[2:];
        newfnm = "" + nwdffnm;
    elif (2 < len(sys.argv)):
        classlist = sys.argv[2:];
        newfnm = "" + sys.argv[1];
        wrtemd = "b";
    else: raise ValueError(merrmsg);
    clslines = None;
    try:
        clslines = genFileLines(classlist);
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
