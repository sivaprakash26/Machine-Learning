# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 00:01:24 2019

@author: siva1
"""

from flask import Flask, jsonify, request, Response
import json
import os
os.chdir(r'D:\Siva Learning')
from Settings import *

app = Flask(__name__)

Books = [
        {
                'Name' : 'Rich Dad Poor Dad',
                'Price': 200,
                'ISBN': 100
        },
        {
                'Name' : 'I too had a love story',
                'Price': 450,
                'ISBN': 200
        }        
        ]

def valid_book_object(bookobject):
    if ("Name" in bookobject and "Price" in bookobject and "ISBN" in bookobject):
        return True
    else:
        return False

#Get Book Info
@app.route('/books')
def Get_Books():
    return jsonify({'books' : Books})
    
@app.route('/books', methods = ['POST'])
def Add_books():
    request_data = request.get_json()
    if valid_book_object(request_data):
        new_book = {
                        "Name": request_data["Name"],
                        "Price": request_data["Price"],
                        "ISBN": request_data["ISBN"]
                }
        Books.insert(0, new_book)
        response = Response("", 201, mimetype = "application/json")
        response.headers["Location"] = "/books/"+str(new_book["ISBN"]) 
        return response
    else:
        invalidDataObjectException = {
                "Error" : "Data Object not formed correctly",
                "Message": "Pass the data object in the specified format : {'Name':'Book Name', 'Price', 'Book Price', 'ISBN': 'Book ISBN'}"}
        response = Response(json.dumps(invalidDataObjectException), 400, mimetype = "application/json")
        return response
    
@app.route("/books/<int:isbn>", methods = ["PUT"])
def Update_Books(isbn):
    request_data = request.get_json()
    new_book = {
            "Name": request_data["Name"],
            "Price": request_data["Price"],
            "ISBN": isbn            
            }
    i = 0
    for book in Books:
        book_isbn = book["ISBN"]
        if book_isbn == isbn:
            Books[i] = new_book
        i+=1
    response = Response("", 204, mimetype = "application/json")
    return response
    

@app.route("/books/<int:isbn>", methods = ["PATCH"])
def Update_Books_fields(isbn):
    request_data = request.get_json()
    updated_book = {}
    if 'Name' in request_data:
        updated_book["Name"] = request_data["Name"]
    if 'Price' in request_data:
        updated_book["Price"] = request_data["Price"]
    for book in Books:
        if isbn == book["ISBN"]:
            book.update(updated_book)
    response = Response("", status = 204)
    response.headers["Location"] = "/books/"+str(isbn)
    return response


@app.route("/books/<int:isbn>", methods = ["DELETE"])
def Delete_Books(isbn):
    i = 0
    for book in Books:
        if isbn == book["ISBN"]:
            Books.pop(i)
            response = Response("", status = 200)
            return response
        i += 1
    invalid_error = {
            "Error":"Book with the provided ISBN was not found"}
    response = Response(json.dumps(invalid_error), status = 404, mimetype="application/json")
    return response
        

#Get Book by ISBN
@app.route("/books/<int:isbn>")
def Get_book_by_ISBN(isbn):
    return_book = {}
    for book in Books:
        if book['ISBN'] == isbn:
            return_book = {
                    'Name' : book['Name'],
                    'Price' : book['Price']
                    }
    return jsonify(return_book)
            
app.run()