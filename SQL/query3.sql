WITH week1 as (
	SELECT patient_id, COUNT(patient_id) as num FROM appointment WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '1 week' AND CURRENT_DATE
	GROUP BY patient_id
	HAVING count(patient_id) >= 2
), 	week2 as (
	SELECT patient_id, COUNT(patient_id) as num FROM appointment
	WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '2 week' AND CURRENT_DATE - INTERVAL '1 week'
	GROUP BY patient_id
	HAVING count(patient_id) >= 2
), 	week3 as (
	SELECT patient_id, COUNT(patient_id) as num FROM appointment
	WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '3 week' AND CURRENT_DATE - INTERVAL '2 week'
	GROUP BY patient_id
	HAVING count(patient_id) >= 2
),  week4 as (
	SELECT patient_id, COUNT(patient_id) as num FROM appointment
	WHERE start_time BETWEEN CURRENT_DATE - INTERVAL '4 week' AND CURRENT_DATE - INTERVAL '3 week'
	GROUP BY patient_id
	HAVING count(patient_id) >= 2
), p_ids as (
	SELECT patient_id FROM week1
	INTERSECT SELECT patient_id FROM week2
	INTERSECT SELECT patient_id FROM week3
	INTERSECT SELECT patient_id FROM week4
)
SELECT patient_id, fname, lname FROM p_ids NATURAL JOIN patient NATURAL JOIN general_user;