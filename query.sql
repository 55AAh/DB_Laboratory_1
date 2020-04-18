--	Запит 1 - Вивести кількість неодружених техніків 1-го розряду в кожній компанії

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
    rec_source;



--	Запит 2 - Вивести імена п'яти менеджерів, у яких звільнилося найбільше низькооплачуваних робітників з Массачусетсу, разом з відповідною кількістю

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
    ROWNUM <= 5;



--	Запит 3 - Вивести середній рівень задоволення активно працюючих професіоналів в кожному департаменті всіх компаній

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
    avg_level DESC;