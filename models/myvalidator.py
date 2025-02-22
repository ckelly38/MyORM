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
    def stringContainsOnlyAlnumCharsIncludingUnderscores(cls, mstr):
        if (cls.isvaremptyornull(mstr)): return True;
        else:
            cls.varmustbethetypeonly(mstr, str, "mstr");
            for c in mstr:
                if (c.isalnum() or c == '_'): pass;
                else: return False;
        return True;


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
        else:
            if (cls.stringContainsOnlyAlnumCharsIncludingUnderscores(consnm)): pass;
            else: raise ValueError("the constraint name must contain alpha-numeric characters only!");
        if (myvalidator.isvaremptyornull(colnames) or len(colnames) < 2): return None;
        else:
            for mcnm in colnames:
                if (cls.stringContainsOnlyAlnumCharsIncludingUnderscores(mcnm)): pass;
                else: raise ValueError("the colname must contain alpha-numeric characters only!");   
            return "CONSTRAINT " + consnm + " UNIQUE(" + (", ".join(colnames)) + ")";

    @classmethod
    def genCheckConstraint(cls, consnm, val):
        #may be a problem if the calling class is not the table class...
        #may need to take the tablename in as a parameter
        if (myvalidator.isvaremptyornull(consnm)):
            return cls.genUniqueConstraint("chkmulcols" + cls.getTableName(), val);
        else:
            if (cls.stringContainsOnlyAlnumCharsIncludingUnderscores(consnm)): pass;
            else: raise ValueError("the constraint name must contain alpha-numeric characters only!");
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
        #GROUP BY(tablenamea.colnamea, tablenameb.colnameb ...);
        #GROUP BY(COUNT(CustomerID))
        myvalidator.varmustnotbeempty(val, "val");
        return "GROUP BY(" + val + ")";

    @classmethod
    def genBetween(cls, vala, valb):
        myvalidator.varmustnotbenull("vala", "vala");
        myvalidator.varmustnotbenull("valb", "valb");
        return f"BETWEEN {vala} AND {valb}";

    
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
        return "SELECT " ("DISTINCT " if usedistinct else "") + wtval + " FROM " + wrval;
    
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
            from mybase import mybase;#may need to change or get removed
            myutnames = list(set(mybase.combineTwoLists(seltbles, cnttables)));
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

        #if use select only: no counts
        #if use count only it will be inside of select statement still.
        #we will still need the seltables, and cntcols and cnttables...
        #SELECT DISTINCT? tnamea.colnamea, tnameb.colnameb ...,
        #COUNT(DISTINCT? tnamea.colnamea, tnameb.colnameb ...) FROM alluniquetnames
        from mybase import mybase;#may need to change or get removed
        myutnames = list(set(mybase.combineTwoLists(seltbles, cnttables)));
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
