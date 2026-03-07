import enum


class IssueStatusName(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    DECLINED = "DECLINED"


INITIAL_ISSUE_STATUS = IssueStatusName.NEW
