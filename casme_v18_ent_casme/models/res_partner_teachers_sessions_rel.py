# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class ResPartnerTeachersSessionsRel(models.Model):
    _name = "res.partner.teachers.sessions.rel"
    _description = 'res.partner.teachers.sessions.rel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    teacher_id = fields.Many2one('res.partner.teachers', ondelete='restrict', auto_join=True, store=True,
                                         string='Teacher', help='Teacher')
    session_id = fields.Many2one('school.sessions', ondelete='restrict', auto_join=True, store=True,
                                         string='Session', help='Session/event')