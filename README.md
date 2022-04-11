# Cisco Live! DevNet Workshop 1671 (DEVWKS-1671)

## Scenario

Welcome to Cisco Live! In this DevNet workshop we will be covering how to automate the collection of inventory information utilizing Cisco Network Services Orchestator and Python3. While NSO is a key component in this lab many of these task can also be performed utilizing other Cisco technologies such as DNA Center. The main goals of this lab are to demonstrate how to:

- make REST calls to controllers (NSO in this case).
- parse and utilize the data you receive.
- read API documentation (the NSO RESTConf API in this case).
- turn your data into a useful product.

### Notes:

If you are taking this lab at CLUS 2022 you should be provided a workstation. This workstation has been configured with the correct Python packages, tools, and an IDE (vsCode) to perform the lab. If you are performing this lab on your own equipment please refer to the **SETUP.md** file. 

In this lab we try not to make any assumptions about your level of experience with any of the various components (Linux, vscode, Python, etc). For this reason the instructions are detailed. 

Throughout the lab guide there will be images of Linux terminals. In some instances your machine name, or user name may not match what is in the image. As long as you are in the correct directory this should cause you no issues. 

## Network Diagram/Lab Environment:

The lab you will be interacting with today consists of the workstation, an NSO instance, and various Cisco devices. These Cisco devices are virtualized and running on Cisco Modeling Labs (CML). The Cisco devices include platforms running IOS-XE, IOS-XR, ASA, NX-OS. We will discover more about these devices during the lab. 

# Lab Guide

## TASK 1: Obtaining the code:

### STEP 1: Open Terminal

We will be utilizing Git to clone the project repository onto our workstations. Right-click anywhere on your desktop and select 'Open in terminal'. This should open a terminal window in the Desktop directory:

![text!](/images/open_term.png)

### STEP 2: Clone repository

In the terminal box enter the command: 

`git clone https://github.com/snakesonaguy/CL_DEVWKS-1671`

You should now have **CL_DEVWKS-1671** directory on your desktop. 

---

## TASK 2: Opening the code in your Integrated Development Environment:

### STEP 1: Move to project directory

You can now move into the lab directory. From the open terminal type:

`cd CL_DEVWKS-1671`

### STEP 2: View project directory contents

You can see the contents of the directory by issuing the `ls` command. 

![text!](/images/ls.png)

Note: there are some additional hidden files that we cannot see with `ls`.

### STEP 3: Launch vscode

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

---

## TASK 3: Creating/Editing Environmental Variables

### STEP 1 Create and Edit .env file: 

We are going to start off creating a new file within the CL_DEVWKS-225 directory. You can do this from vscode by selecting the **New File** button from the left plane. 

![text!](images/new_file.png)

When prompted to name the file enter **.env**. Once you have done this the blank files should open in the editing plane. You will need to open the **.env-sample** file and copy its contents to the newly created **.env** file. The contents of your **.env** file should now look like this:

```
    # This is a sample of the .env file needed by python-dotenv package. 
    # You should add the information for your NSO instance in the quotes below.
    # You will need to rename this file to '.env' for python-dotenv to find it.
     Note that the NSO_HOST variable should be formatted as 'https://url_of_nso.com'

    NSO_HOST=""
    NSO_USERNAME=""
    NSO_PASSWORD=""
```

Your facilitator will provide with you data to populate these variables. We will explore more about what this file does in the next section. 

---

## TASK 4: Exploring **main.py**

From the left plane select open the **main.py** file. Lets take a look at some of the components of the program.

### STEP 1: Import Statements

At the top of **main.py** you will notice several `import` statements. 

```
    # Imported packages
    import requests
    import urllib3
    import json
    import pandas as pd
    from dotenv import load_dotenv, find_dotenv
    import os
```

Each of these statements is giving our program access to code that resides in other Python libraries. This is a very small collection of libraries that will allow our program to operate. We didn't have to implement any of this functionality and can simply utilize the API available to interact with the code. Python has a very large collection of libraries to do all sorts of things. So what do our imported libraries do?:

