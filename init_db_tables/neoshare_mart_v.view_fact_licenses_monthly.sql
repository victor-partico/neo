CREATE VIEW IF NOT EXISTS `neoshare_mart_v`.`view_fact_licenses_monthly` AS 
    SELECT
        CAST(DATE_FORMAT(app_date, '%Y-%m-01') AS DATE) AS dim_date_id,
        `type` AS application_type,
        COUNT(DISTINCT IF(status='Approved - License Issued', app_no, NULL )) AS number_of_approved_licenses,
        COUNT(DISTINCT IF(status='Denied', app_no, NULL )) AS number_of_denied_licenses
    FROM
        `neoshare_lake`.`tlc_new_driver_application_status`
    WHERE
        app_date >= DATE(CONCAT(YEAR(DATE_SUB(CURDATE(), INTERVAL 5 YEAR)), '-01-01'))
    GROUP BY
        dim_date_id,
        `type`
    ORDER BY
        dim_date_id DESC,
        `type`