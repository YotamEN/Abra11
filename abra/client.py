from .common import CLIENT_DEFAULT_HOST, CLIENT_DEFAULT_PORT, FAIL, SUCCESS
import click
from .mind_read_protocol import ProtocolHandler
from .reader import MindReader
from termcolor import cprint


@click.group()
def main():
    pass


@main.command("upload-sample")
@click.option("--host", "-h", default=CLIENT_DEFAULT_HOST)
@click.option("--port", "-p", default=CLIENT_DEFAULT_PORT)
@click.argument('path')
def upload_sample(host, port, path):
    # TODO add context manager for errors
    reader = MindReader(path)
    protocol_h = ProtocolHandler(host=host, port=port, path=path)
    cprint(f"User {reader.user_id}:\n{reader.username}, born {reader.user_birth_date} ({reader.user_gender})",
           "blue", "on_white", attrs=['bold'])
    if protocol_h.post(reader.user.SerializeToString()) == FAIL:
        print("Connection to server failed, please re-run the client")
        return FAIL
    print("\n\nsent user info!\n\n")
    while not reader.is_done():
        message = next(reader)
        if message is None:
            return
        ret = protocol_h.post(message.SerializeToString())
        if ret != SUCCESS:
            print("Error Occurred!")  # FIXME ERRORS


# FOR DEBUG:
@main.command("read-snapshot")
@click.option("--num_samples", "-n", default=-1)
@click.argument('path')
def read_snapshot(path, num_samples=-1):
    reader = MindReader(path)
    cprint(f"User {reader.user_id}:\n{reader.username}, born {reader.user_birth_date} "
           f"({'female' if reader.user_gender==0 else 'male' if reader.user_gender==1 else 'other'})",
           "blue", "on_white", attrs=['bold'])
    if num_samples < 0:
        while not reader.is_done():
            read_next(reader)
    else:
        for i in range(num_samples):
            read_next(reader, pr=1)


def read_next(reader, pr=0):
    message = next(reader)
    if message is None:
        return
    if pr:
        print_message(message.snapshot)


def print_message(message):
    print(f"Datetime: {message.datetime}")
    print(f"Pose:")
    print(f"\tTranslation: ("
          f"x={message.pose.translation.x}, "
          f"y={message.pose.translation.y}, "
          f"z={message.pose.translation.z}")
    print(f"\tRotation: ("
          f"x={message.pose.rotation.x}, "
          f"y={message.pose.rotation.y}, "
          f"z={message.pose.rotation.z}")
    print(f"ColorImage: (width={message.color_image.width}, "
          f"height={message.color_image.height}")
    print(f"DepthImage: (width={message.depth_image.width}, "
          f"height={message.depth_image.height}")
    print(f"Feelings: hunger={message.feelings.hunger}, "
          f"thirst={message.feelings.thirst}, "
          f"exhaustion={message.feelings.exhaustion}, "
          f"happiness={message.feelings.happiness}")


if __name__ == '__main__':
    main()
