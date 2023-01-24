from __future__ import annotations
from sqlalchemy import Column, Table, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


page_to_link = Table(
    "page_to_link",
    Base.metadata,
    Column("page_id", Integer, ForeignKey("page.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("page.id"), primary_key=True),
)


class Page(Base):
    __tablename__ = "page"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    links: Mapped[list[Page]] = relationship(
        secondary=page_to_link,
        primaryjoin=id==page_to_link.c.page_id,
        secondaryjoin=id==page_to_link.c.link_id,
        backref="pages"
    )
