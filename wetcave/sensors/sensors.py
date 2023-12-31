from .hp206c import hp206c
import RPi.GPIO as GPIO
import sys
import time
from logging import getLogger
from statistics import mean,stdev
from datetime import datetime
from math import sqrt
usleep = lambda x: time.sleep(x*1e-6)
logger=getLogger(__name__)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class SensorCollector:
    sounderpin=24
    nbarosamples=10
    nsoundersamples=15
    def __init__(self):
        self.pres_temp=hp206c()
        ret=self.pres_temp.isAvailable()
        if self.pres_temp.OK_HP20X_DEV == ret:
            logger.info("Barometer is available.")
        else:
            logger.info("Barometer isn't availablei, disabling")
            self.pres_temp=None
        
        #setup ultrasounder
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
    
    def __del__(self):
        logger.info("Cleanup of GPIO")
        GPIO.cleanup()

    def sampleBaro(self):
            pres=None
            temp=None
            presstd=None
            tempstd=None
            if self.pres_temp:
                preslist=[]
                templist=[]
                for i in range(self.nbarosamples+1):
                    p=self.pres_temp.ReadPressure()
                    if (p < 600):
                        #sometimes the first measurement is wrong
                        continue
                    t=self.pres_temp.ReadTemperature()
                    
                    preslist.append(p)
                    templist.append(t)
                
                error_scale=1.0/sqrt(len(preslist)) 
                pres=mean(preslist)
                temp=mean(templist)
                presstd=stdev(preslist)*error_scale
                tempstd=stdev(templist)*error_scale

            return {"pressure":pres,"temperature":temp,"pressure_error":presstd,"temperature_error":tempstd}

    def sampleRangeSingle(self):
        #To initiate a measurement start by sending a pulse to the pin as output 
        GPIO.setup(self.sounderpin, GPIO.OUT)
        
        GPIO.output(self.sounderpin,GPIO.LOW)
        usleep(2)
        GPIO.output(self.sounderpin,GPIO.HIGH)
        usleep(10)
        GPIO.output(self.sounderpin,GPIO.LOW)
        
        #turn the pin in an input pin and wait for a pulse (and compute the length of the pulse)
        GPIO.setup(self.sounderpin, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        
        riseDetected=GPIO.wait_for_edge(self.sounderpin, GPIO.RISING,timeout=100)
        if not riseDetected:
            return None

        t1=time.time()

        fallDetected=GPIO.wait_for_edge(self.sounderpin, GPIO.FALLING,timeout=100)
        
        if not fallDetected:
            return None
        t2=time.time()

        traveltime=t2-t1
        return traveltime*1e6

    def sampleRange(self,outlierbounds=[800,12000]):
        dtlist=[]
        for i in range(self.nsoundersamples+1):
            dt=self.sampleRangeSingle()
            if dt == None:
                #try again
                continue
            if dt < outlierbounds[0] or dt > outlierbounds[1]:
                #outlier don't use in the computation of the mean
                continue
            dtlist.append(dt)
        nsamples=len(dtlist)
        if nsamples < 2:
            #don't return data if the amount of data points is below the bare minimum
            logger.info(f"Not enough samples for the range: {nsamples}")
            return {}

        error_scale=1.0/sqrt(nsamples) 
        return {"traveltime":mean(dtlist),"traveltime_error":stdev(dtlist)* error_scale}

    def sample(self,traveltime_outlierbounds=None):
        sensordict=self.sampleBaro()
        sensordict.update(self.sampleRange(traveltime_outlierbounds))
        sensordict["epoch"]=datetime.now().astimezone()
        return sensordict
