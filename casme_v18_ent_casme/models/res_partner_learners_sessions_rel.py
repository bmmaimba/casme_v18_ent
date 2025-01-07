# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class ResPartnerLearnersSessionsRel(models.Model):
    _name = "res.partner.learners.sessions.rel"
    _description = 'res.partner.learners.sessions.rel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    learner_id = fields.Many2one('res.partner.learners', ondelete='restrict', auto_join=True, store=True,
                                         string='Learner', help='Learner')
    session_id = fields.Many2one('school.sessions', ondelete='restrict', auto_join=True, store=True,
                                         string='Session', help='Session/event')
    session_attendance = fields.Selection([
        ('absent', 'Absent'),
        ('present', 'Present'), ], string='Session Attendance')

    def select_present_attendance(self):
        self.session_attendance = 'present'

    def select_absent_attendance(self):
        self.session_attendance = 'absent'