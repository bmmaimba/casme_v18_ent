# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class ResPartnerLearners(models.Model):
    _name = "res.partner.learners"
    _description = 'Learners'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    #Inherited Partner for Contacts.
    partner_id = fields.Many2one('res.partner', ondelete='restrict', auto_join=True, required=True,
                                 string='RelatedPartner', help='Contact-related to Learner')
    #Learners Fields
    # company_type = fields.Selection([('person','Individual'),('company','Company')], default="person")
    learner_fname = fields.Char('First Name', tracking=True)
    learner_surname = fields.Char('Surname', tracking=True)
    learner_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], tracking=True)
    learner_race = fields.Selection([
        ('A', 'African'),
        ('C', 'Coloured'),
        ('I', 'Indian'),
        ('W', 'White'),
        ('O', 'Other')
    ], tracking=True)
    disability_status = fields.Selection([
        ('sight', 'Sight ( even with glasses )'),
        ('hearing', 'Hearing ( even with h.aid )'),
        ('communication', 'Communication ( talk/listen)'),
        ('physical', 'Physical ( move/stand, etc)'),
        ('intellectual', 'Intellectual ( learn,etc)'),
        ('emotional', 'Emotional ( behav/psych)'),
        ('multiple', 'Multiple'),
        ('disabled', 'Disabled but unspecified'),
        ('none', 'None'), ], string='Disability Status', default='none')
    learner_phone = fields.Char('Phone', size=10)
    learner_mobile = fields.Char('Mobile', size=10, tracking=True)
    learner_email = fields.Char('Email', tracking=True)
    learner_rsa_id_number = fields.Char('ID Number', size=13, tracking=True)
    learner_unique_id = fields.Char('Unique Learner Id ', tracking=True)
    learner_dob = fields.Date(string="Date of Birth", store=True)
    learner_age = fields.Integer(string="Age", store=True)
    learner_school_id = fields.Many2one('res.partner.schools', ondelete='restrict', auto_join=True, store=True, tracking=True,
                                  string='School', help='School')
    learner_grade_id = fields.Many2one('school.grades', ondelete='restrict', auto_join=True, store=True, tracking=True,
                                  string='Grade', help='Grade')

    @api.onchange('learner_fname', 'learner_surname')
    def onchange_learner_name(self):
        self.name = str(self.learner_fname) + ' ' + str(self.learner_surname)

    @api.model_create_multi
    def create(self, vals):
        # Ensure the partner_id is provided or create a new partner with the full name
        if not vals.get('partner_id'):
            partner_vals = {
                'name': vals.get('learner_fname', '') + ' ' + vals.get('learner_surname', ''),
                'email': vals.get('learner_email', ''),
                'phone': vals.get('learner_phone', ''),
                'mobile': vals.get('learner_mobile', ''),
                'company_type': vals.get('company_type', 'person'),
            }
            partner = self.env['res.partner'].create(partner_vals)
            vals['partner_id'] = partner.id  # Link the partner_id to the new partner
        # Create the ResPartnerLearners record with the updated vals
        res = super(ResPartnerLearners, self).create(vals)
        # Now update the partner fields with learner information
        res.partner_id.email = res.learner_email
        res.partner_id.phone = res.learner_phone
        res.partner_id.mobile = res.learner_mobile
        res.partner_id.company_type = res.company_type
        #     #if res.is_learner_school:
        #         #res.partner_id.is_school = True
        #         #res.partner_id.ref = res.sdl_number
        return res

    def write(self, vals):
        # Update the partner's fields based on the changes in the ResPartnerLearners model
        if vals.get('learner_fname') or vals.get('learner_surname'):
            learner_fname = vals.get('learner_fname', self.learner_fname)
            learner_surname = vals.get('learner_surname', self.learner_surname)
            # Update the partner's name
            self.partner_id.name = f"{learner_fname} {learner_surname}"
        if vals.get('learner_email'):
            self.partner_id.email = vals.get('learner_email')
        if vals.get('learner_phone'):
            self.partner_id.phone = vals.get('learner_phone')
        if vals.get('learner_mobile'):
            self.partner_id.mobile = vals.get('learner_mobile')
        if vals.get('learner_rsa_id_number'):
            self.partner_id.ref = vals.get('learner_rsa_id_number')
        if vals.get('company_type'):
            self.partner_id.company_type = vals.get('company_type')
        # Call the parent write method to apply the changes to the ResPartnerLearners model
        return super(ResPartnerLearners, self).write(vals)
