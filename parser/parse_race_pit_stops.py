# -*- coding: utf-8 -*-
import pymupdf as fitz
import pandas as pd


def parse_race_pit_stop(file: str) -> pd.DataFrame:
    """Parse the table from "Pit Stop Summary" PDF

    :param file: Path to PDF file
    :return: A dataframe of [driver No., lap No., local time of the stop, pit stop No., duration]
    """

    doc = fitz.open(file)
    page = doc[0]
    # TODO: definitely have PDFs containing multiple pages

    # Get the position of the table
    t = page.search_for('DRIVER')[0].y0      # "DRIVER" gives the top of the table
    bh = page.search_for('DRIVER')[0].y1     # "DRIVER" gives the bottom of the header
    w, h = page.bound()[2], page.bound()[3]  # Page width and height
    bbox = fitz.Rect(0, t, w, h)

    # Extract headers
    header_words = page.get_text("text", clip=fitz.Rect(0, t, w, bh))

    # Sort the header words from left to right
    # Take all except the last one as it is empty
    header_words = [w.lower() for w in header_words.split("\n")[:-1]]

    # Parse
    df = page.find_tables(clip=bbox)[0].to_pandas()

    first_row = [s.split("-")[1] for s in list(df.columns)]
    df.columns = header_words
    df.loc[-1] = first_row  # add as first row
    df.index = df.index + 1  # shift index
    df = df.sort_index()  # re-sort by index

    # Clean up the table
    df.dropna(subset=['no'], inplace=True)  # Drop empty rows, if any
    df = df[df['no'] != '']
    df = df[['no', 'lap', 'time of day', 'stop', 'duration']].reset_index(drop=True)
    df.rename(columns={
        'no': 'driver_no',
        'lap': 'lap',
        'time of day': 'local_time',
        'stop': 'no',
        'duration': 'duration'
    }, inplace=True)
    return df

if __name__ == '__main__':
    pass
