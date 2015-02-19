# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
import itertools
from lxml import etree
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging

_logger = logging.getLogger(__name__)

class account_analytic_line(models.Model):
    _inherit = "account.analytic.line"
    
    start_time  = fields.Datetime(string="Start time", default=fields.Datetime.now)
    stop_time   = fields.Datetime(string="Stop time")

class hr_analytic_timesheet(models.Model):
    _inherit = "hr.analytic.timesheet"
    
    @api.onchange('start_time', 'stop_time')
    def onchange_timesheet_timer_start_stop_time(self):
        if self.start_time and self.stop_time:
            self.unit_amount = (datetime.strptime(self.stop_time, 
            '%Y-%m-%d %H:%M:%S') - datetime.strptime(self.start_time, 
            '%Y-%m-%d %H:%M:%S')).seconds / 3600.0

class project_work(models.Model):
    _inherit = "project.task.work"
    
    start_time  = fields.Datetime(string="Start time", default=fields.Datetime.now)
    stop_time   = fields.Datetime(string="Stop time")
    
    """
    Overwrite to add start and stop time to timesheet.sheet
    def _create_analytic_entries(self, cr, uid, vals, context):
        
    def write(self, cr, uid, ids, vals, context=None):
    """


    @api.onchange('start_time', 'stop_time')
    def onchange_timesheet_timer_start_stop_time(self):
        if self.start_time and self.stop_time:
            self.hours = (datetime.strptime(self.stop_time, 
            '%Y-%m-%d %H:%M:%S') - datetime.strptime(self.start_time, 
            '%Y-%m-%d %H:%M:%S')).seconds / 3600.0

class project_work_task(models.Model):
    _inherit = "project.task"
    
    @api.one
    def start_stop_work(self):
        work = self.env['project.task.work'].search([['task_id', '=', self.id], ['hours', '=', 0]])
        if len(work) == 0:
            #create new work
            self.env['project.task.work'].create({
            'name': 'foobar',
            'date': fields.Datetime.now(),
            'start_time': fields.Datetime.now(),
            'task_id': self.id,
            'hours': 0,
            'user_id': self.env.user.id,
            'company_id': self.company_id.id,
            })
        elif len(work) == 1:
            work.stop_time = fields.Datetime.now()
            work.onchange_timesheet_timer_start_stop_time()
        else:
            #error
            return False
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: