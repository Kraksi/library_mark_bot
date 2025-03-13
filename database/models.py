from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text



class Base(DeclarativeBase):
    ...

class Map(Base):
    __tablename__ = 'map'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    tp: Mapped[int] = mapped_column(int)
    status: Mapped[int] = mapped_column(int)
