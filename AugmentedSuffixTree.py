from queue import LifoQueue as Stack

class AugmentedSuffixTree:
    def __init__(self):
        self.theta = 0.0
        self.suffixCount = 0
        self.totalCount = 0
        self.totalTagCount = 0
        self.nodes = {} #contains subtrees
        self.tagCount = {}
        self.tagSuffixCount = {}
    
    def hasSuffix(self, suffix : str):
        sub = self.getSubTree(suffix)
        return sub.getCount() > 0

    def setTheta(self, theta:float):
         self.theta = float(theta)
    
    def incrementCount(self):
        self.suffixCount += 1
    
    def getTagCount(self, tag:str):
        count = 0
        if tag in self.tagCount:
            count = self.tagCount[tag]
        return count

    def incrementTagCount(self, tag:str):
        if tag in self.tagCount:
            self.tagCount[tag] += 1
        else:
            self.tagCount[tag] = 0
        
    def getTagSuffixCount(self, tag:str):
        count = 0
        if tag in self.tagSuffixCount:
            count = self.tagSuffixCount[tag]
        return count
    
    def incrementTagSuffixCount(self, tag:str):
        if tag in self.suffixCount:
            self.suffixCount[tag] += 1
        else:
            self.suffixCount[tag] = 0
    
    def get(self, letter:str):
        return self.nodes[letter]

    def put(self, key:str, val):
        self.nodes[key] = val
    
    def getSubTree(self, suffix:str):
        subTree = self
        for i in range(0, len(suffix)):
            letter = suffix[i:]
            if(subTree.containsKey(letter)):
                subTree.put(letter, AugmentedSuffixTree())
            subTree = subTree.get(letter)
        return subTree

    def addSuffix(self, suffix:str, tag:str):
        self.incrementTagCount(tag)
        for i in range(0, len(suffix)):
            subTree = self.getSubTree(suffix[i:])
            subTree.incrementTagSuffixCount(tag)
            self.totalCount += 1
            self.totalTagCount += 1

    def containsKey(self, key:str):
        #is the key found in the tree
        return (key in self.nodes)
    
    def getTagSuffixProbability(self, suffix:str, tag:str):
        mles = Stack()
        
        for i in range(0, len(suffix)):
            subTree = self.getSubTree(suffix[i:])
            suffixCount = subTree.getCount()
            tagSuffixCount = subTree.getTagSuffixCount(tag)

            mle = float(tagSuffixCount) / float(suffixCount)
            mles.put(mle)
        
        probability = 0.0
        while not mles.empty():
            probability = (mles.get() + (self.theta * probability)) / (1 + self.theta)
        
        return probability

    def getSuffixProbability(self, suffix:str):
        subTree = self.getSubtree(suffix)
        suffixCount = subTree.getCount()

        return float(suffixCount) / float(self.totalCount)

    def getTragProbability(self, suffix:str, tag:str):
        tagCount = self.getTagCount(tag)
        return float(tagCount) / float(self.totalTagCount)