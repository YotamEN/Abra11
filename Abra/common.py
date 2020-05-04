# General:
SUCCESS = 0
FAIL = 1

# ********************* #

# Connections:
LOCAL_HOST = '127.0.0.1'
APP_SERVER_PORT = 8000
APP_SERVER_HOST = LOCAL_HOST
API_SERVER_PORT = 5000
API_SERVER_HOST = LOCAL_HOST
GUI_SERVER_HOST = LOCAL_HOST
GUI_SERVER_PORT = 5050
DATABASE_DEFAULT_URL = 'postgresql://127.0.0.1:5432'

# ********************* #

#  keys for dict returned by parsers:
PARSER_NAME_KEY = "parser_name"
# User: --------
USER_ID_KEY = "user_id"
USERNAME_KEY = "username"
BIRTHDAY_KEY = "birthday"
GENDER_KEY = "gender"
# Snapshot: --------
DATETIME_KEY = "datetime"
# Pose:
TRANS_X_KEY = "trans_x"
TRANS_Y_KEY = "trans_y"
TRANS_Z_KEY = "trans_z"
ROT_X_KEY = "rot_x"
ROT_Y_KEY = "rot_y"
ROT_Z_KEY = "rot_z"
# Image
WIDTH_KEY = "width"
HEIGHT_KEY = "height"
IMAGE_DATA_KEY = "image_data"
# Feelings
HUNGER_KEY = "hunger"
THIRST_KEY = "thirst"
EXHAUSTION_KEY = "exhaustion"
HAPPINESS_KEY = "happiness"

# API/ CLI/ GUI keys
SNAPSHOT_ID_KEY = "snapshot_id"
AVAILABLE_RESULTS_KEY = "available_results"
USER_URL_KEY = "user_url"
USER_SNAPSHOTS_URL_KEY = "user_snapshots_url"
SNAPSHOTS_LIST_KEY = "snapshots_list"
# ********************* #

# Topics for mq:
USER_TOPIC = "user"
POSE_TOPIC = "pose"
C_IMAGE_TOPIC = "color-image"
D_IMAGE_TOPIC = "depth-image"
FEELINGS_TOPIC = "feelings"
TOPICS = [USER_TOPIC, POSE_TOPIC, C_IMAGE_TOPIC, D_IMAGE_TOPIC, FEELINGS_TOPIC]

# ********************* #

# Image data directory:
C_IMG_DATA_DIR = "./images/c_images/"
D_IMG_DATA_DIR = "./images/d_images/"

# ********************* #


def create_snapshot_id(user_id, date):
    return str(user_id)+str(date)
