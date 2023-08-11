from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"


print(User.__tablename__)
print(Address.__table__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# investiga o schema do banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    leo = User(
        name='leonardo',
        fullname='Leonardo Scatolin',
        address=[Address(email_address='leo@email.com')]
    )

    scatolin = User(
        name='scatolin',
        fullname='Scatolin Junior',
        address=[Address(email_address='sct@email.com'),
                 Address(email_address='lin@email.com')]
    )

    pk = User(
        name='pk',
        fullname='Patrick de Paula'
    )

    # enviando para o banco de dados (persistência de dados)
    session.add_all([leo, scatolin, pk])

    session.commit()

stmt = select(User).where(User.name.in_(["leonardo", 'pk']))
print('Recuperando usuários a partir de condição de filtragem')
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print('\nRecuperando os endereços de scatolin')
for address in session.scalars(stmt_address):
    print(address)


stmt_order = select(User).order_by(User.fullname.desc())
print('\nRecuperando info de maneira ordenada')
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

# print(select(User.fullname, Address.email_address).join_from(Address, User))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print('\nExecutando statment a partir da connection')
for result in results:
    print(result)

print('\nTotal de instância em User')
stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)
