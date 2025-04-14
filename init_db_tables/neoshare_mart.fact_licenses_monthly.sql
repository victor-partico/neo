CREATE TABLE IF NOT EXISTS `neoshare_mart`.`fact_licenses_monthly` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`dim_date_id` DATETIME NOT NULL,
	`application_type` CHAR(3) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`number_of_approved_licenses` INT(11) NULL DEFAULT '0',
	`number_of_denied_licenses` INT(11) NULL DEFAULT '0',
	UNIQUE INDEX `dim_date_id_application_type` (`dim_date_id`, `application_type`) USING BTREE,
	INDEX `id` (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
