import json
import os
from collections import defaultdict
from collections import OrderedDict
from numpy import *
from sklearn import *


def RectifySense(sense):
	Rectifier = defaultdict(int)
	Rectifier["Asynchronous"] =  "Temporal.Asynchronous"
	Rectifier["Synchrony"] = "Temporal.Synchrony"
	Rectifier["Cause"] = "Contingency.Cause"
	Rectifier["Pragmatic_cause"] = "Contingency.Pragmatic_cause"
	Rectifier["Condition"] = "Contingency.Condition"
	Rectifier["Pragmatic_condition"] = "Contingency.Pragmatic_condition"
	Rectifier["Contrast"] = "Comparison.Contrast"
	Rectifier["Pragmatic_contrast"] = "Comparison.Pragmatic_contrast"
	Rectifier["Concession"] = "Comparison.Concession"
	Rectifier["Pragmatic_concession"] = "Comparison.Pragmatic_concession"
	Rectifier["Conjunction"] = "Expansion.Conjunction"
	Rectifier["Instantiation"] = "Expansion.Instantiation"
	Rectifier["Restatement"] = "Expansion.Restatement"
	Rectifier["Alternative"] = "Expansion.Alternative"
	Rectifier["Exception"] = "Expansion.Exception"
	Rectifier["List"] = "Expansion.List"
	return Rectifier[sense]

def PopulateFeatValMatrix(training_lines, CartVocab):
	
	nColumns = len(CartVocab)
	nRows = len(training_lines)


	FeatureMatrix = zeros((nRows,nColumns),dtype=float)
	ValueMatrix = empty(nRows,dtype=object)
	k=0

	for t,lines in enumerate(training_lines):
		instance = json.loads(lines)
		ValueMatrix[t]=instance["Sense"][0]
		vocab1 = instance["Arg1"]["RawText"].split()
		vocab2 = instance["Arg2"]["RawText"].split()
		for i in vocab1:
			for j in vocab2:
				if (i,j) in CartVocab:
					FeatureMatrix[t][CartVocab[(i,j)]] = 1.0
					

	return (FeatureMatrix,ValueMatrix)

def ParseRaw(input_path, output_path, pdtb_dir):
        os.system(pdtb_dir+"/pdtb-parser/src/parse.rb "+ input_path +" > " + output_path)

def ParseOutput(input_file_path, output_file, pdtb_dir):

	args=open(output_file,'w')
	print "aha"

	for input_file in os.listdir(input_file_path):

		os.system(pdtb_dir+"/pdtb-parser/src/parse.rb "+ input_file_path+input_file +" > temp_file")

		parse_output = open('temp_file','r')        
		Collector = defaultdict(int)
		Output = defaultdict(int)

		j=0

		for i in parse_output.readlines():
			for k in i.split():
				if k[0]=='{':
					key = k[1:].split('_')
					if len(key)>=3:
						Collector[(key[0],key[1],key[2])]={"TokenList": [], "RawText": ""}
						if len(key)>3:
							Output[(key[0],key[1],"Sense")] = [RectifySense(key[3])]
				elif k[-1]=='}':
					key=k[0:-1].split('_')
					if len(key)>=3:
						Output[(key[0],key[1],key[2])] = Collector[(key[0],key[1],key[2])]
						del Collector[(key[0],key[1],key[2])]
				else:
					j+=1
					for (n,keys) in enumerate(Collector):
						Collector[keys]["TokenList"].append(j)
						Collector[keys]["RawText"]+=k+" "
		jsonDict = defaultdict(int)

		sortedOutput = OrderedDict(sorted(Output.items(), key=lambda t: (t[0],t[1])))

		temp_keys = ("bla","bla")
		i=-1
		for keys in sortedOutput:
			if (keys[0:2]!=temp_keys):
				i+=1
				jsonDict[i]=defaultdict(int)
				jsonDict[i]["Connective"]={"TokenList":[]}
				jsonDict[i]["DocID"] = input_file
				if keys[0]=="Exp":
					jsonDict[i]["Type"]="Explicit"
				else:
					jsonDict[i]["Type"]="Implicit"
				if keys[2]=="conn":
					jsonDict[i]["Connective"]=Output[keys]
				else:
					jsonDict[i][keys[2]]=Output[keys]
				temp_keys=keys[0:2]
			else:
				if keys[2]=="conn":
					jsonDict[i]["Connective"]=Output[keys]
				else:
					jsonDict[i][keys[2]]=Output[keys]
		for keys in jsonDict:
			if jsonDict[keys]["Type"]=="Explicit":
				args.write(json.dumps(jsonDict[keys]))
				args.write('\n')





def PopulateCartesianVocabulary(training_data_lines):
	CartVocab = defaultdict(int)
	k=0

	for lines in training_data_lines:
		instance = json.loads(lines)
		vocab1 = instance["Arg1"]["RawText"].split()
		vocab2 = instance["Arg2"]["RawText"].split()
		for i in vocab1:
			#print type(i)
			for j in vocab2:
				if not((i,j) in CartVocab):
					CartVocab[(i,j)]=k
					k+=1

	return CartVocab
				
def GetAccuracy(testData,CartVocab,clf):

	(testFeat,testVal) = PopulateFeatValMatrix(testData, CartVocab)
	predVal = clf.predict(testFeat)
	ninst = len(testVal)
	k=0.0
	for i in range(0,ninst):
		if (predVal[i]==testVal[i]):
			k+=1

	return k/ninst 




ParseOutput("./test_data/", "args", "../..")


args = open("args",'r')
training = open("/media/training-datasets/shallow-discourse-parsing/conll15-st-train-2015-03-04/pdtb-data.json",'r')
input_lines = training.readlines() + args.readlines()
training_lines = input_lines[:100]
testing_lines = input_lines[-3:]



CartVocab = PopulateCartesianVocabulary(training_lines)

(trainFeat,trainVal) = PopulateFeatValMatrix(training_lines, CartVocab)

clf = svm.SVC()
clf.fit(trainFeat,trainVal)

print GetAccuracy(testing_lines,CartVocab,clf)

#print CartVocab[("Goodman","Haag")]

#Vocab = PopulateVocabulary()
#print Vocab['the']
#print Vocab['hence']
#print Vocab['girl']	
#print len(Vocab)
