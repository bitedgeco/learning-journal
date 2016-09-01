from sqlalchemy import (
    Column,
    # Index,
    Integer,
    Text,
    DateTime,
)

from .meta import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    date = Column(DateTime)
    body = Column(Text)


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
