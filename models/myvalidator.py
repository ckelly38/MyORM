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
    @classmethod
    def getValidSQLDataTypes(cls):
        #if using lite:
        #INTEGER AND REAL ARE 8 BYTES MAX (1byte=8bits,so 64bits, signed)
        #return ["NULL", "REAL", "INTEGER", "TEXT", "BLOB"];
        #if not using lite:
        #MYSQL:
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
        #ENUM(values...) you can have 65,535 values and they map to an integer index,
        # you can either use that or the given values in the ENUM.
        # If a value not on the list is entered then a blank value will be inserted.
        #SET(values...) you can have 0 up to 64 values.
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
        #FLOAT(size, d) deprecated size is the number of digits,
        # d is the number of digits after the decmial point.
        #
        #FLOAT(p) where p is the precision in bits if p is 0 to 24 FLOAT else 25 to 53 DOUBLE.
        #DOUBLE(size, d) ?
        #DOUBLE PRECISION(size, d) ?
        #DECIMAL(size, d), DEC(size, d) ?
        #?
        #?
        #?
        #?
        #?
        #?
        #return ["CHAR(size)", "VARCHAR(size)", "BINARY(size)", "VARBINARY(size)", "TINYBLOB",
        # "TINYTEXT", "TEXT(size)", "BLOB(size)", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT", "LONGBLOB",
        # "ENUM(values...)", "SET(values...)", "BIT(size)", "TINYINT(size)", "BOOL", "BOOLEAN",
        # "SMALLINT(size)", "MEDIUMINT(size)", "INTEGER(size)", "INT(size)", "BIGINT(size)",
        # "FLOAT(size, d)", "FLOAT(p)", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?"];
        #?:
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
        #?:
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
        #?:
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
        pass;
