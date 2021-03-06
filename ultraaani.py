# VCC an Pin 2 (VCC)
# GND an Pin 6 (GND)
# TRIG an Pin 12 (GPIO18)
# ECHO 330 ohm vastuskytkenta (GPIO24) ja  GND

# Tuodaan kirjastot kayttoon
import RPi.GPIO as GPIO
import time

# GPIO tila (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO kaytettavat  pinnit
GPIO_TRIGGER = 18  # Fyysinen 12
GPIO_ECHO = 24  # Fyysinen 18

# GPIO-Pinnien toimintasuunta, asettaminen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def etaisyys():
    # Aseta Trigger HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Aseta Trigger 0.01ms jalkeen LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    aloitus_aika = time.time()
    lopetus_aika = time.time()

    # Tallenna aloitus_aika
    while GPIO.input(GPIO_ECHO) == 0:
        aloitus_aika = time.time()

    # Tallenna lopetus_aika
    while GPIO.input(GPIO_ECHO) == 1:
        lopetus_aika = time.time()

    # Aikaero
    kulunut_aika = lopetus_aika - aloitus_aika
    # Aanennopeus (34300 cm/s)
    # jaetaan 2:lla, koska ultraääni menee edestakaisin
    etaisyys = (kulunut_aika * 34300) / 2

    return etaisyys

if __name__ == '__main__':
    try:
        print("Mittaus aloitettu.")
        while True:
            mitattu_etaisyys = etaisyys()
            print("Mitattu etaisyys  {:.1f} cm".format(mitattu_etaisyys))
            time.sleep(1)
    except KeyboardInterrupt:
        # Keskeytys ctrl+C
        print("Mittaus pysaytetty.")
        GPIO.cleanup()
