from Matrix import Matrix
from AugmentedSuffixTree import AugmentedSuffixTree as SuffixTree
from SuffixStats import SuffixStats
import numpy as np
import math
class Viterbi:
    def __init__(self, bigramModel, upperCaseSuffixTree : SuffixTree, lowerCaseSuffixTree : SuffixTree, maxSuffixLength : int) -> None:
        self.model = bigramModel
        self.upperCaseTree = upperCaseSuffixTree
        self.lowerCaseTree = lowerCaseSuffixTree
        self.maxSuffixLength = maxSuffixLength

        self.tags = list(self.model.getTags().keys())
        self.numTags = len(self.tags)

    def run(self, sentence):
        sentenceLength = len(sentence)
        ppMatrix = Matrix(self.numTags, sentenceLength, 'float')
        backPointer = Matrix(self.numTags, sentenceLength, 'int')

        for state in range(0, self.numTags):
            timeStep = 0
            prob = float(self.model.getStartProbability(self.tags[state]))
            word = sentence[timeStep]
            emmisionProb = float(self.getEmissionProbability(state, word))
            ppMatrix.set(state, timeStep, prob * emmisionProb)
            backPointer.set(state, timeStep, -1)

        for timeStep in range(1, sentenceLength):
            word = sentence[timeStep]
            for state in range(0, self.numTags):
                maxProb = 0.0
                maxPrevState = 0
                for prevState in range(0, self.numTags):
                    if self.model.getTagTransitionCount(self.tags[prevState], self.tags[state]) > 0:
                        transitionProb = float(self.model.getTransitionProbablity(self.tags[prevState], self.tags[state]))
                        prevProb = ppMatrix.get(prevState, timeStep - 1)
                        if maxProb < transitionProb * prevProb:
                            maxProb = transitionProb * prevProb
                            maxPrevState = prevState
                emmisionProb = float(self.getEmissionProbability(state, word))
                ppMatrix.set(state, timeStep, maxProb + emmisionProb)
                backPointer.set(state, timeStep, maxPrevState)

        return self.getWordTags(ppMatrix, backPointer, sentenceLength)


    def getEmissionProbability(self, state : int, word : str):
        return self.model.getEmissionProbability(self.tags[state], word)
    
        #iz nekog razloga, niti suffixTree pristup nije radio dobro
        # stateProbs = self.getSuffixStats(word)
        # return stateProbs[state]
    
    #ova metoda vraca najbolju sekvencu tagova iz backpointer matrice
    def getWordTags(self, ppMatrix : Matrix, backPointer : Matrix, sentenceLength : int):
        bestPathPointer = 0
        for state in range(1, self.numTags):
            timeStep = sentenceLength - 1
            if(ppMatrix.get(state, timeStep) > ppMatrix.get(bestPathPointer, timeStep)):
                bestPathPointer = state
        
        bestPath = np.zeros(sentenceLength, dtype=int)
        bestPath[sentenceLength - 1] = bestPathPointer
        for timeStep in range(sentenceLength - 2, -1, -1):
            nextTimeStep = timeStep + 1
            bestPath[timeStep] = backPointer.get(bestPath[nextTimeStep], nextTimeStep)
        
        #lista stringova
        wordTags = []
        for timeStep in range (0, sentenceLength):
            wordTags.append(self.tags[bestPath[timeStep]])
        
        return wordTags

    def getSuffixStats(self, word : str):
        numTags = len(self.tags)

        #<Integer, Double>
        stateProbs = {}
        for state in range(0, numTags):
            tag = self.tags[state]
            suffixLength : int = min(self.maxSuffixLength, len(word))

            startingIndex = len(word) - suffixLength
            suffix = word[:startingIndex]

            stats = None
            if(word[0] == word[0].upper()):
                stats = SuffixStats(self.upperCaseTree, suffix, tag)
            else:
                stats = SuffixStats(self.lowerCaseTree, suffix, tag)
            
            #just in case that the tag never occurs in the tree
            #maybe i will need to implement laplacian here
            probWordIsTag = 0.0
            if stats.tagProb > 0.0:
                probWordIsTag = stats.tagSuffixProb * stats.suffixProb / stats.tagProb
            
            stateProbs[state] = probWordIsTag
        return stateProbs