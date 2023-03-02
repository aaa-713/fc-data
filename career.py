import csv
import sqlite3


ethnic_group = []
age = []
status = []
number_employed = []

ethnic_group_2 = []
got_services = []
number_services = []

with open('employment.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if row[1]=='United States' and row[5]=='Number' and row[3]!='Declined or Blank' and row[2]!='Unknown' and row[2]!='Total':
                ethnic_group.append(row[2])
                age.append(row[4])
                status.append(row[3])
                number_employed.append(row[6])
            line_count += 1


with open('career_prep_services.csv') as csv_file:
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
                got_services.append(row[3])
                number_services.append(row[6])
            line_count += 1


conn = sqlite3.connect('career.db')
c = conn.cursor()

c.execute("DROP TABLE employment")
c.execute("CREATE TABLE employment(ethnic_group, age, employment_status, count)")
i=0
for data in ethnic_group:
    c.execute("INSERT INTO employment VALUES (?,?,?,?)", (ethnic_group[i], age[i], status[i], number_employed[i]))
    i+=1
    if i%5==0:
        conn.commit()

c.execute("DROP TABLE career_services")
c.execute("CREATE TABLE career_services(ethnic_group, got_services, count)")

i=0
for data in ethnic_group_2:
    c.execute("INSERT INTO career_services VALUES (?,?,?)", (ethnic_group_2[i], got_services[i], number_services[i]))
    i+=1
    if i%5==0:
        conn.commit()


total_groups = []

r = c.execute("SELECT ethnic_group FROM employment")

for t in r:
    if t[0] not in total_groups:
        total_groups.append(t[0])

print(total_groups)

ethnic_group_3 = []
percent_employed = []
percent_received_services = []

for group in total_groups:
    print(group)
    count_yes = 0
    count_no = 0
    r = c.execute("SELECT employment_status, count FROM employment WHERE age='Age 21' and employment_status='Yes' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_yes = int(re[1])
        else:
            count_yes = 5
        #print(count_yes)

    r = c.execute("SELECT employment_status, count FROM employment WHERE age='Age 21' and employment_status='No' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_no = int(re[1])
        else:
            count_no = 5
        #print(count_no)

    a_yes = 0
    a_no = 0
    r = c.execute("SELECT got_services, count FROM career_services WHERE got_services='Yes' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_yes = int(re[1])
        else:
            a_yes = 5
        #print(a_yes)

    r = c.execute("SELECT got_services, count FROM career_services WHERE got_services='No' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_no = int(re[1])
        else:
            a_no = 5
        #print(a_no)

    ethnic_group_3.append(group)
    percent_employed.append((count_yes/(count_yes+count_no))*100)
    percent_received_services.append((a_yes/(a_yes+a_no))*100)

print(ethnic_group_3)
print(percent_employed)
print(percent_received_services)
