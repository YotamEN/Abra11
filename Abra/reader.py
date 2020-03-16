# from mind_read_protocol import Snapshot
from abra_pb2 import User, Snapshot
import gzip
import struct

UNDEFINED = -1
MSG_SIZE_HEADER = 4
DOUBLE_SIZE = 8
UINT_64_SIZE = 8
UINT_32_SIZE = 4
FLOAT_SIZE = 4

# TODO add context manager for errors
class Reader:

    def __init__(self, path, next_func=None, endian='little'):
        self._path = path
        self._next_func = next_func
        self._endian = endian

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_func is None:
            return None
        return self._next_func()


# FIXME - add try, except, finally and close file
class MindReader(Reader):

    def __init__(self, path):
        self.user = None
        self.user_id = UNDEFINED
        self.username = ""
        self.user_gender = ""
        self.user_birth_date = UNDEFINED

        super().__init__(path, self.get_snapshot)
        self._file = gzip.open(self._path)
        self.get_user_info()

    def get_user_info(self):
        num_of_bytes = self.get_msg_length()
        user_data_raw = self._file.read(num_of_bytes)
        user = User.FromString(user_data_raw)
        self.user = user
        self.user_id = user.user_id
        self.username = user.username
        self.user_gender = user.gender
        self.user_birth_date = user.birthday

    def get_snapshot(self):
        num_of_bytes = self.get_msg_length()
        user_data_raw = self._file.read(num_of_bytes)
        snapshot = Snapshot.FromString(user_data_raw)
        return snapshot

    def get_msg_length(self):
        length_in_bytes = self._file.read(MSG_SIZE_HEADER)
        length_int = int.from_bytes(length_in_bytes, byteorder=self._endian)
        return length_int



