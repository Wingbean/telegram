SELECT 
	o.main_dep AS "รหัส"
	,k.department AS "แผนก"
	,COUNT(vn) AS "จำนวน"
FROM ovst o 
LEFT OUTER JOIN kskdepartment k ON k.depcode = o.main_dep 
WHERE o.vstdate BETWEEN CURDATE() AND CURDATE() AND o.main_dep != "999"
GROUP BY o.main_dep 
;