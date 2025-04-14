INSERT INTO `neoshare_lake`.`tlc_new_driver_application_status` (
    app_no,
    type,
    app_date,
    status,
    fru_interview_scheduled,
    drug_test,
    wav_course,
    defensive_driving,
    driver_exam,
    medical_clearance_form,
    other_requirements,
    last_updated
)
VALUES (
    %(app_no)s,
    %(type)s,
    %(app_date)s,
    %(status)s,
    %(fru_interview_scheduled)s,
    %(drug_test)s,
    %(wav_course)s,
    %(defensive_driving)s,
    %(driver_exam)s,
    %(medical_clearance_form)s,
    %(other_requirements)s,
    %(last_updated)s
)
ON DUPLICATE KEY UPDATE
    type = VALUES(type),
    app_date = VALUES(app_date),
    status = VALUES(status),
    fru_interview_scheduled = VALUES(fru_interview_scheduled),
    drug_test = VALUES(drug_test),
    wav_course = VALUES(wav_course),
    defensive_driving = VALUES(defensive_driving),
    driver_exam = VALUES(driver_exam),
    medical_clearance_form = VALUES(medical_clearance_form),
    other_requirements = VALUES(other_requirements),
    last_updated = VALUES(last_updated);
