#!/bin/env python

import argparse
from pathlib import Path
import former

parser = argparse.ArgumentParser(description='Build forms using Markdown.')
args = parser.parse_args()

if __name__ == "__main__":
    former.run()