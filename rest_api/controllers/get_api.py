from odoo import http

class HellowApi(http.Controller):
    ## Generate QR
    @http.route('/generate_qr', type='json', auth='public', website=False, csrf=False, methods=['GET','POST'])
    def generate(self, **kw):
        return "QR Generado. OK."
    
    @http.route('/example', type='json', auth='public', website=False, csrf=False, methods=['GET','POST'])
    def example(self, **kw):
        contact_list =[
            {
            'name':"Miguel",
            'last_name':"Zelaya",
            'email':"miguelzelaya99@gmail.com"
            },
            {
            'name':"Jackyr",
            'last_name':"Discua",
            'email':"jackyrdc@gmail.com"
            },
            {
            'name':"Suyapa",
            'last_name':"Santos",
            'email':"santos@gmail.com"
            }
            ]
        return contact_list
    
    @http.route('/get/contacts', type='json', auth='public', website=False, csrf=False, methods=['GET','POST'])
    def contacts(self, **kw):

        contacts = http.request.env['res.partner'].sudo().search([])

        contact_list = []
        for contact in contacts:
            contact_list.append(
            {
                'name': contact.name,
                'email': contact.email,
                'name': contact.name,
            })
        return contact_list
    
    
    