import argparse
import datetime
import json

from src.factory import MemoNestFactory, MemoNestMode
from src.interaction import (
    MemoCreateData,
    MemoDeleteData,
    MemoGetData,
    MemoUpdateData,
    OutputHandler,
)


def convert_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_datetime(item) for item in obj]
    return obj


class ConsoleJsonOutput(OutputHandler):

    def output(self, data: dict) -> None:
        converted_data = convert_datetime(data)
        json_data = json.dumps(converted_data, indent=4)
        print(json_data)
        print("\n")

    def error_output(self, code: int, message: str) -> None:
        print(f"Error code {code}: {message}")
        print("\n")


memo_nest_factory = MemoNestFactory()
memo_nest = memo_nest_factory.create_memo_nest(MemoNestMode.SINGLE_USER)
memo_nest.set_output(ConsoleJsonOutput())


def create_memo(title):
    data = MemoCreateData(title=title)
    memo_nest.create_memo(data)


def get_memo(memo_id):
    data = MemoGetData(id=memo_id)
    memo_nest.get_memo(data)


def get_memos():
    memo_nest.get_memos()


def update_memo(memo_id, new_title):
    data = MemoUpdateData(id=memo_id, title=new_title)
    memo_nest.update_memo(data)


def delete_memo(memo_id):
    data = MemoDeleteData(id=memo_id)
    memo_nest.delete_memo(data)


def print_help(parsers: list) -> None:
    for parser in parsers:
        print("\n----------------------------------")
        parser.print_help()
    print("\n")


def main():
    parser = argparse.ArgumentParser(description="Memo management console application")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a new memo")
    create_parser.add_argument(
        "--title", type=str, required=True, help="Title of the memo"
    )

    get_parser = subparsers.add_parser("get", help="Get a memo by ID")
    get_parser.add_argument("--id", type=str, required=True, help="ID of the memo")

    get_all_parser = subparsers.add_parser("get_all", help="Get all memos")

    update_parser = subparsers.add_parser("update", help="Update a memo by ID")
    update_parser.add_argument("--id", type=str, required=True, help="ID of the memo")
    update_parser.add_argument(
        "--title", type=str, required=True, help="New title of the memo"
    )

    delete_parser = subparsers.add_parser("delete", help="Delete a memo by ID")
    delete_parser.add_argument("--id", type=str, required=True, help="ID of the memo")

    help_parser = subparsers.add_parser("help", help="Show this help message and exit")

    exit_parser = subparsers.add_parser("exit", help="Exit the application")

    while True:
        try:
            args = parser.parse_args(input("Enter command: ").split())

            if args.command == "create":
                create_memo(args.title)
            elif args.command == "get":
                get_memo(args.id)
            elif args.command == "get_all":
                get_memos()
            elif args.command == "update":
                update_memo(args.id, args.title)
            elif args.command == "delete":
                delete_memo(args.id)
            elif args.command == "help":
                print_help(
                    [
                        create_parser,
                        get_parser,
                        get_all_parser,
                        update_parser,
                        delete_parser,
                        help_parser,
                        exit_parser,
                    ]
                )
            elif args.command == "exit":
                print("Exiting the application.")
                break

        except SystemExit as e:
            print(e)
            print("\n")
            print_help(
                [
                    create_parser,
                    get_parser,
                    get_all_parser,
                    update_parser,
                    delete_parser,
                    help_parser,
                    exit_parser,
                ]
            )


if __name__ == "__main__":
    main()
