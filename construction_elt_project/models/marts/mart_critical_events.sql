SELECT
    site_id,
    event_type,
    severity,
    score,
    description,
    timestamp
FROM {{ ref('int_site_health_events') }}
WHERE severity = 'CRITICAL'