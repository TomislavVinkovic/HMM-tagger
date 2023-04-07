from AugmentedSuffixTree import AugmentedSuffixTree
from BigramModel import BigramModel
import math

class AugmentedSuffixTreeFactory:
    def __init__(self, bigramModel:BigramModel, maxSuffixLength, maxWordFrequency):
        self.MAX_SUFFIX_LENGTH = maxSuffixLength
        self.MAX_WORD_FREQUENCY = maxWordFrequency

        self.model = bigramModel
    
    def buildUpperCaseTree(self) -> AugmentedSuffixTree:
        #words that start with an upper case letter
        words = [word for word in list(filter(lambda word: word[0].upper() == word[0], self.model.wordCount.keys()))]
        return self.buildTree(words)
    
    def buildLowerCaseTree(self) -> AugmentedSuffixTree:
        #words that start with an lower case letter
        words = [word for word in list(filter(lambda word: word[0].lower() == word[0], self.model.wordCount.keys()))]
        return self.buildTree(words)
    
    def buildTree(self, words):
        suffixWords = []
        for word in words:
            if self.model.getWordCount(word) < self.MAX_WORD_FREQUENCY:
                suffixWords.append(word)
        
        tags = self.model.getTags()
        suffixTagCount = {}
        for tag in tags:
            for word in suffixWords:
                stc = 0
                if tag in suffixTagCount:
                    stc = suffixTagCount[tag]
                count = self.model.getWordTagCount(tag, word) + stc
                stc[tag] = count
        
        suffixTags = list(suffixTagCount.keys())
        totalTags = 0
        for tag in suffixTags:
            totalTags += suffixTagCount.get(tag)
        
        tree = AugmentedSuffixTree()
        for word in suffixWords:
            wordTags = self.model.getTagsForWord(word)
            for tag in wordTags:
                suffixLength = min(self.MAX_SUFFIX_LENGTH, len(word))
                i = len(word) - suffixLength
                tree.addSuffix(word[i:], tag)
        
        theta = self.calculateTheta(suffixTags, suffixTagCount, totalTags)

        return tree
    
    def calculateTheta(self, suffixTags, suffixTagCount, totalTagCount):
        tagProbs = [float(suffixTagCount[tag]) / float(totalTagCount) for tag in suffixTags]
        avg = float(sum(tagProbs)) / float(len(suffixTags))
        squaredDiff = [math.pow(prob - avg, 2) for prob in tagProbs]

        return float(sum(squaredDiff)) / float(len(suffixTags) - 1)
