import struct
from PIL import Image


class Snapshot:

    def __init__(self, timestamp, trans, rot, col_img_data, depth_img_data, feelings):
        self.timestamp = timestamp
        self.translation = trans
        self.rotation = rot
        self.color_image = self.get_image(*col_img_data)
        self.depth_image = self.get_image(*depth_img_data)
        self.user_feelings = feelings

    def get_image(self, height, width, msg):
        im = Image.frombytes('RGB', (width, height), msg)
        b, g, r = im.split()
        im = Image.merge('RGB', (r, g, b))
        return im

    def get_feelings(self, msg):
        feelings = struct.unpack('<4f', msg)
        return feelings


class Hello:

    def __init__(self, user_id, username, user_birth_date, user_gender):
        self.user_id = user_id
        self.username = username
        self.user_birth_date = user_birth_date
        self.user_gender = user_gender

    def serialize(self):
        return struct.pack(f'<LI{len(self.username)}sIc', self.user_id, len(self.username), self.username,
                           self.user_birth_date, self.user_gender)

    @classmethod
    def deserialize(cls, message):
        user_id, username_length = struct.unpack('<LI', message[:8])
        username, user_birth_date, user_gender = struct.unpack(f'<{username_length}sIc', message[8:])
        return cls(user_id, username, user_birth_date, user_gender)


class Config:

    def __init__(self, num_of_fields, fields):
        self.num_of_fields = num_of_fields
        self.fields = fields

    def serialize(self):
        data = struct.pack('<I', self.num_of_fields)[0]
        for field in self.fields:
            data += struct.pack(f'<I{len(field)}s', len(field), field)[0]
        return data

    @classmethod
    def deserialize(cls, message):
        i=4
        fields = set()
        num_of_fields = struct.unpack('<I', message[:i])
        while i < len(message):
            length = struct.unpack('<I', message[i:i+4])[0]
            i += 4
            field = struct.unpack(f"<{length}s", message[i: i + length])[0]
            i += length
            fields.add(field)
        return cls(num_of_fields, fields)
