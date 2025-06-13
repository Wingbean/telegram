SELECT o.hn
FROM ovst o
LEFT OUTER JOIN clinicmember c ON o.hn = c.hn
WHERE o.vstdate = CURDATE() AND o.main_dep = '033' AND c.regdate IS NULL
GROUP BY o.hn
;