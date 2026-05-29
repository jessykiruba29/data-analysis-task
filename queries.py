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

