SELECT avg(links.count_links)
FROM (
    SELECT tptl.page_id, count(tptl.link_id) AS count_links
    FROM page_to_link AS tptl
    WHERE tptl.page_id IN (
        SELECT ptl.link_id 
        FROM page AS pg 
        JOIN page_to_link AS ptl
        ON pg.id = ptl.page_id
        WHERE pg.id = 1
        )
    GROUP BY tptl.page_id
) AS links
