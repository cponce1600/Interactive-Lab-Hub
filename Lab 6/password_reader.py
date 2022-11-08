import paho.mqtt.client as mqtt
import uuid

# the # wildcard means we subscribe to all subtopics of IDD
topic = 'IDD/pass'
last_messages = []
password = ['1','2','3']

# some other examples
# topic = 'IDD/a/fun/topic'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	# you can filter by topics
    if msg.topic == 'IDD/some/other/topic':
        last_messages.append(msg.payload.decode('UTF-8'))

    verified = False
    if len(last_messages)>2:
        if (last_messages[-3] == password[0] and last_messages[-1] == password[1] and last_messages[-1] == password[2]):
            verified = True
    if(verified):
        # NOTED: Here we attempted to include text to speech.  
        # Trevor's pi would not recognize the board or microphone and had numerous issues 
        # Thus we ended up going with just printing the statement and wizarded the voice setup
        print("Go get the verified user at the door")



# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
client.loop_forever()