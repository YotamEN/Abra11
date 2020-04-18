from Abra.abra_pb2 import Snapshot, SnapshotPathWrapper
import click
from pathlib import Path
from utils.errors import *
from utils.mq.mq_handlers import MQHandler
import json
from .parsers import *


@click.group()
def main():
    pass


@main.command('parse')
@click.argument('parser', help="Name of requested parser")
@click.argument('data_path', help="Path to data for parsing")
def parse_cli(parser: str, data_path: str):
    res = parse(parser, data_path)
    print(res)
    return res


@main.command("run-parser")
@click.argument('parser', help="Name of requested parser")
@click.argument('mq_url', help="URL of your Message Queue")
def run_parser_cli(parser: str, mq_url: str):
    parser = parser.lower()
    if parser not in PARSER_NAMES:
        raise UnknownParserError()
    parser_class = get_parser_type(parser)
    parser_h = parser_class()
    mq_handler = MQHandler(mq_url)

    def on_message(self, ch, method, props, body):
        user, path = unpack_path_wrapper(body)
        snapshot = load_snapshot(path)
        parsed_data = parser_h.parse(msg=snapshot)
        wrapped_json_parsed_data = wrap_data_for_saver(user, parsed_data)
        mq_handler.publish_to_saver_queue(wrapped_json_parsed_data)

    # runs forever... stops on CTRL-C
    mq_handler.consume_queue(queue=parser, callback=on_message)


def parse(parser, raw_data):
    parser = parser.lower()
    if parser not in PARSER_NAMES:
        raise UnknownParserError(f"Unknown parser! please choose one of the following:\n{PARSER_NAMES!r}")
    parser_class = get_parser_type(parser)
    parser_h = parser_class()
    user, path = unpack_path_wrapper(raw_data)
    snapshot = load_snapshot(path)
    parsed_data = parser_h.parse(msg=snapshot)
    wrapped_json_parsed_data = wrap_data_for_saver(user, parsed_data)
    return wrapped_json_parsed_data


def get_parser_type(parser_name: str):
    if parser_name == "pose":
        return PoseParser
    elif parser_name == "color image":
        return CImageParser
    elif parser_name == "depth image":
        return DImageParser
    elif parser_name == "feelings":
        return FeelingsParser
    else:
        return None


def load_snapshot(path):
    p = Path(path)
    if not p.is_file():
        raise UnknownPathError(f"ERROR: no file detected on '{path}'")
    snapshot = Snapshot()
    with p.open("rb") as file:
        snapshot.ParseFromString(file.read())
    return snapshot


def unpack_path_wrapper(raw_data):
    snapshot_path_wrapper = SnapshotPathWrapper.ParseFromString(raw_data)
    user, path = snapshot_path_wrapper.user, snapshot_path_wrapper.path
    return user, path


def wrap_data_for_saver(user, data):
    wrapped = {USER_ID_KEY: user.user_id}
    wrapped.update(data)
    return json.dumps(wrapped)
