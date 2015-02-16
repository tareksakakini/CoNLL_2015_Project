def DictToDist(inputDict):
        sum=0
        for keys in inputDict:
                sum+=inputDict[keys]
        for keys in inputDict:
                #print inputDict[keys]
                inputDict[keys]=float(inputDict[keys])/sum
                #print inputDict[keys]
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
		path = '../conll15st_data/raw_train/' + Path_Completion
		f=open(path,'r')
		Articles[i]=f.read()
	for i in range(2100,2200):
		Path_Completion = 'wsj_'+str(i)
                path = '../conll15st_data/raw_train/' + Path_Completion
                f=open(path,'r')
                Articles[i]=f.read()
	for i in range(2200,2300):
                Path_Completion = 'wsj_'+str(i)
                path = '../conll15st_data/raw_dev/' + Path_Completion
                f=open(path,'r')
                Articles[i]=f.read()
	return Articles


import json

print "Oh yea"

Debug_Read_PDTB_Data = True
Debug_Read_Articles = False

if Debug_Read_PDTB_Data:
	pdtb_dev_list = readFile('../conll15st_data/pdtb-data-01-20-15-train.json')
	pdtb_train_list = readFile('../conll15st_data/pdtb-data-01-20-15-train.json')

	Dict_Dev_Conn = getDictConn(pdtb_dev_list)
	Dict_Dev_Sense = getDictSense(pdtb_dev_list)
	Dict_Train_Type = getDictType(pdtb_train_list)

	Dist_Train_Type = DictToDist(Dict_Train_Type)

	for keys in Dist_Train_Type:
		print keys,Dist_Train_Type[keys]


if Debug_Read_Articles:
	articles = readArticles()
	print articles[2200][253]
	print articles[2200][254]
	print articles[2200][257]
