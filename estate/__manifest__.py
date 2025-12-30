{
    "name":"Real State",
    "author":"Tesfalidet",
    "license":"LGPL-3",
    "depends":["base"],
    "demo": [
        "demo/demo.xml"
    ],
    "data":[
        #security
        "security/res_groups.xml" ,
        "security/ir.model.access.csv",
        
        #views
        # "views/realstate_property_views.xml",
        "views/realstate_property_views.xml",
        "views/realestate_property_type.xml",
        "views/realestate_property_tags.xml",
        "views/estate_property_offer.xml",
        "views/realstate_property_menu.xml",
    ],

    "application":True
}