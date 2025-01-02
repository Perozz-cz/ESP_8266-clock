from machine import I2C, Pin
from DIYables_MicroPython_LCD_I2C import LCD_I2C
import utime
import network
import ntptime
import gc

gc.collect()  # Spustí garbage collector
print("Volná paměť:", gc.mem_free())  # Ukáže volnou paměť

ssid = "hodiny"       # Zde zadej název Wi-Fi sítě
password = "12345678"   # Zde zadej heslo k Wi-Fi síti

# nastaveni delky rozsviceni po zazanamenanam pohybu v sekundach
delka_rozsviceni = 20
# Initialize I2C
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=400000)
# Initialize LCD
lcd = LCD_I2C(i2c, 0x27, 2, 16)

tlacitko_1 = Pin(13, Pin.IN, Pin.PULL_UP)
tlacitko_2 = Pin(12, Pin.IN, Pin.PULL_UP)

detektor_pohybu = Pin(14, Pin.IN)

buzzer = Pin(15, Pin.OUT)
buzzer.value(0)


posledni_detekce = utime.ticks_ms()



screen_selected = 0


budiky = [[], ["__", "__", "__", "", ""], ["__", "__", "__", "", ""]]



# Setup function
lcd.backlight_on()
lcd.clear()
lcd.set_cursor(0, 0)

def ziskat_cas():
    global year, month, day, hour, minute, second
    current_time = utime.localtime()  # Získání aktuálního času
    year, month, day, hour, minute, second, _, _ = current_time
    hour += 1 # casove pasmo
    if hour > 23: hour = 0

def detekce_pohybu():
    global posledni_detekce
    aktualni_cas = utime.ticks_ms()

    if detektor_pohybu.value() == 1: 
        print("Pohyb detekovan")
        utime.sleep(0.2)
        lcd.backlight_on()
        posledni_detekce = utime.ticks_ms()
    # zhasnuti po uplinulem casu od detekce
    if utime.ticks_diff(aktualni_cas, posledni_detekce) > delka_rozsviceni * 1000:
        lcd.backlight_off()


def screen_selector():
    global screen_selected
    if tlacitko_1.value() == 0: 
        print("tlacitko 1")
        screen_selected += 1 # tlacitko 1 - dalsi obrazovka
        lcd.clear()
    if screen_selected == 0:
        home_screen() # zobrazeni home screen
    elif screen_selected == 1:
        wifi_setting_screen() # zobrazeni nastaveni wifi
    elif screen_selected == 2:
        budik_setting_screen() # zobrazeni nastaveni budiku
    elif screen_selected == 3:
        screen_selected = 0


def home_screen():
    lcd.set_cursor(0, 0) # prvni radek
    lcd.print(str(hour) + ":" + str(minute) + ":" + str(second) + "        ")
    lcd.set_cursor(0, 1) # druhy radek
    lcd.print(str(day) + "." + str(month) + "." + str(year) + "      ")


def budik_setting_screen():
    global screen_selected
    lcd.set_cursor(0, 0) # prvni radek
    lcd.print("nastaveni budiku")
    if tlacitko_2.value() == 0:
        lcd.set_cursor(0, 0)
        lcd.print("  vyber budiku  ")
        lcd.set_cursor(0, 1)
        lcd.print("   tlacitko 2   ")
        utime.sleep(2)
        lcd.clear()
        while True:
            lcd.set_cursor(0, 0)
            lcd.print("    budik 1     ")
            utime.sleep(2)
            if tlacitko_2.value() == 0:
                lcd.clear()
                lcd.set_cursor(0, 0)
                lcd.print("    loading     ")
                utime.sleep(3)
                budik_setting(1)
                screen_selected = 0
                return
            if tlacitko_1.value() == 0:
                return
            lcd.set_cursor(0, 0)
            lcd.print("    budik 2     ")
            utime.sleep(2)
            if tlacitko_2.value() == 0:
                lcd.clear()
                lcd.set_cursor(0, 0)
                lcd.print("    loading     ")
                utime.sleep(3)
                budik_setting(2)
                screen_selected = 0
                return
            if tlacitko_1.value() == 0:
                return


