from odoo import models, fields

class PropertyTag(models.Model):
    _name="estate.property.tags"
    _description="Real Estate Property Tags"
    _order="name asc"

    color=fields.Integer()



    _sql_constraints=[
        ("unique_name","UNIQUE(name)","Tag should be unique!")
    ]
    name = fields.Char(required=True)

