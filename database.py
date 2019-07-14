import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, DateTime, create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#Data Pre-processing
df0 = pd.read_csv('./data_in/LOS-ANGELES-DOWNTOWN_722874_CZ2010.CSV', low_memory=False)
df1 = pd.read_csv('./data_in/LONG-BEACH_722970_CZ2010.CSV', low_memory=False)
df2 = pd.read_csv('./data_in/BURBANK-GLENDALE_722880_CZ2010.CSV', low_memory=False)

df0['TYPE'] = 'CZ_2010'
df0['STATION'] = 'LOS-ANGELES-DOWNTOWN-USC'
df0['STATION_NBR'] = '722874'

df1['TYPE'] = 'CZ_2010'
df1['STATION'] = 'LONG-BEACH'
df1['STATION_NBR'] = '722970'

df2['TYPE'] = 'CZ_2010'
df2['STATION'] = 'BURBANK-GLENDALE'
df2['STATION_NBR'] = '722880'

df = pd.concat([df0, df1, df2])

df['date_time'] = df['Date (MM/DD/YYYY)'] + ' ' + df['Time (HH:MM)']

df.columns = df.columns.str.upper()

df_subset = df[['DATE (MM/DD/YYYY)',
                'TIME (HH:MM)',
                'TYPE',
                'STATION_NBR',
                'STATION',
                'DRY-BULB (C)']]

df_subset.columns = df_subset.columns.str.replace('(', '')
df_subset.columns = df_subset.columns.str.replace(')', '')
df_subset.columns = df_subset.columns.str.replace(' ', '_')
df_subset.columns = df_subset.columns.str.replace('/', '_')
df_subset.columns = df_subset.columns.str.replace('-', '_')
df_subset.columns = df_subset.columns.str.replace(':', '_')

df_subset['TIME_DT_H'] = df_subset['TIME_HH_MM'].str.split(':').str[0]
df_subset['TIME_DT_HH'] = df_subset['TIME_DT_H'].apply(lambda x: x.zfill(2))
df_subset['TEMP_F'] = 'TEMP_F_'
df_subset['TIME_DT_M'] = '00'
df_subset['DRY_BULB_F'] = (df_subset['DRY_BULB_C'] * (9 / 5)) + 32
df_subset['TIMESTAMP'] = df_subset[['TEMP_F',
                                    'TIME_DT_HH',
                                    'TIME_DT_M']].apply(lambda x: ''.join(x), axis=1)

FILTER = ['DATE_MM_DD_YYYY',
          'TIMESTAMP',
          'DRY_BULB_F',
          'TYPE',
          'STATION',
          'STATION_NBR']

df = df_subset[FILTER]

df_pivot = df.pivot_table(index=['DATE_MM_DD_YYYY',
                                 'TYPE',
                                 'STATION',
                                 'STATION_NBR'],
                          columns='TIMESTAMP',
                          values='DRY_BULB_F',
                          aggfunc='sum')

# https://stackoverflow.com/questions/38951345/how-to-get-rid-of-multilevel-index-after-using-pivot-table-pandas
df_pivot = df_pivot.rename_axis(None, axis=1).reset_index()

df_pivot.rename(columns={'DATE_MM_DD_YYYY': 'READ_DT'}, inplace=True)

df_pivot['READ_DT_MON'] = df_pivot['READ_DT'].str.split('-').str[1]
df_pivot['READ_DT_DAY'] = df_pivot['READ_DT'].str.split('-').str[2]
df_pivot['READ_DT_YEAR'] = df_pivot['READ_DT'].str.split('-').str[0]

df = df_pivot[[
    'READ_DT',
    'READ_DT_MON',
    'READ_DT_DAY',
    'READ_DT_YEAR',
    'TYPE',
    'STATION',
    'STATION_NBR',
    'TEMP_F_0000',
    'TEMP_F_0100',
    'TEMP_F_0200',
    'TEMP_F_0300',
    'TEMP_F_0400',
    'TEMP_F_0500',
    'TEMP_F_0600',
    'TEMP_F_0700',
    'TEMP_F_0800',
    'TEMP_F_0900',
    'TEMP_F_1000',
    'TEMP_F_1100',
    'TEMP_F_1200',
    'TEMP_F_1300',
    'TEMP_F_1400',
    'TEMP_F_1500',
    'TEMP_F_1600', 'TEMP_F_1700', 'TEMP_F_1800', 'TEMP_F_1900',
    'TEMP_F_2000', 'TEMP_F_2100', 'TEMP_F_2200', 'TEMP_F_2300']]

df.sort_values(by=['STATION_NBR',
                   'READ_DT_MON',
                   'READ_DT_DAY'], inplace=True)

df.reset_index(drop=True, inplace=True)

df['READ_DT'] = pd.to_datetime(df['READ_DT'])

data_dict = df.to_dict(orient='records')


#Populate SQLite Database with the data in `data_dict`
engine = create_engine('sqlite:///cz_2010.sqlite')
conn = engine.connect()
Base = declarative_base()


class Data(Base):
    __tablename__ = 'cz_2010_usc'

    id = Column(Integer, primary_key=True)
    READ_DT = Column(DateTime)
    READ_DT_MON = Column(Integer)
    READ_DT_DAY = Column(Integer)
    READ_DT_YEAR = Column(Integer)
    TYPE = Column(String)
    STATION = Column(String)
    STATION_NBR = Column(Integer)
    TEMP_F_0000 = Column(Float)
    TEMP_F_0100 = Column(Float)
    TEMP_F_0200 = Column(Float)
    TEMP_F_0300 = Column(Float)
    TEMP_F_0400 = Column(Float)
    TEMP_F_0500 = Column(Float)
    TEMP_F_0600 = Column(Float)
    TEMP_F_0700 = Column(Float)
    TEMP_F_0800 = Column(Float)
    TEMP_F_0900 = Column(Float)
    TEMP_F_1000 = Column(Float)
    TEMP_F_1100 = Column(Float)
    TEMP_F_1200 = Column(Float)
    TEMP_F_1300 = Column(Float)
    TEMP_F_1400 = Column(Float)
    TEMP_F_1500 = Column(Float)
    TEMP_F_1600 = Column(Float)
    TEMP_F_1700 = Column(Float)
    TEMP_F_1800 = Column(Float)
    TEMP_F_1900 = Column(Float)
    TEMP_F_2000 = Column(Float)
    TEMP_F_2100 = Column(Float)
    TEMP_F_2200 = Column(Float)
    TEMP_F_2300 = Column(Float)

    def __repr__(self):
        return f"id={self.id}, name={self.name}"


Base.metadata.create_all(engine)
metadata = MetaData(bind=engine)
metadata.reflect()
table = sqlalchemy.Table('cz_2010_usc', metadata, autoload=True)
conn.execute(table.delete())
conn.execute(table.insert(), data_dict)
