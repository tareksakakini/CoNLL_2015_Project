import json
from collections import defaultdict

def ReadParse(path):	
	f=open(path,'r')
	parses = json.loads(f.readline())
	return parses

def BuildOffsets(parses,DocID):	
	Offsets=defaultdict(int)
	for i in parses[DocID]["sentences"]:
		for j in i["words"]:
			if j[1]["PartOfSpeech"][0:2]=="VB":
				Offsets[j[1]["CharacterOffsetBegin"]]=j[0]
	return Offsets

def ReturnVerb(Arg,Offsets):
	for j in Arg["TokenList"]:
		if j[0] in Offsets:
			return Offsets[j[0]]	

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
