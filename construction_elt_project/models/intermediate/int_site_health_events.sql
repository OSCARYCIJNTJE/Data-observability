SELECT
    site_id,
    event_type,
    severity,

    CASE
        WHEN severity = 'CRITICAL' THEN 3
        WHEN severity = 'HIGH' THEN 2
        WHEN severity = 'MEDIUM' THEN 1
        ELSE 0
    END AS severity_rank,

    score,
    event_description,
    event_timestamp

FROM {{ ref('stg_site_health') }}