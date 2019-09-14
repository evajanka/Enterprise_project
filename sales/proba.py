
header = ["hétfő", "kedd", "szerda", "csütörtök", "péntek"]
table = ["12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:30", "18:00", "18:30", "19:00"]


lens = [len(day) for day in header]
maxlen = max(lens)
cell = " "*maxlen
row = [cell*5]
head = ("|"+'|'.join(header)+"|")
print(head)
print ("-"*len(head))
i = 0
row = [table[i], " "*5]
for hour in table:
    print(hour + "|".join(row))
    i += 1



students = {"barnus": [("hétfő", "12:00", "17:00"), ("kedd", "13:30", "15:30"), ("c", "15:00", "16:00")],
            "réka": [("szerda","16:30", "17:30")],
            "janka": [("kedd", "16:00", "17:30"), ("hétfő", "13:00", "15:00")] }

