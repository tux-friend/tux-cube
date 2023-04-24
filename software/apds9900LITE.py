"""`apdsS9900LITE`
====================================================

Low memory Driver class for the APDS9900 

    Author: Rune Langøy  2022
 
    Licence GNU General Public License v3.0
    https://www.gnu.org/licenses/gpl-3.0.html
"""
from time import sleep
from micropython import const
#APDS9960_ADDR        = const(0x39)

class I2CEX:
    """micropython i2c adds functions for reading / writing byte to a register 

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    """

    def __init__(self,
                 i2c, 
                 address):
        self.__i2c=i2c
        self.__address=address
        
    def __regWriteBit(self,reg,bitPos,bitVal):
        """Reads a I2C register byte changes a bit and writes the new value

            :param reg: The I2C register that is writen to
            :type reg: int

            :param bitPos: The bit position (0 - 7)
            :type bitPos: int        
            
            :param value: True = set-bit / False =clear bit
            :type value: bool        
        """
        val=self.__readByte(reg)   # read reg 
        if bitVal == True:
            val=val | (1<<bitPos)  # set bit
        else:
            val=val & ~(1<<bitPos) # clear bit
        
        self.__writeByte(reg,val) #write reg
  
    
    def __writeByte(self,reg,val):
        """Writes a I2C byte to the address APDS9960_ADDR (0x39)

            :param reg: The I2C register that is writen to
            :type reg: int
            :param val: The I2C value to write in the range (0- 255)
            :type val: int        
        """
        self.__i2c.writeto_mem(self.__address,reg,bytes((val,)))

    def __readByte(self,reg):
        """Reads a I2C byte from the address APDS9960_ADDR (0x39)

        :param reg: The I2C register to read
        :type reg: int

        :returns: a value in the range (0- 255)
        :rtype: int      
        """

        val =self.__i2c.readfrom_mem(self.__address,reg, 1)
        return int.from_bytes(val, 'big', True)

    def __write2Byte(self,reg,val):
        """Writes a I2C byte to the address APDS9960_ADDR (0x39)

            :param reg: The I2C register that is writen to
            :type reg: int
            :param val: The I2C value to write in the range (0- 255)
            :type val: int        
        """
        b = bytearray(2)
        b[0]=val & 0xff
        b[1]=(val>>8) & 0xff
        self.__i2c.writeto_mem(self.__address,reg,b)

    def __read2Byte(self,reg):
        """Reads a I2C byte from the address APDS9960_ADDR (0x39)

        :param reg: The I2C register to read
        :type reg: int

        :returns: a value in the range (0- 65535)
        :rtype: int      
        """
        val =self.__i2c.readfrom_mem(self.__address,reg, 2)
        return int.from_bytes(val, 'little', True)
   
  
    
class ALS(I2CEX):
    """APDS9960 Digital Ambient Light Sense (ALS) (Clear light) functionalities 
    
    :param i2c: The I2C driver
    :type i2C: machine.i2c
    """    
    def __init__(self,
                 i2c):
        super().__init__(i2c,0x39) # initiate I2CEX with APDS9960_ADDR

    def enableSensor(self,on=True):
        """Enable/Disable the Light sensor

        :param on: Enables / Disables the Light sensor
                (Default True)
        :type on: bool
        """
        AEN=1  #ALS enable bit 1 (AEN) in reg APDS9960_REG_ENABLE
        super().__regWriteBit(reg=0x00,bitPos=AEN,bitVal=on)

    @property
    def eLightGain(self):
        """Sets the receiver gain for light measurements.

        :getter: Returns the reciever gain (0 -3)
        :setter: Sets the reciever gain (0 -3)
        :type: int

        ::

            eGain    Gain
              0       1x
              1       2x
              2       16x
              3       64x
        """
        #APDS9960_REG_CONTROL = const(0x8f)
        val=super().__readByte(0x0f)
        val= val  & 0b00000011 
        return val

    @eLightGain.setter
    def eLightGain(self, eGain):
        #APDS9960_REG_CONTROL = const(0x8f)
        val=super().__readByte(0x0f)
        # set bits in register to given value
        eGain &= 0b00000011
        val &= 0b11111100
        val |= eGain

        super().__writeByte(0x0f,val)


    @property
    def ambientLightLevel(self):
        """Reads the APDS9960 ambient light level (apds9960 clear channel data)

            :getter: Returns the ambient light level (0 - 1025 ) 
            :type: int     
        """
        val_lo=super().__read2Byte(0x14)
        val_hi_byte=super().__read2Byte(0x15)
        val = val_lo + (val_hi_byte*256);
        return val  #returns CDATAL and CDATAH

    
    def setInterruptThreshold(self,high=0,low=20,persistance=4):
        """Enable/Disable the proimity sensor

        :param high: high level for generating light hardware interrupt (Range 0 - 1025)
        :type high: int 

        :param low: low level for generating light hardware interrupt (Range 0 - 1025)
        :type low: int 

        :param persistance: Number of consecutive reads before IRQ is raised (Range 0 - 7)
        :type persistance: int 

        """
        #ALS low threshold, lower byte
        super().__write2Byte(0x04, low);  #set ALS low threshold
        super().__write2Byte(0x06, high); #set ALS low threshold 
 
 
        if (persistance>7) :
            persistance=7

        val=super().__readByte(0x0C) #APDS9960_PERS 0x8C<3:0>  Proximity Interrupt Persistence 
        val=val & 0b11111000          # Clear APERS
        val=val | persistance         # Set   APERS
        super().__writeByte(0x0C,val) # Update APDS9960_PERS

    def clearInterrupt(self):
        """Crears the proimity interrupt
        IRQ HW output goes low (enables triggering of new IRQ)
        """
        super().__readByte(0xe6)    #All Non-Gesture Interrupt Clear

    def enableInterrupt(self,on=True):
        """Enables/Disables IRQ dependent on limits given by setLightInterruptThreshold()

        :param on: Enable / Disable Hardware IRQ  
        :type on: bool 
        """
        #ENABLE<AIEN> 0x80<4> ALS Interrupt Enable
        AIEN=4    #ALS Interrupt Enable bit 4 (AIEN) in reg APDS9960_REG_ENABLE
        super().__regWriteBit(reg=0x00,bitPos=AIEN,bitVal=on)
        self.clearInterrupt(); 


