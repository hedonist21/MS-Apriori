import os
import itertools

#initialization
SDC = 0.0			         #support contraint
MIS = dict()		                 #MIS later sorted
temp = dict()		                 #rows of Txns
sortDict = dict()	                 #
itemList = list()	                 #SortedItem acc to MIS
listFk = list([] for _ in range(10))	 #Frequent Set
CList = list([] for _ in range(10))	 #Candidate Set
CCount = dict()				 #Candidate Freq
itemCount = dict()                       #
T = list()			         #Txns
n = 0				         #total Txns
L = list()
cannotBeTogether = list()
mustHave = list()
tailCount = {}


#open all files
parameter_file = "/Users/ut_mactb/Documents/dm/para3.txt"
para = open(parameter_file)

transaction_file = "/Users/ut_mactb/Documents/dm/data3.txt"
data = open(transaction_file)

output_file = "/Users/ut_mactb/Documents/dm/result1.txt"
out = open(output_file, "w")

# Methods in accordance with MSApriory Algo

#initial pass
def initialPass(itemList,itemCount,sortDict,MIS):
    L=list()
    for i in range(len(itemList)):
        if(i == 0):
            L.append(itemList[0])
        else:
            if((itemCount.get(itemList[i]) / n) >= MIS.get(itemList[0])):
                L.append(itemList[i])

    for i in range(len(L)):
        sortDict[L[i]] = i

    return L


#checking musthave and cantbetogether          
def constraint(cannotBeTogether,mustHave):
    global listFk
    if(mustHave != [] or cannotBeTogether !=[] ):
        for listFkIndex in range(len(listFk)):
            listIndex = len(listFk[listFkIndex])-1
            while listIndex > -1:
                subset = listFk[listFkIndex][listIndex]
                for i in range(len(cannotBeTogether)):
                    if (mustHave != [] and cannotBeTogether !=[]):
                        if(set(cannotBeTogether[i]) <= set(subset) or set(mustHave).isdisjoint(subset)):
                            listFk[listFkIndex].pop(listFk[listFkIndex].index(subset))
                            break

                    elif (cannotBeTogether !=[] and mustHave == []):
                        if (set(cannotBeTogether[i]) <= set(subset)):
                            listFk[listFkIndex].pop(listFk[listFkIndex].index(subset))
                            break

                    elif (mustHave != [] and cannotBeTogether ==[]):
                        if (set(mustHave).isdisjoint(subset)):
                            listFk[listFkIndex].pop(listFk[listFkIndex].index(subset))
                            break

                listIndex = listIndex - 1
                    


# Adding 1-ItemSets to the listFk
def F1(L,itemCount,MIS):
    global listFk
    if(not listFk[1]):
        for i in range(len(L)):
            if((itemCount.get(L[i])/n)>=MIS.get(L[i])):
                listFk[1].append([L[i]])
 


#Generating Candidate =2
def Cand2_Gen(L,itemCount):
    global CList
    for l in range (0, len(L)):
        if (itemCount[L[l]] / n) >= MIS[L[l]]:
            for h in range( l + 1, len(L)):
                if (itemCount[L[h]] / n) >= MIS[L[l]] and abs((itemCount[L[h]] / n) - (itemCount[L[l]] / n)) <= SDC:
                    CList[2].append(list())
                    CList[2][len(CList[2])-1].append(L[l])
                    CList[2][len(CList[2])-1].append(L[h])
    CList[2].sort(key = lambda row: row[1])



#Generating Candidates for >2
def MISCand_Gen(a,MIS,itemCount,SDC,sortDict):
    global Clist,listFk
    m = a - 1
    k = 0
    for Fi in range(0, len(listFk[m])):
        for Fj in range(0, len(listFk[m])):
            while ((k < m-1) and (listFk[m][Fi][k] == listFk[m][Fj][k])):
                k += 1
                
            if (k == m - 1):
                if ((sortDict[listFk[m][Fi][k]] < sortDict[listFk[m][Fj][k]]) and (abs((itemCount[listFk[m][Fi][k]] / n) - (itemCount[listFk[m][Fj][k]] / n)) <= SDC)):
                    CList[m+1].append(list(listFk[m][Fi]))
                    CList[m+1][len(CList[m+1])-1].append(listFk[m][Fj][k])
                    # Finding subsets via itertools class
                    subset = list(set(itertools.combinations(CList[m+1][len(CList[m+1])-1],m)))
                    for sub in range(0,len(subset)):
                        if(not CList[m+1]):
                            if ((bool(CList[m+1][len(CList[m+1])-1][0]) in subset[sub]) or (MIS[CList[m+1][len(CList[m+1])-1][1]] == MIS[CList[m+1][len(CList[m+1])-1][0]])):
                                if (bool(subset[sub]) not in listFk[m]):
                                    CList[m+1][len(CList[m+1])-1].remove()
            
            k=0



