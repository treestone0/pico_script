import board
import digitalio
import general
import enp

pin1 = digitalio.DigitalInOut(board.GP1)
pin1.direction = digitalio.Direction.INPUT
print('pin1, family', pin1.value)
if pin1.value is True:
    app = "family"
    general.run(app)

pin2 = digitalio.DigitalInOut(board.GP2)
pin2.direction = digitalio.Direction.INPUT
print('pin2, gin', pin2.value)
if pin2.value is True:
    app = "gin"
    general.run(app)

pin3 = digitalio.DigitalInOut(board.GP3)
pin3.direction = digitalio.Direction.INPUT
print('pin3, match masters', pin3.value)
if pin3.value is True:
    app = "match_masters"
    general.run(app)

pin4 = digitalio.DigitalInOut(board.GP4)
pin4.direction = digitalio.Direction.INPUT
print('pin4, club vegas', pin4.value)
if pin4.value is True:
    app = "club_vegas"
    general.run(app)

pin5 = digitalio.DigitalInOut(board.GP5)
pin5.direction = digitalio.Direction.INPUT
print('pin5, coin', pin5.value)
if pin5.value is True:
    app = "coin"
    general.run(app)

print('pin null, enp')
app = "enp"
general.run(app)