def budik_setting(budik):
    global budiky
    global posledni_detekce
    pocitadlo = 0
    misto = 0
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.print(" nastav budik " + str(budik) + "")
    while True:
        if tlacitko_1.value() == 0:
            if misto < 4: misto += 1
            else : misto = 0

        if tlacitko_2.value() == 0:
            if budiky[budik][misto] == "__":
               budiky[budik][misto] = "00"
            elif misto == 0:
                if budiky[budik][misto] == "23":
                    budiky[budik][misto] = "00"
                else:
                    i = str(int(budiky[budik][misto]) + 1)
                    if len(i) == 1:
                        i = "0" + i
                    budiky[budik][misto] = i

            elif misto == 1:
                if budiky[budik][misto] == "59":
                    budiky[budik][misto] = "00"
                else:
                    i = str(int(budiky[budik][misto]) + 1)
                    if len(i) == 1:
                        i = "0" + i
                    budiky[budik][misto] = i

            elif misto == 2:
                if budiky[budik][misto] == "59":
                    budiky[budik][misto] = "00"
                else:
                    i = str(int(budiky[budik][misto]) + 1)
                    if len(i) == 1:
                        i = "0" + i
                    budiky[budik][misto] = i

            elif misto == 3:
                print("saved")
                posledni_detekce = utime.ticks_ms()
                lcd.clear()
                return

            elif misto == 4:
                budiky[budik] = ["__", "__", "__", "", ""]
                lcd.clear()
                posledni_detekce = utime.ticks_ms()
                return

        if pocitadlo % 4 == 0:
            lcd.set_cursor(0, 1)
            lcd.print(budiky[budik][0] + ":" + budiky[budik][1] + ":" + budiky[budik][2] + "  OK" + "  ><")
        elif pocitadlo % 2 == 0:
            lcd.set_cursor(0, 1)
            if misto == 0:
                lcd.print("  " + ":" + budiky[budik][1] + ":" + budiky[budik][2] + "  OK" + "  ><")
            elif misto == 1:
                lcd.print(budiky[budik][0] + ":" + "  " + ":" + budiky[budik][2] + "  OK" + "  ><")
            elif misto == 2:
                lcd.print(budiky[budik][0] + ":" + budiky[budik][1] + ":" + "  " + "  OK" + "  ><")
            elif misto == 3:
                lcd.print(budiky[budik][0] + ":" + budiky[budik][1] + ":" + budiky[budik][2] + "    " + "  ><")
            elif misto == 4:
                lcd.print(budiky[budik][0] + ":" + budiky[budik][1] + ":" + budiky[budik][2] + "  OK" + "    ")
        pocitadlo += 1
        utime.sleep(0.2)



def wifi_setting_screen():
    global screen_selected
    lcd.set_cursor(0, 0) # prvni radek
    lcd.print(" nastaveni casu ")
    lcd.set_cursor(0, 1) # druhy radek
    lcd.print("   pres wifi    ")
    if tlacitko_2.value() == 0:
        global ssid
        global password
        while True:
            lcd.set_cursor(0, 0)
            lcd.print("tlac. 1  zruseni")
            lcd.set_cursor(0, 1)
            lcd.print("vytvorte hotspot")
            
            utime.sleep(2)
            lcd.set_cursor(0, 0)
            lcd.print(" nazev: hodiny  ")
            lcd.set_cursor(0, 1)
            lcd.print("heslo: 12345678 ")
            
            utime.sleep(2)
            wifi = network.WLAN(network.STA_IF)
            wifi.active(True)
            print("Pripojuji se k Wi-Fi ...")
            lcd.set_cursor(0, 0)
            lcd.print("  Pripojuji se  ")
            lcd.set_cursor(0, 1)
            lcd.print("  k Wi-Fi ...   ")
            wifi.connect(ssid, password)
            utime.sleep(0.7)
            if tlacitko_1.value() == 0:
                return
            if wifi.isconnected():
                while True:
                    print("Pripojen k Wi-Fi!")
                    lcd.set_cursor(0, 0)
                    lcd.print("    Pripojen    ")
                    lcd.set_cursor(0, 1)
                    lcd.print("    k Wi-Fi     ")
                    print("IP adresa:", wifi.ifconfig()[0])
                    utime.sleep(0.5)
                    while True:
                        try:
                            ntptime.settime()
                            print("NTP synchronizace OK")
                            lcd.set_cursor(0, 0)
                            lcd.print("  NTP synchroni-  ")
                            lcd.set_cursor(0, 1)
                            lcd.print("    zace OK     ")
                            lcd.clear()
                            screen_selected = 0
                            return
                        except OSError:
                            print("Chyba synchronizace ...")
                            lcd.set_cursor(0, 0)
                            lcd.print(" Chyba synch... ")
                            lcd.set_cursor(0, 1)
                            lcd.print("opakuji synch...")
                            utime.sleep(1)

def budik_vyhodnotit():
    global budiky
    print(budiky)
    global year, month, day, hour, minute, second
    lenhour = str(hour)
    if len(str(hour)) == 1: lenhour = "0" + str(lenhour)
    lenminute = str(minute)
    if len(str(minute)) == 1: lenminute = "0" + str(lenminute)
    lensecond = str(second)
    if len(str(second)) == 1: lensecond = "0" + str(lensecond)


    if budiky[1][0] == lenhour and budiky[1][1] == lenminute and budiky[1][2] == lensecond:
        budik_start(1)
        return
    if budiky[2][0] == lenhour and budiky[2][1] == lenminute and budiky[2][2] == lensecond:
        budik_start(2)
        return

def budik_start(budik):
    global posledni_detekce
    global budiky
    global year, month, day, hour, minute, second
    global screen_selected
    screen_selected = 0
    lcd.backlight_on()
    lcd.clear()
    while True:
        ziskat_cas()
        lcd.set_cursor(0, 0)
        lcd.print(str(hour) + ":" + str(minute) + ":" + str(second) + "        ")
        print("beep " + str(budik))
        lcd.set_cursor(0, 1)
        lcd.print("budik " + str(budik) + " " + budiky[budik][0] + ":" + budiky[budik][1] + ":" + budiky[budik][2])
        buzzer.value(1)  # Zapnutí
        if tlacitko_1.value() == 0 or tlacitko_2.value() == 0:
            buzzer.value(0)  # Vypnutí
            posledni_detekce = utime.ticks_ms()
            return
        utime.sleep(0.3)


# Main loop function
while True:
    detekce_pohybu()
    ziskat_cas()
    budik_vyhodnotit()
    print(f"Aktuální čas: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")

    screen_selector()
    utime.sleep(0.5)
