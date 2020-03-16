from mind_read_protocol import Snapshot
import struct


class Reader:

    def __init__(self):
        self.user_id = 0
        self.username = 'None'
        self.user_birth_date = 0
        self.user_gender = 'o'


# FIXME - add try, except, finally and close file
class MindReader(Reader):

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._file = open(self._path, "rb")
        self.get_user_info(self._file)

    def __iter__(self):
        return self

    def __next__(self):
        return self.create_snapshot_from_file()

    def get_user_info(self, file):
        self.user_id = struct.unpack('<L', file.read(8))[0]
        username_length = struct.unpack('<I', file.read(4))[0]
        self.username = struct.unpack(f'<{username_length}s', file.read(username_length))[0]
        self.user_birth_date = struct.unpack('<I', file.read(4))[0]
        self.user_gender = struct.unpack('c', file.read(1))[0]

    def create_snapshot_from_file(self):
        timestamp = struct.unpack('<L', self._file.read(8))[0]
        translation = struct.unpack('<3d', self._file.read(8 * 3))
        rotation = struct.unpack('<4d', self._file.read(8 * 4))
        height, width = struct.unpack('<II', self._file.read(4 * 2))
        color_image = self._file.read(height*width*3)
        col_img_data = height, width, color_image
        height, width = struct.unpack('<II', self._file.read(4 * 2))
        depth_image = self._file.read(height*width*3)
        depth_img_data = height, width, depth_image
        user_feelings = struct.unpack('<4f', self._file.read(4 * 4))
        return Snapshot(timestamp, translation, rotation, col_img_data, depth_img_data, user_feelings)