- requests - allows you to send HTTP/HTTPS request in a simple elegant manner
- urllib3 - requests is built on-top of urllib3, we need to import it to suppress HTTPS warnings
- json - a json encoder and decoder
- pandas - a data analysis tool, we will use it to build data frames
- dotenv - allows you to access environmental variables outside of your code
- os - a portable way of using operating system functionality

### STEP 2: Code Specific Requirements

Next you will see a comment labeled `Code specific requirements`. There are two statements in this code block:

```
    # Code specific requirements
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv(find_dotenv())
```
Here is what those statements do:

- `urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)` - since we are using self-signed certificates on NSO the request library will complain about an insecure connection. This line disables that warning. 
- `load_dotenv(find_dotenv())` - consists of two function calls. The outer call `load_dotenv()` takes as an argument the location of a **.env** file (remember we made that earlier) and makes the variables in that file available to the program. Conveniently, `find_dotenv()` will locate the **.env** file by looking in the present working directory.  

### STEP 3: Global Varibles Accessed By python-dotenv()

The next block of code is labeled `Global variables accessed via python-dotenv`

```
    # Global variables accessed via python-dotenv
    NSO_HOST = os.getenv('NSO_HOST')
    USERNAME = os.getenv('NSO_USERNAME')
    PASSWORD = os.getenv('NSO_PASSWORD')
```

These statements make the variables that we configured in our **.env** file into variables in our program. So why go through the trouble of using python-dotenv to access these specific variables? Many times we may want to share our code with others, but we do not want to share our usernames, passwords, or other information. By using python-dotenv we can share our code without exposing our secure information. Additionally, we place our **.env** in our **.gitignore** so that when we push this code to a Git repository it is not uploaded. 

### STEP 4: Additional Global Variables

Next you will find an additional block of global variables. 

```
    # Additional global variables
    AUTH = (USERNAME, PASSWORD)
    VERIFY = False
    HEADERS = {'Content-type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
    DEVICES = []
    PLATFORM_DETAILS = {}
```
Here is what these variables are:

- AUTH - a Python tuple that consists of the USERNAME and PASSWORD variables
- VERIFY - a boolean set to `False`
- HEADERS - a Python dictionary that consists of 2 key value pairs
- DEVICES - an empty Python list 
- PLATFORM_DETAILS - an empty Python dictionary

When we explore the functions within the code we will see how these are used.

Note: You'll notice that we refer to these as 'global' variables. That means that these variables have global scope i.e. they can be accessed and modified (if they are of a mutable type) from anywhere within the code. A convention in many programming languages is to use UPPERCASE for global variables. This makes them easily recognizable. 

### STEP 5: The main() Function

Below the global variables you will find all of the function definitions for our program. If you scroll to the very bottom you will find a function definition called `main()` and an `if` statement:

```
    def main():
        pass
        # commented out function calls

    if __name__ == '__main__':
        main()
```

The `main()` function is the driver for your program. Any function calls that we execute will be called from here. This is also the simplest of the functions so we can use it to explain the layout of a function. First the function is defined with the `def` keyword followed the name of the function (in this case `main`) and `()`. The `()` will contain any parameters (arguments) that the specific function is expecting. 

So a simple function might looks something like this:

```
    def double(num):
        return num * 2
```

