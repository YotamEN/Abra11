from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, BIGINT, BYTEA, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
GENDER_ENUM = ENUM(("male", "female", "other"), name="gender_enum")


class Pose(Base):
    __tablename__ = "poses"
    user_id = Column(Integer, ForeignKey('user_snapshots.user_id'))
    translation = Column(ARRAY(BIGINT, dimensions=3), primary_key=True)
    rotation = Column(ARRAY(BIGINT, dimensions=3))

    def __repr__(self):
        return f"Pose<translation='{self.height}', rotation='{self.data}'>"


class ColorImage(Base):
    __tablename__ = "color_images"
    user_id = Column(Integer, ForeignKey('user_snapshots.user_id'))
    width = Column(Integer, primary_key=True)
    height = Column(Integer)
    data_path = Column(String)

    def __repr__(self):
        return f"ColorImage<width='{self.width}', height='{self.height}', " \
               f"data='{self.data_path}'>"


class DepthImage(Base):
    __tablename__ = "depth_images"
    user_id = Column(Integer, ForeignKey('user_snapshots.user_id'))
    width = Column(Integer, primary_key=True)
    height = Column(Integer)
    data_path = Column(String)

    def __repr__(self):
        return f"DepthImage<width='{self.width}', height='{self.height}', " \
               f"data='{self.data_path}'>"


class Feelings(Base):
    __tablename__ = "feelings"
    user_id = Column(Integer, ForeignKey('user_snapshots.user_id'))
    hunger = Column(FLOAT, primary_key=True)
    thirst = Column(FLOAT)
    exhaustion = Column(FLOAT)
    happiness = Column(FLOAT)

    def __repr__(self):
        return f"Feelings<hunger='{self.hunger}', thirst='{self.thirst}', " \
               f"exhaustion='{self.exhaustion}', happiness='{self.happiness}'>"


class Snapshot(Base):
    __tablename__ = 'user_snapshots'
    user_id = Column(Integer, ForeignKey('user.id'))
    datetime = Column(Date, primary_key=True)
    pose = relationship(Pose)
    color_image = relationship(ColorImage)
    depth_image = relationship(DepthImage)
    feelings = relationship(Feelings)

    def __repr__(self):
        return f"Snapshot<user_id='{self.user_id}', datetime='{self.datetime}', pose='{self.pose!r}'," \
               f" color_image='{self.color_image!r}', depth_image='{self.depth_image!r}'"


class User(Base):
    __tablename__ = 'user'
    id = Column(BIGINT, primary_key=True)
    name = Column(String)
    birthday = Column(Integer)
    gender = Column(GENDER_ENUM)  # FIXME
    snapshots = relationship(Snapshot, backref="user")

    def __repr__(self):
        return f"User<id='{self.id}', name='{self.name}', birthday='{self.birthday}', gender='{self.gender}'>"
