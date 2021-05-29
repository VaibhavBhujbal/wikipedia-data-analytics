DROP TABLE IF EXISTS wiki.outdated_pages;
CREATE table wiki.outdated_pages as 
SELECT c1.cl_to as category,
       page_id
FROM   (SELECT c.cl_to,
               Max( p.page_links_updated - p.page_touched) AS duration
        FROM   wiki.page p
               JOIN wiki.categorylinks c
                 ON p.page_id = c.cl_from
               JOIN (SELECT DISTINCT cat_title
                     FROM   wiki.category
                     ORDER  BY cat_pages DESC
                     LIMIT  10) AS cat
                 ON cat.cat_title = c.cl_to
        GROUP  BY c.cl_to) AS c1
       JOIN wiki.page p1
         ON c1.duration = p1.page_links_updated - p1.page_touched
ORDER  BY c1.duration DESC;