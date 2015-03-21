import json
import os
from collections import defaultdict
from collections import OrderedDict

def ParseRaw(input_path, output_path, pdtb_dir):
        os.system(pdtb_dir+"/pdtb-parser/src/parse.rb "+ input_path +" > " + output_path)

def ParseOutput(input_file, output_file, pdtb_dir):

	args=open(output_file,'w')

        os.system(pdtb_dir+"/pdtb-parser/src/parse.rb "+ input_file +" > temp_file")

	parse_output = open('temp_file','r')        
	Collector = defaultdict(int)
        Output = defaultdict(int)

        for i in parse_output.readlines():
                for k in i.split():
                        if k[0]=='{':
                                key = k[1:].split('_')
                                if (len(key)>=3 and (key[2]=="Arg1" or key[2]=="Arg2")):
                                        Collector[(key[0],key[1],key[2])]={"RawText": ""}
                        elif k[-1]=='}':
                                key=k[0:-1].split('_')
                                if (len(key)>=3 and (key[2]=="Arg1" or key[2]=="Arg2")):
                                        Output[(key[0],key[1],key[2])] = Collector[(key[0],key[1],key[2])]
                                        del Collector[(key[0],key[1],key[2])]
                        else:
                                for keys in Collector:
                                        Collector[keys]["RawText"]+=k+" "


        jsonDict = defaultdict(int)

        sortedOutput = OrderedDict(sorted(Output.items(), key=lambda t: (t[0],t[1])))

        temp_keys = ("bla","bla")
        i=-1
        for keys in sortedOutput:
		print keys
                if (keys[0:2]!=temp_keys):
                        i+=1
                    	jsonDict[i]=defaultdict(int)
                        jsonDict[i][keys[2]]=Output[keys]
                        temp_keys=keys[0:2]
		else:
			jsonDict[i][keys[2]]=Output[keys]
        for keys in jsonDict:
                args.write(json.dumps(jsonDict[keys]))
                args.write('\n')



def PopulateVocabulary():
	Vocabulary = defaultdict(int)
	i=0
	training_path = "/media/training-datasets/conll15-st-train-2015-03-04/raw/"
	for filename in os.listdir(training_path):
		#print filename
		#print "aha"
		text = open(training_path+filename,'r')
		for lines in text.readlines():
			for words in lines.split():
				if not(words in Vocabulary) :
					Vocabulary[words]=i
					i+=1
					#print words
					#print filename
	return Vocabulary


ParseOutput("test1", "args", "../..")
#Vocab = PopulateVocabulary()
#print Vocab['the']
#print Vocab['hence']
#print Vocab['girl']	
#print len(Vocab)
