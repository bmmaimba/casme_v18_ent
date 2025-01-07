# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class ResPartnerSchools(models.Model):
    _name = "res.partner.schools"
    _description = 'Schools'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    # Inherited Partner for Organisation.
    partner_id = fields.Many2one('res.partner', ondelete='restrict', auto_join=True, required=True,
                                 string='RelatedPartner', help='Contact-related data of the organisation')
    company_type = fields.Selection([('person','Individual'),('company','Company')], default="company")
    natemis_number = fields.Integer(string="NatEmis Number", store=True)
    natemis_province_id = fields.Char(string="Province")
    natemis_city_id = fields.Char(string="City")
    natemis_quintile = fields.Char(string="Quintile")
    res_partner_learners_ids = fields.One2many('res.partner.learners','learner_school_id', string='Learners')

    @api.model_create_multi
    def create(self, vals):
        # Ensure the partner_id is provided or create a new partner with the full name
        if not vals.get('partner_id'):
            partner_vals = {
                'name': vals.get('name', ''),
                'ref': vals.get('natemis_number', ''),
                'company_type': vals.get('company_type', 'person'),
            }
            partner = self.env['res.partner'].create(partner_vals)
            vals['partner_id'] = partner.id  # Link the partner_id to the new partner
        # Create the ResPartnerSchools record with the updated vals
        res = super(ResPartnerSchools, self).create(vals)
        # Now update the partner fields with teacher information
        res.partner_id.company_type = res.company_type
        #     #if res.is_teacher_school:
        #         #res.partner_id.is_school = True
        #         #res.partner_id.ref = res.sdl_number
        return res

    def write(self, vals):
        # Update the partner's fields based on the changes in the ResPartnerSchools model
        if vals.get('name'):
            self.partner_id.name = vals.get('name')
        if vals.get('natemis_number'):
            self.partner_id.ref = vals.get('natemis_number')
        if vals.get('company_type'):
            self.partner_id.company_type = vals.get('company_type')
        # Call the parent write method to apply the changes to the ResPartnerSchools model
        return super(ResPartnerSchools, self).write(vals)
