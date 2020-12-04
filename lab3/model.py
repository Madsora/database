from sqlalchemy import create_engine, Column, String, Integer, Numeric, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgres://postgres:7654ann321@localhost:5432/postgres')
Base = declarative_base()


class Customers(Base):
    __tablename__ = 'Customers'

    cust_id = Column(Integer, primary_key=True)
    fullname = Column(String)
    adress = Column(String)
    email = Column(String)
    phone_number = Column(Integer)

    def __init__(self, fullname=None, adress=None, email=None, phone_number=None ):
        self.fullname = fullname
        self.adress = adress
        self.email = email
        self.phone_number = phone_number

class Products(Base):
    __tablename__ = 'Products'

    prod_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
    availability = Column(Boolean)
    orderlines = relationship('OrderLine')
    categ_id = Column(Integer, ForeignKey('Categories.categ_id'))

    def __init__(self, name=None, description=None, price=None, availability=None, categ_id = None):
        self.name = name
        self.description = description
        self.price = price
        self.availability = availability
        self.categ_id = categ_id


class Orders(Base):
    __tablename__ = 'Orders'

    order_id = Column(Integer, primary_key=True)
    order_data = Column(Date)
    cust_id = Column(Integer, ForeignKey('Customers.cust_id'))

    orderlines = relationship('OrderLine')

    def __init__(self, order_data=None, cust_id=None):
        self.order_data = order_data
        self.cust_id = cust_id


class Categories(Base):
    __tablename__ = 'task'

    categ_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name=None):
        self.name = name


class OrderLine(Base):
    __tablename__ = 'OrderLine'

    id = Column(Integer, primary_key=True)
    prod_id = Column(Integer, ForeignKey('Products.prod_id'))
    order_id = Column(Integer, ForeignKey('Orders.order_id'))
    quantity = Column(Integer)

    def __init__(self, prod_id=None, order_id=None, quantity = None):
        self.prod_id = prod_id
        self.order_id = order_id
        self.quantity = quantity


session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'Customers': Customers, 'Products': Products, 'Orders': Orders, 'Categories': Categories, 'OrderLine': OrderLine}


class Model:
    def pairs_from_str(self, string):
        lines = string.split(',')
        pairs = {}

        for line in lines:
            key, value = line.split('=')
            pairs[key.strip()] = value.strip()
        return pairs

    def filter_by_pairs(self, objects, pairs, cls):
        for key, value in pairs.items():
            field = getattr(cls, key)
            objects = objects.filter(field == value)
        return objects

    def insert(self, tname, columns, values):
        columns = [c.strip() for c in columns.split(',')]
        values = [v.strip() for v in values.split(',')]

        pairs = dict(zip(columns, values))
        object_class = TABLES[tname]
        obj = object_class(**pairs)

        session.add(obj)

    def commit(self):
        session.commit()

    def delete(self, tname, condition):
        pairs = self.pairs_from_str(condition)
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        objects.delete()

    def update(self, tname, condition, statement):
        pairs = self.pairs_from_str(condition)
        new_values = self.pairs_from_str(statement)
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        for obj in objects:
            for field_name, value in new_values.items():
                setattr(obj, field_name, value)

    
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
            session.execute(sql)
        finally:
            session.commit()