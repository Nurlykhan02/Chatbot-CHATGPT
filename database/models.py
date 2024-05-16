from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, VARCHAR
Base = declarative_base()

class CustomersTable(Base):
    __tablename__ = "openai_customers"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(VARCHAR(100), index=True)
    saID = Column(Integer, index=True)
    openai_thread = Column(VARCHAR(255), index= True)