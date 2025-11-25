# -*- coding: utf-8 -*-
import pymupdf as fitz
import pandas as pd

from parser.utils import clean_row


def parse_driver_championship_page(page: fitz.Page) -> pd.DataFrame:
    """Get the table from a given page in "Drivers' Championship" PDF

    :param page: A `fitz.Page` object
    :return: A dataframe of [pos, driver, total, wins]
    """

    # Get the position of "DRIVER" the table is located beneath it
    t = page.search_for("DRIVER")[0].y0
    bh = page.search_for("DRIVER")[0].y1
    b = page.search_for("Formula One World Championship Limited")[0].y0

    # Page width and height
    w = page.bound()[2]

    # Extract headers
    header_words = page.get_text("words", clip=fitz.Rect(0, t, w, bh))

    # Sort the header words from left to right
    header_words.sort(key=lambda w: w[0])
    header_words = [w[4].lower() for w in header_words]

    df = page.find_tables(clip=fitz.Rect(0, t, w, b))[0].to_pandas()

    # Trick to retrieve the first row
    first_row = df.columns
    df.columns = ["pos"] + header_words
    df.loc[-1] = first_row  # add as first row
    df.index = df.index + 1  # shift index
    df = df.sort_index()  # re-sort by index

    df = df.apply(clean_row, axis=1)
    df['wins'] = [count_wins(row) for row in df.iloc[:, 3:].values]

    return df[["pos", "driver", "total", "wins"]]


def parse_driver_championship(file: str) -> pd.DataFrame:
    """
    Parse "Drivers' Championship" PDF

    :param file: Path to PDF file
    :return: The output dataframe will be [pos, driver, total, wins]
    """
    # Get page width and height
    doc = fitz.open(file)
    page = doc[0]
    global W
    W = page.bound()[2]

    # Parse all pages
    tables = []
    for page in doc:
        tables.append(parse_driver_championship_page(page))
    df = pd.concat(tables, ignore_index=True)

    return df

# Count the number of wins for a given row
def count_wins(row):
    result = 0
    for i in range(len(row)):
        if len(row[i].split("\n")) < 2:
            continue
        else:
            pos = row[i].split("\n")[1]
            if pos == "1" or pos == "1F":
                result += 1
            else:
                continue
    return result

if __name__ == '__main__':
    pass
