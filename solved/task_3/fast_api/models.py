from datetime import date

from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text())


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(String(100))
    deadline: Mapped[date] = mapped_column(Date)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    project: Mapped[Project] = relationship(foreign_keys=[project_id])
