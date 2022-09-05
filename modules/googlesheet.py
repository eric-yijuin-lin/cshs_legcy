import pygsheets
from pandas import DataFrame

class GoogleSheetHelper:
    def __init__(self, credential: str, sheet_url) -> None:
        self.gc = pygsheets.authorize(service_account_file=credential)
        self.sheet = self.gc.open_by_url(sheet_url).sheet1
        # print(self.workbook.worksheets)

    def read_all_as_df(self) -> DataFrame:
        df = self.sheet.get_as_df(
            start='A1',
            index_colum=None,
            empty_value='',
            include_tailing_empty=False # index 從 1 開始算
        )
        return df

    def insert_row(self, row: list) -> None:
        row_index = self.get_next_row_index()
        self.sheet.insert_rows(row_index, number=1, values= row)
        self.update_shadow(row)

    def get_next_row_index(self) -> int:
        current_row_count = int(self.shadow_df.iloc[-1].name)
        row_index =  current_row_count + 2 # +1 忽略表頭, +1 到下一個 row
        return row_index

    def convert_to_range(self,
    start_col: str,
    start_row: int,
    end_col: str = None,
    end_row: int = None) -> str:
        start_cell = f"{start_col.upper()}{start_row}"
        if end_col is None or end_row is None:
            return start_cell
        return f"{start_cell}:{end_col}{end_row}"
