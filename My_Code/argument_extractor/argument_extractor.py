def ParseOutput(input_path, conll_format, rawInput):

	parse_output = open(input_path,'r')
	Collector = defaultdict(int)
	Output = defaultdict(int)

	DocID = rawInput.split('/')[-1]

	j=0

	for i in parse_output.readlines():
		for k in i.split():
			if k[0]=='{':
				key = k[1:].split('_')
				if len(key)>=3:
					Collector[(key[0],key[1],key[2])]={"TokenList": []}
					if len(key)>3:
						Output[(key[0],key[1],"Sense")] = [key[3]]
			elif k[-1]=='}':
				key=k[0:-1].split('_')
				if len(key)>=3:
					Output[(key[0],key[1],key[2])] = Collector[(key[0],key[1],key[2])]
					del Collector[(key[0],key[1],key[2])]
			else:
				j+=1
				for (n,keys) in enumerate(Collector):
					Collector[keys]["TokenList"].append(j)
					

	jsonDict = defaultdict(int)

	sortedOutput = OrderedDict(sorted(Output.items(), key=lambda t: t[0]))

	temp_keys = ("bla","bla")
	i=-1			
	for keys in sortedOutput:
		if (keys[0:2]!=temp_keys):
			i+=1
			jsonDict[i]=defaultdict(int)
			jsonDict[i]["Connective"]={"TokenList":[]}
			jsonDict[i]["DocID"] = DocID
			if keys[0]=="Exp":
				jsonDict[i]["Type"]="Explicit"
			else:
				jsonDict[i]["Type"]="Implicit"
			if keys[2]=="conn":
				jsonDict[i]["Connective"]=Output[keys]
			else:
				jsonDict[i][keys[2]]=Output[keys]
			temp_keys=keys[0:2]
			jsonDict[i]["Sense"]=["EntRel"]
		else:
			if keys[2]=="conn":
				jsonDict[i]["Connective"]=Output[keys]
			else:
				jsonDict[i][keys[2]]=Output[keys]
			jsonDict[i]["Sense"]=["EntRel"]
	for keys in jsonDict:
		conll_format.write(json.dumps(jsonDict[keys]))
		conll_format.write('\n')

def ParseRaw(input_path, output_path):

	os.system("../../pdtb-parser/src/parse.rb "+ input_path +" > " + output_path)

import json
import os
from collections import defaultdict
from collections import OrderedDict

print "Oh yea"
tempPath = './parse_output'
outputFile = open('./conll_format','w')

for i in range(2200,2201):
	print i
	ID = "%04d" %(i)
	rawInput = '../../../conll15st_data/raw_dev/wsj_'+ID
	ParseRaw(rawInput,tempPath)
	ParseOutput(tempPath, outputFile, rawInput)
