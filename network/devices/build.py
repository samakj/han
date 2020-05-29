import json
from argparse import ArgumentParser
from shutil import copyfile
from os import listdir, system, path as path_lib

TLS_CA_FOLDER = "/Users/samakj/repos/HAN/network/tls"


def build(path: str) -> None:
    print(f"Building {path}...")
    build_dir = f"./builds/{path.strip('/')}"
    node_id = path.strip('/').split('/')[-1]

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

    if sketch_config.get("certs", False):
        print(f"Creating cert files.")
        if not path_lib.isfile(f"{build_dir}/certificates.h"):
            # system(f"cd /Users/samakj/repos/HAN/network/tls && sh generate-client-keys.sh {node_id}")

            # with open(f"{TLS_CA_FOLDER}/{node_id}.key") as file:
            #     client_key = file.read().strip("\n").split("\n")
            # with open(f"{TLS_CA_FOLDER}/{node_id}.crt") as file:
            #     client_cert = file.read().strip("\n").split("\n")
            with open(f"{TLS_CA_FOLDER}/ca.crt") as file:
                ca_cert = file.read().strip("\n").split("\n")

            print(f"Writing certs.h")
            with open(f"{build_dir}/certificates.h", "w") as file:
                # file.write(f'const char CLIENT_KEY[] PROGMEM =\n')
                # for line in client_key:
                #     file.write(f'"{line}\\n" \\\n')
                # file.write(f';\n')
                #
                # file.write(f'const char CLIENT_CERT[] PROGMEM =\n')
                # for line in client_cert:
                #     file.write(f'"{line}\\n" \\\n')
                # file.write(f';\n')

                file.write(f'const char CA_CERT[] PROGMEM =\n')
                for line in ca_cert:
                    file.write(f'"{line}\\n" \\\n')
                file.write(f';\n')

            # system(f"cd /Users/samakj/repos/HAN/network/tls && rm {node_id}*")
        else:
            print("File exists so not recreating.")

    variables = {
        "NODE_ID": node_id,
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

