import csv
import sqlite3


ethnic_group = []
age = []
status = []
number_pregnancy = []

ethnic_group_2 = []
got_health_education = []
number_health_education = []

with open('young_pregnancy.csv') as csv_file:
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
                status.append(row[3])
                number_pregnancy.append(row[6])
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
                got_health_education.append(row[3])
                number_health_education.append(row[6])
            line_count += 1


conn = sqlite3.connect('health.db')
c = conn.cursor()

c.execute("DROP TABLE young_pregnancy")
c.execute("CREATE TABLE young_pregnancy(ethnic_group, age, pregnancy, count)")
i=0
for data in ethnic_group:
    c.execute("INSERT INTO young_pregnancy VALUES (?,?,?,?)", (ethnic_group[i], age[i], status[i], number_pregnancy[i]))
    i+=1
    if i%5==0:
        conn.commit()

c.execute("DROP TABLE health_education")
c.execute("CREATE TABLE health_education(ethnic_group, got_health_education, count)")

i=0
for data in ethnic_group_2:
    c.execute("INSERT INTO health_education VALUES (?,?,?)", (ethnic_group_2[i], got_health_education[i], number_health_education[i]))
    i+=1
    if i%5==0:
        conn.commit()


total_groups = []

r = c.execute("SELECT ethnic_group FROM young_pregnancy")

for t in r:
    if t[0] not in total_groups:
        total_groups.append(t[0])

print(total_groups)

ethnic_group_3 = []
percent_pregnant = []
percent_received_health_education = []

for group in total_groups:
    print(group)
    count_yes = 0
    count_no = 0
    r = c.execute("SELECT pregnancy, count FROM young_pregnancy WHERE pregnancy='Yes' and age='Age 21' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_yes = int(re[1])
        else:
            count_yes = 5
        #print(count_yes)

    r = c.execute("SELECT pregnancy, count FROM young_pregnancy WHERE pregnancy='No' and age='Age 21' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_no = int(re[1])
        else:
            count_no = 5
        #print(count_no)

    a_yes = 0
    a_no = 0
    r = c.execute("SELECT got_health_education, count FROM health_education WHERE got_health_education='Yes' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_yes = int(re[1])
        else:
            a_yes = 5
        #print(a_yes)

    r = c.execute("SELECT got_health_education, count FROM health_education WHERE got_health_education='No' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_no = int(re[1])
        else:
            a_no = 5
        #print(a_no)

    ethnic_group_3.append(group)
    percent_pregnant.append((count_yes/(count_yes+count_no))*100)
    percent_received_health_education.append((a_yes/(a_yes+a_no))*100)

print(ethnic_group_3)
print(percent_pregnant)
print(percent_received_health_education)
