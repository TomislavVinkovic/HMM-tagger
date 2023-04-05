class EvaluationResult:
    def __init__(self, sententes, sentenceTags) -> None:
        self.sentences = sententes #list<list<string>>
        self.sentenceTags = sentenceTags #list<list<string>>