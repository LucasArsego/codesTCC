import os

def extractCFG(arquivo,opts,arquivoName,numOpt):
    nameOpt = str(arquivoName) + str(numOpt) + ".ll"

    newName = str(arquivoName ) + "_" + str(opts[0][0]) + "_" + str(numOpt) + '.ll'

    s = "opt -march=x86 -mcpu=core-avx2 -mem2reg " + str(opts[0][0]) + " -S " + str(arquivo) + " -o " + nameOpt
    # print(s)
    os.system(s)

    x = "opt -dot-cfg" + " " + nameOpt
    # print(x)
    os.system(x)

    cfgName_d = "/TCC/CFGs/dequeue/cfg_dequeue_"
    cfgName_di = "/TCC/CFGs/dijkstra/cfg_dijkstra_"
    cfgName_en = "/TCC/CFGs/enqueue/cfg_enqueue_"
    cfgName_m = "/TCC/CFGs/main/cfg_main_"
    cfgName_q = "/TCC/CFGs/qcount/cfg_qcount_"
    cfgName_f = ".dot"

    os.rename("cfg.dequeue.dot", cfgName_d + str(numOpt) + "," +str(opts[0][0]) + cfgName_f)
    os.rename("cfg.dijkstra.dot", cfgName_di + str(numOpt) + "," + str(opts[0][0]) + cfgName_f)
    os.rename("cfg.enqueue.dot", cfgName_en + str(numOpt) + "," + str(opts[0][0]) + cfgName_f)
    os.rename("cfg.main.dot", cfgName_m + str(numOpt) + "," + str(opts[0][0]) + cfgName_f)
    os.rename("cfg.qcount.dot", cfgName_q + str(numOpt) + "," + str(opts[0][0]) + cfgName_f)

    numOpt += 1
    opts[0].pop(0)
    # print(len(opts[0]),opts[0])
    if(len(opts[0]) == 0):
        opts.pop(0)
    if(len(opts) == 0):
        return
    extractCFG(nameOpt,opts,arquivoName, numOpt)

def lerOpt():
    f = open("opts.txt")
    l = []
    for i in f:
        j = i.split("\n")
        j = j[0].split("Pass Arguments: ")
        j = j[1].split(" ")
        l.append(j)
    return l

### MAIN ##

opts = lerOpt()
extractCFG("codes/djikstra.ll",opts,"codes/",1)
