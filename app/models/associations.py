from sqlalchemy import Table, Column, ForeignKey
from app.core.db import Base

definitions_meanings = Table(
    "definitions_meanings",
    Base.metadata,
    Column("definition_id", ForeignKey("definitions.id"), primary_key=True),
    Column("meaning_id", ForeignKey("meanings.id"), primary_key=True),
)
