DROP TABLE TerminationStatus CASCADE CONSTRAINTS;
DROP TABLE EmployeeTerminated CASCADE CONSTRAINTS;
DROP TABLE EmploymentStatus CASCADE CONSTRAINTS;
DROP TABLE EmploymentPosition CASCADE CONSTRAINTS;
DROP TABLE ManagerInfo CASCADE CONSTRAINTS;
DROP TABLE RecruitmentSource CASCADE CONSTRAINTS;
DROP TABLE PerformanceScore CASCADE CONSTRAINTS;
DROP TABLE StateInfo CASCADE CONSTRAINTS;
DROP TABLE ZipCode CASCADE CONSTRAINTS;
DROP TABLE MaritalStatus CASCADE CONSTRAINTS;
DROP TABLE Department CASCADE CONSTRAINTS;
DROP TABLE Employee CASCADE CONSTRAINTS;

CREATE TABLE TerminationStatus(
    termination_status_id  NUMBER PRIMARY KEY
,   termination_reason     VARCHAR(40) NOT NULL
);

CREATE TABLE EmployeeTerminated(
    employee_id             NUMBER PRIMARY KEY
,   termination_status_id   NUMBER NOT NULL
,   termination_date        DATE
);

CREATE TABLE EmploymentStatus(
    employment_status_id    NUMBER PRIMARY KEY
,   employment_status       VARCHAR(30) NOT NULL
);

CREATE TABLE EmploymentPosition(
    employment_position_id  NUMBER PRIMARY KEY
,   employment_position     VARCHAR(30) NOT NULL
);

CREATE TABLE ManagerInfo(
    manager_id              NUMBER PRIMARY KEY
,   manager_name            VARCHAR(30) NOT NULL
);

CREATE TABLE RecruitmentSource(
    rec_source_id           NUMBER PRIMARY KEY
,   rec_source              VARCHAR(40) NOT NULL
);

CREATE TABLE PerformanceScore(
    perf_score_id           NUMBER PRIMARY KEY
,   perf_score              VARCHAR(30) NOT NULL
);

CREATE TABLE StateInfo(
    state_id                NUMBER PRIMARY KEY
,   state_name              VARCHAR(30) NOT NULL
);

CREATE TABLE ZipCode(
    zip_code                NUMBER PRIMARY KEY
,   state_id                NUMBER NOT NULL
);

CREATE TABLE MaritalStatus(
    marital_status_id       NUMBER PRIMARY KEY
,   marital_status_desc     VARCHAR(30) NOT NULL
);

CREATE TABLE Department(
    department_id           NUMBER PRIMARY KEY
,   department              VARCHAR(30) NOT NULL
);

CREATE TABLE Employee(
    employee_id             NUMBER PRIMARY KEY
,   employment_status_id    NUMBER
,   employment_position_id  NUMBER NOT NULL
,   manager_id              NUMBER NOT NULL
,   rec_source_id           NUMBER NOT NULL
,   perf_score_id           NUMBER NOT NULL
,   zip_code                NUMBER NOT NULL
,   marital_status_id       NUMBER NOT NULL
,   department_id           NUMBER NOT NULL
,   employee_satisfaction   NUMBER NOT NULL
);

ALTER TABLE EmployeeTerminated ADD CONSTRAINT
    EmployeeTerminatedFK_emp_id FOREIGN KEY (employee_id) REFERENCES Employee(employee_id);
ALTER TABLE EmployeeTerminated ADD CONSTRAINT
    EmployeeTerminatedFK_stat_id FOREIGN KEY (termination_status_id) REFERENCES TerminationStatus(termination_status_id);

ALTER TABLE ZipCode ADD CONSTRAINT
    ZipCodeFK_state_id FOREIGN KEY (state_id) REFERENCES StateInfo(state_id);

ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_emp_stat_id FOREIGN KEY (employment_status_id) REFERENCES EmploymentStatus(employment_status_id);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_emp_pos_id FOREIGN KEY (employment_position_id) REFERENCES EmploymentPosition(employment_position_id);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_man_id FOREIGN KEY (manager_id) REFERENCES ManagerInfo(manager_id);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_rec_src_id FOREIGN KEY (rec_source_id) REFERENCES RecruitmentSource(rec_source_id);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_perf_scr_id FOREIGN KEY (perf_score_id) REFERENCES PerformanceScore(perf_score_id);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_zipcode FOREIGN KEY (zip_code) REFERENCES ZipCode(zip_code);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_mrt_stat_id FOREIGN KEY (marital_status_id) REFERENCES MaritalStatus(marital_status_id);
ALTER TABLE Employee ADD CONSTRAINT
    EmployeeFK_dept_id FOREIGN KEY (department_id) REFERENCES Department(department_id);