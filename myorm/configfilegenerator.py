from myorm.myvalidator import myvalidator;
from myorm.mybase import mybase;
from myorm.modelsgenerator import getOptsFlagsDict;
import sys;

#the config file has the following lines
tstgenlinea = "testfile_new_file_name: the_name_and_loc";
tstgenlineb = "usedefaultconfigmodulename: false";
tstgenlinec = "usenodb: false";
tstgenlined = "usedefaultdbobjname: false";
tstgenlinee = "configmodulename: the_name";
tstgenlinef = "dbobjname: the_name";

mdlsgenlinea = "models_class_new_file_name: the_name_and_loc";
mdlsgenlineb = "models_class_list:";
mdlsgenlinec = "classnamea, tablenamea: None";
mdlsgenlined = "classnameb, tablenameb: None";
mdlsgenlinee = "classnamec, tablenamec: None";
#...

mlines = [tstgenlinea, tstgenlineb, tstgenlinec, tstgenlined, tstgenlinee, tstgenlinef,
          "", mdlsgenlinea, mdlsgenlineb, mdlsgenlinec, mdlsgenlined, mdlsgenlinee];

if __name__ == "__main__":
    dffnm = "genconfig.txt";
    errmsg = "Please enter a filename no extension and the location to it! If not a default will be ";
    errmsg += "used. This is the only argument accepted! ";
    errmsg += "If you have -? or -help it will also display a message about the model classes options.";
    cfnm = None;
    optsdictobj = getOptsFlagsDict();
    mdlclsoptsmsg = "Note models start options are: " + str(optsdictobj["allopts"]);
    mdlclsoptsmsg += " you may also have None.";
    #print(mdlclsoptsmsg + "\n\n");
    if (len(sys.argv) == 1): cfnm = "" + dffnm;
    elif (len(sys.argv) == 2):
        if (sys.argv[1].startswith("-")): raise ValueError(mdlclsoptsmsg + "\n\n" + errmsg);
        myvalidator.stringMustHaveAtMinNumChars(sys.argv[1], 1, varnm="sys.argv[1]");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(sys.argv[1], varnm="sys.argv[1]");
        cfnm = "" + sys.argv[1] + ".txt";
    else: raise ValueError(errmsg);
    mybase.blockifmyfileexistswritelines(cfnm, mlines, dscptrmsg="generator config");
