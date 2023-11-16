from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\justi\\OneDrive\\Desktop\\Data Analysis Boot Camp\\Projects\\Project 3\\ipc-county\\Benny\\project3.sqlite')
Base = declarative_base()

class CountyData(Base):
    __tablename__ = 'counties'

    id = Column(Integer, primary_key=True)
    FIPS_Code = Column(Integer)
    State = Column(String)
    Area_Name = Column(String)
    Civilian_labor_force_2020 = Column(Integer)
    Employed_2020 = Column(Integer)
    Unemployed_2020 = Column(Integer)
    Unemployment_rate_2020 = Column(Integer)
    Civilian_labor_force_2021 = Column(Integer)
    Employed_2021 = Column(Integer)
    Unemployed_2021 = Column(Integer)
    Unemployment_rate_2021 = Column(Integer)
    Civilian_labor_force_2022 = Column(Integer)
    Employed_2022 = Column(Integer)
    Unemployed_2022 = Column(Integer)
    Unemployment_rate_2022 = Column(Integer)
    POP_ESTIMATE_2020 = Column(Integer)
    POP_ESTIMATE_2021 = Column(Integer)
    POP_ESTIMATE_2022 = Column(Integer)
    BIRTHS_2020 = Column(Integer)
    BIRTHS_2021 = Column(Integer)
    BIRTHS_2022 = Column(Integer)
    DEATHS_2020 = Column(Integer)
    DEATHS_2021 = Column(Integer)
    DEATHS_2022 = Column(Integer)
    NoHSB = Column(Integer)
    HSB = Column(Integer)
    CAD = Column(Integer)
    BD = Column(Integer)



def get_counties_list(sqlVar):
    Session = sessionmaker(bind=engine)
    session = Session()
    column = getattr(CountyData, sqlVar)
    results = session.query(CountyData.FIPS_Code, column).all()
    county_data_map = {fips: column for fips, column in results}
    session.close()

    return county_data_map


