import pandas as pd
from matplotlib import pyplot as plt 
import seaborn as sns
import numpy as num

# READ AND SAVE DATA

jan19 = pd.read_csv('2019_01_Gener_qualitat_aire_BCN.csv') 
feb19 = pd.read_csv('2019_02_Febrer_qualitat_aire_BCN.csv') 
mar19 = pd.read_csv('2019_03_Marc_qualitat_aire_BCN.csv') 
apr19 = pd.read_csv('2019_04_Abril_qualitat_aire_BCN.csv')
jan20 = pd.read_csv('2019_01_Gener_qualitat_aire_BCN.csv') 
feb20 = pd.read_csv('2019_01_Gener_qualitat_aire_BCN.csv') 
mar20 = pd.read_csv('2019_01_Gener_qualitat_aire_BCN.csv') 
apr20 = pd.read_csv('2020_04_Abril_qualitat_aire_BCN.csv')
det = pd.read_csv('Qualitat_Aire_Detall.csv')

# QUICK INSPECTION AND MERGING DATA

#print(jan19.columns)
#visual inspection to check if all datasets contain roughly the same data
#print(jan19.columns, feb19.columns, mar19.columns, apr19.columns, jan20.columns, feb20.columns, mar20.columns, apr19.columns)
#all datasets expect for the months of april (april 2019 and 2020) contain the same column indexes.
#let's first work on the dates of january, feb and march, since they have the same characteristics.
#join datasets
frames = [jan19, feb19, mar19, jan20, feb20, mar20]
df = pd.concat(frames, keys = ['jan19', 'feb19', 'mar19', 'jan20', 'feb20', 'mar20'])
#add keys to add a column to easily see where that particular row was belonging too. Because I don't know 
#if the date column is complete in the data
#print(df.head(20))

# GENERAL DESCRIPTION OF FIELDS

# nom_cabina: the name of the city (all the same - neighborhood)
# qualitat_aire: general quality of air. Takes values Bad, Moderate, Good and '--'
# codi_dtes:code of the station/cabin
# zqa? Codi de la zona de qualitat de l'aire on està situada l'estació/cabina.
# let's see the values that it takes:
#print(df.zqa.unique())
#print(df.zqa.nunique())
#zqa only contains 1 value. 
# codi_eoi: european code to indentify station. 
# longitud and latitude: location of measure station, given in decimal degree system:
# print(df[['longitud', 'latitud']].head(50))
# hora_o3. Hora de la mesura de l'Ozó troposfèric (interval d'una hora)
# qualitat_o3. Qualitat de l'Ozó troposfèric
# valor_o3 Mitjana del valor rebut durant una hora de l'Ozó troposfèric (quan s'indica les 11:00 vols dir que la mesura s'ha fet de les 11:00 a les 12:00 hores)
# hora_no2. Hora de la mesura del Diòxid de Nitrogen (interval d'una hora)
# qualitat_no2. Qualitat del Diòxid de Nitrogen
# valor_no2. Mitjana del valor rebut durant una hora del Diòxid de Nitrogen (quan s'indica les 11:00 vols dir que la mesura s'ha fet de les 11:00 a les 12:00 hores)
# hora_pm10. Hora de la mesura de les partícules en suspensió PM10 (interval d'una hora)
# qualitat_pm10. Qualitat de les partícules en suspensió PM10: Bona, Regular o Pobra
# valor_pm10. Mitjana del valor rebut durant una hora de les partícules en suspensió PM10 (quan s'indica les 11:00 vols dir que la mesura s'ha fet de les 11:00 a les 12:00 hores)
# generat: date of colection of the data. Data i hora de generació de la informació en origen
# dateTime: Time Stamp de l'hora de descàrrega del fitxer

# IN DEPTH ANALYSIS OF IMPORTANT FIELDS

## MEASUREMENTS
#analyze data about pollution only, to better understand values:
pollutants = df[['qualitat_aire','qualitat_o3', 'valor_o3','qualitat_no2', 'valor_no2', 'qualitat_pm10', 'valor_pm10']]
#print(pollutants.head(50))
# check if the quality of air takes the said values.
#print('number quality ranges', pollutants.qualitat_aire.unique())
#it takes values of Good, Moderate, Bad, and '--' (this last one was not mentioned before)
#From observing the data, it seems that the Quality of air and other quality indecators are redundant, because:
# Air quality will take the qualification of good or moderate even if only one of the values of measurement is present
is_airq_bad = pollutants['qualitat_aire'] == 'Pobra'
airq_bad = pollutants[is_airq_bad]
#print(airq_bad)
# If one of the measurements is bad, the general air quality will be assigned as bad
is_airq_good = pollutants['qualitat_aire'] == 'Bona'
airq_good = pollutants[is_airq_good]
#print(airq_good.head(50))
# Now for '--'
is_airq_nonexistant = pollutants['qualitat_aire'] == '--'
airq_nonex = pollutants[is_airq_nonexistant]
#print(airq_nonex.head(50))
#all of this need to go (later)
#i will discard the columns for qualitative values. the values for qualitative measures should be more strict.



# Range of each measurement.


## TIME

#print(df[['hora_o3','qualitat_o3', 'valor_o3' ]])
#gives time of the o3 measurement. Is it the same time as the rest of measurementes in that row? is it the same as the refelcted in date?
#let's check if its the same as for no2, pm and generat:
times = df[['hora_o3', 'hora_no2', 'hora_pm10', 'generat']]
#print(times.head(50))

#there are inconsistencies in the times. for example:
#in the line 49: sais o3 was taken at 3h, n02 as 3h and pm at 5h, but the time says 6:00. let's first
#this is not further explained in the info of the data. if that happens, we might want to discard that data.

#CLEANING DATA

#remove column of qualitative data. keep lcation and values
#print(df.head(50))
#print(df.columns)
df1 = df[['nom_cabina', 'longitud', 'latitud', 'hora_o3', 'valor_o3', 'hora_no2', 'valor_no2', 'hora_pm10', 'valor_pm10', 'generat']]
#print(df1.head(50))
df1.info()
#son, from all 34920 rows of data, the o3 value is the one that is less present in the data.
#are there full empty rows?

#"generat", and 'hours are not datatype

#check info datasets
#print(df.info)



#imp = df[['qualitat_aire','qualitat_o3', 'valor_o3','qualitat_no2', 'valor_no2', 'qualitat_pm10', 'valor_pm10']]
#print(imp.head(50))


#index ofQuè és l'Índex Català de Qualitat de l'Aire? 
#  http://mediambient.gencat.cat/ca/05_ambits_dactuacio/atmosfera/qualitat_de_laire/avaluacio/icqa/que_es_lindex_catala_de_qualitat_de_laire/index.html

#how many different stations are? 

