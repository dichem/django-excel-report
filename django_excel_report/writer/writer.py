import xlsxwriter
import math


class Writer:
    """Значения ширины и высоты в ячкйках подобраны эмпирически"""
    def __init__(self, sheet):
        self.workbook = xlsxwriter.Workbook("report.xlsx")
        self.sheet = self.workbook.add_worksheet(sheet)
        self.current_row = 0
        self.columns_max_length = {}
        self.format = self.get_format()
        self.__saved = False

    def write_row(self, row: list[list[str]]) -> None:
        lcm = math.lcm(*map(list.__len__, row))
        col_num = 0
        for cell in row:
            self._write_cell(cell, lcm, col_num)
            col_num += 1
        self.current_row += lcm

    def _write_cell(self, cell: list[str], lcm: int, col_number: int):
        merging_range = lcm // len(cell)
        row_position = 0
        row_height = 20
        for data in cell:
            row_height = min(max(len(data), row_height), 120)
            self.columns_max_length[col_number] = max(len(data), self.columns_max_length.get(col_number, 0))

            if merging_range == 1:
                self.sheet.write(
                    self.current_row + row_position,  # first row
                    col_number,
                    data,
                    self.format
                )
            else:
                self.sheet.merge_range(
                    self.current_row + row_position,  # first row
                    col_number,
                    self.current_row + row_position + merging_range - 1,  # end row
                    col_number,
                    data,
                    self.format
                )
            row_position += merging_range
        for row in range(self.current_row, self.current_row + lcm):
            self.sheet.set_row(row, max(row_height, self.sheet.row_sizes.get(row, [0])[0]))

    def wrap(self):
        for col_number, value in self.columns_max_length.items():
            self.sheet.set_column(col_number, col_number, min(value + 5, 80))

    @property
    def saved(self):
        return self.__saved

    def save(self):
        self.workbook.close()

    def get_format(self):
        format_ = self.workbook.add_format()
        format_.set_text_wrap()
        format_.set_align('center')
        format_.set_align('vcenter')
        return format_
