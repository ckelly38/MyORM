import traceback;
import types;
class myvalidator:
    @classmethod
    def varmustbethetypeandornull(clsnm, val, tpcls, canbenull, varnm="varname"):
        if (varnm == None or (type(varnm) == str and len(varnm) < 1)):
            return myvalidator.varmustbethetypeornull(val, tpcls, varnm="varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None):
            if (canbenull): return True;
            else: raise TypeError(varnm + " was not the correct type!");
        else:
            if (type(val) == tpcls): return True;
            else: raise TypeError(varnm + " was not the correct type!");
    @classmethod
    def varmustbethetypeonly(clsnm, val, tpcls, varnm="varname"):
        return myvalidator.varmustbethetypeandornull(val, tpcls, False, varnm=varnm);
    @classmethod
    def varmustbeboolean(clsnm, val, varnm="varname"):
        return myvalidator.varmustbethetypeonly(val, bool, varnm=varnm);
    
    @classmethod
    def varmustnotbenull(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return myvalidator.varmustnotbenull(val, varnm="varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None): raise ValueError(varnm + " must not be null!");
        else: return True;

    @classmethod
    def isvaremptyornull(clsnm, val): return (val == None or len(val) < 1);

    @classmethod
    def isvarnull(cls, val): return (val == None);
    @classmethod
    def varisnull(cls, val): return myvalidator.isvarnull(val);

    @classmethod
    def varmustnotbeempty(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return myvalidator.varmustnotbeempty(val, varnm="varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None or len(val) < 1): raise ValueError(varnm + " must not be empty!");
        else: return True;

    @classmethod
    def varmustbeemptyornull(clsnm, val, varnm="varname"):
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.varmustbeemptyornull(val, varnm="varname");
        if (myvalidator.isvaremptyornull(val)): return True;
        else: raise ValueError(varnm + " must be empty or null, but it was not!");

    @classmethod
    def twoBoolVarsMustBeDifferentOrEqual(cls, vala, valb, usediff,
                                          varnma="boolvara", varnmb="boolvarb"):
        myvalidator.varmustbeboolean(vala, varnm=varnma);
        myvalidator.varmustbeboolean(valb, varnm=varnmb);
        myvalidator.varmustbeboolean(usediff, varnm="usediff");
        if (myvalidator.isvaremptyornull(varnma)):
            return myvalidator.twoBoolVarsMustBeDifferentOrEqual(vala, valb, usediff,
                                                                 varnma="boolvara", varnmb=varnmb);
        if (myvalidator.isvaremptyornull(varnmb)):
            return myvalidator.twoBoolVarsMustBeDifferentOrEqual(vala, valb, usediff,
                                                                 varnma=varnma, varnmb="boolvarb");
        if (usediff):
            if (vala == valb):
                raise ValueError(varnma + " and " + varnmb + " both cannot be the same!");
        else:
            if (vala == valb): pass;
            else: raise ValueError(varnma + " and " + varnmb + " must be the same, but they were not!");
        return True;
    @classmethod
    def twoBoolVarsMustBeDifferent(cls, vala, valb, varnma="boolvara", varnmb="boolvarb"):
        return myvalidator.twoBoolVarsMustBeDifferentOrEqual(vala, valb, True,
                                                             varnma=varnma, varnmb=varnmb);
    @classmethod
    def twoBoolVarsMustBeEqual(cls, vala, valb, varnma="boolvara", varnmb="boolvarb"):
        return myvalidator.twoBoolVarsMustBeDifferentOrEqual(vala, valb, False,
                                                             varnma=varnma, varnmb=varnmb);


    @classmethod
    def isstranumber(cls, mstr):
        if (myvalidator.isvaremptyornull(mstr)): return False;
        if (myvalidator.isvaranumber(mstr)): return True;
        else:
            if (type(mstr) == str): pass;
            else: return False;
            #if (mstr.isnumeric() or mstr.isdecimal()): return True;
            fnddpt = False;
            for n in range(len(mstr)):
                if (mstr[n].isdigit()): pass;
                else:
                    if (mstr[n] == '-'):
                        if (n == 0): pass;
                        else: return False;
                    elif (mstr[n] == '.'):
                        if (fnddpt): return False;
                        else: fnddpt = True;
                    else: return False;     
            return True;

    @classmethod
    def isvaranumber(cls, val): 
        return (False if (val == None) else (type(val) == int or type(val) == float));

    @classmethod
    def varmustbeanumber(cls, val, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.varmustbeanumber(val, varnm="varnm");
        if (myvalidator.isvaranumber(val)): return True;
        else: raise ValueError("" + varnm + " must be a number, but it was not!");

    @classmethod
    def varIsAListOfColNameStringsOrEmpty(cls, mval):
        if (myvalidator.isvaremptyornull(mval)): pass;
        else:
            if (mval == list): pass;
            else: return False;
            for item in mval:
                if (myvalidator.stringHasAtMinNumChars(item, 1)): pass;
                else: return False;
                if (myvalidator.stringContainsOnlyAlnumCharsIncludingUnderscores(item)): pass;
                else: return False;
        return True;

    @classmethod
    def varMustBeAListOfColNameStringsOrEmpty(cls, mval, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.varMustBeAListOfColNameStringsOrEmpty(mval, varnm="varnm");
        if (myvalidator.isvaremptyornull(mval)): pass;
        else:
            myvalidator.varmustbethetypeonly(mval, list, varnm=varnm);
            for item in mval:
                myvalidator.stringMustHaveAtMinNumChars(item, 1, varnm="item");
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(item, varnm="item");
        return True;

    @classmethod
    def isClass(clsnm, val): return (type(val) == type);
    @classmethod
    def isModule(cls, val): return (type(val) == types.ModuleType);
    @classmethod
    def isClassOrModule(cls, val): return (myvalidator.isClass(val) or myvalidator.isModule(val));

    #note: mdl is for module, but it can be a module, a class, or an object
    @classmethod
    def getAttrsFromModule(cls, mdl):
        return [attrnm for attrnm in dir(mdl)
               if not attrnm.startswith("__") and not myvalidator.isClassOrModule(getattr(mdl, attrnm))];

    #note: mdl is for module, but it can be a module, a class, or an object
    @classmethod
    def getDBAttrOrValFromConfigModuleMain(cls, mdl, myvars, useval):
        myvalidator.varmustnotbeempty(myvars, varnm="myvars");
        from myorm.MyDB import MyDB;
        tmpdbobj = None;
        for vnm in myvars:
            tmpval = getattr(mdl, vnm);
            if (isinstance(tmpval, MyDB)):
                tmpdbobj = tmpval;
                if (useval): pass;
                else: return vnm;
                break;
        myvalidator.varmustbethetypeonly(tmpdbobj, MyDB, varnm="tmpdbobj");
        return tmpdbobj;
    @classmethod
    def getDBAttrFromConfigModule(cls, mdl, myvars):
        return myvalidator.getDBAttrOrValFromConfigModuleMain(mdl, myvars, False);
    @classmethod
    def getDBValFromConfigModule(cls, mdl, myvars):
        return myvalidator.getDBAttrOrValFromConfigModuleMain(mdl, myvars, True);
    @classmethod
    def getDBAttrOrValFromConfigModuleNoVars(cls, mdl, useval):
        myvars = myvalidator.getAttrsFromModule(mdl);
        return myvalidator.getDBAttrOrValFromConfigModuleMain(mdl, myvars, useval);
    @classmethod
    def getDBAttrFromConfigModuleNoVars(cls, mdl):
        return myvalidator.getDBAttrOrValFromConfigModuleNoVars(mdl, False);
    @classmethod
    def getDBValFromConfigModuleNoVars(cls, mdl):
        return myvalidator.getDBAttrOrValFromConfigModuleNoVars(mdl, True);

    #this takes the module reference and it gets the attribute names, values, and the file name
    #then it takes the db object reference and programatically sets these values for the user
    @classmethod
    def setupConfigModule(cls, mdl):
        myvalidator.varmustbethetypeonly(mdl, types.ModuleType, varnm="module mdl");
        #print(mdl.__file__);
        
        myfnm = mdl.__file__[mdl.__file__.rindex("/")+1:mdl.__file__.rindex(".")];
        #print(myfnm);
        #print(dir(mdl));
        
        myvars = myvalidator.getAttrsFromModule(mdl);
        myvals = [getattr(mdl, vnm) for vnm in myvars];
        #print(myvars);
        #print(myvals);
        myvalidator.twoListsMustBeTheSameSize(myvars, myvals, arranm="myvars", arrbnm="myvals");

        tmpdbobj = myvalidator.getDBAttrOrValFromConfigModuleMain(mdl, myvars, True);
        tmpdbobj.setConfigFileName(myfnm);
        tmpdbobj.setConfigAttrNames(myvars);
        tmpdbobj.setConfigAttrValues(myvals);
        print("MYVALIDATOR: CONFIG MODULE SETUP SUCCESSFULLY DONE!");
        return True;

    @classmethod
    def listMustContainUniqueValuesOnly(clsnm, mlist, ignorelist=None, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.listMustContainUniqueValuesOnly(mlist, ignorelist=ignorelist,
                                                               varnm="varnm");
        if (myvalidator.isvaremptyornull(mlist) or len(mlist) < 2): return True;
        if (myvalidator.isvaremptyornull(ignorelist)): pass;
        else:
            #ignore list is not empty. we want to filter these items out of the list first,
            #then see if the rest of the items are unique.
            nwlist = [item for item in mlist if item not in ignorelist];
            #print(f"mlist = {mlist}");
            #print(f"nwlist = {nwlist}");
            #print(f"ignorelist = {ignorelist}");
            return myvalidator.listMustContainUniqueValuesOnly(nwlist, ignorelist=None, varnm=varnm);
    
        myset = set(mlist);
        mynwlist = list(myset);
        if (len(mlist) == len(mynwlist)): return True;
        else: raise ValueError(f"the list {varnm} must contain unique values, but it did not!");

    @classmethod
    def areTwoListsTheSame(clsnm, lista, listb):
        if (myvalidator.isvaremptyornull(lista)): return (myvalidator.isvaremptyornull(listb));
        else:
            if (myvalidator.isvaremptyornull(listb)): return False;
            else:
                if (len(lista) == len(listb)):
                    for n in range(len(lista)):
                        if (myvalidator.isvaremptyornull(lista[n])):
                            if (myvalidator.isvaremptyornull(listb[n])): pass;
                            else: return False;
                        else:
                            if (myvalidator.isvaremptyornull(listb[n])): return False;
                            else:
                                if (lista[n] == listb[n]): pass;
                                else: return False;
                    return True;
                else: return False;
    
    @classmethod
    def areTwoArraysTheSameSize(cls, arra, arrb):
        if (myvalidator.isvaremptyornull(arra)): return myvalidator.isvaremptyornull(arrb);
        else: return (False if myvalidator.isvaremptyornull(arrb) else (len(arra) == len(arrb)));
    @classmethod
    def areTwoListsTheSameSize(cls, arra, arrb): return myvalidator.areTwoArraysTheSameSize(arra, arrb);

    @classmethod
    def twoArraysMustBeTheSameSize(cls, arra, arrb, arranm="arranm", arrbnm="arrbnm"):
        if (myvalidator.isvaremptyornull(arranm)):
            return myvalidator.twoArraysMustBeTheSameSize(arra, arrb, arranm="arranm", arrbnm=arrbnm);
        if (myvalidator.isvaremptyornull(arrbnm)):
            return myvalidator.twoArraysMustBeTheSameSize(arra, arrb, arranm=arranm, arrbnm="arrbnm");
        errmsg = "the two arrays " + arranm + " and " + arrbnm + " must be the same size!";
        if (myvalidator.areTwoArraysTheSameSize(arra, arrb)): return True;
        else: raise ValueError(errmsg);
    @classmethod
    def twoListsMustBeTheSameSize(cls, arra, arrb, arranm="arranm", arrbnm="arrbnm"):
        return myvalidator.twoArraysMustBeTheSameSize(arra, arrb, arranm=arranm, arrbnm=arrbnm);

    @classmethod
    def combineTwoLists(cls, lista, listb, nodups=False):
        myvalidator.varmustbeboolean(nodups, varnm="nodups");
        if (myvalidator.isvaremptyornull(lista)):
            return (None if myvalidator.isvaremptyornull(listb) else listb);
        else:
            if (myvalidator.isvaremptyornull(listb)): return lista;
            else:
                #combine both of the lists...
                #list of strings and another list of strings
                #copy one, then copy the other directly
                mynwlist = [mstr for mstr in lista];
                if (nodups):
                    for mstr in listb:
                        if (mstr not in lista): mynwlist.append(mstr);
                else:
                    for mstr in listb: mynwlist.append(mstr);
                return mynwlist;

    @classmethod
    def removeDuplicatesFromList(cls, mlist):
        return (mlist if (myvalidator.isvaremptyornull(mlist)) else list(set(mlist)));

    @classmethod
    def isListAInListB(cls, lista, listb):
        if (myvalidator.isvaremptyornull(lista)): return myvalidator.isvaremptyornull(listb);
        for itema in lista:
            if (itema in listb): pass;
            else: return False;
        return True;

    @classmethod
    def doTwoListsContainTheSameData(cls, lista, listb):
        return (myvalidator.areTwoArraysTheSameSize(lista, listb) and
                myvalidator.isListAInListB(lista, listb));

    @classmethod
    def itemMustBeOneOf(cls, item, mvals, varnm="varnm"):
        myvalidator.varmustnotbeempty(mvals, varnm="mvals");
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.itemMustBeOneOf(item, mvals, varnm="varnm");
        errmsg = "the item " + varnm + " must be one of the following ";
        errmsg += myvalidator.myjoin(", ", mvals) + ", but it was not!";
        if (type(item) in [list, tuple]):
            if (myvalidator.isListAInListB(item, mvals)): return True;
            else: raise ValueError(errmsg);
        else:
            if (item in mvals): return True;
            else: raise ValueError(errmsg);

    @classmethod
    def objvarmusthavethesekeysonit(cls, mobj, rkys, varnm="mobj"):
        if (myvalidator.isvaremptyornull(rkys)): return True;
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.objvarmusthavethesekeysonit(mobj, rkys, varnm="mobj");
        myvalidator.varmustnotbenull(mobj, varnm=varnm);
        errmsg = "the object " + varnm + " must have " + (", ".join(rkys));
        errmsg += " as keys on it, but it did not!";
        if (myvalidator.isListAInListB(rkys, mobj.keys())): return True;
        else: raise ValueError(errmsg);

    @classmethod
    def doesCaseMatch(cls, stra, strb):
        myvalidator.varmustbethetypeandornull(stra, str, True, varnm="stra");
        myvalidator.varmustbethetypeandornull(strb, str, True, varnm="strb");
        if (myvalidator.isvaremptyornull(stra)): return myvalidator.isvaremptyornull(strb);
        else: return (stra.isupper() == strb.isupper() and stra.islower() == strb.islower());

    @classmethod
    def stringContainsOnlyAlnumCharsIncludingUnderscores(cls, mstr):
        if (myvalidator.isvaremptyornull(mstr)): return True;
        else:
            myvalidator.varmustbethetypeonly(mstr, str, varnm="mstr");
            for c in mstr:
                if (c.isalnum() or c == '_'): pass;
                else: return False;
        return True;

    @classmethod
    def stringMustContainOnlyAlnumCharsIncludingUnderscores(cls, mstr, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mstr, varnm="varnm");
        if (myvalidator.stringContainsOnlyAlnumCharsIncludingUnderscores(mstr)): return True;
        else: raise ValueError(varnm + " must contain alpha-numeric characters only!");

    @classmethod
    def stringHasAtMaxOrAtMinNumChars(cls, mstr, mxormnlen, usemax):
        myvalidator.varmustbeboolean(usemax, varnm="usemax");
        myvalidator.varmustbethetypeonly(mxormnlen, int, varnm="mxormnlen");
        if (mxormnlen < 0): raise ValueError("mxormnlen must be at least zero, but it was not!");
        if (usemax):
            if (myvalidator.isvaremptyornull(mstr)): pass;
            else: return (not((mxormnlen < 1) or (mxormnlen < len(mstr))));
        else:
            if (0 < mxormnlen):
                return (not(myvalidator.isvaremptyornull(mstr) or (len(mstr) < mxormnlen)));
        return True;
    @classmethod
    def stringHasAtMostNumChars(cls, mstr, mxormnlen):
        return myvalidator.stringHasAtMaxOrAtMinNumChars(mstr, mxormnlen, True);
    @classmethod
    def stringHasAtMaxNumChars(cls, mstr, mxormnlen):
        return myvalidator.stringHasAtMaxOrAtMinNumChars(mstr, mxormnlen, True);
    @classmethod
    def stringHasAtMinNumChars(cls, mstr, mxormnlen):
        return myvalidator.stringHasAtMaxOrAtMinNumChars(mstr, mxormnlen, False);

    @classmethod
    def stringMustHaveAtMaxOrAtMinNumChars(cls, mstr, mxormnlen, usemax, varnm="varnm"):
        myvalidator.varmustbeboolean(usemax, varnm="usemax");
        myvalidator.varmustbethetypeonly(mxormnlen, int, varnm="mxormnlen");
        if (mxormnlen < 0): raise ValueError("mxormnlen must be at least zero, but it was not!");
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, usemax,
                                                                  varnm="varnm");
        fpterrstr = "the string " + varnm + " must ";
        mnomxstr = ("most " if usemax else "minimum ");
        myerrmsgbase = fpterrstr + "have at " + mnomxstr + str(mxormnlen) + " characters on it, but it ";
        if (usemax):
            if (myvalidator.isvaremptyornull(mstr)): pass;
            else:
                myvalidator.varmustbethetypeonly(mstr, str, varnm="mstr");
                if (mxormnlen < 1):
                    raise ValueError(fpterrstr + "be empty null or undefined, but it was not!");
                else:
                    if (mxormnlen < len(mstr)): raise ValueError(myerrmsgbase + "had more!");
        else:
            if (0 < mxormnlen):
                if (myvalidator.isvaremptyornull(mstr)):
                    raise ValueError(myerrmsgbase + "was empty or null!");
                else:
                    myvalidator.varmustbethetypeonly(mstr, str, varnm="mstr");
                    if (len(mstr) < mxormnlen): raise ValueError(myerrmsgbase + "had less than that!");
        return True;
    @classmethod
    def stringMustHaveAtMostNumChars(cls, mstr, mxormnlen, varnm="varnm"):
        return myvalidator.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, True, varnm=varnm);
    @classmethod
    def stringMustHaveAtMaxNumChars(cls, mstr, mxormnlen, varnm="varnm"):
        return myvalidator.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, True, varnm=varnm);
    @classmethod
    def stringMustHaveAtMinNumChars(cls, mstr, mxormnlen, varnm="varnm"):
        return myvalidator.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, False, varnm=varnm);

    @classmethod
    def stringMustStartOrEndOrBothWith(cls, mstr, estr, usestart, useboth, varnm="varnm"):
        myvalidator.varmustbeboolean(usestart, varnm="usestart");
        myvalidator.stringMustHaveAtMinNumChars(mstr, 1, varnm="mstr");
        if (estr == None): return myvalidator.stringMustEndWith(mstr, "", varnm="varnm");
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.stringMustEndWith(mstr, estr, varnm="varnm");
        sorewstr = ("start and end" if (useboth) else ("start" if (usestart) else "end"));
        errmsg = "the string " + mstr + " called " + varnm + " does not " + sorewstr + " with " + estr;
        errmsg += ", but it must!";
        if ((useboth and (mstr.startswith(estr) and mstr.endswith(estr))) or
            ((not useboth) and ((usestart and mstr.startswith(estr)) or
                                ((not usestart) and mstr.endswith(estr))))):
            return True;
        else: raise ValueError(errmsg);
    @classmethod
    def stringMustStartOrEndWith(cls, mstr, estr, usestart, varnm="varnm"):
        return myvalidator.stringMustStartOrEndOrBothWith(mstr, estr, usestart, False, varnm=varnm);
    @classmethod
    def stringMustStartAndEndWith(cls, mstr, estr, varnm="varnm"):
        return myvalidator.stringMustStartOrEndOrBothWith(mstr, estr, True, True, varnm=varnm);
    @classmethod
    def stringMustStartWith(cls, mstr, estr, varnm="varnm"):
        return myvalidator.stringMustStartOrEndWith(mstr, estr, True, varnm=varnm);
    @classmethod
    def stringMustEndWith(cls, mstr, estr, varnm="varnm"):
        return myvalidator.stringMustStartOrEndWith(mstr, estr, False, varnm=varnm);

    @classmethod
    def doesLineHaveStringOnItAtIndex(cls, mstr, line, indxval):
        mstrisemptyornull = myvalidator.isvaremptyornull(mstr);
        if (myvalidator.isvaremptyornull(line)):
            if (indxval == 0): return mstrisemptyornull;
            else: myvalidator.valueMustBeInRange(indxval, 0, 0, True, True, varnm="indxval");
        elif (mstrisemptyornull): return False;
        else:
            myvalidator.valueMustBeInRange(indxval, 0, len(line) - 1, True, True, varnm="indxval");
            return (mstr in line and line.index(mstr) == indxval);
    @classmethod
    def lineHasStringOnItAtIndex(cls, mstr, line, indxval):
        return myvalidator.doesLineHaveStringOnItAtIndex(mstr, line, indxval);
    @classmethod
    def lineHasMSTROnItAtIndex(cls, mstr, line, indxval):
        return myvalidator.doesLineHaveStringOnItAtIndex(mstr, line, indxval);

    @classmethod
    def getLineIndexesWithStringOnIt(cls, mstr, mlines):
        myvalidator.stringMustHaveAtMinNumChars(mstr, 1, varnm="mstr");
        if (myvalidator.isvaremptyornull(mlines)): return [];
        #                                    if (cls.doesLineHaveStringOnItAtIndex(mstr, mlines[n], 0))
        return [n for n in range(len(mlines)) if (mstr in mlines[n] and mlines[n].index(mstr) == 0)];

    @classmethod
    def isValueInRange(cls, val, minval, maxval, hasmin, hasmax):
        myvalidator.varmustbeboolean(hasmin, varnm="hasmin");
        myvalidator.varmustbeboolean(hasmax, varnm="hasmax");
        myvalidator.varmustbeanumber(val, varnm="val");
        myvalidator.varmustbeanumber(minval, varnm="minval");
        myvalidator.varmustbeanumber(maxval, varnm="maxval");
        return (not((hasmin and (val < minval)) or (hasmax and (maxval < val))));
    @classmethod
    def isValueInRangeWithMaxAndMin(cls, val, minval, maxval):
        return myvalidator.isValueInRange(val, minval, maxval, True, True);
    @classmethod
    def isValueMoreThanOrAtTheMinOnly(cls, val, minval):
        return myvalidator.isValueInRange(val, minval, 0, True, False);
    @classmethod
    def isValueLessThanOrAtTheMaxOnly(cls, val, maxval):
        return myvalidator.isValueInRange(val, 0, maxval, False, True);

    @classmethod
    def valueMustBeInRange(cls, val, minval, maxval, hasmin, hasmax, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.valueMustBeInRange(val, minval, maxval, hasmin, hasmax, varnm="varnm");
        if (myvalidator.isValueInRange(val, minval, maxval, hasmin, hasmax)): return True;
        else:
            if (hasmin or hasmax): pass;
            else:
                raise ValueError("either hasmin or hasmax or both must be true, but neither were " +
                                 "and isValueInRange returned false!");
            mystr = " must be";
            if (hasmin): mystr += " at least " + str(minval);
            if (hasmin and hasmax): mystr += " and";
            if (hasmax): mystr += " at most " + str(maxval);
            raise ValueError("" + varnm + mystr + " but it was not!");
    @classmethod
    def valueMustBeInMinAndMaxRange(cls, val, minval, maxval, varnm="varnm"):
        return myvalidator.valueMustBeInRange(val, minval, maxval, True, True, varnm=varnm);
    @classmethod
    def valueMustBeAtMinOnly(cls, val, minval, varnm="varnm"):
        return myvalidator.valueMustBeInRange(val, minval, 0, True, False, varnm=varnm);
    @classmethod
    def valueMustBeAtMaxOnly(cls, val, maxval, varnm="varnm"):
        return myvalidator.valueMustBeInRange(val, 0, maxval, False, True, varnm=varnm);

    @classmethod
    def myjoin(cls, sepstr, mlist):
        if (myvalidator.isvaremptyornull(mlist)): return "";
        nosep = myvalidator.isvaremptyornull(sepstr);
        if (nosep or not (type(mlist[0]) == str)):
            mystr = "";
            for n in range(len(mlist)):
                mystr += str(mlist[n]);
                if (nosep): pass;
                elif (n + 1 < len(mlist)): mystr += "" + sepstr;
            return mystr;
        else: return sepstr.join(mlist);

    @classmethod
    def mysplit(cls, mystr, delimis, delimlens, offset=0):
        myvalidator.varmustbeanumber(offset, varnm="offset");
        if (mystr == None): return None;
        myvalidator.varmustbethetypeonly(mystr, str, varnm="mystr");
        if ((len(mystr) < 2) or myvalidator.isvaremptyornull(delimis)): return [mystr];
        isonedelimlen = False;
        if (myvalidator.areTwoArraysTheSameSize(delimis, delimlens)):
            for n in range(len(delimis)):
                myvalidator.varmustbeanumber(delimis[n], varnm="delimis[" + str(n) + "]");
                myvalidator.varmustbeanumber(delimlens[n], varnm="delimlens[" + str(n) + "]");
        else:
            isonedelimlen = (len(delimlens) == 1);
            merrmsg = "delimis len(" + str(len(delimis)) + ") and delimilens len(" + str(len(delimlens));
            merrmsg += ") must both be the same size, but they were not!";
            if (isonedelimlen and 0 < len(delimis)):
                myvalidator.varmustbeanumber(delimlens[0], varnm="delimlen");
                for n in range(len(delimis)):
                    myvalidator.varmustbeanumber(delimis[n], varnm="delimis[" + str(n) + "]");
            else: raise ValueError(merrmsg);
        
        #the resultant array must have num delimis + 1 so if 2 indexes 3 parts
        #the last part is allowed to be empty
        #the resultant string rejoined should have at most the same number of characters in mystr
        merrmsgb = "the delimeter indexes were not in the correct order (often caused by an invalid ";
        merrmsgb += "value)!";
        myresarr = None;
        prevdelimi = 0;
        prevdelimlen = 0;
        for n in range(len(delimis)):
            cdelimi = delimis[n] + offset;
            cdelimlen = (delimlens[0] if isonedelimlen else delimlens[n]);
            #print(f"cdelimi = {cdelimi}");
            #print(f"cdelimlen = {cdelimlen}");
            #print(f"prevdelimi = {prevdelimi}");
            #print(f"prevdelimlen = {prevdelimlen}");
            
            myvalidator.valueMustBeInRange(cdelimi, 0, len(mystr), True, True, varnm="cdelimi");
            if (n == 0): myresarr = [mystr[0: cdelimi]];
            else:
                if (cdelimi < prevdelimi + prevdelimlen): raise ValueError(merrmsgb);
                myresarr.append(mystr[prevdelimi + prevdelimlen: cdelimi]);
            if (n + 1 == len(delimis)): myresarr.append(mystr[cdelimi + cdelimlen:]);
            prevdelimlen = cdelimlen;
            prevdelimi = cdelimi;
        #print(f"delimis = {delimis}");
        #print(f"delimlens = {delimlens}");
        #print(f"myresarr = {myresarr}");

        if (len(myresarr) == len(delimis) + 1): pass;
        else: raise ValueError("generated split array did not have the correct number of strings!");
        resstr = myvalidator.myjoin("", myresarr);
        #print(f"mystr = {mystr}");
        #print(f"resstr = {resstr}");

        myvalidator.stringMustHaveAtMostNumChars(resstr, len(mystr), varnm="resstr");
        return myresarr;
    @classmethod
    def mysplitWithLen(cls, mystr, delimis, delimlen, offset=0):
        myvalidator.varmustbeanumber(delimlen, varnm="delimlen");
        return myvalidator.mysplit(mystr, delimis, [delimlen], offset);
    @classmethod
    def mysplitWithDelimeter(cls, mystr, delimstr, offset=0):
        if (delimstr == None): return myvalidator.mysplitWithDelimeter(mystr, "", offset=offset);
        else: myvalidator.varmustbethetypeonly(delimstr, str, varnm="delimstr");
        delimis = [i for i in range(len(mystr)) if mystr.startswith(delimstr, i)];
        return myvalidator.mysplitWithLen(mystr, delimis, len(delimstr), offset);

    @classmethod
    def genStringWithNumberText(cls, numchars, modval=10):
        if (myvalidator.isValueMoreThanOrAtTheMinOnly(numchars, 0)): pass;
        else: raise ValueError("numchars must be at minimum 0, but it was not!");
        myvalidator.varmustbethetypeonly(modval, int, varnm="modval");
        myvalidator.valueMustBeInRange(modval, 1, 0, True, False, varnm="modval");
        #return myvalidator.myjoin("", [(n % modval) for n in range(numchars)]);
        mystr = "";
        for n in range(numchars): mystr += str(n % modval);
        return mystr;

    @classmethod
    def genListOfSameVals(cls, numvals, val): return [val for n in range(numvals)];
    @classmethod
    def genListOfBoolVals(cls, numbools, boolval):
        myvalidator.varmustbeboolean(boolval, varnm="boolval");
        return myvalidator.genListOfSameVals(numbools, boolval);
    
    @classmethod
    def listOfBoolsMustHaveXNumTrueYNumFalse(cls, blsarr, rqnumt, rqnumf, tpnumt=None, tpnumf=None,
                                             varnm="varnm"):
        myvalidator.varmustbethetypeonly(rqnumt, int, varnm="rqnumt");
        myvalidator.varmustbethetypeonly(rqnumf, int, varnm="rqnumf");
        mintpopts = ["MIN", "min", "MINIMUM", "minimum", ">"];
        maxtpopts = ["MAX", "max", "MAXIMUM", "maximum", "<"];
        exacttpopts = ["EXACT", "exact", "EQUAL", "equal", "SAME", "same", "="];
        mytpopts = [None, ""];
        mytpopts = myvalidator.combineTwoLists(mytpopts, mintpopts, nodups=True);
        mytpopts = myvalidator.combineTwoLists(mytpopts, maxtpopts, nodups=True);
        mytpopts = myvalidator.combineTwoLists(mytpopts, exacttpopts, nodups=True);
        myvalidator.itemMustBeOneOf(tpnumt, mytpopts, varnm="tpnumt");
        myvalidator.itemMustBeOneOf(tpnumf, mytpopts, varnm="tpnumf");
        if (myvalidator.isvaremptyornull(varnm)):
            return myvalidator.listOfBoolsMustHaveXNumTrueYNumFalse(blsarr, rqnumt, rqnumf, tpnumt,
                                                                    tpnumf, varnm="blsarrnm");
        cnumt = 0;
        cnumf = 0;
        if (myvalidator.isvaremptyornull(blsarr)): pass;
        else:
            for n in range(len(blsarr)):
                bval = blsarr[n];
                myvalidator.varmustbeboolean(bval, varnm=varnm + "[" + str(n) + "]");
                if (bval): cnumt += 1;
                else: cnumf += 1;
        #now that we have the actual counts we need to compare them with the requested counts and
        #the types
        #if the type is min, max, or exact, or empty or none for no restrictions on this
        tvnm = varnm + " num true";
        fvnm = varnm + " num false";
        for itemtp in ["cnumt", "cnumf"]:
            #oitemtp = ("rqnumt" if (itemtp == "cnumt") else "rqnumf");
            cntval = (cnumt if (itemtp == "cnumt") else cnumf);
            rqval = (rqnumt if (itemtp == "cnumt") else rqnumf);
            tpval = (tpnumt if (itemtp == "cnumt") else tpnumf);
            avnm = (tvnm if (itemtp == "cnumt") else fvnm);
            #print(f"itemtp = {itemtp}");
            #print(f"cntval = {cntval}");
            #print(f"rqval = {rqval}");
            #print(f"tpval = {tpval}");
            #print(f"avnm = {avnm}");
            if (myvalidator.isvaremptyornull(tpval)): pass;
            else:
                if (tpval in mintpopts):
                    myvalidator.valueMustBeAtMinOnly(cntval, rqval, varnm=avnm);
                elif (tpval in maxtpopts):
                    myvalidator.valueMustBeAtMaxOnly(cntval, rqval, varnm=avnm);
                else:#elif (tpval in exacttpopts):
                    if (cntval == rqval): pass;
                    else:
                        raise ValueError("actual " + avnm + " must be the same as the requested " +
                                         "count for " + avnm + ", but they were not!");
        return True;

    #compare arrays methods and sorting of two arrays of numbers

    @classmethod
    def insertionSortNums(cls, arra, arrb):
        #insertion sort here:
        #print(f"arra = {arra}");
        #print(f"arrb = {arrb}");
        if (myvalidator.isvaremptyornull(arra)): return arrb;
        elif (myvalidator.isvaremptyornull(arrb)): return arra;
        spt = "array was not sorted, but must be!";
        for n in range(len(arra)):
            if (n + 1 < len(arra)):
                if (arra[n + 1] < arra[n]): raise ValueError("the first " + spt);
        for n in range(len(arrb)):
            if (n + 1 < len(arrb)):
                if (arrb[n + 1] < arrb[n]): raise ValueError("the second " + spt);
        
        maxarra = arra[len(arra) - 1];
        minarra = arra[0];
        maxarrb = arrb[len(arrb) - 1];
        minarrb = arrb[0];
        resarr = None;
        if (minarrb < maxarra):
            if (minarra < maxarrb): 
                #do the sorting of the two arrays here...
                #of the two arrays figure out which one is the smallest
                #if they are not equal smallest first
                #if they are equal do a before b.
                #the min will come from the resarr these items will need to be bigger than that.
                #get the first item(s) by comparing minimums
                #if amin < bmin a is first
                #if bmin < amin b is first
                #if they are equal a is first then b
                asi = 0;
                bsi = 0;
                resarr = [];
                if (minarrb < minarra):
                    resarr.append(minarrb);
                    bsi = 1;
                elif (minarra < minarrb):
                    resarr.append(minarra);
                    asi = 1;
                else:
                    resarr.append(minarra);
                    resarr.append(minarrb);
                    bsi = 1;
                    asi = 1;
                #copy all from a, then from b if they are the same
                for n in range(asi, len(arra)):
                    if (arra[n] == resarr[0]):
                        asi += 1;
                        resarr.append(arra[n]);
                for n in range(bsi, len(arrb)):
                    if (arrb[n] == resarr[0]):
                        bsi += 1;
                        resarr.append(arrb[n]);
                #print(f"asi = {asi}");
                #print(f"bsi = {bsi}");
                
                for n in range(asi, len(arra)):
                    for k in range(bsi, len(arrb)):
                        #print(f"arra[{n}] = {arra[n]}");
                        #print(f"arrb[{k}] = {arrb[k]}");
                        
                        bkaftrcp = False;
                        if (arra[n] < arrb[k]):
                            resarr.append(arra[n]);
                            asi += 1;
                            bkaftrcp = True;
                            #print(f"asi = {asi}");
                            #print(f"bsi = {bsi}");
                            #print(f"resarr = {resarr}");
                            #raise ValueError("item in a is less than item in b!");
                        elif (arrb[k] < arra[n]):
                            resarr.append(arrb[k]);
                            bsi += 1;
                            #print(f"asi = {asi}");
                            #print(f"bsi = {bsi}");
                            #print(f"resarr = {resarr}");
                            #raise ValueError("item in b is less than item in a!");
                        else:
                            resarr.append(arra[n]);
                            resarr.append(arrb[k]);
                            asi += 1;
                            bsi += 1;
                            bkaftrcp = True;
                            #print(f"asi = {asi}");
                            #print(f"bsi = {bsi}");
                            #print(f"resarr = {resarr}");
                            #raise ValueError("they are equal!");
                        
                        #copy all from a, then from b if they are the same
                        for oai in range(asi, len(arra)):
                            if (arra[oai] == resarr[len(resarr) - 1]):
                                asi += 1;
                                resarr.append(arra[oai]);
                        for obi in range(bsi, len(arrb)):
                            if (arrb[obi] == resarr[len(resarr) - 1]):
                                bsi += 1;
                                resarr.append(arrb[obi]);
                        #print(f"NEW asi = {asi}");
                        #print(f"NEW bsi = {bsi}");
                        
                        if (bkaftrcp):
                            bkaftrcp = False;
                            break;
                #print(f"resarr = {resarr}");
            else:
                #minarra >= maxarrb b is before all of a
                resarr = [item for item in arrb];
                for item in arra: resarr.append(item);
        else:
            #minarrb >= maxarra b is after all of a
            resarr = [item for item in arra];
            for item in arrb: resarr.append(item);
        #print(f"resarr = {resarr}");
        
        if (len(resarr) == len(arra) + len(arrb)): return resarr;
        else:
            raise ValueError("the length of the resarr (" + str(len(resarr)) + ") must be the " +
                             "sum of the lengths of the two original arrays, " +
                             "len(arra) = " + str(len(arra)) + " len(arrb) = " + str(len(arrb)) +
                             ", but it was not!");

    #list of indexes for adding will be first array (assumed ints sorted in ascending order)
    #list of indexes for deleting will be second array (assumed ints sorted in ascending order)
    #we need to kind of merge or insertion sort these arrays assume that they are sorted
    #we want to know the order of add or deleting if we combine these two and sort them...
    #the catch is if we sort them then we can tell which one will be where
    #if we do not modify the original arrays
    #return info dict with the data
    @classmethod
    def compareTwoArraysItemByItemInfoObj(cls, arra, arrb):
        srtdabarr = myvalidator.insertionSortNums(arra, arrb);
        #if in arra only 0 if in arrb only 1 if both 2.
        isaempty = myvalidator.isvaremptyornull(arra);
        isbempty = myvalidator.isvaremptyornull(arrb);
        resarr = ([] if (isaempty and isbempty) else
                  [(1 if (isaempty) else (0 if (isbempty) else
                    (2 if (item in arra and item in arrb) else (0 if (item in arra) else 1))))
                  for item in srtdabarr]);
        #print(f"arra = {arra}");
        #print(f"arrb = {arrb}");
        #print(f"srtdabarr = {srtdabarr}");
        #print(f"resarr = {resarr}");
        return {"arraisempty": isaempty, "arrbisempty": isbempty, "addarr": arra, "delarr": arrb,
                "sortedarr": srtdabarr, "resarr": resarr};
    @classmethod
    def getValueFromCompareArraysDataObject(cls, key, datobj):
        myvalidator.objvarmusthavethesekeysonit(datobj, [key], varnm="arrscompdatobj");
        return datobj[key];
    @classmethod
    def compareTwoArraysItemByItemResArrFromDatObj(cls, datobj):
        return myvalidator.getValueFromCompareArraysDataObject("resarr", datobj);
    @classmethod
    def compareTwoArraysItemByItemResArr(cls, arra, arrb):
        return myvalidator.compareTwoArraysItemByItemResArrFromDatObj(
            myvalidator.compareTwoArraysItemByItemInfoObj(arra, arrb));
    @classmethod
    def compareTwoArraysItemByItemSortedArrFromDatObj(cls, datobj):
        return myvalidator.getValueFromCompareArraysDataObject("sortedarr", datobj);
    @classmethod
    def compareTwoArraysItemByItemSortedArr(cls, arra, arrb):
        return myvalidator.compareTwoArraysItemByItemSortedArrFromDatObj(
            myvalidator.compareTwoArraysItemByItemInfoObj(arra, arrb));


    #convenience methods since the validators list (and all of these methods) reside in the mycol class

    @classmethod
    def getAllValidators(cls):
        from mycol import mycol;
        return mycol.getAllValidators();

    @classmethod
    def getMyValidators(cls, mcnm):
        from mycol import mycol;
        return mycol.getMyValidators(mcnm);

    @classmethod
    def getMyValidatorsThatContainKeys(cls, mcnm, mkys):
        from mycol import mycol;
        return mycol.getMyValidatorsThatContainKeys(mcnm, mkys);

    @classmethod
    def getMyIndividualOrMultiColumnValidators(cls, mcnm, useindiv):
        from mycol import mycol;
        return mycol.getMyIndividualOrMultiColumnValidators(mcnm, useindiv);
    @classmethod
    def getMyIndividualColumnValidators(cls, mcnm):
        return myvalidator.getMyIndividualOrMultiColumnValidators(mcnm, True);
    @classmethod
    def getMyMultiColumnValidators(cls, mcnm):
        return myvalidator.getMyIndividualOrMultiColumnValidators(mcnm, False);

    @classmethod
    def setAllValidators(cls, vlist):
        from mycol import mycol;
        return mycol.setAllValidators(vlist);

    #This is a decorator. This actually calls a decorator.
    #https://www.datacamp.com/tutorial/decorators-python
    #@classmethod
    def validates(*args):#cls, 
        from mycol import mycol;
        return mycol.validates(args);

    @classmethod
    def addValidator(cls, classname, methodref, keys):
        from mycol import mycol;
        return mycol.addValidator(classname, methodref, keys);

    @classmethod
    def removeValidator(cls, classname, keys):
        from mycol import mycol;
        return mycol.removeValidator(classname, keys);

    @classmethod
    def runGivenValidatorsForClass(cls, mcnm, mobj, mvs):
        from mycol import mycol;
        return mycol.runGivenValidatorsForClass(mcnm, mobj, mvs);

    @classmethod
    def runValidatorsByKeysForClass(cls, mcnm, mobj, mkys):
        from mycol import mycol;
        return mycol.runValidatorsByKeysForClass(mcnm, mobj, mkys);

    @classmethod
    def runAllValidatorsForClass(cls, mcnm, mobj):
        from mycol import mycol;
        return mycol.runAllValidatorsForClass(mcnm, mobj);

    
    #pretty much all of these need the table name
    #it is my responsibility as the programmer to make sure that the columns are on the table
    #passing in the class refs instead will be a lot bigger, but will make the validation possible
    #otherwise... I need some sort of reverse look up way to get the table names or the classes
    #given one or the other... I already have a way to get the tablename from the classes of course.
    #what I do not have is a way to get the classname string or the class ref given the tablename.

    @classmethod
    def combineTableNamesWithColNames(cls, mcolnames, mtablenames, singleinctname):
        #if there is only one tablename, do we still do tablename.mcolname, ... or just mcolname...
        from mycol import mycol;#may need to change or get removed
        isonetable = (len(mtablenames) == 1);
        if (isonetable or len(mcolnames) == len(mtablenames)):
            if (isonetable):
                #still need to make sure all of the column names are on the table...
                mclsref = mycol.getClassFromTableName(mtablenames[0]);
                if (mclsref.areGivenColNamesOnTable(mcolnames, mycols=None)): pass;
                else:
                    raise ValueError("the col names were not found on the table class(" +
                                     mclsref.__name__ + ")");
                if (singleinctname): pass;
                else: return ", ".join(mcolnames);
            mystr = "";
            for n in range(len(mcolnames)):
                mcolnm = mcolnames[n];
                ctablename = (mtablenames[0] if (isonetable and singleinctname) else mtablenames[n]);
                myvalidator.varmustnotbeempty(mcolnm, varnm="mcolnm");
                mytempcls = mycol.getClassFromTableName(ctablename);
                myvalidator.varmustnotbenull(mytempcls, varnm="mytempcls");
                #is col name on table...
                if (mytempcls.areGivenColNamesOnTable([mcolnm], mycols=None)): pass;
                else:
                    raise ValueError("the col names were not found on the table class(" +
                                     mytempcls.__name__ + ")");
                mystr += "" + ctablename + "." + mcolnm;
                if (n + 1 < len(mcolnames)): mystr += ", ";
            return mystr;
        else: raise ValueError("the column names must be the same length as the table names!");


    #other file change log methods

    #rnm table from old_name to new_name
    #rnm col from old_name to new_name on table_name
    #rnm cons from old_name to new_name on table_name
    #del/add table table_name
    #del/add col col_name on table_name
    #del/add cons cons_name on table_name
    #del/add icolcons type from col_name on table_name
    #-nonnull, unique, unsigned, datatype 
    
    @classmethod
    def renameItemString(cls, tp, oldnm, nwnm, tnm=""):
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tp, varnm="the type string");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(oldnm, varnm="the old name");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(nwnm, varnm="the new name");
        mpt = " from " + oldnm + " to " + nwnm;
        tpstr = ("table" if (tp.upper() == "TABLE") else ("col" if (tp.upper() == "COL") else "cons"));
        fptstr = "rnm " + tpstr + mpt;
        if (tp.upper() == "TABLE"): return fptstr;
        elif (tp.upper() in ["COL", "CONS", "CONSTRAINT"]):
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tnm,
                                                                            varnm="the table name");
            return fptstr + " on " + tnm;
        else:
            myvalidator.itemMustBeOneOf(tp.upper(), ["TABLE", "COL", "CONS", "CONSTRAINT"],
                                        varnm="tpstr");
            raise ValueError("the type was not on the list or table, col, or cons, but it should be!");
    
    @classmethod
    def addOrDeleteItemString(cls, useadd, tp, tnm, itnm="", icltp=""):
        myvalidator.varmustbeboolean(useadd, varnm="useadd");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tnm, varnm="the table name");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tp, varnm="the type string");
        addstr = ("add" if (useadd) else "del");
        icolconstpslist = ["INDIVIDUAL-COLUMN-CONSTRAINT", "INDIVIDUAL COLUMN CONSTRAINT", "ICOLCONS"];
        constplist = ["CONS", "CONSTRAINT"];
        inittpslist = ["TABLE", "COL", "CONS", "CONSTRAINT"];
        tpslist = myvalidator.combineTwoLists(inittpslist, icolconstpslist);
        myvalidator.itemMustBeOneOf(tp.upper(), tpslist, varnm="tpstr");
        myrettpstr = ("icolcons" if (tp.upper() in icolconstpslist) else
                      ("cons" if (tp.upper() in constplist) else tp.upper().lower()));
        basestr = addstr + " " + myrettpstr + " ";
        if (myrettpstr == "table"): return basestr + tnm;
        else:
            #itemname is required now.
            #everything will have itemname from tablename
            myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(itnm, varnm="item name");
            fpart = itnm + " on " + tnm;
            midptstr = "";
            if (myrettpstr == "icolcons"):
                nltpslist = ["NONNULL", "NOTNULL", "NON-NULL", "NOT-NULL"];
                otpslist = ["UNIQUE", "UNSIGNED", "DATATYPE"];
                fintpslist = myvalidator.combineTwoLists(nltpslist, otpslist);
                myvalidator.itemMustBeOneOf(icltp.upper(), fintpslist, varnm="constpstr");
                finicltp = ("notnull" if (icltp.upper() in nltpslist) else icltp.upper().lower());
                midptstr = finicltp + " from ";
            return basestr + midptstr + fpart;
    @classmethod
    def addItemString(cls, tp, tnm, itnm="", icltp=""):
        return myvalidator.addOrDeleteItemString(True, tp, tnm, itnm=itnm, icltp=icltp);
    @classmethod
    def delItemString(cls, tp, tnm, itnm="", icltp=""):
        return myvalidator.addOrDeleteItemString(False, tp, tnm, itnm=itnm, icltp=icltp);


    #SQL methods might get removed from the validator class

    #will raise a value error if the constraint is not valid unless it is empty or null
    #in that case it will return false if it is valid it will return true;
    @classmethod
    def isConstraintValid(cls, mval):
        if (myvalidator.isvaremptyornull(mval)): return False;
        else:
            #the constraint must be in the following format:
            #CONSTRAINT name TYPE(value)
            #0123456789012345678901234567
            #0         1         2
            #the only valid constraint types are: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK
            #the name cannot include spaces newlines tabs etc and
            #is only alphanumeric with underscores.
            ivfmterrmsg = "the constraint value was not in the correct format! ";
            ivfmterrmsg += "It must be in: 'CONSTRAINT name TYPE(value)' format!";
            #print(f"mval = {mval}");
            
            if (mval.index("CONSTRAINT ") == 0): pass;
            else: raise ValueError(ivfmterrmsg);
            #the name starts at index 11 and ends at an indeterminate value, but the next space
            spci = -1;
            for i in range(11, len(mval)):
                if (mval[i] == ' '):
                    spci = i;
                    break;
            if (spci < 12): raise ValueError(ivfmterrmsg);
            mynmstr = mval[11:spci];
            #print(f"mynmstr = {mynmstr}");

            try:
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mynmstr, "mynmstr");
            except Exception as ex:
                #add the ex as the cause of this value error and then raise that.
                raise ValueError(ivfmterrmsg) from ex;
            #name is valid
            #type starts after the space index and goes to the first (
            opi = mval.index("(");
            if (12 < opi): pass;
            else: raise ValueError(ivfmterrmsg);
            tpstr = mval[spci + 1:opi];
            #print(f"tpstr = {tpstr}");

            if (tpstr in ["PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK"]): pass;
            else: raise ValueError(ivfmterrmsg);
            if (mval[len(mval) - 1] == ')'): pass;
            else: raise ValueError(ivfmterrmsg);
            #cannot error check the value itself here, but constraint is in the correct format
            #or appears to be...
            #we can still check the value somewhat using a leveling algorithmn
            #but we are pretty confident that it is in the correct format
            #?;
            return True;

    @classmethod
    def getNameFromConstraint(cls, cnst):
        if (myvalidator.isConstraintValid(cnst)): pass;
        else: raise ValueError("constraint (" + cnst + ") was not valid!");
        nmstr = cnst[11:];
        return nmstr[0: nmstr.index(" ")];


    @classmethod
    def genSQLConstraint(cls, consnm, constpnm, val):
        if (myvalidator.isvaremptyornull(constpnm)):
            return myvalidator.genSQLConstraint(cls, consnm, "CHECK", val);
        if (constpnm.isupper()): pass;
        else: return myvalidator.genSQLConstraint(consnm, constpnm.upper(), val);
        if (constpnm in ["CHECK", "UNIQUE", "PRIMARY KEY"]): pass;
        else: raise ValueError("invalid constraint type found and used here!");
        usechck = (constpnm == "CHECK");

        #myvalidator.varmustbeboolean(useunc, varnm="useunc");
        myvrnm = "constraint name";
        if (myvalidator.isvaremptyornull(consnm)):
            if (constpnm in ["CHECK", "UNIQUE"]):
                useunc = (not usechck);
                from mycol import mycol;#may need to change or get removed
                pnm = ("un" if (useunc) else "ch") + "mulcols_";
                fnm = pnm + str(mycol.incrementAndGetUniqueOrCheckConstraintCounterBy(useunc, 1));
                return myvalidator.genSQLConstraint(fnm, constpnm, val);
            else: myvalidator.varmustnotbeempty(consnm, varnm=myvrnm);
        else: myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(consnm, varnm=myvrnm);
        finval = "";
        if (usechck): finval = "" + val;#usecheck
        else:#use anything other than check
            #colnames are assumed to be on the table, because if they are not,
            #then SQL ERROR RESULTS IMMEDIATELY,
            #but this method may not take into account the correct table class as the caller
            #so cannot verify
            myvalidator.varmustbethetypeandornull(val, list, True, varnm="val");
            if (myvalidator.isvaremptyornull(val) or len(val) < 1): return None;
            else:
                for mcnm in val:
                    myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mcnm,
                                                                                    varnm="the colname");
                finval = (", ".join(val));
        return "CONSTRAINT " + consnm + " " + constpnm + "(" + finval + ")";
    @classmethod
    def genUniqueConstraint(cls, consnm, colnames):
        return myvalidator.genSQLConstraint(consnm, "UNIQUE", colnames);
    @classmethod
    def genSQLUnique(cls, consnm, colnames): return myvalidator.genUniqueConstraint(consnm, colnames);
    @classmethod
    def genCheckConstraint(cls, consnm, val):
        return myvalidator.genSQLConstraint(consnm, "CHECK", val);
    @classmethod
    def genSQLCheck(cls, consnm, val): return myvalidator.genCheckConstraint(consnm, val);
    @classmethod
    def genSQLPrimaryKeyConstraint(cls, consnm, colnames):
        return myvalidator.genSQLConstraint(consnm, "PRIMARY KEY", colnames);
    
    #this method does not assume that the foreign class has already been initialized
    #however, it is assumed that when CREATE TABLE is run that at least one object already exists
    @classmethod
    def genSQLForeignKeyConstraint(cls, consnm, colnm, ftblnm, refcolnames):
        #this method assumes that the colnm and recolnames and ref table name is valid.
        #we can still verify the formats and stuff of them...
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(consnm, varnm="consnm");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(colnm, varnm="colnm");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(ftblnm, varnm="ftblnm");
        if (myvalidator.isvaremptyornull(refcolnames) or len(refcolnames) < 1): return None;
        else:
            for mcnm in refcolnames:
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mcnm,
                                                                                varnm="the ref colname");
        myretstr = "CONSTRAINT " + consnm + " FOREIGN KEY(" + colnm + ") REFERENCES " + ftblnm + "(";
        return myretstr + (", ".join(refcolnames)) + ")";
    #this convenience method assumes that the foreign class has already been initialized here.
    #that assumption is only made if the foreign table name is not provided.
    @classmethod
    def genSQLForeignKeyConstraintFromColObj(cls, consnm, mcolobj, ftblnm=None):
        myvalidator.varmustnotbenull(mcolobj, varnm="mcolobj");
        finftblnm = None;
        fcolnms = mcolobj.getForeignColNames();
        merrmsgpta = "at least one of the foreign column names (" + str(fcolnms);
        if (myvalidator.isvaremptyornull(ftblnm)):
            fclsref = type(mcolobj).getMyClassRefFromString(mcolobj.getForeignClass());
            merrmsgpta += ") was not on the foreign table with class name (" + fclsref.__name__;
            finftblnm = fclsref.getTableName();
            allfcols = fclsref.getMyCols();
            if (fclsref.areGivenColNamesOnTable(fcolnms, mycols=allfcols)): pass;
            else:
                allfcolnames = fclsref.getMyColNames(mycols=allfcols);
                raise ValueError(merrmsgpta + ")! Its column names are (" + str(allfcolnames) + ")!");
        else: finftblnm = ftblnm;
        return myvalidator.genSQLForeignKeyConstraint(consnm, mcolobj.getColName(), finftblnm, fcolnms);

    #DOES NOT VALIDATE THE TABLE NAME, DOES NOT DEPEND ON IT, BUT THE OTHER LENGTH METHODS DO.
    @classmethod
    def genSQLLength(cls, colname):
        myvalidator.stringMustHaveAtMinNumChars(colname, 1, varnm="colname");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(colname, varnm="colname");
        return "LENGTH(" + colname + ")";

    @classmethod
    def genLengthCol(cls, colname, mtablename):
        myvalidator.varmustnotbeempty(colname, varnm="colname");
        from mycol import mycol;#may need to change or get removed
        myclstablenameref = mycol.getClassFromTableName(mtablename);
        myvalidator.varmustnotbenull(myclstablenameref, varnm="myclstablenameref");
        if (myclstablenameref.areGivenColNamesOnTable([colname], mycols=None)):
            return myvalidator.genSQLLength(colname);
        else: raise ValueError("the colname must be on the table!");


    #it is expected that ORDER BY and MIN or MAX appear after a SELECT statement in SQL
    #therefore, since SELECTs only run after the class has been initialized
    #we can assume the table name is defined already for these:

    #DOES NOT VALIDATE THE TABLE NAME, DOES NOT DEPEND ON IT, BUT THE OTHER MIN OR MAXS DO.
    @classmethod
    def genSQLMinOrMax(cls, usemin, valorvals):
        myvalidator.varmustbeboolean(usemin, varnm="usemin");
        myvalidator.varmustnotbeempty(valorvals, varnm="valorvals");
        finval = None;
        if (type(valorvals) == str): finval = "" + valorvals;
        elif (type(valorvals) in [list, tuple]): finval = myvalidator.myjoin(", ", valorvals);
        else: raise ValueError("valorvals must be either a string or a list!");
        return "M" + ("IN" if usemin else "AX") + "(" + finval + ")";

    @classmethod
    def genSQLMinOrMaxFromTable(cls, colname, tablename, singleinctname, usemin):
        myvalidator.varmustbeboolean(usemin, varnm="usemin");
        myvalidator.varmustbeboolean(singleinctname, varnm="singleinctname");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(colname, varnm="colname");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tablename, varnm="tablename");
        
        from mycol import mycol;#may need to change or get removed
        myclstablenameref = mycol.getClassFromTableName(tablename);
        myvalidator.varmustnotbenull(myclstablenameref, varnm="myclstablenameref");
        if (myclstablenameref.areGivenColNamesOnTable([colname], mycols=None)): pass;
        else: raise ValueError("the colname must be on the table!");
        finstr = "" + (tablename + "." if singleinctname else "") + colname;
        return myvalidator.genSQLMinOrMax(usemin, finstr);
    @classmethod
    def genSQLMinFromTable(cls, colname, tablename, singleinctname):
        return myvalidator.genSQLMinOrMaxFromTable(colname, tablename, singleinctname, True);
    @classmethod
    def genSQLMaxFromTable(cls, colname, tablename, singleinctname):
        return myvalidator.genSQLMinOrMaxFromTable(colname, tablename, singleinctname, False);
    
    @classmethod
    def genOrderBy(cls, colnames, tablenames, singleinctname, sorder=None):
        #if sorder.length is less than colnames.length:
        #then add ASC or nothing at the end...
        #if sorder.length is greater than colnames.length: error
        myvalidator.varmustnotbeempty(colnames, varnm="colnames");
        myvalidator.varmustnotbeempty(tablenames, varnm="tablenames");
        myvalidator.varmustbeboolean(singleinctname, varnm="singleinctname");
        basestr = "ORDER BY ";
        if (myvalidator.isvaremptyornull(sorder)):
            return basestr + myvalidator.combineTableNamesWithColNames(colnames, tablenames,
                                                                       singleinctname);
        else:
            if (len(colnames) < len(sorder)):
                raise ValueError("sorder must be at most as long as the number of columns!");
            if (len(tablenames) == len(colnames)): pass;
            else:
                if (len(tablenames) == 1): pass;
                else:
                    raise ValueError("there must be the same number of columns as tablenames " +
                                     "if there is more than one tablename!");
            from mycol import mycol;#may need to change or get removed
            mystr = "";
            clvarnm = "the colname";
            tnmvarnm = "the tablename";
            for n in range(len(colnames)):
                colnm = colnames[n];
                tnm = (tablenames[n] if (1 < len(tablenames)) else tablenames[0]);
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(colnm, varnm=clvarnm);
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tnm, varnm=tnmvarnm);
                myclstablenameref = mycol.getClassFromTableName(tnm);
                myvalidator.varmustnotbenull(myclstablenameref, varnm="myclstablenameref");
                if (myclstablenameref.areGivenColNamesOnTable([colnm], mycols=None)): pass;
                else: raise ValueError("the colname must be on the table!");
                
                #include the table name if not single,
                #include the table name if single and include is set to true
                inctnm = ((1 < len(tablenames)) or singleinctname);
                incval = (n < len(sorder));
                if (incval): myvalidator.varmustbeboolean(sorder[n], varnm=f"sorder[{n}]");
                mystr += "" + (tnm + "." if inctnm else "") + colnm;
                mystr += ((" ASC" if sorder[n] else " DESC") if incval else "");
                if (n + 1 < len(colnames)): mystr += ", ";
            return basestr + mystr;
    
    #ascending or descending all bool vals list of the same bool val
    @classmethod
    def genSortOrderByAscVal(cls, numcols, boolval):
        return myvalidator.genListOfBoolVals(numcols, boolval);
    
    #this convenience method combines the two methods needed for order by more or less.
    #
    #takes in the col names, but only one bool val will be used for the direction and one table name
    #however, if the SELECT statement this is attached to has multiple table names,
    #we need to include the single table name on the order by part.
    #if not, we mays still want to include the single table name. That is why the boolean is required.
    @classmethod
    def genOrderByOneTableOneVal(cls, colnames, tname, sinctname, boolval):
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tname, varnm="tname");
        sorder = myvalidator.genSortOrderByAscVal(len(colnames), boolval);
        return myvalidator.genOrderBy(colnames, [tname], sinctname, sorder=sorder);
    

    #create table methods here

    #NOT DONE YET WITH ALL OF THESE 4-30-2025 9:30 PM MST

    #bug here 4-21-2025 4 AM MST
    #added a small bug in the create table method to test or write a better leveling algorithm

    #DOES NOT VALIDATE THE TABLE NAME, DOES NOT DEPEND ON IT, BUT THE OTHER createTable methods DO.
    #HOWEVER, THIS METHOD ASSUMES THAT ALL MODEL CLASSES HAVE BEEN INITIALIZED OR
    #SETUP BEFORE THIS RUNS.
    #
    #varstr is the SQL VARIANT.
    #DEPENDS ON THE SQL VARIANT.
    @classmethod
    def genSQLCreateTable(cls, name, varstr, mycols, mulcolreqs, alltablereqs,
                          onlyifnot=True, isinctable=False):
        #this command has a very specific order of generating these
        #at least with constraints and primary keys
        myvalidator.varmustbeboolean(onlyifnot, varnm="onlyifnot");
        myvalidator.varmustbeboolean(isinctable, varnm="isinctable");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(name, varnm="name");
        myvalidator.varmustnotbeempty(mycols, varnm="mycols");
        myvalidator.stringMustHaveAtMinNumChars(varstr, 1, varnm="varstr");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(varstr, varnm="varstr");
        print("\nINSIDE OF GEN CREATE TABLE METHOD():");
        print(f"table name = {name}");
        print("mycols = [");
        numpkycols = 0;
        for mc in mycols:
            if (mc.isPrimaryKey()): numpkycols += 1;
            print(mc);
        print("]");
        print(f"mulcolreqs = {mulcolreqs}");
        print(f"alltablereqs = {alltablereqs}");
        print(f"numpkycols = {numpkycols}");

        myvalidator.valueMustBeInRange(numpkycols, 1, 0, True, False, varnm="#_of_primary_key_cols");
        
        #the column name will be displayed on each line FIRST
        #the data type of course will be displayed on each line SECOND
        #if there is only one primary key, we display that on the column
        #if an individual column is not-null or unique, etc. it goes on the col line
        #
        #be careful, we do not want to double up on the constraints lists...
        #
        #multi-col primary and foreign key and unique constraints should go second to last
        #all table constraints and multi-column constraints should go last
        #genUniqueConstraint(cls, consnm, colnames) could come in handy

        #https://www.w3schools.com/sql/sql_foreignkey.asp
        #https://www.w3schools.com/sql/sql_primarykey.asp
        #https://www.w3schools.com/sql/sql_autoincrement.asp
        #https://www.w3schools.com/sql/sql_unique.asp
        
        #what if we have the situation where the thing only has foreign keys and the primary key
        #is composed of said foreign keys?
        #what order do we put the keys in?

        #mstr = "";
        mstrs = [];
        haveonepkycol = (numpkycols == 1 and varstr == "LITE");
        for n in range(len(mycols)):
            mstr = "";
            mc = mycols[n];
            mstr += mc.getColName() + " " + mc.getDataType();
            #now not sure about the order of the other stuff
            #like AutoIncrement, primary_key, isnonnull, isunique, etc.
            #server defaults and there even maybe other stuff that I completely missed.
            #if col is a foreign key do we handle that at all here in this batch?
            
            if (mc.isPrimaryKey() and haveonepkycol): mstr += " PRIMARY KEY";

            #auto_increment is different or not supported this way on some DBs like ORACLE.
            if (mc.autoIncrements()):
                if (varstr == "LITE"): mstr += " AUTOINCREMENT";
                else: mstr += " AUTO_INCREMENT";
        
            if (mc.isNonNull()): 
                if (mc.autoIncrements()): pass;
                else: mstr += " NOT NULL";
        #    if (mc.isUnique()): mstr += "UNIQUE";#unique is also one that has different ways
        #    if (mc.isForeignKey()): mstr += "*?FOREIGN KEY?*";
            mstrs.append(mstr);
            #also need some ,s in there and maybe a newline for formatting sake???.
            #if (n + 1 < len(mycols)): mstr += ", ";
            #print(f"\nNEW mstrs = {mstrs}");
        print("\nAFTER FIRST LOOP:");
        print(f"mstrs = {mstrs}");

        #bug here 5-21-2025 4 AM
        #enmbasestr = "menm ENUM('something, other', 'some ofht', 'this, some, other, else', 'else', ";
        #enmodptstr = "'something else, other', 'last'";
        #finenmstr = enmbasestr + "'mychar\\\'s poses)sive', " + enmodptstr + ")";
        #oenumpstr = enmbasestr + "'mychar\'s poses)sive', " + enmodptstr + ")";
        #mstrs.append(finenmstr);
        
        for n in range(len(mycols)):
            mc = mycols[n];
            if (mc.isUnique()):
                mcnm = "" + mc.getColName();
                nwconstnm = "individualcol" + mcnm + "uniqueconstraint";
                nwuconst = myvalidator.genUniqueConstraint(nwconstnm, [mcnm]);
                #mstr += ", " + nwuconst;
                mstr = nwuconst;
                mstrs.append(mstr);
                mc.addConstraint(nwuconst, isinctable=isinctable);
                #print(f"\nNEW mstrs = {mstrs}");
        print("\nAFTER SECOND LOOP:");
        print(f"mstrs = {mstrs}");
        
        #now need to get all of the primary key columns and then make the pky constraint.
        if (haveonepkycol): pass;
        else:
            from mybase import mybase;
            pkycols = mybase.getMyPrimaryKeyCols(mycols);
            #mstr += ", ";
            nwpkyconst = myvalidator.genSQLPrimaryKeyConstraint("pkyfor" + name,
                                                                mybase.getMyColNames(pkycols));
            #mstr += nwpkyconst;
            mstrs.append(nwpkyconst);
            print("\nAFTER THE PRIMARY KEY:");
            print(f"mstrs = {mstrs}");
            
            #add this to the table here as a multi-col constraint or an individual column constraint
            #but there can only be one primary key constraint on the table.
            if (1 < numpkycols):
                #this is a multi-column primary key constraint
                from mycol import mycol;
                myclsref = mycol.getClassFromTableName(name);
                myclsref.addMultiColumnConstraint(nwpkyconst);
            else:
                #this is an individual column primary key constraint
                mc.addConstraint(nwpkyconst, isinctable=isinctable);

        #now get the foreign keys
        #if the foreign table name is provided, the assumption that all classes have been initialized
        #is not made, instead the assumption that that name is correct and that the foreign col names
        #are on that given foreign table name
        #
        #since the foreign table names are not stored in the mycol object class, but rather the
        #foreign class name is, we are forced to assume that all classes have been initialized.
        #that is before this method runs. unless there are no foreign keys on the column
        #or the foreign table names are stored in the mycol object class.
        #genSQLForeignKeyConstraintFromColObj(cls, consnm, mcolobj, ftblnm=None)
        for mc in mycols:
            if (mc.isForeignKey()):
                consnm = "fkeyreqsforcol" + mc.getColName();
                nwfkycolconst = myvalidator.genSQLForeignKeyConstraintFromColObj(consnm, mc);
                #mstr += ", " + nwfkycolconst;
                mstrs.append(nwfkycolconst);
                mc.addConstraint(nwfkycolconst, isinctable=isinctable);
                #print(f"\nNEW mstr = {mstr}");
        print("\nAFTER THIRD LOOP:");
        print(f"mstrs = {mstrs}");

        #now handle the other contraints...
        #the original constraint lists have changed since it was printed as have the objects
        #so if we have already included it or them on the mstrs we do not want to include it
        for mc in mycols:
            if (myvalidator.isvaremptyornull(mc.getConstraints())): pass;
            else:
                for mval in mc.getConstraints():
                    if (myvalidator.isConstraintValid(mval) and mval not in mstrs):
                        mstrs.append(mval);
        print(f"\nFINAL mstrs = {mstrs}");

        retstr = "CREATE TABLE " + name + (" IF NOT EXISTS " if (onlyifnot) else "") + "(";
        return retstr + (", ".join(mstrs)) + ");";
    
    #depends on the table name
    #
    #varstr is the SQL VARIANT.
    #DEPENDS ON THE SQL VARIANT.
    @classmethod
    def genSQLCreateTableFromRef(cls, myclsref, varstr, onlyifnot=True):
        myvalidator.varmustnotbenull(myclsref, varnm="myclsref");
        errmsg = "myclsref must be a subclass of mybase class and not mybase, but it was not!";
        from mybase import mybase;#may need to change or get removed
        if (issubclass(myclsref, mybase) and not myclsref == mybase): pass;
        else: raise TypeError(errmsg);
        return cls.genSQLCreateTable(myclsref.getTableName(), varstr, myclsref.getMyCols(),
                                     myclsref.getMultiColumnConstraints(),
                                     myclsref.getAllTableConstraints(), onlyifnot=onlyifnot);
    
    #depends on the table name
    #
    #varstr is the SQL VARIANT.
    #DEPENDS ON THE SQL VARIANT.
    @classmethod
    def genSQLCreateTableFromTableOrClassName(cls, name, varstr, isclsnm, onlyifnot=True):
        #if name is classname get class ref from the name then call the other method
        #look up the classname if valid or on the list;
        #if it is not valid => error.
        #this is a tablename
        #we need to get the class name with the table name
        #then we can get the reference...
        #if not valid => error.
        myvalidator.varmustbeboolean(onlyifnot, varnm="onlyifnot");
        myvalidator.varmustbeboolean(isclsnm, varnm="isclsnm");
        
        from mycol import mycol;#may need to change or get removed
        myfuncref = (mycol.getMyClassRefFromString if (isclsnm) else mycol.getClassFromTableName);
        return cls.genSQLCreateTableFromRef(myfuncref(name), varstr, onlyifnot=onlyifnot);
    @classmethod
    def genSQLCreateTableFromTableName(cls, name, varstr, onlyifnot=True):
        return cls.genSQLCreateTableFromTableOrClassName(name, varstr, False, onlyifnot=onlyifnot);
    @classmethod
    def genSQLCreateTableFromClassName(cls, name, varstr, onlyifnot=True):
        return cls.genSQLCreateTableFromTableOrClassName(name, varstr, True, onlyifnot=onlyifnot);
    
    @classmethod
    def genSQLDropTable(cls, tname, onlyifnot=False):
        myvalidator.varmustbeboolean(onlyifnot, varnm="onlyifnot");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tname, varnm="tname");
        return "DROP TABLE " + ("IF EXISTS " if (onlyifnot) else "") + tname + ";";

    #IF EXISTS IS NOT SUPPORTED ON THE TRUNCATE NOR IS IT SUPPORTED ON THE DELETE COMMANDS
    @classmethod
    def genSQLTruncateTable(cls, tname):
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tname, varnm="tname");
        return "TRUNCATE TABLE " + tname + ";";

    #does not end with a semi-colon.
    @classmethod
    def genSQLDeleteNoWhere(cls, mtname):
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mtname, varnm="mtname");
        return "DELETE FROM " + mtname;
    @classmethod
    def genSQLClearTable(cls, mtname): return myvalidator.genSQLDeleteNoWhere(mtname);
    
    @classmethod
    def genSQLDelete(cls, mtname, colnms):
        myretstr = myvalidator.genSQLDeleteNoWhere(mtname) + " WHERE ";
        return myretstr + myvalidator.genColNameEqualsValString(colnms, nvals=None) + ";";
    

    #NOT TESTED WELL YET AND NOT NECESSARILY DONE YET 5-8-2025 3:50 AM MST...

    #possible bug found 5-8-2025 3:50 AM MST in the UPDATE and INSERT INTO command methods:
    #the values if they are strings must include quotes of some kind, but probably will not...

    @classmethod
    def genColNameEqualsValOrQuestionString(cls, colnames, inccolnms, nvals=None):
        myvalidator.varmustbeboolean(inccolnms, varnm="inccolnms");
        incnvals = (not myvalidator.isvaremptyornull(nvals));
        if (incnvals):
            myvalidator.twoListsMustBeTheSameSize(colnames, nvals, arranm="colnames", arrbnm="nvals");
        mstr = "";
        for n in range(len(colnames)):
            mstr += "" + (colnames[n] + " = " if (inccolnms) else "");
            mstr += (nvals[n] if (incnvals) else "?");
            if (n + 1 < len(colnames)): mstr += ", ";
        return mstr;
    @classmethod
    def genColNameEqualsValString(cls, colnames, nvals=None):
        return myvalidator.genColNameEqualsValOrQuestionString(colnames, True, nvals=nvals);
    @classmethod
    def genQuestionString(cls, colnames):
        return myvalidator.genColNameEqualsValOrQuestionString(colnames, False, nvals=None);

    @classmethod
    def genSQLInsertInto(cls, mtname, colnames, vals=None):
        #the colnames are all of the required col names at minimum,
        #but if the column is say an integer primary key that autoincrements,
        #then we do not need to provide the value here nor do we need to provide its name
        #however, the values must correspond with the colnames...
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mtname, varnm="mtname");
        mstr = "";
        if (myvalidator.isvaremptyornull(vals)): mstr = myvalidator.genQuestionString(colnames);
        else: mstr = myvalidator.myjoin(", ", vals);
        return "INSERT INTO " + mtname + "(" + (", ".join(colnames)) + ") VALUES (" + mstr + ");";
    @classmethod
    def genSQLInsertIntoFromClsRef(cls, myclsrf, vals=None):
        return myvalidator.genSQLInsertInto(myclsrf.getTableName(), myclsrf.getMyColNames(), vals=vals);

    @classmethod
    def genSQLUpdate(cls, mtname, colnames, wrval, nvals=None):
        #UPDATE tablename SET colnamea = ?, colnameb = ?, ... WHERE pkycolname = ?;
        #UPDATE tablename SET colnamea = newvalue, colnameb = newvalue, ...
            # WHERE colnamea = oldvalue; (or just use the primary key to access it).
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(mtname, varnm="mtname");
        myvalidator.stringMustHaveAtMinNumChars(wrval, 1, varnm="wrval");
        mstr = myvalidator.genColNameEqualsValString(colnames, nvals=nvals);
        return "UPDATE " + mtname + " SET " + mstr + " WHERE " + wrval + ";";


    #SELECT whatval/tablenames.colnames/* FROM whereval/tablenames
    #SELECT DISTINCT whatval/table.colnames/* FROM whereval/tablenames
    #
    #DATA ON THE SELECT OFTEN COMES FROM A SPECIFIC TABLE OR MULTIPLE TABLES
    #BUT DATA ON THE SELECT CAN COME FROM A CUSTOM BUILT TABLE ON THAT SELECT THE WHEREVALUE.
    #IF IT COMES FROM THE WHEREVALUE, THEN THE WHEREVALUE TABLE CREATED MAY HAVE A
    #SHORTER OR A GIVEN NAME, BUT DOES NOT HAVE TO. 

    #COUNT(tablenames.colnames/*)
    #COUNT(DISTINCT tablenames.colnames/*)
    #
    #THE COUNT DOES NOT NEED THE TABLENAME IF THERE IS ONLY ONE TABLE BEING USED IN THE SELECT WITH IT
    #THE WITH COUNTS THE TABLE IN THE COUNT AS 1. SO IF THAT IS THE ONLY ONE, THEN NO TABLENAME NEEDED.
    #OTHERWISE THE TABLE NAMES ARE NEEDED.
    #THE COUNT MUST ALWAYS INCLUDE A COLUMN NAME OR THE * NOT NUMBERS.

    #BUT FOR SOME REASON, YOU CANNOT HAVE:
    #SELECT DISTINCT COUNT(DISTINCT *) FROM whereval/tablenames

    #DOES NOT VALIDATE THE TABLE NAME, DOES NOT DEPEND ON IT, BUT THE OTHER SELECTS DO.
    @classmethod
    def genCustomSelect(cls, wtval, wrval, usedistinct=False):
        myvalidator.varmustbeboolean(usedistinct, varnm="usedistinct");
        myvalidator.varmustbethetypeonly(wtval, str, varnm="wtval");
        myvalidator.varmustbethetypeonly(wrval, str, varnm="wrval");
        myvalidator.varmustnotbeempty(wtval, varnm="wtval");
        myvalidator.varmustnotbeempty(wrval, varnm="wrval");
        errmsg = "INVALID SQL QUERY: \"SELECT DISTINCT *, COUNT(DISTINCT *)\" IS NOT ALLOWED!";
        if ("COUNT(DISTINCT *)" in wtval): raise ValueError(errmsg);
        return "SELECT " + ("DISTINCT " if usedistinct else "") + wtval + " FROM " + wrval;
    
    @classmethod
    def genCount(cls, colnames, tablenames, inctnameonone=False, usedistinct=False):
        myvalidator.varmustbeboolean(inctnameonone, varnm="inctnameonone");
        myvalidator.varmustbeboolean(usedistinct, varnm="usedistinct");
        isonetable = False;
        nomtnmerrmsg = "there must be at least one tablename if there is at least one colname, but ";
        nomtnmerrmsg += "there was not!";
        tnmsclnmserrmsg = "the number of the tablenames and columnnames must be the same!";
        if (myvalidator.isvaremptyornull(colnames)):
            if (myvalidator.isvaremptyornull(tablenames)):
                return "COUNT(" + ("DISTINCT " if usedistinct else "") + "*)";
            else:
                return myvalidator.genCount(None, None,
                                            inctnameonone=inctnameonone, usedistinct=usedistinct);
        else:
            if (myvalidator.isvaremptyornull(tablenames)): raise ValueError(nomtnmerrmsg);
            else:
                isonetable = (len(tablenames) == 1);
                if (len(colnames) == len(tablenames) or isonetable): pass;
                else: raise ValueError(tnmsclnmserrmsg);
        #if there is more than one table, we need to include the tablename
        #if there is one table, we may still need it, we may not
        #for validation purposes either way we do need it.
        inctnm = (inctnameonone if isonetable else True);
        from mycol import mycol;#may need to change or get removed
        mystr = "";
        errmsgpta = "the colname (";
        errmsgptb = ") must be found on the table class(";
        for n in range(len(colnames)):
            #need to verify that the col name is on the corresponding table
            mcnm = colnames[n];
            tnm = (tablenames[0] if isonetable else tablenames[n]);
            myvalidator.varmustnotbeempty(mcnm, varnm="mcnm");
            myclstablenameref = mycol.getClassFromTableName(tnm);
            myvalidator.varmustnotbenull(myclstablenameref, varnm="myclstablenameref");
            if (myclstablenameref.areGivenColNamesOnTable([mcnm], mycols=None)):
                mystr += "" + (tnm + "." if inctnm else "") + mcnm;
                if (n + 1 < len(colnames)): mystr += ", ";
            else: raise ValueError(errmsgpta + mcnm + errmsgptb + myclstablenameref.__name__ + ")!");
        return "COUNT(" + ("DISTINCT " if usedistinct else "") + mystr + ")";
    @classmethod
    def genCountAll(cls, usedistinct=False):
        return myvalidator.genCount(None, None, inctnameonone=False, usedistinct=usedistinct);

    @classmethod
    def genSelectAllAndOrCountOnTables(cls, seltbles, cntcols, cnttables, useselonly=False,
        useseldistinct=False, usecntdistinct=False):
            myvalidator.varmustbeboolean(useselonly, varnm="useselonly");
            myvalidator.varmustbeboolean(useseldistinct, varnm="useseldistinct");
            myvalidator.varmustbeboolean(usecntdistinct, varnm="usecntdistinct");
            errmsg = "INVALID SQL QUERY: \"SELECT DISTINCT *, COUNT(DISTINCT *)\" IS NOT ALLOWED!";
            if (useseldistinct == usecntdistinct):
                if (useselonly): pass;
                else:
                    if (useseldistinct):
                        if (myvalidator.isvaremptyornull(cntcols)): raise ValueError(errmsg);
            myutnames = list(set(myvalidator.combineTwoLists(seltbles, cnttables)));
            mylenutnms = len(myutnames);
            inctname = (1 < mylenutnms);
            myvalidator.varmustnotbeempty(myutnames, varnm="myutnames");
            mywtstr = "*";
            if (useselonly): pass;
            else:
                mywtstr += ", " + myvalidator.genCount(cntcols, cnttables, inctnameonone=inctname,
                                                       usedistinct=usecntdistinct);
            wrval = ", ".join(myutnames);
            return myvalidator.genCustomSelect(mywtstr, wrval, usedistinct=useseldistinct);
    @classmethod
    def genSelectAllAndCountOnTables(cls, seltbles, cntcols, cnttables, useseldistinct=False,
                                     usecntdistinct=False):
            return myvalidator.genSelectAllAndOrCountOnTables(seltbles, cntcols, cnttables,
                        useselonly=False, useseldistinct=useseldistinct, usecntdistinct=usecntdistinct);
    @classmethod
    def genSelectAllAndCountAllOnTables(cls, seltbles, useseldistinct=False, usecntdistinct=False):
        return myvalidator.genSelectAllAndCountOnTables(seltbles, None, None,
                                        useseldistinct=useseldistinct, usecntdistinct=usecntdistinct);
    @classmethod
    def genSelectAllOnlyOnTables(cls, seltbles, useseldistinct=False):
        return myvalidator.genSelectAllAndOrCountOnTables(seltbles, None, None, useselonly=True,
                                                    useseldistinct=useseldistinct, usecntdistinct=False);
    
    @classmethod
    def genSelectSomeAndOrCountOnTables(cls, selcols, seltbles, cntcols, cnttables,
                                        useselonly=False, usecntonly=False, useseldistinct=False,
                                        usecntdistinct=False):
        myvalidator.varmustbeboolean(useseldistinct, varnm="useseldistinct");
        myvalidator.varmustbeboolean(usecntdistinct, varnm="usecntdistinct");
        myvalidator.twoBoolVarsMustBeDifferent(useselonly, usecntonly,
                                               varnma="useselonly", varnmb="usecntonly");
        
        errmsg = "INVALID SQL QUERY: \"SELECT DISTINCT *, COUNT(DISTINCT *)\" IS NOT ALLOWED!";
        if (useseldistinct == usecntdistinct):
                if (useselonly): pass;
                else:
                    if (useseldistinct):
                        if (myvalidator.isvaremptyornull(cntcols)): raise ValueError(errmsg);
    
        #if use select only: no counts
        #if use count only it will be inside of select statement still.
        #we will still need the seltables, and cntcols and cnttables...
        #SELECT DISTINCT? tnamea.colnamea, tnameb.colnameb ...,
        #COUNT(DISTINCT? tnamea.colnamea, tnameb.colnameb ...) FROM alluniquetnames
        myutnames = list(set(myvalidator.combineTwoLists(seltbles, cnttables)));
        mylenutnms = len(myutnames);
        inctname = (1 < mylenutnms);
        myvalidator.varmustnotbeempty(myutnames, varnm="myutnames");
        wtval = "";
        wrval = "";
        if (useselonly):
            wtval = myvalidator.combineTableNamesWithColNames(selcols, seltbles, inctname);
            wrval = ", ".join(seltbles);
        else:
            #either way we need the count here now...
            #either way the where is the combined list of unique table names...
            cntvalstr = myvalidator.genCount(cntcols, cnttables,
                                             inctnameonone=inctname, usedistinct=usecntdistinct);
            wrval = ", ".join(myutnames);
            if (usecntonly): wtval = cntvalstr;
            else:
                wtval = myvalidator.combineTableNamesWithColNames(selcols, seltbles, inctname);
                wtval += ", " + cntvalstr;
        return myvalidator.genCustomSelect(wtval, wrval, usedistinct=useseldistinct);

    @classmethod
    def genSelectCountOnlyOnTables(cls, seltbles, cntcols, cnttables, useseldistinct=False,
                                   usecntdistinct=False):
        return myvalidator.genSelectSomeAndOrCountOnTables(None, seltbles, cntcols, cnttables,
                                useselonly=False, usecntonly=True, useseldistinct=useseldistinct,
                                usecntdistinct=usecntdistinct);
    @classmethod
    def genSelectSomeOnlyOnTables(cls, selcols, seltbles, useseldistinct=False):
        return myvalidator.genSelectSomeAndOrCountOnTables(selcols, seltbles, None, None,
                useselonly=True, usecntonly=False, useseldistinct=useseldistinct, usecntdistinct=False);

    #THESE SQL METHODS DO NOT DEPEND ON THE TABLE NAME AT ALL:
    #
    #note: the genCustomSelect() and genSQLMinOrMax() do not depend on the table name at all,
    #but all other select and min or max methods do as you are selecting data from a table.
    #
    #When I say these do not depend on it, they do not need it from the class
    #you may pass it in, but it does not get validated.

    @classmethod
    def genSQLSumOrAvg(cls, val, usedistinct, usesum):
        myvalidator.varmustbeboolean(usesum, varnm="usesum");
        myvalidator.varmustbeboolean(usedistinct, varnm="usedistinct");
        myvalidator.varmustbethetypeonly(val, str, varnm="val");
        myvalidator.varmustnotbeempty(val, varnm="val");
        return ("SUM" if usesum else "AVG") + "(" + ("DISTINCT " if usedistinct else "") + val + ")";
    @classmethod
    def genSQLSumOrAverage(cls, val, usedistinct, usesum):
        return myvalidator.genSQLSumOrAvg(val, usedistinct, usesum);
    @classmethod
    def genSQLSum(cls, val, usedistinct): return myvalidator.genSQLSumOrAvg(val, usedistinct, True);
    @classmethod
    def genSQLAvg(cls, val, usedistinct): return myvalidator.genSQLSumOrAvg(val, usedistinct, False);

    @classmethod
    def genSQLimit(cls, num, offset=0):
        if (num == None or offset == None): raise ValueError("illegal number or offset used!");
        elif (type(num) == int and type(offset) == int): pass;
        else: raise ValueError("illegal number or offset used!");
        if (num < 1 or offset < 0): raise ValueError("illegal number or offset used!");
        return (f"LIMIT {num}" if (offset == 0) else f"LIMIT {num} OFFSET {offset}");
    
    @classmethod
    def genGroupBy(cls, val):
        #GROUP BY(tablenamea.colnamea, tablenameb.colnameb ...);#GROUP BY(COUNT(CustomerID))
        myvalidator.varmustnotbeempty(val, varnm="val");
        return "GROUP BY(" + val + ")";

    @classmethod
    def genBetween(cls, vala, valb):
        myvalidator.varmustnotbenull(vala, varnm="vala");
        myvalidator.varmustnotbenull(valb, varnm="valb");
        return f"BETWEEN {vala} AND {valb}";

    @classmethod
    def genSQLIn(cls, mvals, incnull=False):
        myvalidator.varmustbeboolean(incnull, varnm="incnull");
        for val in mvals:
            if (val == None):
                return myvalidator.genSQLIn([oval for oval in mvals if not (oval == None)],
                                            incnull=True);
        return ("IN(NULL)" if (myvalidator.isvaremptyornull(mvals)) else "IN(" +
                ("NULL" + (", " if (0 < len(mvals)) else "")  if incnull else "") +
                myvalidator.myjoin(", ", mvals) + ")");
    
    @classmethod
    def genWhereOrHaving(cls, mval, usewhere):
        myvalidator.varmustbeboolean(usewhere, varnm="usewhere");
        myvalidator.varmustbethetypeonly(mval, str, varnm="mval");
        myvalidator.varmustnotbeempty(mval, varnm="mval");
        #note: WHERE does not allow agragate functions where as HAVING does,
        #but this is not easily enforced because the mval may have it elsewhere...
        #so no validation other than type will be preformed and the error will propogate down to the DB.
        return ("WHERE " if usewhere else "HAVING ") + mval;
    @classmethod
    def genWhere(cls, mval): return myvalidator.genWhereOrHaving(mval, True);
    @classmethod
    def genHaving(cls, mval): return myvalidator.genWhereOrHaving(mval, False);

    #SQL-SWITCH-CASE statement looks like:
    #CASE
    #   WHEN condition1 THEN result1
    #   ...
    #   ELSE defaultresult
    #END;
    #note: NO TABS, and no newline between case and the first when.
    @classmethod
    def genSQLSwitchCase(cls, condsarr, resarr, defres=None, csnm=None):
        myvalidator.twoArraysMustBeTheSameSize(condsarr, resarr, arranm="condsarr", arrbnm="resarr");
        addfnwline = False;
        addtabs = False;
        mystr = "CASE" + ("\n" if addfnwline else " ");
        for n in range(len(condsarr)):
            ccond = condsarr[n];
            cres = resarr[n];
            myvalidator.varmustnotbeempty(ccond, varnm="ccond");
            myvalidator.varmustnotbeempty(cres, varnm="cres");
            if (addtabs): mystr += "\t";
            mystr += "WHEN " + ccond + " THEN " + cres  + "\n";
        if (addtabs): mystr += "\t";
        mystr += "ELSE " + ("NULL\n" if (myvalidator.isvaremptyornull(defres)) else "" + defres + "\n");
        mystr += "END" + ("" if (myvalidator.isvaremptyornull(csnm)) else " AS " + csnm) + "\n";
        return mystr;
    @classmethod
    def genSQLSwitchCaseWithName(cls, condsarr, resarr, csnm, defres=None):
        return myvalidator.genSQLSwitchCase(condsarr, resarr, defres, csnm);
    @classmethod
    def genSQLSwitchCaseNoName(cls, condsarr, resarr, defres=None):
        return myvalidator.genSQLSwitchCase(condsarr, resarr, defres, None);

    @classmethod
    def getCompleteSetListFromList(cls, mlist):
        #print(f"mlist = {mlist}");
        if (mlist == None): return None;
        elif (len(mlist) < 1): return [];
        elif (len(mlist) == 1): return [mlist[0]];
        elif (len(mlist) == 2):
            #a, b
            #a,b, b,a
            return [mlist[0], mlist[1], mlist[0] + "," + mlist[1], mlist[1] + "," + mlist[0]];
        else:
            #keep all items initially on the list
            #then take a and add 1 of them only
            #then take a and add 2 of them only
            #then take a and add 3 of them only
            #... until all are done for item a
            #then repeat for the other items
            #example: a, b, c, d, e, f
            #a,b, a,c, a,d, a,e, a,f
            #a,b,c, a,b,d, a,b,e, a,b,f, a,c,d, a,c,e, a,c,f, 
            retlist = [mitem for mitem in mlist];
            for mitem in mlist:
                tmplist = myvalidator.getCompleteSetListFromList([item for item in mlist
                                                                  if not(item == mitem)]);
                #print(f"tmplist = {tmplist}");
                for item in tmplist: retlist.append(mitem + "," + item);
            return retlist;


    #MOST OF THE METHODS BELOW HERE DEPEND ON THE SQL VARIANT


    #https://www.w3schools.com/sql/sql_datatypes.asp
    #https://www.w3resource.com/sqlite/sqlite-data-types.php
    #https://www.w3resource.com/mysql/mysql-data-types.php
    #https://blog.devart.com/mysql-data-types.html
    #https://www.geeksforgeeks.org/sql-tutorial/?ref=shm
    #https://www.tutorialspoint.com/mysql/
    #https://dev.mysql.com/doc/refman/8.4/en/fractional-seconds.html#:
    #~:text=MySQL%20has%20fractional%20seconds%20support,is%20the%20fractional%20seconds%20precision.
    #https://www.dbvis.com/thetable/the-ultimate-guide-to-the-sql-server-date-format/
    #https://www.sqlshack.com/different-sql-timestamp-functions-in-sql-server/
    #https://www.mssqltips.com/sqlservertip/6575/sql-server-data-types/
    #https://count.co/sql-resources/sql-server/data-types
    #https://support.microsoft.com/en-us/office/
    #data-types-for-access-desktop-databases-df2b83ba-cef6-436d-b679-3418f622e482
    #https://support.microsoft.com/en-us/office/
    #introduction-to-data-types-and-field-properties-30ad644f-946c-442e-8bd2-be067361987c
    #https://www.linkedin.com/pulse/part-8-overview-sqlite-data-types-integer-text-blob-etc-julles/
    #https://dev.mysql.com/doc/refman/8.4/en/constraint-enum.html
    #https://dev.mysql.com/doc/refman/8.4/en/enum.html
    #https://www.geeksforgeeks.org/enumerator-enum-in-mysql/
    #https://www.tutorialspoint.com/mysql/mysql-enum.htm
    #https://learnsql.com/blog/mysql-data-types/
    #https://www.programiz.com/sql/min-and-max
    #
    #if using lite:
    #
    #INTEGER AND REAL ARE 8 BYTES MAX (1byte=8bits,so 64bits, signed)
    #integer signed range: -9223372036854775808 to 9223372036854775807
    #integer unsigned range: 0 to 18446744073709551615 (2^64-1 absolute max of course).
    #real signed range: -3.402*10^38 to 3.402*10^38
    #TEXT max length: 2^31-1 bytes max
    #BLOB max size in bytes: 2^31-1 bytes max
    #
    #return ["NULL", "REAL", "INTEGER", "TEXT", "BLOB"];
    #
    #if not using lite:
    #
    #MYSQL:
    #
    #CHAR(size) size is length 0 to 255 inclusive default is 1.
    #VARCHAR(size) size max length 0 to 65535 inclusive default is 1.
    #BINARY(size) size in bytes default is 1 similar to char (8 I believe, but not stated).
    #VARBINARY(size) size in bytes default is 1 similar to varchar (8 I believe, but not stated).
    #TINYBLOB size in bytes max length is 255 bytes (but no size parameter given).
    #TINYTEXT max length in characters is 255 characters (but no size parameter given).
    #TEXT(size) size in bytes max length is 65,535 bytes.
    #BLOB(size) (Binary Large OBjects) size in bytes max length is 65,535 bytes.
    #MEDIUMTEXT max length in characters is 16,777,215 characters.
    #MEDIUMBLOB for (Binary Large OBjects) size in bytes max length is 16,777,215 bytes.
    #LONGTEXT max length in characters is 4,294,967,295 characters.
    #LONGBLOB for (Binary Large OBjects) size in bytes max length is 4,294,967,295 bytes.
    #
    #NOTES FOR ENUMS AND SETS HERE:
    #
    #if the value is not on the enum list, then it is not valid
    #(in strict error, not strict, empty or null will be inserted instead)
    #either way it should return false.
    #
    #a set is different, if it is a member of one or more it is valid
    #both set and enum do not allow duplicate values
    #SET('a', 'b', 'c');
    #new values: '' valid, 'NULL' valid, 'a,b' valid, but 'ab' is not
    #(in strict error, not strict, ignored).
    #
    #ENUM(values) you can have 65,535 values and they map to an integer index,
    # you can either use that or the given values in the ENUM.
    # If a value not on the list is entered then a blank value will be inserted.
    #SET(values) you can have 0 up to 64 values.
    #
    #ALL NUMERIC DATA TYPES BELOW FOR MYSQL HAVE THE OPTIONS: UNSIGNED OR ZEROFILL
    #UNSIGNED MEANS ZERO OR POSITIVE ONLY AND ACTS AS AN OFFSET. ZEROFILL IS SIMILAR.
    #note: the size parameter has sort of been depricated (so add an option to not have it)
    #absolute size max is 255 though. Minimum is 1. This refers to how many digits to display,
    #but does not really have any affect.
    #note: ZEROFILL suppose you have an INT(3) and you insert 1 into it: the value is 001
    #that is the only time the size parameter will be taken into account and used.
    #note: due to size being depricated ZEROFILL has also been sort of depricated.
    #note: if you want something to be UNSIGNED you need to include UNSIGNED else it will be signed.
    #note: unsigned FLOAT will be depricated due to data storage requirements and
    #it being an integer.
    #note: FLOAT(size, d) is depricated due to size being depricated.
    #
    #BIT(size) size can be from 1 to 64 inclusive. 64 bit processor.
    #TINYINT(size) signed is from -127 to 128 inclusive unsigned 0 to 255 inclusive.
    # size maximum display width for the maximum number which is 255 (so max size is 3).
    #BOOL, BOOLEAN zero is false, everything else is true.
    #SMALLINT(size) signed is from -32768 to 32767 inclusive; unsigned is from 0 to 65535
    # size maximum display width which is 5 digits for 65535.
    #MEDIUMINT(size) signed is from -8388608 to 8388607 unsigned is from 0 to 16777215.
    #INTEGER(size), INT(size) signed is from -2147483648 to 2147483647
    # unsigned is from 0 to 4294967295.
    #BIGINT(size) signed is from -9223372036854775808 to 9223372036854775807
    # unsigned is from 0 to 18446744073709551615. (2^64-1 is absolute max of course).
    #
    #IT IS ALSO STRONGLY SUGGESTED TO USE BELOW WITHOUT PARAMETERS.
    #
    #FLOAT(size, d), DOUBLE(size, d), DOUBLE PRECISION(size, d) are depricated where
    # size is the number of digits, d is the number of digits after the decmial point.
    #
    #FLOAT(p) where p is the precision in bits if p is 0 to 24 FLOAT else 25 to 53 DOUBLE.
    #range -3.40*10^38 to 3.40*10^38 4 bytes.
    #DOUBLE(size, d), DOUBLE PRECISION(size, d) is depricated where size is the
    # total number of digits, d is the number of digits after the decmial point, same as a float.
    #DECIMAL(size, d), DEC(size, d) size is the total number of digits,
    # d is the number of digits after the decmial point, same as a float.
    #the maximum number for size is 65. The maximum number for d is 30.
    #default for size 10 and d is 0.
    #this means that the maximum magnitude for this number has 65 9s in it.
    #99999999999999999999999999999999999999999999999999999999999999999
    #
    #DATE format YYYY-MM-DD starting from 1000-01-01 to 9999-12-31.
    #DATETIME(fsp) format YYYY-MM-DD hh:mm:ss same date starting from 00:00:00 to 23:59:59.
    #if you want the current date and time add DEFAULT and ON UPDATE. the fsp max is 6 and default
    #if omitted it is 0. This means you can have 6 decimal places.
    #TIMESTAMP(fsp) same format as above UTC time seconds since 1970-01-01 00:00:00.0.
    #Starting from 1970-01-01 00:00:01 to 2038-01-09 03:14:07. You can have the current time with
    #DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP.
    #TIME(fsp) format hh:mm:ss starting from -838:59:59 to 838:59:59. no idea why on that range.
    #YEAR starting from 1901 to 2155 and 0000. 2 digit years are not supported in version 8.0.
    #
    #return ["CHAR(size)", "VARCHAR(size)", "BINARY(size)", "VARBINARY(size)", "TINYBLOB",
    # "TINYTEXT", "TEXT(size)", "BLOB(size)", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT", "LONGBLOB",
    # "ENUM(values...)", "SET(values...)", "BIT(size)", "TINYINT(size)", "BOOL", "BOOLEAN",
    # "SMALLINT(size)", "MEDIUMINT(size)", "INTEGER(size)", "INT(size)", "BIGINT(size)",
    # "FLOAT(size, d)", "FLOAT(p)", "DOUBLE(size, d)", "DOUBLE PRECISION(size, d)",
    # "DECIMAL(size, d)", "DEC(size, d)", "FLOAT", "DOUBLE PRECISION", "DOUBLE", "DATE",
    # "DATETIME(fsp)", "TIMESTAMP(fsp)", "TIME(fsp)", "YEAR", "DATETIME", "TIMESTAMP", "TIME"];
    #
    #SQL SERVER:
    #
    #CHAR(n) fixed length non-unicode characters each takes up 1 byte n is from 1 to 8000 inclusive.
    #VARCHAR(n) variable length non-unicode characters same as char(n) otherwise.
    #VARCHAR(max) variable length non-unicode characters up to 2 GB of space.
    #NCHAR(n) fixed length unicode characters each takes up 2 bytes n is from 1 to 4000 inclusive.
    #NVARCHAR(n) variable length unicode characters same as char(n) otherwise.
    #NVARCHAR(max) variable length unicode characters up to 2 GB of space.
    #BINARY(n) fixed length binary characters each takes up 1 byte n is from 1 to 8000 inclusive.
    #VARBINARY(n) variable length binary same as binary(n) otherwise.
    #VARBINARY(max) variable length binary up to 2 GB of space.
    #
    #BIT integer than can be 0, 1, or NULL.
    #TINYINT allows integers from 0 to 255 inclusive.
    #SMALLINT allows integers between -32768 and 32767 inclusive.
    #INT allows integers between -2147483648 and 2147483647 inclusive.
    #BIGINT allows integers between -9223372036854775808 and 9223372036854775807 inclusive.
    #DECIMAL(size, d) size is the total number of digits like size,
    # and d is the number of digits after the decimal point.
    #size must be from 1 to 38 inclusive. d default is 0, size default is 18.
    #for fixed precision and scale numbers.
    #
    #note: 2^64-1 =                                      18,446,744,073,709,551,615
    #note: python can store 10^38. pow(10, 38) - 1 is how I got it or 10**38 - 1 will also work.
    #
    #range is -10^38, 10^38-1: -100,000,000,000,000,000,000,000,000,000,000,000,000
    #                            99,999,999,999,999,999,999,999,999,999,999,999,999
    #                              ^           ^           ^           ^
    #NUMERIC(size, d) is the same as DECIMAL(size, d).
    #SMALLMONEY allows numbers between -214748.3648 to 214748.3647 inclusive.
    #MONEY allows numbers between -922337203685477.5808 and 922337203685477.5807 inclusive.
    #FLOAT(p) p max value is 53 and min is 1 if p is less than 25: 4 bytes (7 digits),
    # else 25 to 53 inclusive 8 bytes (15 digits) in size.
    #range is from -1.79*10^308 to 1.79*10^308 for 15 digits (after decimal point).
    #REAL range -3.40*10^38 to 3.40*10^38 4 bytes.
    #
    #note: the nanoseconds are optional but there if the format can store it.
    #King Henry Died Mother Didn't Care Much
    #Kilo Hecto Deca Mother. Deci Centi Mili ???
    #
    #DATETIME YYYY-MM-DD HH:MM:SS[.NNN] from 1753-01-01 to 9999-12-31
    # with an accuracy of 3.33 miliseconds.
    #DATETIME2 YYYY-MM-DD HH:MM:SS[.NNNNNNN] from 0001-01-01 to 9999-12-31
    # with an accuracy of 100 nanoseconds.
    #SMALLDATETIME YYYY-MM-DD HH:MM:SS from 1900-01-01 to 2079-06-06 with an accuracy of 1 minute.
    #DATE YYYY-MM-DD 0001-01-01 to 9999-12-31.
    #TIME HH:MM:SS[.NNNNNNN] store a time only with an accuracy of 100 nanoseconds.
    #DATETIMEOFFSET YYYY-MM-DD HH:MM:SS[.NNNNNNN] [+|-] HH:MM (in UTC)
    # the same as DATETIME2 with a timezone offset.
    #TIMESTAMP stores a unique integer that gets updated everytime a row gets created or modified.
    #A timestamp is based on an internal clock. Each table may have only one timestamp variable.
    #
    #SQL_VARIANT stores up to 8,000 bytes of data of varying type,
    # except text and ntext and timestamp.
    #UNIQUEIDENTIFIER a globally unique identifier number or string of characters (GUID).
    #XML stores XML formatted data up to 2 GB.
    #CURSOR stores a cursor reference used for database opperations.
    #TABLE stores a result-set for later processing.
    #
    #return ["CHAR(n)", "VARCHAR(n)", "VARCHAR(max)", "NCHAR(n)", "NVARCHAR(n)", "NVARCHAR(max)",
    # "BINARY(n)", "VARBINARY(n)", "VARBINARY(max)", "BIT", "TINYINT", "SMALLINT", "INT", "BIGINT",
    # "DECIMAL(p, s)", "NUMERIC(p, s)", "SMALLMONEY", "MONEY", "FLOAT(p)", "REAL", "DATETIME",
    # "DATETIME2", "SMALLDATETIME", "DATE", "TIME", "DATETIMEOFFSET", "TIMESTAMP", "SQL_VARIANT",
    # "UNIQUEIDENTIFIER", "XML", "CURSOR", "TABLE"];
    #
    #MS ACCESS:
    #(the docs detailing this are so hard to read, I will ignore all of this and
    #not do data validation on this unless I can get real specifics.)
    #
    #SHORT TEXT, TEXT up to 255 (inclusive) characters.
    #LONG TEXT, MEMO up to 65536 (inclusive) characters is searchable, but not sortable. 
    #BYTE integers from 0 to 255 inclusive.
    #INTEGER whole numbers from -32768 to 32767 inclusive.
    #LONG integers from -2147483648 to 2147483647 inclusive.
    #NUMBER ?
    #LARGE NUMBER ?
    #DATE/TIME for years 100 to 9999 ?
    #DATE/TIME EXTENDED for years 1 to 9999 ?
    #CURRENCY for money values ?
    #AUTONUMBER unique id number that auto increments. ?
    #YES/NO contain only one of two values ?
    #OLE OBJECT objects such as word docs. ?
    #RICH TEXT text that can be formatted using color and font controls ?
    #HYPERLINK text used as a hyperlink ?
    #ATTACHMENT attached documents and files to the database ?
    #CALCULATED, CALCULATED FIELD results of a calculation and must refer to other columns
    # on the same table. ?
    #LOOKUP WIZARD, LOOKUP list of values from the query as SHORTTEXT or NUMBERs. ?
    #?
    #?
    #
    #return ["SHORT TEXT", "TEXT", "LONG TEXT", "MEMO", "INTEGER", "LONG", "?", "?", "?",
    # "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?"];
    #
    #extra included as a space holder for other variants, but there are many variants:
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #?
    #return ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?",
    # "?", "?", "?", "?", "?"];
    #
    #varstr is the SQL VARIANT
    @classmethod
    def getValidSQLDataTypes(cls, varstr):
        #need some way to get the variant...
        #if the variant is something that is not recognized, this will return null or empty.
        #but will treat the data types and values as if they are all valid when they may not be...
        if (varstr == "LITE"): return ["NULL", "REAL", "INTEGER", "TEXT", "BLOB"];
        elif (varstr == "MYSQL"):
            return ["CHAR(size)", "VARCHAR(size)", "BINARY(size)", "VARBINARY(size)", "TINYBLOB",
                    "TINYTEXT", "TEXT(size)", "BLOB(size)", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT",
                    "LONGBLOB", "ENUM(values)", "SET(values)", "BIT(size)", "TINYINT(size)",
                    "BOOL", "BOOLEAN", "SMALLINT(size)", "MEDIUMINT(size)",
                    "INTEGER(size)", "INT(size)", "BIGINT(size)", "FLOAT(size, d)", "FLOAT(p)",
                    "DOUBLE(size, d)", "DOUBLE PRECISION(size, d)", "DECIMAL(size, d)", "DEC(size, d)",
                    "FLOAT", "DOUBLE PRECISION", "DOUBLE", "DATE", "DATETIME(fsp)", "TIMESTAMP(fsp)",
                    "TIME(fsp)", "YEAR", "DATETIME", "TIMESTAMP", "TIME"];
        elif (varstr == "SQLSERVER"):
            return ["CHAR(n)", "VARCHAR(n)", "VARCHAR(max)", "NCHAR(n)", "NVARCHAR(n)", "NVARCHAR(max)",
                    "BINARY(n)", "VARBINARY(n)", "VARBINARY(max)", "BIT", "TINYINT", "SMALLINT", "INT",
                    "BIGINT", "DECIMAL(size, d)", "NUMERIC(size, d)", "SMALLMONEY", "MONEY", "FLOAT(p)",
                    "REAL", "DATETIME", "DATETIME2", "SMALLDATETIME", "DATE", "TIME", "DATETIMEOFFSET",
                    "TIMESTAMP", "SQL_VARIANT", "UNIQUEIDENTIFIER", "XML", "CURSOR", "TABLE"];
        else: return [];

    #p, s -> ?;
    #what if no range can be specified, but we have a name
    #add default values for the parameter (if they have one)
    #what if they do not have any default values?
    #I guess we need a parameter that says if they have a default value or not.
    #paramobj: paramname
    #canspecifyrange: val
    #maxval: max
    #minval: min
    #note: default value may or may not be in the specified range because it might be an exception
    #often the default value is in the range, but not always the case.
    @classmethod
    def genRangeDataDict(cls, name, canspecifyrange, hasadefault, minval, maxval, mdefval):
        myvalidator.varmustbeboolean(hasadefault, varnm="hasadefault");
        myvalidator.varmustbeboolean(canspecifyrange, varnm="canspecifyrange");
        #myvalidator.varmustbeanumber(minval, varnm="minval");#can be a number or a string
        #myvalidator.varmustbeanumber(maxval, varnm="maxval");#can be a number or a string
        myvalidator.varmustnotbeempty(name, varnm="name");
        if (name.isalpha()): pass;
        else: raise ValueError("the paramname must be alphabetic, but it was not!");
        return {"paramname": name, "canspecifyrange": canspecifyrange, "hasadefault": hasadefault,
                "min": minval, "max": maxval, "defaultval": mdefval};
    @classmethod
    def genRangeDataDictNoRange(cls, name, hasadefault, mdefval):
        return myvalidator.genRangeDataDict(name, False, hasadefault, None, None, mdefval);
    @classmethod
    def genRangeDataDictNoRangeNoDefault(cls, name):
        return myvalidator.genRangeDataDictNoRange(name, False, None);
    @classmethod
    def genRangeDataDictNoDefault(cls, name, canspecifyrange, minval, maxval):
        return myvalidator.genRangeDataDict(name, canspecifyrange, False, minval, maxval, None);

    #if type can be signed or unsigned
    #if type is some kind of value
    #the base type name
    #the parameter names if required
    #ranges on parameters if parameters are given or if range can be specified
    #can range on values be specified
    #range on the values if can be specified (just a max and a min)
    @classmethod
    def genTypeInfoDict(cls, names, isval, canbesignedornot, pnmsranges, valsranges):
        myvalidator.varmustbeboolean(isval, varnm="isval");
        myvalidator.varmustbeboolean(canbesignedornot, varnm="canbesignedornot");
        myvalidator.varmustnotbeempty(names, varnm="names");
        for nm in names:
            myvalidator.varmustnotbeempty(nm, varnm="nm");
            if (nm.isalnum()): pass;
            else:
                isvalid = True;
                if ("(max)" in nm):
                    mxi = nm.index("(max)");
                    nmpa = nm[0:mxi];
                    nmpb = (nm[mxi + 5:] if (mxi + 5 < len(nm)) else "");
                    isvalid = (len(nmpb) < 1);
                else: nmpa = "" + nm;

                for n in range(len(nmpa)):
                    if (not isvalid): break;
                    c = nmpa[n];
                    if (c.isalnum()):
                        if (0 < n): pass;
                        else:
                            if (c.isdigit()):
                                isvalid = False;
                                break;
                    else:
                        if (c == " " or c == "_"):
                            if (0 < n): pass;
                            else:
                                isvalid = False;
                                break;
                        else:
                            isvalid = False;
                            break;
                if (not isvalid): raise ValueError("the typename must be alphabetic, but it was not!");
        
        #add some additional defaults for the data type properties that can be inferred
        useunsigneddefault = False;
        isnonnulldefault = False;
        signedhasadefault = False;
        if (canbesignedornot):
            isnonnulldefault = True;
            #if signed and unsigned are present on the ranges then no default for signed
            #otherwise a default is present and can be determined.
            #is a number type so default initally for the number type isnonnull: True
            #but still cannot say one way or the other on the signed until we check the ranges
            #if "signed", "unsigned" are present, that means two ranges
            #no default present for signed
            #print("this is a number type!");
            #print(f"names = {names}");
            #print(f"valsranges = {valsranges}");
            
            sp = False;
            usp = False;
            valsp = False;
            minsp = 0;
            minusp = 0;
            for rngobj in valsranges:
                if (rngobj["paramname"] == "values" or rngobj["paramname"] == "range"):
                    valsp = True;
                if (rngobj["paramname"] == "signed"):
                    sp = True;
                    minsp = rngobj["min"];
                elif (rngobj["paramname"] == "unsigned"):
                    usp = True;
                    minusp = rngobj["min"];
                if (sp and usp): break;
            #print(f"sp = {sp}");
            #print(f"usp = {usp}");
            #print(f"minsp = {minsp}");
            #print(f"minusp = {minusp}");
            #print(f"valsp = {valsp}");

            if (sp and usp):
                #two ranges most likely no default present for signed
                #if the minimum for both of these is at least 0, then use unsigned
                #if the minimum for both of these is less than 0, use signed
                #otherwise no default is present
                if (minsp < 0 and minusp < 0):
                    useunsigneddefault = False;
                    signedhasadefault = True;
                elif (0 <= minsp and 0 <= minusp):
                    useunsigneddefault = True;
                    signedhasadefault = True;
                else:
                    useunsigneddefault = False;
                    signedhasadefault = False;
            else:
                #one range is present, so a default will be assigned.
                #but still do not know what it is yet.
                #look for the param name with values or range.
                if (valsp):
                    for rngobj in valsranges:
                        if (rngobj["paramname"] == "values" or rngobj["paramname"] == "range"):
                            useunsigneddefault = (not(rngobj["min"] < 0));
                            signedhasadefault = True;
                            break;
                else:
                    raise ValueError(f"the range object was built wrong for type with names: {names}!");
        else:
            useunsigneddefault = True;
            isnonnulldefault = False;
            signedhasadefault = True;
        #print(f"useunsigneddefault = {useunsigneddefault}");
        #print(f"isnonnulldefault = {isnonnulldefault}");
        #print(f"signedhasadefault = {signedhasadefault}");
        
        return {"names": names, "isvalue": isval, "canbesignedornot": canbesignedornot,
                "useunsigneddefault": useunsigneddefault, "isnonnulldefault": isnonnulldefault,
                "signedhasadefault": signedhasadefault, "paramnameswithranges": pnmsranges,
                "valuesranges": valsranges};
    @classmethod
    def genValueTypeInfoDict(cls, names): return myvalidator.genTypeInfoDict(names, True, False, [], []);
    @classmethod
    def genNonValueTypeInfoDict(cls, names, canbesignedornot, pnmsranges, valsranges):
        return myvalidator.genTypeInfoDict(names, False, canbesignedornot, pnmsranges, valsranges);
    @classmethod
    def genNonNumNonValTypeInfoDict(cls, names, pnmsranges, valsranges):
        return myvalidator.genNonValueTypeInfoDict(names, False, pnmsranges, valsranges);
    @classmethod
    def genNonNumNonValNoParamsTypeInfoDict(cls, names, valsranges):
        return myvalidator.genNonValueTypeInfoDict(names, False, [], valsranges);

    #note: range or values is used as the default range name
    #note: length is used for the length allowed for either the values or of the values
    #note: for number types like integer:
    #signed or unsigned are names of the ranges indicating that the issigned parameter determines
    #which range is actually used, but not actually affecting this here.
    #note: for number types like real which is only signed we use the default instead
    #
    #varstr is the SQL VARIANT
    @classmethod
    def getSQLDataTypesInfo(cls, varstr):
        #if type can be signed or unsigned
        #if type is some kind of value
        #the parameter names if required
        #ranges on parameters if parameters are given or if range can be specified
        #the base type name
        #can range on values be specified
        #range on the values if can be specified
        tnyintmx = 255;
        smlintmagmx = 32768;
        nrmlintmagmx = 2147483648;
        ltintmag = 9223372036854775808;#plus or minus this for int max - 1 from this
        ltintmxmag = 18446744073709551615;
        ltrlmag = 3.402*(10**38);#plus or mins this for real
        if (varstr == "LITE"):
            mxbts = (2**31) - 1;#max TEXT length and BLOB size in bytes 
            return [ myvalidator.genValueTypeInfoDict(["NULL"]),
                    myvalidator.genNonValueTypeInfoDict(["REAL"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True, -ltrlmag, ltrlmag, 0)]),
                    
                    myvalidator.genNonValueTypeInfoDict(["INTEGER"], True, [], [
                        myvalidator.genRangeDataDict("signed", True, True, -ltintmag, ltintmag - 1, 0),
                        myvalidator.genRangeDataDict("unsigned", True, True, 0, ltintmxmag, 0)]),
                    
                    myvalidator.genNonNumNonValTypeInfoDict(["TEXT"], [], [
                        myvalidator.genRangeDataDict("length", True, True, 0, mxbts, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),
                    
                    myvalidator.genNonNumNonValTypeInfoDict(["BLOB"], [], [
                        myvalidator.genRangeDataDict("size", True, True, 0, mxbts, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")])];
            #return ["NULL", "REAL", "INTEGER", "TEXT", "BLOB"];
        elif (varstr == "MYSQL"):
            smlintmx = 65535;
            decmxmg = 99999999999999999999999999999999999999999999999999999999999999999;
            return [ myvalidator.genNonValueTypeInfoDict(["CHAR"], False, [
                    myvalidator.genRangeDataDict("size", True, True, 0, tnyintmx, 1)], [
                    myvalidator.genRangeDataDictNoRange("range", True, "NULL")]),
                
                myvalidator.genNonValueTypeInfoDict(["VARCHAR"], False, [
                    myvalidator.genRangeDataDict("size", True, True, 0, smlintmx, 1)], [
                    myvalidator.genRangeDataDictNoRange("range", True, "NULL")]),
                
                myvalidator.genNonValueTypeInfoDict(["BINARY"], False, [
                    myvalidator.genRangeDataDict("size", True, True, 0, tnyintmx, 1)], [
                    myvalidator.genRangeDataDictNoRange("range", True, "NULL")]),
                
                myvalidator.genNonValueTypeInfoDict(["VARBINARY"], False, [
                    myvalidator.genRangeDataDict("size", True, True, 0, smlintmx, 1)], [
                    myvalidator.genRangeDataDictNoRange("range", True, "NULL")]),
                
                myvalidator.genNonValueTypeInfoDict(["TINYBLOB"], False, [], [
                    myvalidator.genRangeDataDict("length", True, True, 0, tnyintmx, 0),
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["TINYTEXT"], False, [], [
                    myvalidator.genRangeDataDict("length", True, True, 0, tnyintmx, 0),
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["BLOB"], False, [
                    myvalidator.genRangeDataDict("size", True, True, 0, smlintmx, 0)], [
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["TEXT"], False, [
                    myvalidator.genRangeDataDict("size", True, True, 0, smlintmx, 0)], [
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["MEDIUMBLOB"], False, [], [
                    myvalidator.genRangeDataDict("length", True, True, 0, 16777215, 0),
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["MEDIUMTEXT"], False, [], [
                    myvalidator.genRangeDataDict("length", True, True, 0, 16777215, 0),
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["LONGBLOB"], False, [], [
                    myvalidator.genRangeDataDict("length", True, True, 0, 4294967295, 0),
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["LONGTEXT"], False, [], [
                    myvalidator.genRangeDataDict("length", True, True, 0, 4294967295, 0),
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["ENUM"], False, [
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")], [
                    myvalidator.genRangeDataDict("length", True, True, 0, smlintmx, 0)]),

                myvalidator.genNonValueTypeInfoDict(["SET"], False, [
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")], [
                    myvalidator.genRangeDataDict("length", True, True, 0, 64, 0)]),
                
                myvalidator.genNonValueTypeInfoDict(["BIT"], False, [
                    myvalidator.genRangeDataDictNoDefault("size", True, 1, 64)], [
                    myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["BOOL", "BOOLEAN"], False, [], [
                    myvalidator.genRangeDataDict("values", True, True, 0, 1, 0)]),
                
                myvalidator.genNonValueTypeInfoDict(["TINYINT"], True, [
                    myvalidator.genRangeDataDict("size", True, True, 0, 3, 3)], [
                    myvalidator.genRangeDataDict("signed", True, True, -127, 128, 0),
                    myvalidator.genRangeDataDict("unsigned", True, True, 0, tnyintmx, 0)]),

                myvalidator.genNonValueTypeInfoDict(["SMALLINT"], True, [
                    myvalidator.genRangeDataDict("size", True, True, 0, 5, 5)], [
                    myvalidator.genRangeDataDict("signed", True, True,
                                                 -smlintmagmx, smlintmagmx - 1, 0),
                    myvalidator.genRangeDataDict("unsigned", True, True, 0, smlintmx, 0)]),

                myvalidator.genNonValueTypeInfoDict(["MEDIUMINT"], True, [
                    myvalidator.genRangeDataDict("size", True, True, 0, 8, 8)], [
                    myvalidator.genRangeDataDict("signed", True, True, -8388608, 8388607, 0),
                    myvalidator.genRangeDataDict("unsigned", True, True, 0, 16777215, 0)]),

                myvalidator.genNonValueTypeInfoDict(["INT", "INTEGER"], True, [
                    myvalidator.genRangeDataDict("size", True, True, 0, 10, 10)], [
                    myvalidator.genRangeDataDict("signed", True, True,
                                                 -nrmlintmagmx, nrmlintmagmx - 1, 0),
                    myvalidator.genRangeDataDict("unsigned", True, True, 0, 4294967295, 0)]),

                myvalidator.genNonValueTypeInfoDict(["BIGINT"], True, [
                    myvalidator.genRangeDataDict("size", True, True, 0, 20, 20)], [
                    myvalidator.genRangeDataDict("signed", True, True, -ltintmag, ltintmag - 1, 0),
                    myvalidator.genRangeDataDict("unsigned", True, True, 0, ltintmxmag, 0)]),

                myvalidator.genNonValueTypeInfoDict(["FLOAT"], True, [
                    myvalidator.genRangeDataDict("p", True, True, 0, 53, 53)], [
                    myvalidator.genRangeDataDict("values", True, True, -decmxmg, decmxmg, 0)]),

                myvalidator.genNonValueTypeInfoDict(["DECIMAL", "DEC", "FLOAT", "DOUBLE",
                                                     "DOUBLE PRECISION"], True, [
                    myvalidator.genRangeDataDict("size", True, True, 0, 65, 10),
                    myvalidator.genRangeDataDict("d", True, True, 0, 30, 0)], [
                    myvalidator.genRangeDataDict("values", True, True, -decmxmg, decmxmg, 0)]),
                    
                myvalidator.genNonValueTypeInfoDict(["DATE"], False, [], [
                    myvalidator.genRangeDataDict("values", True, True, "1000-01-01", "9999-12-31",
                                                 "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["DATETIME"], False, [
                    myvalidator.genRangeDataDict("fsp", True, True, 0, 6, 0)], [
                    myvalidator.genRangeDataDict("values", True, True, "1000-01-01 00:00:00.000000",
                                                 "9999-12-31 23:59:59.999999", "NULL")]),
                
                myvalidator.genNonValueTypeInfoDict(["TIMESTAMP"], False, [
                    myvalidator.genRangeDataDict("fsp", True, True, 0, 6, 0)], [
                    myvalidator.genRangeDataDict("values", True, True, "1970-01-01 00:00:01.000000",
                                                 "2038-01-09 03:14:07.999999", "NULL")]),

                myvalidator.genNonValueTypeInfoDict(["TIME"], False, [
                    myvalidator.genRangeDataDict("fsp", True, True, 0, 6, 0)], [
                    myvalidator.genRangeDataDict("values", True, True, "-838:59:59.000000",
                                                 "838:59:59.999999", "NULL")]),
                
                myvalidator.genNonValueTypeInfoDict(["YEAR"], False, [], [
                    myvalidator.genRangeDataDict("values", True, True, 1901, 2155, 0)])];

            #return ["CHAR(size)", "VARCHAR(size)", "BINARY(size)", "VARBINARY(size)", "TINYBLOB",
            #        "TINYTEXT", "TEXT(size)", "BLOB(size)", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT",
            #        "LONGBLOB", "ENUM(values)", "SET(values)", "BIT(size)", "TINYINT(size)",
            #        "BOOL", "BOOLEAN", "SMALLINT(size)", "MEDIUMINT(size)",
            #        "INTEGER(size)", "INT(size)", "BIGINT(size)", "FLOAT(size, d)", "FLOAT(p)",
            #        "DOUBLE(size, d)", "DOUBLE PRECISION(size, d)", "DECIMAL(size, d)", "DEC(size, d)",
            #        "FLOAT", "DOUBLE PRECISION", "DOUBLE", "DATE", "DATETIME(fsp)", "TIMESTAMP(fsp)",
            #        "TIME(fsp)", "YEAR", "DATETIME", "TIMESTAMP", "TIME"];
        elif (varstr == "SQLSERVER"):
            mnypw = 10**(-4);
            fltmxmag = 1.79*(10**308);
            decmxmg = 10**38;
            mxblobsz = 2000000000;
            return [ myvalidator.genNonValueTypeInfoDict(["CHAR"], False, [
                        myvalidator.genRangeDataDict("n", True, True, 1, 8000, 0)], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),
                    
                    myvalidator.genNonValueTypeInfoDict(["VARCHAR"], False, [
                        myvalidator.genRangeDataDict("n", True, True, 1, 8000, 0)], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["VARCHAR(max)"], False, [], [
                        myvalidator.genRangeDataDict("size", True, True, 1, mxblobsz, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["NCHAR"], False, [
                        myvalidator.genRangeDataDict("n", True, True, 1, 4000, 0)], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["NVARCHAR"], False, [
                        myvalidator.genRangeDataDict("n", True, True, 1, 4000, 0)], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["NVARCHAR(max)"], False, [], [
                        myvalidator.genRangeDataDict("size", True, True, 1, mxblobsz, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["BINARY"], False, [
                        myvalidator.genRangeDataDict("n", True, True, 1, 8000, 0)], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["VARBINARY"], False, [
                        myvalidator.genRangeDataDict("n", True, True, 1, 8000, 0)], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["VARBINARY(max)"], False, [], [
                        myvalidator.genRangeDataDict("size", True, True, 1, mxblobsz, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["BIT"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True, 0, 1, "NULL")]),
                    
                    myvalidator.genNonValueTypeInfoDict(["TINYINT"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True, 0, tnyintmx, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["SMALLINT"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True,
                                                     -smlintmagmx, smlintmagmx - 1, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["INT", "INTEGER"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True,
                                                     -nrmlintmagmx, nrmlintmagmx - 1, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["BIGINT"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True,
                                                     -ltintmag, ltintmag - 1, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["DECIMAL", "NUMERIC"], True, [
                        myvalidator.genRangeDataDict("size", True, True, 0, 38, 18),
                        myvalidator.genRangeDataDict("d", True, True, 0, 38, 0)], [
                        myvalidator.genRangeDataDict("values", True, True, -decmxmg, decmxmg - 1, 0)]),
                    
                    myvalidator.genNonValueTypeInfoDict(["SMALLMONEY"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True, (-nrmlintmagmx)*mnypw,
                                                     (nrmlintmagmx - 1)*mnypw, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["MONEY"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True, (-ltintmag)*mnypw,
                                                     (ltintmag - 1)*mnypw, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["FLOAT"], True, [
                        myvalidator.genRangeDataDict("p", True, True, 0, 53, 53)], [
                    myvalidator.genRangeDataDict("values", True, True, -fltmxmag, fltmxmag, 0)]),
                    
                    myvalidator.genNonValueTypeInfoDict(["REAL"], True, [], [
                        myvalidator.genRangeDataDict("values", True, True, -ltrlmag, ltrlmag, 0)]),

                    myvalidator.genNonValueTypeInfoDict(["DATETIME"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True, "1753-01-01 00:00:00.000",
                                                     "9999-12-31 23:59:59.999", "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["DATETIME2"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True,
                                                     "0001-01-01 00:00:00.0000000",
                                                     "9999-12-31 23:59:59.9999999", "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["SMALLDATETIME"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True, "1900-01-01 00:00:00",
                                                     "2079-06-06 23:59:59", "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["DATE"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True,
                                                     "0001-01-01", "9999-12-31", "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["TIME"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True, "00:00:00.0000000",
                                                     "23:59:59.9999999", "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["DATETIMEOFFSET"], False, [], [
                        myvalidator.genRangeDataDict("values", True, True,
                                                     "0001-01-01 00:00:00.0000000 - 23:59",
                                                     "9999-12-31 23:59:59.9999999 + 23:59", "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["TIMESTAMP"], False, [], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["SQL_VARIANT"], False, [], [
                        myvalidator.genRangeDataDict("length", True, True, 0, 8000, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["UNIQUEIDENTIFIER"], False, [], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["XML"], False, [], [
                        myvalidator.genRangeDataDict("length", True, True, 0, mxblobsz, 0),
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["CURSOR"], False, [], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")]),

                    myvalidator.genNonValueTypeInfoDict(["TABLE"], False, [], [
                        myvalidator.genRangeDataDictNoRange("values", True, "NULL")])];

            #return ["CHAR(n)", "VARCHAR(n)", "VARCHAR(max)", "NCHAR(n)", "NVARCHAR(n)",
            #        "NVARCHAR(max)", "BINARY(n)", "VARBINARY(n)", "VARBINARY(max)", "BIT", "TINYINT",
            #        "SMALLINT", "INT", "BIGINT", "DECIMAL(size, d)", "NUMERIC(size, d)", "SMALLMONEY",
            #        "MONEY", "FLOAT(p)", "REAL", "DATETIME", "DATETIME2", "SMALLDATETIME", "DATE",
            #        "TIME", "DATETIMEOFFSET", "TIMESTAMP", "SQL_VARIANT", "UNIQUEIDENTIFIER", "XML",
            #        "CURSOR", "TABLE"];
        else: return [];

    @classmethod
    def getDefaultValueKeyNameForDataTypeObj(cls, tpobj, mycolobj):
        #values works if the type is not signed
        #if the type is signed, you need to choose signed or unsigned instead
        rkys = ["canbesignedornot", "signedhasadefault", "valuesranges"];
        myvalidator.objvarmusthavethesekeysonit(tpobj, rkys, varnm="tpobj");
        myvalidator.varmustnotbenull(mycolobj, varnm="mycolobj");
        mykynm = None;
        if (tpobj["canbesignedornot"]):
            if (tpobj["signedhasadefault"]):
                #may need to use values here, but may still need to use either
                #this means that the ranges agreed on the minimum and if it was less than 0 or not
                #there may still be signed and unsigned here or just values
                mynms = [vrobj["paramname"] for vrobj in tpobj["valuesranges"]];
                if ("signed" in mynms):
                    mykynm = ("signed" if (mycolobj.getIsSigned()) else "unsigned");
                else: mykynm = "values";
            else:
                #now need to pick from signed or unsigned
                #let this come in from the col object
                mykynm = ("signed" if (mycolobj.getIsSigned()) else "unsigned");
        else: mykynm = "values";
        #print(f"mykynm = {mykynm}");
        return mykynm;

    @classmethod
    def getDefaultValueForDataTypeObjWithName(cls, tpobj, nm="values", isparam=False):
        myvalidator.varmustbeboolean(isparam, varnm="isparam");
        myvalidator.varmustnotbenull(tpobj, varnm="tpobj");
        myvalidator.stringMustHaveAtMinNumChars(nm, 1, varnm="nm");
        mlist = tpobj[("paramnameswith" if (isparam) else "values") + "ranges"];
        vrlist = ["values", "range"];
        for mobj in mlist:
            ismatch = ((mobj["paramname"] in vrlist) if (nm in vrlist) else (mobj["paramname"] == nm));
            if (ismatch):
                if (mobj["hasadefault"]): return mobj["defaultval"];
                else: break;
        raise ValueError("data type object with name (" + nm + ") and isparam (" + str(isparam) +
                         ") type not found or has no default value!");

    #this method identifies all of the type names by variant that has
    #total number of digits and the number of digits after the decimal point
    #
    #varnm is the SQL VARIANT
    @classmethod
    def getAllDataTypesWithASetAmountOfDigitsAndAfterDecimalPoint(cls, varnm):
        #but not all floats on MYSQL one does one does not
        if (varnm == "SQLSERVER"): return ["DECIMAL", "NUMERIC"];
        elif (varnm == "MYSQL"): return ["DECIMAL", "DEC", "FLOAT", "DOUBLE", "DOUBLE PRECISION"];
        else: return [];

    #what data types for the variants controls how many digits are allowed after the decimal point?
    #these only have one parameter. unlike the method above.
    #
    #varnm is the SQL VARIANT
    @classmethod
    def getAllDataTypesWithASetAmountOfDigitsAfterTheDecimalPointOnly(cls, varnm):
        return (["FLOAT"] if (varnm == "SQLSERVER") else
                (["DATETIME", "TIMESTAMP", "TIME"] if (varnm == "MYSQL") else []));

    #varnm is the SQL VARIANT
    @classmethod
    def getAllDataTypesWithAListAsTheParameter(cls, varnm):
        return (["ENUM", "SET"] if (varnm == "MYSQL") else []);
    
    #the BINARY(n)s on sql server (n is byte related so maybe not quite)
    #so maybe take nmax multiply by 8 for bit length IE actual length stored???
    #the BLOB(size)s on my sql are similar.
    #the BINARY(size)s on my sql are similar, but not sure on the max???.
    #
    #varstr is the SQL VARIANT
    @classmethod
    def getTypesThatHaveAByteRelatedLength(cls, varstr, tp="ALL"):
        if (varstr == "MYSQL"):
            if (tp == "PSONLY"): return ["BINARY", "VARBINARY", "BLOB"];
            elif (tp == "NOPSONLY"): return ["TINYBLOB", "MEDIUMBLOB", "LONGBLOB"];
            else: return ["BINARY", "VARBINARY", "BLOB", "TINYBLOB", "MEDIUMBLOB", "LONGBLOB"];
        elif (varstr == "SQLSERVER"):
            if (tp == "PSONLY"): return ["BINARY", "VARBINARY"];
            elif (tp == "NOPSONLY"): return ["VARBINARY(max)"];
            else: return ["BINARY", "VARBINARY", "VARBINARY(max)"];
        elif (varstr == "LITE"):
            nopsalllist = ["BLOB"];
            if (tp == "NOPSONLY"): return nopsalllist;
            elif (tp == "PSONLY"): return [];
            else: return nopsalllist;
        else: return [];
    @classmethod
    def getTypesThatHaveAByteRelatedLengthAsTheParam(cls, varstr):
        return myvalidator.getTypesThatHaveAByteRelatedLength(varstr, "PSONLY");
    @classmethod
    def getTypesThatHaveAByteRelatedLengthNoParams(cls, varstr):
        return myvalidator.getTypesThatHaveAByteRelatedLength(varstr, "NOPSONLY");
    @classmethod
    def getAllTypesThatHaveAByteRelatedLength(cls, varstr):
        return myvalidator.getTypesThatHaveAByteRelatedLength(varstr, "ALL");

    #we need to know if something has a parameter that dictates the length and maybe which it is
    #we need to know when size as a parameter is length, and when it is not relevant
    #
    #for sql server anything with CHAR(n) n is the length (EXCLUDING THOSE WITH max OF COURSE)
    #same for char and varchar and text and bit on mysql size is length.
    #
    #varstr is the SQL VARIANT
    @classmethod
    def getTypesThatHaveLengthAsTheParam(cls, varstr):
        return (["CHAR", "VARCHAR", "NCHAR", "NVARCHAR"] if (varstr == "SQLSERVER") else
                (["CHAR", "VARCHAR", "TEXT", "BIT"] if (varstr == "MYSQL") else []));
    
    #all INTs on mysql have the size parameter being the display width.
    #this does not effect how the value is stored at all.
    #"TINYINT", "SMALLINT", "MEDIUMINT", "INTEGER", "INT", "BIGINT"
    #
    #varstr is the SQL VARIANT
    @classmethod
    def getTypesThatHaveADisplayWidthParam(cls, varstr):
        return (["TINYINT", "SMALLINT", "MEDIUMINT", "INTEGER", "INT", "BIGINT"]
                if (varstr == "MYSQL") else []);


    #begin date time methods section here...

    @classmethod
    def getMonthNames(cls):
        return ["January", "February", "March", "April", "May", "June", "July", "August",
                "September", "October", "November", "December"];
    @classmethod
    def getAllThreeLetterAbbreviationsForMonthNames(cls):
        return [mnth[0:3] for mnth in myvalidator.getMonthNames()];
    @classmethod
    def getAllFourLetterAbbreviationsForMonthNames(cls):
        return [(mnth[0:4] if (3 < len(mnth)) else mnth) for mnth in myvalidator.getMonthNames()];
    @classmethod
    def getAllThreeOrFourLetterAbbreviationsForMonthNames(cls, usefrltrs):
        myvalidator.varmustbeboolean(usefrltrs, varnm="usefrltrs");
        if (usefrltrs): return myvalidator.getAllFourLetterAbbreviationsForMonthNames();
        else: return myvalidator.getAllThreeLetterAbbreviationsForMonthNames();

    @classmethod
    def getThreeOrFourLetterAbbreviationForMonthName(cls, mnthnm, usefrltrs):
        myvalidator.varmustbeboolean(usefrltrs, varnm="usefrltrs");
        myvalidator.varmustbethetypeonly(mnthnm, str, varnm="mnthnm");
        lwrmnthnm = mnthnm.lower();
        finmnthnm = lwrmnthnm[0].upper() + lwrmnthnm[1:];
        if (finmnthnm in myvalidator.getMonthNames()):
            if (len(finmnthnm) == 3): return finmnthnm;
            else: return finmnthnm[0: (4 if (usefrltrs) else 3)];
        else: raise ValueError("illegal month name used (" + mnthnm + ")");
    @classmethod
    def getThreeLetterAbbreviationForMonthName(cls, mnthnm):
        return myvalidator.getThreeOrFourLetterAbbreviationForMonthName(mnthnm, False);
    @classmethod
    def getFourLetterAbbreviationForMonthName(cls, mnthnm):
        return myvalidator.getThreeOrFourLetterAbbreviationForMonthName(mnthnm, True);

    @classmethod
    def getFullMonthNameFromAbreviation(cls, abbr):
        lwrmnthnm = abbr.lower();
        finmnthnm = lwrmnthnm[0].upper() + lwrmnthnm[1:];
        mnthnms = myvalidator.getMonthNames();
        for mtnm in mnthnms:
            if finmnthnm in mtnm: return mtnm;
        raise ValueError("illegal abbreviated month name used (" + abbr + ")");

    @classmethod
    def getMonthNumFromName(cls, mnthnm):
        myvalidator.varmustbethetypeonly(mnthnm, str, varnm="mnthnm");
        lwrmnthnm = mnthnm.lower();
        finmnthnm = lwrmnthnm[0].upper() + lwrmnthnm[1:];
        mnthnms = myvalidator.getMonthNames();
        for n in range(len(mnthnms)):
            if (mnthnms[n] == finmnthnm): return n + 1;
        raise ValueError("illegal month name used (" + mnthnm + ")");

    @classmethod
    def getMonthNameFromNum(cls, mnthnum):
        myvalidator.valueMustBeInRange(mnthnum, 1, 12, True, True, varnm="mnthnum");
        mnthnms = myvalidator.getMonthNames();
        return mnthnms[mnthnum - 1];

    @classmethod
    def getNumDaysInMonth(cls, mnthnum, islpyr):
        myvalidator.varmustbeboolean(islpyr, varnm="islpyr");
        myvalidator.valueMustBeInRange(mnthnum, 1, 12, True, True, varnm="mnthnum");
        #(30 days has (9)September, (4)April, (6)June, and (11)November, all the rest have 31 except
        #(2)February which has 28 or 29 if leap year)
        if (mnthnum in [4, 6, 9, 11]): return 30;
        elif (mnthnum == 2): return (29 if islpyr else 28);
        else: return 31;

    @classmethod
    def addLeadingZeros(cls, val, numdgts):
        myvalidator.varmustbeanumber(val, varnm="val");
        myvalidator.valueMustBeInRange(numdgts, 1, 0, True, False, varnm="numdgts");
        if (val < 0): return "-" + myvalidator.addLeadingZeros(-val, numdgts - 1);
        valstr = str(val);
        valstrlen = len(valstr);
        if (valstrlen < numdgts):
            mystr = "";
            for n in range(numdgts - valstrlen): mystr += "0";
            return mystr + valstr;
        elif (valstrlen == numdgts): return valstr;
        else:
            #raise ValueError("the length of the numstr (" + str(valstrlen) + ") must be less than " +
            #                 "or equal to the number of digits (" + str(numdgts) +
            #                 "), but it was not!");
            return valstr;

    #https://en.wikipedia.org/wiki/Leap_year
    @classmethod
    def isLeapYear(cls, yrnum):
        myvalidator.varmustbethetypeonly(yrnum, int, varnm="yrnum");
        myvalidator.valueMustBeInRange(yrnum, 1, 0, True, False, varnm="yrnum");
        #every 4 years except (if divisible by 400 it is otherwise not on the 100s)
        return (((yrnum % 400 == 0) if (yrnum % 100 == 0) else True) if (yrnum % 4 == 0) else False);

    @classmethod
    def isValidDate(cls, mnthnum, daynum, yrnum):
        if (myvalidator.isValueInRangeWithMaxAndMin(mnthnum, 1, 12)):
            dysinmnth = myvalidator.getNumDaysInMonth(mnthnum, myvalidator.isLeapYear(yrnum));
            if (myvalidator.isValueInRangeWithMaxAndMin(daynum, 1, dysinmnth)): return True;
        return False;
    @classmethod
    def isValidDateFromObj(cls, mdyrobj):
        myvalidator.varmustnotbenull(mdyrobj, varnm="mdyrobj");
        return myvalidator.isValidDate(mdyrobj["monthnum"], mdyrobj["daynum"], mdyrobj["yearnum"]);
    @classmethod
    def isValidDateFromString(cls, datestr):
        mdyrobj = None;
        try:
            mdyrobj = myvalidator.getMonthDayYearFromDateString(datestr);
        except Exception as ex:
            #print(dir(ex));
            #print(ex);
            #traceback.print_exc();
            #print("the value was not valid!");
            return False;
        return myvalidator.isValidDateFromObj(mdyrobj);
    
    @classmethod
    def genDateString(cls, mnthnum, daynum, yrnum, usemthdyyr, usedshs):
        dysinmnth = myvalidator.getNumDaysInMonth(mnthnum, myvalidator.isLeapYear(yrnum));
        myvalidator.valueMustBeInRange(daynum, 1, dysinmnth, True, True, varnm="daynum");
        myvalidator.valueMustBeInRange(yrnum, 1, 9999, True, True, varnm="yrnum");#max may be wrong here
        #well strictly speaking sql allows 4 digit years, but we humans want to live forever
        #so theoretically there is no max..., but one is being imposed by the current restrictions.
        mdshorslsh = ("-" if usedshs else "/");
        myretstr = None;
        if (usemthdyyr):
            #MM-DD-YYYY
            myretstr = myvalidator.addLeadingZeros(mnthnum, 2) + mdshorslsh;
            myretstr += myvalidator.addLeadingZeros(daynum, 2) + mdshorslsh;
            myretstr += myvalidator.addLeadingZeros(yrnum, 4);
        else:
            #YYYY-MM-DD
            #0123456789
            myretstr = myvalidator.addLeadingZeros(yrnum, 4) + mdshorslsh;
            myretstr += myvalidator.addLeadingZeros(mnthnum, 2) + mdshorslsh;
            myretstr += myvalidator.addLeadingZeros(daynum, 2);
        return myretstr;
    @classmethod
    def genDateStringFromObj(cls, mdyrobj, usedshs):
        myvalidator.varmustnotbenull(mdyrobj, varnm="mdyrobj");
        return myvalidator.genDateString(mdyrobj["monthnum"], mdyrobj["daynum"], mdyrobj["yearnum"],
                                         (list(mdyrobj.keys())[0] == "monthnum"), usedshs);
    @classmethod
    def genDateStringUseMonthDayYear(cls, mnthnum, daynum, yrnum, usedshs):
        return myvalidator.genDateString(mnthnum, daynum, yrnum, True, usedshs);
    @classmethod
    def genDateStringUseYearMonthDay(cls, mnthnum, daynum, yrnum, usedshs):
        return myvalidator.genDateString(mnthnum, daynum, yrnum, False, usedshs);
    @classmethod
    def genDateStringUseSlashes(cls, mnthnum, daynum, yrnum, usemthdyyr):
        return myvalidator.genDateString(mnthnum, daynum, yrnum, usemthdyyr, False);
    @classmethod
    def genDateStringUseDashes(cls, mnthnum, daynum, yrnum, usemthdyyr):
        return myvalidator.genDateString(mnthnum, daynum, yrnum, usemthdyyr, True);
    
    @classmethod
    def getDelimeterIndexesForDateStrings(cls, usemthdyyr):
        #MM-DD-YYYY
        #YYYY-MM-DD
        #0123456789
        myvalidator.varmustbeboolean(usemthdyyr, varnm="usemthdyyr");
        return ([2, 5] if (usemthdyyr) else [4, 7]);

    @classmethod
    def getMonthDayYearFromDateString(cls, datestr):
        if (myvalidator.isvaremptyornull(datestr)): return None;
        if (len(datestr) == 10): pass;
        else: raise ValueError("datestring must have exactly 10 characters on it, but it did not!");
        dimdyr = myvalidator.getDelimeterIndexesForDateStrings(True);
        diyrmd = myvalidator.getDelimeterIndexesForDateStrings(False);
        if ((datestr[dimdyr[0]] == datestr[dimdyr[1]]) and (datestr[dimdyr[0]] in ["-", "/"])):
            #MM-DD-YYYY
            marr = myvalidator.mysplitWithLen(datestr, dimdyr, 1, 0);
            if (len(marr[2]) == 4): pass;
            else: raise ValueError("invalid date string not in the correct format!");
            return {"monthnum": int(marr[0]), "daynum": int(marr[1]), "yearnum": int(marr[2])};
        else:
            if ((datestr[diyrmd[0]] == datestr[diyrmd[1]]) and (datestr[diyrmd[0]] in ["-", "/"])):
                #YYYY-MM-DD
                marr = myvalidator.mysplitWithLen(datestr, diyrmd, 1, 0);
                if (len(marr[2]) == 2): pass;
                else: raise ValueError("invalid date string not in the correct format!");
                return {"yearnum": int(marr[0]), "monthnum": int(marr[1]), "daynum": int(marr[2])};
            else: raise ValueError("invalid date string not in the correct format!");

    @classmethod
    def genTimeString(cls, hrnum, minnum, secs, inchrnum=True, incminnum=True, incsecs=True):
        myvalidator.varmustbeboolean(inchrnum, varnm="inchrnum");
        myvalidator.varmustbeboolean(incminnum, varnm="incminnum");
        myvalidator.varmustbeboolean(incsecs, varnm="incsecs");
        myvalidator.valueMustBeInRange(hrnum, -838, 838, True, True, varnm="hrnum");
        #no idea why on the hour range
        myvalidator.valueMustBeInRange(minnum, 0, 59.9999999, True, True, varnm="minnum");
        myvalidator.valueMustBeInRange(secs, 0, 59.9999999, True, True, varnm="secs");
        if (incsecs):
            if (inchrnum):
                if (incminnum): pass;
                else: raise ValueError("if including seconds and hours, minutes must be included!");
        mystr = "";
        if (inchrnum): mystr += myvalidator.addLeadingZeros(hrnum, 2);
        if (incminnum): mystr += (":" if inchrnum else "") + myvalidator.addLeadingZeros(minnum, 2);
        if (incsecs): mystr += (":" if incminnum else "") + str(secs);
        return mystr;
    @classmethod
    def genTimeStringFromObj(cls, mhrsobj):
        if (mhrsobj == None):
            return myvalidator.genTimeString(0, 0, 0, inchrnum=False, incminnum=False, incsecs=False);
        mkys = mhrsobj.keys();
        #if not on the keys list then not included in the resulting string that gets generated
        inchrnum = (mhrsobj["hoursnuminstr"] if "hoursnum" in mkys else False);
        #inchrnum = ("hoursnum" in mkys);
        incminnum = (mhrsobj["minutesnuminstr"] if "minutesnum" in mkys else False);
        #incminnum = ("minutesnum" in mkys);
        incsecs = (mhrsobj["secondsnuminstr"] if "secondsnum" in mkys else False);
        #incsecs = ("secondsnum" in mkys);
        hrnum = (mhrsobj["hoursnum"] if inchrnum else 0);
        minnum = (mhrsobj["minutesnum"] if incminnum else 0);
        secs = (float(str(mhrsobj["secondsnum"]) + "." + str(mhrsobj["fractionalsecondsnum"]))
                if incsecs else 0);
        return myvalidator.genTimeString(hrnum, minnum, secs,
                                         inchrnum=inchrnum, incminnum=incminnum, incsecs=incsecs);

    #inchrs tells us if we include hours or not when we just have one colon on the string
    #this tells us to use hours:minutes for the format if true,
    #else it will use minutes:seconds.fractionalsecondsnum
    #this returns an object with hoursnum, minutesnum, secondsnum, and fractionalsecondsnum keys
    #the values returned in the object are all integers
    @classmethod
    def getTimeObject(cls, mstr, inchrs):
        #HHH:MM:SS.SSSSSSS OR MM:SS.SSSSSSS OR HHH:MM
        #with just a colon we do not know the format hours and minutes or minutes and seconds?
        myvalidator.varmustbeboolean(inchrs, varnm="inchrs");
        
        #print(f"mstr = {mstr}");
        
        mkys = ["hoursnum", "minutesnum", "secondsnum", "fractionalsecondsnum"];
        if (myvalidator.isvaremptyornull(mstr)):
            mdict = {};
            for n in range(len(mkys)):
                mdict[mkys[n]] = 0;
                mdict[mkys[n] + "instr"] = False;
            return mdict;

        numclns = 0;
        clis = [];
        pfnd = False;
        pdi = -1;
        for i in range(len(mstr)):
            c = mstr[i];
            errstr = "";
            if (c == ":"):
                if (0 < i):
                    numclns += 1;
                    clis.append(i);
                    if (2 < numclns): errstr = "invalid number of colons found in the string! ";
                else: errstr = "colon cannot start the string! ";
            elif (c == "."):
                if (0 < i):
                    if (pfnd): errstr = "only one period can be found on the string! ";
                    else:
                        pdi = i;
                        pfnd = True;
                else: errstr = "period cannot start the string! ";
            elif (c == "-"):
                if (i == 0): pass;
                else: errstr = "only one minus can start the time string! ";
            elif (c.isdigit()): pass;
            else: errstr = "invalid character found on the string! ";
            if (0 < len(errstr)):
                raise ValueError(errstr + "invalid string found and used here for the time string!");
        #print("mstr is valid!");
        #print(f"clis = {clis}");
        #print(f"pfnd = {pfnd}");

        if (len(clis) in [1, 2]): pass;
        else: raise ValueError("invalid number of colons found on the time string!");

        usehms = (len(clis) == 2);
        #print(f"usehms = {usehms}");
        #print(f"inchrs = {inchrs}");

        mydelimis = [c for c in clis];
        if (pfnd): mydelimis.append(pdi);
        finkys = ([ky for ky in mkys] if (usehms) else 
                  ([mkys[0], mkys[1]] if (inchrs) else [mkys[1], mkys[2], mkys[3]]));
        marr = myvalidator.mysplitWithLen(mstr, mydelimis, 1, 0);
        if (pfnd): pass;
        else:
            if (usehms or not(inchrs)): marr.append(0);
            
        #print(f"mydelimis = {mydelimis}");
        #print(f"mkys = {mkys}");
        #print(f"finkys = {finkys}");
        #print(f"marr = {marr}");

        if (len(finkys) == len(marr)): pass;
        else: raise ValueError("the number of final keys and the number of values must match!");
        
        mdict = {};
        for n in range(len(finkys)): mdict[finkys[n]] = int(marr[n]);
        #print(f"OLD mdict = {mdict}");

        for ky in mkys:
            if (ky in finkys): mdict[ky + "instr"] = True;
            else:
                mdict[ky] = 0;
                mdict[ky + "instr"] = False;
        #print(f"FINAL mdict = {mdict}");

        return mdict;

    #none is older than not none.
    #returns 0 if equal, if a is less older than b then -1, else if b is less than a 1
    @classmethod
    def compareTwoDateTimeObjs(cls, dateaobj, timeaobj, datebobj, timebobj):
        #what if the date object is empty?
        #what if the time object is empty?
        #what if one is empty but not the other?
        #then of course what if both are not empty?
        #time keys: ["hoursnum", "minutesnum", "secondsnum", "fractionalsecondsnum"];
        #date keys: ["monthnum", "daynum", "yearnum"];#the order determines how to generate the string

        dtkyscompordr = ["yearnum", "monthnum", "daynum"];
        alessthanb = -1;
        agtrthanb = 1;
        if (dateaobj == None or datebobj == None):
            if (dateaobj == datebobj): pass;#need to check times otherwise return 0
            else: return (alessthanb if (dateaobj == None) else agtrthanb);#none is before not null
        else:
            for dky in dtkyscompordr:
                if (dateaobj[dky] == datebobj[dky]): pass;
                else: return (alessthanb if (dateaobj[dky] < datebobj[dky]) else agtrthanb);
        
        tkyscompordr = ["hoursnum", "minutesnum", "secondsnum", "fractionalsecondsnum"];
        if (timeaobj == None or timebobj == None):
            if (timeaobj == timebobj): pass;#need to check times otherwise return 0
            else: return (alessthanb if (timeaobj == None) else agtrthanb);#none is before not null
        else:
            for tky in tkyscompordr:
                if (timeaobj[tky] == timebobj[tky]): pass;
                else: return (alessthanb if (timeaobj[tky] < timebobj[tky]) else agtrthanb);
        return 0;
    @classmethod
    def compareTwoDateObjsOnly(cls, dateaobj, datebobj):
        return myvalidator.compareTwoDateTimeObjs(dateaobj, None, datebobj, None);
    @classmethod
    def compareTwoTimeObjsOnly(cls, timeaobj, timebobj):
        return myvalidator.compareTwoDateTimeObjs(None, timeaobj, None, timebobj);

    @classmethod
    def getDateTimeStringType(cls, mstr):
        myvalidator.varmustbethetypeandornull(mstr, str, True, varnm="mstr");
        if (myvalidator.isvaremptyornull(mstr)): return "DATE-TIME";
        myvalidator.stringMustHaveAtMaxNumChars(mstr, 32, varnm="mstr");
        #need to tell if we have a:
        #date-time string, just a date string, or just a time string
        #if the string is longer than 10 characters and has a space at index 10, then date-time
        #if the string is longer than 10 characters and does not have a space at index 10,
        # then time only
        #else: if the character length is less than 10: time only
        #else if the character length is exactly 10 it could be either date only or time only.
        #now check to see if the string is a date string...
        #check the delimeter indexes for either format if it matches, then this is a date string
        #if not, then time only.
        #YYYY-MM-DD HHH:MM:SS.NNNNNNNNNNN
        #MM-DD-YYYY HHH:MM:SS.NNNNNNNNNNN
        #012345678901234567890123456789012
        #0         1         2         3
        if (10 < len(mstr)): return ("DATE-TIME" if (mstr[10] == ' ') else "TIME-ONLY");
        elif (len(mstr) < 10): return "TIME-ONLY";
        else:#len(mstr) == 10
            mdydelimis = myvalidator.getDelimeterIndexesForDateStrings(True);
            ymddelimis = myvalidator.getDelimeterIndexesForDateStrings(False);
            if ((mstr[mdydelimis[0]] == mstr[mdydelimis[1]] and mstr[mdydelimis[0]] in ["-", "/"]) or
                (mstr[ymddelimis[0]] == mstr[ymddelimis[1]] and mstr[ymddelimis[0]] in ["-", "/"])):
                    return "DATE-ONLY";
            else: return "TIME-ONLY";

    @classmethod
    def dateTimeStringIncludesHours(cls, mstr, usehrs):
        myvalidator.varmustbethetypeandornull(mstr, str, True, varnm="mstr");
        if (myvalidator.isvaremptyornull(mstr)): return False;
        tpstra = myvalidator.getDateTimeStringType(mstr);
        myvalidator.varmustbeboolean(usehrs, varnm="usehrs");
        inchrsa = False;
        if (tpstra == "DATE-ONLY"): inchrsa = False;
        else:
            clis = [n for n in range(len(mstr)) if mstr[n:].startswith(":")];
            if (len(clis) == 2): inchrsa = True;
            elif (len(clis) < 1 or 2 < len(clis)): inchrsa = False;
            else:
                pis = [n for n in range(len(mstr)) if mstr[n:].startswith(".")];
                if (len(pis) == 1): inchrsa = False;
                elif (1 < len(pis)): inchrsa = False;
                else: inchrsa = usehrs;
        return inchrsa;

    @classmethod
    def getDateAndTimeObjectInfoFromString(cls, mstr, usehrs):
        myvalidator.varmustbeboolean(usehrs, varnm="usehrs");
        if (myvalidator.isvaremptyornull(mstr)):
            return {"datestr": "", "timestr": "", "dateobj": None,
                    "timeobj": myvalidator.genTimeStringFromObj(None),
                    "inchours": False, "userhours": usehrs};
        
        tpstra = myvalidator.getDateTimeStringType(mstr);
        #print(f"tpstr = {tpstr}");#DATE-TIME, TIME-ONLY, DATE-ONLY

        datestra = None;
        timestra = None;
        if (tpstra == "DATE-TIME"):
            datestra = mstr[0:10];
            timestra = mstr[11:];
        elif (tpstra == "DATE-ONLY"):
            datestra = "" + mstr;
            timestra = "";
        else:
            timestra = "" + mstr;#TIME-ONLY
            datestra = "";
        inchrsa = myvalidator.dateTimeStringIncludesHours(mstr, usehrs);
        dateaobj = myvalidator.getMonthDayYearFromDateString(datestra);
        timeaobj = myvalidator.getTimeObject(timestra, inchrsa);

        return {"datestr": datestra, "timestr": timestra, "dateobj": dateaobj, "timeobj": timeaobj,
                "inchours": inchrsa, "userhours": usehrs};

    #if the string is invalid, it just returns it unchanged
    #otherwise it removes the space at 1 and ignores the plus entirely
    @classmethod
    def convertTimeOffsetStringToTimeString(cls, mstr):
        if (myvalidator.isvaremptyornull(mstr)): return mstr;
        if (mstr[0] == '-' or mstr[0] == '+'):
            if (mstr[1] == ' ' and mstr[2].isdigit()):
                resstr = "";
                if (mstr[0] == '-'): resstr += "-";
                resstr += "" + mstr[2:];
                return resstr;
            else: return mstr;#invalid string
        else: return mstr;#invalid starting character

    #FORMATS SUPPORTED:
    #YYYY-MM-DD HHH:MM:SS.NNNNNNNNNNN
    #MM-DD-YYYY HHH:MM:SS.NNNNNNNNNNN
    #YYYY-MM-DD
    #MM-DD-YYYY
    #HHH:MM:SS.NNNNNNNNNNN
    #HHH:MM
    #MM:SS.NNNNNNNNNNN
    #SS.NNNNNNNNNNN
    #none is older than not none.
    #returns 0 if equal, if a is less than b then -1, else if b is less than a 1
    @classmethod
    def compareTwoDateTimeStrs(cls, mstra, mstrb, usehrsa, usehrsb):
        #get the date time objects from the strings
        #print(f"mstra = {mstra}");
        #print(f"mstrb = {mstrb}");
        #print(f"usehrsa = {usehrsa}");
        #print(f"usehrsb = {usehrsb}");
        
        myvalidator.varmustbeboolean(usehrsa, varnm="usehrsa");
        myvalidator.varmustbeboolean(usehrsb, varnm="usehrsb");
        if (myvalidator.isvaremptyornull(mstra)):
            return (0 if (myvalidator.isvaremptyornull(mstrb)) else -1);
        else:
            if (myvalidator.isvaremptyornull(mstrb)): return 1;
            else:
                if (mstra == mstrb): return 0;
    
        #get the types of the two strings here now:
        dtobja = myvalidator.getDateAndTimeObjectInfoFromString(mstra, usehrsa);
        dtobjb = myvalidator.getDateAndTimeObjectInfoFromString(mstrb, usehrsb);
        #print(f"dtobja = {dtobja}");
        #print(f"dtobjb = {dtobjb}");

        return myvalidator.compareTwoDateTimeObjs(dtobja["dateobj"], dtobja["timeobj"],
                                                  dtobjb["dateobj"], dtobjb["timeobj"]);

    #end of date time methods section


    @classmethod
    def printSQLDataTypesInfoObj(cls, mlistobjs):
        if (myvalidator.isvaremptyornull(mlistobjs)): print("list is empty or null!");
        else:
            for mobj in mlistobjs: print(f"{mobj}\n");

    @classmethod
    def getParamNamesFromInfoListObj(cls, mobj):
        #if no param names return an empty string else
        #get a list of names and then join them
        myvalidator.objvarmusthavethesekeysonit(mobj, ["paramnameswithranges"], varnm="mobj");
        if (myvalidator.isvaremptyornull(mobj["paramnameswithranges"])): return "";
        else:
            #note the validator method returns True or errors out.
            pnames = [pobj["paramname"] for pobj in mobj["paramnameswithranges"]
                      if (myvalidator.objvarmusthavethesekeysonit(pobj, ["paramname"], varnm="pobj"))];
            return "(" + (", ".join(pnames)) + ")";

    #ptpstr is PSONLY means parameters only
    #ptpstr is NOPSONLY means no parameters only
    #ptpstr is anything else ALL
    @classmethod
    def getUseParamsOrNotOrAll(cls, mpobjlist, ptpstr="ALL"):
        #need to know if getting everything
        #those with parameters only
        #those without parameters only
        if (ptpstr == None): return True;
        else:
            if (ptpstr.isupper()): pass;
            else: return myvalidator.getUseParamsOrNotOrAll(mpobjlist, ptpstr.upper());
        if (ptpstr == "PSONLY"): return not(myvalidator.isvaremptyornull(mpobjlist));
        elif (ptpstr == "NOPSONLY"): return (myvalidator.isvaremptyornull(mpobjlist));
        else: return True;#use all

    @classmethod
    def getValidSQLDataTypesFromInfoList(cls, mlist, ptype="ALL"):
        if (mlist == None): return None;
        else:
            return [nm + myvalidator.getParamNamesFromInfoListObj(mobj)
                    for mobj in mlist for nm in mobj["names"]
                    if (myvalidator.getUseParamsOrNotOrAll(mobj["paramnameswithranges"], ptype))];
    @classmethod
    def getValidSQLDataTypesWithParametersOnlyFromInfoList(cls, mlist):
        return myvalidator.getValidSQLDataTypesFromInfoList(mlist, ptype="PSONLY");
    @classmethod
    def getValidSQLDataTypesWithNoParametersOnlyFromInfoList(cls, mlist):
        return myvalidator.getValidSQLDataTypesFromInfoList(mlist, ptype="NOPSONLY");
    @classmethod
    def getAllValidSQLDataTypesFromInfoList(cls, mlist):
        return myvalidator.getValidSQLDataTypesFromInfoList(mlist, ptype="ALL");

    #this is meant more for the test file and not meant for production
    #this helps me know what data types have been classified and what are remaining
    #what is classified and the number of parameters for each goes in
    #a list of all for the variant also goes in
    #then using this we can get what we still need to classify
    @classmethod
    def getRemainingParameters(cls, alllist, objlistsfvar, numrpslist):
        #print(f"alllist = {alllist}");
        #print(f"objlistsfvar = {objlistsfvar}");
        #print(f"numrpslist = {numrpslist}");
        #the last two lists must be the same
        #if all is empty or null, then they all must be empty or null
        #with the exception of the last one, that is constant
        if (myvalidator.isvaremptyornull(alllist)):
            if (len(objlistsfvar) == len(numrpslist)):
                for mlist in objlistsfvar:
                    if (len(mlist) < 1): pass;
                    else: raise ValueError("the lists of all of the objects must be empty!");
            else: raise ValueError("the objlistsfvar and numrpslist must be the same length!");
            return [];
        if (len(objlistsfvar) == len(numrpslist)): pass;
        else: raise ValueError("the objlistsfvar and numrpslist must be the same length!");
        myexlist = [];
        for n in range(len(objlistsfvar)):
            clistpnms = objlistsfvar[n];
            numpsoneach = numrpslist[n];
            #print(f"clistpnms = {clistpnms}");
            #print(f"numpsoneach = {numpsoneach}");
            
            for mynm in clistpnms:
                #print(f"mynm = {mynm}");
                #print();

                for itemnm in alllist:
                    absnm = itemnm[0:itemnm.index("(")];
                    #print(f"itemnm = {itemnm}");
                    #print(f"absnm = {absnm}");

                    if (mynm == absnm):
                        #print("found a possible match!");
        
                        #see if the number of parameters match
                        #if the number of parameters match then this is our match else not
                        #if it is a match add this on our exclusion list and exit this loop
                        valsps = myvalidator.getParamsFromValType(itemnm);
                        #print(f"valsps = {valsps}");

                        if (len(valsps) == numpsoneach):
                            #print("this is a match!");
                            myexlist.append(itemnm);
                        #else: print("this is not a match!");
        #print(f"alllist = {alllist}");
        #print(f"myexlist = {myexlist}");
        return [itemnm for itemnm in alllist if itemnm not in myexlist];

    @classmethod
    def getDataTypesObjsWithNameFromList(cls, mlist, tpnm):
        if (mlist == None): return None;
        else: return [mobj for mobj in mlist for nm in mobj["names"] if (nm == tpnm)];
    
    @classmethod
    def errorCheckAndReturnTheLevels(cls, lvls, val):
        if (myvalidator.isvaremptyornull(val)):
            return {"finlvs": [], "origlvs": [], "val": val, "errmsg": ""};
        
        errmsg = "";
        if (len(val) == len(lvls)):
            if (lvls[len(lvls) - 1] == 1): pass;
            else:
                errmsg = "invalid last level!";
                #print(errmsg);
                return {"finlvs": [], "origlvs": lvls, "val": val, "errmsg": errmsg};
        else:
            errmsg = "invalid number of levels found!";
            #print(errmsg);
            return {"finlvs": [], "origlvs": lvls, "val": val, "errmsg": errmsg};

        plv = 1;
        for lv in lvls:
            if (lv < 1 or len(val) < lv):
                errmsg = "invalid level found!";
                #print(errmsg);
                return {"finlvs": [], "origlvs": lvls, "val": val, "errmsg": errmsg};
            else:
                if (lv == plv or lv == plv + 1 or lv + 1 == plv): pass;
                else:
                    errmsg = "level diff was not valid!";
                    #print(errmsg);
                    return {"finlvs": [], "origlvs": lvls, "val": val, "errmsg": errmsg};
            plv = lv;
        return {"finlvs": lvls, "origlvs": lvls, "val": val, "errmsg": errmsg};

    @classmethod
    def getLevelsForValStr(cls, val):
        if (myvalidator.isvaremptyornull(val)):
            return {"finlvs": [], "origlvs": [], "val": val, "errmsg": ""};
        #params are everything after the first ( and the last )
        #everything else is ignored.
        #if value is not valid, then return empty or null
        #params can be inside ' or ", but ignore it if it is escaped
        #commas inside ' or " can be ignored, but others outside of that cannot be ignored.
        #stuff inside this will not go any lower than 3 I think
        #levels will switch to 2 inside of the parenthesis levels 1 outside of them
        #if levels are not valid, val is not valid
        #
        #"ENUM('something, other', 'some ofht', 'this, some, other, else', 'else',
        # 0123456789012345678901234567890123456789012345678901234567890123456789012 indexs part 1
        # 0         1         2         3         4         5         6         7
        # 1111123333333333333333222233333333322223333333333333333333333322223333222 levels part 1
        #
        #  'mychar\'s poses)sive', 'something else, other', 'last')"
        # 345678901234567890123456789012345678901234567890123456789 indexs part 2
        #        8         9         0         1         2
        #                            1
        # 233333333333333333333322223333333333333333333332222333321 levels part 2
        #note: the newline is not in the test example. This was just because it would not fit.
        #
        clvlnum = 1;
        fpfnd = False;
        lvls = [-1 for n in range(len(val))];#init level algorithm
        inclvaset = False;
        fqti = -1;
        fndqt = False;
        isopqt = True;
        for n in range(len(val)):
            mc = val[n];
            if (mc == '('):
                if (fpfnd): pass;
                else:
                    fpfnd = True;
                    inclvaset = True;
            elif (mc == ')'):
                #decrement the level before this, but there are exceptions
                #because this is not a strict leveling algorithm
                #parenthesis only have an effect if on level 1 to level 2 or level 2 to level 1 only
                if (clvlnum == 1 or clvlnum == 2): clvlnum -= 1;
            elif (mc == "'" or mc == '"'):
                #found a quote here.
                #print(f"found a quote at n = {n}!");
                #print(f"fndqt = {fndqt}");
                #print("need to tell if we can use this because if it got escaped, then cannot!");
                #print(val[n - 1]);
                if (fndqt):
                    if (0 < n and (val[n - 1] == "\\" or val[n - 1] == '\\')): pass;
                    else:
                        if (mc == val[fqti]):
                            #this quote is the same as our first quote therefore use it
                            #print(f"fndqt at n = {n}!");
                            #print(f"prev isopqt = {isopqt}");
                            if (isopqt): clvlnum -= 1;
                            else: inclvaset = True;
                            isopqt = not(isopqt);
                else:
                    if (0 < n and (val[n - 1] == "\\" or val[n - 1] == '\\')): pass;
                    else:
                        fndqt = True;
                        isopqt = True;
                        fqti = n;
                        inclvaset = True;
            lvls[n] = clvlnum;
            if (inclvaset):
                clvlnum += 1;
                inclvaset = False;
        #print(f" val = {val}");
        #print(f'lvls = {myvalidator.myjoin("", lvls)}');

        return myvalidator.errorCheckAndReturnTheLevels(lvls, val);

    @classmethod
    def oLevelsAlgorithm(cls, valstr):
        if (myvalidator.isvaremptyornull(valstr)):
            return {"finlvs": [], "origlvs": [], "val": valstr, "errmsg": ""};
        #print(f"valstr = {valstr}");

        levels = [-1 for i in range(len(valstr))];
        clevel = 1;
        inclvl = False;
        declvl = False;
        fqti = -1;
        fndqt = False;
        isopqt = True;
        for i in range(len(valstr)):
            mc = valstr[i];
            if (mc == '[' or mc == '('):
                #if inside a quote but reached here... then do not increment
                if (clevel > 4): pass;
                else: inclvl = True;#
            elif (mc == ']' or mc == ')'):
                #if inside a quote but reached here... then do not decrement
                if (clevel > 5): pass;
                else: declvl = True;#
            elif (mc == "'" or mc == '"'):
                #found a quote here.
                #print(f"found a quote at i = {i}!");
                #print(f"fndqt = {fndqt}");
                #print("need to tell if we can use this because if it got escaped, then cannot!");
                #print(valstr[i - 1]);
                if (fndqt):
                    if (0 < i and (valstr[i - 1] == "\\" or valstr[i - 1] == '\\')): pass;
                    else:
                        if (mc == valstr[fqti]):
                            #this quote is the same as our first quote therefore use it
                            #print(f"fndqt at i = {i}!");
                            #print(f"prev isopqt = {isopqt}");
                            if (isopqt): declvl = True;
                            else: inclvl = True;
                            isopqt = not(isopqt);
                else:
                    if (0 < i and (valstr[i - 1] == "\\" or valstr[i - 1] == '\\')): pass;
                    else:
                        fndqt = True;
                        isopqt = True;
                        fqti = i;
                        inclvl = True;
            if (declvl):
                #dec immediately, then add level, then set to false
                clevel -= 1;
                levels[i] = clevel;
                declvl = False;
            else:
                #add the level here..., then increment..., then set to false
                levels[i] = clevel;
                if (inclvl):
                    clevel += 1;
                    inclvl = False;
        
        #print(f"valstr = {valstr}");
        #print(f"levels = {myvalidator.myjoin('', levels)}");
        return myvalidator.errorCheckAndReturnTheLevels(levels, valstr);

    @classmethod
    def getParamsFromValType(cls, val):
        #params are everything after the first ( and the last )
        #everything else is ignored.
        #if value is not valid, then return empty or null
        #params can be inside ' or ", but ignore it if it is escaped
        #commas inside ' or " can be ignored, but others outside of that cannot be ignored.
        lvsobj = myvalidator.getLevelsForValStr(val);
        #print(f"lvsobj = {lvsobj}");

        if (len(lvsobj["errmsg"]) < 1):
            if (2 in lvsobj["finlvs"]): pass;
            else: return [];#level 2 is not found no parenthesis no parameters

            #get all of the comma space indexes on level 2 only.
            #these will be the values... stored pretty much exactly as they are.
            #after the first ( index and before the last )
            cmaisonlvtwo = [n for n in range(len(lvsobj["finlvs"]))
                            if (val[n] == "," and lvsobj["finlvs"][n] == 2)];
            #print(f"cmaisonlvtwo = {cmaisonlvtwo}");
            
            #the delimeter is , space so the items in the list are all values
            #we might be able to split the string at these indexes only
            #but we need to know where the bounds are that we want
            #given that the algorithmn is special, we can figure out based on where the levels change
            #where is the first change from 1 to 2 and the last change from 2 to 1?
            fpi = -1;
            fndit = False;
            for n in range(len(val)):
                if ((lvsobj["finlvs"][n] == 2) and ((0 < n) and (lvsobj["finlvs"][n - 1] == 1))):
                    fpi = n;
                    fndit = True;
                    break;
            #print(f"fpi = {fpi}");
            #print(f"fndit = {fndit}");
            
            if (fndit):
                if (0 < fpi and fpi < len(val)): pass;
                else: raise ValueError("fpi is invalid!");
            else: raise ValueError("we must have found the interchange!");

            lpi = -1;
            fndit = False;
            for n in range(len(val) - 1, 0, -1):
                if ((lvsobj["finlvs"][n] == 1) and (0 < n) and (lvsobj["finlvs"][n - 1] == 2)):
                    lpi = n;
                    fndit = True;
                    break;
            #print(f"lpi = {lpi}");
            #print(f"fndit = {fndit}");

            if (fndit):
                if (0 < lpi and lpi < len(val) and fpi < lpi): pass;
                else: raise ValueError("lpi is invalid!");
            else: raise ValueError("we must have found the interchange!");
            psstronly = val[fpi: lpi];
            #print(f"psstronly = {psstronly}");

            #all we have to do is split the string properly now and then return
            strssplit = myvalidator.mysplitWithLen(psstronly, cmaisonlvtwo, 2, -fpi);
            #print(f"strssplit = {strssplit}");

            #what about the empty strings that split will occassionally leave us with?
            #the empty strings that split will leave us with should be removed.
            return [mstr for mstr in strssplit if (0 < len(mstr))];
        else: return [];

    #val is the data type value
    #varstr is the SQL VARIANT string
    @classmethod
    def isValidDataType(cls, val, varstr):
        #get data types for the specific variant
        #if the list is empty or null, then assumed valid
        #if on the list, valid
        #if not on the list and list is not empty, then not valid.
        #print(f"val = {val}");
        #print(f"varstr = {varstr}");

        datatypesinfolist = myvalidator.getSQLDataTypesInfo(varstr);
        mvtpslist = myvalidator.getValidSQLDataTypesFromInfoList(datatypesinfolist);
        if (myvalidator.isvaremptyornull(mvtpslist)): return True;
        else:
            valnmhasps = ("(" in val and ")" in val);
            valnmhascma = ("," in val);
            #print(f"valnmhasps = {valnmhasps}");
            #print(f"valnmhascma = {valnmhascma}");
            
            valfpi = (val.index("(") if valnmhasps else -1);
            if (valnmhasps):
                valfinpi = val.rindex(")");
                if (valnmhascma):
                    valbgcmai = val.index(",");
                    valfincmai = val.rindex(",");
                    #print(f"valfpi = {valfpi}");
                    #print(f"valbgcmai = {valbgcmai}");
                    #print(f"valfincmai = {valfincmai}");
                    #print(f"valfinpi = {valfinpi}");

                    if (valfpi < valbgcmai and valbgcmai < valfinpi and
                        valfpi < valfincmai and valfincmai < valfinpi):
                            pass;
                    else:
                        #raise ValueError("the comma in the name must be inside of a set of " +
                        #                 "parenthesis in order for the name " + val +
                        #                 " to be valid, but it did not have parenthesis!");
                        return False;
            else:
                if (valnmhascma):
                    #raise ValueError("the comma in the name must be inside of a set of " +
                    #                 "parenthesis in order for the name " + val +
                    #                 " to be valid, but it did not have parenthesis!");
                    return False;

            valbgnm = (val[0:valfpi] if valnmhasps else "" + val);
            #print(f"valbgnm = {valbgnm}");

            pmtchmsg = "only perfect matchs in the form tpnm(max) are allowed with parentheis, ";
            pmtchmsg += "perfect matchs that only have alphabetic characters A-Z and a-z only ";
            pmtchmsg += "are allowed! The last character can be a number!";
            for mtp in mvtpslist:
                nmhasps = ("(" in mtp and ")" in mtp);
                #print(f"mtp = {mtp}");
                #print(f"nmhasps = {nmhasps}");

                if (valnmhasps == nmhasps):
                    #likely a match; otherwise definitely not a match
                    if (nmhasps):
                        #go to first (
                        #this is the iniitial type name
                        #go to last )
                        #everything in between are values parameters or max
                        #if everything in between is max only
                        #ie only (max) is in there and after that is end of the string immediately
                        #then it is a perfect match...
                        bgpindx = mtp.index("(");
                        #print(f"bgpindx = {bgpindx}");

                        bgnm = mtp[0:bgpindx];
                        #print(f"bgnm = {bgnm}");

                        if (valbgnm == bgnm):
                            #it can be a perfect match and not be valid
                            #the only perfect matchs accepted are if no parenthesis,
                            #or with tpnm(max) only
                            if (val == mtp):
                                #print("found our perfect match!");
                                #print(pmtchmsg);
                                return ((valbgnm + "(max)" == val) and (bgnm + "(max)" == mtp));
                            else:
                                #need to know if unsigned...
                                #need to get the ranges for those types on those numbers...
                                #need to verify the ranges on the numbers for those data types...
                                #verify that the number of parameters given match
                                #if can have none, then the defaults are used.
                                #if some are given where none is accepted, error.
                                #
                                #get the parameters provided from the value then
                                #
                                #what we want is a specific range object for the variant
                                #with the type names
                                #for each object on this list:
                                #-check and see if the number of parameters match
                                #--if using max num params = 0
                                #-if no match on parameters, error out
                                #-if there is a match, check the range
                                #-if the range matches or is valid, this is probably it. say valid.
                                #-if the range does not match, move on there might be another.
                                
                                mynm = ("" + val if ("(max)" in val) else bgnm);
                                psonval = ([] if ("(max)" in val) else
                                           myvalidator.getParamsFromValType(val));
                                numpsonval = (0 if ("(max)" in val) else len(psonval));
                                tpobjslist = myvalidator.getDataTypesObjsWithNameFromList(
                                    datatypesinfolist, mynm);
                                #print(f"mynm = {mynm}");
                                #print(f"psonval = {psonval}");
                                #print(f"numpsonval = {numpsonval}");
                                #print(f"tpobjslist = {tpobjslist}");
                                
                                for tpobj in tpobjslist:
                                    if (len(tpobj["paramnameswithranges"]) == numpsonval):
                                        #then we check the values to see if they match or are valid
                                        #if the length is zero no need to check the parameter values
                                        #that one is valid. once a match is found
                                        if (numpsonval == 0): return True;
                                    elif (len(tpobj["paramnameswithranges"]) < numpsonval):
                                        #if param type is an array or list, this is wrong
                                        #so wrong for ENUMs and SETs for MYSQL for sure.
                                        #print("number of params on val is more than for the type!");
                                        if (mynm == "ENUM" or mynm == "SET"): pass;
                                        else: continue;#not a match, maybe another is.
                                    if (numpsonval == 0):
                                        #check to see if all of the parameters have a default value
                                        #if they do not move on
                                        getnext = False;
                                        for n in range(len(tpobj["paramnameswithranges"])):
                                            cpobj = tpobj["paramnameswithranges"][n];
                                            #print(f"cpobj = {cpobj}");

                                            if (cpobj["hasadefault"]): pass;
                                            else:
                                                getnext = True;
                                                break;
                                        if (getnext): continue;
                                        else: return True;
                                    else:
                                        #either equal to or less than the max parameters were provided
                                        #if the param data type is a number,
                                        #then the values will need to be converted to that first
                                        #otherwise no conversion is needed.
                                        #if can be signed or not is true, then number
                                        #cannot use a list comprehension here because
                                        #that is too comprehensive
                                        getnext = False;
                                        finpsonval = None;
                                        
                                        #if type is a number then the parameters are numbers for sure
                                        #if type is not a number, then it may have parameters
                                        #which are numbers and it may not.
                                        #we need to know which types do have parameters
                                        #which are numbers and the ones that do not
                                        #print(f"tpobj = {tpobj}");

                                        #we really only care about the parameters sake
                                        #if can specify range is true for all of the parameters
                                        #then this is a number type too
                                        tphasnumparams = tpobj["canbesignedornot"];
                                        if (tphasnumparams): pass;
                                        else:
                                            if (myvalidator.isvaremptyornull(
                                                tpobj["paramnameswithranges"])): pass;
                                            else: tphasnumparams = True;
                                            for paramobj in tpobj["paramnameswithranges"]:
                                                if (paramobj["canspecifyrange"]): pass;
                                                else:
                                                    tphasnumparams = False;
                                                    break;
                                        #print(f"tphasnumparams = {tphasnumparams}");

                                        if (tphasnumparams):
                                            finpsonval = [];
                                            for pval in psonval:
                                                if (myvalidator.isstranumber(pval)):
                                                    if ("." in pval):
                                                        #the parameters are not valid
                                                        #return False;
                                                        getnext = True;
                                                        break;
                                                    finpsonval.append(int(pval));
                                                else:
                                                    #the parameters are not valid
                                                    #return False;
                                                    getnext = True;
                                                    break;
                                            if (getnext): continue;
                                        else: finpsonval = [pval for pval in psonval];
                                        #print(f"finpsonval = {finpsonval}");
                                        
                                        #make sure the given values are in the ranges...
                                        #if all have default values, you may not need any
                                        #if one is different than the rest,
                                        #you need to provide up to and including it,
                                        #but do not have to provide after of course
                                        if (mynm == "ENUM" or mynm == "SET"):
                                            #the values do not have a specified range,
                                            #but they do have a specified length,
                                            #but it is not a parameter
                                            #the length or size is given on the type object,
                                            #but not on the params range object(s).
                                            #look for length or size on the main type object.
                                            #then compare the length of the valparams against this
                                            
                                            #both ENUMS and SETS cannot have duplicate values
                                            #print("THIS IS AN ENUM OR A SET!");
                                            for n in range(len(finpsonval)):
                                                if (getnext): break;
                                                for k in range(n + 1, len(finpsonval)):
                                                    if (finpsonval[n] == finpsonval[k]):
                                                        getnext = True;
                                                        break;
                                            
                                            for valobj in tpobj["valuesranges"]:
                                                if (getnext): break;
                                                #print(f"valobj = {valobj}");

                                                if (valobj["paramname"] in ["length", "size"]):
                                                    if (numpsonval < 0 or valobj["max"] < numpsonval):
                                                        getnext = True;
                                                        break;
                                                    else: return True;
                                            if (getnext): pass;
                                            else:
                                                raise ValueError("the data type info object was " +
                                                                 "built wrong for (" + mynm +
                                                                 ") for variant (" + varstr + ")!");
                                        else:
                                            for n in range(len(tpobj["paramnameswithranges"])):
                                                isivforbth = (n < numpsonval);
                                                #print(f"isivforbth = {isivforbth}");
                                                
                                                cpobj = tpobj["paramnameswithranges"][n];
                                                cpval = (finpsonval[n] if isivforbth else None);
                                                #print(f"cpval = {cpval}");
                                                #print(f"cpobj = {cpobj}");

                                                if (isivforbth):
                                                    if (cpobj["canspecifyrange"]):
                                                        if (cpval < cpobj["min"] or
                                                            cpobj["max"] < cpval):
                                                                getnext = True;#invalid
                                                else:
                                                    if (cpobj["hasadefault"]): pass;
                                                    else: getnext = True;#invalid must have a default
                                                if (getnext): break;
                                        if (getnext): continue;
                                        else: return True;
                    else:
                        #comma in name, but no parenthesis has already been handled.
                        #name must be alphabetic only for a perfect match without parenthesis
                        #to be valid.
                        if (val == mtp):
                            #print("found our perfect match!");
                            #print(pmtchmsg);
                            if (val.isalpha()): return True;
                            else:
                                if (1 < len(val)):
                                    return (val[0:len(val) - 1].isalpha() and
                                            val[len(val) - 1].isalnum()); 
                                else: return val.isalpha();
            #print("data type is not valid!");
            return False;

    @classmethod
    def isDataTypeOnList(cls, tobj, tpnmslist, numps):
        myvalidator.varmustbethetypeonly(numps, int, varnm="numps");
        myvalidator.valueMustBeInRange(numps, 0, 0, True, False, varnm="numps");
        rkys = ["names", "paramnameswithranges"];
        myvalidator.objvarmusthavethesekeysonit(tobj, rkys, varnm="tobj");
        return (myvalidator.isListAInListB(tobj[rkys[0]], tpnmslist) and len(tobj[rkys[1]]) == numps);

    #varnm is the SQL VARIANT
    @classmethod
    def getDataTypesObjsFromTypeName(cls, fulltpnm, varnm):
        #or the ones that match that name...
        #if the full type name has (max) on it, then use the full name
        #else use the beginning name
        myvalidator.varmustnotbeempty(fulltpnm, varnm="fulltpnm");
        myvalidator.varmustnotbeempty(varnm, varnm="varnm");
        nmhaspsonit = ("(" in fulltpnm and ")" in fulltpnm);
        bgnm = (fulltpnm[0: fulltpnm.index("(")] if (nmhaspsonit) else "" + fulltpnm);
        mynm = ("" + fulltpnm if ("(max)" in fulltpnm) else bgnm);
        psonval = ([] if ("(max)" in fulltpnm) else myvalidator.getParamsFromValType(fulltpnm));
        numpsonval = (0 if ("(max)" in fulltpnm) else len(psonval));
        datatypesinfolist = myvalidator.getSQLDataTypesInfo(varnm);
        return myvalidator.getDataTypesObjsWithNameFromList(datatypesinfolist, mynm);

    #results for this method cannot always be assumed to be correct.
    #if the type has multiple parameters and multiple options for these and there are multiple types
    #for example: FLOAT(side, d) and FLOAT(p) are two different types on the same variant.
    #if that is the case, then if you want the one with 1 parameter, it may still match the other.
    #
    #this method will notice that if there is a type name that matches and the number of parameters
    #are an exact match, then it will return this option.
    #otherwise it will return the first one found on the list. That list may have multiple.
    #in that case, the results of this method may be wrong.
    #
    #varnm is the SQL VARIANT
    @classmethod
    def getDataTypeObjectWithNameOnVariant(cls, fulltpnm, varnm):
        #get the list of objects for the variant
        #or the ones that match that name...
        #if the full type name has (max) on it, then use the full name
        #else use the beginning name
        myvalidator.varmustnotbeempty(fulltpnm, varnm="fulltpnm");
        myvalidator.varmustnotbeempty(varnm, varnm="varnm");
        myvalidator.varmustbethetypeonly(fulltpnm, str, varnm="fulltpnm");
        myvalidator.varmustbethetypeonly(varnm, str, varnm="varnm");
        nmhaspsonit = ("(" in fulltpnm and ")" in fulltpnm);
        bgnm = (fulltpnm[0: fulltpnm.index("(")] if (nmhaspsonit) else "" + fulltpnm);
        mynm = ("" + fulltpnm if ("(max)" in fulltpnm) else bgnm);
        psonval = ([] if ("(max)" in fulltpnm) else myvalidator.getParamsFromValType(fulltpnm));
        numpsonval = (0 if ("(max)" in fulltpnm) else len(psonval));
        datatypesinfolist = myvalidator.getSQLDataTypesInfo(varnm);
        tpobjslist = myvalidator.getDataTypesObjsWithNameFromList(datatypesinfolist, mynm);
        #print(f"mynm = {mynm}");
        #print(f"psonval = {psonval}");
        #print(f"numpsonval = {numpsonval}");
        #print(f"tpobjslist = {tpobjslist}");

        if (myvalidator.isvaremptyornull(tpobjslist)):
            raise ValueError("no data type object found on that variant (" + varnm + ") with name: " +
                             str(fulltpnm) + "!");

        for tpobj in tpobjslist:
            #print(f"tpobj = {tpobj}");
            if (len(tpobj["paramnameswithranges"]) == numpsonval): return tpobj;
        
        #no exact matches and the type was valid so there must be a match
        #print("no exact matches found!");
        return tpobjslist[0];


    #tpnm is the SQL Data Type name for the specific variant specified by varstr
    #val is the value we are inserting into the column of that type...
    #useunsigned is for the signed or unsigned data range for numerical data types
    #-by default useunsigned is true because some data types non numerical ones are in fact unsigned.
    #-it is note worthy that some numerical data types are only signed or unsigned.
    #isnonnull is by default false to allow null as a value,
    #-however sometimes the user does not want null to be an option at all.
    #-Setting this to true ensures that.
    #varstr is the SQL VARIANT
    @classmethod
    def isValueValidForDataType(cls, tpnm, val, varstr, useunsigned=True, isnonnull=False):
        myvalidator.varmustbeboolean(isnonnull, varnm="isnonnull");
        myvalidator.varmustbeboolean(useunsigned, varnm="useunsigned");
        if (myvalidator.isValidDataType(tpnm, varstr)): pass;
        else: return False;
        
        #if the type object is not specified then the value is assumed to be valid
        datatypesinfolist = myvalidator.getSQLDataTypesInfo(varstr);
        mvtpslist = myvalidator.getValidSQLDataTypesFromInfoList(datatypesinfolist);
        if (myvalidator.isvaremptyornull(mvtpslist)): return True;

        #numeric data types are going to be easier to validate than the others
        #then dates probably
        #then we will go by those that have some sort of length or size requirement
        #then those without restrictions are valid.
        #without restrictions means no range on the values and no limit on the size or length.
        
        nmhasps = ("(" in tpnm and ")" in tpnm);
        bgnm = (tpnm[0:tpnm.index("(")] if (nmhasps) else "" + tpnm);
        mynm = ("" + tpnm if ("(max)" in tpnm) else bgnm);
        #print(f"tpnm = {tpnm}");
        #print(f"varstr = {varstr}");
        #print(f"val = {val}");
        #print(f"nmhasps = {nmhasps}");
        #print(f"bgnm = {bgnm}");
        #print(f"mynm = {mynm}");
        #print(f"isnonnull = {isnonnull}");
        #print(f"useunsigned = {useunsigned}");
        
        
        # or not(nmhasps)
        psonval = ([] if ("(max)" in tpnm) else myvalidator.getParamsFromValType(tpnm));
        numpsonval = (0 if ("(max)" in tpnm or not(nmhasps)) else len(psonval));
        #print(f"psonval = {psonval}");
        #print(f"numpsonval = {numpsonval}");
        
        tpobjslist = myvalidator.getDataTypesObjsWithNameFromList(datatypesinfolist, mynm);
        #print(f"tpobjslist = {tpobjslist}");
        #print();

        if (myvalidator.isvaremptyornull(tpobjslist)): return True;

        tpnmswithfdptdgts = myvalidator.getAllDataTypesWithASetAmountOfDigitsAndAfterDecimalPoint(
            varstr);
        #print(f"tpnmswithfdptdgts = {tpnmswithfdptdgts}");
        dgtsadptonly = myvalidator.getAllDataTypesWithASetAmountOfDigitsAfterTheDecimalPointOnly(
            varstr);
        #print(f"dgtsadptonly = {dgtsadptonly}");
        tpswithlistp = myvalidator.getAllDataTypesWithAListAsTheParameter(varstr);
        #print(f"tpswithlistp = {tpswithlistp}");
        tpswdispwp = myvalidator.getTypesThatHaveADisplayWidthParam(varstr);
        #print(f"tpswdispwp = {tpswdispwp}");
        tpslenasp = myvalidator.getTypesThatHaveLengthAsTheParam(varstr);
        #print(f"tpslenasp = {tpslenasp}");
        tpsrellenasp = myvalidator.getTypesThatHaveAByteRelatedLengthAsTheParam(varstr);
        #print(f"tpsrellenasp = {tpsrellenasp}");
        alltpsrelen = myvalidator.getAllTypesThatHaveAByteRelatedLength(varstr);
        #print(f"alltpsrelen = {alltpsrelen}");
        #print();

        dtpinfoobjerrmsg = "the data type info object was built wrong for (" + mynm;
        dtpinfoobjerrmsg += ") for the variant (" + varstr + ")!";

        for tobj in tpobjslist:
            #print(f"tobj = {tobj}");
            #print();

            if (myvalidator.isvaremptyornull(tobj["valuesranges"])):
                if (tobj["isvalue"]): return (val in tobj["names"]);
                else: raise ValueError(dtpinfoobjerrmsg);
            else:
                getnext = False;
                twodiffranges = False;
                minrngval = 0;
                invalidvalontperrmsg = "invalid value stored on a " + (', '.join(tobj['names'])) + "!";
                for vrobj in tobj["valuesranges"]:
                    #print(f"vrobj = {vrobj}");
                    #print();

                    isnumcomp = False;
                    valforcomp = val;
                    if (vrobj["paramname"] in ["length", "size"]):
                        #enforce the length restriction here...
                        #this may also come in as a required parameter
                        #print("vr has length or size as a required parameter!");
                        
                        if (vrobj["canspecifyrange"]):
                            isnumcomp = True;
                            valforcomp = len(val);
                        else: raise ValueError(dtpinfoobjerrmsg);
                
                    elif (vrobj["paramname"] in ["values", "range"]):
                        #paramname is something else like values or range
                        if (vrobj["hasadefault"]):
                            if (val == vrobj["defaultval"]):
                                if (val == "NULL"):
                                    if (isnonnull):
                                        #print("non-null required, but NULL found!");
                                        getnext = True;
                                        break;
                                    else: return True;
                                else: return True;
                        if (vrobj["canspecifyrange"]):
                            #this value has a max and min
                            #sensitive to format and type now
                            #if it is some sort of number type comparisions are easy
                            if (tobj["canbesignedornot"]):
                                #these are numerical comparisons
                                isnumcomp = True;
                                #valforcomp = val;
                            else:
                                #value is not a number but has a range...
                                #DATEs TIMEs stuff like that here...
                                #
                                #MYSQL DATE TIME TYPES:
                                #
                                #"DATE" min "1000-01-01" max "9999-12-31"
                                #"DATETIME"(fsp) min "1000-01-01 00:00:00.000000"
                                # max "9999-12-31 23:59:59.999999"
                                #"TIMESTAMP"(fsp) min "1970-01-01 00:00:01.000000"
                                # max "2038-01-09 03:14:07.999999"
                                #"TIME"(fsp) min "-838:59:59.000000" max "838:59:59.999999"
                                #"YEAR" min 1901 max 2155;
                                #
                                #SQLSERVER DATE TIME TYPES:
                                #
                                #"DATETIME" min "1753-01-01 00:00:00.000" max "9999-12-31 23:59:59.999"
                                #"DATETIME2" min "0001-01-01 00:00:00.0000000"
                                #max "9999-12-31 23:59:59.9999999"
                                #"SMALLDATETIME" min "1900-01-01 00:00:00" max "2079-06-06 23:59:59"
                                #"DATE" min "0001-01-01" max "9999-12-31"
                                #"TIME" min "00:00:00.0000000" max "23:59:59.9999999"
                                #"DATETIMEOFFSET" min "0001-01-01 00:00:00.0000000 - 23:59"
                                # max "9999-12-31 23:59:59.9999999 + 23:59"
                                #      012345678901234567890123456789012345
                                #      0         1         2         3
                                #
                                #comparison method I wrote will work on everything except
                                #"DATETIMEOFFSET" on SQLSERVER.
                                
                                #need to check to see if the value is in the given range.
                                #the range values include hours.
                                #we do not know if the value includes hours or not
                                #if it is a time string
                                #either we can flag it as not being in the correct format and skip it
                                #or just always treat it as if the hour string was included.
                                
                                #print("type is not number, but has a range.\n");
                                
                                minrngval = vrobj["min"];
                                maxrngval = vrobj["max"];
                                
                                #if TIME in the type name, then hours will be included on min and max
                                #otherwise hours will not be included
                                inchrsonmnandmx = False;
                                for tpnm in tobj["names"]:
                                    if ("TIME" in tpnm):
                                        inchrsonmnandmx = True;
                                        break;
                                incvdtcheck = False;
                                for tpnm in tobj["names"]:
                                    if ("DATE" in tpnm):
                                        incvdtcheck = True;
                                        break;
                                #print(f"inchrsonmnandmx = {inchrsonmnandmx}");
                                #print(f"incvdtcheck = {incvdtcheck}");
                                #print(f"minrngval = {minrngval}");
                                #print(f"maxrngval = {maxrngval}");
                                #print(f"val = {val}");

                                #handle the "DATETIMEOFFSET" on SQLSERVER here.
                                #the mins and maxs and vals need to be split into two parts
                                dtnoval = None;
                                dtmxval = None;
                                dtmnval = None;
                                if ("DATETIMEOFFSET" in tobj["names"]):
                                    #val = "0001-01-01 00:00:00.0000000";#so can test other case
                                    valspcis = [n for n in range(len(val)) if val[n:].startswith(" ")];
                                    minrngvalpts = myvalidator.mysplitWithLen(minrngval, [27], 1, 0);
                                    maxrngvalpts = myvalidator.mysplitWithLen(maxrngval, [27], 1, 0);
                                    minrngvalpta = minrngvalpts[0];
                                    minrngvalptb = minrngvalpts[1];
                                    maxrngvalpta = maxrngvalpts[0];
                                    maxrngvalptb = maxrngvalpts[1];
                                    valdelimi = (valspcis[1] if (1 < len(valspcis)) else len(val));
                                    valpts = myvalidator.mysplitWithLen(val, [valdelimi], 1, 0);
                                    valpta = valpts[0];
                                    valptb = valpts[1];
                                    dtnoval = "" + valpta;
                                    dtmxval = "" + maxrngvalpta;
                                    dtmnval = "" + minrngvalpta;
                                    #print(f"valspcis = {valspcis}");
                                    #print(f"valpts = {valpts}");
                                    #print(f"valdelimi = {valdelimi}");
                                    #print(f"minrngvalpts = {minrngvalpts}");
                                    #print(f"maxrngvalpts = {maxrngvalpts}");
                                    #print(f"minrngvalpta = {minrngvalpta}");
                                    #print(f"minrngvalptb = {minrngvalptb}");
                                    #print(f"maxrngvalpta = {maxrngvalpta}");
                                    #print(f"maxrngvalptb = {maxrngvalptb}");
                                    #print(f"valpta = {valpta}");
                                    #print(f"valptb = {valptb}");

                                    #where do we split the val then?
                                    #if it is valid, we would maybe split it at 27, but could earlier
                                    #there is a limit as to how early and what format it would have
                                    #to be in though
                                    #assume val is valid and split at the second space index
                                    #
                                    #what do we do with all of the part b values?
                                    #we need to make sure that they are valid too.
                                    #processing the min and max part b values will be the same
                                    #it is processing the value that I do not know.
                                    
                                    mnptbcnvtstr = myvalidator.convertTimeOffsetStringToTimeString(
                                        minrngvalptb);
                                    mxptbcnvtstr = myvalidator.convertTimeOffsetStringToTimeString(
                                        maxrngvalptb);
                                    valptbcnvtstr = myvalidator.convertTimeOffsetStringToTimeString(
                                        valptb);
                                    mnptbtimeobj = myvalidator.getTimeObject(mnptbcnvtstr, True);
                                    mxptbtimeobj = myvalidator.getTimeObject(mxptbcnvtstr, True);
                                    valptbtimeobj = None;
                                    try:
                                        valptbtimeobj = myvalidator.getTimeObject(valptbcnvtstr, True);
                                    except Exception as ex:
                                        #print(dir(ex));
                                        #print(ex);
                                        #traceback.print_exc();
                                        #print("the value was not valid!");
                                        getnext = True;
                                        break;
                                    #print(f"mnptbtimeobj = {mnptbtimeobj}");
                                    #print(f"mxptbtimeobj = {mxptbtimeobj}");
                                    #print(f"valptbtimeobj = {valptbtimeobj}");

                                    compvalptbmin = myvalidator.compareTwoTimeObjsOnly(valptbtimeobj,
                                                                                       mnptbtimeobj);
                                    compvalptbmax = myvalidator.compareTwoTimeObjsOnly(valptbtimeobj,
                                                                                       mxptbtimeobj);
                                    #print(f"compvalptbmin = {compvalptbmin}");
                                    #print(f"compvalptbmax = {compvalptbmax}");
                                    #0 same, -1 means a is less than b, 1 means a is greater than b.
                                    #val < maxrngval is -1 when a is before b.
                                    #val < maxrngval is 1 when b is before a.
                                    #if (valforcomp < minrngval or maxrngval < valforcomp):
                                    if (compvalptbmin == -1 or compvalptbmax == 1):
                                        #value is invalid
                                        #print("the value is outside of the required range!");
                                        getnext = True;
                                        break;
                                else:
                                    dtnoval = "" + val;
                                    dtmxval = "" + maxrngval;
                                    dtmnval = "" + minrngval;
                                #print(f"dtnoval = {dtnoval}");
                                #print(f"dtmnval = {dtmnval}");
                                #print(f"dtmxval = {dtmxval}");

                                #if inchrsonmnandmx is FALSE, then for sure the value will not have it
                                #if it is TRUE, the value could include it or not.
                                valusehrs = False;
                                if (inchrsonmnandmx):
                                    try:
                                        valusehrs = myvalidator.dateTimeStringIncludesHours(dtnoval,
                                                                                            True);
                                    except Exception as ex:
                                        #print(dir(ex));
                                        #print(ex);
                                        #traceback.print_exc();
                                        #print("the value was not valid!");
                                        getnext = True;
                                        break;
                                #print(f"valusehrs = {valusehrs}");

                                compvalmin = -2;
                                compvalmax = -2;
                                try:
                                    compvalmin = myvalidator.compareTwoDateTimeStrs(dtnoval, dtmnval,
                                                                                    valusehrs,
                                                                                    inchrsonmnandmx);
                                except Exception as ex:
                                    #print(dir(ex));
                                    #print(ex);
                                    #traceback.print_exc();
                                    #print("the value was not valid (compminfail)!");
                                    getnext = True;
                                    break;
                                try:
                                    compvalmax = myvalidator.compareTwoDateTimeStrs(dtnoval, dtmxval,
                                                                                    valusehrs,
                                                                                    inchrsonmnandmx);
                                except Exception as ex:
                                    #print(dir(ex));
                                    #print(ex);
                                    #traceback.print_exc();
                                    #print("the value was not valid (compmaxfail)!");
                                    getnext = True;
                                    break;
                                #print(f"compvalmin = {compvalmin}");
                                #print(f"compvalmax = {compvalmax}");
                                
                                dtobja = myvalidator.getDateAndTimeObjectInfoFromString(dtnoval,
                                                                                            valusehrs);
                                #print(f"dtobja = {dtobja}");
                                
                                if (incvdtcheck):
                                    if (myvalidator.isValidDateFromObj(dtobja["dateobj"])): pass;
                                    else:
                                        #print("the date is not valid!");
                                        getnext = True;
                                        break;
                                
                                if (inchrsonmnandmx and varstr == "SQLSERVER"):
                                    fscsnum = dtobja["timeobj"]["fractionalsecondsnum"];
                                    fscsnuminstr = dtobja["timeobj"]["fractionalsecondsnuminstr"];
                                    fscsnumstr = str(fscsnum);
                                    #print(f"fscsnum = {fscsnum}");
                                    #print(f"fscsnuminstr = {fscsnuminstr}");

                                    #extract the maximum number of digits from the max value
                                    #go to the last index of the decimal point if it exists
                                    #then extract it...
                                    #it will be after the last colon index
                                    
                                    mxlci = dtmxval.rindex(":");
                                    #print(f"mxlci = {mxlci}");
                                    #print(f"dtmxval = {dtmxval}");
                                    #print(f"len(dtmxval) = {len(dtmxval)}");
                                    
                                    mxlpi = -1;
                                    mxlpifnd = False;
                                    for i in range(mxlci + 1, len(dtmxval)):
                                        if (dtmxval[i] == '.'):
                                            mxlpi = i;
                                            mxlpifnd = True;
                                            break;
                                    #print(f"mxlpi = {mxlpi}");
                                    #print(f"mxlpifnd = {mxlpifnd}");

                                    vallci = -1;
                                    valclifnd = False;
                                    lpi = -1;
                                    lpifnd = False;
                                    for i in range(len(dtnoval)):
                                        if (dtnoval[i] == ':'):
                                            valclifnd = True;
                                            vallci = i;
                                        elif (dtnoval[i] == '.'):
                                            lpi = i;
                                            lpifnd = True;
                                    #print(f"vallci = {vallci}");
                                    #print(f"valclifnd = {valclifnd}");
                                    #print(f"lpi = {lpi}");
                                    #print(f"NEW lpifnd = {lpifnd}");

                                    #assume that the value is right even if there is no colon
                                    #this may not be correct.
                                    #but we only care about the decimal point anyways
                                    if (lpi < vallci): lpifnd = False;
                                    #print(f"FINAL lpifnd = {lpifnd}");
                                    
                                    compfscnumval = (len(fscsnumstr) if (fscsnuminstr and lpifnd)
                                                     else 0);
                                    #print(f"compfscnumval = {compfscnumval}");

                                    mxnumdgts = 0;
                                    if (mxlci < mxlpi and mxlpi < len(dtmxval)):
                                        #valid
                                        #print("the last period index was valid!");
                                        mxnumdgts = len(dtmxval) - mxlpi - 1;
                                    #print(f"mxnumdgts = {mxnumdgts}");
                                    
                                    if (mxnumdgts < compfscnumval):
                                        #print("the number of digits after the decimal point on the " +
                                        #      "seconds num is not valid!");
                                        getnext = True;
                                        break;

                                #val < maxrngval is -1 when a is before b.
                                #val < maxrngval is 1 when b is before a.
                                #if (valforcomp < minrngval or maxrngval < valforcomp):
                                if (compvalmin == -1 or compvalmax == 1):
                                    #value is invalid
                                    #print("the value is outside of the required range!");
                                    getnext = True;
                                    break;
                
                    elif (vrobj["paramname"] in ["signed", "unsigned"]):
                        #need to know which one we are using signed or unsigned if it matches this
                        #then this will be the range we use else skip it.
                        #need to know if unsigned...
                        #print(f"useunsigned = {useunsigned}");
                        
                        if ((useunsigned and (vrobj["paramname"] == "unsigned")) or
                            (not(useunsigned) and (vrobj["paramname"] == "signed"))):
                                #these are numerical comparisons
                                twodiffranges = True;
                                isnumcomp = True;
                                #valforcomp = val;
                    else:
                        #this is the this should not make it here case
                        #paramname is really specific to type and variant
                        print(f"tobj = {tobj}");
                        print(f"vrobj = {vrobj}");
                        print(f"vrobj['paramname'] = {vrobj['paramname']}");
                        print("this param name is really specific to the type and the range!");
                        raise ValueError("the parameters need to be handled, but have not been!");
                    
                    #print(f"isnumcomp = {isnumcomp}");
                    #print(f"valforcomp = {valforcomp}");
                    
                    if (isnumcomp):
                        #these are numerical comparisons
                        if (myvalidator.isvaranumber(valforcomp)): pass;
                        else:
                            #print("value is not not a number on a numerical comparison!");
                            getnext = True;
                            break;
                        
                        minrngval = vrobj["min"];
                        maxrngval = vrobj["max"];
                        dobooldatacheck = myvalidator.isListAInListB(tobj["names"], alltpsrelen);
                        if (dobooldatacheck):
                            minrngval *= 8;
                            maxrngval *= 8;
                        
                        if (valforcomp < minrngval or maxrngval < valforcomp):
                            #invalid, but the next one in the type object might be
                            #need to exit vrloop and need to move on to the next type object
                            #print("value is not in the range, not the default, and not valid!");
                            getnext = True;
                            break;
                        else:
                            #print("value is in the range!");

                            if (dobooldatacheck):
                                valstr = str(val);
                                for c in valstr:
                                    if (c == "0" or c == "1"): pass;
                                    else:
                                        #print(invalidvalontperrmsg);
                                        getnext = True;
                                        break;

                if (getnext): pass;
                else:
                    if (tobj["canbesignedornot"]):
                        #print(f"twodiffranges = {twodiffranges}");
                        #print(f"isnonnull = {isnonnull}");
                        #print(f"useunsigned = {useunsigned}");
                        #print(f"minrngval = {minrngval}");
                        #if not a number, then useunsigned must be true.
                        #if some kind of number:
                        #-if two different ranges is true, then we can for sure use unsigned
                        #-if one range, depends on what the minimum is if minimum is at least 0
                        #then this is unsigned otherwise, error if useunsigned is true.

                        if (isnonnull):
                            if (twodiffranges): pass;#useunsigned can be true or false in this case
                            else:
                                if (minrngval < 0):
                                    if (useunsigned):
                                        #print("using unsigned, but the min range value is signed!");
                                        getnext = True;
                                else:
                                    if (useunsigned): pass;
                                    else:
                                        #print("using signed, but the min range value is unsigned!");
                                        getnext = True;
                        else:
                            #print("this is a number, therefore not null, but null required!");
                            getnext = True;
                    else:
                        if (useunsigned): pass;
                        else:
                            #print("this is not a number, but required to be signed!");
                            getnext = True;

                finpsonval = None;
                if (getnext): pass;
                else:
                    #we really only care about the parameters sake
                    #if can specify range is true for all of the parameters
                    #then this is a number type too
                    tphasnumparams = tobj["canbesignedornot"];
                    if (tphasnumparams): pass;
                    else:
                        if (myvalidator.isvaremptyornull(tobj["paramnameswithranges"])): pass;
                        else: tphasnumparams = True;
                        for paramobj in tobj["paramnameswithranges"]:
                            if (paramobj["canspecifyrange"]): pass;
                            else:
                                tphasnumparams = False;
                                break;
                    #print(f"tphasnumparams = {tphasnumparams}");

                    if (tphasnumparams):
                        finpsonval = [];
                        for pval in psonval:
                            if (myvalidator.isstranumber(pval)):
                                if ("." in pval):
                                    #the parameters are not valid
                                    #return False;
                                    #print("the parameters must be an integer number only!");
                                    getnext = True;
                                    break;
                                finpsonval.append(int(pval));
                            else:
                                #the parameters are not valid
                                #return False;
                                #print("the parameters must be an integer number only!");
                                getnext = True;
                                break;
                        if (getnext): continue;
                    else: finpsonval = [pval for pval in psonval];
                    #print(f"finpsonval = {finpsonval}");

                if (getnext): pass;
                else:
                    #initially the type is correct and is given valid values
                    #if that is not the case, the return False above has already been reached.
                    #need to check the value against the type parameters here too
                    #if the value does not meet the type parameters for the variant, then
                    #we move on maybe it will meet another one
                    #otherwise, ours is valid so now return True.
                    if (myvalidator.isvaremptyornull(tobj["paramnameswithranges"])): return True;
                    
                    #print();
                    #print("now we need to check the type parameters!");
                    #print();
                    #print(f"val = {val}");
                    #print(f"mynm = {mynm}");
                    #print(f"tpnm = {tpnm}");
                    #print(f"finpsonval = {finpsonval}");

                    if (myvalidator.isDataTypeOnList(tobj, tpnmswithfdptdgts, 2)):
                        #print("need to handle the total number of digits and the num digits " +
                        #    "after the decimal point here!");#class 1
                        
                        mdict = {};
                        for n in range(len(tobj["paramnameswithranges"])):
                            pnmobj = tobj["paramnameswithranges"][n];
                            #print(f"pnmobj = {pnmobj}");
                            #print();
                            
                            mdict[pnmobj["paramname"]] = finpsonval[n];
                        #print(f"mdict = {mdict}");

                        #now do the length check against the value here...
                        usedkys = ["size"];
                        okys = [ky for ky in list(mdict.keys()) if ky not in usedkys];
                        
                        #note the plus 1 for the decimal point
                        #the without it for normal integer only
                        valstr = str(val);
                        szvld = ((len(valstr) == mdict["size"] + 1) if ("." in valstr) else
                                    (len(valstr) == mdict["size"]));
                        nmdsz = 0;
                        if ("." in valstr): nmdsz = len(valstr[valstr.index(".") + 1:]);
                        numdvld = (nmdsz == mdict[okys[0]]);
                        #print(f"szvld = {szvld}");
                        #print(f"numdvld = {numdvld}");

                        if (szvld and numdvld): pass;#valid
                        else:
                            #print("either the size or the number itself is out of range!");
                            getnext = True;
                    elif (myvalidator.isDataTypeOnList(tobj, dgtsadptonly, 1)):
                        #print("this has a set digits after the decimal point only!");#class 2

                        pval = finpsonval[0];
                        numdgts = -1;
                        if (varstr == "SQLSERVER" and ("FLOAT" in tobj["names"])):
                            numdgts = (7 if (pval < 25) else 15);
                        else: numdgts = pval;
                        #print(f"pval = {pval}");
                        #print(f"numdgts = {numdgts}");

                        valstr = str(val);
                        valstradpt = valstr[valstr.index(".") + 1:];
                        numdgtsadptonval = len(valstradpt);
                        #print(f"valstradpt = {valstradpt}");
                        #print(f"numdgtsadptonval = {numdgtsadptonval}");

                        if (numdgts < numdgtsadptonval):
                            #print("the number of digits on the val must be at most the " +
                            #      "required amount, but was not!");
                            getnext = True;#invalid
                    elif (myvalidator.isDataTypeOnList(tobj, tpswithlistp, 1)):
                        #print("these types have a list as the parameter!");#class 3

                        #now for these types we need to strip the quotes off of each string first
                        nwfinpsontp = [mstr[1:len(mstr) - 1] for mstr in finpsonval
                                       if myvalidator.stringMustStartAndEndWith(mstr, "'", varnm="mstr")];
                        nwval = val[1:len(val) - 1];
                        #print(f"nwfinpsontp = {nwfinpsontp}");
                        
                        #regardless of the type if the value is on the list it is a match
                        isvalid = (nwval in nwfinpsontp);
                        #print(f"isvalid = {isvalid}");

                        #the sets have an additional check
                        if (isvalid): pass;
                        else:
                            if ("SET" in tobj["names"]):
                                #print("THIS IS A SET!");
                                if (nwval in myvalidator.getCompleteSetListFromList(nwfinpsontp)):
                                    #print("found it on the full list!");
                                    pass;
                                else:
                                    #print("the value must be present on the set or on the " +
                                    #      "combo list that can be generated from the elements " +
                                    #      "on the set, but was not!");
                                    getnext = True;
                            else:
                                #print("the value was not present on the enum and must be!");
                                getnext = True;
                            #print(f"NEW getnext = {getnext}");
                
                    elif (myvalidator.isDataTypeOnList(tobj, tpswdispwp, 1)):
                        #print("these types have a display width as the parameter!");#class 4
                        
                        #note the display width does not effect what value can be stored
                        #that is the range, we can however enforce it here,
                        #but that would piss off the users.
                        #print("the display width will be depricated soon!");
                        #print("this however is not really enforced anyways!");
                        #print("however for the time being these types need it!");
                        
                        pval = finpsonval[0];
                        valstr = str(val);
                        if (pval < len(valstr)):
                            #print("you are storing a value (" + valstr + ") longer than the " +
                            #        "display width (" + str(pval) + ")!");
                            #print("but this is not actually enforced!");
                            pass;

                        #print("moving on!");
                    elif (myvalidator.isDataTypeOnList(tobj, tpslenasp, 1)):
                        #print("these data types have the length as the parameter!");#class 5
                        
                        pval = finpsonval[0];
                        valstr = str(val);
                        #print(f"pval = {pval}");
                        #print(f"len(valstr) = {len(valstr)}");

                        if (pval < len(valstr)):
                            #print("the value was too long!");
                            getnext = True;
                        else:
                            #here make sure the BIT type is storing the correct data here...
                            #this may be wrong I am not really sure yet how python handles binary
                            #nor the best way to send it to SQL...
                            if ("BIT" in tobj["names"]):
                                for c in valstr:
                                    if (c == "0" or c == "1"): pass;
                                    else:
                                        #print(invalidvalontperrmsg);
                                        getnext = True;
                                        break;
                    elif (myvalidator.isDataTypeOnList(tobj, tpsrellenasp, 1)):
                        #print("these types are byte length relative!");#class 6
                        
                        pval = finpsonval[0];
                        valstr = str(val);
                        mxvlen = pval * 8;
                        #print(f"pval = {pval}");
                        #print(f"mxvlen = {mxvlen}");
                        #print(f"len(valstr) = {len(valstr)}");

                        if (mxvlen < len(valstr)):
                            #print("the value was too long!");
                            getnext = True;
                        else:
                            #checks to see if they are storing the correct data here...
                            #this may be wrong I am not really sure yet how python handles binary
                            #nor the best way to send it to SQL...
                            for c in valstr:
                                if (c == "0" or c == "1"): pass;
                                else:
                                    #print(invalidvalontperrmsg);
                                    getnext = True;
                                    break;
                    elif ("FLOAT" in tobj["names"] and len(tobj["paramnameswithranges"]) == 1 and
                          varstr == "MYSQL"):
                        #print("THIS IS FLOAT(p) for MYSQL!");#not in a class, but needs to be handled
                        
                        #other than data storage size 1-24 inc is 4 bytes 25 to 53 inc is 8 bytes max
                        #other than that I do not think p value actually influences the value
                        #ie kind of like display width
                        #for the moment, I am going to keep it like this and do nothing.

                        #print("NOT SURE IF THE PARAMETER IN THIS CASE ACTUALLY AFFECTS THE VALUE " +
                        #      "OTHER THAN IN TERMS OF HOW MANY BYTES CAN BE STORED HERE.");
                        #raise ValueError("NOT DONE YET 3-11-2025 5:22 PM MST!");
                        pass;
                    else:
                        print(f"tobj = {tobj}");
                        print(f"vrobj = {vrobj}");

                        for pnmobj in tobj["paramnameswithranges"]:
                            print(f"pnmobj = {pnmobj}");
                            print();
                        
                            #there are several param names and type names where size is the
                            #display width
                            #if the size is not the display width but actually refers to a value,
                            #then it is more critical
                            #if the size is just the display width which does not effect
                            #the value or storage, then we can safely ignore the violation
                            #but if that is not the case, we cannot.

                            print("NOT DONE YET NEED TO DO SOMETHING HERE...!");
                        
                        raise ValueError("NOT SURE HOW TO HANDLE THESE PARAMETERS YET!");
                
                    if (getnext): pass;
                    else: return True;

        #do something here...
        #print("outside of the type objects loop!");
        return False;
