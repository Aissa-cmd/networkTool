# networkTool

networkTool is a program written in python3 to help network administrators to do subnetting easily, it can do subnitting using both FLSM (Fixed Length Subnet Mask) and VLSM (Variable Length Subnet Mask), it also gives you the ability to save the result to a csv file for later usage.

## Requirements

For the program to work you should have python3.6 or above installed, if you are using **windows** it is recommanded that you use [**Git Bash**](https://gitforwindows.org/) to run the program rather than the command line prompt because it doesn't support colors and the ouput would not be readable, you also need to install the following packages
1. IPy
2. termcolor

you can install these packages using the following command
```
pip3 install -r requirements.txt
```
or
```
pip3 install IPy
pip3 install termcolor
```

## Help

```
usage: networkTool.py [-h] --network CIDR [--network-info] [--contains [CONTAINS [CONTAINS ...]]] [--subnetworks [SUBNETWORKS [SUBNETWORKS ...]]] 
                      [--subnet-technique {VLSM,FLSM}] [--subnet-info] [--available] [-o] [-on OUTPUT_NAME]
optional arguments:                                                                                                                                                       
-h, --help            show this help message and exit                                                                                                                   
--network CIDR        The CIDR notation of a network                                                                                                                    
--network-info        Show the Info section of the network entered with (--network) option                                                                              
--contains [CONTAINS [CONTAINS ...]]
            A list of IP address to check if they belong tho the network or not (separate the ip addressed with space)                                        
--subnetworks [SUBNETWORKS [SUBNETWORKS ...]]
            A list of numbers of hosts in each subnetwork (Enter the values separated by space)                                                               
--subnet-technique {VLSM,FLSM}
            Choose the technique to use when subnetting the network either VLSM or FLSM (required when using the --subnetworks option)                       
--subnet-info         Show Info section for each subnetwork                                                                                                             
--available           Show the available Networks after subnetting                                                                                                      
-o, --output          Save output to a csv file                                                                                                                         
-on OUTPUT_NAME, --output-name OUTPUT_NAME
            Save csv file with custom file name (default: YYMMDD_HHMMSS_subnet_technique_network.csv)                                                                             
```

## Usage

The output of the program is divided into multiple section
1. Info Section
2. Belongs Section
3. VLSM Subnitting Section or FLSM Subnitting Section
4. Available Section

### Info Section
This section shows information about the network specified with the **--network** option and to show this section you need to use the **--network-info** flag

![1](https://user-images.githubusercontent.com/70541804/118563789-211d1280-b767-11eb-92e9-338fe75c68d3.JPG)


### Belong Section
This section is authomaticaly shown when the **--contains** option is used which takes a list of IP addresses (separated by spaces) and tells weather each IP address belongs to the network specified withe **--network** option 

![2](https://user-images.githubusercontent.com/70541804/118563973-65a8ae00-b767-11eb-84f8-1ab1203d05d2.JPG)

### VLSM Subnitting Section or FLSM Subnitting Section
This section is shown when the **--subnetworks** is used and it takes a list of the number of hosts that are needed for each subnetwork (without calculating the network id and the broadcast ip address), you can subnet a network using either **FLSM** or **VLSM***, and you can specify that using the **--subnet-technique** which can take to optional values either VLSM or FLSM (both uppercase)

![3](https://user-images.githubusercontent.com/70541804/118564682-aa811480-b768-11eb-96fd-2ce5ee82c5a8.JPG)

![4](https://user-images.githubusercontent.com/70541804/118564701-afde5f00-b768-11eb-9e2d-650e653bf22c.JPG)

you can also show information about each subnetwork using the **--subnet-info** flag.

![5](https://user-images.githubusercontent.com/70541804/118564878-11063280-b769-11eb-82e7-8a32ab2e0820.JPG)

### Available Section

This section shows the available network that are still available after subnitting (if any) and you can view this section by using the flag **--available**
