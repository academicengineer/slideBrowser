# Replace "127.0.0.1" with the IP of your NAO
leds = ALProxy("ALLeds","127.0.0.1",9559)
# Create a new group
names = [
"Face/Led/Red/Left/0Deg/Actuator/Value",
"Face/Led/Red/Left/90Deg/Actuator/Value",
"Face/Led/Red/Left/180Deg/Actuator/Value",
"Face/Led/Red/Left/270Deg/Actuator/Value"]
leds.createGroup("MyGroup",names)
# Switch the new group on
leds.on("MyGroup")