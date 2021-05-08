#!/usr/bin/python3

# By: Aissa Ouboukioud

from ipaddress import IPv4Network
from IPy import IP
from termcolor import cprint
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('--cidr', required=True, help="The CIDR notation of a network")
parser.add_argument('--network-info', action="store_true", help="Show the Info section of the network entered with CIDR option")
parser.add_argument('--contains', nargs="*", help="An IP address to check if it is within the network or not")
parser.add_argument('--subnetworks', nargs="*", type=int, help="A list of numbers of hosts in each subnetwork (Enter the value separated by space)")
parser.add_argument('--subnet-technique', choices=['VLSM', 'FLSM'], help="Use the VLSM technique to subnite the network")
parser.add_argument('--subnet-info', action="store_true", help="Show Info section for each subnetwork")
parser.add_argument('--available', action="store_true", help="Show the available Networks after subnetting")

args = parser.parse_args()

def section_legend(legend):
    def _outer_wrapper(func):
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


@section_legend("VLSM Subnetting")
def subnet_vlsm(network, subnetworks):
    global q
    q.append(network)
    ii = 1
    for i in range(len(subnetworks)):
        snet = subnetworks.pop()
        snet_prefix_len = 32 - (math.ceil(math.log(snet, 2)))
        new_snet = q.pop(0).subnets(new_prefix=snet_prefix_len)
        j = 0
        insert_pos = 0
        for nsnet in new_snet:
            if j == 0:
                print(f"{ii:2d}", end=") ")
                cprint(f"{str(nsnet):17s}", "cyan", attrs=["bold"], end=" ")
                cprint(f"({snet-2} Hosts)", "green", attrs=["bold"])
                if args.subnet_info:
                    info(nsnet, prefix_text="\t| ")
                ii += 1
                j += 1
            else:
                q.insert(insert_pos, nsnet)
                insert_pos += 1
        else:
            j = 0
            insert_pos = 0


@section_legend("FLSM Subnetting")
def subnet_flsm(network, subnetworks):
    global q
    large_net_hosts = int(max(subnetworks))
    large_prefix_len = 32 - (math.ceil(math.log(large_net_hosts, 2)))
    snets = [sn for sn in network.subnets(new_prefix=large_prefix_len)]
    i = 1
    for j in range(len(subnetworks)):
        sn = snets.pop(0)
        print(f"{i:2d}", end=") ")
        cprint(sn, "cyan", attrs=["bold"])
        if args.subnet_info:
            info(sn, prefix_text="\t| ")
        i += 1
    if args.available:
        for sn in snets:
            q.append(sn)

        
@section_legend("Availble Networks")
def available():
    global q
    if not q:
        print("No available Networks")
    else:
        i = 1 
        for sn in q:
            print(f"{i:2d}", end=") ")
            cprint(f"{str(sn):17s}", "cyan", attrs=["bold"], end=" ")
            cprint("(Available)", "green", attrs=["bold"])
            i += 1


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
        subnets = [x+2 for x in subnets]
        subnets.sort()
        if args.subnet_technique == "FLSM":
            subnet_flsm(net, subnets)
        else:
            subnet_vlsm(net, subnets)
    if args.available:
        available()


if __name__ == "__main__":
    main()
