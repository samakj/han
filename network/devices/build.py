import json
import random
from argparse import ArgumentParser
from shutil import copyfile
from os import listdir, system, path as path_lib
from typing import Any, Dict, Tuple

TLS_CA_FOLDER = "/Users/samakj/repos/HAN/network/tls"
PASSWORD_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
PASSWORD_LENGTH = 16


def generate_password(chars: str, length: int) -> str:
    print(" -> Generating password.")
    return "".join(random.choice(chars) for _ in range(length))


def h_file_path_to_dict(path: str) -> Dict[str, Any]:
    previous_config = {}

    if path_lib.isfile(path):
        with open(path) as file:
            for line in file.readlines():
                key_value_pair = line.replace("#define ", "").strip(" ").strip("\n").split(" ")
                if len(key_value_pair) == 2:
                    try:
                        previous_config[key_value_pair[0]] = int(key_value_pair[1].strip('"'))
                    except ValueError:
                        previous_config[key_value_pair[0]] = key_value_pair[1].strip('"')

    return previous_config


def json_from_path(path: str) -> Dict[str, Any]:
    loaded_json = {}

    if path_lib.isfile(path):
        with open(path) as file:
            loaded_json = json.load(file)

    return loaded_json


def generate_certs(client_name: str) -> Tuple[str, str, str]:
    system(f"cd /Users/samakj/repos/HAN/network/tls && sh generate-client-keys.sh {client_name}")

    with open(f"{TLS_CA_FOLDER}/{client_name}.key") as file:
        client_key = file.read().strip("\n")
    with open(f"{TLS_CA_FOLDER}/{client_name}.crt") as file:
        client_cert = file.read().strip("\n")
    with open(f"{TLS_CA_FOLDER}/ca.crt") as file:
        ca_cert = file.read().strip("\n")

    system(f"cd /Users/samakj/repos/HAN/network/tls && rm {client_name}*")
    return ca_cert, client_cert, client_key


def write_cert_to_h_file(file, cert_name: str, cert: str) -> None:
    file.write(f'const char {cert_name}[] PROGMEM =\n')

    for line in cert.split("\n"):
        file.write(f'"{line}\\n" \\\n')

    file.write(f';\n')


def build(path: str, regenerate_password: bool = False) -> None:
    print(f"Building {path}...")
    build_dir = f"./builds/{path.strip('/')}"
    node_id = path.strip('/').split('/')[-1]

    build_config = json_from_path(path=f"{build_dir}/build.json")
    previous_built_config = h_file_path_to_dict(path=f"{build_dir}/config.h")

    sketch_dir = f"./sketches/{build_config['sketch']}"
    sketch_config = json_from_path(path=f"{sketch_dir}/config.json")

    print(f"Copying sketch file.")
    copyfile(f"{sketch_dir}/sketch.ino", f"{build_dir}/{build_dir.split('/')[-1]}.ino")

    if sketch_config.get("certs", False):
        print(f"Creating cert files.")
        if not path_lib.isfile(f"{build_dir}/certificates.h"):
            ca_cert, client_cert, client_key = generate_certs(client_name=node_id)

            print(f" -> Writing certs.h")
            with open(f"{build_dir}/certificates.h", "w") as file:
                write_cert_to_h_file(file, "CA_CERT", ca_cert)
                write_cert_to_h_file(file, "CLIENT_CERT", client_cert)
                write_cert_to_h_file(file, "CLIENT_KEY", client_key)
        else:
            print(" -> File exists so not recreating.")

    variables = {
        "NODE_ID": node_id,
    }

    if sketch_config.get("configs", None) is not None:
        for config_path in sketch_config["configs"]:
            if "mqtt.json" in config_path:
                variables["MQTT_PASSWORD"] = (
                    generate_password(PASSWORD_CHARS, PASSWORD_LENGTH)
                    if regenerate_password or previous_built_config.get("MQTT_PASSWORD", None) is None else
                    previous_built_config["MQTT_PASSWORD"]
                )

            variables.update(json_from_path(path=f"./config/{config_path.strip('/')}"))
    if sketch_config.get("variables", None) is not None:
        print(f"Adding sketch config variables.")
        variables.update(sketch_config["variables"])
    if build_config.get("variables", None) is not None:
        print(f"Adding build sketch config variables.")
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

    parser.add_argument(
        "--regenerate_password",
        help="Will generate new password if set.",
        default=False,
        type=str,
    )

    args = parser.parse_args()
    build(args.path, args.regenerate_password)

