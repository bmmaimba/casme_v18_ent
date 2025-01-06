# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError
import base64
import io
import json
import xlsxwriter
from odoo.tools import date_utils
import locale


class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  # is_discount_limit = fields.Boolean(string='Discount limit', config_parameter='sale_discount_limit.is_discount_limit',
  #                                    help='Check this field for enabling discount limit')
  # discount_limit = fields.Float(string='Limit amount', config_parameter='sale_discount_limit.discount_limit',
  #                               help='The discount limit amount in percentage')

  @api.model_create_multi
  def read_system_parameter(self):
      #Retrieve a system parameter value by its key
      system_parameter_value = self.env['ir.config_parameter'].get_param('auth_signup.invitation_scope', '')
      #You can convert the value to other data types here if needed
      return system_parameter_value

  @api.model_create_multi
  def update_system_parameter(self):
    custom_value = 'b2b'
    self.env['ir.config_parameter'].set_param('auth_signup.invitation_scope', custom_value)

  auth_signup_uninvited = fields.Selection(default='b2b')