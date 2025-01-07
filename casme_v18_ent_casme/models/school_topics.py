# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class SchoolTopics(models.Model):
    _name = "school.topics"
    _description = 'Topics'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Topic', store=True)