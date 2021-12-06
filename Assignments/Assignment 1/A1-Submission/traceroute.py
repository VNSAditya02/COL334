from scapy.all import *
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
domainName = str(input("Enter hostname: "))
hop_list = []
rtt_list = []
print("Trace route to: " + domainName + ", Max hops: 64")
print("-"*57)
print("Hop Number\tIP Address of the Hop\tRTT Value(in ms)")
print("-"*57)
space1 = 15
for i in range(1, 65):

    # Takes care of spaces in output
    space2 = 24
    if i >= 10:
        space1 = 14
    # Sending ICMP Packets with varying TTL Values, timeout is 10 sec
    # Program tries 3 times to get reply
    count1 = 0
    packet1 = IP(dst = domainName, ttl = i) / ICMP()
    reply1 = sr1(packet1, verbose = 0, timeout = 10)
    count1 += 1
    while (count1 < 3) and (reply1 is None):
        packet1 = IP(dst = domainName, ttl = i) / ICMP()
        reply1 = sr1(packet1, verbose = 0, timeout = 10)
        count1 += 1

    if reply1 is None:
        print(str(i) + " "*space1 + "*"*15 + " "*9 + "0")
        hop_list.append(i)
        rtt_list.append(0)
        continue

    space2 -= len(str(reply1.src))
    # Sending ICMP Packets to hop IP Address and get RTT Value
    # Program tries 3 times to get reply
    count2 = 0
    packet2 = IP(dst = reply1.src) / ICMP()
    reply2, noreply2 = sr(packet2*3, verbose = 0, timeout = 10)
    count2 += 1
    while (count2 < 3) and (reply2 is None):
        packet2 = IP(dst = reply1.src) / ICMP()
        reply2, noreply2 = sr(packet2*3, verbose = 0, timeout = 10)
        count2 += 1
    
    # time stores RTT value, If we won't get any reply RTT value is 0
    time = 0
    if len(reply2) == 0:
        time = 0
    else:
        sent = datetime.fromtimestamp(reply2[0][0].sent_time)
        received = datetime.fromtimestamp(reply2[0][1].time)
        time = (received - sent).total_seconds() * 1000.0

    # If packet reaches destination, we break from the loop, else we continue to the next hop
    if reply1.type == 0:
        print (str(i) + " "*space1 + str(reply1.src) + " "*space2 + str(time)[:7])
        hop_list.append(i)
        rtt_list.append(time)
        break
    else:
        print (str(i) + " "*space1 + str(reply1.src) + " "*space2 + str(time)[:7])
        hop_list.append(i)
        rtt_list.append(time)


toSave = domainName +'_RTT_vs_hop.png'
x = [i for i in range(1, len(hop_list) + 1)]
plt.plot(hop_list, rtt_list)
plt.xlabel('Hop Number')
plt.ylabel('RTT (in ms)')
plt.title('RTT vs Hop Number')
plt.xticks(hop_list, x)
#print(toSave)
plt.savefig(toSave)
#plt.show()
