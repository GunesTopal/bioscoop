from typing import Any, Callable, Union
from prettytable import PrettyTable


class ConsoleColor:
    # Color
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[97m'

    # Style
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'

    # BackgroundColor
    BgBLACK = '\033[40m'
    BgRED = '\033[41m'
    BgGREEN = '\033[42m'
    BgORANGE = '\033[43m'
    BgBLUE = '\033[44m'
    BgPURPLE = '\033[45m'
    BgCYAN = '\033[46m'
    BgGRAY = '\033[47m'

    # End
    END = '\033[0m'


def add_color(text: Any, color: str) -> str:
    return color + str(text) + ConsoleColor.END


def create_table(
    data: list,
    headers: list[str],
    header_colors: dict[str, str] = None,
    column_colors: dict[str, Union[str, Callable[[Any], str]]] = None
) -> PrettyTable:
    """
    Creates a table using PrettyTable that supports colored headers and data

    Arguments:
    - data: list of datarows to display
    - headers: list of field names used as headers
    - header_colors: dictionary of {field_name: color} pairs 
    - column_colors: dictionary of {field_name: color} pairs. 
      In this case the color can also be a callable function that gets passed the column data and returns a string.
      Use this for conditional coloring depending on the data value. 
    """

    if not data or not headers:
        raise ValueError("Table needs data and headers.")

    colored_headers = headers.copy()

    if header_colors:
        colored_headers = [str(header) if not header_colors.get(header) else add_color(
            header, header_colors[header]) for header in headers]

    if column_colors:
        for row in data:
            for index, header in enumerate(headers):
                color = column_colors.get(header)
                if color:
                    if callable(color):
                        row[index] = add_color(
                            row[index], color(row[index]))
                    else:
                        row[index] = add_color(
                            row[index], str(column_colors[header]))

    table = PrettyTable()
    table.field_names = colored_headers
    table.add_rows(data)
    return table


if __name__ == '__main__':
    data = [
        [12, "Frozen", 123],
        [9, "Spiderman", 110],
        [4, "Saw", 199]
    ]
    headers = ["Id", "Titel", "Duur"]
    header_colors = {
        "Id": ConsoleColor.BOLD,
        "Titel": ConsoleColor.GREEN + ConsoleColor.BOLD,
        "Duur": ConsoleColor.RED + ConsoleColor.BOLD,
    }

    column_colors = {
        "Id": ConsoleColor.UNDERLINE,
        "Titel": ConsoleColor.ITALIC,
        "Duur": lambda x: ConsoleColor.RED if x > 120 else ConsoleColor.YELLOW
    }

    print(create_table(data, headers, header_colors, column_colors))
