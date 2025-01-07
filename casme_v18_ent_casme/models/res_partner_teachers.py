# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class ResPartnerTeachers(models.Model):
    _name = "res.partner.teachers"
    _description = 'Partner Teachers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    #Inherited Partner for Contacts.
    partner_id = fields.Many2one('res.partner', ondelete='restrict', auto_join=True, required=True,
                                 string='RelatedPartner', help='Contact-related to Teacher')
    #Teachers Fields
    company_type = fields.Selection([('person','Individual'),('company','Company')], default="person")
    teacher_fname = fields.Char('First Name')
    teacher_surname = fields.Char('Surname')
    teacher_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    teacher_race = fields.Selection([
        ('A', 'African'),
        ('C', 'Coloured'),
        ('I', 'Indian'),
        ('W', 'White'),
        ('O', 'Other')
    ])
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
    teacher_phone = fields.Char('Phone', size=10)
    teacher_mobile = fields.Char('Mobile', size=10)
    teacher_email = fields.Char('Email')
    teacher_rsa_id_number = fields.Char('ID Number', size=13)
    teacher_dob = fields.Date(string="Date of Birth", store=True)
    teacher_age = fields.Integer(string="Age", store=True)
    teacher_school_id = fields.Many2one('res.partner.schools', ondelete='restrict', auto_join=True, store=True,
                                  string='Employer', help='School')

    @api.onchange('teacher_fname', 'teacher_surname')
    def onchange_teacher_name(self):
        self.name = str(self.teacher_fname) + ' ' + str(self.teacher_surname)

    @api.model_create_multi
    def create(self, vals):
        # Ensure the partner_id is provided or create a new partner with the full name
        if not vals.get('partner_id'):
            partner_vals = {
                'name': vals.get('teacher_fname', '') + ' ' + vals.get('teacher_surname', ''),
                'email': vals.get('teacher_email', ''),
                'phone': vals.get('teacher_phone', ''),
                'mobile': vals.get('teacher_mobile', ''),
                'company_type': vals.get('company_type', 'person'),
            }
            partner = self.env['res.partner'].create(partner_vals)
            vals['partner_id'] = partner.id  # Link the partner_id to the new partner
        # Create the ResPartnerTeachers record with the updated vals
        res = super(ResPartnerTeachers, self).create(vals)
        # Now update the partner fields with teacher information
        res.partner_id.email = res.teacher_email
        res.partner_id.phone = res.teacher_phone
        res.partner_id.mobile = res.teacher_mobile
        res.partner_id.company_type = res.company_type
        #     #if res.is_teacher_school:
        #         #res.partner_id.is_school = True
        #         #res.partner_id.ref = res.sdl_number
        return res

    def write(self, vals):
        # Update the partner's fields based on the changes in the ResPartnerTeachers model
        if vals.get('teacher_fname') or vals.get('teacher_surname'):
            teacher_fname = vals.get('teacher_fname', self.teacher_fname)
            teacher_surname = vals.get('teacher_surname', self.teacher_surname)
            # Update the partner's name
            self.partner_id.name = f"{teacher_fname} {teacher_surname}"
        if vals.get('teacher_email'):
            self.partner_id.email = vals.get('teacher_email')
        if vals.get('teacher_phone'):
            self.partner_id.phone = vals.get('teacher_phone')
        if vals.get('teacher_mobile'):
            self.partner_id.mobile = vals.get('teacher_mobile')
        if vals.get('teacher_rsa_id_number'):
            self.partner_id.ref = vals.get('teacher_rsa_id_number')
        if vals.get('company_type'):
            self.partner_id.company_type = vals.get('company_type')
        # Call the parent write method to apply the changes to the ResPartnerTeachers model
        return super(ResPartnerTeachers, self).write(vals)
