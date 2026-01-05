import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB
from kmk.extensions.media_keys import MediaKeys

# --- 1. KEYBOARD SETUP ---
keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

# --- 2. PIN DEFINITIONS (Check these against your final soldering!) ---
# Based on your schematic:
# Switches are on A0, A1, A2, A3
SWITCH_PINS = [board.A0, board.A1, board.A2, board.A3]

# Encoders (Verify which pin is A/B for your specific wiring)
# Left Encoder: Pins D6 (TX) and D7 (RX)
# Right Encoder: Pins D8 (SCK) and D9 (MISO)
ENCODER_PINS = [
    (board.D6, board.D7), 
    (board.D8, board.D9)
]

# LED Pin (MOSI/D10)
LED_PIN = board.D10

# OLED I2C Pins (D4/SDA, D5/SCL)
OLED_SDA = board.D4
OLED_SCL = board.D5

# --- 3. SWITCH CONFIGURATION ---
# Using KeysScanner for direct pin mapping (no matrix)
keyboard.matrix = KeysScanner(
    pins=SWITCH_PINS,
    value_when_pressed=False,
    pull=True,
    interval=0.02,
)

# --- 4. ENCODER CONFIGURATION ---
encoder_handler = EncoderHandler()
encoder_handler.pins = ENCODER_PINS
keyboard.modules.append(encoder_handler)

# --- 5. RGB LED CONFIGURATION ---
rgb = RGB(
    pixel_pin=LED_PIN,
    num_pixels=2,
    val_limit=100,  # Max brightness
    hue_default=10,
    sat_default=255,
    val_default=100,
    animation_speed=1,
    breathe_center=1.5,
    knight_effect_length=2,
)
keyboard.extensions.append(rgb)

# --- 6. OLED CONFIGURATION ---
# We set up the display manually to show text
displayio.release_displays()
i2c = busio.I2C(OLED_SCL, OLED_SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group()
display.root_group = splash

# Draw a background rectangle (optional)
color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000 # Black
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw Text
text_area = label.Label(terminalio.FONT, text="DHIR MACROPAD", color=0xFFFFFF, x=28, y=15)
splash.append(text_area)

# --- 7. KEYMAP ---
# Define what the keys do
# Switches: 4 keys
# Encoders: 2 encoders (CW, CCW) -> 4 actions map

keyboard.keymap = [
    [
        # Switch 1, 2, 3, 4
        KC.A, KC.B, KC.C, KC.D,
        
        # Encoder 1 (Left) - Rot Left, Rot Right
        KC.VOLU, KC.VOLD,
        
        # Encoder 2 (Right) - Rot Left, Rot Right
        KC.PGUP, KC.PGDN
    ]
]

if __name__ == '__main__':
    keyboard.go()