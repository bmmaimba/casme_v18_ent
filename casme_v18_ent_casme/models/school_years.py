# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class SchoolYears(models.Model):
    _name = "school.years"
    _description = 'Years'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Year', store=True)