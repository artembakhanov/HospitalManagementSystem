-- Written by Artem Bakhanov

WITH p_id AS (
        SELECT patient_id
        FROM general_user NATURAL JOIN patient
	    WHERE email = 'mbates@bullock.com'
     ),
	dt_id AS (
	SELECT doctor_team_id
	FROM
		appointment
	WHERE
		start_time = (
			SELECT MAX(start_time)
			FROM appointment
			WHERE patient_id=(SELECT patient_id FROM p_id)
			)
		AND
		patient_id = (SELECT patient_id FROM p_id)
)
SELECT fname, lname
FROM
	doctor_team NATURAL JOIN doctor NATURAL JOIN working_staff NATURAL JOIN general_user
WHERE
	doctor_team_id = (SELECT doctor_team_id FROM dt_id)
		AND
		(
            (fname SIMILAR TO '(L|M)%' AND lname NOT SIMILAR TO '(L|M)%') OR
            (fname NOT SIMILAR TO '(L|M)%' AND lname SIMILAR TO '(L|M)%')
		);
