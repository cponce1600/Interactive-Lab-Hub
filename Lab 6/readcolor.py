import paho.mqtt.client as mqtt
import uuid
import digitalio
import board
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi

display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)


topic = 'IDD/colors'

def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)

screenColor = None
def on_message(cleint, userdata, msg):
    screenColor = msg.payload.decode('UTF-8')
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")


client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

while not screenColor:
    try:
        screenColor = color565(*list(webcolors.name_to_rgb(input('Type the name of a color and hit enter: '))))
    except ValueError:
        print("whoops I don't know that one")

display.fill(screenColor)
 
#client.loop_forever()