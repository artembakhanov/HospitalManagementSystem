WITH
a1 AS (
	SELECT
		floor(extract( day from current_date - start_time) / 365) as yea,
		doc_id,
		COUNT(appointment_id) AS num
	FROM
		appointment NATURAL JOIN doctor_team NATURAL JOIN doctor
	WHERE
	    type = 1 AND
		start_time BETWEEN CURRENT_DATE - interval '3650 day' AND CURRENT_DATE
	GROUP BY
		yea, doc_id
	HAVING
		COUNT(appointment_id) >= 5
	ORDER BY
		doc_id, yea
)
SELECT
		doc_id, fname, lname
FROM
		a1 NATURAL JOIN
		doctor NATURAL JOIN
		working_staff NATURAL JOIN
		general_user
GROUP BY
		doc_id, fname, lname
HAVING
		count(doc_id) = 10 AND SUM(num) >= 100;