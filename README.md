# raspberry PI stream images and pose estimation 

This project is very WIP.

Written then 03-02-2022
This project is designed to create a setup for streaming images from a raspberry pi with the camera to a more robust system to do different processing.

I am adding my processing function related to AR or Pose-estimation.

Planned processing is:
Fiducial marker detection, pose-estimation, and image projection.

When complete, the pi will be a headless worker, and the controller will be designed to be deployed on a host computer.

The first iteration will only be python for my development, but a C++ version is planned.

Hardware is:
Raspberry PI 3b as a worker - Running Raspberry PI os (Buster)
HQ rapsberryPI camrea - IMX477R
Lense is a 6mm Videangle

TODO:
Add arguments for adding IP's to make is simpler
Projection of points for testing the accuracy of 
Worker, coordinator communications.
Error handling.
Optimize code for more frames per second.
GUI development

Longterm TODO:
Add segmentation network for different object detection
Complete headless Linux deployment for raspberry PI without PI os.
