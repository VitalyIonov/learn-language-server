from app.schemas.base import BaseSchema


class IssueStatusOut(BaseSchema):
    id: int
    name: str

    class Config:
        from_attributes = True
