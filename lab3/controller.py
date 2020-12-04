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

def get_input(msg, table_name=''):
    print(msg)
    if table_name:
        print(' | '.join(TABLES[table_name]), end='\n\n')
    return input()


def get_insert_input(msg, table_name):
    print(msg)
    print(' | '.join(TABLES[table_name]), end='\n\n')
    return input(), input()


def press_enter():
    input()


class Controller:
    def __init__(self):
        self.model = Model()

    def show_init_menu(self, msg=''):
        selection_menu = SelectionMenu(
            TABLES_NAMES + ['Fill table "Customers" by random data (10 items)', 'Commit'],
            title='Select the table to work with | command:', subtitle=msg)
        selection_menu.show()

        index = selection_menu.selected_option
        if index < len(TABLES_NAMES):
            table_name = TABLES_NAMES[index]
            self.show_entity_menu(table_name)
        elif index == len(TABLES_NAMES):
            self.fill_customers_by_random()
        elif index == len(TABLES_NAMES) + 1:
            self.model.commit()
            self.show_init_menu(msg='Commit success')
        else:
            print('Bye, have a beautiful day!')

    def show_entity_menu(self, table_name, msg=''):
        options = ['Delete', 'Update', 'Insert']
        functions = [self.delete, self.update, self.insert]

        selection_menu = SelectionMenu(options, f'Name of table: {table_name}',
                                       exit_option_text='Back', subtitle=msg)
        selection_menu.show()
        try:
            function = functions[selection_menu.selected_option]
            function(table_name)
        except IndexError:
            self.show_init_menu()

    def insert(self, table_name):
        try:
            columns, values = get_insert_input(
                f"INSERT {table_name}\nEnter columns divided with commas, then do the same for values in format: [value1, value2, ...]",
                table_name)
            self.model.insert(table_name, columns, values)
            self.show_entity_menu(table_name, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def delete(self, table_name):
        try:
            condition = get_input(
                f'DELETE {table_name}\n Enter condition (SQL):', table_name)
            self.model.delete(table_name, condition)
            self.show_entity_menu(table_name, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def update(self, table_name):
        try:
            condition = get_input(
                f'UPDATE {table_name}\nEnter condition (SQL):', table_name)
            statement = get_input(
                "Enter SQL statement in format [<key>=<value>]", table_name)

            self.model.update(table_name, condition, statement)
            self.show_entity_menu(table_name, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def fill_customers_by_random(self):
        try:
            self.model.fillTaskByRandomData()
            self.show_init_menu('10 customers are generated successfully')
        except Exception as err:
            self.show_init_menu(str(err))