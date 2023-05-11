#!/usr/bin/env python3
# Import
import re
import argparse
import CsvFileParser

# CSV-type file parser utility
pass_parser = argparse.ArgumentParser(prog='csv_utility',
                                      usage='%(prog)s INPUT_FILE [-it INPUT_FILE_TYPE] '
                                            '[-id INPUT_FILE_DELIMITER]',
                                      description='Parse CSV, TSV, DSV files',
                                      add_help=True,
                                      allow_abbrev=False)
pass_parser.add_argument('input',
                         metavar='INPUT_FILE',
                         help='Set input file name'
                         )
pass_parser.add_argument('-it',
                         '--input-type',
                         metavar='INPUT_FILE_TYPE',
                         help='Set input file type (CSV, TSV, DSV)',
                         default='CSV'
                         )
pass_parser.add_argument('-id',
                         '--input-delimiter',
                         metavar='INPUT_FILE_DELIMITER',
                         help='Set input file delimiter for DSV file, for other file types argument is ignored',
                         default=','
                         )
pass_parser.add_argument('-o',
                         '--output',
                         metavar='OUTPUT_FILE',
                         help='Set output file name',
                         default=''
                         )
pass_parser.add_argument('-ot',
                         '--output-type',
                         metavar='OUTPUT_FILE_TYPE',
                         help='Set output file type (CSV, TSV, DSV, JSON)',
                         default='CSV'
                         )
pass_parser.add_argument('-od',
                         '--output-delimiter',
                         metavar='OUTPUT_FILE_DELIMITER',
                         help='Set output file delimiter for DSV file, for other file types argument is ignored',
                         default=','
                         )
pass_parser.add_argument('-head',
                         action='store_true',
                         help='Use header line'
                         )

pass_parser.add_argument('-cols',
                         metavar='SELECTED_COLS',
                         help='Selected columns'
                         )
pass_parser.add_argument('-rows',
                         metavar='SELECTED_ROWS',
                         help='Selected rows'
                         )
pass_parser.add_argument('-filter',
                         nargs="+",
                         metavar='COLUMN REGEX',
                         help='Set filter REGEX on COLUMN (number or name)'
                         )
args = pass_parser.parse_args()

csv_file = CsvFileParser.CsvFileParser(input_file_name=args.input,
                                       input_file_type=args.input_type,
                                       input_file_delimiter=args.input_delimiter,
                                       use_header=args.head)


if args.cols is not None:
    csv_file.select_cols(args.cols)

if args.rows is not None:
    csv_file.select_rows(args.rows)

if args.filter is not None:
    if len(args.filter) % 2 == 0:
        for i in range(0, len(args.filter), 2):
            if re.match(r'^\d*$', args.filter[i]) is not None:
                csv_file.set_filter_to_col(
                    int(args.filter[i]), args.filter[i+1])
            elif args.filter[i] in csv_file.col_names and csv_file.use_header:
                csv_file.set_filter_to_col(csv_file.col_names.index(
                    args.filter[i]), args.filter[i + 1])
            else:
                exit("Error in filter arguments...")
    else:
        exit("Error in filter arguments...")

if args.output_type == "JSON":
    csv_file.json_output(args.output)
else:
    csv_file.csv_output(args.output, args.output_type, args.output_delimiter)
