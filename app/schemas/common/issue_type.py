from app.schemas.base import BaseSchema


class IssueTypeOut(BaseSchema):
    id: int
    name: str

    class Config:
        from_attributes = True


class IssueTypeListResponse(BaseSchema):
    items: list[IssueTypeOut]
