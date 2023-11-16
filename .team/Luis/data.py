from sqlalchemy import create_engine, Column, Integer, String, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\kingl\\Downloads\\ipc-county\\Benny\\project3.sqlite')
Base = declarative_base()
diplomas = [ 'NoHSB', 'HSB', 'CAD', 'BD']

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


def get_counties_array(sqlVar):
    Session = sessionmaker(bind=engine)
    session = Session()

    if sqlVar in diplomas:
        
        query = [getattr(CountyData, x) for x in diplomas]
        query.append(CountyData.Area_Name)
    else:
        col1 = getattr(CountyData, f"{sqlVar}_2020")
        col2 = getattr(CountyData, f"{sqlVar}_2021")
        col3 = getattr(CountyData, f"{sqlVar}_2022")
        query = [CountyData.Area_Name, col1, col2, col3]
    

   
    if sqlVar in diplomas: 
        results = session.query(*query).order_by(desc(getattr(CountyData,sqlVar))).limit(10).all()
        county_data_array = [{"Name":Area_Name, "NoHSB":NoHSB, "HSB":HSB, "CAD":CAD, "BD":BD} for NoHSB, HSB, CAD, BD, Area_Name in results]
    else:
        results = session.query(*query).order_by(desc(query[-1])).limit(10).all()
        county_data_array = [{"Name":Area_Name, 2020:col1, 2021:col2, 2022:col3} for Area_Name, col1, col2, col3 in results]
    session.close()
    return county_data_array
print(get_counties_array("BIRTHS"))