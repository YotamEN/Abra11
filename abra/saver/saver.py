from ..common import *
from abra.db.dbhandlers import PostgresDBHandler
import json
from abra.mq.mq_handlers import RabbitMQHandler
from abra.errors import UnsupportedTopic


class Saver:

    def __init__(self, db_url):
        self.db_handler = PostgresDBHandler(db_url)

    def register_to_topics(self, topics, mq_url):
        for topic in topics:
            if topic not in TOPICS:
                raise UnsupportedTopic(f"ERROR: topic '{topic}' is unrecognized. Known topics: {TOPICS!r}")

        def callback(ch, method, props, body):
            self.save_wrapper(body)

        mq_h = RabbitMQHandler(mq_url)
        mq_h.consume_parsed_data_exchange_by_topic(callback=callback, topics=topics)

    def register_to_all_topics(self, mq_url):
        self.register_to_topics(TOPICS, mq_url)

    def save_wrapper(self, data):
        loaded_data = json.loads(data)
        topic = loaded_data[TOPIC_KEY]
        self.save(topic, data)

    def save(self, topic, data):
        data_to_save = json.loads(data)
        if topic == USER_TOPIC:
            self.save_user(data_to_save)
        elif topic == POSE_TOPIC:
            self.save_pose(data_to_save)
        elif topic == C_IMAGE_TOPIC:
            self.save_c_image(data_to_save)
        elif topic == D_IMAGE_TOPIC:
            self.save_d_image(data_to_save)
        elif topic == FEELINGS_TOPIC:
            self.save_feelings(data_to_save)

    def save_user(self, data):
        user_id = data[USER_ID_KEY]
        name = data[USERNAME_KEY]
        b_day = data[BIRTHDAY_KEY]
        gender = data[GENDER_KEY]
        print(f"Saving user: {name}")
        self.db_handler.create_new_user(user_id=user_id, name=name, birthday=b_day, gender=GENDERS[gender])

    def save_pose(self, data):
        user_id = data[USER_ID_KEY]
        snap_id = data[SNAPSHOT_ID_KEY]
        data = data[PARSED_DATA_KEY]
        datetime = data[DATETIME_KEY]
        trans = [data[TRANS_X_KEY], data[TRANS_Y_KEY], data[TRANS_Z_KEY]]
        rot = [data[ROT_X_KEY], data[ROT_Y_KEY], data[ROT_Z_KEY]]
        # print(f"SAVING POSE: User {user_id}, date: {datetime}, trans:{trans!r}, rot: {rot!r}")
        # print("Saving Pose")
        self.db_handler.update_user_pose(user_id=user_id, datetime=datetime, translation=trans, rotation=rot,
                                         snapshot_id=snap_id)

    def save_c_image(self, data):
        user_id = data[USER_ID_KEY]
        snap_id = data[SNAPSHOT_ID_KEY]
        data = data[PARSED_DATA_KEY]
        datetime = data[DATETIME_KEY]
        width = data[WIDTH_KEY]
        height = data[HEIGHT_KEY]
        data_p = data[RESULT_URL_KEY]
        # print("Saving C_Image")
        self.db_handler.update_user_color_image(user_id=user_id, datetime=datetime, width=width, height=height,
                                                data_path=data_p, snapshot_id=snap_id)

    def save_d_image(self, data):
        user_id = data[USER_ID_KEY]
        snap_id = data[SNAPSHOT_ID_KEY]
        data = data[PARSED_DATA_KEY]
        datetime = data[DATETIME_KEY]
        width = data[WIDTH_KEY]
        height = data[HEIGHT_KEY]
        data_p = data[RESULT_URL_KEY]
        # print("Saving D_Image")
        self.db_handler.update_user_depth_image(user_id=user_id, datetime=datetime, width=width, height=height,
                                                data_path=data_p, snapshot_id=snap_id)

    def save_feelings(self, data):
        user_id = data[USER_ID_KEY]
        snap_id = data[SNAPSHOT_ID_KEY]
        data = data[PARSED_DATA_KEY]
        datetime = data[DATETIME_KEY]
        hunger = data[HUNGER_KEY]
        thirst = data[THIRST_KEY]
        exh = data[EXHAUSTION_KEY]
        happ = data[HAPPINESS_KEY]
        path = data[RESULT_URL_KEY]
        # print("Saving Feelings")
        self.db_handler.update_user_feelings(user_id=user_id, datetime=datetime, hunger=hunger, thirst=thirst,
                                             exhaustion=exh, happiness=happ, path=path, snapshot_id=snap_id)

