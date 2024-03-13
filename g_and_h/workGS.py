import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger
from dataclasses import dataclass
from pprint import pprint
import time

class Sheet():
    
    @logger.catch
    def __init__(self, jsonPath: str, sheetName: str,  servisName: str = None, get_worksheet: int = 0):

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            jsonPath, self.scope)  # Секретынй файл json для доступа к API
        self.client = gspread.authorize(self.creds)
        self.sheetAll = self.client.open(
            #sheetName).sheet1  # get_worksheet(0)  # Имя таблицы
            sheetName)
        self.sheet = self.client.open(
            #sheetName).sheet1  # get_worksheet(0)  # Имя таблицы
            sheetName).get_worksheet(get_worksheet)  # get_worksheet(0)  # Имя таблицы
        
        # self.sheet.range(). (1, 1). # Активируем ячейку
    @logger.catch
    def send_cell(self, cell: str, value, form: bool = False):
        """
            [cell]: str - адрес ячейки 
                Например: "A1" или если [form] == True ([1, 2], 'value')
            [form]: bool = False - обозначение ячейки текстом или цифрами
                Например: True с цифрами ([1, 2], value) False текстом ('A1', value)
        value_input_option='USER_ENTERED' - иногда данные вставляются с ковычкой в начале это решает проблемму
        """
        if form:
            self.sheet.update_cell(
                cell[0], cell[1], value, value_input_option='USER_ENTERED')
        else:
            # update(cell, value)
            # value_input_option='USER_ENTERED')
            self.sheet.update(cell, value, value_input_option='USER_ENTERED')

    def insert_cell(self,data:list):
        """Записывает в последнуюю пустую строку"""
        nextRow = len(self.sheet.get_all_values()) + 1
        self.sheet.insert_row(data,nextRow, value_input_option='USER_ENTERED')

    def get_cell(self, i, n):
        value = self.sheet.cell(i, n).value
        return value

    def get_rom_value(self, i):
        """
        1 - первая строка
        """
        return self.sheet.row_values(i)


    
    def find_cell(self, value:str):
        """Ищет ячейку по значению"""
        return self.sheet.find(value)
    
  

    
   
if __name__ == '__main__':
    pass
    
    json = 'GDtxt.json'
    sheet = Sheet(json,'darkClaw921_Zaluzi', get_worksheet=3)
    a= sheet.find_cell('Скидка')
    sheetSale = sheet.get_rom_value(a.row)[-1]
    print(a)
    #a = sheet.get_rom_value(7) 
    # a = sheet.get_words_and_urls()
    # a = sheet.copy_sheet('testCopy5')
    # pprint(a)
    #for aa in a:
    #    print(f'{aa=}')
    #a = prepare_text(a)
    #pprint(a)