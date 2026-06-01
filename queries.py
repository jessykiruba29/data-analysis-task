regional_demo="""
SELECT a.current_city, b.language, COUNT(a.lead_id) as totalleads, ROUND(avg(watched_percentage),2) as avgtime
FROM leads_basic_details a
INNER JOIN leads_demo_watched_details b
ON a.lead_id=b.lead_id
GROUP BY a.current_city, b. language
ORDER BY totalleads DESC;

"""

lead_source="""
SELECT a.lead_gen_source as source , COUNT(DISTINCT a.lead_id) as totalleads, 
COUNT(DISTINCT
	CASE
		WHEN c.call_status='successful' and lead_stage='conversion' THEN a.lead_id
        END
	) as successful_conversions,
ROUND(100*(COUNT(DISTINCT
	CASE
		WHEN c.call_status='successful' and lead_stage='conversion' THEN a.lead_id
        END
	)/COUNT(DISTINCT a.lead_id)),2) AS converted_rate 
FROM leads_basic_details a
INNER JOIN leads_interaction_details c
ON a.lead_id=c.lead_id
GROUP BY a.lead_gen_source 
ORDER BY converted_rate DESC;

"""

interest="""SELECT 
    'Demo Stage' AS stage,
    CASE
        WHEN reasons_for_not_interested_in_demo IN ("Can't afford", "Cannot afford")
            THEN 'Affordability Issue'
        ELSE reasons_for_not_interested_in_demo
    END AS reason,
    COUNT(lead_id) AS total_students
FROM leads_reasons_for_no_interest
WHERE reasons_for_not_interested_in_demo != ''
GROUP BY reason

UNION ALL

SELECT 
    'Consideration Stage' AS stage,
    CASE
        WHEN reasons_for_not_interested_to_consider IN ("Can't afford", "Cannot afford")
            THEN 'Affordability Issue'
        ELSE reasons_for_not_interested_to_consider
    END AS reason,
    COUNT(lead_id) AS total_students
FROM leads_reasons_for_no_interest
WHERE reasons_for_not_interested_to_consider != ''
GROUP BY reason

UNION ALL

SELECT 
    'Conversion Stage' AS stage,
    CASE
        WHEN reasons_for_not_interested_to_convert IN ("Can't afford", "Cannot afford")
            THEN 'Affordability Issue'
        ELSE reasons_for_not_interested_to_convert
    END AS reason,
    COUNT(lead_id) AS total_students
FROM leads_reasons_for_no_interest
WHERE reasons_for_not_interested_to_convert != ''
GROUP BY reason
ORDER BY stage DESC, total_students DESC;

"""

pricing="""
SELECT a.current_education,  COUNT(a.lead_id) as totalleads,
COUNT(CASE
	WHEN d.reasons_for_not_interested_in_demo="Can't afford" 
    OR d.reasons_for_not_interested_in_demo="Cannot afford"
    OR d.reasons_for_not_interested_to_consider="Can't afford"
    OR d.reasons_for_not_interested_to_consider="Cannot afford"
    OR d.reasons_for_not_interested_to_convert="Can't afford"
    OR d.reasons_for_not_interested_to_convert="Cannot afford"
    THEN a.lead_id
    END) as price_issue,
ROUND(100*(COUNT(CASE
	WHEN d.reasons_for_not_interested_in_demo="Can't afford" 
    OR d.reasons_for_not_interested_in_demo="Cannot afford"
    OR d.reasons_for_not_interested_to_consider="Can't afford"
    OR d.reasons_for_not_interested_to_consider="Cannot afford"
    OR d.reasons_for_not_interested_to_convert="Can't afford"
    OR d.reasons_for_not_interested_to_convert="Cannot afford"
    THEN a.lead_id
    END)/COUNT(a.lead_id))) as drop_percent
FROM leads_basic_details a
INNER JOIN leads_reasons_for_no_interest d
ON a.lead_id=d.lead_id

GROUP BY a.current_education
HAVING COUNT(DISTINCT a.lead_id)>=10
ORDER BY drop_percent DESC;

"""

