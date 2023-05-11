import re
import sys
import json


def csv_line_to_list(line: str, delimiter: str = ',') -> list:
    csv_regular = r'(?:\"[^\"]*(?:\"\"[^\"]*\"\")*[^\"]*(?:\"\"[^\"]*\"\")*[^\"]*\")|' \
                  r'(?<=delimiter)[^\"delimiter]*(?=delimiter)|' \
                  r'^[^\"delimiter]*|(?<=delimiter)[^\"delimiter]*$'
    csv_regular = csv_regular.replace("delimiter", delimiter)
    parsed = re.findall(csv_regular, line)
    parsed_list: list = []
    for part in parsed:
        s = part.strip()
        if len(part) > 0 and part[0] == '"' and part[-1] == '"':
            s = s[1:-1]
        s = s.replace('""', '"')
        parsed_list.append(s)
    return parsed_list


class CsvFileParser:
    def __init__(self, input_file_name: str,
                 input_file_type: str = "CSV",
                 input_file_delimiter: str = ",",
                 use_header: bool = False) -> None:

        self.input_file_name = input_file_name
        if input_file_type == "CSV":
            self.input_file_delimiter = ","
        elif input_file_type == "TSV":
            self.input_file_delimiter = "\t"
        elif input_file_type == "DSV":
            self.input_file_delimiter = input_file_delimiter
        else:
            self.input_file_delimiter = ","
        self.output_file_delimiter = self.input_file_delimiter
        self.use_header = use_header

        # Count cols count and set all cols active
        input_csv_file = open(input_file_name)
        self.cols_count = len(csv_line_to_list(
            input_csv_file.readline(), input_file_delimiter))
        self.cols_selected = []
        self.cols_filter = []
        for col in range(self.cols_count):
            self.cols_selected.append(True)
            self.cols_filter.append("")
        self.cols_template = "0-" + str(self.cols_count)
        input_csv_file.seek(0, 0)

        # Count rows and  of active rows
        self.rows_count = sum(1 for line in input_csv_file)
        self.rows_selected = {}
        self.rows_template = ""
        input_csv_file.seek(0, 0)

        if use_header:
            self.col_names = csv_line_to_list(
                input_csv_file.readline(), input_file_delimiter)
        else:
            self.col_names = []
            for col in range(self.cols_count):
                self.col_names.append("Col_" + str(col))

        input_csv_file.close()

    def select_cols(self, cols_template: str) -> None:
        test = re.match(
            r'(-\d+|\d+-|\d+-\d+|\d+)(,(\d+-\d+|\d+))*(,\d+-)?$', cols_template)
        if test is None or test.group(0) != cols_template:
            exit("Error 1 in cols template")
        cols_str_parts = re.findall(r'^-\d+|\d+-$|\d+-\d+|\d+', cols_template)
        for cols_str_part in cols_str_parts:
            interval = re.match(r'^-\d+$', cols_str_part)
            if interval is not None:
                cols = re.findall(r'\d+', cols_str_part)
                for col in range(0, int(cols[0]) + 1):
                    if not self.cols_selected[col]:
                        exit("Error 2_1 in cols template!")
                    else:
                        self.cols_selected[col] = False
            else:
                interval = re.match(r'^\d+-$', cols_str_part)
                if interval is not None:
                    cols = re.findall(r'\d', cols_str_part)
                    for col in range(int(cols[0]), self.cols_count):
                        if not self.cols_selected[col]:
                            exit("Error 2_2 in cols template!")
                        else:
                            self.cols_selected[col] = False
                else:
                    interval = re.match(r'\d+-\d+', cols_str_part)
                    if interval is not None:
                        cols = re.findall(r'\d+', cols_str_part)
                        for col in range(int(cols[0]), int(cols[1]) + 1):
                            if not self.cols_selected[col]:
                                exit("Error 2_3 in cols template!")
                            else:
                                self.cols_selected[col] = False
                    else:
                        col = re.match(r'\d+', cols_str_part).group(0)
                        if not self.cols_selected[int(col)]:
                            exit("Error 2_4 in cols template!")
                        self.cols_selected[int(col)] = False
        for col in range(len(self.cols_selected)):
            self.cols_selected[col] = not self.cols_selected[col]
        self.cols_template = cols_template

    def select_rows(self, rows_template: str) -> None:
        test = re.match(
            r'(-\d+|\d+-|\d+-\d+|\d+)(,(\d+-\d+|\d+))*(,\d+-)?$', rows_template)
        if test is None or test.group(0) != rows_template:
            exit("Error 1 in rows template")
        self.rows_selected = set()
        rows_str_parts = re.findall(r'^-\d+|\d+-$|\d+-\d+|\d+', rows_template)
        for rows_str_part in rows_str_parts:
            interval = re.match(r'^-\d+$', rows_str_part)
            if interval is not None:
                rows = re.findall(r'\d+', rows_str_part)
                for row in range(0, int(rows[0]) + 1):
                    if row in self.rows_selected:
                        exit("Error 2_1 in rows template!")
                    else:
                        self.rows_selected.add(row)
            else:
                interval = re.match(r'^\d+-$', rows_str_part)
                if interval is not None:
                    rows = re.findall(r'\d+', rows_str_part)
                    for row in range(int(rows[0]), self.rows_count):
                        if row in self.rows_selected:
                            exit("Error 2_2 in rows template!")
                        else:
                            self.rows_selected.add(row)
                else:
                    interval = re.match(r'\d+-\d+', rows_str_part)
                    if interval is not None:
                        rows = re.findall(r'\d+', rows_str_part)
                        for row in range(int(rows[0]), int(rows[1]) + 1):
                            if row in self.rows_selected:
                                exit("Error 2_3 in rows template!")
                            else:
                                self.rows_selected.add(row)
                    else:
                        row = int(re.match(r'\d+', rows_str_part).group(0))
                        if row in self.rows_selected:
                            exit("Error 2_4 in rows template!")
                        self.rows_selected.add(row)
        self.rows_template = rows_template

    def set_filter_to_col(self, col: int, col_filter: str) -> None:
        self.cols_filter[col] = col_filter

    def generate_csv_header(self, in_line: str) -> str:
        list_line = csv_line_to_list(in_line, self.input_file_delimiter)
        res = []
        col = 0
        for part in list_line:
            if self.cols_selected[col]:
                s = part
                if part.find('"') != -1:
                    s = s.replace('"', '""')
                if part.find(self.output_file_delimiter) != -1:
                    s = '"' + s + '"'
                res.append(s)
            col += 1
        if res == "":
            return ""
        else:
            return self.output_file_delimiter.join(res)

    def generate_csv_row(self, in_line: str) -> str:
        list_line = csv_line_to_list(in_line, self.input_file_delimiter)
        res = []
        col = 0
        print_of_row_allowed = True
        for part in list_line:
            if self.cols_filter[col] != "":
                if re.match(self.cols_filter[col], part) is None:
                    print_of_row_allowed = False
                    break
            col += 1
        if print_of_row_allowed:
            col = 0
            for part in list_line:
                if self.cols_selected[col]:
                    s = part
                    if part.find('"') != -1:
                        s = s.replace('"', '""')
                    if part.find(self.output_file_delimiter) != -1:
                        s = '"' + s + '"'
                    res.append(s)
                col += 1
        if res == "":
            return ""
        else:
            return self.output_file_delimiter.join(res)

    def csv_output(self, output_file_name: str = "",
                   output_file_type: str = "CSV",
                   output_file_delimiter: str = ",") -> None:

        if output_file_type == "CSV":
            self.output_file_delimiter = ","
        elif output_file_type == "TSV":
            self.output_file_delimiter = "\t"
        elif output_file_type == "DSV":
            self.output_file_delimiter = output_file_delimiter
        else:
            self.output_file_delimiter = ","

        if output_file_name == "":
            output_file = sys.stdout
        else:
            output_file = open(output_file_name, "w")

        csv_file = open(self.input_file_name, "r")

        if self.use_header:
            csv_line = csv_file.readline()
            print(self.generate_csv_header(csv_line), file=output_file)

        if self.rows_selected == {}:
            for csv_line in csv_file:
                res = self.generate_csv_row(csv_line)
                if res != "":
                    print(res, file=output_file)
        else:
            row = 0
            for csv_line in csv_file:
                if row in self.rows_selected:
                    res = self.generate_csv_row(csv_line)
                    if res != "":
                        print(res, file=output_file)
                row += 1
        csv_file.close()
        output_file.close()

    def generate_list_row(self, in_line: str) -> list:
        list_line = csv_line_to_list(in_line, self.input_file_delimiter)
        res = []
        print_of_row_allowed = True
        for col in range(self.cols_count):
            if self.cols_filter[col] != "":
                if re.match(self.cols_filter[col], list_line[col]) is None:
                    print_of_row_allowed = False
                    break
        if print_of_row_allowed:
            for col in range(self.cols_count):
                if self.cols_selected[col]:
                    res.append(list_line[col])
        return res

    def json_output(self, output_file_name: str = "") -> None:
        col_keys = []
        for col in range(len(self.col_names)):
            if self.cols_selected[col]:
                col_keys.append(self.col_names[col])

        if output_file_name == "":
            output_file = sys.stdout
        else:
            output_file = open(output_file_name, "w")

        csv_file = open(self.input_file_name, "r")

        row = 0
        if self.use_header:
            csv_line = csv_file.readline()
            row = 1

        json_data = []

        if self.rows_selected == {}:
            for csv_line in csv_file:
                res = dict(zip(col_keys, self.generate_list_row(csv_line)))
                if res:
                    json_data.append(res)
        else:
            for csv_line in csv_file:
                if row in self.rows_selected:
                    res = dict(zip(col_keys, self.generate_list_row(csv_line)))
                    if res:
                        json_data.append(res)
                row += 1

        print(json.dumps(json_data, indent=4), file=output_file)
