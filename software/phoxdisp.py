from phyphoxBLE import Experiment
import time
import random

def app(butstate,p):
    if butstate == 0:
        device = "Sensor BME280"
        desc = "Sensor zum Messen von Temperatur, Luftdruck und Luftfeuchtigkeit"
        view = ["Temperatur T", "Temp. 1"]
        a = ["Temperaturverlauf", "s", "C", "t", "T", 1]
        b = ["Druckverlauf", "s", "hPa", "t", "p", 1]
        c = ["Temperaturverlauf","s","C","t","T",1]
        ex =["BME280 data", "Temperatur","Druck","Temp1","Temp2"]
    elif butstate ==1:
        device = "Sensor BME282"
        desc = "Sensor zum Messen von Temperatur, Luftdruck und Luftfeuchtigkeit"
        view = ["Temperatur T  Druck p", "Temp. 1 & Temp. 2"]
        a = ["Temperaturverlauf", "s", "C", "t", "T", 1]
        b = ["Druckverlauf", "s", "hPa", "t", "p", 1]
        c = ["Temperaturverlauf","s","C","t","T",1]
        ex =["BME280 data", "Temperatur","Druck","Temp1","Temp2"]
    elif butstate ==2:
        device = "Sensor BME283"
        desc = "Sensor zum Messen von Temperatur, Luftdruck und Luftfeuchtigkeit"
        view = ["Temperatur T & Druck p", "Temp. 1 & Temp. 2"]
        a = ["Temperaturverlauf", "s", "°C", "t", "T", 1]
        b = ["Druckverlauf", "s", "hPa", "t", "p", 1]
        c = ["Temperaturverlauf","s","°C","t","T",1]
        ex =["BME280 data", "Temperatur","Druck","Temp1","Temp2"]
    elif butstate ==3:
        device = "Sensor BME284"
        desc = "Sensor zum Messen von Temperatur, Luftdruck und Luftfeuchtigkeit"
        view = ["Temperatur T & Druck p", "Temp. 1 & Temp. 2"]
        a = ["Temperaturverlauf", "s", "°C", "t", "T", 1]
        b = ["Druckverlauf", "s", "hPa", "t", "p", 1]
        c = ["Temperaturverlauf","s","°C","t","T",1]
        ex =["BME280 data", "Temperatur","Druck","Temp1","Temp2"]
    elif butstate ==4:
        device = "Sensor BME285"
        desc = "Sensor zum Messen von Temperatur, Luftdruck und Luftfeuchtigkeit"
        view = ["Temperatur T & Druck p", "Temp. 1 & Temp. 2"]
        a = ["Temperaturverlauf", "s", "°C", "t", "T", 1]
        b = ["Druckverlauf", "s", "hPa", "t", "p", 1]
        c = ["Temperaturverlauf","s","°C","t","T",1]
        ex =["BME280 data", "Temperatur","Druck","Temp1","Temp2"]
    else:
        device = "Sensor BME281"
        desc = "Sensor zum Messen von Temperatur, Luftdruck und Luftfeuchtigkeit"
        view = ["Temperatur T & Druck p", "Temp. 1 & Temp. 2"]
        a = ["Temperaturverlauf", "s", "°C", "t", "T", 1]
        b = ["Druckverlauf", "s", "hPa", "t", "p", 1]
        c = ["Temperaturverlauf","s","°C","t","T",1]
        ex =["BME280 data", "Temperatur","Druck","Temp1","Temp2"]
 
    p.start(device)
    p._write_callback = receivedData
    #Experiment
    plot = Experiment()   #generate experiment on Arduino which plot random values
    plot.setTitle(device)
    plot.setCategory("Tux Cube")
    plot.setDescription(desc)

    #View
    firstView = Experiment.View()
    firstView.setLabel(view[0]) #Create a "view"
    secondView = Experiment.View()
    secondView.setLabel(view[1]) #Create a "view"

    #Graph
    firstGraph = Experiment.Graph()   #Create graph which will plot random numbers over time
    firstGraph.setLabel(a[0])
    firstGraph.setUnitX(a[1])
    firstGraph.setUnitY(a[2])
    firstGraph.setLabelX(a[3])
    firstGraph.setLabelY(a[4])
    firstGraph.setXPrecision(a[5])                 #The amount of digits shown after the decimal point
    firstGraph.setYPrecision(a[5])

    firstGraph.setChannel(0, 1)

    #Second Graph
    secondGraph = Experiment.Graph()   #Create graph which will plot random numbers over time
    secondGraph.setLabel(b[0])
    secondGraph.setUnitX(b[1])
    secondGraph.setUnitY(b[2])
    secondGraph.setLabelX(b[3])
    secondGraph.setLabelY(b[4])
    secondGraph.setXPrecision(b[5])                 #The amount of digits shown after the decimal point
    secondGraph.setYPrecision(b[5])
    secondGraph.setColor("2E728E")                #Sets Color of line

    secondGraph.setChannel(0, 2)
    
    #Third Graph
    thirdGraph = Experiment.Graph()   #Create graph which will plot random numbers over time
    thirdGraph.setLabel(c[0])
    thirdGraph.setUnitX(c[1])
    thirdGraph.setUnitY(c[2])
    thirdGraph.setLabelX(c[3])
    thirdGraph.setLabelY(c[4])
    thirdGraph.setXPrecision(c[5])                 #The amount of digits shown after the decimal point
    thirdGraph.setYPrecision(c[5])
    thirdGraph.setColor("2E728E")                #Sets Color of line

    thirdGraph.setChannel(0, 3)

    
    #Forth Graph
    forthGraph = Experiment.Graph()   #Create graph which will plot random numbers over time
    forthGraph.setLabel(c[0])
    forthGraph.setUnitX(c[1])
    forthGraph.setUnitY(c[2])
    forthGraph.setLabelX(c[3])
    forthGraph.setLabelY(c[4])
    forthGraph.setXPrecision(c[5])                 #The amount of digits shown after the decimal point
    forthGraph.setYPrecision(c[5])
    forthGraph.setColor("2E728E")                #Sets Color of line
    
    forthGraph.setChannel(0, 4)

    
    #Export
    mySet = Experiment.ExportSet()        #Provides exporting the data to excel etc.
    mySet.setLabel(ex[0])

    myData1 = Experiment.ExportData() 
    myData1.setLabel(ex[1])
    myData1.setDatachannel(1)

    myData2 = Experiment.ExportData() 
    myData2.setLabel(ex[2])
    myData2.setDatachannel(2)
    
    myData3 = Experiment.ExportData() 
    myData3.setLabel(ex[3])
    myData3.setDatachannel(2)
    
    myData4 = Experiment.ExportData() 
    myData4.setLabel(ex[4])
    myData4.setDatachannel(4)

    #attach to experiment

    firstView.addElement(firstGraph)            #attach graph to view
    firstView.addElement(secondGraph)            #attach second graph to view
    secondView.addElement(thirdGraph)                #attach info to view
    secondView.addElement(forthGraph)
    plot.addView(firstView)         #attach view to experiment
    plot.addView(secondView)
    mySet.addElement(myData1)                   #attach data to exportSet
    mySet.addElement(myData2)                   #attach data to exportSet
    mySet.addElement(myData3)                   #attach data to exportSet
    mySet.addElement(myData4)
    plot.addExportSet(mySet)        #attach exportSet to experiment
    p.addExperiment(plot) #attach experiment to server

def receivedData():          # get data from PhyPhox app
    global editValue
    global firstCall
    if not firstCall:
        editValue = float(p.read())
    firstCall = False
