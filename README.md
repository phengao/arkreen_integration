# Arkreen_integration
Arkreen_integration,  It is a user-defined home assistant integration used to manage Arkreen plants
# How to use:
## 1. Preconditions
### 1.1 Installing Home Assistant Core
The latest version of home assistant core has been installed on the Linux system, link: https://github.com/home-assistant/core

Install and run home assistant core reference link: https://developers.home-assistant.io/docs/development_environment
### 1.2 Adding power generation equipment
Related energy devices have been added to the home assistant application, such as photovoltaic equipment, inverters, energy meters, etc
### 1.3 Application for power station
You have completed the application for mytest plant CSP power station and received confirmation information, obtaining the registration code for mytest plant CSP power station


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


# Arkreen_integration
Arkreen_integration, 是一个用户自定义 home-assistant 集成，用于管理 Arkreen plant
# 如何使用：
## 1. 前提条件
### 1.1 安装 home assistant core 
  在linux系统中已安装最新版本的home-assistant core，链接： https://github.com/home-assistant/core
  安装和运行 home-assistant core 参考链接：https://developers.home-assistant.io/docs/development_environment
### 1.2 发电设备
   在 home-assistant 应用中已经添加了相关能源设备，例如：光伏设备、逆变器、电能表等等
### 1.3 申请电站
   你已经完成  Arkreen plant CSP 电站 申请，并收到确认信息，得到 Arkreen plant CSP 电站的Plant id


## 2. 安装 Arkreen_integration 
### 2.1 下载 Arkreen_integration 安装包
  在 https://github.com/arkreen/integrationHA/releases 下载最新 Source code压缩包
### 2.2 将下载的 integrationHA-x.x.x.zip 解压缩到 home-assistant 的 core/ 文件夹所在的目录下
  完成解压缩后，会得到新文件夹: integrationHA-x.x.x，  新目录结构如下：
```
  |--<your home-assistant folder>
     |--core
     |--...
     |--integrationHA-x.x.x
     |--integrationHA-x.x.x.zip
     |--...
```
### 2.3 关闭  home-assistant 应用  
     
### 2.4 进入 integrationHA-x.x.x 目录，执行以下指令
```
  python3 install.py
```
  按照操作提示完成操作
  
### 2.5 重新启动 home-assistant 应用
  在浏览器登录你的home-assistant账户后，在首页的左侧边框栏中，你可以看到新增的 "Arkreen Integration" 标签。
  
### 2.6 完成 Arkreen plant CSP 电站激活
  在浏览器中 home-assistant 首页左侧边框栏点击 "Arkreen Integration" 标签，进入 Arkreen Integration 管理页面，页面将显示当前你所拥有的 Arkreen plant 信息。
  如果你还没有添加你申请的 Arkreen plant CSP 电站，你可以点击 "Add Plant" 按钮进入添加电站页面添加电站。
  
### 2.7 添加 arkreen plant
  点击 "Add Plant" 按钮进入添加电站页面，填写电站信息，完成电站添加，填写信息说明如下：
  Select Device: 选择 home-assistant 中你要添加为电站的发电设备名称，例如：光伏设备、逆变器、电能表等等，例如：'OWON WSP402-zha:3c:6a:2c:ff:fe:d0:f5:43'
  Select Energy Sensor: 选择发电设备在 home-assistant 中提供 Energy 数据的传感器，例如：'sensor.owon_wsp402_summation_delivered',
  Select Power Sensor: 选择发电设备在 home-assistant 中提供 Power 数据的传感器，例如：'sensor.owon_wsp402_instantaneous_demand',
  Plant ID: 填写你申请电站回复中的 激活码，例如：sUtFhnmtMv8c
  Owner Address: 填写你申请电站时填写的 Owner信息， 例如： 0x123456789
  
  点击 Activate Plant 按钮，如果激活成功，页面的左下侧会显示 "Active successful"
  完成激活后，Arkreen_integration会定期向 Arkreen电站服务上报激活电站数据。
  

  

