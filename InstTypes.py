
class InstTypes(object):
    def __init__(self, **input):

        self.result = None
        
        self.source1RegValue = None 
        self.source2RegValue = None
        self.values = {
                       'op': None,
                       'dest': None,
                       's1': None,
                       's2': None,
                       'immed': None,
                       'target': None
        }
        self.controls = {'aluop'   : None,
                         'regRead' : None,
                         'regWrite': None,
                         'readMem' : None,
                         'writeMem': None, }

        for key in input:

            if key in self.values.keys():

                self.values[key] = input[key]
            else:

                self.controls[key] = input[key]

    @property
    def op(self):
        return self.values['op']
    
    @property
    def dest(self):

        return self.values['dest']
    
    @property
    def s1(self):

        return self.values['s1']
    
    @property
    def s2(self):

        return self.values['s2']
    
    @property
    def immed(self):

        return self.values['immed']
    
    @property
    def target(self):

        return self.values['target']
    
    @property
    def aluop(self):

        return self.controls['aluop']
    
    @property
    def regRead(self):

        return self.controls['regRead']
    
    @property
    def regWrite(self):

        return self.controls['regWrite']
    
    @property
    def readMem(self):

        return self.controls['readMem']
    
    @property
    def writeMem(self):

        return self.controls['writeMem']
    
    
    def __str__(self):
        str = "%s\t%s %s %s %s %s" % (self.values['op'],
                                  self.values['dest'] if self.values['dest'] else "",
                                  self.values['s1'] if self.values['s1'] else "",
                                  self.values['s2'] if self.values['s2'] else "",
                                  self.values['immed'] if self.values['immed'] else "",
                                  self.values['target'] if self.values['target'] else "")
        return str
    
    def __repr__(self):
        return repr(self.values)
        
class Nop(InstTypes):
    pass
#nop singleton
Nop = Nop()

class InstructionParser(object):
    def __init__(self):

        self.labelAddress = {}


        self.instructionSet = {
                 'rtype': ['dadd', 'dsub', 'dmul', 'add.d', 'sub.d','mul.d', 'div.d', 'and', 'or'],
                 'itype': ['daddi', 'dsubi', 'andi', 'ori', 'beq', 'bne', 'lw', 'sq', 'l.d', 's.d'],
                 'jtype': ['j']
        }


    def parseFile(self, filename):
        with open(filename) as f:
            data = list(filter((lambda x: x != '\n' and not x.startswith('#')), f.readlines()))

            instructions = [self.parse(a.replace(',',' ').lower()) for a in data]
            return instructions

    def parseConfigFile(self,filename):

        with open(filename) as f:
            data = list(filter((lambda x: x != '\n'), f.readlines()))

            mainDict = {}

            for theLine in data:
                try:
                    theOperation = str(theLine.split(":").__getitem__(0).strip())
                    theCycles = int(theLine.split(":").__getitem__(1).split(",").__getitem__(0).strip())
                    isPipelined = str(theLine.split(":").__getitem__(1).split(",").__getitem__(1).replace("\\n", "").strip())
                    eachDict = {}
                    eachDict = {theOperation: {'cycles': theCycles, 'isPipelined': isPipelined}}
                    mainDict.update(eachDict)
                except IndexError:
                    theCycles = int(theLine.split(":").__getitem__(1).replace("\\n", "").strip())
                    eachDict = {}
                    eachDict = {theOperation: {'cycles': theCycles}}
                    mainDict.update(eachDict)
                    continue

        return mainDict


    def parse(self, s):

        s = s.strip()
        s = s.split()


        if ':' in s[0]:

            instr = s[1]
            self.labelAddress[s[0].replace(":","").strip().lower()] = s

            self.label = True
            s.pop(0)

        elif '(' in s:

            self.offset = True
        else:

            instr = s[0]

        if instr in self.instructionSet['rtype']:

            return self.createRTypeInstruction(s)
        elif instr in self.instructionSet['itype']:

            return self.createITypeInstruction(s)    
        elif instr in self.instructionSet['jtype']:

            return self.createJTypeInstruction(s)
        elif 'hlt' in instr:

            return self.createHLTInstruction(s)
        else:
            print("self.createRTypeInstruction(s) : ", self.createRTypeInstruction(s))
            raise ParseError("Invalid parse instruction")


    def createRTypeInstruction(self, s):
        if s[0] == "jr":
            return InstTypes(op=s[0], s1 = s[1], regRead = 1, aluop=1)
        return InstTypes(op=s[0], dest=s[1], s1=s[2], s2=s[3], regRead=1, regWrite=1, aluop=1)

    def createITypeInstruction(self, s):


        memread = s[0] == "lw" or s[0] == "l.d" or s[0] == "s.d"
        memwrite = s[0] == "lw" or s[0] == "l.d" or s[0] == "s.d"

        #memread= True

        if (memread or memwrite):

            import re
            #regex = re.compile("(\d+\(?\$r\d+\)?)|(\d+)|(\$r\d+)")  ----- Working
            regex = re.compile("((\d*)\(?(r\d+)\)?)")
            #regex = re.compile("((\d+)*\(?\$r\d+\)?)|(\d+)|(\$r\d+)")
            #regex = re.compile("(\d+)\((\$r\d+)\)")
            #regex = re.compile("(\d+)|(\$r\d+)")

            match = regex.match(s[2])

            immedval = match.group(2)

            if immedval is None:
                immedval = 0

            sval = match.group(3)


            if s[0] == "lw" or   s[0] == "l.d":

                return InstTypes(op=s[0], dest = s[1], s1=sval, immed = immedval, regRead = 1, regWrite = 1, aluop=1, readMem = 1)
            else:
                return InstTypes(op=s[0], s1 = s[1], s2=sval, immed = immedval, regRead = 1, aluop=1, writeMem = 1)

        if ( s[0] == 'bne' or s[0] == 'beq') :

            return InstTypes(op=s[0], s1=s[1], s2= s[2], immed = s[3], regRead = 1, aluop = 1)



        return InstTypes(op=s[0], dest=s[1], s1=s[2], immed=s[3], regRead=1, regWrite=1, aluop=1)

    def createJTypeInstruction(self, s):
        return InstTypes(op=s[0], target=s[1])

    def createHLTInstruction(self,s):
        return InstTypes(op=s[0])


class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)