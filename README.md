# Facial-recognition-box


Only runs in Linux

This project is basically a box that opens / closes itself based on whether the person looking at the webcam is recognized as an admin or not. 

The main.py file does the facial recognition part. It uses the facial recognition Machine Learning library from Pypi, as well as the pyserial module in order to communicate with the Arduino. The arduino_code.ino is the code sent to the Arduino itself. The Arduino, based on the output of the main.py file (output generated for one out of two frames), activates a servo motor that acts as a lock, and can be set to either closed or opened positions. It also displays the state (locked or unlocked) of the box on an LCD screen attached to the box. Besides, the video feed is displayed in real time on the computer screen, giving information about the person identified.

