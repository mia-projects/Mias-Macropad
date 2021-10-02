#import board
#import digitalio
import time
#import gc
#import rotaryio
#import keypad
#import neopixel
from adafruit_macropad import MacroPad
from rainbowio import colorwheel

macropad = MacroPad()

# Bind keycodes to the pad
page_count = 4
keybindings = [[macropad.Keycode.A for i in range(12)] for j in range(page_count)]
page_titles = ["MacroPad"] * page_count

#page 0
page_titles[0] = "Number Pad"
keybindings[0][0] = macropad.Keycode.SEVEN
keybindings[0][1] = macropad.Keycode.EIGHT
keybindings[0][2] = macropad.Keycode.NINE
keybindings[0][3] = macropad.Keycode.FOUR
keybindings[0][4] = macropad.Keycode.FIVE
keybindings[0][5] = macropad.Keycode.SIX
keybindings[0][6] = macropad.Keycode.ONE
keybindings[0][7] = macropad.Keycode.TWO
keybindings[0][8] = macropad.Keycode.THREE
keybindings[0][9] = macropad.Keycode.ZERO
keybindings[0][10] = macropad.Keycode.BACKSPACE
keybindings[0][11] = macropad.Keycode.ENTER

#page 1
page_titles[1] = "Function Keys"
keybindings[1][0] = macropad.Keycode.F22
keybindings[1][1] = macropad.Keycode.F23
keybindings[1][2] = macropad.Keycode.F24
keybindings[1][3] = macropad.Keycode.F19
keybindings[1][4] = macropad.Keycode.F20
keybindings[1][5] = macropad.Keycode.F21
keybindings[1][6] = macropad.Keycode.F16
keybindings[1][7] = macropad.Keycode.F17
keybindings[1][8] = macropad.Keycode.F18
keybindings[1][9] = macropad.Keycode.F13
keybindings[1][10] = macropad.Keycode.F14
keybindings[1][11] = macropad.Keycode.F15

#page 2
keybindings[2][0] = macropad.Keycode.F22
keybindings[2][1] = macropad.Keycode.F23
keybindings[2][2] = macropad.Keycode.F24
keybindings[2][3] = macropad.Keycode.F19
keybindings[2][4] = macropad.Keycode.F20
keybindings[2][5] = macropad.Keycode.F21
keybindings[2][6] = macropad.Keycode.F16
keybindings[2][7] = macropad.Keycode.F17
keybindings[2][8] = macropad.Keycode.F18
keybindings[2][9] = macropad.Keycode.F13
keybindings[2][10] = macropad.Keycode.F14
keybindings[2][11] = macropad.Keycode.F15

#page 3
keybindings[3][0] = macropad.Keycode.F22
keybindings[3][1] = macropad.Keycode.F23
keybindings[3][2] = macropad.Keycode.F24
keybindings[3][3] = macropad.Keycode.F19
keybindings[3][4] = macropad.Keycode.F20
keybindings[3][5] = macropad.Keycode.F21
keybindings[3][6] = macropad.Keycode.F16
keybindings[3][7] = macropad.Keycode.F17
keybindings[3][8] = macropad.Keycode.F18
keybindings[3][9] = macropad.Keycode.F13
keybindings[3][10] = macropad.Keycode.F14
keybindings[3][11] = macropad.Keycode.F15

#config rainbow colors
color_iterator = 0 # just an iterator
color_speed = 2 # controls the speed of the color changes
color_seperation = 13 #controls how far apart the colors are

macropad.pixels.brightness = 0.2

text_lines = macropad.display_text()

encoder_state = macropad.encoder
page = macropad.encoder

activity_time = time.monotonic()
is_asleep = False
while True:
    now = time.monotonic()

    #event handler for the encoder
    if encoder_state != macropad.encoder:
        encoder_state = macropad.encoder
        page = encoder_state % page_count
        text_lines[0].text = page_titles[page]
        text_lines[1].text = "Page: " + str(page)
        text_lines.show()
        activity_time = now
        is_asleep = False
        

    #event handler for keys
    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            macropad.keyboard.send(keybindings[page][key_event.key_number])
            text_lines[2].text = "Key: " + str(key_event.key_number)
            text_lines.show()
            activity_time = now
            is_asleep = False

    #rainbow effect
    color_iterator = (color_iterator + color_speed) % 255
    for i in range(12):
        macropad.pixels[i] = colorwheel((color_iterator + (12 - i) * color_seperation) % 255)

    if now - activity_time > 20 and not is_asleep:
        text_lines[0].text = ""
        text_lines[1].text = ""
        text_lines[2].text = ""
        text_lines[3].text = ""
        text_lines.show()
        is_asleep = True


