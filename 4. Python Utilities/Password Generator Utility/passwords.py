import string
import random
import re
import logging

# Regular expression for template
reg = r'[aAdp@]\d+%|\-%|@%|\[([aAdp\-@]%)+\]\d+%'

# Lists of symbols
list_p = list(string.punctuation)
list_p.remove('-')
list_p.remove('@')
list_a = list(string.ascii_lowercase)
list_A = list(string.ascii_uppercase)
list_d = list(string.digits)


# Get n random symbols from given list


def get_random_symbols(list_of_symbols: list, n: int) -> list:
    """
    Generate list of n symbols selected from list_of_symbols

    :param list_of_symbols: list of symbols
    :param n: symbols count to select from list_of_symbols
    :return  list of n symbols selected from list_of_symbols
    """
    res = []
    for i in range(n):
        res.append(random.choice(list_of_symbols))
    return res


# Check template for password


def check_template(template: str) -> bool:
    """
    Check basic template correctness

    :param template: template for password
    :return  boolean result of checking
    """
    logging.info("Checking template '" + template + "'")
    return ''.join([part.group(0) for part in re.finditer(reg, template)]) == template


# Get random passwords for given template


def get_passwords(template: str, multiplication_allowed: bool) -> list:
    """
    Generate list of random passwords based on template and multiplication_allowed

    :param template: template for password
    Rules of TEMPLATE:
        a) Each token of template are separate symbol %.
        b) Tokens consist of two part <type_token> and <count>, A10.
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
    :param multiplication_allowed: allow general password multiplication count
        for '[****]count%' sub templates
    :return  list of generated passwords (in string format)
    """
    logging.info("Generate list of random passwords based on template='" + template + "' and multiplication_allowed="
                 + str(multiplication_allowed))
    if not check_template(template):
        logging.error("Error in template " + template + "!")
        logging.critical("Exiting...")
        exit("Error in template " + template + "!")
    passwords = []

    # Count passwords to generate
    passwords_count = 1
    if multiplication_allowed:
        for part in re.finditer(r'\[([aAdp\-@]%)+\]\d+%', template):
            template_short = part.group(0)
            search_digits = re.search(r'\d+', template_short)
            if search_digits is not None:
                m = int(search_digits.group(0))
            if m == 0:
                logging.error("Error in template '" + template + " (zero count is not allowed in sub template '"
                              + template_short + "')!")
                logging.critical("Exiting...")
                exit("Error in template '" + template + " (zero count is not allowed in sub template '"
                     + template_short + "')!")
            passwords_count *= m
    logging.info("* Based on template have to generate " + str(passwords_count) + " passwords ")

    # Generate passwords randomly
    for password_no in range(passwords_count):
        logging.info("* Generating " + str(password_no+1) + " password")
        password_parts = []
        for part in re.finditer(reg, template):
            # Build list of symbols for random symbols generator
            list_for_random = []
            template_short = part.group(0)
            logging.debug("*** Working with sub template '" + template_short + "'")
            symbol_to_find = ['a', 'A', 'd', 'p', '-', '@']
            lists_add_to_list_of_random = [list_a, list_A, list_d, list_p, '-', '@']
            for symbol_no in range(6):
                found_symbols_pos_left = template_short.find(symbol_to_find[symbol_no])
                found_symbols_pos_right = template_short.rfind(symbol_to_find[symbol_no])
                if found_symbols_pos_left != found_symbols_pos_right:
                    logging.error("Error in template '" + template + "' (duplication of symbol '" + symbol_to_find[symbol_no]
                                  + "' in sub template '" + template_short + "')!")
                    logging.critical("Exiting...")
                    exit("Error in template '" + template + "' (duplication of symbol '" + symbol_to_find[symbol_no]
                         + "' in sub template '" + template_short + "')!")
                if found_symbols_pos_left != -1:
                    list_for_random += lists_add_to_list_of_random[symbol_no]
            logging.debug("***** List of symbols for random generator: " + str(list_for_random))
            if template_short == '-%' or template_short == '@%':
                symbols_count = 1
            else:
                search_digits = re.search(r'\d+', template_short)
                symbols_count = int(search_digits.group(0))
            logging.debug("***** Count of symbols for random generator: " + str(symbols_count))
            if symbols_count == 0:
                logging.error("Error in template '" + template + " (zero count is not allowed in sub template '"
                              + template_short + "')!")
                logging.critical("Exiting...")
                exit("Error in template '" + template + " (zero count is not allowed in sub template '"
                     + template_short + "')!")

            # Append generated password part to current password
            password_part_str = ''.join(get_random_symbols(list_for_random, symbols_count))
            logging.debug("*** For sub template '" + template_short + "' generated password '" + password_part_str + "'")
            password_parts.append(password_part_str)
        # Add generated password to the list of passwords
        password_str = ''.join(password_parts)
        logging.info("* Generated password '" + password_str + "'")
        passwords.append(password_str)
    return passwords
