from EvaluationResult import EvaluationResult

class BigramModel:
    def __init__(self, maxSuffixLength : int):
        self.maxSuffixLength = maxSuffixLength
        self.sentenceCount = 0
        self.totalTagCount = 0
        self.tagCount = {}
        self.wordCount = {}
        self.tagStartCount = {}
        #Map<String, Map<String, Integer>> 
        self.tagTransitionCount = {}
        #Map<String, Map<String, Integer>> 
        self.tagWordCount = {}
        #Map<String, Map<String, Integer>>
        self.tagWordCount = {}
    
    #we assume that the sents are already tagged
    def train(self, tagged_train_sents):
        prevTag = ""
        for sent in tagged_train_sents:
            for word, tag in sent:
                #add word in word appearences
                if word in self.wordCount:
                    self.wordCount[word] += 1
                else:
                    self.wordCount[word] = 1
                
                #add tag in tag appearences
                self.totalTagCount += 1
                if tag in self.tagCount:
                    self.tagCount[tag] += 1
                else:
                    self.tagCount[tag] = 1

                #add word-tag appearence
                if tag not in self.tagWordCount:
                    self.tagWordCount[tag] = {}
                if tag not in self.tagTransitionCount[prevTag]:
                        self.tagWordCount[tag] = 1
                else:
                    self.tagWordCount[tag] += 1 

                #setting relations between previous and
                #current tag
                if len(prevTag) == 0 and prevTag != None:
                    if prevTag not in self.tagTransitionCount:
                        self.tagTransitionCount[prevTag] = {}
                    if tag not in self.tagTransitionCount[prevTag]:
                        self.tagTransitionCount[prevTag] = 1
                    else:
                       self.tagTransitionCount[prevTag] += 1 


                elif len(prevTag) == 0:
                    if tag in self.tagStartCount[tag]:
                        self.tagStartCount[tag] += 1
                    else:
                        self.tagStartCount[tag] = 1
                prevTag = tag

    def evaluate(self) -> EvaluationResult:
        pass

    def getTags(self):
        #vrati novu kopiju tagova
        return dict(self.tagCount)
    
    def getTagTransitionCount(self, fromTag : str, toTag: str):
        if fromTag not in self.tagTransitionCount:
            self.tagTransitionCount[fromTag] = {}
        if fromTag not in self.tagTransitionCount and toTag in self.tagTransitionCount[fromTag]:
            return self.tagTransitionCount[fromTag]
        return 0
        
    def getTransitionProbablity(self, fromTag: str, toTag : str):
        tagToTagCount = 0
        tagOccurences = 0
        if fromTag not in self.tagTransitionCount:
            self.tagTransitionCount[fromTag] = {}
        if fromTag in self.tagTransitionCount and toTag in self.tagTransitionCount:
            tagToTagCount = self.tagTransitionCount[fromTag][toTag]
        
        if fromTag in self.tagCount:
            tagOccurences = self.tagCount[fromTag]
        
        return float(tagToTagCount) / float(tagOccurences) if tagOccurences > 0 else 0
    
    def getWordCount(self, word : str):
        if(word in self.wordCount):
            return self.wordCount(word)
        return 0

    def getEmissionProbability(self, tag : str, word : str):
        tagAndWordCount = 0
        tagOccurences = 0
        
        if tag in self.tagWordCount and word in self.tagWordCount[tag]:
            tagAndWordCount = self.tagWordCount[tag][word]
        
        if tag in self.tagCount:
            tagOccurences = self.tagWordCount[tag]
        
        return float(tagAndWordCount) / float(tagOccurences) if tagOccurences > 0 else 0