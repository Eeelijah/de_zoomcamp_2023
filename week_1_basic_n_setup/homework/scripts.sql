-- Homework, questions 3-6
-- 3
select count("index")
from green_taxi_data gtd
where date(lpep_pickup_datetime) = to_date('2019-01-15', 'YYYY-MM-DD')
and date(lpep_dropoff_datetime) = to_date('2019-01-15', 'YYYY-MM-DD')

-- 4
select lpep_pickup_datetime
from green_taxi_data gtd
where trip_distance = (select max(trip_distance) from green_taxi_data gtd2)

-- 5
select count("index"), passenger_count
from green_taxi_data gtd
where date(lpep_pickup_datetime) = to_date('2019-01-01', 'YYYY-MM-DD')
and passenger_count in (2, 3)
group by passenger_count

-- 6
with tmp as (
select max(t1.tip_amount), t1."DOLocationID"
from green_taxi_data t1
join zones zpu on t1."PULocationID" = zpu."LocationID"
where zpu."Zone" = 'Astoria'
group by t1."DOLocationID"
order by max(t1.tip_amount) desc
limit 1
)
select zdo."Zone"
from tmp t1
JOIN zones zdo ON t1."DOLocationID"=zdo."LocationID"