from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, BIGINT, FLOAT, DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship

Base = declarative_base()


class Pose(Base):
    __tablename__ = "pose"
    id = Column(Integer, primary_key=True, unique=True)
    snapshot_id = Column(BIGINT)  # ForeignKey('user_snapshot.id'))
    translation_x = Column(DOUBLE_PRECISION)
    translation_y = Column(DOUBLE_PRECISION)
    translation_z = Column(DOUBLE_PRECISION)
    rotation_x = Column(DOUBLE_PRECISION)
    rotation_y = Column(DOUBLE_PRECISION)
    rotation_z = Column(DOUBLE_PRECISION)

    def __repr__(self):
        return f"Pose<translation='{self.height}', rotation='{self.data}'>"


class ColorImage(Base):
    __tablename__ = "color_image"
    id = Column(Integer, primary_key=True, unique=True)
    snapshot_id = Column(BIGINT)  # ForeignKey('user_snapshot.id'))
    width = Column(Integer, unique=False)
    height = Column(Integer, unique=False)
    data_path = Column(String)

    def __repr__(self):
        return f"ColorImage<width='{self.width}', height='{self.height}', " \
               f"data='{self.data_path}'>"


class DepthImage(Base):
    __tablename__ = "depth_image"
    id = Column(Integer, primary_key=True, unique=True)
    snapshot_id = Column(BIGINT)  # ForeignKey('user_snapshot.id'))
    width = Column(Integer, unique=False)
    height = Column(Integer, unique=False)
    data_path = Column(String)

    def __repr__(self):
        return f"DepthImage<width='{self.width}', height='{self.height}', " \
               f"data='{self.data_path}'>"


class Feelings(Base):
    __tablename__ = "feelings"
    id = Column(Integer, primary_key=True, unique=True)
    snapshot_id = Column(BIGINT)  # ForeignKey('user_snapshot.id'))
    hunger = Column(FLOAT)
    thirst = Column(FLOAT)
    exhaustion = Column(FLOAT)
    happiness = Column(FLOAT)
    path = Column(String)

    def __repr__(self):
        return f"Feelings<hunger='{self.hunger}', thirst='{self.thirst}', " \
               f"exhaustion='{self.exhaustion}', happiness='{self.happiness}'>"


class Snapshot(Base):
    __tablename__ = 'user_snapshot'
    id = Column(BIGINT, primary_key=True, unique=True)
    user_id = Column(Integer)  # ForeignKey('user.id'))
    datetime = Column(BIGINT)

    def __repr__(self):
        return f"Snapshot<user_id='{self.user_id}',\n datetime='{self.datetime}'\nsnapshot_id='{self.id}'"


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    birthday = Column(Integer)
    gender = Column(ENUM("female", "male", "other", name="gender_enum", create_type=False))
    # snapshots = relationship("Snapshot", backref="user")  # , foreign_keys=[id])

    def __repr__(self):
        return f"User<id='{self.id}', name='{self.name}', birthday='{self.birthday}', gender='{self.gender}'>"
