#!/usr/bin/env python3

# By: Aissa Ouboukioud

from ipaddress import IPv4Network
from functools import wraps
from IPy import IP
from termcolor import cprint
import argparse
import math
import csv
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('--network', dest="cidr", required=True, help="The CIDR notation of a network")
parser.add_argument('--network-info', action="store_true", help="Show the Info section of the network entered with (--network) option")
parser.add_argument('--contains', nargs="*", help="A list of IP address to check if they belong tho the network or not (separate the ip addressed with space)")
parser.add_argument('--subnetworks', nargs="*", type=int, help="A list of numbers of hosts in each subnetwork (Enter the values separated by space)")
parser.add_argument('--subnet-technique', choices=['VLSM', 'FLSM'], help="Choose the technique to use when subnetting the network either VLSM or FLSM (required when using the --subnetworks option)")
parser.add_argument('--subnet-info', action="store_true", help="Show Info section for each subnetwork")
parser.add_argument('--available', action="store_true", help="Show the available Networks after subnetting")
parser.add_argument('-o', '--output', action="store_true", help="Save output to a csv file")
parser.add_argument('-on', '--output-name', help="Save csv file with custom file name (default: YYMMDD_HHMMSS_subnet_technique_network.csv)")


args = parser.parse_args()


def section_legend(legend):
    def _outer_wrapper(func):
        @wraps(func)
        def _inner_wrapper(*args, **kwargs):
            print(f"\n===================[{legend}]=====================")
            func(*args, **kwargs)
            print("==============================================")
        return _inner_wrapper
    return _outer_wrapper


def info(cidr,  prefix_text="", color="white"):
    cprint(f"{prefix_text}CIDR notation   : {cidr}", color, attrs=["bold"])
    cprint(f"{prefix_text}Network mask    : {cidr.netmask}", color, attrs=["bold"])
    cprint(f"{prefix_text}IP type         : {IP(str(cidr), make_net=True).iptype()}", color, attrs=["bold"])
    cprint(f"{prefix_text}Network ID      : {cidr[0]}", color, attrs=["bold"])
    cprint(f"{prefix_text}Broadcast IP    : {cidr.broadcast_address}", color, attrs=["bold"])
    cprint(f"{prefix_text}Usable IP addrs : {cidr.num_addresses-2}", color, attrs=["bold"])
    cprint(f"{prefix_text}Range of IPs    : {cidr[1]}-{cidr[-2]}", color, attrs=["bold"])


def getStringInfo(numhosts ,cidr):
    return f"{numhosts},{str(cidr)},{cidr.netmask},{IP(str(cidr), make_net=True).iptype()},{str(cidr).split('/')[0]},{cidr.broadcast_address},{cidr.num_addresses-2},{cidr[1]},{cidr[-2]}"


@section_legend("Belongs")
def contains(network, ips):
    network = IP(str(network), make_net=True)
    for ip in ips:
        if network.overlaps(ip):
            cprint(f"{ip:13s}", "green", attrs=["bold"], end=" ")
            print(f"Belongs to the network {network}")
        else:
            cprint(f"{ip:13s}", "red", attrs=["bold"], end=" ")
            print(f"Doesn't Belongs to the network {network}")


q = []
sub_networks = []
subnetworks_dict = []
"""
{
    'numhosts': ,
    'cidr': ,
    'netmask': ,
    'iptype': ,
    'netid': ,
    'broadcastip': ,
    'usableip': ,
    'firstip': ,
    'lastip': 
}
"""


@section_legend("VLSM Subnetting")
def subnet_vlsm(network, subnetworks):
    global q
    q.append(network.subnets(new_prefix=network.prefixlen))
    i = 1
    while subnetworks:
        snet = subnetworks[-1]+2
        snet_prefix_len = 32 - (math.ceil(math.log(snet, 2)))
        try:
            new_snet = next(q[0])
        except StopIteration:
            q.pop(0)
            continue
        except IndexError:
            cprint(f"\n[!!] The network {str(network)} can't cover all the subetworks\n     these networks are not covered {str(subnetworks)}\n", "red", attrs=["bold"])
            raise Exception("Can't cover all networks")
        subnetworks.pop()
        q.insert(0, new_snet.subnets(new_prefix=snet_prefix_len))
        new_snet = next(q[0])
        sub_networks.append(str(new_snet))
        print(f"{i:2d}", end=") ")
        cprint(f"{str(new_snet):17s}", "cyan", attrs=["bold"], end=" ")
        cprint(f"({snet-2} Hosts)", "green", attrs=["bold"])
        if args.subnet_info:
            info(new_snet, prefix_text="\t| ")
        if args.output:
            subnetworks_dict.append(getStringInfo(snet-2, new_snet))
        i += 1    


@section_legend("FLSM Subnetting")
def subnet_flsm(network, subnetworks):
    global q
    large_net_hosts = subnetworks[-1]+2
    large_prefix_len = 32 - (math.ceil(math.log(large_net_hosts, 2)))
    q.append(network.subnets(new_prefix=large_prefix_len))
    i = 1
    while subnetworks:
        try:
            sn = next(q[0])
        except:
            q.pop()
            cprint(f"\n[!!] The network {str(network)} can't cover all the subetworks\n     these networks are not covered {str(subnetworks)}\n", "red", attrs=["bold"])
            raise Exception("Can't cover all networks")
        snet = subnetworks.pop()
        sub_networks.append(str(sn))
        print(f"{i:2d}", end=") ")
        cprint(f"{str(sn):17s}", "cyan", attrs=["bold"], end=" ")
        cprint(f"({snet} Hosts)", "green", attrs=["bold"])
        if args.subnet_info:
            info(sn, prefix_text="\t| ")
        if args.output:
            subnetworks_dict.append(getStringInfo(snet, sn))
        i += 1


@section_legend("Availble Networks")
def available(network):
    global q
    if not q:
        print("No available Networks")
    else:
        i = 1
        net = IP(network, make_net=True)
        for snet in sub_networks:
            net -= IP(snet)

        for avnet in net:
            print(f"{i:2d}", end=") ")
            cprint(f"{str(avnet):17s}", "cyan", attrs=["bold"])
            i += 1


def getfile_name(netmask):
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{args.subnet_technique}_{args.cidr.split('/')[0]}_{netmask}.csv"


def save_output(netmask, file_name=None):
    if file_name is None:
        file_name = getfile_name(netmask)
    with open(file_name, "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Number of hosts', 'Network', 'Network mask', 'IP type', 'Network ID', 'Broadcast IP', 'Usable IPs', 'First IP', 'Last IP'])
        for snet in subnetworks_dict:
            csv_writer.writerow(snet.split(','))
    

def main():
    cidr = args.cidr
    try:
        net = IPv4Network(cidr, strict=False)
    except:
        parser.print_help()
        exit()
    if args.network_info:
        section_legend("Info")(info)(net, color="yellow")
    if args.contains is not None:
        contains_ips = args.contains
        contains(net, contains_ips)
    if args.subnetworks != None and args.subnet_technique != None:
        subnets = args.subnetworks
        subnets.sort()
        if args.subnet_technique.upper() == "FLSM":
            try:
                subnet_flsm(net, subnets)
            except:
                return
        else:
            try:
                subnet_vlsm(net, subnets)
            except:
                return
        if args.available:
            available(cidr)
        if args.output:
            save_output(net.netmask, args.output_name)


if __name__ == "__main__":
    main()
