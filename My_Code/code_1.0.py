def ImplicitArgumentDistanceCheck(inputDictOriginal):
	inputDict = inputDictOriginal
	yes = 0
	no = 0
	connec = defaultdict(int)
	for keys in inputDict:
		endArg1 = keys["Arg1"]["CharacterSpanList"][-1][1]
		startArg2 = keys["Arg2"]["CharacterSpanList"][0][0]
		if startArg2>endArg1:
			no += 1
		else:
			yes += 1
			if (yes==1):
				print keys
			connec[keys["Connective"]["RawText"]]+=1
	print yes
	print no
	print connec




def DictToDist(inputDictOriginal):
        sum=0
	inputDict = inputDictOriginal
        for keys in inputDict:
                sum+=inputDict[keys]
        for keys in inputDict:
                #print inputDict[keys]
                inputDict[keys]=float(inputDict[keys])/sum
                #print inputDict[keys]
	
	inputDict = sorted(inputDict.items(),key=operator.itemgetter(1),reverse=True)

        return inputDict

def readFile(path):
	temp = open(path,'r')
	temp_list = []
	for lines in temp:
		temp_list.append(json.loads(lines))
	temp.close()
	return temp_list

def getDictConn(inputList):
	Dict_Conn = {}
	for i in inputList:
		if (Dict_Conn.get(i["Connective"]["RawText"])!=Dict_Conn.get("aha")):
			Dict_Conn[i["Connective"]["RawText"]]+=1
		else:
			Dict_Conn[i["Connective"]["RawText"]]=1
	return Dict_Conn

def getDictType(inputList):
        Dict_Type = {}
        for i in inputList:
                if (Dict_Type.get(i["Type"])!=Dict_Type.get("aha")):
                        Dict_Type[i["Type"]]+=1
                else:
                        Dict_Type[i["Type"]]=1
        return Dict_Type


def getDictSense(inputList):
	Dict_Sense = {}
	for i in inputList:
		if (Dict_Sense.get(tuple(i["Sense"]))!=Dict_Sense.get("aha")):
			Dict_Sense[tuple(i["Sense"])]+=1
		else:
			Dict_Sense[tuple(i["Sense"])]=1
	return Dict_Sense


def readArticles():
	Articles = ['' for i in range(0,2300)]
	for i in range(200,2000):
		if i<1000:
			Path_Completion = 'wsj_0'+str(i)
		else:
			Path_Completion = 'wsj_'+str(i)
		path = '../../conll15st_data/raw_train/' + Path_Completion
		f=open(path,'r')
		Articles[i]=f.read()
	for i in range(2100,2200):
		Path_Completion = 'wsj_'+str(i)
                path = '../../conll15st_data/raw_train/' + Path_Completion
                f=open(path,'r')
                Articles[i]=f.read()
	for i in range(2200,2300):
                Path_Completion = 'wsj_'+str(i)
                path = '../../conll15st_data/raw_dev/' + Path_Completion
                f=open(path,'r')
                Articles[i]=f.read()
	return Articles


import json
import operator
from collections import defaultdict

print "Oh yea"

Debug_Read_PDTB_Data = False
Debug_Read_Articles = False

pdtb_dev_list = readFile('../../conll15st_data/pdtb-data-01-20-15-dev.json')
n=0
for keys in pdtb_dev_list:
	if((n<5)&(keys["Sense"][0]=="Comparison.Contrast")):
		print "Arg1:"
		print keys["Arg1"]["RawText"]
		print "Arg2:"
		print keys["Arg2"]["RawText"]
		n+=1
fout = open('Output','w')

if Debug_Read_PDTB_Data:
	pdtb_dev_list = readFile('../../conll15st_data/pdtb-data-01-20-15-dev.json')
	pdtb_train_list = readFile('../../conll15st_data/pdtb-data-01-20-15-train.json')

	ImplicitArgumentDistanceCheck(pdtb_train_list)

	fout.write("Connectives: \n \n")

	Dict_Train_Conn = getDictConn(pdtb_train_list)
	Dist_Train_Conn = DictToDist(Dict_Train_Conn)
	for items in Dist_Train_Conn:
		fout.write(str(items[0]) + ',' + str(items[1]) + '\n')

	fout.write("\n \n Types: \n \n")

 	Dict_Train_Type = getDictType(pdtb_train_list)
        Dist_Train_Type = DictToDist(Dict_Train_Type)
        for items in Dist_Train_Type:
                fout.write(str(items[0]) + ',' + str(items[1]) + '\n')

	fout.write("\n \n Senses: \n \n")

 	Dict_Train_Sense = getDictSense(pdtb_train_list)
        Dist_Train_Sense = DictToDist(Dict_Train_Sense)
        for items in Dist_Train_Sense:
		for elems in items[0]:
			fout.write(str(elems) + ',')
		fout.write(str(items[1]) + '\n')

if Debug_Read_Articles:
	articles = readArticles()
