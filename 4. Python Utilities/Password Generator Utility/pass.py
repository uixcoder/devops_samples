#!/usr/bin/env python3
# Import
import argparse
import passwords
import logging
import os.path
from os import path

# Create the parser
pass_parser = argparse.ArgumentParser(prog='pass',
                                      usage='%(prog)s  [ -h | [ [ -l | -t | -f ] [ -c ] [ -v | -vv | -vvv ] ] ]',
                                      description='Generate passwords according to a given template',
                                      add_help=False,
                                      allow_abbrev=False)

pass_group1 = pass_parser.add_mutually_exclusive_group(required=False)

# Add the arguments
pass_group1.add_argument('-h',
                         action='store_true',
                         help="help")
pass_group1.add_argument('-l',
                         action='store',
                         type=int,
                         metavar='LENGTH',
                         help='Set length of password and generate random password from set {small lateral ASCII, '
                              'big lateral ASCII, digit}')
pass_group1.add_argument('-t',
                         action='store',
                         metavar='TEMPLATE',
                         help="Set template for generate passwords")
pass_group1.add_argument('-f',
                         action='store',
                         metavar='FILE',
                         help="Getting list of patterns from file (one per line) and generate for each random password")
pass_parser.add_argument('-c',
                         action='store',
                         type=int,
                         metavar='COUNT',
                         default=1,
                         help="number of passwords")
pass_group2 = pass_parser.add_mutually_exclusive_group(required=False)

pass_group2.add_argument('-v',
                         action='store_true',
                         help="verbose / warning+ level")
pass_group2.add_argument('-vv',
                         action='store_true',
                         help="verbose / info+ level")
pass_group2.add_argument('-vvv',
                         action='store_true',
                         help="verbose / debug+ level")

# Execute the parse_args() method
args = pass_parser.parse_args()

if args.h:
    help_templ = """Rules of TEMPLATE:
        a. Each token of template are separate symbol %.
        b. Tokens consist of two part <type_token> and <count>, A10.
            List of <type tokens>
                Type of Token    description
                a                small lateral ASCII
                A                big lateral ASCII
                d                digit
                p                Punctuations
                -                - (same symbol)
                @                @(same symbol)
                [ ]              set type of token
            <count> - number of symbols
    """
    print(pass_parser.format_help())
    print(help_templ)
else:
    # Set logging level
    logging.getLogger().setLevel(100)
    if args.v:
        logging.getLogger().setLevel(logging.WARNING)
    if args.vv:
        logging.getLogger().setLevel(logging.INFO)
    if args.vvv:
        logging.getLogger().setLevel(logging.DEBUG)
    # Scan arguments and generate passwords
    res = []
    if args.c is not None:
        for _ in range(args.c):
            if args.l is not None:
                template = r'[a%A%d%]' + str(args.l) + '%'
                res.append(' | '.join(passwords.get_passwords(template, False)))
            if args.t is not None:
                res.append(' | '.join(passwords.get_passwords(args.t, True)))
            if args.f is not None:
                if path.isfile(args.f):
                    template_file = open(args.f, "r")
                    template_list = template_file.readlines()
                    for template in template_list:
                        res.append(' | '.join(passwords.get_passwords(template.strip(), True)))
                else:
                    logging.error("File '" + args.f + "' does not exist!")
                    exit("File '" + args.f + "' does not exist!")

    res = ' | '.join(res)
    if res == '':
        print(pass_parser.format_help())
    else:
        print(res)
