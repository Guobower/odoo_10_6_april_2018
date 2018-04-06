# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ChkBook(models.Model):
    _name = 'cheque.book.maintain'
    _rec_name = 'cheque_no'

    acct_no = fields.Char('Account No.')
    t_amount =  fields.Float('Total Amount')
    bank = fields.Many2one('bank.bank',string="Bank Name")
    cheque_no = fields.Integer(string="Cheque No.")
    cheque_lev = fields.Integer(string="Cheque Leaves.")
    rem_lev = fields.Integer(string="Remainig Leaves.")
    fst_cheque_no = fields.Integer(string="First Cheque No.")
    cheque_tree_id = fields.One2many('cheque.book.tree','chk_tree')

    @api.multi
    def genrate_leaves(self):
        if self.cheque_lev:
            new = self.fst_cheque_no
            for x in range(self.cheque_lev):
                records = self.env['cheque.book.tree'].create({
                    'tree_cheque_no':new,
                    'chk_tree':self.id,
                    })
                new = new + 1 


class ChkBookTree(models.Model):
    _name = 'cheque.book.tree'

    date = fields.Date()
    tree_cheque_no = fields.Char(string="Cheque No.")
    amount =  fields.Float('Total Amount')
    desc =  fields.Char('Description')
    pay_ref =  fields.Char('Payment Reference')
    received =  fields.Char('Received By.')

    chk_tree = fields.Many2one('cheque.book.maintain')


class bank(models.Model):
    _name = 'bank.bank'
    name = fields.Char()

