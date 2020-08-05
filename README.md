
Final GitHub Public Repository that contains (link):

https://github.com/HSS-Autonomous-Vehicles-Team-2/route-planning

Final Report: Document summarizing all the work:

https://docs.google.com/document/d/1yxM9Neq-PtiPqXNC8gv6_98rRcDZEB936f3ltZJC4T8/edit?usp=sharing

Slides:

https://docs.google.com/presentation/d/13Lg12XX58tdk59Jm75Jf46mrFwnmdhGPJ1F2EGJlz9Y/edit?usp=sharing

Live Demo video(2-3 minutes):

Code:
https://github.com/HSS-Autonomous-Vehicles-Team-2/route-planning

Data

https://cocodataset.org/#home

https://github.com/HSS-Autonomous-Vehicles-Team-2/Route_planning_example



Summer RV | Autonomous Route Planning (Collision avoidance and object folliwng in complex situation)
2020 DGMDS17 Robotics, Autonomous Vehicles, Drones, and Artificial Intelligence 

1. Proposed Topic Summary
Assignment: Final Project Proposal

Course: Robotics, Autonomous Vehicles, Drones, and Artificial Intelligence: DGMD S-17 (34560)

Course Instructor: Professor Jose Luis Ramirez Herran

Term: Summer 2020

Team Name: Summer RV

Team Members: Fei Du, Lucy Chen Zhang, Luke Liang, Sourabh S. Bunnan, Bobby Wang, Youtai Cui

Last edited: Aug. 4th, 2020 by Lucy


Goal:
Apply the object detection model to detect target/destination object, plan a path to navigate to it from starting point. On the trip, the robot car may encounter obstacles. Apply the object detection model to find a bounding box, type and distance of an obstacle object in an image, decide whether and how to avoid it. Specifically, plan a local path to avoid an obstacle based on the object detection result, execute the plan by converting the path to motor instructions. After obstacle avoidance, continue to go towards the target object until reaching a very close location.
Start building the model by absorb all data in the set:
https://github.com/tensorflow/models/blob/master/research/object_detection/data/mscoco_complete_label_map.pbtxt


Action:

Detect target object and move toward it
This is very similar to “object following” https://www.waveshare.com/wiki/JetBot_AI_Kit
We just need to make some changes to the tutorial so that it can be use for our case

Distance estimation: it has 2 usages:
Decide how far the car is from obstacle, this is an input to local steering
decide whether we reach to target or not (distance to target < threshold)

Local route planning (local steering)
Based on object bounding box (size and location on the image), type and estimated distance, design local path to avoid it
Convert path to motor instruction (how to operate left, right wheel)
After local steering, re-lock target object and move toward it
A termination module that decides whether the target object is reached or not
	    -  if target is reached, stop the car
 

PROJECT OBJECTIVE: 
The objective of this sub-team is to utilize the data for detected objects to navigate towards the target object meanwhile respecting the pre-set protocols for each object class. This would initially consist of a local navigation system, which reacts to the objects directly obstructing the straight path to the target object. Time permitting a global navigation system can be implemented where the robot uses landmark objects to achieve an understanding of its position on the field. By then it would also take into account the dynamic objects randomly placed to plot out a shortest course to the target. The data we utilize will be initially provided by an existing model from a repository to start implementation without sub-team A’s completed deliverable. Once sub-team A’s progress is advanced enough, we will integrate their data into our system.

SOFTWARE & DEVELOPING TOOLS REQUIRED:
GitHub repository
https://github.com/HSS-Autonomous-Vehicles-Team-2
Slack https://s-17jetbot.slack.com/join/shared_invite/zt-fkpc4ej6-oHmdG5MeMbTmYSx735Zerw#/
Zoom
Google Docs
Trello

HARDWARE REQUIRED:
Laptop Computer
Nvidia Jetson Nano Developer kit
Jetson Nano compatible vehicle (i.e. Waveshare’s Jetbot)
Extraneous Computer Hardware:
Mouse
Keyboard
HDMI cable
Monitor

MEETING TIMES:
Meeting: Saturdays, 3:00 PM - 5:00 PM PST, every Tuesday and Thursday after class around 20 min sync. 


MILESTONES (Adjust as Needed):
Week 3 (July 6 - July 12): 
Complete Vehicle Assembly
Become Familiarized with Nvidia Jetson Nano Development Kit and Robots
General Research on How to Achieve Project Objectives
Become Familiarized with Object Detection Process
Become Familiarized with Route Planning Process

Week 4 (July 13 - July 19): 
Prepare Route Planning Programming 
Test Existing Detection Model to Understand It’s Capabilities and Give Standards to Team A
Integrate Route Planning

Week 5 (July 20 - July 26): 
Set Up Vehicle Route(s)
Implement Team A Data
Testing & Troubleshooting

Week 6 (July 27 - August 2): 
Further Testing & Troubleshooting
Finalize Project Report
Prepare & Finalize Project Presentation
NOTES (To be Later Organized into Detailed Progress Report):
Subteam Suggestion: Project Component Idea: Use camera and sensor data to detect, identify track and classify an object on the road. It should classify whether an object is a hazard, person/animal or other category. Then enact whether the car should stop, slow down or pull off the road for safety.