In the above function the argument `num` is passed to the function `double`. The function returns `num * 2`. You will notice that none of our functions take any arguments or return anything. This is because we are using global variables (we don't need to pass variables around since each function has direct access to them (global scope).

The `if __name__ == '__main__':` statement basically allows our code to either be run as a standalone program or imported into a different program. This is a good practice. 

### STEP 6: Run the program

For now let's run our program for the first time. With the **main.py** file open push the play button in the top right corner of vscode. 

You'll notice that the program does nothing. This is because the only statement within `main`, that is not commented out, is `pass`. `pass` is a NULL statement meaing that it does nothing. Let's move on to something more relevant. 

--- 

## TASK 5: Verifying Access to the NSO Instance

### STEP 1: Explore the get_verify_restconf() function

One of the first things we should do is to verify that we have access to our NSO instance. We need to ensure that our NSO instance is reachable via the RESTConf API, and that our user has the ability to make calls. To this end we have a function called `get_verify_restconf()`. Let's take a look at this function: 

```
    ## Verifies access to the RestConf API of NSO
    def get_verify_restconf():
        path = '{}/restconf'.format(NSO_HOST)
        req = requests.get(path, auth=AUTH, headers=HEADERS, verify=VERIFY)
        if req.status_code == 200:
            data = (req.json())
            print(json.dumps(data, indent=4))
        else:
            print('Error Code: {}'.format(req.status_code))

```
First we see the function definition `def get_verify_restconf()`. For our functions the first part of the name is what type of HTTP verb we are using. All of our calls to NSO will be GET calls, but you can also make POST, PATCH, PUT, DELETE calls. The second part of the name provides information about the intent of the function. So  `get_verify_restconf` means that we are making an HTTP GET in order to verify our access to the RESTConf API. 

The next line is a variable named `path`. 
    
```
    path = '{}/restconf'.format(NSO_HOST)
```

This variable is assigned to `'{}/restconf'.format(NSO_HOST)`. So what is this variable? It is a formated string. This is formatted by taking the variable stored in `NSO_HOST` and placing into the string at the location of the `{}`. So what stored in `path` is `https://path_to_nso.com/restconf`. 

Next we have another variable called `req`.

```
    req = requests.get(path, auth=AUTH, headers=HEADERS, verify=VERIFY)
```
In this line we are assigning the **return** of a function call to requests to the variable `req`. So what does that mean exactly? Within the requests library there are different methods (functions) that can be performed. The one we are using here is **get**. We tell requests to initiate a get with the `request.get()` method. However, we need to pass some parameters to the function. The ones we are passing here are:

1. URL - this is the path to the service we are trying to access. This is only required parameter for a `request.get()` and is assigned to our variable `path`
2. auth - this is a tuple containing authentication information. Ours is assigned to our global variable `AUTH`. Which is pulled from our **.env** file. 
3. headers - this is a dictionary of headers send to the URL. Ours is assigned to our global variable `HEADERS`.
4. verify - this is a boolean (the deafult is == true) that dictates whether the server's TLS certifiate is verified. Ours is assigned to the global variable `VERIFY`.

Note: You can probably see the utility of global functions at this point. Each of those variables are used multiple times within the code. If any of the values ever needed to change we would only need to change them in one location. 

The next section of code you will see is this:

```
    if req.status_code == 200:
        data = (req.json())
        print(json.dumps(data, indent=4))
    else:
        print('Error Code: {}'.format(req.status_code))
```

Stored within the requests object `req` is a lot of information. In the references section you can explore more about the requests object. For our purposes we will be using a few of the attributes. One of the important attributes of the requests object is the `response_code`. For this request a successful **get** will result in the HTTP Response of 200. So our IF-ELSE statement says to check the response code, if it is 200 (successful) do-stuff (we'll see what that stuff is next), if it is not 200 (unssuccessful) print the response code. By using this flow control we keep our program from crashing if the request is not successful, and we get some information about what the problem may be. 

Assuming that the request is successful (we have a response code of 200) we can now do something useful with that object. Here we have the two lines of code executed on a successful get:

```
    data = (req.json())
    print(json.dumps(data, indent=4))
```

Stored within the request object is an attribute called `text`. This attribute is simply the payload of the requests object. In our scenario the `text` attribute is formatted as a JSON string. We could print the string and see what is in it, but we cannot index into the payload in any meaningful way. So in the first line of this code block take the text of the request object render it in JSON (this makes it iterable). We assign that dictionary to the variable `data`. 

The next line is a print statement that takes our `data` variable and prints it as a JSON string with some formatting to make it easier to read. 

### STEP 2: Verify Access RestConf access to the NSO instance

Finally we are able to make our first call to NSO. Go into the `main()` function and uncomment the call to `get_verify_restconf()`. You can then run the program by hitting Ctrl+F5 or the play button in the top right of the vscode window. 

Note: We will be commenting and uncommenting many lines of code. You can easily comment/uncomment a line in vscode by hitting Ctrl+/ while having your cursor on the line to be modified. 

Within your terminal you should see the following:

```
    {
        "ietf-restconf:restconf": {
            "data": {},
            "operations": {},
            "yang-library-version": "2019-01-04"
        }
    }
```

This output means that we can successfully reach and authenticate to our NSO instance. You can now comment out `get_verify_restconf()` and move on to the next section. 

---

## TASK 6: Getting Device Groups

### STEP 1: Explore the get_device_groups() function

Now that we verified our access to the NSO RestConf API we can begin gathering more useful information. One of the convenient features of Cisco NSO is the ability to create device groups. Devices can be group in any manner that suites your orgainization i.e. by vendor, model, operating system, role, etc. Groups can also contain other groups. The purpose of the `get_device_groups()` function is to retreive information about the groups (and their members) that are configured on NSO. 

```
    ## Retrieves the device groups configured on NSO
    def get_device_groups():
        ## You will need to edit the following line to gather only the members of the ALL group
        path = '{}/restconf/data/tailf-ncs:devices/device-group'.format(NSO_HOST)
        req = requests.get(path, auth=AUTH, headers=HEADERS, verify=False)
        if req.status_code == 200:
            data = (json.loads(req.text))
            print(json.dumps(data, indent=4))

            # # UNCOMMENT 1 START
            # groups = data['tailf-ncs:device-group']
            # for group in groups:
            #    print('Group Name: {}'.format(group['name']))
            #    print('\tMembers: ')
            #    for member in group['member']:
            #        print('\t\t{}'.format(member))
            # # UNCOMMENT 1 STOP
            
            # # UNCOMMENT 2 START
            #        DEVICES.append(m)
            # # UNCOMMENT 2 STOP
        else:
            print('Error Code: {}'.format(r.status_code))
```

Go into the the main() function and uncomment the call to this functio (i.e. make the function active).

### STEP 2: Retreive all device group information

Notice that the much of the function is currently commented out. As the function is currently coded it will make a get request to the path: `http://path_to_nso.com/restconf/data/tailf-ncs:devices/device-group`. The function then prints the return payload in the same way as the previous function. Go to the `main()` function and ensure that the `get_device_groups()` function is the only one that active and run the program. 

You can see that the function call returns a sizeable amount of information. Let's look at the structure of the return.

We can see that the return is a dictionary (JSON formatted) that contains a dictionary with the key **tailf-ncs:device-group** and the value is a list of the device groups configured. Each of the list members is itself a dictionary with the following structure:

- name: STRING - name of the group
- device-group: LIST - lists any subgroups that are members of this group
- device-name: LIST - lists any devices that are members of this group
- member: LIST - lists any devices that are members of this group or a subgroup
- ned-id: LIST - lists Network Element Drivers used for the members of this group
- alarm-summary: DICT - details any alarms on members of the group

Note: device-group is only returned on groups with subgroups and device-name is only returned on groups with individual device members. 

### STEP 3: Print out only device members

While the information provided in the payload is helpful all we really need are the individual devices onboarded to NSO. As mentioned above this information is stored in `member` list of each group. Examine this code block:

```
    # # UNCOMMENT 1 START
    # groups = data['tailf-ncs:device-group']
    # for group in groups:
    #    print('Group Name: {}'.format(group['name']))
    #    print('\tMembers: ')
    #    for member in group['member']:
    #        print('\t\t{}'.format(member))
    # # UNCOMMENT 1 STOP
```

This block of code will make it easier to see which devices are members of which groups. First, the contents of **tailf-ncs:device-group** are assigned to a variable `groups`. `groups` now contains a list of all of the groups. The code then iterates through the list and prints the names of the groups, then iterates through the `member` list and prints the names of the members. Uncomment the code block (from **UNCOMMENT 1 START** to **UNCOMMENT 1 STOP**) and run the program again. You should see something similar to this:

```
    Group Name: ALL
        Members: 
            core-rtr01
            core-rtr02
            dist-rtr01
            dist-rtr02
            dist-sw01
            dist-sw02
            edge-firewall01
            internet-rtr01
    Group Name: ASA-DEVICES
        Members: 
            edge-firewall01
    Group Name: IOS-DEVICES
        Members: 
            dist-rtr01
            dist-rtr02
            internet-rtr01
    Group Name: NXOS-DEVICES
        Members: 
            dist-sw01
            dist-sw02
    Group Name: XR-DEVICES
        Members: 
            core-rtr01
            core-rtr02
```

Note: Your list may not contain the same groups or members. In this example we are running the program towards the NSO instance in DevNet sandbox. 

### STEP 4: Modify the URL to return only the **ALL** group and add the devices to the **DEVICES** list

Take a look at the NSO RestConf api documentation here (also listed in the references section): 

https://developer.cisco.com/docs/nso/#!cisco-nso-restconf-swagger-api-docs-overview

On the left hand plan you will see a link to **API**. This link will detail some of the calls that can be made towards NSO. Keep in mind that this section details only a portion of the calls that can be made towards NSO, focusing on some useful **GET** requests to gather information about devices on the network. 

If you expand the section on Device **Groups/Alarms/Authgroups** you will see an example of how we are calling our NSO instance at `tailf-ncs:devices/device-group`. Using the other possible URLs in this section see if you can figure out how to modify the URL (remember the URL is stored in the `path` variable) in this function to only pull the members from the **ALL** group. Once you think you have this figured out run the program again. Your output should be similar to this:

```
Group Name: ALL
    Members: 
        core-rtr01
        core-rtr02
        dist-rtr01
        dist-rtr02
        dist-sw01
        dist-sw02
        edge-firewall01
        internet-rtr01
```
Note: As mentioned previously NSO allows you to group your devices in different ways, but it is a good practice to always have a group that includes all devices. 

We now need to store the device names in the `DEVICES` list. We are going to use the `DEVICES` list to gather information about each device in the next step. Examine this section of the function:

```
    # UNCOMMENT 2 START
        DEVICES.append(m)
    # UNCOMMENT 2 STOP
```

This section of code takes each of the device names and adds them to the global `DEVICES` list. You can now uncomment this section. Now if we print the `DEVICES` list out it will look similar to this:

```
    ['core-rtr01', 'core-rtr02', 'dist-rtr01', 'dist-rtr02', 'dist-sw01', 'dist-sw02', 'edge-firewall01', 'internet-rtr01']
```

Note: It is important that we pulled device names from the **ALL** group only otherwise we would end up with duplicates in our `DEVICES` list. However, we could have done this without modifying the ``path` variable. We could have used Python to test for the presence of an element in the list before adding it. If you have time see if you can figure out how to do this. 

## TASK 7: Getting Device Platform Details

### STEP 1: Explore the get_device_platform_details() function

The global `DEVICES` list is now populated with the names of the devices in our inventory. We can use this information to make calls to NSO in order to gather information about each device. Take a look at the `get_device_platform_deatils()` function below:

```
    def get_device_platform_details():
        os = []
        version = []
        model = []
        serial = []

        for device in DEVICES:
            path = '{}/restconf/data/tailf-ncs:devices/device={}/platform'.format(NSO_HOST, device)
            req = requests.get(path, auth=AUTH, headers=HEADERS, verify=False)
            if req.status_code == 200:
                info = req.json()
                os.append(info['tailf-ncs:platform']['name'])
                version.append(info['tailf-ncs:platform']['version'])
                model.append(info['tailf-ncs:platform']['model'])
                serial.append(info['tailf-ncs:platform']['serial-number'])
            else:
                error = 'Error Code: {}'.format(req.status_code)
                os.append(error)
                version.append(error)
                model.append(error)
                serial.append(error)

        PLATFORM_DETAILS['OS Type'] = os 
        PLATFORM_DETAILS['Version'] =  version 
        PLATFORM_DETAILS['Model'] = model 
        PLATFORM_DETAILS['Serial'] = serial
```

This function will iterate through the `DEVICES` list and make a RestConf call to gather platform information. The retrieved information will be stored in four Python lists:

 - `os` - the operating system of the device 
 - `version` - the version of the operating system 
 - `model` - the model of the device 
 - `serial` - the serial number of the device

Go into the the main() function and uncomment the call to this functio (i.e. make the function active).

### STEP 2: Calling the NSO for platform details

If you go back to the NSO RestConf documentation and navigate to the **Single Device HW / SW Platform Info** (https://developer.cisco.com/docs/nso/#!single-device-hw-sw-platform-info) you can execute that call towards the DevNet Sandbox to see how the return is structured. 

```
    {
        "tailf-ncs:platform": {
            "name": "ios-xe",
            "version": "16.11.1b",
            "model": "CSR1000V",
            "serial-number": "9KEPZN1TV7G"
        }
    }
```
This will make visualizing what our `for` loop is doing more clear. First the code constructs our URL with name of the device in the `DEVICES` list:

```
    path = '{}/restconf/data/tailf-ncs:devices/device={}/platform'.format(NSO_HOST, device)
```

What is stored in `path` is `https://path_to_nso.com/restconf/data/tailf-ncs:devices=DEVICES[0-len(DEVICES)]/platform` 

Now that we have the URL for a single device we can create our requests object in the same way we have done previously:

```
    req = requests.get(path, auth=AUTH, headers=HEADERS, verify=False)
```

Once again if the `status_code` is 200 our call was successful and we can process the data. First we store the return payload in a variable called `info`.

```
    info = req.json()
```

Next we index into `info` storing the the platform details in the previously defined lists(`os`, `version`, `model` and `serial`):

```
    os.append(info['tailf-ncs:platform']['name'])
    version.append(info['tailf-ncs:platform']['version'])
    model.append(info['tailf-ncs:platform']['model'])
    serial.append(info['tailf-ncs:platform']['serial-number'])
```

Since we iterate through the `DEVICES` list in order the same index will apply to the other Python lists. For example, if **router1** is the first device in `DEVICES` its index will be 0. Its platform details will be stored at index 0 of each of the previously created lists. 

As with our previous functions we want to account for errors where the API call is not successful. We do this in our `else` statement:

```
    else:
        error = 'Error Code: {}'.format(req.status_code)
        os.append(error)
        version.append(error)
        model.append(error)
        serial.append(error)

```
First we construct a string `error` which contains the `status_code`. We then append that string into the platform lists in place of the information that should have been received. It is important we do this because if we did not append anything our indexing would be thrown off. 

### STEP 3: Constructing and returning the device_data dictionary

Once all of the platform lists are populated we can populate the global Python dictionary `PLATFORM_DETAILS` with the information we have gathered. We do this with the following lines of code:

```
    PLATFORM_DETAILS['OS Type'] = os 
    PLATFORM_DETAILS['Version'] =  version 
    PLATFORM_DETAILS['Model'] = model 
    PLATFORM_DETAILS['Serial'] = serial

```

Let's see what is now stored in the `PLATFORM_DETAILS` dictionary:

```
    {
        "OS Type": [
            "Error Code: 204",
            "Error Code: 204",
            "ios-xe",
            "ios-xe",
            "NX-OS",
            "NX-OS",
            "asa",
            "ios-xe"
        ],
        "Version": [
            "Error Code: 204",
            "Error Code: 204",
            "16.11.1b",
            "16.11.1b",
            "9.2(3)",
            "9.2(3)",
            "9.12(2)",
            "16.11.1b"
        ],
        "Model": [
            "Error Code: 204",
            "Error Code: 204",
            "CSR1000V",
            "CSR1000V",
            "cisco Nexus9000 9000v Chassis ",
            "cisco Nexus9000 9000v Chassis ",
            "ASAv",
            "CSR1000V"
        ],
        "Serial": [
            "Error Code: 204",
            "Error Code: 204",
            "9KEPZN1TV7G",
            "9NXO8PIMBCS",
            "9I9QUEGF4HH",
            "9MGCEDFFPNT",
            "9AECK15LSLF",
            "929MFXYBMRP"
        ]
    }
```

In the example above you can see that the devices in `DEVICES` at indices 0-1 are returning with a status code of 204. 204 indicates an empty payload so the the information needed is not available. We point this out for illustrative purposes. 

## TASK 8: Creating a Data Frame and Saving to XLSX

### STEP 1: Creating a Pandas Data Frame

Pandas is a Python Library that is used in data analysis. The library includes a host of tools that allow the user to modify, format, and store data. Today we will be using Pandas to create a **data frame**. We do this with a very simple function called `create_data_frame()`:

```
## Creates a Pandas Data Frame 
    def create_data_frame():
        df = pd.DataFrame(PLATFORM_DETAILS, index=DEVICES)
        # Uncomment the line below if you want to see the formatting of the data frame.
        # print(df)
        return(df)
```
This function utilizes the platform data stored in `PLATFORM_DETAILS` to create columns of information, and uses the device names in `DEVICES` to index the columns. The data frame will end up looking similar to this (you can uncomment the the print statement to see your own):

```
                         OS Type          Version                           Model           Serial
core-rtr01       Error Code: 204  Error Code: 204                 Error Code: 204  Error Code: 204
core-rtr02       Error Code: 204  Error Code: 204                 Error Code: 204  Error Code: 204
dist-rtr01                ios-xe         16.11.1b                        CSR1000V      9KEPZN1TV7G
dist-rtr02                ios-xe         16.11.1b                        CSR1000V      9NXO8PIMBCS
dist-sw01                  NX-OS           9.2(3)  cisco Nexus9000 9000v Chassis       9I9QUEGF4HH
dist-sw02                  NX-OS           9.2(3)  cisco Nexus9000 9000v Chassis       9MGCEDFFPNT
edge-firewall01              asa          9.12(2)                            ASAv      9AECK15LSLF
internet-rtr01            ios-xe         16.11.1b                        CSR1000V      929MFXYBMRP
```

We call this function from `main()` with this line of code:

```
    device_df = create_data_frame()
```

This line creates a data frame called `device_df` by passing the `PLATFORM_DETAILS` dictionary as the data, and the `DEVICES` list as the index. The function returns the data frame to the calling function (in this case main().

Go into the the main() function and uncomment the call to this function (i.e. make the function active).

### STEP 2: Writing the inventory to an .xlsx file

You may notice that the Pandas data frame has a structure similar to a spreadsheet. There are columns and rows with cells that contain data. Pandas provides us with a useful method of saving our data frame as a .xlsx file. All we need to do is perform the `to_excel()` function on the data frame, passing in the name of the file we wish to have the inventory saved in. See this line of code in `main()`:

```
    device_df.to_excel('./inventory.xlsx')
```

Go into the the main() function and uncomment the call to this functio (i.e. make the function active).

You should see a new file **inventory.xlsx** appear in the working directory. You can open this file to view its contents by utilizing the file navigator on the desktop. 

![text!](/images/inventory_xlsx.png)

## References

NSO RESTConf API Reference
- https://developer.cisco.com/docs/nso/#!cisco-nso-restconf-swagger-api-docs-overview

Python Requests get() Method (cite W3Schools)
- https://www.w3schools.com/python/ref_requests_get.asp

Python Requests Object (cite W3Schools)
- https://www.w3schools.com/python/ref_requests_response.asp

HTTP Response Codes (cite Mozilla)
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

Python Pandas Documentation (cite Pandas)
- https://pandas.pydata.org