watched_percentage="""
WITH converted_leads AS (
    SELECT DISTINCT lead_id
    FROM leads_interaction_details
    WHERE lead_stage='conversion'
    AND call_status='successful'
)

SELECT
    CASE
        WHEN d.watched_percentage < 25 THEN '0-25%'
        WHEN d.watched_percentage < 50 THEN '26-50%'
        WHEN d.watched_percentage < 75 THEN '51-75%'
        ELSE '76-100%'
    END AS watch_bucket,

    COUNT(d.lead_id) AS total_students,

    COUNT(c.lead_id) AS converted_students,

    ROUND(
        100 * COUNT(c.lead_id) / COUNT(d.lead_id),
        2
    ) AS conversion_rate

FROM leads_demo_watched_details d

LEFT JOIN converted_leads c
ON d.lead_id = c.lead_id

GROUP BY watch_bucket
ORDER BY watch_bucket;

"""

team_performance="""
WITH jnr_stats AS (
    SELECT
        s.snr_sm_id,
        s.jnr_sm_id,

        COUNT(DISTINCT s.lead_id) AS total_leads,

        COUNT(
            DISTINCT CASE
                WHEN li.lead_stage = 'conversion'
                AND li.call_status='successful'
                THEN s.lead_id
            END
        ) AS converted_leads,

        ROUND(
            100.0 *
            COUNT(
                DISTINCT CASE
                    WHEN li.lead_stage = 'conversion'
                    AND li.call_status='successful'
                    THEN s.lead_id
                END
            ) /
            COUNT(DISTINCT s.lead_id),
            2
        ) AS conversion_rate

    FROM sales_managers_assigned_leads_details s
    LEFT JOIN leads_interaction_details li
        ON s.lead_id = li.lead_id

    GROUP BY s.snr_sm_id, s.jnr_sm_id

    HAVING COUNT(DISTINCT s.lead_id) >= 10
)

SELECT
    snr_sm_id,

    COUNT(jnr_sm_id) AS total_juniors,

    ROUND(AVG(conversion_rate),2) AS avg_team_conversion,

    MIN(conversion_rate) AS lowest_conversion,

    MAX(conversion_rate) AS highest_conversion

FROM jnr_stats

GROUP BY snr_sm_id

ORDER BY avg_team_conversion DESC;

"""

junior_performance="""
SELECT
    jnr_sm_id,

    COUNT(DISTINCT lead_id) AS total_leads_handled,

    COUNT(
        DISTINCT CASE
            WHEN lead_stage = 'conversion'
            AND call_status = 'successful'
            THEN lead_id
        END
    ) AS converted_leads,

    ROUND(
        100.0 *
        COUNT(
            DISTINCT CASE
                WHEN lead_stage = 'conversion'
                AND call_status = 'successful'
                THEN lead_id
            END
        ) /
        COUNT(DISTINCT lead_id),
        2
    ) AS conversion_rate

FROM leads_interaction_details

GROUP BY jnr_sm_id

HAVING COUNT(DISTINCT lead_id) >= 10

ORDER BY conversion_rate ASC;

"""

city_neglect="""
SELECT 
    lb.current_city,
    COUNT(DISTINCT s.lead_id) AS leads_assigned,
    COUNT(DISTINCT li.lead_id) AS leads_contacted,
    ROUND(100.0 * COUNT(DISTINCT li.lead_id) / NULLIF(COUNT(DISTINCT s.lead_id), 0), 1) AS contact_rate,
    COUNT(DISTINCT s.lead_id) - COUNT(DISTINCT li.lead_id) AS leads_ignored,
    COUNT(DISTINCT s.jnr_sm_id) AS unique_juniors_assigned
FROM sales_managers_assigned_leads_details s
JOIN leads_basic_details lb ON s.lead_id = lb.lead_id
LEFT JOIN leads_interaction_details li ON s.lead_id = li.lead_id
GROUP BY lb.current_city
HAVING leads_assigned >= 20
ORDER BY contact_rate ASC
LIMIT 10;

"""

