#Python script fr RFID Zeiterfassung
import RPi.GPIO as GPIO
import MFRC522
import urllib.request

buttonPin = 12 #define buttonPin

mfrc = MFRC522.MFRC522()

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    isScan = True
    while isScan:
        (status,TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
        if status == mfrc.MI_OK:
            print("Card detected")
            (status,uid) = mfrc.MFRC522_Anticoll()
            if status == mfrc.MI_OK:
                print ("Card UID: "+ str(list(map(hex,uid))))
                url = "http://localhost:4000/rfidlog?chip=%X%X%X%X%X"%(uid[0], uid[1], uid[2], uid[3], uid[4])
                print("sending http-request to ", url)
                request = urllib.request.urlopen(url).read()
                print(request)
                isScan = False
                
def destroy():
    GPIO.cleanup()
    
if __name__ == "__main__":
    print("Push button to start scan...")
    setup()
    try:
        while True:
            if GPIO.input(buttonPin)==GPIO.LOW:
                print("scanning....")
                loop()
    except Exception as e:
        print("programm aborting due to exception. ")
        print(e)
    finally:     
         destroy()
        

