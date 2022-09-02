# scatbot-edge-ai-shootout

A place to chronical performance of various hardware and software solutions for using computer vision and AI at the edge for object detection.

# Why?

I build bots to train and entertain my canine housemate.  Robotics automation routines like tracking and following your pet around the house require that we be able detect when a dog or cat is in the field of view (FOV) and, even more important, where in the FOV - how many degrees off center the detected object is.   

# Why would you do it at the edge?

It's true that for most applications around the house you could probably just set up a base computer that was much more powerful.  All the computer hardware on the bot would do is send sensor data and video back and recieve motor commands in.   

**But that's not cool!** you yell? I'm with you. I want it to be fully autonomous. Even though it's not really an issue if you have a good mesh, you don't want to send the bot accidentally careening down the stairs when the connection to the controller drops.  This does not mean you're limited to just one single board computer (SBC). For some applications, like bots that fit under furniture, you'll have a difficult time fitting that on to an already crowded chassis that is about as big as your 3D printer will allow you to print. 

This means, at a minimum, that we need to have available some percentage of cpu for behavior logic, video streaming / recording and reading other sensors.  Using the Intel Realvision D435i depth camera and librealvision in Python can take up to 35% of the Raspberry PI 4 overall CPU.   

# Testing ethos and methods  

1. I want relevant benchmarks.  For the application, it does me little good to know how fast I can read and do object detection on a video file.  I most want to know how fast it can process an images from an onboard camera.  All of the benchmarks are based off reading the camera image using openCV. You can also run the benchmark to see how fast openCV is able to read from the camera without object detection.  

1. I want real world benchmarks.  In the real world we have to run other code and the object detection on the same SBC.  I want to know both, how the object detection works without anything else running, and how it performs when only 50% of the SBC CPU is available for object detection.  If space and battery constraints allow, I want to know how much better it would perform if object detection had its own dedicated SBC.   
 
