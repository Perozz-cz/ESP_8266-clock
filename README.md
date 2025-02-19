# ESP_8266-clock
ESP8266 Clock with Alarms and WiFi synchronization

This project implements a clock using the ESP8266 microcontroller. The clock features two alarms, motion detector for activation backlight, a buzzer, and the ability to set the time via WiFi. It is programmed using MicroPython.

## Features
Digital Clock: Displays the current time.

Dual Alarms: Two configurable alarms for different times.

Buzzer: Alarm notification.

Time synchronization via WIFI: Set the time using a WiFi connection.

Automatic display light switch: If there is no motion display light turns off.

## Components Required
ESP8266 microcontroller

Buzzer module

LCD I2C 16x2 display

2 x Push buttons

Motion detector HC-SR501

## How It Works
### Clock Functionality

The ESP8266 keeps track of the current time.

### Alarms

Two alarms can be configured using the buttons.

When an alarm is triggered, the buzzer sounds until dismissed.
### WiFi Configuration

if you want to synchronize the clock create a WiFi hotspot with the name `hodiny` and password `12345678` on your phone or other device.

Pres the first button and navigate to `nastaveni casu pres WIFI` then pres the second button

The ESP8266 will connect to this hotspot.

Once connected, the ESP8266 synchronizes the current time with NTP server.

## Buzzer
The buzzer is activated for alarms and can be silenced by pressing any button.

## Motion detector
If motion isn't detected for 20 seconds, the display background light turns off.

## LCD Display
The LCD I2C 16x2 display shows the current time, alarm settings...

It is connected via I2C and requires minimal wiring.

## Getting Started
### Prerequisites
Install MicroPython on your ESP8266.

Install a MicroPython IDE like Thonny or pymakr.

### Setup
Upload Code

Clone or download the repository.

Use your IDE to upload the Python files to the ESP8266.

## Running the Clock
Power on the ESP8266

The clock will initialize and display the time on the LCD.

Navigate and select `nastaveni casu pres WIFI`

Create a hotspot on your device with the name `hodiny` and password `12345678`.

Navigate using the buttons to set one of the two alarms.

When an alarm goes off, the buzzer will sound. Silence it by pressing any button.

## Dependencies
### library is in this project: 
  DIYables_MicroPython_LCD_I2C: For controlling the LCD.

### preinstalled libraries in micropython
utime: For time-related operations.

network: For WiFi functionality.

ntptime: For synchronizing with an NTP server.

gc: For garbage collection.

# Wiring
## LCD I2C 16x2 display
SCL --> ESP 8266 | Pin D1

SDA --> ESP 8266 | Pin D2

VCC --> ESP 8266 | 3V

GND --> ESP 8266 | GND
## Motion detector HC-SR501
VCC --> ESP 8266 | 3V

OUT --> ESP 8266 | Pin D5

GND --> ESP 8266 | GND
## Push button - 1
Button Pin 1 --> ESP 8266 | GND

Button Pin 2 --> ESP 8266 | Pin D7
## Push button - 2
Button Pin 1 --> ESP 8266 | GND

Button Pin 2 --> ESP 8266 | Pin D6
## Buzzer
Buzzer Pin 1 --> ESP 8266 | GND

Buzzer Pin 2 --> ESP 8266 | D8
