SELECT
    site_id,
    event_type,
    COUNT(*) AS event_count
FROM {{ ref('int_site_health_events') }}
GROUP BY site_id, event_type