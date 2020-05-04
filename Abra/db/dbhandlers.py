from contextlib import contextmanager
from furl import furl
from abra.db.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.errors import *

SUPPORTED_DBS = ["postgres"]


class DBHandler:

    def __init__(self, db_url):
        f_url = furl(db_url)
        # choose mq_h scheme:
        if f_url.scheme == "postgresql":
            self.__dict__ = PostgresDBHandler(db_url).__dict__  # FIXME
        else:
            raise UnsupportedDataBaseError(f'ERROR: only supported data bases are: {SUPPORTED_DBS!r}')


class PostgresDBHandler:

    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy_tables()

    @contextmanager
    def session_scope(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def destroy_tables(self):
        Base.metadata.drop_all(self.engine)

    # ---------------------------- #
    # ------ inserting data ------ #
    # ---------------------------- #

    def create_new_user(self, user_id, name, birthday, gender):
        with self.session_scope() as s:
            user = User(id=user_id, name=name, birthday=birthday, gender=gender)
            s.add(user)

    def update_user_pose(self, user_id, datetime, translation, rotation):
        with self.session_scope() as s:
            pose = Pose(translation=translation, rotation=rotation)
            snapshot = self.get_relevant_snapshot(s, user_id, datetime)
            snapshot.pose.extend([pose])

    def update_user_color_image(self, user_id, datetime, width, height, data_path):
        with self.session_scope() as s:
            c_image = ColorImage(width=width, height=height, data_path=data_path)
            snapshot = self.get_relevant_snapshot(s, user_id, datetime)
            snapshot.color_image.extend([c_image])

    def update_user_depth_image(self, user_id, datetime, width, height, data_path):
        with self.session_scope() as s:
            d_image = DepthImage(width=width, height=height, data_path=data_path)
            snapshot = self.get_relevant_snapshot(s, user_id, datetime)
            snapshot.depth_image.extend([d_image])

    def update_user_feelings(self, user_id, datetime, hunger, thirst, exhaustion, happiness):
        with self.session_scope() as s:
            feelings = Feelings(hunger=hunger, thirst=thirst, exhaustion=exhaustion, happiness=happiness)
            snapshot = self.get_relevant_snapshot(s, user_id, datetime)
            snapshot.feelings.extend([feelings])

    # ------------------------------- #
    # ------ querying for data ------ #
    # ------------------------------- #

    def get_relevant_snapshot(self, session, user_id, datetime):
        snapshot = session.query(Snapshot).filter(
            Snapshot.user_id == user_id,
            Snapshot.datetime == datetime)
        if not session.query(snapshot.exists()):
            user = session.query(User).filter(User.id == user_id)
            snapshot = Snapshot(datetime=datetime)
            user.snapshots.extend([snapshot])
        return snapshot

    def get_all_users(self):
        with self.session_scope() as s:
            users = s.query(User).all()
        return users

    def get_user(self, user_id):
        with self.session_scope() as s:
            user = s.query(User).filter(User.id == user_id)
        return user

    def get_user_snapshots(self, user_id):
        with self.session_scope() as s:
            snapshots = s.query(Snapshot).filter(Snapshot.user_id == user_id)
        return snapshots

    def get_snapshot(self, user_id, datetime):
        with self.session_scope() as s:
            snapshot = s.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.datetime == datetime)
        return snapshot

    def get_snapshot_result(self, user_id, datetime, result_name):
        snapshot = self.get_snapshot(user_id, datetime)
        if result_name == "pose":
            return snapshot.pose
        elif result_name == "color-image":
            return snapshot.color_image
        elif result_name == "depth-image":
            return snapshot.depth_image
        elif result_name == "feelings":
            return snapshot.feelings
        else:
            return None
