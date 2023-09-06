from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, scoped_session, sessionmaker

engine = create_engine('sqlite:///ex3.db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Programmer(Base):
    __tablename__ = 'programmer'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    age = Column(Integer)
    email = Column(String(100))
    programmer_skills = relationship("ProgrammerSkills", back_populates="programmer")

    def __repr__(self):
        return f"Id: {self.id}, Name: {self.name}, Age: {self.age}, Email: {self.email}"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Skills(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    programmer_skills = relationship("ProgrammerSkills", back_populates="skills")

    def __repr__(self):
        return f"Id: {self.id}, Skill: {self.name}"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class ProgrammerSkills(Base):
    __tablename__ = 'programmer_skills'
    id = Column(Integer, primary_key=True)
    programmer_id = Column(Integer, ForeignKey('programmer.id'))
    skills_id = Column(Integer, ForeignKey('skills.id'))
    programmer = relationship(Programmer)
    skills = relationship(Skills)

    def __repr__(self):
        return (f"Id: {self.id}, Name: {self.programmer.name}, Age: {self.programmer.age},"
                f" Email: {self.programmer.email}, Skill_id: {self.skills.id}, Skill: {self.skills.name}")

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
