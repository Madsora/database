import psycopg2

class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5432",
                                               database='postgres', user='postgres', password='7654ann321')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Помилка при з'єднанні з PostgreSQL", error)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def create_db(self):
        f = open("create_db.txt", "r")

        self.cursor.execute(f.read())
        self.connection.commit()

    def get(self, table_name, param, arg):
        try:
            query = f'SELECT {param} FROM public."{table_name}"'

            if arg:
                query += ' WHERE ' + arg

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, table_name, columns, values):
        try:
            query = f'INSERT INTO public."{table_name}" ({columns}) VALUES ({values});'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, table_name, condition):
        try:
            query = f'DELETE FROM public."{table_name}" WHERE {condition};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, table_name, value, new_value):
        try:
            query = f'UPDATE public."{table_name}" SET {new_value} WHERE {value}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()


    def filter_product_category(self, phrase):
        query = f'''
        select
        ts_headline(category_name, query, 'StartSel=\033[94m, StopSel=\033[0m') as category_name,
        ts_headline(product_name, query, 'StartSel=\033[94m, StopSel=\033[0m') as product_name,
        ts_headline(product_description, query, 'StartSel=\033[94m, StopSel=\033[0m') as product_description
    
        from (
        select
            c.name as category_name,
            public."Products".name as product_name,
            public."Products".description as product_description,
            to_tsvector(c.name) ||
            to_tsvector(public."Products".name) ||
            to_tsvector(public."Products".description) as document,
            phraseto_tsquery('{phrase}') as query
        from public."Products"
        join public."Categories" c on public."Products".categ_id = c.categ_id
        ) search
        where document @@ query;
        '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fillTaskByRandomData(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomCustomers()
            RETURNS void AS $$
        DECLARE
            step integer  := 10;
        BEGIN
            LOOP EXIT WHEN step > 20;
                INSERT INTO public."Customers" (fullname, adress, email, phone_number)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 10),
                    (random() * (100000000 - 1) + 1)::integer
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomCustomers();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()