#data refining
def fileParser(parameter_file,transaction_file):
    
    
    para = open(parameter_file)
    data = open(transaction_file)

    global MIS, n, itemList, itemCount, SDC, T, cannotBeTogether, mustHave

    #Extract MIS values and SDC
    for i in para:
        if (i.find('SDC') != -1):
            SDC = float(i.replace(' ','').rstrip().split('=')[1])

        if (i.find('MIS') != -1):
            temp = i.replace(' ','').replace('MIS','').replace('(','').replace(')','').rstrip().split('=')
            MIS[int(temp[0])] = float(temp[1])

        if (i.find('must-have') != -1):
           mustHave = i.replace('must-have:','').replace(' ','').rstrip().split('or')
           mustHave = list(map(int, mustHave))

        if (i.find('cannot_be_together') != -1):
            cannotBeTogether = i.replace(' ','').replace('cannot_be_together:','').replace('{','[').replace('}',']').replace("'", 'a').rstrip().split('a')    
            cannotBeTogether = cannotBeTogether[0].replace('],[',' ').replace('[','').replace(']','').split()
            for i in range(len(cannotBeTogether)):
                cannotBeTogether[i] = list(map(int, cannotBeTogether[i].split(',')))


    txns = sorted(MIS, key = MIS.__getitem__)

    for txn in txns:
        itemList.append(int(txn))
        itemCount[int(txn)] = 0

    
    #Extract Txns 
    for i in data:
        T.append(list())
        transaction = i.replace(' ', '').replace('{','').replace('}','').replace('<','').replace('>','').split(',')
        for tx in transaction:
            T[len(T) - 1].append(int(tx))
            if(itemCount.get(int(tx)) != None):
                itemCount[int(tx)] = itemCount.get(int(tx)) + 1

    n = len(T)




#output generation
def result(tailCount, itemCount, CCount):
    global listFk
    listFk = [x for x in listFk if x != []]
    
    
    freq = 0
    print ("Frequent 1-itemsets")
    out.write("\nFrequent 1-itemsets\n")
    if (listFk != []):
        for fn in listFk[0]:
            freq += 1
            print ('\t' + str(itemCount[fn[0]]) + ' : { ' + str(fn[0]) + ' }')
            out.write('\t' + str(itemCount[fn[0]]) + ' : { ' + str(fn[0]) + ' }\n')
    print ("\tTotal number of frequent 1-itemsets = " + str(freq))
    out.write("\tTotal number of frequent 1-itemsets = " + str(freq) + "\n")


    for i in range(1,len(listFk)):
         print ('\n\nFrequent',str(i+1) + '-itemsets')
         out.write('\n\nFrequent' + str(i+1) + '-itemsets\n')
         freq = 0
         for fn in listFk[i]:
              n = 0
              for j in range(len(T)):
                    if(set(T[j]) >= set(fn)):
                        n += 1
              freq += 1
              print ('\t',n , ' : {',str(fn).replace("[", "").replace("]", ""),'}')
              out.write('\t' + str(n) + ' : {' + str(fn).replace("[", "").replace("]", "") + '}\n')
              print('Tail Count =', tailCount[tuple(fn)])
              out.write('Tail Count = ' + str(tailCount[tuple(fn)]) + "\n")
         print ('\n\tTotal number of frequent', str(i+1) + '-itemsets = ' ,freq)
         out.write('\n\tTotal number of frequent ' + str(i+1) + '-itemsets = '  + str(freq) + "\n")


#calling functions1
fileParser(parameter_file,transaction_file)
L= initialPass(itemList,itemCount,sortDict,MIS)
F1(L,itemCount,MIS)


#Adding i-ItemSets to listFk
k = 2
while (True):
    if (not listFk[k - 1]):
        break

    if (k == 2):
        Cand2_Gen(L,itemCount)
    else:
        MISCand_Gen(k,MIS,itemCount,SDC,sortDict)

    for tx in T:
        for cand in CList[k]:
            if (set(cand).issubset(set(tx))):
                if (CCount.get(tuple(cand)) == None):
                    CCount[tuple(cand)] = 1
                else:
                    CCount[tuple(cand)] = CCount.get(tuple(cand)) + 1

            if (set(cand[1:]).issubset(set(tx))):
                if (tailCount.get(tuple(cand)) == None):
                    tailCount[tuple(cand)] = 1
                else:
                    tailCount[tuple(cand)] = tailCount.get(tuple(cand)) + 1

    for cand in CList[k]:
        if (CCount.get(tuple(cand)) != None):
            if (CCount.get(tuple(cand)) / n >= MIS[cand[0]]):
                listFk[k].append(cand[:])
    k += 1


#calling functions2   
constraint(cannotBeTogether,mustHave)
result(tailCount, itemCount, CCount)
