#generate documentation for a program
#get the name of the class
#class to the :
#and then get the functions inside of the class
#every function starts with the word def
#get the comments above it then move on
#if commented move on only include functions that are not commented out
#only include classes that are not commented out
#the documentation will be saved inside of a file
#this will take in a file and do this for every file it is given...
from myorm.myvalidator import myvalidator;
import sys;
import time;
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

def addLeadingSpacesToNum(n, mxlen):
    numstr = str(n);
    if (len(numstr) < mxlen):
        finstr = "";
        for n in range(mxlen - len(numstr)): finstr += " ";
        return finstr + numstr;
    else: return "" + numstr;

def getFirstExecutableCharacterObjOnALine(mline):
    if (mline == None or len(mline) < 1): return {"fec": None, "si": -1};
    else:
        for i in range(len(mline)):
            if (mline[i] in [' ', '\t', '\n']): pass;
            else: return {"fec": "" + mline[i], "si": i};
        return {"fec": None, "si": -1};

def genInfoLines(fnm, noext=True):
    mflines = getLinesFromFile(fnm, noext=noext);
    csi = -1;
    lastmci = -1;
    myfinlines = [];
    mxlen = len(str(len(mflines)));
    pmerrmsg = "the line with the class def must have a starting parenthesis on it if it has an ";
    pmerrmsg += "ending parenthesis on it!";
    pclnerrmsg = "the class line must either have a parenthesis or a : on it, but it did not!";
    getnext = False;
    for n in range(len(mflines)):
        mline = "" + mflines[n];
        print(addLeadingSpacesToNum(n, mxlen) + ": " + mline);

        fecobj = getFirstExecutableCharacterObjOnALine(mline);
        fec = fecobj["fec"];
        fecsi = fecobj["si"];
        mylen = len(mline);
        #print(f"fecobj = {fecobj} mylen = {mylen}");
        ismthorcls = False;
        if (fec == None): csi = -1;
        elif (fec in ['@', '#']):
            #keep this comment or some decorator call
            if (csi < 0 or len(mflines) - 1 < csi): csi = n;
        elif (fec == 'd'):
            #keep this maybe def
            #print(mline[fecsi:fecsi+4]);
            if ((fecsi + 4 < mylen) and mline[fecsi:fecsi+4] == 'def '):
                #this is a def line
                #i think we want this part of it to the end of the line and the comments
                #on the lines immediately above it if possible.
                print(f"def csi = {csi} and n = {n}");
                if (csi == 0 or 0 < csi < len(mflines)):
                    #adds a line before comments start for a method
                    #if the previous line is empty or null, do not add another one
                    #we only want to add it for comments not the ats...
                    #with diff is 1, it will be for all one liner methods
                    #diff more than 1, implies it must have comments
                    #1 < n - csi and 
                    fstlinefecobj = getFirstExecutableCharacterObjOnALine(mflines[csi]);
                    #print(fstlinefecobj);
                    if (fstlinefecobj["fec"] == '#' and 0 < len(myfinlines) and
                        not myvalidator.isvaremptyornull(myfinlines[len(myfinlines) - 1])):
                        myfinlines.append("");
                    for myn in range(csi, n): myfinlines.append("" + mflines[myn]);
                #now we add our class or method definition line here, but we need the complete
                #definition. That means we need the ): for defs and the : or ): for classes
                #what if it does not end with that? This cannot be inside of a string...
                myfinlines.append("" + mline);
                lastmci = n;
                ismthorcls = True;
            elif (getnext): pass;
            else: csi = -1;
        elif (fec == 'c'):
            #keep this maybe class
            #print(mline[fecsi:fecsi+6]);
            #print(len(mline[fecsi:fecsi+6]));
            if ((fecsi + 6 < mylen) and mline[fecsi:fecsi+6] == 'class '):
                #this is a class line
                #i think we want this part of it to the end of the line and the comments
                #on the lines immediately above it if possible.
                print(f"class csi = {csi} and n = {n}");
                if (csi == 0 or 0 < csi < len(mflines)):
                    #myfinlines.append("");#adds a line before comments start for a class
                    for omyn in range(csi, n): myfinlines.append("" + mflines[omyn]);
                #now we add our class or method definition line here, but we need the complete
                #definition. That means we need the ): for defs and the : or ): for classes
                #what if it does not end with that? This cannot be inside of a string...
                myfinlines.append("" + mline);
                #lastmci = n;
                ismthorcls = True;
            elif (getnext): pass;
            else: csi = -1;
        elif (getnext): pass;
        else: csi = -1;

        if (getnext):
            #add the line then check to see if we want to get the next one...
            myfinlines.append("" + mline);
            hascmntonit = ("#" in mline);
            hasepclnonit = ("):" in mline);
            epclni = (mline.index("):") if hasepclnonit else -1);
            if (hascmntonit):
                cmnti = mline.index("#");
                if (epclni < cmnti and hasepclnonit): getnext = False;
                #else: pass;
            elif (hasepclnonit): getnext = False;
            #if (getnext): pass;
            #else: myfinlines.append("");#adds a new line after multiline method or class names
        
        if (ismthorcls):
            hasasponit = ("(" in mline);
            hasaeponit = (")" in mline);
            hascmntonit = ("#" in mline);
            hasepclnonit = ("):" in mline);
            hasclnonit = (":" in mline);
            getnext = False;
            if (hasaeponit and not hasasponit): raise ValueError(pmerrmsg);
        
            if (hasasponit or hasepclnonit):
                #this extends multiple classes probably,
                #but if it has a comment and if that comment starts before the parenthesis, then no.
                spi = mline.index("(");
                #epi = (mline.index(")") if hasaeponit else -1);
                epclni = (mline.index("):") if hasepclnonit else -1);
                if (hascmntonit):
                    cmnti = mline.index("#");
                    if (spi < epclni < cmnti): getnext = False;#keep the line no need to get another
                    elif (spi < cmnti): getnext = True;#need to get the next one
                    elif (cmnti < spi): getnext = False;#keep the line no need to get another
                    #else: pass;#keep the line no need to get another
                else:
                    if (spi < epclni): getnext = False;
                    else: getnext = True;#need to get the next line
            elif (hasclnonit): getnext = False;
            else: raise ValueError(pclnerrmsg);
            if (getnext): pass;
            else: 
                #myfinlines.append("");#adds a new line after oneliner methods
                csi = -1;
            ismthorcls = False;
    
        #wait some time for the printer to catch up...
        if (n % 1000 == 0 and 0 < n): time.sleep(1/8);
    return myfinlines;

if __name__ == '__main__':
    if (len(sys.argv) < 2): raise ValueError("you need to enter a file name with no extension!");
    fnm = "" + sys.argv[1];
    print(f"fnm = sys.argv[1] = {fnm}.py");
    
    finlines = genInfoLines(fnm, noext=True);
    
    print("\nthe doc lines are: ");
    for n in range(len(finlines)):
        print(finlines[n]);
        #wait some time for the printer to catch up...
        if (n % 1000 == 0 and 0 < n): time.sleep(1/8);
    print("\nend of doc lines!");
    
    #need to safe the file or format the information in a way that it can be saved and displayed to
    #a documentation website
    raise ValueError("NOT DONE YET WITH THE DOCUMENTOR PROGRAM 11-15-2025 1:17 AM MST!");
