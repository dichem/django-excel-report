import xlsxwriter


wb = xlsxwriter.Workbook('asd.xlsx')
ws = wb.add_worksheet()
ws.merge_range(1,1,2,2, 'asdas')
wb.close()
