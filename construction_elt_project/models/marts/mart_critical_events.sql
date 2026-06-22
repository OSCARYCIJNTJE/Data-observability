SELECT
    site_id,
    event_type,
    severity,
    score,
    event_description,
    event_timestamp
FROM {{ ref('int_site_health_events') }}
WHERE severity = 'CRITICAL'