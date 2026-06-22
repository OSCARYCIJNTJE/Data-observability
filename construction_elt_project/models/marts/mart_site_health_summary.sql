SELECT
    site_id,
    event_type,
    severity,

    COUNT(*) AS event_count,

    AVG(score) AS avg_score,

    MAX(timestamp) AS latest_event_timestamp

FROM {{ ref('int_site_health_events') }}

GROUP BY
    site_id,
    event_type,
    severity