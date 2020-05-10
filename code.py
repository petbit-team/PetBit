# importing needed libraries
from adafruit_circuitplayground import cp
import board
import time
import pulseio
import array

# create IR input, maximum of 100 bits.
pulseIn = pulseio.PulseIn(board.IR_RX, maxlen=100, idle_state=True)

# clears any artifacts
pulseIn.clear()

# resume IR pulse detection
pulseIn.resume()

# creates IR output pulse
pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseOut = pulseio.PulseOut(pwm)

# created functions to organize our code, and make it more clear
def is_light_low():
    if cp.light < 6:
        return True

def update_low_light_values(values):
    for i in range (0, 10):
        values[i] = (1, 1, 1)

def play_sound():
    cp.play_tone(1000, 5.0)

def laskoFanInfrared():
    pulseIn.pause()  # pauses IR detection
    cp.red_led = True
    pulseOut.send(pulseArrayFan)  # sends IR pulse
    cp.play_tone(750, 0.3)
    time.sleep(0.2)  # wait so pulses don't run together
    pulseIn.clear()  # clear detected pulses
    cp.red_led = False
    pulseIn.resume()  # resumes IR detection

# create variables for the defaulted product
steps = 0
dailytarget = 10000
dayssinceepoch = int(time.time()/86400)  # this shows the time since 1970
display = True
light = True
fanOn = False
maxTemp = 80
feature = True

# array for pulse, this is the same pulse output when button a is pressed
# inputs are compared against this same array
# array.array('H', [x]) must be used for IR pulse arrays when using pulseio
pulseArrayFan = array.array('H', [1296, 377, 1289, 384, 464, 1219, 1296, 379,
    1287, 394, 464, 1226, 461, 1229, 458, 1233, 464, 1226, 462, 1229, 456, 1232,
    1293, 6922, 1294, 379, 1287, 385, 463, 1220, 1295, 379, 1287, 395, 464,
    1225, 461, 1229, 458, 1232, 465, 1225, 462, 1229, 457, 1231, 1294, 6904, 1291,
    382, 1295, 377, 461, 1221, 1294, 380, 1296, 385, 464, 1226, 460, 1230, 457,
    1233, 464, 1234, 453, 1229, 457, 1230, 1295, 6918, 1287, 386, 1291, 381, 457,
    1225, 1289, 385, 1292, 388, 460, 1230, 457, 1232, 465, 1225, 462, 1228, 458,
    1232, 465, 1222, 1293, 6905, 1290, 382, 1295, 377, 461, 1221, 1293, 387, 1290,
    384, 464, 1225, 461, 1229, 458, 1231, 466, 1224, 463, 1226, 460, 1228, 1286, 6920,
    1296, 377, 1289, 382, 466, 1216, 1288, 386, 1291, 390, 458, 1231, 456, 1233, 464,
    1226, 460, 1229, 458, 1232, 465, 1222, 1292, 6904, 1291, 382, 1295, 376, 462, 1220,
    1295, 379, 1286, 395, 464, 1225, 462, 1232, 454, 1232, 466, 1223, 463, 1227, 460,
    1228, 1286, 6925, 1291, 381, 1296, 376, 462, 1224, 1290, 380, 1286, 394, 465, 1225,
    462, 1227, 460, 1230, 456, 1234, 463, 1227, 460, 1227, 1287, 6964, 1294, 379, 1287,
    384, 464, 1219, 1296, 378, 1288, 392, 456, 1234, 463, 1227, 460, 1230, 457, 1232, 464,
    1226, 461, 1227, 1288])

# this sets the temperature to fahrenheit
temp_f = int(cp.temperature * (9 / 5) + 32)
print("Current temperature:", temp_f)
print("Max temperature:", maxTemp)

