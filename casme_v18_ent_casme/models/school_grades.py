# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class SchoolGrades(models.Model):
    _name = "school.grades"
    _description = 'Grades'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Grade')
    res_partner_learners_ids = fields.One2many('res.partner.learners','learner_grade_id', string='Learners')