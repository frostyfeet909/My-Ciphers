from os import path
import re
import ciphers.transposition as cipher

RESOURCES = path.join(path.dirname(path.realpath(__file__)), "resources")
ENCODED_PATTERN = re.compile("(\w*):(\d*):(.+)")  # Pattern for the encoded file
DECODED_PATTERN = re.compile("(\w+):(\d*):(.+)")  # Pattern for the decoded file


def main() -> None:
    """Reads key and message from the resources folder and encodes/decodes it."""

    processor = cipher.Columnar()

    print("1. Encode")
    print("2. Decode")
    choice = input(">> ")

    if choice == "1":
        decoded = get_message("decoded")
        encoded = []
        for decode in decoded:
            processor.key = decode[0]
            passes = int(decode[1]) if decode[1] and int(decode[1]) > 0 else 1  # Already verified is int
            encode = processor.encode(decode[2], passes)
            encoded.append((processor.key, passes, encode))

        put_message("encoded", encoded)

    elif choice == "2":
        encoded = get_message("encoded")
        decoded = []

        for encode in encoded:
            processor.key = encode[0]
            if not processor.key:
                print("[!] No key detected for: %s")
                print("[!] Would you like to bruteforce?")
                brute = input(">>> (y/n) ")

                if brute.strip().lower() != "y":
                    break
                
                passes = 1
                decode = processor.force_decode(encode[2])
                
            else:
                passes = int(encode[1]) if encode[1] and int(encode[1]) > 0 else 1  # Already verified is int
                decode = processor.decode(encode[2], passes)
        
            decoded.append((processor.key, passes, decode))

        put_message("decoded", decoded)
    else:
        print("Invalid")

    print("Bye!")


def get_message(file_name : str) -> list[tuple[str, str, str]]:
    """Get key:passes:message from a file."""
    # Ooooh look how new it is
    match file_name:
        case "encoded":
            pattern = ENCODED_PATTERN
        case "decoded":
            pattern = DECODED_PATTERN
        case _:
            raise FileExistsError("[!!] Require encoded or decoded")

    file_path = path.join(RESOURCES, file_name)
    verify_file(file_path)

    with open(file_path, "r") as file:
        lines = "".join(file.readlines())

    return pattern.findall(lines)


def put_message(file_name : str, to_write: list[tuple[str, int, str]]) -> None:
    """Save key:passes:message to a file."""
    match file_name:
        case "encoded":
            pass
        case "decoded":
            pass
        case _:
            raise FileExistsError("[!!] Require encoded or decoded")

    file_path = path.join(RESOURCES, file_name)

    with open(file_path, "a") as file:
        for encode in to_write:
            line = ":".join(str(x) for x in encode)
            file.write(line)
            file.write("\n")
        file.write("\n")


def verify_file(file_path) -> None:
    """Raise an error when a file does not exsist."""
    if not path.exists(file_path):
        raise FileNotFoundError("[!!] File does not exsist: %s" % file_path)


if __name__ == "__main__":
    main()
