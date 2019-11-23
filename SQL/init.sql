CREATE TABLE GENERAL_USER (
    User_id SERIAL UNIQUE,
    Email VARCHAR(50) NOT NULL UNIQUE,
    Fname VARCHAR(25) NOT NULL,
    Lname VARCHAR(25) NOT NULL,
    Mname VARCHAR(25) NOT NULL,
    Gender VARCHAR(1) NOT NULL,
    /*
    m - MALE
    f - FEMALE
    o - OTHER
    */
    Birth_date DATE NOT NULL, --YYYY-mm-dd
    Address VARCHAR(50) NOT NULL,
    Role INTEGER NOT NULL,
    /*
    0 - USER
    1 - PATIENT
    2 - WORKING_STAFF
    4 - NURSE
    8 - DOCTOR
    16 - ACCOUNTANT
    32 - PHARMACIST
    64 - CANTEEN_STAFF
    128 - ADMIN
    */
    Password_hash VARCHAR(48) NOT NULL,
    PRIMARY KEY (User_id)
);

CREATE TABLE MESSAGE (
    Message_id SERIAL UNIQUE,
    Message_time TIMESTAMP WITH TIME ZONE NOT NULL, -- 'YYYY-MM-DD HH-MM-SS'
    Content VARCHAR(500),
    Sender_email INTEGER REFERENCES GENERAL_USER(User_id),
    Receiver_email INTEGER REFERENCES GENERAL_USER(User_id),
    PRIMARY KEY (Message_id)
);

CREATE TABLE NOTIFICATION (
    Notification_id SERIAL UNIQUE,
    Notification_time TIMESTAMP WITH TIME ZONE NOT NULL, -- 'YYYY-MM-DD HH-MM-SS'
    Title VARCHAR(50),
    Content VARCHAR(500),
    User_id INTEGER REFERENCES GENERAL_USER(User_id),
    PRIMARY KEY (Notification_id)
);

CREATE TABLE WORKING_STAFF (
    User_id INTEGER REFERENCES GENERAL_USER(User_id),
    Salary INTEGER NOT NULL,
    Qualification VARCHAR(30) NOT NULL,
    W_staff_id SERIAL UNIQUE,
    PRIMARY KEY (W_staff_id)
);

CREATE TABLE SCHEDULE (
    Schedule_id SERIAL UNIQUE,
    Week_day INTEGER NOT NULL,
    Start_time TIME NOT NULL,
    End_time TIME NOT NULL,
    PRIMARY KEY (Schedule_id)
);

CREATE TABLE STAFF_SCHEDULE (
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    Schedule_id INTEGER REFERENCES SCHEDULE (Schedule_id),
    PRIMARY KEY(W_staff_id, Schedule_id)
);

CREATE TABLE PATIENT (
    User_id INTEGER REFERENCES GENERAL_USER(User_id),
    Patient_id SERIAL UNIQUE,
    PRIMARY KEY (Patient_id)
);

CREATE TABLE TIME_SLOT (
    Time_slot_id SERIAL UNIQUE,
    Day VARCHAR(15) NOT NULL,
    Start_time TIME NOT NULL,
    End_time TIME NOT NULL,
    PRIMARY KEY (Time_slot_id)
);

CREATE TABLE ACCOUNTANT (
    Acc_id SERIAL UNIQUE,
    License_id INTEGER NOT NULL,
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    PRIMARY KEY (Acc_id)
);

CREATE TABLE INVOICE_BILL (
    Invoice_bill_id SERIAL UNIQUE,
    Invoice_date DATE NOT NULL,
    Price INTEGER NOT NULL,
    Created_by INTEGER REFERENCES ACCOUNTANT(Acc_id),
    Is_paid BOOLEAN NOT NULL,
    PRIMARY KEY (Invoice_bill_id)
);

CREATE TABLE PHARMACIST (
    Pharm_id SERIAL UNIQUE,
    Licence_id INTEGER NOT NULL,
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    PRIMARY KEY (Pharm_id)
);

CREATE TABLE MEDICAL_SUPPLY (
    Med_supply_id SERIAL UNIQUE,
    Name VARCHAR(30) NOT NULL,
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (Med_supply_id)
);

CREATE TABLE MED_SUPPLY_ORDER (
    Pharmacist_id INTEGER REFERENCES PHARMACIST(Pharm_id),
    Med_supply_id INTEGER REFERENCES MEDICAL_SUPPLY(Med_supply_id),
    Order_time TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (Pharmacist_id, Med_supply_id, Order_time)
);

