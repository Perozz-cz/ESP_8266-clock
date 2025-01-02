# ESP_8266-clock
ESP8266 Clock with Alarms and WiFi Configuration

This project implements a clock using the ESP8266 microcontroller. The clock features two alarms, a buzzer, and the ability to set the time via WiFi. It is programmed using MicroPython.

## Features
Digital Clock: Displays the current time.
Dual Alarms: Two configurable alarms for different times.
Buzzer: Audible alarm notification.
WiFi Time Configuration: Set the time using a WiFi connection.
Low Power: Optimized for low power consumption.

## Components Required
ESP8266 microcontroller
Buzzer module
LCD I2C 16x2 display
2 x Push buttons

## How It Works
### Clock Functionality
The ESP8266 keeps track of the current time.
### Alarms
Two alarms can be configured using the buttons.
When an alarm is triggered, the buzzer sounds until dismissed.
### WiFi Configuration
You can create a WiFi hotspot with the name "hodiny" and password "12345678" on your device.
Pres the first button and navigate to "nastaveni casu pres WIFI" then pres the second button
The ESP8266 will connect to this hotspot.
Once connected, the ESP8266 synchronizes the current time with an NTP server.

## Buzzer
The buzzer is activated for alarms and can be silenced by pressing any button.

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
Navigate and select "nastaveni casu pres WIFI"
Create a hotspot on your device with the name hodiny and password 12345678.
Navigate using the buttons to set one of the two alarms.
When an alarm goes off, the buzzer will sound. Silence it by pressing a button.

## Dependencies

### library is in this project: 
  DIYables_MicroPython_LCD_I2C: For controlling the LCD.

### preinstalled libraries in micropython
utime: For time-related operations.
network: For WiFi functionality.
ntptime: For synchronizing with an NTP server.
gc: For garbage collection.
