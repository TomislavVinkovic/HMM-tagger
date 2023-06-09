from queue import LifoQueue as Stack

class AugmentedSuffixTree:
    def __init__(self):
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
            self.tagCount[tag] = 1
        
    def getTagSuffixCount(self, tag:str):
        count = 0
        if tag in self.tagSuffixCount:
            count = self.tagSuffixCount[tag]
        return count
    
    def incrementTagSuffixCount(self, tag:str):
        if tag in self.tagSuffixCount:
            self.tagSuffixCount[tag] += 1
        else:
            self.tagSuffixCount[tag] = 1
    
    def get(self, letter:str):
        try:
            return self.nodes[letter]
        except:
            return None

    def put(self, key:str, val):
        self.nodes[key] = val
    
    def getSubTree(self, suffix:str):
        subTree = self
        for i in range(0, len(suffix)):
            letter = suffix[i:]
            if not subTree.containsKey(letter):
                subTree.put(letter, AugmentedSuffixTree())
            subTree = subTree.get(letter)
        return subTree

    def addSuffix(self, suffix:str, tag:str):
        self.incrementTagCount(tag)
        for i in range(0, len(suffix)):
            subTree = self.getSubTree(suffix[i:])
            subTree.incrementTagSuffixCount(tag)
            subTree.incrementCount()
            self.totalCount += 1
            self.totalTagCount += 1

    def containsKey(self, key:str):
        #is the key in the tree
        return key in self.nodes
    
    def getCount(self):
        return self.suffixCount

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
        subTree = self.getSubTree(suffix)
        suffixCount = subTree.getCount()

        return float(suffixCount) / float(self.totalCount)

    def getTagProbability(self, suffix:str, tag:str):
        tagCount = self.getTagCount(tag)
        return float(tagCount) / float(self.totalTagCount)