#!/bin/env python

import argparse
from pathlib import Path
import former

parser = argparse.ArgumentParser(description='Build forms using Markdown.')
parser.add_argument('mdfile', type=Path, help='Path to the Mardown file')
parser.add_argument('--post', type=str, help='URL to post the HTML form', default='/post')
args = parser.parse_args()

if __name__ == "__main__":
    former.run(args.post, args.mdfile)