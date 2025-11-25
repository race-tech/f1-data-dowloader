
def clean_row(row):
    if "-" in str(row['pos']):
        row = row.map(lambda x: str(x)[2:])
    return row
