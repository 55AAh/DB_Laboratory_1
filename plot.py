import cx_Oracle
import chart_studio.plotly as py
import plotly.graph_objects as go
import re
import chart_studio.dashboard_objs as dashboard

def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')

db_conn = cx_Oracle.connect(user="kostia", password="my_password")
db_cur = db_conn.cursor()


# Запит 1 - Вивести кількість неодружених техніків 1-го розряду в кожній компанії
print("\tTask 1", flush=True)
fig1_x = []
fig1_y = []
print("Quering db...", end="", flush=True)
for row in db_cur.execute("""
SELECT
    rec_source, COUNT(*) as count
FROM RecruitmentSource
    JOIN Employee ON Employee.rec_source_id = RecruitmentSource.rec_source_id
    JOIN MaritalStatus ON MaritalStatus.marital_status_id = Employee.marital_status_id
    JOIN EmploymentPosition ON EmploymentPosition.employment_position_id = Employee.employment_position_id 
WHERE
    marital_status_desc != 'Married'
    AND employment_position = 'Production Technician I'
GROUP BY
    rec_source"""):
    fig1_x.append(row[0])
    fig1_y.append(row[1])
print(" Done", flush=True)
print("Creating figure...", end="", flush=True)
fig1 = go.Figure(data=go.Bar(x=fig1_x, y=fig1_y), layout=go.Layout(
    xaxis=dict(
        title = "Компанії"
    ),
    yaxis=dict(
        title = "Кількість техніків"
    )
))
print(" Done", flush=True)
print("Plotting figure...", end="", flush=True)
plot1_url = py.plot(fig1, filename="DB_Laboratory_1_plot1")
print(" Done", flush=True)


# Запит 2 - Вивести імена п'яти менеджерів, у яких звільнилося найбільше низькооплачуваних робітників з Массачусетсу, разом з відповідною кількістю
print("\tTask 2", flush=True)
fig2_values = []
fig2_labels = []
print("Quering db...", end="", flush=True)
for row in db_cur.execute("""
SELECT manager_name, count FROM(
    SELECT
        manager_name, COUNT(*) AS count
    FROM ManagerInfo
        JOIN Employee ON Employee.Manager_id = ManagerInfo.manager_id
        JOIN EmployeeTerminated ON EmployeeTerminated.employee_id = Employee.employee_id
        JOIN TerminationStatus ON EmployeeTerminated.termination_status_id = TerminationStatus.termination_status_id
        JOIN ZipCode ON Employee.zip_code = ZipCode.zip_code
        JOIN StateInfo ON StateInfo.state_id = ZipCode.state_id
    WHERE
        termination_reason = 'more money'
        AND state_name = 'MA'
    GROUP BY
        manager_name
    ORDER BY
        count DESC
)
WHERE
    ROWNUM <= 5"""):
    fig2_labels.append(row[0])
    fig2_values.append(row[1])
print(" Done", flush=True)
print("Creating figure...", end="", flush=True)
fig2 = go.Figure(data=go.Pie(values=fig2_values, labels=fig2_labels))
print(" Done", flush=True)
print("Plotting figure...", end="", flush=True)
plot2_url = py.plot(fig2, filename="DB_Laboratory_1_plot2")
print(" Done", flush=True)


# Запит 3 - Вивести середній рівень задоволення активно працюючих професіоналів в кожному департаменті всіх компаній
print("\tTask 3", flush=True)
fig3_x = []
fig3_y = []
print("Quering db...", end="", flush=True)
for row in db_cur.execute("""
SELECT
    department, ROUND(AVG(employee_satisfaction), 1) AS avg_level
FROM Department
    JOIN Employee ON Employee.department_id = Department.department_id
    JOIN EmploymentStatus ON EmploymentStatus.employment_status_id = Employee.employment_status_id
    JOIN PerformanceScore ON PerformanceScore.perf_score_id = Employee.perf_score_id
    JOIN RecruitmentSource ON RecruitmentSource.rec_source_id = Employee.rec_source_id
WHERE
    employment_status = 'Active'
    AND (perf_score = 'Fully Meets' OR perf_score = 'Exceeds')
GROUP BY
    department
ORDER BY
    avg_level DESC"""):
    fig3_x.append(row[0])
    fig3_y.append(row[1])
print(" Done", flush=True)
print("Creating figure...", end="", flush=True)
fig3 = go.Figure(data=go.Bar(x=fig3_x, y=fig3_y), layout=go.Layout(
    xaxis = dict(
        title = "Департамент"
    ),
    yaxis = dict(
        title = "Рівень задоволення"
    )
))
print(" Done", flush=True)
print("Plotting figure...", end="", flush=True)
plot3_url = py.plot(fig3, filename="DB_Laboratory_1_plot3")
print(" Done", flush=True)


print("Assembling dashboard...", end="", flush=True)
my_dboard = dashboard.Dashboard()

plot1_id = fileId_from_url(plot1_url)
plot2_id = fileId_from_url(plot2_url)
plot3_id = fileId_from_url(plot3_url)
box_1 = {
    "type": "box",
    "boxType": "plot",
    "fileId": plot1_id,
    "title": "Кількість неодружених техніків 1-го розряду"
}
box_2 = {
    "type": "box",
    "boxType": "plot",
    "fileId": plot2_id,
    "title": "Топ-5 менеджерів, у яких звільнилося найбільше низькооплачуваних робітників з Массачусетсу"
}
box_3 = {
    "type": "box",
    "boxType": "plot",
    "fileId": plot3_id,
    "title": "Рівень задоволення активно працюючих професіоналів"
}
my_dboard.insert(box_1)
my_dboard.insert(box_2, "below", 1)
my_dboard.insert(box_3, "left", 2)
py.dashboard_ops.upload(my_dboard, "DB_Laboratory_1")
print(" Done", flush=True)
