from odoo import models, fields,api,_

class PropertyType(models.Model):
    _name="property.type"
    _description="Real Estate Property Type"
    _order="sequence desc"
    _sql_constraints=[
        ("check_name","CHECK(name)","Property Type Should be Unique!")
    ]



    name=fields.Char(required=True)
    property_ids=fields.One2many("realstate.property","property_type_id")
    sequence=fields.Integer()
    offer_ids=fields.One2many("property.offer","property_type_id")

    offer_count=fields.Integer(compute="_compute_offer_count",store=True)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count=len(rec.offer_ids)

    def open_offer_view(self):
        return{
            "name":_("Related Lines"),
            "type":"ir.actions.act_window",
            "view_mode":"list,form",
            "res_model":"property.offer",
            "target":"current",
            "domain":[("property_type_id",'=',self.id)],
            "context":{"default_property_type_id":self.id}


        }