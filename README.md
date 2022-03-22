# Cisco Live! DevNet Workshop 2225 (DEVWKS-2225)

Welcome to Cisco Live! In this DevNet workshop we will be covering how to automate the collection of inventory information utilizing Cisco Network Services Orchestator and Python3. While NSO is a key component in this lab many of these task can also be performed utilizing other Cisco technologies such as DNA Center. The main goals of this lab are to demonstrate how to:

- make REST calls to controllers (NSO in this case).
- parse and utilize the data you receive.
- read API documentation (the NSO RESTConf API in this case).
- turn your data into a useful product.

## Notes:

If you are taking this lab at CLUS 2022 you should be provided a workstation. This workstation has been configured with the correct Python packages, tools, and an IDE (vsCode) to perform the lab. If you are performing this lab on your own equipment please refer to the **SETUP.md** file. 

Throughout the lab guide there will be images of Linux terminals. In some instances your machine name, or user name may not match what is in the image. As long as you are in the correct directory this should cause you no issues. 

## Lab Environment:

The lab you will be interacting with today consists of the workstation, an NSO instance, and various Cisco devices. These Cisco devices are virtualized and running on Cisco Modeling Labs (CML). The Cisco devices include platforms running IOS-XE, IOS-XR, ASA, NX-OS. We will discover more about these devices during the lab. 

# Lab Guide

## Obtaining the code:

You should currently be viewing this README.md file at: https://github.com/snakesonaguy/CL_DEVWKS-2225. We will be utilizing Git to clone this repository onto our workstations. Right-click anywhere on your desktop and select 'Open in terminal'. This should open a terminal window in the Desktop directory:

![text!](/images/open_term.png)

In the terminal box enter the command: 

`git clone https://github.com/snakesonaguy/CL_DEVWKS-2225`

You should now have **CL_DEVWKS-2225** directory on your desktop. 

---

## Opening the code in your Integrated Development Environment:

You can now move into the lab directory. From the open terminal type:

`cd CL_DEVWKS-2225`

You can see the contents of the directory by issuing the `ls` command. 

![text!](/images/ls.png)

Note: there are some additional hidden files that we cannot see with `ls`. 

Now that you are in the lab directory we can open our IDE (vscode). To do this issue the command (from the open terminal):

`code .`

Note: `code` is the command to open vscode and `.` is a refrence to the present working directory. 

vscode should open on your desktop and you should see a screen similar to this:

![text!](/images/open_code.png)

Taking a look at the contents of the directory in the left plane we can see that we have several items:

- images (a directory containing the images for the README.md)
- .env-sample (a sample file we will use to configure variables)
- .gitignore (tells git which files not to track)
- main.py (where our main and helper functions/code reside)
- README.md (the markdown version of **THIS** file)
- requirements.txt (a list of the additional Python packages used in this program)
- SETUP.md (supplemental instructions on running this lab from a personal workstation)

The only files that we will need to access during this lab are **.env-sample** and **main.py**.