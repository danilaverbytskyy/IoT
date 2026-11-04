-- Q1. Ряд одного датчика за период
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT datetime, temperature, humidity, light, voltage
FROM sensors_data
WHERE mote_id = 10
  AND datetime >= TIMESTAMP '2004-03-01'
  AND datetime <  TIMESTAMP '2004-03-08'
ORDER BY datetime;

-- Q2. Агрегация по часу для одного датчика
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT date_trunc('hour', datetime) AS hour,
       avg(temperature) AS t_avg,
       min(temperature) AS t_min,
       max(temperature) AS t_max
FROM sensors_data
WHERE mote_id = 10
  AND datetime >= TIMESTAMP '2004-03-01'
  AND datetime <  TIMESTAMP '2004-03-08'
GROUP BY 1
ORDER BY 1;

-- Q3. Сводка по всем датчикам за сутки
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT mote_id,
       avg(temperature) AS t_avg,
       avg(humidity)    AS h_avg,
       avg(voltage)     AS v_avg,
       count(*)         AS n
FROM sensors_data
WHERE datetime >= TIMESTAMP '2004-03-01'
  AND datetime <  TIMESTAMP '2004-03-02'
GROUP BY mote_id
ORDER BY mote_id;

-- Q4. Последнее измерение каждого датчика
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT DISTINCT ON (mote_id)
       mote_id, datetime, temperature, humidity, voltage
FROM sensors_data
ORDER BY mote_id, datetime DESC;