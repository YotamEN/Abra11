from ..common import *
from pathlib import Path
import uuid

"""
In order for you to add your own parser, follow the following steps:
    1. Give it a name! add it's name as a string to the list 'PARSER_NAMES' located after these instructions.
    2. Create a class in the marked section below, look for the "CREATE YOUR OWN PARSER" zone below.
        (If you really want to write it in a new file instead, that's ok.. just make sure to import it in __main__.py
        and put your file in the "parsers" directory)
    3. Inherit from BaseParser and override the "parse" method.
            The "parse" method must be implemented as follows:
            :input:  a Snapshot object as defined in abra.proto
            :output: a dict object with the parsed fields - 
                keys to be set according to the "field names" described in "common.py" file
                + a key and value for the parser name
                + a key and value for datetime
    4. You're good to go!
"""
UNDEFINED = -1
PARSER_NAMES = ["pose", "color_image", "depth_image", "feelings"]


# *************************************
# ************ Base Parser ************
# *************************************
class BaseParser:

    def __init__(self):
        pass

    # each parser must implement this function
    def parse(self, msg):
        pass

    def write_to_disk(self, path, data):
        unique_filename = str(uuid.uuid4())
        try:
            path = Path(path) / unique_filename
            with open(path, "wb") as f:
                f.write(data)
        except OSError as e:
            raise e
        except ValueError:
            return ''
        return unique_filename


# ******************************************
# ************ Specific Parsers ************
# ******************************************
class PoseParser(BaseParser):
    parser_name = "pose"

    def parse(self, msg):
        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            TRANS_X_KEY: msg.pose.translation.x,
            TRANS_Y_KEY: msg.pose.translation.y,
            TRANS_Z_KEY: msg.pose.translation.z,
            ROT_X_KEY: msg.pose.rotation.x,
            ROT_Y_KEY: msg.pose.rotation.y,
            ROT_Z_KEY: msg.pose.rotation.z
        }
        return ret_dict


class CImageParser(BaseParser):
    parser_name = "color_image"

    def parse(self, msg):
        data = msg.color_image.data
        path = self.write_to_disk(C_IMG_DATA_DIR, data)
        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            WIDTH_KEY: msg.color_image.width,
            HEIGHT_KEY: msg.color_image.height,
            IMAGE_DATA_KEY: path
        }
        return ret_dict


class DImageParser(BaseParser):
    parser_name = "depth_image"

    def parse(self, msg):
        data = msg.color_image.data
        path = self.write_to_disk(D_IMG_DATA_DIR, data)
        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            WIDTH_KEY: msg.depth_image.width,
            HEIGHT_KEY: msg.depth_image.height,
            IMAGE_DATA_KEY: path
        }
        return ret_dict


class FeelingsParser(BaseParser):
    parser_name = "feelings"

    def parse(self, msg):
        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            HUNGER_KEY: msg.feelings.hunger,
            THIRST_KEY: msg.feelings.thirst,
            EXHAUSTION_KEY: msg.feelings.exhaustion,
            HAPPINESS_KEY: msg.feelings.happiness
        }
        return ret_dict

# *************************    |     ******************************      |      *************************
# *************************   \|/    CREATE YOUR OWN PARSERS BELOW!     \|/     *************************
# *************************    V     ******************************      V      *************************
#
#
#
# *************************    A     ******************************      A      *************************
# *************************   /|\    CREATE YOUR OWN PARSERS ABOVE!     /|\     *************************
# *************************    |     ******************************      |      *************************
