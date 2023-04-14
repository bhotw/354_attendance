# System Configuration
import time
from tts import TTS

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from luma.core.interface.serial import spi, noop

serial = spi(port = 0, device = 1, gpio = nppp())

reader = SimpleMFRC522()
