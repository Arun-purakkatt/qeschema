#!/usr/bin/env python
#
# Copyright (c), <year> <copyright holders>. All rights reserved.
# This file is distributed under the terms of the MIT License. See the
# file 'LICENSE' in the root directory of the present distribution, or
# http://opensource.org/licenses/MIT.
#
"""
Convert from XML input  to Fortran input
"""

import sys


def parse_args():
    """Command arguments parsing"""
    import argparse

    parser = argparse.ArgumentParser(
            description="This program converts an XML input to the an equivalent "
                        "input file written in a format that is natively readable "
                        "by Fortran's codes of Quantum Espresso"
    )
    parser.add_argument("-v", "--verbosity", action="count", default=1,
                        help="Increase output verbosity.")
    parser.add_argument('--output', metavar='OUTPUT-FILE', type=str,
                        help="Write the input file for QE into a specific file "
                             "instead of display it on screen.")
    parser.add_argument('--xsd', metavar='XSD-FILE', type=str,
                        help='Use a specific XSD schema for XML translation.')
    parser.add_argument('xml_file', help="XML input filename.")
    return parser.parse_args()


if __name__ == '__main__':

    # Python 2.7+ is required. For old versions 'argparse' is available
    # only with extra package: https://pypi.python.org/pypi/argparse.
    if sys.version_info < (2, 7, 0):
        sys.stderr.write("You need python 2.7 or later to run this program\n")
        sys.exit(1)

    args = parse_args()

    if __package__ is None:
        from os import path
        sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

    import qespresso

    qespresso.set_logger(args.verbosity)

    xml_conf = qespresso.PwDocument()
    xml_conf.read(args.xml_file)
    pw_in = xml_conf.get_qe_input()

    if args.output:
        import os

        if os.path.isfile(args.output):
            try:
                choice = raw_input("File exists, overwrite? (y/n) ")
            except NameError:
                choice = input("File exists, overwrite? (y/n) ")
        else:
            choice = 'y'

        if choice.lower() in ("yes", 'y'):
            with open(args.output, mode='w') as f:
                f.write(pw_in)
                print("Input configuration written to file '%s' ..." % args.output)
            sys.exit(0)

    print("=" * 13 + " START OF PW INPUT " + "=" * 13)
    print(pw_in)
    print("=" * 13 + " END OF PW INPUT " + "=" * 13 + "\n")
