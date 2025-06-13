SELECT 
	o.main_dep AS "รหัส"
	,CASE
		WHEN k.department = "คลินิกวัณโรค/ฝ่ายสุขาภิบาลฯ" THEN "ห้องเบอร์ 9"
		WHEN k.department = "จุดซักประวัติ" THEN "OPD"
		WHEN k.department = "คลินิกดอกลำดวน" THEN "NCD"
		ELSE k.department
	END AS "DeptName"
	,COUNT(vn) AS "จำนวน"
FROM ovst o 
LEFT OUTER JOIN kskdepartment k ON k.depcode = o.main_dep 
WHERE o.vstdate BETWEEN CURDATE() AND CURDATE() AND o.main_dep != "999"
GROUP BY o.main_dep
ORDER BY COUNT(vn) DESC
;