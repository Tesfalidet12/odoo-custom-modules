from datetime import timedelta

from odoo import models,fields,api,_
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name="property.offer"
    _description="Property Offer"
    _order="price desc"

    price=fields.Float(required=True)
    status=fields.Selection([
        ("accept","Offer Accepted"),
        ("refuse","Offer Refuse")
    ])
    partner=fields.Many2one("res.partner")
    property_id=fields.Many2one("realstate.property")
    validity=fields.Integer(default=7)
    deadline_date=fields.Date(compute="_compute_deadline_date", inverse="_inverse_date", store=True)
    property_type_id=fields.Many2one("property.type")





    @api.depends("validity")
    def _compute_deadline_date(self):
        for rec in self:
            if rec.create_date:
                rec.deadline_date=rec.create_date.date() + timedelta(days=rec.validity)
            else:
                rec.deadline_date=fields.Date.today() + timedelta(days=rec.validity)


    def _inverse_date(self):
        for rec in self:
            if rec.create_date and rec.deadline_date:
                rec.validity=(rec.deadline_date - rec.create_date.date()).days
            else:
                rec.validity = 7



    def action_accept(self):
        self.ensure_one()
        if "accept" in self.property_id.offer_ids.mapped("status"):
            raise UserError(_("Only one offer can be accepted per property"))
        self.status="accept"
        self.property_id.buyer_id=self.partner
        self.property_id.selling_price=self.price
        self.property_id.state="accepted"
    def action_refuse(self):
        self.ensure_one()
        self.status="refuse"

    _sql_constraints=[
        ("check_price","CHECK(price > 0)","Price Should be Positive!")
    ]

    def create(self,vals):
        self.property_id.state="accepted"
        if self.price < max(self.mapped("price")):
            raise UserError(_("Offered is less than received before!"))
        return super().create(vals)
