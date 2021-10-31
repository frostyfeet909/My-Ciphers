import transposition


def main():
    """Reads key and message from the resources folder and encodes/decodes it."""

    try:
        with open("resources/key.key", "r") as file:
            key = file.read()
    except FileNotFoundError:
        key = ""

    cipher = transposition.Columnar(key)

    print("1. Encode")
    print("2. Decode")
    print("3. Bruteforce")
    choice = input(">> ")

    if choice == "1":
        with open("resources/message.decoded", "r") as file:
            message = file.read()

        message = cipher.encode(message)
        print("Encoded: %s" % message)

        with open("resources/message.encoded", "w") as file:
            file.write(message)

    elif choice == "2":
        with open("resources/message.encoded", "r") as file:
            message = file.read()

        message = cipher.decode(message)
        print("Decoded: %s" % message)

        with open("resources/message.decoded", "w") as file:
            file.write(message)
    elif choice == "3":
        with open("resources/message.encoded", "r") as file:
            message = file.read()

        cipher.force_decode(message)
    else:
        print("Invalid")

    print("Bye!")


if __name__ == "__main__":
    main()
