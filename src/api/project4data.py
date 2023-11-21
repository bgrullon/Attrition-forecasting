from sqlalchemy import create_engine, Column, Integer, String, Float, desc, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\benny\\Github\\Attrition-forecasting\\src\\api\\proj4data.sqlite')
Base = declarative_base()

class AttritionData(Base):
    __tablename__ = 'mytable'

    customer_ID = Column(String, primary_key=True)
    gender = Column(String)
    senior_citizen = Column(Integer)
    partner = Column(String)
    dependants = Column(String)
    tenure = Column(Integer)
    phone_service = Column(String)
    multiple_lines = Column(String)
    internet_service = Column(String)
    online_security = Column(String)
    online_backup = Column(String)
    device_protection = Column(String)
    tech_support = Column(String)
    streaming_TV = Column(String)
    streaming_movies = Column(String)
    contract = Column(String)
    paperless_billing = Column(String)
    payment_method = Column(String)
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    churn = Column(String)
    
def bar_chart_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    column = getattr(AttritionData, 'churn')
    results = session.query(AttritionData.customer_ID, column).all()
    county_data_map = {fips: column for fips, column in results}
    session.close()

    return county_data_map
    



