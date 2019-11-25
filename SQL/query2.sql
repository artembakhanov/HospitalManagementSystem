WITH
-- Here we create a CTE that contains an information about
-- the number of different days of week during the last year.
-- It includes the current date and the date exactly one year before.
-- For example, if today is 26.12.2019 then the CTE contains info
-- in period [26.12.2018; 26.12.2019].
-- It also works with leap years.
-- This is important since the number of days of week is different in each year.
dow_nums AS (
	SELECT EXTRACT (ISODOW FROM datum) AS dow, COUNT(*)
	FROM
	   (SELECT CURRENT_DATE - INTERVAL '1 year' + s*'1day'::interval AS datum
		FROM
			generate_series(0,
			                -- this line is done just for leap years
							EXTRACT (DAY FROM CURRENT_DATE - (CURRENT_DATE - INTERVAL '1 year'))::INTEGER) s) dates
	GROUP BY dow
	ORDER BY dow
),
a1 AS (
	SELECT doctor_team_id,
	to_char(start_time, 'Day') AS day_of_week,
	EXTRACT(ISODOW FROM start_time) AS num_day_of_week,
	start_time::TIME AS time_slot_start,
	end_time::TIME AS time_slot_end
	FROM appointment
	WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '1 year' AND CURRENT_DATE
),	a2 AS (
	SELECT doctor_team_id, day_of_week, time_slot_start, time_slot_end, num_day_of_week, COUNT(*) AS num
	FROM a1
	GROUP BY (day_of_week, doctor_team_id, num_day_of_week, time_slot_start, time_slot_end)
	ORDER BY doctor_team_id, num_day_of_week, time_slot_start
)
SELECT
	doc_id, fname, lname, day_of_week,
	time_slot_start,
	time_slot_end,
	num AS total,
	num / (SELECT count FROM dow_nums WHERE dow = num_day_of_week)::FLOAT AS average
FROM
	a2
	NATURAL JOIN doctor_team
	NATURAL JOIN doctor
	NATURAL JOIN working_staff
	NATURAL JOIN general_user;