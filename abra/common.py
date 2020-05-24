# General:
SUCCESS = 0
FAIL = 1
UNDEFINED = -1

VOLUME_PATH = "./vol"
SNAPSHOT_JSON_FILE_NAME = "snap.json"
# ********************* #

# Connections:
LOCAL_HOST = '127.0.0.1'
ALL_INTF_HOST = '0.0.0.0'
CLIENT_DEFAULT_HOST = ALL_INTF_HOST
CLIENT_DEFAULT_PORT = 8000
APP_SERVER_PORT = 8000
APP_SERVER_HOST = ALL_INTF_HOST
API_SERVER_PORT = 5000
API_SERVER_HOST = LOCAL_HOST
GUI_SERVER_HOST = LOCAL_HOST
GUI_SERVER_PORT = 8080
DATABASE_DEFAULT_URL = 'postgresql://127.0.0.1:5432'

# ********************* #

#  keys for dict returned by parsers:
RESULT_URL_KEY = "result_url"
PARSER_NAME_KEY = "parser_name"
PARSED_DATA_KEY = "parsed_data"
TOPIC_KEY = "topic"
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
IMAGE_DATA_KEY = RESULT_URL_KEY
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
SNAPSHOT_URL_KEY = "snapshot_url"
RESULT_NAME_KEY = "result_name"

# ********************* #

FEELINGS = ["hunger", "thirst", "exhaustion", "happiness"]
GENDERS = ["male", "female", "other"]

# ********************* #
# Topics for mq:
USER_TOPIC = "user"
POSE_TOPIC = "pose"
C_IMAGE_TOPIC = "color-image"
D_IMAGE_TOPIC = "depth-image"
FEELINGS_TOPIC = "feelings"
TOPICS = [USER_TOPIC, POSE_TOPIC, C_IMAGE_TOPIC, D_IMAGE_TOPIC, FEELINGS_TOPIC]

# ********************* #

# directories and URLs:
C_IMG_DATA_DIR = "images/c_images"
D_IMG_DATA_DIR = "images/d_images"
POSE_DIR = "pose"
FEELINGS_DIR = "feelings"

# ********************* #

# db parameters:
DB_NAME = 'postgres'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'postgres'


