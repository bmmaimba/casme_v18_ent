# -*- coding: utf-8 -*-
{
    "name": "casme_v18_ent_base",
    "summary": "casme_v18_ent_base",
    "description": "casme_v18_ent_base",

    'author': 'DataInnovators.',
    'website': 'https://datainnovators.co',
    'support': 'support@datainnovators.co',

    'category': 'Base',
    'version': '18.0.0.0.0',
    "depends": [
                "base",
                "web",
                ],
    "data": [
        "security/ir.model.access.csv",

        "views/ir_attachment.xml",
        "views/res_config_settings.xml",

        "data/data_powered_by_brand_promotion_login.xml",
        "data/ir_cron_data.xml",
        "data/ir_mail_server_data.xml",
        "data/data_res_company.xml",
        "data/data_digest_digest.xml",
    ],
#   'assets': {
#       'web.assets_backend': ['/casme_v18_ent_base/static/src/js/action_manager.js',]
#   },
#        'survey.survey_assets': [
#            'survey_file_upload_field/static/src/css/survey_front_result.css',
#            'survey_file_upload_field/static/src/js/survey_form.js',
#        ],
#    },
    "images": ['static/description/casme.png'],
    "license": "LGPL-3",
    "auto_install": False,
    "installable": True,
    "application": True
    #'pre_init_hook': 'pre_init_check',
}