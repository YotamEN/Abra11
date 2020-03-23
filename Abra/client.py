import click
from .mind_read_protocol import ProtocolHandler
from .reader import MindReader
from termcolor import cprint


@click.group()
def main():
    pass


@main.command()
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('path')
def upload_sample(host, port, path):
    # TODO add context manager for errors
    reader = MindReader(path)
    protocol_h = ProtocolHandler(host=host, port=port, path=path)
    protocol_h.post(reader.user.SerializeToString())
    while not reader.done():
        message = next(reader)
        if message is None:
            return
        ret = protocol_h.post(message.SerializeToString())
        if ret != 0:
            print("Error Occurred!")  # FIXME ERRORs


@main.command()
@click.option("--num_samples", "-n", default=-1)
@click.argument('path')
def read_snapshot(path, num_samples=-1):
    reader = MindReader(path)
    cprint(f"User {reader.user_id}:\n{reader.username}, born {reader.user_birth_date} ({reader.user_gender})",
           "blue", "on_white", attrs=['bold'])
    if num_samples < 0:
        while not reader.done():
            read_next(reader)
    else:
        for i in range(num_samples):
            read_next(reader)


def read_next(reader):
    message = next(reader)
    if message is None:
        return
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
          f"height={message.color_image.height}, "
          f"data={message.color_image.data}")
    print(f"DepthImage: (width={message.depth_image.width}, "
          f"height={message.depth_image.height}, "
          f"data={message.depth_image.data}")
    print(f"Feelings: hunger={message.feelings.hunger}, "
          f"thirst={message.feelings.thirst}, "
          f"exhaustion={message.feelings.exhaustion}, "
          f"happiness={message.feelings.happiness}")


if __name__ == '__main__':
    main()
