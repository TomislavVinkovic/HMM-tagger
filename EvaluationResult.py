class EvaluationResult:
    def __init__(self, sententes, sentenceTags, goldenTaggedSentences) -> None:
        self.sentences = sententes
        self.sentenceTags = sentenceTags
        self.goldenTaggedSentences = goldenTaggedSentences