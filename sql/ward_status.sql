SELECT
    w.name AS "Ward"
    , COUNT(a.hn) AS "จำนวนเตียง" 
FROM ipt a
LEFT OUTER JOIN ovst o ON o.an = a.an
LEFT OUTER JOIN ward w ON w.ward = a.ward
WHERE a.dchstts IS NULL 
GROUP BY a.ward
;