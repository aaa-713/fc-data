import csv
import sqlite3


ethnic_group = []
age = []
in_school = []
number_enrollment = []

ethnic_group_2 = []
got_assisstance = []
number_assisstance = []

with open('school_enrollment.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if row[1]=='United States' and row[5]=='Number' and row[3]!='Declined' and row[2]!='Unknown' and row[3]!='blank' and row[2]!='Total':
                ethnic_group.append(row[2])
                age.append(row[4])
                in_school.append(row[3])
                number_enrollment.append(row[6])
            line_count += 1


with open('financial_education_assisstance.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if row[1]=='United States' and row[5]=='Number' and row[2]!='blank' and row[3] != 'Unknown' and row[3]!= 'Total' and row[4]=='FY 2018':
                print(row)
                ethnic_group_2.append(row[3])
                got_assisstance.append(row[2])
                number_assisstance.append(row[6])
            line_count += 1


conn = sqlite3.connect('education.db')
c = conn.cursor()

c.execute("DROP TABLE enrollment")
c.execute("CREATE TABLE enrollment(ethnic_group, age, enrollment_status, count)")
i=0
for data in ethnic_group:
    c.execute("INSERT INTO enrollment VALUES (?,?,?,?)", (ethnic_group[i], age[i], in_school[i], number_enrollment[i]))
    i+=1
    if i%5==0:
        conn.commit()

c.execute("DROP TABLE ed_assisstance")
c.execute("CREATE TABLE ed_assisstance(ethnic_group, assisstance_status, count)")

i=0
for data in ethnic_group_2:
    c.execute("INSERT INTO ed_assisstance VALUES (?,?,?)", (ethnic_group_2[i], got_assisstance[i], number_assisstance[i]))
    i+=1
    if i%5==0:
        conn.commit()


#result = c.execute("SELECT * FROM enrollment")
#print(result.fetchall())
#
# result = c.execute("SELECT ethnic_group FROM ed_assisstance")
# print(result.fetchall())
total_groups = []

r = c.execute("SELECT ethnic_group FROM enrollment")
for t in r:
    if t[0] not in total_groups:
        total_groups.append(t[0])

print(total_groups)

ethnic_group_3 = []
percent_enrolled = []
percent_received_assisstance = []

for group in total_groups:
    print(group)
    count_yes = 0
    count_no = 0
    r = c.execute("SELECT enrollment_status, count FROM enrollment WHERE age='Age 21' and enrollment_status='Yes' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_yes = int(re[1])
        else:
            count_yes = 5
        #print(count_yes)

    r = c.execute("SELECT enrollment_status, count FROM enrollment WHERE age='Age 21' and enrollment_status='No' and ethnic_group=?;",[group])
    for re in r:
    #     print(re)
        if re[1] !='S':
            count_no = int(re[1])
        else:
            count_no = 5
        #print(count_no)

    a_yes = 0
    a_no = 0
    r = c.execute("SELECT assisstance_status, count FROM ed_assisstance WHERE assisstance_status='Yes' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_yes = int(re[1])
        else:
            a_yes = 5
        #print(a_yes)

    r = c.execute("SELECT assisstance_status, count FROM ed_assisstance WHERE assisstance_status='No' and ethnic_group=?;",[group])
    for re in r:
        #print(re)
        if re[1] !='S':
            a_no = int(re[1])
        else:
            a_no = 5
        #print(a_no)

    ethnic_group_3.append(group)
    percent_enrolled.append((count_yes/(count_yes+count_no))*100)
    percent_received_assisstance.append((a_yes/(a_yes+a_no))*100)

print(ethnic_group_3)
print(percent_enrolled)
print(percent_received_assisstance)
