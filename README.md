# Cisco Live! DevNet Workshop 2225 (DEVWKS-2225)

Welcome to Cisco Live! In this DevNet workshop we will be covering how to automate the collection of inventory information utilizing Cisco Network Services Orchestator and Python3. While NSO is a key component in this lab many of these task can also be performed utilizing other Cisco technologies such as DNA Center. The main goals of this lab are to demonstrate how to:

- make REST calls to controllers (NSO in this case).
- parse and utilize the data you receive.
- read API documentation (the NSO RESTConf API in this case).
- turn your data into a useful product.

## Notes:

If you are taking this lab at CLUS 2022 you should be provided a workstation. This workstation has been configured with the correct Python packages, tools, and an IDE (vsCode) to perform the lab. If you are performing this lab on your own equipment please refer to the **SETUP.md** file. 

Throught the lab guide there will be images of Linux terminals. In some instances your machine name, or user name may not match what is in the image. As long as you are in the correct directory this should cause you no issues. 

## Lab Environment:

The lab you will be interacting with today consists of the workstation, an NSO instance, and various Cisco devices. These Cisco devices are virtualized and running on Cisco Modeling Labs (CML). The Cisco devices include platforms running IOS-XE, IOS-XR, ASA, NX-OS. We will discover more about these devices during the lab. 

# Lab Guide

## Obtaining the code:

You should currently be viewing this README.md file at: https://github.com/snakesonaguy/CL_DEVWKS-2225. We will be utilizing Git to clone this repository onto our workstations. Right-click anywhere on your desktop and select 'Open in terminal'. This should open a terminal window in the Desktop directory:

![text!](/images/open_term.png)