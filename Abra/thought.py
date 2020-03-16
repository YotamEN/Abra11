import datetime
import struct

class Thought:

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        ret = f'Thought(user_id={self.user_id!r}, ' \
              f'timestamp={self.timestamp!r}, ' \
              f'thought={self.thought!r})'
        return ret

    def __str__(self):
        date_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ret = f'[{date_str}] user {self.user_id}: {self.thought}'
        return ret

    def __eq__(self, other):
        if isinstance(other, Thought) and \
                self.user_id == other.user_id and \
                self.timestamp == other.timestamp and \
                self.thought == other.thought:
            return True
        return False

    def serialize(self):
        send_th = self.thought.strip()
        data_packet = struct.pack(f'<QQi{len(send_th)}s', self.user_id,
                                  int(self.timestamp.timestamp()), len(send_th),
                                  send_th.encode())
        return data_packet

    def deserialize(data_packet):
        user_id = int.from_bytes(data_packet[:8], byteorder="little")
        timestamp = datetime.datetime.fromtimestamp(int.from_bytes(data_packet[8:16], byteorder="little"))
        thought = data_packet[20:].decode()
        return Thought(user_id, timestamp, thought)
