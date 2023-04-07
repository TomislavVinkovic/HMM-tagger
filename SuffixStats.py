from AugmentedSuffixTree import AugmentedSuffixTree as SuffixTree

class SuffixStats:
    
    def __init__(self, tree : SuffixTree, suffix, tag):
        self.tagSuffixProb = 0.0
        self.suffixProb = 0.0
        self.tagProb = 0.0

        while not tree.find(suffix) and len(suffix) > 0:
            suffix = suffix[1:]
        #TODO: Finish suffixStats class
        
