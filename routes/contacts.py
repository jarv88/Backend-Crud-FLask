from flask import Blueprint, render_template, request,make_response,jsonify
from models.contact import Contact
from utils.db import db
contacts = Blueprint("contacts", __name__)


@contacts.route("/")
def index():
    return "h" #render_template("index.html")


@contacts.route("/info")
def info():
    contactos = Contact.query.all()
    response = []
    for c in contactos:
        print(c.fullname)
        d1 = {
        "Fullname": c.fullname,
        "email": c.email,
        "Phone": c.phone
        }
        response.append(d1)
    return make_response(jsonify(response)), 200


@contacts.route("/info/<id>", methods=['GET'])
def single_info(id):
    try:

        single_contact = Contact.query.get(id)
        d = {
            "Fullname": single_contact.fullname,
            "email": single_contact.email,
            "Phone": single_contact.phone        
        }
        return make_response(jsonify(d)), 200
    except:
        return make_response(jsonify("Id no encontrado")), 200
    
@contacts.route("/new", methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    token = request.headers.get('token') 
    fullname = new_contact['fullname']
    email = new_contact['email']
    phone = new_contact['phone']
    print(token)
    new_contact =Contact(fullname,email,phone)
    db.session.add(new_contact)
    db.session.commit()
    response= {
        "Mensaje": "Exitoso",
        "Id": new_contact.id
    }
    return make_response(jsonify(response)), 200

@contacts.route("/update", methods=['PUT'])
def update_contact():
    contact_for_update = request.get_json()
    try:
            
        contact = Contact.query.get(contact_for_update['id'])
        print (contact_for_update['id'])
        contact.fullname = contact_for_update['fullname']
        contact.email = contact_for_update['email']
        contact.phone = contact_for_update['phone']

        db.session.commit()
    except:
        return make_response(jsonify("No existente")), 200
    return make_response(jsonify("Exitoso")), 200


@contacts.route("/delete", methods=['DELETE'])
def delete_contact():
    contact_for_delete = request.get_json()
    try:
        contact = Contact.query.get(contact_for_delete['id'])
        db.session.delete(contact)
        db.session.commit()
    except:
        return make_response(jsonify("No existente")), 200
    return make_response(jsonify("Borrado exitoso")), 200