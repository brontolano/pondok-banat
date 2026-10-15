import openpyxl
import glob
import os

for f in sorted(glob.glob('.data-pondokbanat/*.xlsx')):
    try:
        wb = openpyxl.load_workbook(f, read_only=True)
        print(os.path.basename(f), '->', wb.sheetnames)
        wb.close()
    except Exception as e:
        print(os.path.basename(f), 'ERROR', e)
