import os
import openpyxl

def search(dirname,findFile):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.xlsx' and findFile in full_filename:
                    print(full_filename)

    except PermissionError:
        pass

findFile = '716V_DL CA.xlsx'
search("C:/Users/84430/Desktop/metadata",findFile) # 드라이브 내 특정 폴더 안에서 탐색하도록 코드 짠다.


###엑셀에서 불러오는 시트는 무조건 combo 일것
wb =  op.load_workbook(findFile)

divide_sheet = wb['combo']
