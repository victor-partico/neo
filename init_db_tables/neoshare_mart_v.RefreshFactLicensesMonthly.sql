CREATE PROCEDURE IF NOT EXISTS neoshare_mart_v.RefreshFactLicensesMonthly()
BEGIN
    -- Truncate the fact table to remove existing data
    TRUNCATE TABLE neoshare_mart.fact_licenses_monthly;

    -- Insert the aggregated data from the source table
    INSERT INTO neoshare_mart.fact_licenses_monthly (dim_date_id, application_type, number_of_approved_licenses, number_of_denied_licenses)
    SELECT * FROM neoshare_mart_v.view_fact_licenses_monthly;
END;