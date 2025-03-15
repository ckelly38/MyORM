class myvalidator:
    @classmethod
    def varmustbethetypeandornull(clsnm, val, tpcls, canbenull, varnm="varname"):
        if (varnm == None or (type(varnm) == str and len(varnm) < 1)):
            return clsnm.varmustbethetypeornull(val, tpcls, "varname");
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
        return clsnm.varmustbethetypeandornull(val, tpcls, False, varnm);
    @classmethod
    def varmustbeboolean(clsnm, val, varnm="varname"):
        return clsnm.varmustbethetypeonly(val, bool, varnm);
    
    @classmethod
    def varmustnotbenull(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return clsnm.varmustnotbenull(val, "varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None): raise ValueError(varnm + " must not be null!");
        else: return True;

    @classmethod
    def isvaremptyornull(clsnm, val): return (val == None or len(val) < 1);

    @classmethod
    def varmustnotbeempty(clsnm, val, varnm="varname"):
        if (varnm == None or type(varnm) == str and len(varnm) < 1):
            return clsnm.varmustnotbeempty(val, "varname");
        elif (type(varnm) == str): pass;
        else: raise TypeError("varname must be a string!");
        if (val == None or len(val) < 1): raise ValueError(varnm + " must not be empty!");
        else: return True;

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
        if (myvalidator.isvaremptyornull(varnm)): return cls.varmustbeanumber(val, "varnm");
        if (type(val) == int or type(val) == float): return True;
        else: raise ValueError("" + varnm + " must be a number, but it was not!");

    @classmethod
    def isClass(clsnm, val): return (type(val) == type);

    @classmethod
    def listMustContainUniqueValuesOnly(clsnm, mlist, varnm="varnm"):
        if (clsnm.isvaremptyornull(varnm)):
            return clsnm.listMustContainUniqueValuesOnly(mlist, "varnm");
        if (clsnm.isvaremptyornull(mlist) or len(mlist) < 2): return True;
        myset = set(mlist);
        mynwlist = list(myset);
        if (len(mlist) == len(mynwlist)): return True;
        else: raise ValueError(f"the list {varnm} must contain unique values, but it did not!");

    @classmethod
    def areTwoListsTheSame(clsnm, lista, listb):
        if (clsnm.isvaremptyornull(lista)): return (clsnm.isvaremptyornull(listb));
        else:
            if (clsnm.isvaremptyornull(listb)): return False;
            else:
                if (len(lista) == len(listb)):
                    for n in range(len(lista)):
                        if (clsnm.isvaremptyornull(lista[n])):
                            if (clsnm.isvaremptyornull(listb[n])): pass;
                            else: return False;
                        else:
                            if (clsnm.isvaremptyornull(listb[n])): return False;
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
    def twoArraysMustBeTheSameSize(cls, arra, arrb, arranm="arranm", arrbnm="arrbnm"):
        if (myvalidator.areTwoArraysTheSameSize(arra, arrb)): return True;
        else:
            raise ValueError("the two arrays " + arranm + " and " + arrbnm + " must be the same size!");

    @classmethod
    def combineTwoLists(cls, lista, listb):
        if (myvalidator.isvaremptyornull(lista)):
            return (None if myvalidator.isvaremptyornull(listb) else listb);
        else:
            if (myvalidator.isvaremptyornull(listb)): return lista;
            else:
                #combine both of the lists...
                #list of strings and another list of strings
                #copy one, then copy the other directly
                mynwlist = [mstr for mstr in lista];
                for mstr in listb:
                    mynwlist.append(mstr);
                return mynwlist;

    @classmethod
    def isListAInListB(cls, lista, listb):
        if (myvalidator.isvaremptyornull(lista)): return myvalidator.isvaremptyornull(listb);
        for itema in lista:
            if (itema in listb): pass;
            else: return False;
        return True;

    @classmethod
    def stringContainsOnlyAlnumCharsIncludingUnderscores(cls, mstr):
        if (cls.isvaremptyornull(mstr)): return True;
        else:
            cls.varmustbethetypeonly(mstr, str, "mstr");
            for c in mstr:
                if (c.isalnum() or c == '_'): pass;
                else: return False;
        return True;

    @classmethod
    def stringMustContainOnlyAlnumCharsIncludingUnderscores(cls, mstr, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return cls.stringMustContainOnlyAlnumCharsIncludingUnderscores(mstr, "varnm");
        if (cls.stringContainsOnlyAlnumCharsIncludingUnderscores(mstr)): return True;
        else: raise ValueError(varnm + " must contain alpha-numeric characters only!");

    @classmethod
    def stringHasAtMaxOrAtMinNumChars(cls, mstr, mxormnlen, usemax):
        myvalidator.varmustbeboolean(usemax, "usemax");
        myvalidator.varmustbethetypeonly(mxormnlen, int, "mxormnlen");
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
        return cls.stringHasAtMaxOrAtMinNumChars(mstr, mxormnlen, True);
    @classmethod
    def stringHasAtMaxNumChars(cls, mstr, mxormnlen):
        return cls.stringHasAtMaxOrAtMinNumChars(mstr, mxormnlen, True);
    @classmethod
    def stringHasAtMinNumChars(cls, mstr, mxormnlen):
        return cls.stringHasAtMaxOrAtMinNumChars(mstr, mxormnlen, False);

    @classmethod
    def stringMustHaveAtMaxOrAtMinNumChars(cls, mstr, mxormnlen, usemax, varnm="varnm"):
        myvalidator.varmustbeboolean(usemax, "usemax");
        myvalidator.varmustbethetypeonly(mxormnlen, int, "mxormnlen");
        if (mxormnlen < 0): raise ValueError("mxormnlen must be at least zero, but it was not!");
        if (myvalidator.isvaremptyornull(varnm)):
            return cls.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, usemax, "varnm");
        if (usemax):
            if (myvalidator.isvaremptyornull(mstr)): pass;
            else:
                if (mxormnlen < 1):
                    raise ValueError("the string " + varnm +
                        " must be empty null or undefined, but it was not!");
                else:
                    if (mxormnlen < len(mstr)):
                        raise ValueError("the string " + varnm + " must have at most " +
                            str(mxormnlen) + " characters on it, but it had more!");
        else:
            if (0 < mxormnlen):
                if (myvalidator.isvaremptyornull(mstr)):
                    raise ValueError("the string " + varnm + " must have at minimum " + str(mxormnlen) +
                        " characters on it, but it was empty or null!");
                else:
                    if (len(mstr) < mxormnlen):
                        raise ValueError("the string " + varnm + " must have at minimum " +
                            str(mxormnlen) + " characters on it, but it had less than that!");
        return True;
    @classmethod
    def stringMustHaveAtMostNumChars(cls, mstr, mxormnlen, varnm="varnm"):
        return cls.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, True, varnm);
    @classmethod
    def stringMustHaveAtMaxNumChars(cls, mstr, mxormnlen, varnm="varnm"):
        return cls.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, True, varnm);
    @classmethod
    def stringMustHaveAtMinNumChars(cls, mstr, mxormnlen, varnm="varnm"):
        return cls.stringMustHaveAtMaxOrAtMinNumChars(mstr, mxormnlen, False, varnm);

    @classmethod
    def isValueInRange(cls, val, minval, maxval, hasmin, hasmax):
        myvalidator.varmustbeboolean(hasmin, "hasmin");
        myvalidator.varmustbeboolean(hasmax, "hasmax");
        myvalidator.varmustbeanumber(val, "val");
        myvalidator.varmustbeanumber(minval, "minval");
        myvalidator.varmustbeanumber(maxval, "maxval");
        return (not((hasmin and (val < minval)) or (hasmax and (maxval < val))));
    @classmethod
    def isValueInRangeWithMaxAndMin(cls, val, minval, maxval):
        return cls.isValueInRange(val, minval, maxval, True, True);
    @classmethod
    def isValueMoreThanOrAtTheMinOnly(cls, val, minval):
        return cls.isValueInRange(val, minval, 0, True, False);
    @classmethod
    def isValueLessThanOrAtTheMaxOnly(cls, val, maxval):
        return cls.isValueInRange(val, 0, maxval, False, True);

    @classmethod
    def valueMustBeInRange(cls, val, minval, maxval, hasmin, hasmax, varnm="varnm"):
        if (myvalidator.isvaremptyornull(varnm)):
            return cls.valueMustBeInRange(val, minval, maxval, hasmin, hasmax, "varnm");
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
    def myjoin(cls, sepstr, mlist):
        if (myvalidator.isvaremptyornull(sepstr)):
            mystr = "";
            for val in mlist:
                mystr += str(val);
            return mystr;
        else: return sepstr.join(mlist);

    @classmethod
    def mysplit(cls, mystr, delimis, delimlens, offset=0):
        myvalidator.varmustbeanumber(offset, "offset");
        if (mystr == None): return None;
        myvalidator.varmustbethetypeonly(mystr, str, "mystr");
        if ((len(mystr) < 2) or myvalidator.isvaremptyornull(delimis)): return [mystr];
        isonedelimlen = False;
        if (myvalidator.areTwoArraysTheSameSize(delimis, delimlens)):
            for n in range(len(delimis)):
                myvalidator.varmustbeanumber(delimis[n], "delimis[" + str(n) + "]");
                myvalidator.varmustbeanumber(delimlens[n], "delimlens[" + str(n) + "]");
        else:
            isonedelimlen = (len(delimlens) == 1);
            if (isonedelimlen and 0 < len(delimis)):
                myvalidator.varmustbeanumber(delimlens[0], "delimlen");
                for n in range(len(delimis)):
                    myvalidator.varmustbeanumber(delimis[n], "delimis[" + str(n) + "]");
            else:
                raise ValueError("delimis len(" + str(len(delimis)) +") and delimilens len(" +
                                 str(len(delimlens)) +
                                 ") must both be the same size, but they were not!");
        #the resultant array must have num delimis + 1 so if 2 indexes 3 parts
        #the last part is allowed to be empty
        #the resultant string rejoined should have at most the same number of characters in mystr
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
            
            myvalidator.valueMustBeInRange(cdelimi, 0, len(mystr), True, True, "cdelimi");
            if (n == 0): myresarr = [mystr[0: cdelimi]];
            else: myresarr.append(mystr[prevdelimi + prevdelimlen: cdelimi]);
            if (n + 1 == len(delimis)): myresarr.append(mystr[cdelimi + cdelimlen:]);
            prevdelimlen = cdelimlen;
            prevdelimi = cdelimi;
        #print(f"myresarr = {myresarr}");

        if (len(myresarr) == len(delimis) + 1): pass;
        else: raise ValueError("generated split array did not have the correct number of strings!");
        resstr = myvalidator.myjoin("", myresarr);
        #print(f"resstr = {resstr}");

        myvalidator.stringMustHaveAtMostNumChars(resstr, len(mystr), "resstr");
        return myresarr;
    @classmethod
    def mysplitWithLen(cls, mystr, delimis, delimlen, offset=0):
        myvalidator.varmustbeanumber(delimlen, "delimlen");
        return cls.mysplit(mystr, delimis, [delimlen], offset);
    @classmethod
    def mysplitWithDelimeter(cls, mystr, delimstr, offset=0):
        if (delimstr == None): return cls.mysplitWithDelimeter(mystr, "", offset);
        else: myvalidator.varmustbethetypeonly(delimstr, str, "delimstr");
        delimis = [i for i in range(len(mystr)) if mystr.startswith(delimstr, i)];
        return cls.mysplitWithLen(mystr, delimis, len(delimstr), offset);

    @classmethod
    def genStringWithNumberText(cls, numchars):
        if (myvalidator.isValueMoreThanOrAtTheMinOnly(numchars, 0)): pass;
        else: raise ValueError("numchars must be at minimum 0, but it was not!");
        #return myvalidator.myjoin("", [(n % 10) for n in range(numchars)]);
        mystr = "";
        for n in range(numchars):
            mystr += str(n % 10);
        return mystr;

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
                if (mclsref.areGivenColNamesOnTable(mcolnames, None)): pass;
                else:
                    raise ValueError("the col names were not found on the table class(" +
                                     mclsref.__name__ + ")");
                if (singleinctname): pass;
                else: return ", ".join(mcolnames);
            mystr = "";
            for n in range(len(mcolnames)):
                mcolnm = mcolnames[n];
                ctablename = (mtablenames[0] if (isonetable and singleinctname) else mtablenames[n]);
                myvalidator.varmustnotbeempty(mcolnm, "mcolnm");
                mytempcls = mycol.getClassFromTableName(ctablename);
                myvalidator.varmustnotbenull(mytempcls, "mytempcls");
                #is col name on table...
                if (mytempcls.areGivenColNamesOnTable([mcolnm], None)): pass;
                else:
                    raise ValueError("the col names were not found on the table class(" +
                                     mytempcls.__name__ + ")");
                mystr += "" + ctablename + "." + mcolnm;
                if (n + 1 < len(mcolnames)): mystr += ", ";
            return mystr;
        else: raise ValueError("the column names must be the same length as the table names!");

    #SQL methods might get removed from the validator class

    @classmethod
    def genUniqueConstraint(cls, consnm, colnames):
        #for multi-columns only
        #colnames are assumed to be on the table, because if they are not,
        #then SQL ERROR RESULTS IMMEDIATELY,
        #but this method may not take into account the correct table class as the caller
        #so cannot verify
        #
        #may be a problem if the calling class is not the table class...
        #may need to take the tablename in as a parameter
        if (myvalidator.isvaremptyornull(consnm)):
            return cls.genUniqueConstraint("unkmulcols" + cls.getTableName(), colnames);
        else: cls.stringMustContainOnlyAlnumCharsIncludingUnderscores(consnm, "the constraint name");
        if (myvalidator.isvaremptyornull(colnames) or len(colnames) < 2): return None;
        else:
            for mcnm in colnames:
                cls.stringMustContainOnlyAlnumCharsIncludingUnderscores(mcnm, "the colname");   
            return "CONSTRAINT " + consnm + " UNIQUE(" + (", ".join(colnames)) + ")";

    @classmethod
    def genCheckConstraint(cls, consnm, val):
        #may be a problem if the calling class is not the table class...
        #may need to take the tablename in as a parameter
        if (myvalidator.isvaremptyornull(consnm)):
            return cls.genUniqueConstraint("chkmulcols" + cls.getTableName(), val);
        else: cls.stringMustContainOnlyAlnumCharsIncludingUnderscores(consnm, "the constraint name");
        return "CONSTRAINT " + consnm + " CHECK(" + val + ")";

    @classmethod
    def genSQLimit(cls, num, offset=0):
        if (num == None or offset == None): raise ValueError("illegal number or offset used!");
        elif (type(num) == int and type(offset) == int): pass;
        else: raise ValueError("illegal number or offset used!");
        if (num < 1 or offset < 0): raise ValueError("illegal number or offset used!");
        return (f"LIMIT {num}" if (offset == 0) else f"LIMIT {num} OFFSET {offset}");

    @classmethod
    def genLengthCol(cls, colname, mtablename):
        myvalidator.varmustnotbeempty(colname, "colname");
        from mycol import mycol;#may need to change or get removed
        myclstablenameref = mycol.getClassFromTableName(mtablename);
        myvalidator.varmustnotbenull(myclstablenameref, "myclstablenameref");
        if (myclstablenameref.areGivenColNamesOnTable([colname], None)):
            return "LENGTH(" + colname + ")";
        else: raise ValueError("the colname must be on the table!");

    @classmethod
    def genGroupBy(cls, val):
        #GROUP BY(tablenamea.colnamea, tablenameb.colnameb ...);#GROUP BY(COUNT(CustomerID))
        myvalidator.varmustnotbeempty(val, "val");
        return "GROUP BY(" + val + ")";

    @classmethod
    def genBetween(cls, vala, valb):
        myvalidator.varmustnotbenull("vala", "vala");
        myvalidator.varmustnotbenull("valb", "valb");
        return f"BETWEEN {vala} AND {valb}";

    @classmethod
    def genOrderBy(cls, colnames, tablenames, singleinctname, sorder=None):
        #if sorder.length is less than colnames.length:
        #then add ASC or nothing at the end...
        #if sorder.length is greater than colnames.length: error
        myvalidator.varmustnotbeempty(colnames, "colnames");
        myvalidator.varmustnotbeempty(tablenames, "tablenames");
        myvalidator.varmustbeboolean(singleinctname, "singleinctname");
        basestr = "ORDER BY ";
        if (myvalidator.isvaremptyornull(sorder)):
            return basestr + cls.combineTableNamesWithColNames(colnames, tablenames, singleinctname);
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
            for n in range(len(colnames)):
                colnm = colnames[n];
                tnm = (tablenames[n] if (1 < len(tablenames)) else tablenames[0]);
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(colnm, "the colname");
                myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tnm, "the tablename");
                myclstablenameref = mycol.getClassFromTableName(tnm);
                myvalidator.varmustnotbenull(myclstablenameref, "myclstablenameref");
                if (myclstablenameref.areGivenColNamesOnTable([colnm], None)): pass;
                else: raise ValueError("the colname must be on the table!");
                
                #include the table name if not single,
                #include the table name if single and include is set to true
                inctnm = ((1 < len(tablenames)) or singleinctname);
                incval = (n < len(sorder));
                if (incval): myvalidator.varmustbeboolean(sorder[n], f"sorder[{n}]");
                mystr += "" + (tnm + "." if inctnm else "") + colnm;
                mystr += ((" ASC" if sorder[n] else " DESC") if incval else "");
                if (n + 1 < len(colnames)): mystr += ", ";
            return basestr + mystr;
    @classmethod
    def genSortOrderByAscVal(cls, numcols, boolval): return [boolval for n in range(numcols)];

    @classmethod
    def genSQLMinOrMax(cls, colname, tablename, singleinctname, usemin):
        myvalidator.varmustbeboolean(usemin, "usemin");
        myvalidator.varmustbeboolean(singleinctname, "singleinctname");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(colname, "colname");
        myvalidator.stringMustContainOnlyAlnumCharsIncludingUnderscores(tablename, "tablename");
        
        from mycol import mycol;#may need to change or get removed
        myclstablenameref = mycol.getClassFromTableName(tablename);
        myvalidator.varmustnotbenull(myclstablenameref, "myclstablenameref");
        if (myclstablenameref.areGivenColNamesOnTable([colname], None)): pass;
        else: raise ValueError("the colname must be on the table!");
        mystr = "M" + ("IN" if usemin else "AX") + "(" + (tablename + "." if singleinctname else "");
        mystr += "" + colname + ")";
        return mystr;
    @classmethod
    def genSQLMin(cls, colname, tablename, singleinctname):
        return cls.genSQLMinOrMax(colname, tablename, singleinctname, True);
    @classmethod
    def genSQLMax(cls, colname, tablename, singleinctname):
        return cls.genSQLMinOrMax(colname, tablename, singleinctname, False);
    
    @classmethod
    def genSQLSumOrAvg(cls, val, usedistinct, usesum):
        myvalidator.varmustbeboolean(usesum, "usesum");
        myvalidator.varmustbeboolean(usedistinct, "usedistinct");
        myvalidator.varmustbethetypeonly(val, str, "val");
        myvalidator.varmustnotbeempty(val, "val");
        return ("SUM" if usesum else "AVG") + "(" + ("DISTINCT " if usedistinct else "") + val + ")";
    @classmethod
    def genSQLSumOrAverage(cls, val, usedistinct, usesum):
        return cls.genSQLSumOrAvg(val, usedistinct, usesum);
    @classmethod
    def genSQLSum(cls, val, usedistinct): return cls.genSQLSumOrAvg(val, usedistinct, True);
    @classmethod
    def genSQLAvg(cls, val, usedistinct): return cls.genSQLSumOrAvg(val, usedistinct, False);

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

    @classmethod
    def genCustomSelect(cls, wtval, wrval, usedistinct=False):
        myvalidator.varmustbeboolean(usedistinct, "usedistinct");
        myvalidator.varmustbethetypeonly(wtval, str, "wtval");
        myvalidator.varmustbethetypeonly(wrval, str, "wrval");
        myvalidator.varmustnotbeempty(wtval, "wtval");
        myvalidator.varmustnotbeempty(wrval, "wrval");
        if ("COUNT(DISTINCT *)" in wtval):
            raise ValueError("INVALID SQL QUERY: \"SELECT DISTINCT *, " +
                                             "COUNT(DISTINCT *)\" IS NOT ALLOWED!");
        return "SELECT " + ("DISTINCT " if usedistinct else "") + wtval + " FROM " + wrval;
    
    @classmethod
    def genCount(cls, colnames, tablenames, inctnameonone=False, usedistinct=False):
        myvalidator.varmustbeboolean(inctnameonone, "inctnameonone");
        myvalidator.varmustbeboolean(usedistinct, "usedistinct");
        isonetable = False;
        if (myvalidator.isvaremptyornull(colnames)):
            if (myvalidator.isvaremptyornull(tablenames)):
                return "COUNT(" + ("DISTINCT " if usedistinct else "") + "*)";
            else: return cls.genCount(None, None, usedistinct);
        else:
            if (myvalidator.isvaremptyornull(tablenames)):
                raise ValueError("there must be at least one tablename if there is at least " +
                    "one colname, but there was not!");
            else:
                isonetable = (len(tablenames) == 1);
                if (len(colnames) == len(tablenames) or isonetable): pass;
                else:
                    raise ValueError("the number of the tablenames and columnnames must be the same!");
        #if there is more than one table, we need to include the tablename
        #if there is one table, we may still need it, we may not
        #for validation purposes either way we do need it.
        inctnm = (inctnameonone if isonetable else True);
        from mycol import mycol;#may need to change or get removed
        mystr = "";
        for n in range(len(colnames)):
            #need to verify that the col name is on the corresponding table
            mcnm = colnames[n];
            tnm = (tablenames[0] if isonetable else tablenames[n]);
            myvalidator.varmustnotbeempty(mcnm, "mcnm");
            myclstablenameref = mycol.getClassFromTableName(tnm);
            myvalidator.varmustnotbenull(myclstablenameref, "myclstablenameref");
            if (myclstablenameref.areGivenColNamesOnTable([mcnm], None)):
                mystr += "" + (tnm + "." if inctnm else "") + mcnm;
                if (n + 1 < len(colnames)): mystr += ", ";
            else: raise ValueError("the colname must be found on the table class(" +
                myclstablenameref.__name__ + ")");
        return "COUNT(" + ("DISTINCT " if usedistinct else "") + mystr + ")";
    @classmethod
    def genCountAll(cls, usedistinct=False): return cls.genCount(None, None, False, usedistinct);

    @classmethod
    def genSelectAllAndOrCountOnTables(cls, seltbles, cntcols, cnttables, useselonly=False,
        useseldistinct=False, usecntdistinct=False):
            myvalidator.varmustbeboolean(useselonly, "useselonly");
            myvalidator.varmustbeboolean(useseldistinct, "useseldistinct");
            myvalidator.varmustbeboolean(usecntdistinct, "usecntdistinct");
            if (useseldistinct == usecntdistinct):
                if (useselonly): pass;
                else:
                    if (useseldistinct):
                        if (myvalidator.isvaremptyornull(cntcols)):
                            raise ValueError("INVALID SQL QUERY: \"SELECT DISTINCT *, " +
                                             "COUNT(DISTINCT *)\" IS NOT ALLOWED!");
            myutnames = list(set(myvalidator.combineTwoLists(seltbles, cnttables)));
            mylenutnms = len(myutnames);
            inctname = (1 < mylenutnms);
            myvalidator.varmustnotbeempty(myutnames, "myutnames");
            mywtstr = "*";
            if (useselonly): pass;
            else: mywtstr += ", " + cls.genCount(cntcols, cnttables, inctname, usecntdistinct);
            wrval = ", ".join(myutnames);
            return cls.genCustomSelect(mywtstr, wrval, useseldistinct);
    @classmethod
    def genSelectAllAndCountOnTables(cls, seltbles, cntcols, cnttables, useseldistinct=False,
                                     usecntdistinct=False):
            return cls.genSelectAllAndOrCountOnTables(seltbles, cntcols, cnttables, False,
                                                      useseldistinct, usecntdistinct);
    @classmethod
    def genSelectAllAndCountAllOnTables(cls, seltbles, useseldistinct=False, usecntdistinct=False):
        return cls.genSelectAllAndCountOnTables(seltbles, None, None, useseldistinct, usecntdistinct);
    @classmethod
    def genSelectAllOnlyOnTables(cls, seltbles, useseldistinct=False):
        return cls.genSelectAllAndOrCountOnTables(seltbles, None, None, True, useseldistinct, False);
    
    @classmethod
    def genSelectSomeAndOrCountOnTables(cls, selcols, seltbles, cntcols, cnttables,
                                        useselonly=False, usecntonly=False, useseldistinct=False,
                                        usecntdistinct=False):
        myvalidator.varmustbeboolean(useselonly, "useselonly");
        myvalidator.varmustbeboolean(usecntonly, "usecntonly");
        myvalidator.varmustbeboolean(useseldistinct, "useseldistinct");
        myvalidator.varmustbeboolean(usecntdistinct, "usecntdistinct");
        if (useselonly == usecntonly):
            if (useselonly): raise ValueError("useselonly and usecntonly both cannot be true!");
        if (useseldistinct == usecntdistinct):
                if (useselonly): pass;
                else:
                    if (useseldistinct):
                        if (myvalidator.isvaremptyornull(cntcols)):
                            raise ValueError("INVALID SQL QUERY: \"SELECT DISTINCT *, " +
                                             "COUNT(DISTINCT *)\" IS NOT ALLOWED!");
    
        #if use select only: no counts
        #if use count only it will be inside of select statement still.
        #we will still need the seltables, and cntcols and cnttables...
        #SELECT DISTINCT? tnamea.colnamea, tnameb.colnameb ...,
        #COUNT(DISTINCT? tnamea.colnamea, tnameb.colnameb ...) FROM alluniquetnames
        myutnames = list(set(myvalidator.combineTwoLists(seltbles, cnttables)));
        mylenutnms = len(myutnames);
        inctname = (1 < mylenutnms);
        myvalidator.varmustnotbeempty(myutnames, "myutnames");
        wtval = "";
        wrval = "";
        if (useselonly):
            wtval = cls.combineTableNamesWithColNames(selcols, seltbles, inctname);
            wrval = ", ".join(seltbles);
        else:
            #either way we need the count here now...
            #either way the where is the combined list of unique table names...
            cntvalstr = cls.genCount(cntcols, cnttables, inctname, usecntdistinct);
            wrval = ", ".join(myutnames);
            if (usecntonly): wtval = cntvalstr;
            else:
                wtval = cls.combineTableNamesWithColNames(selcols, seltbles, inctname);
                wtval += ", " + cntvalstr;
        return cls.genCustomSelect(wtval, wrval, useseldistinct);

    @classmethod
    def genSelectCountOnlyOnTables(cls, seltbles, cntcols, cnttables, useseldistinct=False,
                                   usecntdistinct=False):
        return cls.genSelectSomeAndOrCountOnTables(None, seltbles, cntcols, cnttables,
                                        False, True, useseldistinct, usecntdistinct);
    @classmethod
    def genSelectSomeOnlyOnTables(cls, selcols, seltbles, useseldistinct=False):
        return cls.genSelectSomeAndOrCountOnTables(selcols, seltbles,
                                                   None, None, True, False, useseldistinct, False);

    @classmethod
    def genSQLIn(cls, mvals, incnull=False):
        myvalidator.varmustbeboolean(incnull, "incnull");
        for val in mvals:
            if (val == None): return cls.genSQLIn([oval for oval in mvals if not (oval == None)], True);
        return ("IN(NULL)" if (myvalidator.isvaremptyornull(mvals)) else "IN(" +
                ("NULL" + (", " if (0 < len(mvals)) else "")  if incnull else "") +
                (", ".join(mvals)) + ")");
    
    @classmethod
    def genWhereOrHaving(cls, mval, usewhere):
        myvalidator.varmustbeboolean(usewhere, "usewhere");
        myvalidator.varmustbethetypeonly(mval, str, "mval");
        myvalidator.varmustnotbeempty(mval, mval);
        #note: WHERE does not allow agragate functions where as HAVING does,
        #but this is not easily enforced because the mval may have it elsewhere...
        #so no validation other than type will be preformed and the error will propogate down to the DB.
        return ("WHERE " if usewhere else "HAVING ") + mval;
    @classmethod
    def genWhere(cls, mval): return cls.genWhereOrHaving(mval, True);
    @classmethod
    def genHaving(cls, mval): return cls.genWhereOrHaving(mval, False);

    #SQL-SWITCH-CASE statement looks like:
    #CASE
    #   WHEN condition1 THEN result1
    #   ...
    #   ELSE defaultresult
    #END;
    #note: NO TABS, and no newline between case and the first when.
    @classmethod
    def genSQLSwitchCase(cls, condsarr, resarr, defres=None, csnm=None):
        myvalidator.twoArraysMustBeTheSameSize(condsarr, resarr, "condsarr", "resarr");
        addfnwline = False;
        addtabs = False;
        mystr = "CASE" + ("\n" if addfnwline else " ");
        for n in range(len(condsarr)):
            ccond = condsarr[n];
            cres = resarr[n];
            myvalidator.varmustnotbeempty(ccond, "ccond");
            myvalidator.varmustnotbeempty(cres, "cres");
            if (addtabs): mystr += "\t";
            mystr += "WHEN " + ccond + " THEN " + cres  + "\n";
        if (addtabs): mystr += "\t";
        mystr += "ELSE " + ("NULL\n" if (myvalidator.isvaremptyornull(defres)) else "" + defres + "\n");
        mystr += "END" + ("" if (myvalidator.isvaremptyornull(csnm)) else " AS " + csnm) + "\n";
        return mystr;
    @classmethod
    def genSQLSwitchCaseWithName(cls, condsarr, resarr, csnm, defres=None):
        return cls.genSQLSwitchCase(condsarr, resarr, defres, csnm);
    @classmethod
    def genSQLSwitchCaseNoName(cls, condsarr, resarr, defres=None):
        return cls.genSQLSwitchCase(condsarr, resarr, defres, None);


    #https://www.w3schools.com/sql/sql_datatypes.asp
    #https://www.w3resource.com/sqlite/sqlite-data-types.php
    #https://www.w3resource.com/mysql/mysql-data-types.php
    #https://blog.devart.com/
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
    #
    #if using lite:
    #INTEGER AND REAL ARE 8 BYTES MAX (1byte=8bits,so 64bits, signed)
    #integer signed range: -9223372036854775808 to 9223372036854775807
    #integer unsigned range: 0 to 18446744073709551615 (2^64-1 absolute max of course).
    #real signed range: -3.402*10^38 to 3.402*10^38
    #TEXT max length: 2^31-1 bytes max
    #BLOB max size in bytes: 2^31-1 bytes max
    #return ["NULL", "REAL", "INTEGER", "TEXT", "BLOB"];
    #
    #if not using lite:
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
        myvalidator.varmustbeboolean(hasadefault, "hasadefault");
        myvalidator.varmustbeboolean(canspecifyrange, "canspecifyrange");
        #myvalidator.varmustbeanumber(minval, "minval");#can be a number or a string
        #myvalidator.varmustbeanumber(maxval, "maxval");#can be a number or a string
        myvalidator.varmustnotbeempty(name, "name");
        if (name.isalpha()): pass;
        else: raise ValueError("the paramname must be alphabetic, but it was not!");
        return {"paramname": name, "canspecifyrange": canspecifyrange, "hasadefault": hasadefault,
                "min": minval, "max": maxval, "defaultval": mdefval};
    @classmethod
    def genRangeDataDictNoRange(cls, name, hasadefault, mdefval):
        return cls.genRangeDataDict(name, False, hasadefault, None, None, mdefval);
    @classmethod
    def genRangeDataDictNoRangeNoDefault(cls, name):
        return cls.genRangeDataDictNoRange(name, False, None);
    @classmethod
    def genRangeDataDictNoDefault(cls, name, canspecifyrange, minval, maxval):
        return cls.genRangeDataDict(name, canspecifyrange, False, minval, maxval, None);

    #if type can be signed or unsigned
    #if type is some kind of value
    #the base type name
    #the parameter names if required
    #ranges on parameters if parameters are given or if range can be specified
    #can range on values be specified
    #range on the values if can be specified (just a max and a min)
    @classmethod
    def genTypeInfoDict(cls, names, isval, canbesignedornot, pnmsranges, valsranges):
        myvalidator.varmustbeboolean(isval, "isval");
        myvalidator.varmustbeboolean(canbesignedornot, "canbesignedornot");
        myvalidator.varmustnotbeempty(names, "names");
        for nm in names:
            myvalidator.varmustnotbeempty(nm, "nm");
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
        return {"names": names, "isvalue": isval, "canbesignedornot": canbesignedornot,
                "paramnameswithranges": pnmsranges, "valuesranges": valsranges};
    @classmethod
    def genValueTypeInfoDict(cls, names): return cls.genTypeInfoDict(names, True, False, [], []);
    @classmethod
    def genNonValueTypeInfoDict(cls, names, canbesignedornot, pnmsranges, valsranges):
        return cls.genTypeInfoDict(names, False, canbesignedornot, pnmsranges, valsranges);
    @classmethod
    def genNonNumNonValTypeInfoDict(cls, names, pnmsranges, valsranges):
        return cls.genNonValueTypeInfoDict(names, False, pnmsranges, valsranges);
    @classmethod
    def genNonNumNonValNoParamsTypeInfoDict(cls, names, valsranges):
        return cls.genNonValueTypeInfoDict(names, False, [], valsranges);

    #note: range or values is used as the default range name
    #note: length is used for the length allowed for either the values or of the values
    #note: for number types like integer:
    #signed or unsigned are names of the ranges indicating that the issigned parameter determines
    #which range is actually used, but not actually affecting this here.
    #note: for number types like real which is only signed we use the default instead
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

    #this method identifies all of the type names by variant that has
    #total number of digits and the number of digits after the decimal point
    @classmethod
    def getAllDataTypesThatHaveASetAmountOfDigitsAfterDecimalPoint(cls, varnm):
        #but not all floats on MYSQL one does one does not
        if (varnm == "SQLSERVER"): return ["DECIMAL", "NUMERIC"];
        elif (varnm == "MYSQL"): return ["DECIMAL", "DEC", "FLOAT", "DOUBLE", "DOUBLE PRECISION"];
        else: return [];

    #we need to know if something has a parameter that dictates the length and maybe which it is
    #
    #

    #we need to know when size as a parameter is length, and when it is not relevant
    #
    #

    #may want to make a method that determines the recommended
    #useunsigned and/or isnonnull values for a given type on the varient or if it is up to the user
    #
    #

    #begin date time methods section here...

    #also need date and time methods
    #need a method to generate the time string
    #to take a string and given format and extract the hours, minutes and seconds values
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
        myvalidator.varmustbeboolean(usefrltrs, "usefrltrs");
        if (usefrltrs): return myvalidator.getAllFourLetterAbbreviationsForMonthNames();
        else: return myvalidator.getAllThreeLetterAbbreviationsForMonthNames();

    @classmethod
    def getThreeOrFourLetterAbbreviationForMonthName(cls, mnthnm, usefrltrs):
        myvalidator.varmustbeboolean(usefrltrs, "usefrltrs");
        myvalidator.varmustbethetypeonly(mnthnm, str, "mnthnm");
        lwrmnthnm = mnthnm.lower();
        finmnthnm = lwrmnthnm[0].upper() + lwrmnthnm[1:];
        if (finmnthnm in myvalidator.getMonthNames()):
            if (len(finmnthnm) == 3): return finmnthnm;
            else: return finmnthnm[0: (4 if (usefrltrs) else 3)];
        else: raise ValueError("illegal month name used (" + mnthnm + ")");
    @classmethod
    def getThreeLetterAbbreviationForMonthName(cls, mnthnm):
        return cls.getThreeOrFourLetterAbbreviationForMonthName(mnthnm, False);
    @classmethod
    def getFourLetterAbbreviationForMonthName(cls, mnthnm):
        return cls.getThreeOrFourLetterAbbreviationForMonthName(mnthnm, True);

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
        myvalidator.varmustbethetypeonly(mnthnm, str, "mnthnm");
        lwrmnthnm = mnthnm.lower();
        finmnthnm = lwrmnthnm[0].upper() + lwrmnthnm[1:];
        mnthnms = myvalidator.getMonthNames();
        for n in range(len(mnthnms)):
            if (mnthnms[n] == finmnthnm): return n + 1;
        raise ValueError("illegal month name used (" + mnthnm + ")");

    @classmethod
    def getMonthNameFromNum(cls, mnthnum):
        myvalidator.valueMustBeInRange(mnthnum, 1, 12, True, True, "mnthnum");
        mnthnms = myvalidator.getMonthNames();
        return mnthnms[mnthnum - 1];

    @classmethod
    def getNumDaysInMonth(cls, mnthnum, islpyr):
        myvalidator.varmustbeboolean(islpyr, "islpyr");
        myvalidator.valueMustBeInRange(mnthnum, 1, 12, True, True, "mnthnum");
        #(30 days has (9)September, (4)April, (6)June, and (11)November, all the rest have 31 except
        #(2)Februrary which has 28 or 29 if leap year)
        if (mnthnum in [4, 6, 9, 11]): return 30;
        elif (mnthnum == 2): return (29 if islpyr else 28);
        else: return 31;

    @classmethod
    def addLeadingZeros(cls, val, numdgts):
        myvalidator.varmustbeanumber(val, "val");
        myvalidator.valueMustBeInRange(numdgts, 1, 0, True, False, "numdgts");
        if (val < 0): return "-" + cls.addLeadingZeros(-val, numdgts - 1);
        valstr = str(val);
        valstrlen = len(valstr);
        if (valstrlen < numdgts):
            mystr = "";
            for n in range(numdgts - valstrlen):
                mystr += "0";
            return mystr + valstr;
        elif (valstrlen == numdgts): return valstr;
        else:
            raise ValueError("the length of the numstr (" + str(valstrlen) + ") must be less than " +
                             "or equal to the number of digits (" + str(numdgts) +
                             "), but it was not!");

    #https://en.wikipedia.org/wiki/Leap_year
    @classmethod
    def isLeapYear(cls, yrnum):
        myvalidator.varmustbethetypeonly(yrnum, int, "yrnum");
        myvalidator.valueMustBeInRange(yrnum, 1, 0, True, False);
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
        myvalidator.varmustnotbenull(mdyrobj, "mdyrobj");
        return myvalidator.isValidDate(mdyrobj["monthnum"], mdyrobj["daynum"], mdyrobj["yearnum"]);
    @classmethod
    def isValidDateFromString(cls, datestr):
        mdyrobj = None;
        try:
            mdyrobj = myvalidator.getMonthDayYearFromDateString(datestr);
        except Exception as ex:
            #print(ex);
            return False;
        return myvalidator.isValidDateFromObj(mdyrobj);
    

    @classmethod
    def genDateString(cls, mnthnum, daynum, yrnum, usemthdyyr, usedshs):
        dysinmnth = myvalidator.getNumDaysInMonth(mnthnum, myvalidator.isLeapYear(yrnum));
        myvalidator.valueMustBeInRange(daynum, 1, dysinmnth, True, True, "daynum");
        myvalidator.valueMustBeInRange(yrnum, 1, 9999, True, True);#max may be wrong here
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
        myvalidator.varmustnotbenull(mdyrobj, "mdyrobj");
        return myvalidator.genDateString(mdyrobj["monthnum"], mdyrobj["daynum"], mdyrobj["yearnum"],
                                         (list(mdyrobj.keys())[0] == "monthnum"), usedshs);
    @classmethod
    def genDateStringUseMonthDayYear(cls, mnthnum, daynum, yrnum, usedshs):
        return cls.genDateString(mnthnum, daynum, yrnum, True, usedshs);
    @classmethod
    def genDateStringUseYearMonthDay(cls, mnthnum, daynum, yrnum, usedshs):
        return cls.genDateString(mnthnum, daynum, yrnum, False, usedshs);
    @classmethod
    def genDateStringUseSlashes(cls, mnthnum, daynum, yrnum, usemthdyyr):
        return cls.genDateString(mnthnum, daynum, yrnum, usemthdyyr, False);
    @classmethod
    def genDateStringUseDashes(cls, mnthnum, daynum, yrnum, usemthdyyr):
        return cls.genDateString(mnthnum, daynum, yrnum, usemthdyyr, True);
    
    @classmethod
    def getDelimeterIndexesForDateStrings(cls, usemthdyyr):
        #MM-DD-YYYY
        #YYYY-MM-DD
        #0123456789
        myvalidator.varmustbeboolean(usemthdyyr, "usemthdyyr");
        return ([2, 5] if (usemthdyyr) else [4, 7]);

    @classmethod
    def getMonthDayYearFromDateString(cls, datestr):
        myvalidator.stringMustHaveAtMinNumChars(datestr, 10, "datestr");
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
        myvalidator.varmustnotbenull(mobj, "mobj");
        if (myvalidator.isvaremptyornull(mobj["paramnameswithranges"])): return "";
        else:
            pnames = [pobj["paramname"] for pobj in mobj["paramnameswithranges"]];
            return "(" + (", ".join(pnames)) + ")";

    @classmethod
    def getValidSQLDataTypesFromInfoList(cls, mlist):
        if (mlist == None): return None;
        else:
            return [nm + cls.getParamNamesFromInfoListObj(mobj)
                    for mobj in mlist for nm in mobj["names"]];

    @classmethod
    def getDataTypesObjsWithNameFromList(cls, mlist, tpnm):
        if (mlist == None): return None;
        else: return [mobj for mobj in mlist for nm in mobj["names"] if (nm == tpnm)];

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
    def getParmsFromValType(cls, val):
        #params are everything after the first ( and the last )
        #everything else is ignored.
        #if value is not valid, then return empty or null
        #params can be inside ' or ", but ignore it if it is escaped
        #commas inside ' or " can be ignored, but others outside of that cannot be ignored.
        lvsobj = cls.getLevelsForValStr(val);
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
    #varstr is the sql variant string
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
                                #print("only perfect matchs in the form tpnm(max) are allowed with " +
                                #      "parentheis, perfect matchs that only have alphabetic " +
                                #      "characters A-Z and a-z only are allowed!");
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
                                psonval = ([] if ("(max)" in val) else cls.getParmsFromValType(val));
                                numpsonval = (0 if ("(max)" in val) else len(psonval));
                                tpobjslist = cls.getDataTypesObjsWithNameFromList(datatypesinfolist,
                                                                                  mynm);
                                print(f"mynm = {mynm}");
                                print(f"psonval = {psonval}");
                                print(f"numpsonval = {numpsonval}");
                                print(f"tpobjslist = {tpobjslist}");
                                
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
                                        if (tpobj["canbesignedornot"]):
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
                                            for valobj in tpobj["valuesranges"]:
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
                            #print("only perfect matchs in the form tpnm(max) are allowed with " +
                            #        "parentheis, perfect matchs that only have alphabetic " +
                            #        "characters A-Z and a-z only are allowed!");
                            return val.isalpha();
            return False;


    #BELOW METHODS ARE NOT DONE YET 3-12-2025 1:08 AM MST

    #tpnm is the SQL Data Type name for the specific variant specified by varstr
    #val is the value we are inserting into the column of that type...
    #useunsigned is for the signed or unsigned data range for numerical data types
    #-by default useunsigned is true because some data types non numerical ones are in fact unsigned.
    #-it is note worthy that some numerical data types are only signed or unsigned.
    #isnonnull is by default false to allow null as a value,
    #-however sometimes the user does not want null to be an option at all.
    #-Setting this to true ensures that.
    @classmethod
    def isValueValidForDataType(cls, tpnm, val, varstr, useunsigned=True, isnonnull=False):
        myvalidator.varmustbeboolean(isnonnull, "isnonnull");
        myvalidator.varmustbeboolean(useunsigned, "useunsigned");
        if (cls.isValidDataType(tpnm, varstr)): pass;
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
        print(f"tpnm = {tpnm}");
        print(f"varstr = {varstr}");
        print(f"val = {val}");
        print(f"nmhasps = {nmhasps}");
        print(f"bgnm = {bgnm}");
        print(f"mynm = {mynm}");
        print(f"isnonnull = {isnonnull}");
        print(f"useunsigned = {useunsigned}");
        
        
        # or not(nmhasps)
        psonval = ([] if ("(max)" in tpnm) else cls.getParmsFromValType(tpnm));
        numpsonval = (0 if ("(max)" in tpnm or not(nmhasps)) else len(psonval));
        print(f"psonval = {psonval}");
        print(f"numpsonval = {numpsonval}");
        
        tpobjslist = cls.getDataTypesObjsWithNameFromList(datatypesinfolist, mynm);
        print(f"tpobjslist = {tpobjslist}");
        print();

        if (myvalidator.isvaremptyornull(tpobjslist)): return True;

        tpnmswithfdptdgts = myvalidator.getAllDataTypesThatHaveASetAmountOfDigitsAfterDecimalPoint(
            varstr);
        print(f"tpnmswithfdptdgts = {tpnmswithfdptdgts}");

        for tobj in tpobjslist:
            print(f"tobj = {tobj}");
            print();

            if (myvalidator.isvaremptyornull(tobj["valuesranges"])):
                if (tobj["isvalue"]): return (val in tobj["names"]);
                else:
                    raise ValueError("the data type info object was built wrong for (" + mynm +
                                     ") for variant (" + varstr + ")!");
            else:
                getnext = False;
                twodiffranges = False;
                minrngval = 0;
                for vrobj in tobj["valuesranges"]:
                    print(f"vrobj = {vrobj}");
                    print();

                    isnumcomp = False;
                    valforcomp = val;
                    if (vrobj["paramname"] in ["length", "size"]):
                        #enforce the length restriction here...
                        #this may also come in as a required parameter
                        print("vr has length or size as a required parameter!");
                        
                        if (vrobj["canspecifyrange"]):
                            isnumcomp = True;
                            valforcomp = len(val);
                        else:
                            raise ValueError("the data type info object was built wrong for (" + mynm +
                                             ") for variant (" + varstr + ")!");
                
                    elif (vrobj["paramname"] in ["values", "range"]):
                        #paramname is something else like values or range
                        if (vrobj["hasadefault"]):
                            if (val == vrobj["defaultval"]):
                                if (val == "NULL"):
                                    if (isnonnull):
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
                                print("type is not number, but has a range.");
                                raise ValueError("NOT DONE YET 3-11-2025 5:22 PM MST!");
                
                    elif (vrobj["paramname"] in ["signed", "unsigned"]):
                        #need to know which one we are using signed or unsigned if it matches this
                        #then this will be the range we use else skip it.
                        #need to know if unsigned...
                        print(f"useunsigned = {useunsigned}");
                        
                        if ((useunsigned and (vrobj["paramname"] == "unsigned")) or
                            (not(useunsigned) and (vrobj["paramname"] == "signed"))):
                                #these are numerical comparisons
                                twodiffranges = True;
                                isnumcomp = True;
                                #valforcomp = val;
                    else:
                        #this is the this should not make it here case
                        #paramname is really specific to type and variant
                        print(f"vrobj['paramname'] = {vrobj['paramname']}");
                        print("this param name is really specific to the type and the range!");
                        raise ValueError("the parameters need to be handled, " +
                                         "but as of yet have not been!");
                    
                    print(f"isnumcomp = {isnumcomp}");
                    print(f"valforcomp = {valforcomp}");
                    
                    if (isnumcomp):
                        #these are numerical comparisons
                        if (myvalidator.isvaranumber(valforcomp)): pass;
                        else:
                            getnext = True;
                            break;
                        minrngval = vrobj["min"];
                        if (valforcomp < vrobj["min"] or vrobj["max"] < valforcomp):
                            #invalid, but the next one in the type object might be
                            #need to exit vrloop and need to move on to the next type object
                            print("value is not in the range, not the default, and not valid!");
                            getnext = True;
                            break;
                        else: print("value is in the range!");

                finpsonval = None;
                if (getnext): pass;
                else:
                    if (tobj["canbesignedornot"]):
                        print(f"twodiffranges = {twodiffranges}");
                        print(f"isnonnull = {isnonnull}");
                        print(f"useunsigned = {useunsigned}");
                        print(f"minrngval = {minrngval}");
                        #if not a number, then useunsigned must be true.
                        #if some kind of number:
                        #-if two different ranges is true, then we can for sure use unsigned
                        #-if one range, depends on what the minimum is if minimum is at least 0
                        #then this is unsigned otherwise, error if useunsigned is true.

                        if (isnonnull):
                            if (twodiffranges): pass;#useunsigned can be true or false in this case
                            else:
                                if (minrngval < 0):
                                    if (useunsigned): getnext = True;
                                else:
                                    if (useunsigned): pass;
                                    else: getnext = True;
                                #raise ValueError("NOT SURE ON THIS CASE HERE 3-14-2025 11 PM MST!");
                        else: getnext = True;

                        finpsonval = [];
                        for pval in psonval:
                            if (getnext): break;
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
                    else:
                        if (useunsigned): finpsonval = [pval for pval in psonval];
                        else: getnext = True;
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
                    
                    print();
                    print("now we need to check the type parameters!");
                    print();
                    print(f"val = {val}");
                    print(f"mynm = {mynm}");
                    print(f"tpnm = {tpnm}");
                    print(f"finpsonval = {finpsonval}");

                    if (myvalidator.isListAInListB(tobj["names"], tpnmswithfdptdgts) and
                        len(tobj["paramnameswithranges"]) == 2):
                            print("need to handle the total number of digits and the num digits " +
                                "after the decimal point here!");
                            
                            mdict = {};
                            for n in range(len(tobj["paramnameswithranges"])):
                                pnmobj = tobj["paramnameswithranges"][n];
                                print(f"pnmobj = {pnmobj}");
                                print();
                                
                                mdict[pnmobj["paramname"]] = finpsonval[n];
                            print(f"mdict = {mdict}");

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
                            print(f"szvld = {szvld}");
                            print(f"numdvld = {numdvld}");

                            if (szvld and numdvld): pass;#valid
                            else: getnext = True;
                    else:
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
                        
                        raise ValueError("NOT DONE YET 3-11-2025 5:22 PM MST!");
                
                    if (getnext): pass;
                    else: return True;

        #do something here...
        print("outside of the type objects loop!");
        return False;
