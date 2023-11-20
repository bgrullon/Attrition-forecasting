from sqlalchemy import create_engine, Column, Integer, String, Decimal, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\kingl\\Downloads\\Attrition-forecasting\\Luis\\proj4data.sqlite')
Base = declarative_base()

class AttritionData(Base):
    __tablename__ = 'attrition'

    customerID = Column(String, primary_key=True)
    gender = Column(String)
    SeniorCitizen = Column(Integer)
    Partner = Column(String)
    Dependants = Column(String)
    tenure = Column(Integer)
    PhoneService = Column(String)
    MultipleLines = Column(String)
    InternetService = Column(String)
    OnlineSecurity = Column(String)
    OnlineBackup = Column(String)
    DeviceProtection = Column(String)
    TechSupport = Column(String)
    StreamingTV = Column(String)
    StreamingMovies = Column(String)
    Contract = Column(String)
    PaperlessBilling = Column(String)
    PaymentMethod = Column(String)
    MonthlyCharges = Column(Decimal(precision=10, scale=2))
    TotalCharges = Column(Decimal(precision=10, scale=2))
    Churn = Column(String)
    
def bar_chart_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    columns = AttritionData.__table__.columns.keys()
    data_dict = {}
    for column in columns:
    
        if column == 'customerID':
            continue

        results = session.query(AttritionData.customerID, column).all()

        data_dict = {fips: column for fips, column in results}
        return data_dict
    



