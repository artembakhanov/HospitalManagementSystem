WITH a1 AS (
	SELECT doctor_team_id,
	to_char(start_time, 'Day') AS day_of_week,
	EXTRACT(ISODOW from start_time) AS num_day_of_week,
	EXTRACT(MINUTE FROM start_time) AS minu,
	EXTRACT (HOUR FROM start_time) AS hou
	FROM appointment
	WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '1 year' AND CURRENT_DATE
),	a2 AS (
	SELECT doctor_team_id, day_of_week, hou, minu, num_day_of_week, COUNT(*) AS num
	FROM a1
	GROUP BY (day_of_week, minu, doctor_team_id, hou, num_day_of_week)
	ORDER BY doctor_team_id, num_day_of_week, hou, minu
)
SELECT doc_id, fname, lname, day_of_week,
make_time(hou::INTEGER, minu::INTEGER, 0.00) AS time_slot, num AS total, num / 52::FLOAT AS average
FROM a2
NATURAL JOIN doctor_team
NATURAL JOIN doctor
NATURAL JOIN working_staff
NATURAL JOIN general_user;