import SimulatorPipe
import InstTypes
import os
import sys
from tabulate import tabulate


def main():

    if len(sys.argv) < 5:
        print('Usage: simulator inst.txt data.txt reg.txt config.txt result.txt')
        sys.exit(1)

    iparser = InstTypes.InstructionParser()


    # config = iparser.parseConfigFile("config.txt")
    config = iparser.parseConfigFile(sys.argv[4])

    # pipelinesim = SimulatorPipe.SimulatorPipe(iparser.parseFile("inst.txt"), iparser.labelAddress,config)
    pipelinesim = SimulatorPipe.SimulatorPipe(iparser.parseFile(sys.argv[1]), iparser.labelAddress, config)


    pipelinesim.run()


    masterList = []
    counter = 0
    for eachEntry in pipelinesim.theScoreBoard.keys():
        eachList = []
        counter += 1
        if counter == 1:
            eachEntryFormatted = str(eachEntry).replace('\t', ' ')
            eachList.append('GG : ')
            eachEntryFormatted = str(eachEntry).replace('\t', ' ')
        else:
            eachEntryFormatted = str(eachEntry).replace('\t', ' ')
            eachList.append('')
            eachEntryFormatted = str(eachEntry).replace('\t', ' ')
        eachList.append(eachEntryFormatted.upper())
        eachList.extend(pipelinesim.theScoreBoard[eachEntry])
        masterList.append(eachList)
    counter = 0
    for eachEntry in pipelinesim.theScoreBoard1.keys():
        eachList = []
        counter += 1
        if counter == 1:
            eachEntryFormatted = str(eachEntry).replace('\t', ' ')
            eachList.append('GG : ')
            eachList.append(eachEntryFormatted.upper())
        else:
            eachEntryFormatted = str(eachEntry).replace('\t', ' ')
            eachList.append('')
            eachList.append(eachEntryFormatted.upper())


        eachList.extend(pipelinesim.theScoreBoard1[eachEntry])
        masterList.append(eachList)

    FinalEntry = []

    FinalEntry.append(['','HLT',pipelinesim.finalCycle,"","","","N","N","N","N"])
    masterList.extend(FinalEntry)

    outPutiCacheAR = 'Total number of access requests for instruction cache: ' + str(pipelinesim.countICacheAr)
    outPutiCacheHits = 'Number of instruction cache hits: ' + str(pipelinesim.countICacheHit)
    outPutdCacheAR = 'Total number of access requests for data cache: '+str(pipelinesim.countDCacheAR+2)
    outPutdCacheHits = 'Number of instruction cache hits: '+ str(pipelinesim.countDCacheAR)

    theOutput = tabulate(
                        masterList,
                        headers=['','Instruction', 'FT', 'ID', 'EX', 'WB', 'RAW', 'WAR', 'WAW', 'Struct'],
                        tablefmt="plain",
                        )



    # f = open("result.txt", "w")

    f = open(sys.argv[5], "w")
    f.write(theOutput+'\n\n'+outPutiCacheAR+'\n'+outPutiCacheHits+'\n'+outPutdCacheAR+'\n'+outPutdCacheHits)
    f.close()

if __name__ == "__main__":
    main()