CREATE TABLE ADMIN (
    Admin_id SERIAL UNIQUE,
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    PRIMARY KEY (Admin_id)
);

CREATE TABLE BLOCKED (
  User_id INTEGER REFERENCES GENERAL_USER(User_id),
  Admin_id INTEGER REFERENCES ADMIN(Admin_id)
);

CREATE TABLE NOTICE (
    Notice_id SERIAL UNIQUE,
    Title VARCHAR(50),
    Content VARCHAR(500),
    Notice_time TIMESTAMP WITH TIME ZONE NOT NULL,
    Posted_by INTEGER REFERENCES ADMIN(Admin_id),
    PRIMARY KEY (Notice_id)
);

CREATE TABLE CANTEEN_STAFF (
    Cant_id SERIAL UNIQUE,
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    PRIMARY KEY (Cant_id)
);

CREATE TABLE MENU (
    Menu_id SERIAL UNIQUE,
    Menu_date DATE NOT NULL,
    Type VARCHAR(30) NOT NULL,
    Published_by INTEGER REFERENCES ADMIN(Admin_id),
    PRIMARY KEY (Menu_id)
);

CREATE TABLE DISH (
    Dish_id SERIAL UNIQUE,
    Name VARCHAR(30) NOT NULL,
    Energy_value INTEGER NOT NULL,
    Components VARCHAR(60) NOT NULL,
    PRIMARY KEY (Dish_id)
);

CREATE TABLE DISH_IN_MENU (
    Menu_id INTEGER REFERENCES MENU(Menu_id),
    Dish_id INTEGER REFERENCES DISH(Dish_id),
    PRIMARY KEY (Menu_id, Dish_id)
);

CREATE TABLE DOCTOR (
    Doc_id SERIAL UNIQUE,
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    Room INTEGER,
    PRIMARY KEY (Doc_id)
);

CREATE TABLE DOCTOR_TEAM (
    Doctor_team_id SERIAL UNIQUE,
    Doc_id INTEGER REFERENCES DOCTOR(Doc_id),
    PRIMARY KEY (Doctor_team_id)
);

CREATE TABLE NURSE (
    Nurse_id SERIAL UNIQUE,
    W_staff_id INTEGER REFERENCES WORKING_STAFF(W_staff_id),
    Doctor_team_id INTEGER REFERENCES DOCTOR_TEAM(Doctor_team_id),
    PRIMARY KEY (Nurse_id)
);

CREATE TABLE NURSE_TASK (
    Task_id SERIAL UNIQUE,
    Importance_level INTEGER NOT NULL,
    Description VARCHAR(200) NOT NULL,
    doc_id INTEGER REFERENCES DOCTOR(Doc_id),
    Nurse_id INTEGER REFERENCES NURSE(Nurse_id),
    Is_completed BOOLEAN,
    Start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    Deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (Task_id)
);

CREATE TABLE APPOINTMENT (
    Appointment_id SERIAL UNIQUE,
    Room INTEGER NOT NULL,
    Type INTEGER NOT NULL,
    Start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    End_time TIMESTAMP WITH TIME ZONE NOT NULL,
    Patient_id INTEGER REFERENCES PATIENT(Patient_id),
    Doctor_team_id INTEGER REFERENCES DOCTOR_TEAM(Doctor_team_id),
    Invoice_bill_id INTEGER REFERENCES INVOICE_BILL(Invoice_bill_id),
    PRIMARY KEY (Appointment_id)
);

CREATE TABLE MEDICAL_RECORD (
    Med_rec_id SERIAL UNIQUE,
    Description VARCHAR(500) NOT NULL,
    Med_rec_date DATE NOT NULL,
    Appointment_id INTEGER REFERENCES APPOINTMENT(Appointment_id),
    Created_by INTEGER REFERENCES DOCTOR_TEAM(Doctor_team_id),
    PRIMARY KEY(Med_rec_id)
);

CREATE TABLE PRESCRIPTION (
    Prescription_id SERIAL UNIQUE,
    Medicals VARCHAR(50) NOT NULL,
    Med_rec_id INTEGER REFERENCES MEDICAL_RECORD(Med_rec_id),
    PRIMARY KEY (Prescription_id)
);
