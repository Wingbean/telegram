SELECT
    w.name AS "Ward"
    ,COUNT(i.an) AS "Count"
FROM ipt i
LEFT OUTER JOIN ward w ON w.ward = i.ward
LEFT OUTER JOIN pttype p  ON p.pttype = i.pttype
WHERE i.regdate = CURDATE()
GROUP BY Ward
;