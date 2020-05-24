import gpiozero
import Adafruit_DHT
import sqlite3 as lite
import time

conn = sqlite3.connect('SystemTemp.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS atable(Timestamp TEXT, DHT11_Temp REAL, DHT11_Hum REAL, DHT22_Temp REAL, DHT22_Hum REAL, Light_exp REAL)')

def data_entry():
    unix = time.time()
    timestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

    temp11, hum11 = getDHT11data()
    temp22, hum22 = getDHT22data()


    c.execute('INSERT INTO atable (Timestamp, DHT11_Temp, DHT11_Hum, DHT22_Temp, DHT22_Hum, Light_exp) VALUES(?, ?, ?, ?, ?, ?)',
            (timestamp, temp11, hum11, temp22, hum22, light))
    conn.commit())
# dbname = 'NameofDatabase.
# get data from DHT sensor
def getDHT11data():
    DHT11sensor = Adafruit_DHT.DHT11
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHT11sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp)
        temp = temp * 9/5 + 32
    return temp, hum

def getDHT22data():
    DHT22sensor = Adafruit_DHT.DHT22
    DHTpin = 17
    hum, temp = Adafruit_DHT.read_retry(DHT22sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp)
        temp = temp * 9/5 + 32
    return temp, hum
def getSoilTemp():
    adc0 = gpiozero.MCP3008(channel=0, device=0)
    adc0 = adc0.value*3.0 # conversion from digital output (scaled from 0 to 1) to voltage output (0 to 3V)
    adc0 = adc0*75.006 - 40 # conversion from Vout to temperature [deg F]
    return adc0

def getSoilMoist():
    adc1 = gpiozero.MCP3008(channel=1, device=0)
    adc1 = adc1.value
    if adc1 <= 1.1:
        adc1 = adc1*10 - 1
    elif adc1>1.1 and adc1<=1.3:
        adc1 = adc1*25 - 17.5
    elif adc1>1.3 and adc1<=1.82:
        adc1 = adc1*48.08 - 47.5
    elif adc1>1.82 and adc1<=2.2:
        adc1 = adc1*26.32 - 7.89
    else:
        adc1 = adc1*62.5 - 87.5
    return adc1

n = 0
while n < 10:
    print('Soil Temperature: {} *F\n'.format(getSoilTemp()))
