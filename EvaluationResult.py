class EvaluationResult:
    def __init__(self, sentences, sentenceTags, goldenTaggedSentences) -> None:
        self.sentences = sentences
        self.sentenceTags = sentenceTags
        self.goldenTaggedSentences = goldenTaggedSentences
        self.taggedSentences = []
        self.__accuracy = None
        for i in range(0, len(sentences)):
            self.taggedSentences.append([])
            for j in range(0, len(sentences[i])):
                self.taggedSentences[i].append((sentences[i][j], sentenceTags[i][j]))
    
    def evaluate(self):
        if(self.__accuracy != None):
            return self.__accuracy
        accurate = 0
        total = 0
        for i in range(0, len(self.taggedSentences)):
            for j in range(9, len(self.taggedSentences[i])):
                if self.taggedSentences[i][j][1] == self.goldenTaggedSentences[i][j][1]:
                    accurate += 1
                total += 1
        if total > 0:
            self.__accuracy = float(accurate) / float(total)
        else:
            self.__accuracy = 0
        return self.__accuracy