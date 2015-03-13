import json
import operator
from collections import defaultdict
import gensim
import os

import Functions

model = gensim.models.word2vec.Word2Vec.load_word2vec_format(os.path.join(os.path.dirname('../../Word2VecTool/'), 'GoogleNews-vectors-negative300.bin'), binary=True)

print "Oh yea"

Debug_Read_PDTB_Data = False
Debug_Read_Articles = False


pdtb_dev_list = Functions.readFile('../../conll15st_data/pdtb-data-01-20-15-dev.json')
#DocID =  pdtb_dev_list[0]["DocID"]
#Arg1 = pdtb_dev_list[0]["Arg1"]
#Arg2 = pdtb_dev_list[0]["Arg2"]

parses=Functions.ReadParse('../../conll15st_data/pdtb-parses-01-12-15-dev.json')
#print parses[DocID]["sentences"][0]["words"]#["dependencies"][0][:]

#Offsets = Functions.BuildOffsets(parses,DocID)
#print Functions.ReturnVerb(Arg1,Offsets)

def printArgs(pdtb_list, parses):
	DistAv = defaultdict(int)
	DistAv["Expansion"]=[0]
	DistAv["Temporal"]=[0]
	DistAv["Contingency"]=[0]
	DistAv["Comparison"]=[0]
	
	for i in pdtb_list:
		Sense = i["Sense"][0].split('.')[0]
		DocID = i["DocID"]
		Arg1 = i["Arg1"]
		Arg2 = i["Arg2"]
		Offsets = Functions.BuildOffsets(parses,DocID)
		verb1 = Functions.ReturnVerb(Arg1,Offsets)
		verb2 = Functions.ReturnVerb(Arg2,Offsets)
		if ((verb1 in model)&(verb2 in model)):
			sim = model.similarity(verb1,verb2)
		else:
			sim = 0
		if ((Sense in DistAv)&(sim!=0)):
			DistAv[Sense].append(sim)
	for key in DistAv:
		print key, float(sum(DistAv[key]))/float(len(DistAv[key])-1)
			

printArgs(pdtb_dev_list,parses)

if Debug_Read_PDTB_Data:
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



