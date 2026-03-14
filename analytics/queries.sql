-- total events
SELECT COUNT(*) FROM events;

-- events by type
SELECT
event_data->>'event_type' AS event_type,
COUNT(*)
FROM events
GROUP BY event_type;

-- active users
SELECT
COUNT(DISTINCT event_data->>'user_id')
FROM events;

-- events per user
SELECT
event_data->>'user_id',
COUNT(*)
FROM events
GROUP BY event_data->>'user_id'
ORDER BY COUNT(*) DESC
LIMIT 10;