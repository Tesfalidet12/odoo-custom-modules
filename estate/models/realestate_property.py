from dateutil.relativedelta import relativedelta

from odoo import fields, models,api,_

from odoo.exceptions import UserError, ValidationError




class RealState(models.Model):
    _name="realstate.property"
    _description="Realstate Property"
    _order="id desc"

    # def _check_expected_price(self):
    #     for rec in self:
    #         if rec.expected_price <= 0:
    #             raise ValidationError(_("expected price should be positive"))

    def _default_date(self):
        return fields.Date.today() + relativedelta (months=3)


    
    selling_price=fields.Float(default=100000 , readonly=True,required=True)

    availability_date=fields.Date(default=_default_date )
    active=fields.Boolean(default=True)
    state=fields.Selection([
        ("new","New"),
        ("received","Offer Received"),
        ("accepted","Offer Accepted"),
        ("sold","Sold"),
        ("cancel","Canceled")

    ],required=True,default="new")
    description=fields.Char()
    bedroom=fields.Float(default=2)
    title=fields.Char(required=True)
    postcode=fields.Float()
    living_area=fields.Float()
    expected_price=fields.Float(required=True,default=1.0)
    property_type_id=fields.Many2one("property.type")
    buyer_id=fields.Many2one("res.partner")
    sales_person_id=fields.Many2one("res.users")
    offer_ids=fields.One2many("property.offer","property_id" )
    tags_ids=fields.Many2many("estate.property.tags")
    garden_area=fields.Integer()
    total_area=fields.Float(compute="_compute_total_area")
    best_price=fields.Float(compute="_compute_best_price")
    currency_id=fields.Many2one("res.currency")
    offer_set=fields.Boolean(compute="_compute_offer_set")
    # has_offered_accepted=fields.Boolean(compute="_compute_offer_ids_status")


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            prices=rec.offer_ids.mapped("price")
            rec.best_price=max(prices) if prices else 0

    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area=rec.living_area + rec.garden_area


    garden= fields.Boolean()
    garden_orientation=fields.Selection([
        ("north","North"),
        ("south", "South"),
        ("east", "East"),
    ])

    @api.onchange("garden")
    def _onchnage_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area=0
                estate.garden_orientation=""

    @api.onchange("availability_date")
    def _oncchange_availability_date(self):
        for estate in self:
            if estate.availability_date < fields.Date.today():
                return {
                    "warning":{
                        "title":_("Warning"),
                        "message":_("The date is in the past")
                    }
                }




    def action_sold(self):
        self.ensure_one()
        for rec in self:
          if rec.state == "cancel":
                raise UserError(_("Cancelled property can't be sold!"))
          rec.state="sold"

    def action_cancel(self):
        self.ensure_one()
        for rec in self:
            if rec.state == "sold":
                raise UserError(_("Sold property can't be canceled"))
            rec.state="cancel"

    @api.constrains("selling_price","expected_price")
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price <= rec.expected_price:
                raise ValidationError(_("Selling Price Should not be less than 90% expected Price!"))
            if rec.expected_price < 0:
                raise ValidationError(_("Expected Price Must NOT be negative value !"))


    @api.depends("offer_ids")
    def _compute_offer_set(self):
        for rec in self:
            if rec.offer_ids and rec.state=='draft':
                rec.state='received'


    @api.ondelete(at_uninstall=False)
    def _delete_prevention(self):
        for s in self:
            if s.state not in ['new','cancel']:
                raise UserError(_("You Cant Delete This property! "))


