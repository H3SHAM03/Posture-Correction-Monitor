# Posture-Correction-Monitor
## Overview
The Posture Corrector project aims to develop a wearable device that helps individuals improve their posture and reduce the risk of musculoskeletal issues caused by poor posture habits.  The device provides real-time feedback and guidance to the user. 

## Hardware Components
The following hardware components were used in the project: 
• Arduino uno microcontroller: It serves as the brain of the system, responsible for data acquisition, processing, and control. 

• Force-sensing resistor (FSR) is a type of sensor that changes its resistance when pressure or force is applied to its surface. 

• Flex sensor is a type of bend sensor that changes its resistance as it is flexed or bent. 

• 10k resistor. 

• Breadboard: It provides a platform for connecting and prototyping the various components of the system. 

• Jumper wires: They are used to establish connections between the Arduino, ultrasonic sensor, and breadboard. 

• Buzzer: Connect one terminal of the buzzer to a digital output pin of the microcontroller, connect the other terminal of the buzzer to the ground. 

## Mechanism of Action
• The Flex and FSR sensors are mounted at a suitable position on the patient’s body. 

• The Arduino is connected to the sensors and programmed to read the pressure and degree of bending. 

• It works by assessing the user's posture through real-time feedback, providing reminders to check and adjust posture. 

• When the user bends his back more than the acceptable range, the flex sensor detects the bending degree, and the buzzer alarms the user to correct his posture. 

• The program uses the FSR sensor to know the whole time the user wore the belt.   
Integrate the buzzer control logic into the overall system design of the medical storage monitoring System. 

• Connect the trigger conditions for the buzzer to relevant sensor data or system events. 

• Ensure the buzzer's alerts and notifications align with the intended purpose and functionality of the project. 

## Prototype
![image](https://github.com/H3SHAM03/Posture-Correction-Monitor/assets/115306247/855793dd-8b1c-419e-b97c-01d2f57e974d)
![image](https://github.com/H3SHAM03/Posture-Correction-Monitor/assets/115306247/8de058fe-6bc2-4bd1-bc0a-d2090c65fd71)
![image](https://github.com/H3SHAM03/Posture-Correction-Monitor/assets/115306247/815f3863-4c8c-497d-bf12-18f0dd156e26)

## Example UI Images
![Screenshot 2024-03-06 202345](https://github.com/H3SHAM03/Posture-Correction-Monitor/assets/115306247/96d163ca-a838-41f7-9ca4-f87477134d38)
![Screenshot 2024-03-06 202247](https://github.com/H3SHAM03/Posture-Correction-Monitor/assets/115306247/686d738f-17bf-465d-a03c-3a9c4d7bec56)
![Screenshot 2024-03-06 202420](https://github.com/H3SHAM03/Posture-Correction-Monitor/assets/115306247/fae8bea1-ea93-4b81-aeb2-83ec2e071d2d)