while True:
    values = [(0,0,0)]*10  # this makes sure that the neopixels don’t flash

    # if button b is pressed, the infrared temperature feature turns on/off
    if cp.button_b:
        print("Button B Pressed!")
        if feature:
            feature = False
        else:
            feature = True

    # if the owner has enabled the feature, this sets the maximum temperature the owner wants for their pet
    if feature == True:
        if cp.touch_A4:
            maxTemp = 70
            print("The max temp has been changed to", maxTemp, "degrees") # all print statements are a prototype of an app sending a text to owners
        if cp.touch_A5:
            maxTemp = 80
            print("The max temp has been changed to", maxTemp, "degrees")
        if cp.touch_A6:
            maxTemp = 90
            print("The max temp has been changed to", maxTemp, "degrees")

        # this sets the temperature to fahrenheit
        temp_f = int(cp.temperature * (9 / 5) + 32)

        # if the temperature is too high and the owner wants the feature enabled, the infrared temperature feature will run
        if temp_f >= maxTemp and not fanOn:
            print("It's", temp_f, ". Too hot! The max temp is ", maxTemp, ". Turning fan on now.")  # all print statements are a prototype of an app sending a text to owners
            laskoFanInfrared()
            fanOn = True

        # if the temperature exceeds the maximum temperature the owner sets, the red led will flash
        if fanOn:
            cp.red_led = True
            time.sleep(1)
            cp.red_led = False
        else:
            cp.red_led = False

        # turns fan off under these circumstances
        if temp_f < maxTemp-1 and fanOn:
            print("Not too hot! The temp is" , temp_f)
            laskoFanInfrared()
            fanOn = False
        if cp.button_b:
            print("Turning off.")
            if fanOn:
                laskoFanInfrared()
                fanOn = False
            feature = False

        # checks temperature every 0.5 seconds
        time.sleep(0.5)

        if cp.switch == True:  # if switch is true display is false
            display = False
        else:  # if the switch is false display is true
            display = True

    # this sets the daily target the owner wants for their pet
    if cp.touch_A1:
        dailytarget = 10000
        print("The daily target has been changed to", dailytarget, "steps")
    if cp.touch_A2:
        dailytarget = 20000
        print("The daily target has been changed to", dailytarget, "steps")
    if cp.touch_A3:
        dailytarget = 30000
        print("The daily target has been changed to", dailytarget, "steps")

    # if a step is detected, the steps variable will increase by 1
    if cp.shake(10):
        steps = steps + 1

    # the red neopixel is the percentage of steps done
    if steps < dailytarget:
        for i in range (0, steps*10/dailytarget):
            values[i] = (30, 0, 0)
            
  # the blue neopixel shows each step taken
    stepprogressled = steps % 10
    values[stepprogressled] = (0, 0, 30)           

    # calling out the functions for the low light feature
    if is_light_low() and light == True:
        update_low_light_values(values)

    # if button a is pressed, the low light feature turns on/off
    if cp.button_a:
        print ("Button A Pressed!")
        if light == True:
            light = False
        else:
            light = True

    # if display is false the neopixels are off, but still continues to count the steps
    if display == False:
        values = [(0,0,0)]*10

    # measures the days since 1970 again
    currentdayssinceepoch = int(time.time()/86400)

    # have the step count reset everyday
    if currentdayssinceepoch > dayssinceepoch:
        steps = 0
        dayssinceepoch = currentdayssinceepoch

    # if the pet reaches the daily target, a sound will play
    if steps == dailytarget:
        play_sound()  # calling out our function for sound

    # neopixels will turn green to show the daily target has been reached to alert the owner if they didn’t hear the sound, but the steps will still be counted
    if steps >= dailytarget:
        for i in range (0, 10):
            values[i] = (0, 15, 0)
        stepprogressled = steps % 10
        values[stepprogressled] = (0, 70, 0)

    # print(temp_f, maxTemp)
    # print(steps, dailytarget)

    # lights up the neopixels as per data in values
    for i in range (0, 10):
        cp.pixels[i] = values[i]
