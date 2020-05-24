from abra.common import *
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from PIL import Image
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
PARSER_NAMES = ["pose", "color-image", "depth-image", "feelings"]


def debug_print(parser_name):
    #  print(f"{parser_name} parsing!")
    return None


# *************************************
# ************ Base Parser ************
# *************************************
class BaseParser:

    def __init__(self):
        self.path = ''
        self.data = ''

    # each parser must implement this function
    def parse(self, msg):
        pass

    def write(self, path):
        with open(path, "w") as f:
            f.write(self.data)
        return path

    def write_to_disk(self):
        unique_filename = str(uuid.uuid4())
        try:
            path = Path(self.path) / unique_filename
            Path(path).mkdir(parents=True, exist_ok=True)
            return self.write(path)
        except OSError as e:
            raise e
        except ValueError:
            return ''


# ******************************************
# ************ Specific Parsers ************
# ******************************************
class PoseParser(BaseParser):
    parser_name = "pose"
    path = Path(VOLUME_PATH) / POSE_DIR

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
    parser_name = "color-image"
    path = Path(VOLUME_PATH) / C_IMG_DATA_DIR
    image = None

    def parse(self, msg):
        width, height, data = msg.color_image.width, msg.color_image.height, msg.color_image.data
        self.image = Image.frombytes(data=data, mode='RGB', size=(width, height))
        path = self.write_to_disk()
        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            WIDTH_KEY: msg.depth_image.width,
            HEIGHT_KEY: msg.depth_image.height,
            RESULT_URL_KEY: path
        }

        return ret_dict

    def write(self, path):
        path = path / "c_image.png"
        self.image.save(path, "PNG")
        return str(path.absolute())


class DImageParser(BaseParser):
    parser_name = "depth-image"
    path = Path(VOLUME_PATH) / D_IMG_DATA_DIR

    def parse(self, msg):
        width, height, data = msg.depth_image.width, msg.depth_image.height, msg.depth_image.data
        mat = np.array(data, dtype=np.float32)
        mat.shape = (width, height)
        plt.imshow(mat, cmap='hot', interpolation='nearest')
        path = self.write_to_disk()
        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            WIDTH_KEY: msg.depth_image.width,
            HEIGHT_KEY: msg.depth_image.height,
            RESULT_URL_KEY: path
        }

        return ret_dict

    def write(self, path):
        path = path / "d_image.png"
        plt.savefig(path)
        return str(path.absolute())


class FeelingsParser(BaseParser):
    parser_name = "feelings"
    path = Path(VOLUME_PATH) / FEELINGS_DIR

    def parse(self, msg):
        left = [i+1 for i in range(len(PARSER_NAMES))]
        tick_label = [feeling for feeling in FEELINGS]
        height = [msg.feelings.hunger, msg.feelings.thirst, msg.feelings.exhaustion, msg.feelings.happiness]
        colors = ['b', 'g', 'r', 'c', 'm']
        plt.bar(left, height, tick_label=tick_label, width=0.8, color=colors)
        plt.xlabel('Feelings')
        plt.ylabel('Intensity')
        path = self.write_to_disk()

        ret_dict = {
            PARSER_NAME_KEY: self.parser_name,
            DATETIME_KEY: msg.datetime,
            HUNGER_KEY: msg.feelings.hunger,
            THIRST_KEY: msg.feelings.thirst,
            EXHAUSTION_KEY: msg.feelings.exhaustion,
            HAPPINESS_KEY: msg.feelings.happiness,
            RESULT_URL_KEY: path
        }
        return ret_dict

    def write(self, path):
        path = path / "feelings.png"
        plt.savefig(path)
        return str(path.absolute())

# *************************    |     ******************************      |      *************************
# *************************   \|/    CREATE YOUR OWN PARSERS BELOW!     \|/     *************************
# *************************    V     ******************************      V      *************************
#
#
#
# *************************    A     ******************************      A      *************************
# *************************   /|\    CREATE YOUR OWN PARSERS ABOVE!     /|\     *************************
# *************************    |     ******************************      |      *************************
