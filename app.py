import argparse

from yaml import load

from json_placeholder.parser.parser import parse_yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hello World")

    parser.add_argument(
        "--path",
        type=str,
        help="file path",
        default="./test.yaml"
    )

    args = parser.parse_args()
    path = args.path

    with open(path) as yaml_file:
        yaml_obj = load(yaml_file)
        parse_yaml(yaml_obj)
