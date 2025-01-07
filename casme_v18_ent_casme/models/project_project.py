# -*- coding: utf-8 -*-
from odoo import _, models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools import config
from datetime import date, datetime, timedelta
from lxml import etree
from odoo.http import request
from odoo.exceptions import UserError

class ProjectProject(models.Model):
    _inherit = "project.project"

    # name = fields.Char('Year', store=True)