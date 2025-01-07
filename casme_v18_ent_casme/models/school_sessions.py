# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class SchoolSessions(models.Model):
    _name = "school.sessions"
    _description = 'Sessions'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.onchange('session_project_id', 'session_topic_id', 'session_school_id', 'session_subject_id', 'session_grade_id', 'session_term_id')
    def _get_onchange_school_sessions_name(self):
        self.name = str(self.session_project_id.name) + '-' + str(self.session_school_id.name) + '-' + str(self.session_subject_id.name) + '-' + str(self.session_grade_id.name) + '-' + str(self.session_term_id.name)

    name = fields.Char('Session/Event Name', store=True, default=_get_onchange_school_sessions_name)

    session_type = fields.Selection([
        ('learners', 'Learners'),
        ('teachers', 'Teachers'), ], string='Session Type')

    session_project_id = fields.Many2one('project.project', ondelete='restrict', auto_join=True, store=True,
                                         string='Project', help='The school associated with the session/event')

    session_project_types_id = fields.Many2one('project.types', ondelete='restrict', auto_join=True, store=True,
                                         string='Project Type', help='The project types associated with the session/event')

    session_school_id = fields.Many2one('res.partner.schools', ondelete='restrict', auto_join=True, store=True,
                                        string='School', help='The school where the session is held')

    session_subject_id = fields.Many2one('school.subjects', ondelete='restrict', auto_join=True, store=True,
                                         string='Subject', help='The subject of the session/event')

    session_topic_id = fields.Many2one('school.topics', ondelete='restrict', auto_join=True, store=True,
                                         string='Topic', help='The topic of the session/event')

    session_grade_id = fields.Many2one('school.grades', ondelete='restrict', auto_join=True, store=True,
                                       string='Grade', help='The grade level of students in the session')

    session_term_id = fields.Many2one('school.terms', ondelete='restrict', auto_join=True, store=True,
                                      string='Term', help='The academic term of the session')

    session_year_id = fields.Many2one('school.years', ondelete='restrict', auto_join=True, store=True,
                                      string='Academic Year', help='The academic year of the session',
                                      default=lambda self: self._get_default_session_year()
                                      )

    def _get_default_session_year(self):
        """Find the school year record for the current year."""
        current_year = date.today().year  # Get the current year
        # Only set the default if the field is empty (False or None)
        if not self.session_year_id:
            year_record = self.env['school.years'].search([('name', '=', current_year)], limit=1)
            return year_record.id if year_record else False
        return self.session_year_id  # Keep the existing value if it's not empty

    res_partner_learners_ids = fields.One2many(
        'res.partner.learners.sessions.rel',  # The target model
        'session_id',  # The field in the target model that references this model
        string='Learners',  # Label for the field in the UI
    )

    res_partner_teachers_ids = fields.One2many(
        'res.partner.teachers.sessions.rel',  # The target model
        'session_id',  # The field in the target model that references this model
        string='Teachers',  # Label for the field in the UI
    )
    def action_add_learners_to_session(self):
        """Add learners from the selected grade and school to the session."""
        learners = self.env['res.partner.learners'].search([
            ('learner_school_id', '=', self.session_school_id.id),
            ('learner_grade_id', '=', self.session_grade_id.id)
        ])
        existing_learners = self.res_partner_learners_ids.mapped('learner_id')
        new_learners = learners - existing_learners
        for learner in new_learners:
            self.env['res.partner.learners.sessions.rel'].create({
                'learner_id': learner.id,
                'session_id': self.id
            })
    def delete_all_lines_in_res_partner_learners_ids(record):
        record.res_partner_learners_ids = [(6, 0, [])]

    def delete_session_lines(self):
        session_id = self.env.context.get('session_id')
        if session_id:
            self.env['res.partner.learners.sessions.rel'].sudo().search([('session_id', '=', session_id)]).unlink()

    def action_add_teachers_to_session(self):
        """Add teachers from the selected school to the session."""
        teachers = self.env['res.partner.teachers'].search([
            ('teachers_school_id', '=', self.session_school_id.id)
        ])
        self.res_partner_teachers_ids = [(4, teacher.id) for teacher in teachers]