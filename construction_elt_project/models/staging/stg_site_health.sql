SELECT
    site_id,
    event_type,
    severity,
    score,
    event_description,
    event_timestamp
FROM {{ ref('site_health_events') }}