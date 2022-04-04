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
            data = (json.loads(req.text))
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
        data = (json.loads(req.text))
        print(json.dumps(data, indent=4))
    else:
        print('Error Code: {}'.format(req.status_code))
```

Stored within the requests object `req` is a lot of information. In the references section you can explore more about the requests object. For our purposes we will be using a few of the attributes. One of the important attributes of the requests object is the `response_code`. For this request a successful **get** will result in the HTTP Response of 200. So our IF-ELSE statement says to check the response code, if it is 200 (successful) do-stuff (we'll see what that stuff is next), if it is not 200 (unssuccessful) print the response code. By using this flow control we keep our program from crashing if the request is not successful, and we get some information about what the problem may be. 

Assuming that the request is successful (we have a response code of 200) we can now do something useful with that object. Here we have the two lines of code executed on a successful get:

```
    data = (json.loads(req.text))
    print(json.dumps(data, indent=4))
```

Stored within the request object is an attribute called `text`. This attribute is simply the payload of the requests object. In our scenario the `text` attribute is formatted as a JSON string. We could print the string and see what is in it, but we cannot index into the payload in any meaningful way. So in the first line of this code block take the text of the request object and use the `json.loads()` function to create a Python dictionary. We assign that dictionary to the variable `data`. 

The next line is a print statement that takes our `data` dictionary and prints it as a JSON string with some formatting to make it easier to read. 

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

Now that we covered our first requests call to NSO 



## References

NSO RESTConf API Reference
- https://developer.cisco.com/docs/nso/#!cisco-nso-restconf-swagger-api-docs-overview

Python Requests get() Method (cite W3Schools)
- https://www.w3schools.com/python/ref_requests_get.asp

Python Requests Object (cite W3Schools)
- https://www.w3schools.com/python/ref_requests_response.asp

HTTP Response Codes (cite Mozilla)
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status