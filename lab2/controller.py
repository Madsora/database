from consolemenu import SelectionMenu
from model import Model
from view import View

TABLES_NAMES = ['Customers', 'Orders', 'OrderLine', 'Products', 'Categories']
TABLES = {
'Customers': ['cust_id', 'fullname', 'adress', 'email', 'phone_number'],
'Orders': ['order_id', 'order_data', 'cust_id'],
'OrderLine': ['id', 'prod_id', 'order_id', 'quantity'],
'Products': ['prod_id', 'name', 'description', 'price', 'availability', 'categ_id'],
'Categories': ['categ_id', 'name']
}

def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print('  '.join(TABLES[tableName]), end='\n\n')
    return input()

def getInsertInput(msg, tableName):
    print(msg)
    print('  '.join(TABLES[tableName]), end='\n\n')
    return input(), input()

def pressEnter():
    input()

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_init_menu(self, msg=''):
        selectionMenu = SelectionMenu(
        TABLES_NAMES + ['Find text by word or phrase',
        'Fill table "Customers" by random data (10 items)'], title='Select the table or option:', subtitle=msg)
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 5:
            self.filter_product_category()
        elif index == 6:
            self.fillByRandom()
        else:
            print('END OF THE PROGRAMM')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        selectionMenu = SelectionMenu(options, f'Name of table: {tableName}',
        exit_option_text='Back', subtitle=msg)
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.show_init_menu()

    def get(self, tableName):
        try:
            param = getInput(
            f'{tableName}\nEnter table argument or *\n', tableName)
            condition = getInput(
            f'Enter condition (SQL) or leave empty:', tableName)
            data = self.model.get(tableName,param, condition)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        try:
            columns, values = getInsertInput(
            f"INSERT {tableName}\nEnter colums divided with commas, then do the same for values in format: ['value1', 'value2', ...]", tableName)
            self.model.insert(tableName, columns, values)
            self.show_entity_menu(tableName, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        try:
            condition = getInput(f'DELETE {tableName}\n Enter condition (SQL):', tableName)
            self.model.delete(tableName, condition)
            self.show_entity_menu(tableName, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        try:
            condition = getInput(
            f'UPDATE {tableName}\nEnter condition (SQL):', tableName)
            statement = getInput(
            "Enter SQL statement in format [<key>='<value>']", tableName)

            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def filter_product_category(self):
        try:
            phrase = getInput('Enter word or phrase for search:')
            data = self.model.filter_product_category(phrase)
            self.view.print(data)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def fillByRandom(self):
        try:
            self.model.fillTaskByRandomData()
            self.show_init_menu('Generated successfully')

        except Exception as err:
            self.show_init_menu(str(err))