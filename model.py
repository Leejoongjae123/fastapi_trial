# coding: utf-8
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE


class PostingTable(Base):
    __tablename__ = 'posting'
    id = Column(Integer, primary_key=True)
    platform = Column(String(100))
    region = Column(String(100))
    dday=Column(String(100))
    title = Column(String(100))
    demandCount = Column(String(100))
    applyCount = Column(String(100))
    imageUrl = Column(String(100))
    url = Column(String(100))
    myImage = Column(String(100))

    # def __init__(self, name, fullname, password):
    #     self.name = name
    #     self.fullname = fullname
    #     self.password = password
    #
    # def __repr__(self):
    #     return "<Tada('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)


class Posting(BaseModel):
    platform : str
    region: str
    dday:str
    title:str
    demandCount:str
    imageUrl:str
    url:str
    myImage:str
    applyCount:str


def main():
    # Table 없으면 생성
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main()