SELECT doctor_team_id
FROM
	appointment
NATURAL JOIN
    patient
NATURAL JOIN
   doctor_team
NATURAL JOIN
   doctor
WHERE
	start_time = (
		SELECT MAX(start_time)
		FROM appointment
		WHERE patient_id=31
		)
	AND
	patient_id = 31;
