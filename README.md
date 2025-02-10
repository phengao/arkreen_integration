# Arkreen_integration
hello, Arkreen ha
# How to use:
## 1. Preconditions
###  1.1 The latest version of home assistant core has been installed on the Linux system, link: https://github.com/home-assistant/core
Install and run home assistant core reference link: https://developers.home-assistant.io/docs/development_environment
### 1.2 Relevant energy devices have been added to the home assistant application, such as photovoltaic equipment, inverters, energy meters, etc
### 1.3 You have completed the application for Arkreen plant CSP power station and received confirmation information, obtaining the registration code for Arkreen plant CSP power station


## 2. Install Arkreen_integration
### 2.1 Download Arkreen_integration installation package
In https://github.com/Arkreen_integration/releases Download the latest Source code compressed file
### 2.2 Extract the downloaded Arkreen_inintegration-x.x.x.zip file to the directory where the home assistant core/folder is located
After completing the decompression, a new folder will be obtained: Arkreen_integration-x.x.x，   The new directory structure is as follows:
```
|--<your home-assistant folder>
   |--core
   |--...
   |--Arkreen_integration-x.x.x
   |--Arkreen_integration-x.x.x.zip
   |--...
```
### 2.3 Close the home assistant application
     
### 2.4 Enter the Arkreen_integration-x.x.x directory and execute the following command
python3 install.py

Follow the instructions to complete the confirmation operation
  
### 2.5 Restarting Home Assistant Application
After logging into your home assistant account in the browser, you can see the newly added "Arkreen Plant" tag in the left border bar of the homepage.
  
### 2.6 Complete activation of Arkreen plant CSP power station
Click on the "Arkreen Plant" tab in the left border bar of the home illness homepage in the browser to enter the Arkreen Plant management page, which will display the information about the Arkreen plants you own.

If you have not activated the Arkreen plant CSP power plant you applied for, you can click the "Active Plant" button on the Arkreen plant management page to enter the power plant activation page and complete the power plant activation
  
### 2.7 Activate the power station
To enter the power station activation page, you need to fill in the power station information to complete the power station activation. The instructions for filling in the information are as follows:

Select Device:  Select the name of the power generation equipment for your activated power station in the home assistant, such as photovoltaic equipment, inverters, energy meters, etc., for example: OWON WSP402-zha:3c:6a:2c:ff:fe:d0:f5:43'

Select Energy Sensor:  Choose a sensor that provides energy data for power generation equipment in home assistant, such as: sensor.owon_wsp402_summation_delivered',

Select Power Sensor:  Select sensors for power generation equipment to provide power data in home assistant, such as: sensor.owon_wsp402_instantaneous_demand',

Active Code:  Fill in the activation code in your response to the power station application, for example: sUtFhnmtMv8c

Owner Address:  Fill in the Owner information you provided when applying for the power station, for example: 0x123456789
  
Click the Activate Plant button, and if activated successfully, the bottom left corner of the page will display "Active successful"

After activation is completed, Arkreen_integration will regularly report the activated power station data to the Arkreen power station service.
  

