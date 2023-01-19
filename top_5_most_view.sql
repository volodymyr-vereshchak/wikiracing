SELECT pg.name, count(ptl.link_id) AS ptl_count
FROM page AS pg
JOIN page_to_link AS ptl
ON pg.id = ptl.link_id
GROUP BY pg.name
ORDER BY ptl_count DESC
LIMIT 5