junior_neglect="""
-- CORRECTED: Leads assigned but never called (per junior manager summary)
WITH junior_neglect_stats AS (
    SELECT 
        s.jnr_sm_id,
        COUNT(DISTINCT s.lead_id) AS total_assigned,
        COUNT(DISTINCT li.lead_id) AS total_contacted,
        COUNT(DISTINCT s.lead_id) - COUNT(DISTINCT li.lead_id) AS never_touched
    FROM sales_managers_assigned_leads_details s
    LEFT JOIN leads_interaction_details li ON s.lead_id = li.lead_id
    GROUP BY s.jnr_sm_id
)
SELECT 
    jns.jnr_sm_id,
    jns.total_assigned,
    jns.total_contacted,
    jns.never_touched,
    ROUND(100.0 * jns.never_touched / jns.total_assigned, 1) AS neglect_rate_percent,
    -- Get most common source among their ignored leads
    (
        SELECT lb.lead_gen_source
        FROM sales_managers_assigned_leads_details s2
        JOIN leads_basic_details lb ON s2.lead_id = lb.lead_id
        LEFT JOIN leads_interaction_details li2 ON s2.lead_id = li2.lead_id
        WHERE s2.jnr_sm_id = jns.jnr_sm_id AND li2.lead_id IS NULL
        GROUP BY lb.lead_gen_source
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS most_common_source_of_ignored
FROM junior_neglect_stats jns
WHERE jns.never_touched > 0
ORDER BY neglect_rate_percent DESC;

"""

age_group="""
SELECT
    CASE
        WHEN age BETWEEN 16 AND 20 THEN '16-20'
        WHEN age BETWEEN 21 AND 25 THEN '21-25'
        WHEN age BETWEEN 26 AND 30 THEN '26-30'
        ELSE '31+'
    END AS age_group,
    COUNT(lead_id) AS total_leads,
    ROUND(
        100.0 * COUNT(lead_id) /
        (SELECT COUNT(lead_id) FROM leads_basic_details),
        2
    ) AS percentage_of_leads
FROM leads_basic_details
GROUP BY age_group
ORDER BY age_group;

"""

call_analysis="""
WITH converted_leads AS (
    SELECT DISTINCT lead_id
    FROM leads_interaction_details
    WHERE lead_stage = 'conversion'
    AND call_status = 'successful'
)

SELECT
    total_calls,
    COUNT(lead_id) AS converted_leads
FROM (
    SELECT
        li.lead_id,
        COUNT(li.lead_id) AS total_calls
    FROM leads_interaction_details li
    INNER JOIN converted_leads c
        ON li.lead_id = c.lead_id
    GROUP BY li.lead_id
) x

GROUP BY total_calls
ORDER BY converted_leads;

"""

regional_conversions="""
WITH converted_leads AS (
    SELECT DISTINCT lead_id
    FROM leads_interaction_details
    WHERE lead_stage = 'conversion'
    AND call_status = 'successful'
)

SELECT
    b.current_city,

    COUNT(DISTINCT b.lead_id) AS total_leads,

    COUNT(DISTINCT c.lead_id) AS converted_students,

    ROUND(
        100.0 * COUNT(DISTINCT c.lead_id)
        / COUNT(DISTINCT b.lead_id),
        2
    ) AS conversion_rate

FROM leads_basic_details b

LEFT JOIN converted_leads c
ON b.lead_id = c.lead_id

GROUP BY b.current_city

HAVING COUNT(DISTINCT b.lead_id) >= 10

ORDER BY conversion_rate DESC;

"""
