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

    #SQL methods might get removed from the validator class

    #pretty much all of these need the table name
    #it is my responsibility as the programmer to make sure that the columns are on the table
    #passing in the class refs instead will be a lot bigger, but will make the validation possible
    #otherwise... I need some sort of reverse look up way to get the table names or the classes
    #given one or the other... I already have a way to get the tablename from the classes of course.
    #what I do not have is a way to get the classname string or the class ref given the tablename.

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

    @classmethod
    def genSelectAllAndOrCountAllColsOnTable(cls, mtablename, countall=False):
        from mycol import mycol;#may need to change or get removed
        myvalidator.varmustnotbenull(mycol.getClassFromTableName(mtablename), "myclstablenameref");
        myvalidator.varmustbeboolean(countall, "countall");
        return "SELECT *" + (", COUNT(*)" if countall else "") + " FROM " + mtablename;
    @classmethod
    def genSelectAllAndCountAllColsOnTable(cls, mtablename):
        return cls.genSelectAllAndOrCountAllColsOnTable(mtablename, True);
    @classmethod
    def genSelectAllColsOnTableOnly(cls, mtablename):
        return cls.genSelectAllAndOrCountAllColsOnTable(mtablename, False);

    @classmethod
    def genSelectCountOnlyOnTable(cls, mtablename):
        from mycol import mycol;#may need to change or get removed
        myvalidator.varmustnotbenull(mycol.getClassFromTableName(mtablename), "myclstablenameref");
        return "SELECT COUNT(*) FROM " + mtablename;

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

    @classmethod
    def genSelectSomeColsFromTables(cls, mcolnames, mtablenames, countcols=None, counttnames=None):
        #SELECT tablenamea.colnamea, tablenameb.colnameb, ...,
        #COUNT(tablenamea.colnamea, ...) FROM alltablenames...
        #
        #if NO COUNT COLS, THEN REMOVE THAT PART FROM ABOVE.
        #if the count and select use only one table and it is the same, then do not it but in one place.
        #what if the count is from multiple tables, but the columns on the main select are only from 1?
        #what if the count is from one table, but the columns on the main select are from multiple?
        #-we still need all of the table names if multiple are present.
        print(f"mcolnames = {mcolnames}");
        print(f"mtablenames = {mtablenames}");
        print(f"countcols = {countcols}");
        print(f"counttnames = {counttnames}");
        
        myvalidator.varmustnotbeempty(mcolnames, "mcolnames");
        myvalidator.varmustnotbeempty(mtablenames, "mtablenames");
        nocounts = myvalidator.isvaremptyornull(countcols);
        #singleinctname = True;
        if (nocounts):
            if (myvalidator.isvaremptyornull(counttnames)): pass;
            else:
                raise ValueError("countcols and counttnames must be the same size, but they were not!");
        else:
            if (myvalidator.isvaremptyornull(counttnames)):
                raise ValueError("countcols and counttnames must be the same size, but they were not!");
            else:
                #both countcols and counttnames are not empty
                #if there is only one counttname and only one table on the select then do not need it
                #otherwise they need to be the same length...
                dolencheck = True;
                if ((len(counttnames) == 1) and (len(mtablenames) == 1)
                    and (counttnames[0] == mtablenames[0])):
                        #singleinctname = False;
                        dolencheck = False;
                if (dolencheck):
                    if (len(counttnames) == len(countcols)): pass;
                    else:
                        raise ValueError("countcols and counttnames must be the same size, but " +
                                         "they were not!");
        isonetable = (len(mtablenames) == 1);
        print(f"nocounts = {nocounts}");
        print(f"isonetable = {isonetable}");
        #print(f"singleinctname = {singleinctname}");

        from mybase import mybase;#may also need to move this method...
        alluniquetablenames = list(set(mybase.combineTwoLists(mtablenames, counttnames)));
        print(f"alluniquetablenames = {alluniquetablenames}");

        ismorethanonetable = (1 < len(alluniquetablenames));
        print(f"ismorethanonetable = {ismorethanonetable}");

        mystr = "SELECT " + cls.combineTableNamesWithColNames(mcolnames, mtablenames,
                                                              ismorethanonetable);
        if nocounts: pass;
        else:
            mystr += ", COUNT(" + cls.combineTableNamesWithColNames(countcols, counttnames,
                                                                    ismorethanonetable) + ")";
        mystr += " FROM " + (", ".join(alluniquetablenames));
        print(f"mystr = {mystr}");

        return mystr;
