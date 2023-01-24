--1. --iidfile string

--2. 3

--3. 20530
SELECT count(*) FROM green_taxi_trips 
WHERE lpep_pickup_datetime>'2019-01-15' AND '2019-01-16'>lpep_dropoff_datetime


--4. 2019-01-15
SELECT s.lpep_pickup_datetime, s.trip_distance 
FROM green_taxi_trips s 
ORDER BY s.trip_distance DESC


--5. 2: 1282 ; 3: 254
SELECT count(*) FROM green_taxi_trips s 
WHERE lpep_pickup_datetime > '2019-01-01' AND  '2019-01-02' > lpep_pickup_datetime AND passenger_count = 3


--6. Long Island City/Queens Plaza
SELECT s.tip_amount, "z"."Zone", "z2"."Zone" FROM green_taxi_trips s
INNER JOIN taxi_zones z
ON s."PULocationID" = z."LocationID"
LEFT JOIN taxi_zones z2
ON s."DOLocationID" = z2."LocationID"
WHERE "z"."Zone" = 'Astoria'
ORDER BY tip_amount DESC
LIMIT 1
