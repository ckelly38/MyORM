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
        if (myvalidator.isvaremptyornull(sorder)):
            return "ORDER BY " + cls.combineTableNamesWithColNames(colnames, tablenames, singleinctname);
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
            return "ORDER BY " + mystr;
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
    #if not using lite:
    #MYSQL:
    #
    #CHAR(size) size 0 to 255 inclusive default is 1.
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
    #note: due to size being deprecated ZEROFILL has also been sort of deprecated.
    #note: if you want something to be UNSIGNED you need to include UNSIGNED else it will be signed.
    #note: unsigned FLOAT will be depricated due to data storage requirements and
    #it being an integer.
    #note: FLOAT(size, d) is deprecated due to size being deprecated.
    #
    #BIT(size) size can be from 1 to 64 inclusive. 64 bit processor.
    #TINYINT(size) signed is from -127 to 128 inclusive unsigned 0 to 255 inclusive.
    # size maximum display width for the maximum number which is 255 (so max size is 3).
    #BOOL, BOOLEAN zero is false, everything else is true.
    #SMALLINT(size) signed is from -32767 to 32768 inclusive; unsigned is from 0 to 65535
    # size maximum display width which is 5 digits for 65535.
    #MEDIUMINT(size) signed is from -8388608 to 8388607 unsigned is from 0 to 16777215.
    #INTEGER(size), INT(size) signed is from -2147483648 to 2147483647
    # unsigned is from 0 to 4294967295.
    #BIGINT(size) signed is from -9223372036854775808 to 9223372036854775807
    # unsigned is from 0 to 18446744073709551615. (2^64-1 is absolute max of course).
    #
    #IT IS ALSO STRONGLY SUGGESTED TO USE BELOW WITHOUT PARAMETERS.
    #
    #FLOAT(size, d), DOUBLE(size, d), DOUBLE PRECISION(size, d) are deprecated where
    # size is the number of digits, d is the number of digits after the decmial point.
    #
    #FLOAT(p) where p is the precision in bits if p is 0 to 24 FLOAT else 25 to 53 DOUBLE.
    #DOUBLE(size, d), DOUBLE PRECISION(size, d) is deprecated where size is the
    # total number of digits, d is the number of digits after the decmial point, same as a float.
    #DECIMAL(size, d), DEC(size, d) size is the total number of digits,
    # d is the number of digits after the decmial point, same as a float.
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
    #DECIMAL(p, s) p is the total number of digits like size,
    # and s is the number of digits after the decimal point.
    #p must be from 1 to 38 inclusive. s default is 0, p default is 18.
    #for fixed precision and scale numbers.
    #
    #note: 2^64-1 =                                      18,446,744,073,709,551,615
    #note: python can store 10^38. pow(10, 38) - 1 is how I got it or 10**38 - 1 will also work.
    #
    #range is -10^38, 10^38-1: -100,000,000,000,000,000,000,000,000,000,000,000,000
    #                            99,999,999,999,999,999,999,999,999,999,999,999,999
    #                              ^           ^           ^           ^
    #NUMERIC(p, s) is the same as DECIMAL(p, s).
    #SMALLMONEY allows integers between -214748.3648 to 214748.3647 inclusive.
    #MONEY allows integers between -922337203685477.5808 and 922337203685477.5807 inclusive.
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
                    "BIGINT", "DECIMAL(p, s)", "NUMERIC(p, s)", "SMALLMONEY", "MONEY", "FLOAT(p)",
                    "REAL", "DATETIME", "DATETIME2", "SMALLDATETIME", "DATE", "TIME", "DATETIMEOFFSET",
                    "TIMESTAMP", "SQL_VARIANT", "UNIQUEIDENTIFIER", "XML", "CURSOR", "TABLE"];
        else: return [];

    #BELOW METHODS ARE NOT DONE YET 3-6-2025 1:41 AM MST

    #p, s -> ?;
    #what if no range can be specified, but we have a name
    #add default values for the parameter (if they have one)
    #what if they do not have any default values?
    #I guess we need a parameter that says if they have a default value or not.
    #paramobj: paramname
    #canspecifyrange: val
    #maxval: max
    #minval: min    
    @classmethod
    def genRangeDataDict(cls, name, canspecifyrange, minval, maxval):
        myvalidator.varmustbeboolean(canspecifyrange, "canspecifyrange");
        myvalidator.varmustbeanumber(minval, "minval");
        myvalidator.varmustbeanumber(maxval, "maxval");
        myvalidator.varmustnotbeempty(name, "name");
        if (name.isalpha()): pass;
        else: raise ValueError("the paramname must be alphabetic, but it was not!");
        return {"paramname": name, "canspecifyrange": canspecifyrange, "min": minval, "max": maxval};

    #if type can be signed or unsigned
    #if type is some kind of value
    #the base type name
    #the parameter names if required
    #ranges on parameters if parameters are given or if range can be specified
    #can range on values be specified
    #range on the values if can be specified (just a max and a min)
    @classmethod
    def genTypeInfoDict(cls, name, isval, canbesignedornot, pnmsranges, valsranges):
        myvalidator.varmustbeboolean(isval, "isval");
        myvalidator.varmustbeboolean(canbesignedornot, "canbesignedornot");
        myvalidator.varmustnotbeempty(name, "name");
        if (name.isalpha()): pass;
        else: raise ValueError("the typename must be alphabetic, but it was not!");
        return {"name": name, "isvalue": isval, "canbesignedornot": canbesignedornot,
                "paramnameswithranges": pnmsranges, "valuesranges": valsranges};
    @classmethod
    def genValueTypeInfoDict(cls, name): return cls.genTypeInfoDict(name, True, False, [], []);
    @classmethod
    def genNonValueTypeInfoDict(cls, name, canbesignedornot, pnmsranges, valsranges):
        return cls.genTypeInfoDict(name, False, canbesignedornot, pnmsranges, valsranges);
    @classmethod
    def genNonNumNonValTypeInfoDict(cls, name, pnmsranges, valsranges):
        return cls.genNonValueTypeInfoDict(cls, name, False, pnmsranges, valsranges);
    @classmethod
    def genNonNumNonValNoParamsTypeInfoDict(cls, name, valsranges):
        return cls.genNonValueTypeInfoDict(cls, name, False, [], valsranges);

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
        if (varstr == "LITE"):
            ltrlmag = 3.402*(10**38);#plus or mins this for real
            ltintmag = 9223372036854775808;#plus or minus this for int max - 1 from this
            mxbts = (2**31) - 1;#max TEXT length and BLOB size in bytes 
            return [ myvalidator.genValueTypeInfoDict("NULL"),
                    myvalidator.genNonValueTypeInfoDict("REAL", True, [], [
                        myvalidator.genRangeDataDict("range", True, -1*ltrlmag, ltrlmag)]),
                    myvalidator.genNonValueTypeInfoDict("INTEGER", True, [], [
                        myvalidator.genRangeDataDict("signed", True, -1*ltintmag, ltintmag - 1),
                        myvalidator.genRangeDataDict("unsigned", True, 0, 18446744073709551615)]),
                    myvalidator.genNonNumNonValTypeInfoDict("TEXT", [], [
                        myvalidator.genRangeDataDict("length", True, 0, mxbts)]),
                    myvalidator.genNonNumNonValTypeInfoDict("BLOB", [], [
                        myvalidator.genRangeDataDict("length", True, 0, mxbts)])];
            #return ["NULL", "REAL", "INTEGER", "TEXT", "BLOB"];
        elif (varstr == "MYSQL"):
            return ["CHAR(size)", "VARCHAR(size)", "BINARY(size)", "VARBINARY(size)", "TINYBLOB",
                    "TINYTEXT", "TEXT(size)", "BLOB(size)", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT",
                    "LONGBLOB", "ENUM(values)", "SET(values)", "BIT(size)", "TINYINT(size)",
                    "BOOL", "BOOLEAN", "SMALLINT(size)", "MEDIUMINT(size)",
                    "INTEGER(size)", "INT(size)", "BIGINT(size)", "FLOAT(size, d)", "FLOAT(p)",
                    "DOUBLE(size, d)", "DOUBLE PRECISION(size, d)", "DECIMAL(size, d)", "DEC(size, d)",
                    "FLOAT", "DOUBLE PRECISION", "DOUBLE", "DATE", "DATETIME(fsp)", "TIMESTAMP(fsp)",
                    "TIME(fsp)", "YEAR", "DATETIME", "TIMESTAMP", "TIME"];

            #return ["CHAR(size)", "VARCHAR(size)", "BINARY(size)", "VARBINARY(size)", "TINYBLOB",
            #        "TINYTEXT", "TEXT(size)", "BLOB(size)", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT",
            #        "LONGBLOB", "ENUM(values)", "SET(values)", "BIT(size)", "TINYINT(size)",
            #        "BOOL", "BOOLEAN", "SMALLINT(size)", "MEDIUMINT(size)",
            #        "INTEGER(size)", "INT(size)", "BIGINT(size)", "FLOAT(size, d)", "FLOAT(p)",
            #        "DOUBLE(size, d)", "DOUBLE PRECISION(size, d)", "DECIMAL(size, d)", "DEC(size, d)",
            #        "FLOAT", "DOUBLE PRECISION", "DOUBLE", "DATE", "DATETIME(fsp)", "TIMESTAMP(fsp)",
            #        "TIME(fsp)", "YEAR", "DATETIME", "TIMESTAMP", "TIME"];
        elif (varstr == "SQLSERVER"):
            return ["CHAR(n)", "VARCHAR(n)", "VARCHAR(max)", "NCHAR(n)", "NVARCHAR(n)", "NVARCHAR(max)",
                    "BINARY(n)", "VARBINARY(n)", "VARBINARY(max)", "BIT", "TINYINT", "SMALLINT", "INT",
                    "BIGINT", "DECIMAL(p, s)", "NUMERIC(p, s)", "SMALLMONEY", "MONEY", "FLOAT(p)",
                    "REAL", "DATETIME", "DATETIME2", "SMALLDATETIME", "DATE", "TIME", "DATETIMEOFFSET",
                    "TIMESTAMP", "SQL_VARIANT", "UNIQUEIDENTIFIER", "XML", "CURSOR", "TABLE"];

            #return ["CHAR(n)", "VARCHAR(n)", "VARCHAR(max)", "NCHAR(n)", "NVARCHAR(n)", "NVARCHAR(max)",
            #        "BINARY(n)", "VARBINARY(n)", "VARBINARY(max)", "BIT", "TINYINT", "SMALLINT", "INT",
            #        "BIGINT", "DECIMAL(p, s)", "NUMERIC(p, s)", "SMALLMONEY", "MONEY", "FLOAT(p)",
            #        "REAL", "DATETIME", "DATETIME2", "SMALLDATETIME", "DATE", "TIME", "DATETIMEOFFSET",
            #        "TIMESTAMP", "SQL_VARIANT", "UNIQUEIDENTIFIER", "XML", "CURSOR", "TABLE"];
        else: return [];

    @classmethod
    def isValidDataType(cls, val, varstr):
        #get data types for the specific variant
        #if the list is empty or null, then assumed valid
        #if on the list, valid
        #if not on the list and list is not empty, then not valid.
        print(f"val = {val}");
        print(f"varstr = {varstr}");

        mvtpslist = myvalidator.getValidSQLDataTypes(varstr);
        if (myvalidator.isvaremptyornull(mvtpslist)): return True;
        else:
            valnmhasps = ("(" in val and ")" in val);
            valnmhascma = ("," in val);
            print(f"valnmhasps = {valnmhasps}");
            print(f"valnmhascma = {valnmhascma}");
            
            valfpi = (val.index("(") if valnmhasps else -1);
            if (valnmhasps):
                valfinpi = val.rindex(")");
                if (valnmhascma):
                    valbgcmai = val.index(",");
                    valfincmai = val.rindex(",");
                    print(f"valfpi = {valfpi}");
                    print(f"valbgcmai = {valbgcmai}");
                    print(f"valfincmai = {valfincmai}");
                    print(f"valfinpi = {valfinpi}");

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
            print(f"valbgnm = {valbgnm}");

            for mtp in mvtpslist:
                nmhasps = ("(" in mtp and ")" in mtp);
                print(f"mtp = {mtp}");
                print(f"nmhasps = {nmhasps}");

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
                        print(f"bgpindx = {bgpindx}");

                        bgnm = mtp[0:bgpindx];
                        print(f"bgnm = {bgnm}");

                        if (valbgnm == bgnm):
                            #it can be a perfect match and not be valid
                            #the only perfect matchs accepted are if no parenthesis,
                            #or with tpnm(max) only
                            if (val == mtp):
                                print("found our perfect match!");
                                print("only perfect matchs in the form tpnm(max) are allowed with " +
                                      "parentheis, perfect matchs that only have alphabetic " +
                                      "characters A-Z and a-z only are allowed!");
                                return (valbgnm + "(max)" == val) and (bgnm + "(max)" == mtp);
                            else:
                                #need to know if unsigned...
                                #need to get the ranges for those types on those numbers...
                                #need to verify the ranges on the numbers for those data types...
                                raise ValueError("NOT DONE YET 3-5-2025 10 PM MST...");
                    else:
                        #comma in name, but no parenthesis has already been handled.
                        #name must be alphabetic only for a perfect match without parenthesis
                        #to be valid.
                        if (val == mtp):
                            print("found our perfect match!");
                            print("only perfect matchs in the form tpnm(max) are allowed with " +
                                    "parentheis, perfect matchs that only have alphabetic " +
                                    "characters A-Z and a-z only are allowed!");
                            return (val.isalpha());
            return False;
