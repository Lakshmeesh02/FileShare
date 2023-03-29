# FileShare
File sharing using socket programming in python

To run on the same system:
1) Uncomment the "post" section on the program in both the server and the client.
2) Save the server.py file in a different folder
3) The folder which contains client.py file must have a file to send to the server
4) Run both the scripts and follow the instructions
5) The folder with server.py will have a copy of the sent file... Voila!

To run on different devices:
1) Specify the device's IP address in both the client and the server (host variable)
2) Only the "get" command works between devices, meaning the client can only receive files from the server and not the other way around
3) If you are reading this, please try to implement a both way file tranfer between 2 devices. Help is very much appreciated :) 

NOTE: The file can be an image, a pdf, a word doc or a video too!
