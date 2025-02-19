# -*- coding: utf-8 -*-
{
    "name": "casme_v18_ent_casme",
    "summary": "casme_v18_ent_casme",
    "description": "casme_v18_ent_casme",

    'author': 'DataInnovators.',
    'website': 'https://datainnovators.co',
    'support': 'support@datainnovators.co',

    'category': 'Base',
    'version': '18.0.0.0.0',
    "depends": [
                "appointment",
                "appointment_hr",
                "calendar",
                "base",
                "base_setup",
                "base_import",
                "base_automation",
                "base_import_module",
                "base_install_request",
                "base_geolocalize",
                "contacts",
                "contacts_enterprise",
                "board",
                "spreadsheet",
                "spreadsheet_dashboard",
                "spreadsheet_dashboard_edition",
                "project",
                "project_hr_skills",
                "project_enterprise",
                "project_enterprise_hr",
                "project_enterprise_hr_skills",
                "project_sms",
                "project_todo",
                "timesheet_grid",
                "timer",
                "timer",
                "mail",
                "mail_enterprise",
                "partner_autocomplete",
                "mass_mailing",
                "survey",
                "link_tracker",
                "mass_mailing_themes",
                "knowledge",
                "hr_attendance",
                "hr_timesheet",
                "hr_hourly_cost",
                "sign",
                "casme_v18_ent_base",
                ],
    "data": [
        "security/ir.model.access.csv",

        "views/casme.xml",
        "views/res_partner_learners.xml",
        "views/res_partner_learners_sessions_rel.xml",
        "views/res_partner_teachers.xml",
        "views/res_partner_teachers_sessions_rel.xml",
        "views/res_partner_schools.xml",
        "views/school_grades.xml",
        "views/school_subjects.xml",
        "views/school_topics.xml",
        "views/school_years.xml",
        "views/school_terms.xml",
        "views/school_sessions.xml",
        "views/project_types.xml",
        "views/project_project.xml",

        "data/data_digest_digest.xml",
        "data/data_project_types.xml",
        "data/data_school_terms.xml",
        "data/data_school_grades.xml",
        "data/data_school_years.xml",
        "data/data_res_users.xml",

        "data/ir_cron_data.xml",
        "data/ir_sequence_data.xml",
    ],
    'assets': {
        'web.assets_backend': [
            '/casme_v18_ent_casme/static/src/css/header.css',
            '/casme_v18_ent_casme/static/src/js/one2manysearch.js',
            '/casme_v18_ent_casme/static/src/fields/one2manysearch/one2manysearch_template.xml',
        ],
    # 'survey.survey_assets': [
    #        'survey_file_upload_field/static/src/css/survey_front_result.css',
    #        'survey_file_upload_field/static/src/js/survey_form.js',
    #    ],
   },
    "images": ['static/description/casme.png'],
    "license": "LGPL-3",
    "auto_install": False,
    "installable": True,
    "application": True,
    #"pre_init_hook: 'pre_init_check',
}