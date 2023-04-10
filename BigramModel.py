from EvaluationResult import EvaluationResult
from AugmentedSuffixTree import AugmentedSuffixTree
from Viterbi import Viterbi
class BigramModel:
    def __init__(self, maxSuffixLength : int, maxWordFrequency: int):
        self.maxSuffixLength = maxSuffixLength
        self.maxWordFrequency = maxWordFrequency
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
        self.wordTagCount = {}
    
    #we assume that the sents are already tagged
    def train(self, tagged_train_sents):
        for sent in tagged_train_sents:
            prevTag = ""
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

                #add tag-word appearence
                self.incrementTagWordCount(tag, word)

                #setting relations between previous and
                #current tag
                if len(prevTag) > 0 and prevTag != None:
                    self.incrementTagTransitionCount(prevTag, tag)
                elif len(prevTag) == 0:
                    self.incrementTagStartCount(tag)
                prevTag = tag

    def evaluate(self, upperCaseTree:AugmentedSuffixTree, lowerCaseTree:AugmentedSuffixTree, sentences) -> EvaluationResult:
        #sentences are actually taggedSentences

        sentenceTags = []
        rawSentences = []

        viterbi = Viterbi(self, upperCaseTree, lowerCaseTree, self.maxSuffixLength)

        for sentence in sentences:
            rawSentence = [word for (word, _) in sentence]
            sentenceTags.append(viterbi.run(rawSentence))
            rawSentences.append(rawSentence)
        return EvaluationResult(rawSentences, sentenceTags, sentences)

    def getTags(self):
        #return a new copy of the tags
        return dict(self.tagCount)

    def getTagCount(self, tag:str):
        count = 0
        if tag in self.tagCount:
            count = self.tagCount[tag]
        return count
    
    def getTagStartCount(self, tag:str):
        count = 0
        if tag in self.tagStartCount:
            count = self.tagStartCount[tag]
        return count

    def getTagTransitionCount(self, fromTag : str, toTag: str):
        if fromTag in self.tagTransitionCount and toTag in self.tagTransitionCount[fromTag]:
            return self.tagTransitionCount[fromTag][toTag]
        return 0
        
    def getTransitionProbablity(self, fromTag: str, toTag : str):
        tagToTagCount = 0
        tagOccurences = 0
        if fromTag in self.tagTransitionCount and toTag in self.tagTransitionCount[fromTag]:
            tagToTagCount = self.tagTransitionCount[fromTag][toTag]
        
        if fromTag in self.tagCount:
            tagOccurences = self.tagCount[fromTag]
        
        # if tagOccurences > 0:
        #     return float(tagToTagCount) / float(tagOccurences)
        # return 0

        #laplacian
        return float(tagToTagCount + 1) / float(tagOccurences + 12) #12 je broj
    
    def getWordCount(self, word : str):
        if(word in self.wordCount):
            return self.wordCount[word]
        return 0

    def getTagsForWord(self, word:str):
        wordTag = {}
        if word in self.wordTagCount:
            wordTag = self.wordTagCount[word]
        return list(wordTag.keys())
    
    def getTagWordCount(self, tag:str, word:str):
        if tag in self.tagWordCount and word in self.tagWordCount[tag]:
            return self.tagWordCount[tag][word]
        return 0

    
    def getWordTagCount(self, tag:str, word:str):
        if word in self.wordTagCount and tag in self.wordTagCount[word]:
            return self.wordTagCount[word][tag]
        return 0
    
    #zadnja promjena
    def incrementTagCount(self, tag:str):
        if tag in self.tagCount:
            self.tagCount[tag] += 1
        else:
            self.tagCount[tag] = 1
        self.totalTagCount += 1

    def incrementTagTransitionCount(self, fromTag:str, toTag:str):
        if fromTag not in self.tagTransitionCount:
            self.tagTransitionCount[fromTag] = {}
        count = 1
        if toTag in self.tagTransitionCount[fromTag]:
            count += self.tagTransitionCount[fromTag][toTag]
        self.tagTransitionCount[fromTag][toTag] = count

    def incrementTagStartCount(self, tag:str):
        if tag in self.tagStartCount:
            self.tagStartCount[tag] += 1
        else:
            self.tagStartCount[tag] = 1
        self.sentenceCount += 1
        

    def incrementWordCount(self, word:str):
        if word in self.wordCount:
            self.wordCount[word] += 1
        else:
            self.wordCount[word] = 1

    def incrementTagWordCount(self, tag:str, word:str):
        if tag not in self.tagWordCount:
            self.tagWordCount[tag] = {}
        
        tWCount = 1
        if word in self.tagWordCount[tag]:
            tWCount += self.tagWordCount[tag][word]
        self.tagWordCount[tag][word] = tWCount

        if word not in self.wordTagCount:
            self.wordTagCount[word] = {}
        
        wTcount = 1
        if tag in self.wordTagCount[word]:
            wTcount += self.wordTagCount[word][tag]
        
        self.wordTagCount[word][tag] = wTcount

    def getEmissionProbability(self, tag : str, word : str):
        tagAndWordCount = 0
        tagOccurences = 0
        
        if tag in self.tagWordCount and word in self.tagWordCount[tag]:
            tagAndWordCount = self.tagWordCount[tag][word]
        
        if tag in self.tagCount:
            tagOccurences = self.tagCount[tag]
        
        if tagOccurences > 0:
            return float(tagAndWordCount) / float(tagOccurences)
        
        #laplacian, nije radio najbolje
        return 1.0 / 12.0 #12 je broj tagova

        #uzmi najvjerojatniji tag, isto nije radilo najbolje
        #return float(self.tagCount[max(self.tagCount, key=self.tagCount.get)]) / float(sum(self.tagCount.values()))
        
        #Imenica, isto nije radilo nabolje
        #return self.tagCount['NOUN']/sum(self.tagCount.values())

    def getStartProbability(self, tag:str):
        startCount = 0
        if tag in self.tagStartCount:
            startCount += self.tagStartCount[tag]
        
        return float(startCount) / float(self.sentenceCount)