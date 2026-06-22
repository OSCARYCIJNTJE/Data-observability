SELECT
    site_id,
    event_type,
    severity,
    score,
    description,
    timestamp
FROM {{ ref('site_health_events') }}