# My Ciphers

A quickly put together implemetation of the Columnar transposition.

## Installation

1. Install the latest stable version of [python3](https://www.python.org/downloads/).
2. Install the remaining packages in requirements and setup the file structure by running `install_requirements.py`:

   ```bash
   python3 install_requirements.py
   ```

## Usage

1. Write encoded/decoded keys/messages in there respective files in the following format:

   ```bash
   key:passes:message

   // decoded
   hi:1:Hello World!
   hello::Hello World!

   // encoded
   HI:1:HLOOL! ELWRD
   HELLO:1:EO HW! LR LL OD
   ```

2. Run `main.py`

## License

Pls use it.
