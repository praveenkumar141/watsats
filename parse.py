import re
import sys
from os import path


date = re.compile(r"\d{1,2}\/\d{1,2}\/\d{2}")
phno = re.compile(r"(\d{5}\s\d{5})")
cont = re.compile(r"\-\s[\w\s]+?\:")
jond = re.compile(r"(\w+\s?\w+)(?:\s)(?=joined using this group's invite link)")
addd = re.compile(r"((\d{5}\s\d{5})|(\w*\s?\w+?))\sadded\s((\d{5}\s\d{5})|(\w*\s?\w+?))\n")
left = re.compile(r"((\d{5}\s\d{5})|(\w*\s?\w+?))\s(left)") # Doesn't work
subj = re.compile(r"((\d{5}\s\d{5})|(\w*\s?\w+?))\schanged the subject from (\".+?\") to (\".+?\")", flags=re.S)
icon = re.compile(r"((\d{5}\s\d{5})|(\w*\s?\w+?))\schanged this group's icon")


with open(sys.argv[1], 'r', encoding='utf-8') as red:
    data = red.read()

def counter(compd, early= False, merge = None):
    outp = {}
    for mi in compd.finditer(data):
        m = mi.group()
        if m not in outp:
            outp[m] = 0
        outp[m] += 1

    if merge:
        p = {**outp, **merge}
        outp = p

    if early:
        return outp

    j = []
    for i in outp:
        j.append((i, outp[i]))

    outp = sorted(j, key = lambda x: x[1], reverse = True)
    
    return outp

def lens(compd):
    return len(compd.findall(data))

# Arranging the dates
days = counter(date)
fp = open('days.txt', 'w')
print('mm/dd/yy -> no. of messages(descending order)', file=fp)
for day in days:
    print(day[0], '->', day[1], file = fp)
fp.close()


# Arranging the users
ussr = counter(phno, early=True)
kusers = counter(cont, merge=ussr)

print(dir(path))
users = kusers

fp = open('users.txt', 'w')
print('Member -> no. of messages(descending order)', file=fp)
for user in users:
    print(user[0], '->', user[1], file = fp)
fp.close()

# Joined and left stats
joins = lens(jond)
adds = lens(addd)
leaves = lens(left)
isko = lens(icon)

with open('stats.txt', 'w') as wir:
    wir.write(f"No of users joined: {joins}\n")
    wir.write(f"No of users added: {adds}\n")
    wir.write(f"No of users who left: {leaves}\n")
    wir.write(f"No of times group logo was changed: {isko}\n")
    

# Showing the changes in group names
fp = open('subj.txt', 'wb')
fp.write("Old subject -> New subject\n".encode())
for m in subj.finditer(data):
    fp.write(f"{m[4]} -> {m[5]}".encode('utf-8'))
    fp.write("\n".encode())
fp.close()

with open('final.txt', 'w') as wir:
    with open('days.txt') as red:
        data = red.readlines()[:7]
    wir.writelines(data); wir.write('\n')
    with open('users.txt') as red:
        data = red.readlines()[:7]
    wir.writelines(data); wir.write('\n')
    with open('stats.txt') as red:
        data = red.readlines()[:7]
    wir.writelines(data); wir.write('\n')
