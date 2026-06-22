SELECT
    site_id,
    severity,
    COUNT(*) AS risk_event_count,
    AVG(score) AS avg_risk_score,
    MAX(score) AS max_risk_score
FROM {{ ref('int_site_health_events') }}
WHERE event_type = 'RISK'
GROUP BY site_id, severity