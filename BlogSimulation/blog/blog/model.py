from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, create_engine, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TEXT, TINYINT
from sqlalchemy.orm import relationship, sessionmaker
from . import config

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return "<User id={}, name={}, email={}>".format(self.id, self.name, self.email)


class PostBlog(Base):
    __tablename__ = 'postblog'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    postdate = Column(DateTime, nullable=False)
    authorid = Column(Integer, ForeignKey('user.id'), nullable=False)
    hits = Column(BigInteger, nullable=False,default=0)

    author = relationship('User')
    content = relationship('Content', uselist=False)

    def __repr__(self):
        return '<PostBlog id={}, title={}, authorid={}>'.format(self.id, self.title, self.authorid)


class Content(Base):
    __tablename__ = 'content'

    id = Column(BigInteger, ForeignKey('postblog.id'), nullable=False, primary_key=True)
    content = Column(TEXT, nullable=False)

    def __repr__(self):
        return '<Content id={}, content={}>'.format(self.id, self.content[:20])


class Dig(Base):
    __tablename__ = 'dig'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    blog_id = Column(BigInteger, ForeignKey('postblog.id'), nullable=False)
    state = Column(TINYINT, nullable=False, default=0, comment='0 bury, 1 dig')
    putdate = Column(DateTime, nullable=False)

    user = relationship('User')

    __table_args__ = (UniqueConstraint('user_id', 'blog_id'),)


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tag = Column(String(10), nullable=False, unique=True)


class BlogTag(Base):
    __tablename__ = 'blogtags'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    blog_id = Column(BigInteger, ForeignKey('postblog.id'), nullable=False)
    tag_id = Column(BigInteger, ForeignKey('tags.id'), nullable=False)

    __tableargs__ = (PrimaryKeyConstraint('blog_id', 'tag_id'),)

    tag = relationship('Tags')
    blog = relationship('PostBlog')


engine = create_engine(config.URL, echo=config.DATABASE_DEBUG)

Session = sessionmaker(bind=engine)

session = Session()


def createtables(tables=None):
    Base.metadata.create_all(engine,tables)

def droptables():
    Base.metadata.drop_all(engine)
