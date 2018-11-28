import pydot
import glob
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

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


def extractInfos(file):
    saida = csv.writer(open("saida.csv", "wb"))
    saida.writerow(["function","numOpt","opt","nodes","edges"])
    x = []
    s = file + "dequeue/*.dot"
    x.append(glob.glob(s))
    s = file + "enqueue/*.dot"
    x.append(glob.glob(s))
    s = file + "dijkstra/*.dot"
    x.append(glob.glob(s))
    s = file + "main/*.dot"
    x.append(glob.glob(s))
    s = file + "qcount/*.dot"
    x.append(glob.glob(s))
    for j in x:
        for i in j:
            G = pydot.graph_from_dot_file(i)
            if(len(G)>1):
                print("erro, numero de grafos")
                exit(-1)
            G = G[0]
            out = []
            name = i.split("/")
            out.append(name[2])
            name = name[3].split("_")
            name = name[2].split(".")
            name = name[0].split(",")
            out.append(name[0])
            out.append(name[1])
            out.append(str(len(G.get_nodes())))
            out.append(str(len(G.get_edges())))
            saida.writerow(out)

### MAIN ##

opts = lerOpt()
extractCFG("codes/djikstra.ll",opts,"codes/",1)
extractInfos("./CFGs/")
