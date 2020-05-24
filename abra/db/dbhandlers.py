from abra.common import DB_PASSWORD, DB_USERNAME, DB_NAME
from contextlib import contextmanager
from furl import furl
from abra.db.models import *
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from abra.errors import *

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
        f_url = furl(db_url)
        db_uri = f'postgres+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{f_url.host}:{f_url.port}/{DB_NAME}'
        print(db_uri)
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.counter = {"pose": 0, "color-image": 0, "depth-image": 0, "feelings": 0}

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

    def update_user_pose(self, user_id, datetime, translation, rotation, snapshot_id):
        self.make_sure_snapshot_exists(user_id, datetime, snapshot_id)
        with self.session_scope() as s:
            self.counter["pose"] += 1
            pose = Pose(id=self.counter["pose"], translation_x=translation[0], translation_y=translation[1],
                        translation_z=translation[2], rotation_x=rotation[0], rotation_y=rotation[1],
                        rotation_z=rotation[2], snapshot_id=snapshot_id)
            s.add(pose)

    def update_user_color_image(self, user_id, datetime, width, height, data_path, snapshot_id):
        self.make_sure_snapshot_exists(user_id, datetime, snapshot_id)
        with self.session_scope() as s:
            self.counter["color-image"] += 1
            c_image = ColorImage(id=self.counter["color-image"], width=width, height=height, data_path=data_path,
                                 snapshot_id=snapshot_id)
            s.add(c_image)

    def update_user_depth_image(self, user_id, datetime, width, height, data_path, snapshot_id):
        self.make_sure_snapshot_exists(user_id, datetime, snapshot_id)
        with self.session_scope() as s:
            self.counter["depth-image"] += 1
            d_image = DepthImage(id=self.counter["depth-image"], width=width, height=height, data_path=data_path,
                                 snapshot_id=snapshot_id)
            s.add(d_image)

    def update_user_feelings(self, user_id, datetime, hunger, thirst, exhaustion, happiness, path, snapshot_id):
        self.make_sure_snapshot_exists(user_id, datetime, snapshot_id)
        with self.session_scope() as s:
            self.counter["feelings"] += 1
            feelings = Feelings(id=self.counter["feelings"], hunger=hunger, thirst=thirst, exhaustion=exhaustion,
                                happiness=happiness, path=path, snapshot_id=snapshot_id)
            s.add(feelings)

    def make_sure_snapshot_exists(self, user_id, datetime, snap_id):
        with self.session_scope() as s:
            s_exists = s.query(exists().where(Snapshot.id == snap_id)).scalar()
            print(f"EXISTS: {s_exists}")
            if not s.query(exists().where(Snapshot.id == snap_id)).scalar():
                datetime = datetime & 0xffffffff
                snapshot = Snapshot(datetime=datetime, id=snap_id, user_id=user_id)
                s.add(snapshot)
            else:
                print("Snapshot exists!")

    # ------------------------------- #
    # ------ querying for data ------ #
    # ------------------------------- #

    def get_all_users(self):
        with self.session_scope() as s:
            users = s.query(User).all()
            s.expunge_all()
        return users

    def get_user(self, user_id):
        with self.session_scope() as s:
            user = s.query(User).filter(User.id == user_id).first()
            s.expunge_all()
        return user

    def get_user_snapshots(self, user_id):
        with self.session_scope() as s:
            snapshots = s.query(Snapshot).all()
            print(f"All snapshots: {snapshots}")
            snapshots = s.query(Snapshot).filter(Snapshot.user_id == user_id).all()
            print(f"User Snapshots: {snapshots}")
            s.expunge_all()
        return snapshots

    def get_snapshot(self, snapshot_id):
        with self.session_scope() as s:
            snapshot = s.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
            s.expunge_all()
        return snapshot

    def available_res(self, snapshot_id):
        res = []
        with self.session_scope() as s:
            if s.query(exists().where(Pose.snapshot_id == snapshot_id)).scalar():
                res.append("pose")
            if s.query(exists().where(ColorImage.snapshot_id == snapshot_id)).scalar():
                res.append("color-image")
            if s.query(exists().where(DepthImage.snapshot_id == snapshot_id)).scalar():
                res.append("depth-image")
            if s.query(exists().where(Feelings.snapshot_id == snapshot_id)).scalar():
                res.append("feelings")
        return res

    def get_snapshot_result(self, snapshot_id, result_name):
        with self.session_scope() as s:
            if result_name == "pose":
                res = s.query(Pose).filter(Pose.snapshot_id == snapshot_id).first()
            elif result_name == "color-image":
                res = s.query(ColorImage).filter(ColorImage.snapshot_id == snapshot_id).first()
            elif result_name == "depth-image":
                res = s.query(DepthImage).filter(DepthImage.snapshot_id == snapshot_id).first()
            elif result_name == "feelings":
                res = s.query(Feelings).filter(Feelings.snapshot_id == snapshot_id).first()
            else:
                res = None
            s.expunge_all()
        return res
