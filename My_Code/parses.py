from collections import defaultdict
import json

def Parse_Dict():
	Dictionary=defaultdict(int)
	parses_dict = defaultdict(int)
	parses_file = open("/media/training-datasets/conll15-st-dev-2015-03-04/pdtb-parses.json",'r')
	parses_dict = json.loads(parses_file.readline())
	#print parses_dict["wsj_1000"]["sentences"][0]
	for DOC_ID in parses_dict:
		#print DOC_ID

		Dictionary[DOC_ID] = defaultdict(int)
		for sentences in parses_dict[DOC_ID]["sentences"]:
			for i,words in enumerate(sentences["words"]):
				Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]=defaultdict()
				Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["word"]=words[0]
				Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["wordIndex"]=i+1
				Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["POS"]=words[1]["PartOfSpeech"]
				Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["modifiers"]=[]
				Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["modifierTo"]=[]
				for j,dep in enumerate(sentences["dependencies"]):
					depType = dep[0]
					depHead = dep[1].split('-')
					#print depHead
					depMod  = dep[2].split('-')
					if str(i+1)==depHead[1]:
						Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["modifiers"].append((depMod[0],depType))
					elif str(i+1)==depMod[1]:
						Dictionary[DOC_ID][words[1]["CharacterOffsetBegin"]]["modifierTo"].append((depHead[0],depType))

						
					
				

	print Dictionary["wsj_2200"][42]
				
		
Parse_Dict()
	