class PROX(I2CEX):
    """APDS9960 proximity functons

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    """    
    def __init__(self,
                 i2c):
        super().__init__(i2c,0x39) # initiate I2CEX with APDS9960_ADDR
        
    def enableSensor(self,on=True):
        """Enable/Disable the proimity sensor

        :param on: Enables / Disables the proximity sensor
                (Default True)
        :type on: bool
        """
        
        
        
        #WriteRegData (0xf, PDRIVE | PDIODE | PGAIN | AGAIN);
        
        #WriteRegData(0, 0); //Disable and Powerdown
        super().__writeByte(0x80,0x00)
        #ATIME = 0xff; // 2.7 ms – minimum ALS integration time
        super().__writeByte(0x81,0x0f)
        #PTIME = 0xff; // 2.7 ms – minimum Prox integration time
        super().__writeByte(0x82,0xff)
        #WTIME = 0xff; // 2.7 ms – minimum Wait time
        super().__writeByte(0x83,0xff)
        #WriteRegData (0xe, PPCOUNT);
        super().__writeByte(0x8e,0x1)
        
        #Set gain
        super().__writeByte(0x8f,0x20)
        
        #WEN = 8; // Enable Wait PEN = 4; // Enable Prox AEN = 2; // Enable ALS PON = 1; // Enable Power On
        super().__writeByte(0x80, 0x05);   #set low proximity threshold APDS9960_PILT
        sleep(.05)    
        #Power off
        #PON=0  #Power on
        #super().__regWriteBit(reg=0x00,bitPos=PON,bitVal=0)
        #sleep(.05)

        #setMode(PROXIMITY, 1) 
         # PEN - bit 2
        #self.eProximityGain=2 #(x4)
         
        #self.eLEDCurrent=0  #100mA
         
         
        #PON=0  #Power on
        #super().__regWriteBit(reg=0x00,bitPos=PON,bitVal=1)
        #sleep(.05)
         
        #PEN=2  #Proximity enable bit 2 (PEN) in reg APDS9960_REG_ENABLE
        #super().__regWriteBit(reg=0x00,bitPos=PEN,bitVal=1)
        #super().__writeByte(0x00, 5);   #all on

    def setInterruptThreshold(self,high=0,low=20,persistance=4):
        """Enable/Disable the proimity sensor

        :param high: high level for generating proximity hardware interrupt (Range 0 - 255)
        :type high: int 

        :param low: low level for generating proximity hardware interrupt (Range 0 - 255)
        :type low: int 

        :param persistance: Number of consecutive reads before IRQ is raised (Range 0 - 7)
        :type persistance: int 

        """   
        super().__writeByte(0x09, low);   #set low proximity threshold APDS9960_PILT
        super().__writeByte(0x0B, high);  #set high proximity threshold APDS9960_PIHT
        
        if (persistance>7) :
            persistance=7

        val=super().__readByte(0x0C) #APDS9960_PERS 0x8C<7:4>  Proximity Interrupt Persistence 
        val=val & 0b00011111          # Clear PERS
        val=val | (persistance << 4)  # Set   PERS
        super().__writeByte(0x0C,val) # Update APDS9960_PERS
        
    def clearInterrupt(self):
        """Crears the proimity interrupt
        IRQ HW output goes low (enables triggering of new IRQ)
        """
        super().__writeByte(0xE7,0) #  APDS9960_AICLEAR clear all interrupts
        super().__readByte(0xE5)    #(APDS9960_PICLEAR)
     
    def enableInterrupt(self,on=True):
        """Enables/Disables IRQ dependent on limits given by setProximityInterruptThreshold()

        :param on: Enable / Disable Hardware IRQ  
        :type on: bool 
        """
        PIEN=5    #Proximity interrupt enable bit 5 (PIEN) in reg APDS9960_REG_ENABLE
        super().__regWriteBit(reg=0x00,bitPos=PIEN,bitVal=on)
        self.clearInterrupt(); 

    @property
    def eProximityGain(self):
        """Sets the receiver gain for proximity detection.

        :getter: Returns the reciever gain (0 -3)
        :setter: Sets the reciever gain (0 -3)
        :type: int

            ::

                eGain    Gain
                  0       1x
                  1       2x
                  2       4x
                  3       8x
        """
        #APDS9960_REG_CONTROL = const(0x8f)
        val=super().__readByte(0x0f)
        val=((val >>2) & 0b00000011) 
        return val
 
    @eProximityGain.setter
    def eProximityGain(self, eGain):
        #APDS9960_REG_CONTROL = const(0x8f)
        val=super().__readByte(0x0f)
        # set bits in register to given value
        eGain &= 0b00000011
        eGain = eGain << 2
        val &= 0b11110011
        val |= eGain

        #i2c.writeto_mem(APDS9960_ADDR,APDS9960_REG_CONTROL,bytes((val,)))
        super().__writeByte(0x0f,val)

    @property
    def eLEDCurrent(self):
        """
        Sets LED current for proximity and ALS.

        :getter: Returns the LED current (0 -3)
        :setter: Sets the LED current(0 -3)
        :type: int

            ::

              eCurent  LED Current
                0        100 mA
                1         50 mA
                2         25 mA
                3         12.5 mA
        """
        #APDS9960_REG_CONTROL = const(0x8f)
        val=super().__readByte(0x0f)
        val=val >>6
        return val
  
       
    @eLEDCurrent.setter
    def eLEDCurrent(self, eCurent):
        #APDS9960_REG_CONTROL = const(0x8f)
        val=super().__readByte(0x0f)        
        
        # set bits in register to given value
        eCurent &= 0b00000011
        eCurent = eCurent << 6
        val &= 0b00111111
        val |= eCurent

        super().__writeByte(0x0f,val)
 
    @property
    def proximityLevel(self):
        """Reads the APDS9960 proximity level

            :getter: Returns the proximity level (0 - 255 ) 
            :type: int     
        """
        low=super().__readByte(0xb8)
        high=super().__readByte(0xb9)
        # (high*256)+low
        return (high*256)+low
    

