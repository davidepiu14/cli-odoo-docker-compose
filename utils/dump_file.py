import yaml

class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)
    
COMPOSE_BLUEPRINT = {
    "version": "3.1",
    
    "services":  {
        "web": 
            {
            "image": "odoo:14.0",
            "depends_on": ["db"],
            "ports": ["8069:8069", "8072:8072"],
            "volumes": [
                "./:/mnt/extra-addons", 
            ]
            },
        "db": 
            {
                "image": "postgres:13",
                "environment" : [
                    "POSTGRES_DB=postgres",
                    "POSTGRES_PASSWORD=odoo",
                    "POSTGRES_USER=odoo"
                ],
                "ports": ["5433:5432"]
            }
    }
}



