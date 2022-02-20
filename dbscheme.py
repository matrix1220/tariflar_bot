
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Integer, String, Boolean, Text, DateTime
from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint

from sqlalchemy.ext.mutable import Mutable, MutableList, MutableDict

from sqlalchemy.types import TypeDecorator, VARCHAR, JSON
import json

class JSONEncoded(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None: value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None: value = json.loads(value)
        return value

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	menu_stack = Column(MutableList.as_mutable(JSONEncoded), nullable=False)
	shared_data = Column(JSON)
	keyboard = Column(MutableDict.as_mutable(JSONEncoded))
	language = Column(Integer)
	last_time = Column(Integer)
	blocked = Column(Boolean, default=False)

	def __init__(self, menu_stack=[], keyboard={}, **kwargs):
		super().__init__(menu_stack=menu_stack, keyboard=keyboard, **kwargs)

class Message(Base): # InlineMenu
	__tablename__ = 'messages'

	chat_id = Column(Integer, primary_key=True)
	message_id = Column(Integer, primary_key=True)
	content = Column(MutableDict.as_mutable(JSONEncoded))
	menu_stack = Column(MutableList.as_mutable(JSONEncoded), nullable=False)
	shared_data = Column(JSON)
	#menu_arguments = Column(MutableObject.as_mutable(JSONEncoded))
	keyboard = Column(MutableDict.as_mutable(JSONEncoded))
	sent_at = Column(Integer)

	def __init__(self, menu_stack=[], keyboard={}, **kwargs):
		super().__init__(menu_stack=menu_stack, keyboard=keyboard, **kwargs)

class Company(Base):
	__tablename__ = 'companies'

	id = 			Column(Integer, primary_key=True)
	name = 			Column(String)

class Tariff(Base):
	__tablename__ = 'tariffs'

	company_id = 	Column(Integer, ForeignKey('companies.id'), primary_key=True)
	id = 			Column(Integer, primary_key=True)
	name = 			Column(String)

class TariffProperty(Base):
	__tablename__ = 'tariff_properties'

	# foreign key bug
	company_id = 	Column(Integer, primary_key=True)
	tariff_id = 	Column(Integer, primary_key=True)
	name = 			Column(String)
	value = 		Column(JSON)

	__table_args__ = (
		ForeignKeyConstraint(
			[company_id, tariff_id],
			[Tariff.company_id, Tariff.id]
		),
	)

from config import engine
Base.metadata.create_all(engine)