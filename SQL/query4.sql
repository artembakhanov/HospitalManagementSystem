WITH a1 AS (
	SELECT patient_id, COUNT(patient_id) as num
	FROM appointment
	WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '1 month' AND CURRENT_DATE
	GROUP BY patient_id
	ORDER BY patient_id
),	a2 AS (
	SELECT patient_id, num, DATE_PART('year', CURRENT_DATE) - DATE_PART('year', birth_date) AS age FROM a1 NATURAL JOIN patient NATURAL JOIN general_user
),  p1 AS (
	SELECT COUNT(patient_id) * 200 as total_price
	FROM a2
	WHERE age < 50 AND num < 3
),  p2 AS (
	SELECT COUNT(patient_id) * 400 as total_price
	FROM a2
	WHERE age >= 50 AND num < 3
),	p3 AS (
	SELECT COUNT(patient_id) * 250 as total_price
	FROM a2
	WHERE age < 50 AND num >= 3
),	p4 AS (
	SELECT COUNT(patient_id) * 500 as total_price
	FROM a2
	WHERE age >= 50 AND num >= 3
)

SELECT
	SUM(total_price) as total_price
FROM
	(SELECT * FROM p1 UNION
	SELECT * FROM p2 UNION
	SELECT * FROM p3 UNION
	SELECT * FROM p4) AS p_all;
