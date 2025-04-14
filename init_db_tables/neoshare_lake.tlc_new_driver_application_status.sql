CREATE TABLE IF NOT EXISTS `neoshare_lake`.`tlc_new_driver_application_status` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`app_no` BIGINT(20) NOT NULL,
	`type` CHAR(3) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`app_date` DATETIME NULL DEFAULT NULL,
	`status` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci',
	`fru_interview_scheduled` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`drug_test` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`wav_course` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`defensive_driving` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`driver_exam` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`medical_clearance_form` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`other_requirements` LONGTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`last_updated` DATETIME NOT NULL,
	`_sc_arrival_ts` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`_sc_updated_ts` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`app_no`) USING BTREE,
	INDEX `id` (`id`) USING BTREE,
	INDEX `type` (`type`) USING BTREE,
	INDEX `status` (`status`) USING BTREE,
	INDEX `app_date` (`app_date`) USING BTREE
	-- table is too small, so it does not need partition
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;