class APDS9900LITE(I2CEX) :
    """APDS9900LITE low memory driver for ASDS9900  

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    
    :example:
      .. code:: python

        import machine 
        from uPy_APDS9960.APDS9960LITE import APDS9960LITE
        
        i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))  # Creates I2C Driver on Pin 5 / 6
        adps9960=APDS9960LITE(i2c)                                  # Create APDS9960 Driver
    """
    def __init__(self,
                i2c):      
        """Construct the APDS9960 driver class 

        :param i2c: The I2C driver
        :type i2C: machine.i2c
        """
        super().__init__(i2c,0x39) # initiate I2CEX with APDS9960_ADDR

        self.powerOn(False) # APDS9900_ENABLE PON=0
        sleep(.05)
        self.powerOn(True) # APDS9900_ENABLE PON=1
        self.prox=PROX(i2c)
        self.als=ALS(i2c)
        
    prox = None
    """Prvides APDS9960 Proximity functions.See class: :class:`.PROX`  

    :type PROX: 

    :example:
      .. code:: python

        apds9960=APDS9960LITE(i2c)         # Enable sensor
        apds9960.prox.enableProximity()    # Enable Proximit sensing

    """
    als = None
    """Prvides APDS9960 Light sensor functions.See class: :class:`.ALS`  

    :type PROX: 
    """
    def powerOn(self,on=True):
        """Enable/Disable the apds9900 sensor

        :param on: Enables / Disables the proximity sensor
                (Default True)
        :type on: bool
        """

        PON=0
        super().__regWriteBit(reg=0x00,bitPos=PON,bitVal=True)


    @property
    def statusRegister(self):
            """
            Status Register (0x13)
            The read-only Status Register provides the status of the device. The register is set to 0x04 at power-up.
            Returns the device status.

            :getter: Status register content byte 
  
                ====== ===== =============================
                Field  Bits  Description
                ====== ===== =============================
                x         7  Reserved 
                x         6  Reserved 
                PINT      5  Proximity Interrupt. 
                AINT      4  ALS Interrupt. 
                x         3  Reserved
                x         2  Reserved
                PVALID    1  Proximity Valid. 
                AVALID    0  ALS Valid. 
                ====== ===== =============================
 
            :rtype: int      
            """
            return super().__readByte(0x13)

