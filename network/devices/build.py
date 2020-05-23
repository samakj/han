import json
from argparse import ArgumentParser
from shutil import copyfile
from os import listdir


def build(path: str) -> None:
    print(f"Building {path}...")
    build_dir = f"./builds/{path.strip('/')}"

    with open(f"{build_dir}/build.json") as file:
        build_config = json.load(file)

    sketch_dir = f"./sketches/{build_config['sketch']}"

    with open(f"{sketch_dir}/config.json") as file:
        sketch_config = json.load(file)

    print(f"Copying sketch file")
    copyfile(f"{sketch_dir}/sketch.ino", f"{build_dir}/{build_dir.split('/')[-1]}.ino")

    print(f"Copying sketch dir files")
    for file in listdir(sketch_dir):
        if file not in {"sketch.ino", "config.json"}:
            copyfile(f"{sketch_dir}/{file}", f"{build_dir}/{file}")

    variables = {
        "NODE_ID": build_config["node_id"],
    }

    if sketch_config.get("configs", None) is not None:
        for config_path in sketch_config["configs"]:
            with open(f"./config/{config_path.strip('/')}") as file:
                print(f"Adding sketch config file: {config_path}")
                variables.update(json.load(file))
    if sketch_config.get("variables", None) is not None:
        print(f"Adding sketch config variables")
        variables.update(sketch_config["variables"])
    if build_config.get("variables", None) is not None:
        print(f"Adding build sketch config variables")
        variables.update(build_config["variables"])

    print(f"Writing config.h")
    with open(f"{build_dir}/config.h", "w") as file:
        for name, value in variables.items():
            if isinstance(value, str):
                value = f"\"{value}\""

            file.write(f"#define {name} {value}\n")


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "path",
        help="The folder to build.",
        type=str,
    )

    args = parser.parse_args()
    build(args.path)

