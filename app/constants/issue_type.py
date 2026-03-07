import enum


class IssueTypeName(str, enum.Enum):
    TYPO = "TYPO"
    AMBIGUITY = "AMBIGUITY"
    WRONG_TRANSLATION = "WRONG_TRANSLATION"
    POOR_AUDIO = "POOR_AUDIO"
    DISLIKE = "DISLIKE"
    OTHER = "OTHER"
