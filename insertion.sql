INSERT INTO NOTIFICATION (Notification_time, Title, Content, User_id) VALUES('2015-06-04 17:30:00', 'Upcoming appointment', 'Do not forget that you have appointment 1492 in room 3.', 8);
INSERT INTO NOTIFICATION (Notification_time, Title, Content, User_id) VALUES('2015-06-04 17:30:00', 'Upcoming appointment', 'Do not forget that you have appointment 1492 in room 3.', 100);
INSERT INTO INVOICE_BILL (Invoice_date, Price, Created_by, Is_paid) VALUES('2015-06-04 18:00:00', 100, 8, False);
INSERT INTO APPOINTMENT (Room, Type, Start_time, End_time, Patient_id, Doctor_team_id, Invoice_bill_id) VALUES( 3, 1, '2015-06-04 17:45:00', '2015-06-04 18:00:00', 100, 10, 1492);
INSERT INTO MEDICAL_RECORD (Description, Med_rec_date, Appointment_id, Created_by) VALUES('Medical record description 871.', '2015-06-04 18:00:00', 1492, 10);
