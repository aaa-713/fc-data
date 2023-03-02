import csv
import sqlite3


ethnic_group = []
age = []
incarceration_status = []
count = []

ethnic_group_2 = []
got_mentoring = []
number_mentoring = []

with open('incarceration.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if row[1]=='United States' and row[5]=='Number' and row[3]!='Declined' and row[3]!='blank' and row[2]!='Unknown' and row[2]!='Total':
                ethnic_group.append(row[2])
                age.append(row[4])
                incarceration_status.append(row[3])
                count.append(row[6])
            line_count += 1


with open('health_education.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if row[1]=='United States' and row[5]=='Number' and row[3]!='blank' and row[2] != 'Unknown' and row[2]!= 'Total' and row[4]=='FY 2018':
                #print(row)
                ethnic_group_2.append(row[2])
                got_mentoring.append(row[3])
                number_mentoring.append(row[6])
            line_count += 1


conn = sqlite3.connect('incarceration.db')
c = conn.cursor()

c.execute("DROP TABLE incarceration")
c.execute("CREATE TABLE incarceration(ethnic_group, age, status, count)")
i=0
for data in ethnic_group:
    c.execute("INSERT INTO incarceration VALUES (?,?,?,?)", (ethnic_group[i], age[i], incarceration_status[i], count[i]))
    i+=1
    if i%5==0:
        conn.commit()

c.execute("DROP TABLE mentoring_services")
c.execute("CREATE TABLE mentoring_services(ethnic_group, got_mentoring, count)")

i=0
for data in ethnic_group_2:
    c.execute("INSERT INTO mentoring_services VALUES (?,?,?)", (ethnic_group_2[i], got_mentoring[i], number_mentoring[i]))
    i+=1
    if i%5==0:
        conn.commit()


total_groups = []

r = c.execute("SELECT ethnic_group FROM incarceration")

for t in r:
    if t[0] not in total_groups:
        total_groups.append(t[0])

print(total_groups)

ethnic_group_3 = []
percent_incarcerated = []
percent_received_mentoring = []

for group in total_groups:
    print(group)
    count_yes = 0
    count_no = 0
    r = c.execute("SELECT status, count FROM incarceration WHERE status='Yes' and age='Age 19' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_yes = int(re[1])
        else:
            count_yes = 5
        #print(count_yes)

    r = c.execute("SELECT status, count FROM incarceration WHERE status='No' and age='Age 19' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_no = int(re[1])
        else:
            count_no = 5
        #print(count_no)

    a_yes = 0
    a_no = 0
    r = c.execute("SELECT got_mentoring, count FROM mentoring_services WHERE got_mentoring='Yes' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_yes = int(re[1])
        else:
            a_yes = 5
        #print(a_yes)

    r = c.execute("SELECT got_mentoring, count FROM mentoring_services WHERE got_mentoring='No' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_no = int(re[1])
        else:
            a_no = 5
        #print(a_no)

    ethnic_group_3.append(group)
    percent_incarcerated.append((count_yes/(count_yes+count_no))*100)
    percent_received_mentoring.append((a_yes/(a_yes+a_no))*100)

print(ethnic_group_3)
print(percent_incarcerated)
print(percent_received_mentoring)
