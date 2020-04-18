def parse_line(line):
    line.replace('""', '')
    if line[0] == '"' and line[-1] == '"':
        line = line[1:-1]
    if line=="" or line[:2]==",,":
        return None
    line_sp = line.split(",")
    try:
        _ = int(line_sp[1])
    except ValueError:
        line_sp[0] += line_sp[1]
        del line_sp[1]
    if line_sp[23]=="\"\"no-call":
        del line_sp[24]
        line_sp[23] = "no-call, no-show"
    return line_sp

TerminationStatus = dict()
TerminationStatusIND = 0
EmployeeTerminated = dict()
EmploymentStatus = dict()
EmploymentPosition = dict()
ManagerInfo = dict()
ManagerInfoIND = 0
RecruitmentSource = dict()
RecruitmentSourceIND = 0
PerformanceScore = dict()
ZipCode = dict()
StateInfo = dict()
StateInfoIND = 0
MaritalStatus = dict()
Department = dict()
Employee = dict()

with open("HRDataset_v13.csv") as file:
    for line in file.readlines()[1:]:
        record = parse_line(line.strip())
        if record is None:
            continue
        employee_name = record[0]
        employee_id = record[1]
        married_id = record[2]
        marital_status_id = record[3]
        gender_id = record[4]
        employment_status_id = record[5]
        dept_id = record[6]
        perf_score_id = record[7]
        from_diversity_job_fair = record[8]
        pay_rate = record[9]
        term_d = record[10]
        position_id = record[11]
        position = record[12]
        state = record[13]
        zipcode = record[14]
        birth_date = record[15]
        sex = record[16]
        marital_status_desc = record[17]
        citizen_desc = record[18]
        hispanic_latino = record[19]
        race_desc = record[20]
        hire_date = record[21]
        term_date = record[22]
        term_reason = record[23]
        employment_status = record[24]
        department = record[25]
        manager_name = record[26]
        manager_id = record[27]
        recruitment_source = record[28]
        performance_score = record[29]
        engagement_survey = record[30]
        employee_satisfaction = record[31]
        special_projects_count = record[32]
        last_performance_review_date = record[33]
        days_late_last_30 = record[34]

        if term_d == "1":
            if term_reason == "":
                term_reason = "unknown"
            if term_reason not in [TerminationStatus[k] for k in TerminationStatus.keys()]:
                TerminationStatusIND += 1
                TerminationStatus[TerminationStatusIND] = term_reason
            for k in TerminationStatus.keys():
                if term_reason == TerminationStatus[k]:
                    EmployeeTerminated[int(employee_id)] = [k, term_date]
                    break
        
        EmploymentStatus[int(employment_status_id)] = employment_status
        
        EmploymentPosition[int(position_id)] = position
        
        if manager_name not in [ManagerInfo[k] for k in ManagerInfo.keys()]:
            ManagerInfoIND += 1
            ManagerInfo[ManagerInfoIND] = manager_name
            
        if recruitment_source not in [RecruitmentSource[k] for k in RecruitmentSource.keys()]:
            RecruitmentSourceIND += 1
            RecruitmentSource[RecruitmentSourceIND] = recruitment_source
            
        PerformanceScore[int(perf_score_id)] = performance_score
        
        if state not in [StateInfo[k] for k in StateInfo.keys()]:
            StateInfoIND += 1
            StateInfo[StateInfoIND] = state
            
        for k in StateInfo.keys():
            if StateInfo[k] == state:
                ZipCode[zipcode] = k
                break
            
        MaritalStatus[int(marital_status_id)] = marital_status_desc
        
        Department[int(dept_id)] = department

        Employee[int(employee_id)] = [
                [k for k in EmploymentStatus.keys() if EmploymentStatus[k]==employment_status][0],
                [k for k in EmploymentPosition.keys() if EmploymentPosition[k]==position][0],
                [k for k in ManagerInfo.keys() if ManagerInfo[k]==manager_name][0],
                [k for k in RecruitmentSource.keys() if RecruitmentSource[k]==recruitment_source][0],
                [k for k in PerformanceScore.keys() if PerformanceScore[k]==performance_score][0],
                [k for k in ZipCode.keys() if k==zipcode][0],
                [k for k in MaritalStatus.keys() if MaritalStatus[k]==marital_status_desc][0],
                [k for k in Department.keys() if Department[k]==department][0],
                employee_satisfaction
            ]

with open("populate.sql", "w") as script_file:
    script_file.write("""DELETE FROM Employee;
DELETE FROM EmployeeTerminated;
DELETE FROM TerminationStatus;
DELETE FROM EmploymentStatus;
DELETE FROM EmploymentPosition;
DELETE FROM ManagerInfo;
DELETE FROM RecruitmentSource;
DELETE FROM PerformanceScore;
DELETE FROM ZipCode;
DELETE FROM StateInfo;
DELETE FROM MaritalStatus;
DELETE FROM Department;\n\n""")
    
    for k in sorted(TerminationStatus.keys()):
        v=TerminationStatus[k]
        script_file.write("INSERT INTO TerminationStatus (termination_status_id, termination_reason) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(EmploymentStatus.keys()):
        v=EmploymentStatus[k]
        script_file.write("INSERT INTO EmploymentStatus (employment_status_id, employment_status) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(EmploymentPosition.keys()):
        v=EmploymentPosition[k]
        script_file.write("INSERT INTO EmploymentPosition (employment_position_id, employment_position) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(ManagerInfo.keys()):
        v=ManagerInfo[k]
        script_file.write("INSERT INTO ManagerInfo (manager_id, manager_name) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(RecruitmentSource.keys()):
        v=RecruitmentSource[k]
        script_file.write("INSERT INTO RecruitmentSource (rec_source_id, rec_source) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(PerformanceScore.keys()):
        v=PerformanceScore[k]
        script_file.write("INSERT INTO PerformanceScore (perf_score_id, perf_score) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(StateInfo.keys()):
        v=StateInfo[k]
        script_file.write("INSERT INTO StateInfo (state_id, state_name) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(ZipCode.keys()):
        v=ZipCode[k]
        script_file.write("INSERT INTO ZipCode (zip_code, state_id) VALUES ({0}, {1});\n".format(k,v))
    script_file.write("\n")

    for k in sorted(MaritalStatus.keys()):
        v=MaritalStatus[k]
        script_file.write("INSERT INTO MaritalStatus (marital_status_id, marital_status_desc) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(Department.keys()):
        v=Department[k]
        script_file.write("INSERT INTO Department (department_id, department) VALUES ({0}, '{1}');\n".format(k,v))
    script_file.write("\n")

    for k in sorted(Employee.keys()):
        v=Employee[k]
        script_file.write("INSERT INTO Employee (employee_id, employment_status_id, employment_position_id, manager_id, rec_source_id, perf_score_id, zip_code, marital_status_id, department_id, employee_satisfaction) VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});\n".format(k,v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8]))
    script_file.write("\n")

    for k in sorted(EmployeeTerminated.keys()):
        v=EmployeeTerminated[k]
        script_file.write("INSERT INTO EmployeeTerminated (employee_id, termination_status_id, termination_date) VALUES ({0}, {1}, TO_DATE('{2}', 'mm/dd/yy'));\n".format(k,v[0],v[1]))
    script_file.write("\n")
