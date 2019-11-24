SELECT *
FROM
	appointment
WHERE
	start_time = (
		SELECT MAX(start_time)
		FROM appointment
		WHERE patient_id=31
		)
	AND
	patient_id = 31;
