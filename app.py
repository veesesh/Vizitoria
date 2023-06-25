from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Create a connection to MongoDB
client = MongoClient('mongodb+srv://veesesh:pawanfanikkada@cluster0.9wi8jx6.mongodb.net/')
db = client['visitor_management']

# Initialize Twilio client
twilio_client = Client('AC030ceb2e77676aa35c2ea83e177fa05e', '519c357831fbe52193bcf6f44c5cff8a')
twilio_phone_number = '+14155238886'  # Your Twilio phone number for sending messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get the visitor information from the form
            name = request.form.get('name')
            contact = request.form.get('contact')
            reason = request.form.get('reason')
            
            # Create a visitor document
            visitor = {
                'name': name,
                'contact': contact,
                'reason': reason
            }
            
            # Insert the visitor document into the 'visitors' collection
            db.visitors.insert_one(visitor)
            
            # Send a WhatsApp message to the staff member using Twilio
            twilio_client.messages.create(
                from_='whatsapp:' + twilio_phone_number,
                body=f"New visitor registration:\nName: {name}\nContact: {contact}\nReason: {reason}",
                to='whatsapp:+918260964309'
            )
            
            # Redirect to the response page with a success message
            return redirect('/response?status=success')
        
        except Exception as e:
            print(f"An error occurred during registration: {str(e)}")
            return 'Registration Failed! Please try again later.'
    
    return render_template('register.html')

@app.route('/response', methods=['GET', 'POST'])
def response():
    if request.method == 'GET':
        status = request.args.get('status')
        if status == 'success':
            return render_template('response.html', response='Registration Successful!')
        else:
            return render_template('response.html', response='Registration Failed! Please try again later.')
    elif request.method == 'POST':
        return render_template('response.html', response=request.form.get('response'))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming message content
    incoming_message = request.form.get('Body', '')
    sender_phone_number = request.form.get('From', '')

    # Process the incoming message
    response = process_message(incoming_message, sender_phone_number)

    return render_template('response.html', response=response)


def process_message(message, sender_phone_number):
    # Retrieve the visitor's document from the 'visitors' collection
    visitor = db.visitors.find_one({'contact': sender_phone_number})

    if visitor:
        # Update the visitor's document with the response
        db.visitors.update_one({'_id': visitor['_id']}, {'$set': {'response': message}})

        # Return the response message
        return f"Response received:\n{message}"
    else:
        return "No visitor found with the provided contact number."


if __name__ == '__main__':
    app.run(debug=True)






# from flask import Flask, render_template, request
# from pymongo import MongoClient
# from twilio.rest import Client

# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Create a connection to MongoDB:
# client = MongoClient('mongodb+srv://veesesh:pawanfanikkada@cluster0.9wi8jx6.mongodb.net/')

# # Access the desired database:
# # Replace 'your-database-name' with the name of your MongoDB database.
# db = client['visitor_management']

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         try:
#             # Get the visitor information from the form
#             name = request.form.get('name')
#             contact = request.form.get('contact')
#             reason = request.form.get('reason')
            
#             # Create a visitor document
#             visitor = {
#                 'name': name,
#                 'contact': contact,
#                 'reason': reason
#             }
            
#             # Insert the visitor document into the 'visitors' collection
#             db.visitors.insert_one(visitor)
            
#             # Send a WhatsApp message to the staff member using Twilio
#             # initialize
#             twilio_client = Client('AC030ceb2e77676aa35c2ea83e177fa05e', '519c357831fbe52193bcf6f44c5cff8a')

#             twilio_client.messages.create(
#                 from_='whatsapp:+14155238886',
#                 body=f"New visitor registration:\nName: {name}\nContact: {contact}\nReason: {reason}",
#                 to='whatsapp:+918260964309'
#             )
            
#             return 'Registration Successful!'
        
#         except Exception as e:
#             print(f"An error occurred during registration: {str(e)}")
#             return 'Registration Failed! Please try again later.'
    
#     return render_template('register.html')

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # Get the incoming message content
#     incoming_message = request.form.get('Body', '')
#     sender_phone_number = request.form.get('From', '')

#     # Process the incoming message
#     response = process_message(incoming_message, sender_phone_number)

#     # Generate a TwiML response
#     twiml_response = MessagingResponse()
#     twiml_response.message(response)

#     return str(twiml_response)

# def process_message(message, sender_phone_number):
#     # Process the message content and sender's phone number
#     # Add your logic here
#     # You can query the database, generate an ID card, and send a response message
    
#     response_message = "Thank you for your message. We will process your request."

#     return response_message


# if __name__ == '__main__':
#     app.run(debug=True) 

# NEW CODE WITH APISCHEDULER 

# from flask import Flask, render_template, request
# from pymongo import MongoClient
# from twilio.rest import Client
# from twilio.twiml.messaging_response import MessagingResponse
# from apscheduler.schedulers.background import BackgroundScheduler

# app = Flask(__name__)

# # Create a connection to MongoDB
# client = MongoClient('mongodb+srv://veesesh:pawanfanikkada@cluster0.9wi8jx6.mongodb.net/')
# db = client['visitor_management']
# security_notifications = db['security_notifications']

# # Initialize Twilio client
# twilio_client = Client('AC030ceb2e77676aa35c2ea83e177fa05e', '519c357831fbe52193bcf6f44c5cff8a')
# twilio_phone_number = '+14155238886'  # Your Twilio phone number for sending messages

# def send_notification_to_security(visitor):
#     message = f"Visitor Request Update:\nName: {visitor['visitor_name']}\nContact: {visitor['sender_phone_number']}\nHOD Response: {visitor['response']}"
#     security_phone_number = '+919441229988'  # Replace with the security personnel's phone number
#     twilio_client.messages.create(
#         from_='whatsapp:' + twilio_phone_number,
#         body=message,
#         to='whatsapp:' + security_phone_number
#     )


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         try:
#             # Get the visitor information from the form
#             name = request.form.get('name')
#             contact = request.form.get('contact')
#             reason = request.form.get('reason')

#             # Create a visitor document
#             visitor = {
#                 'name': name,
#                 'contact': contact,
#                 'reason': reason,
#                 'hod_response': None  # Initialize HOD response as None
#             }

#             # Insert the visitor document into the 'visitors' collection
#             db.visitors.insert_one(visitor)

#             # Send a WhatsApp message to the HOD using Twilio
#             hod_phone_number = '+918260964309'  # Replace with the HOD's phone number
#             twilio_client.messages.create(
#                 from_='whatsapp:' + twilio_phone_number,
#                 body=f"New visitor registration:\nName: {name}\nContact: {contact}\nReason: {reason}",
#                 to='whatsapp:' + hod_phone_number
#             )

#             return 'Registration Successful!'

#         except Exception as e:
#             print(f"An error occurred during registration: {str(e)}")
#             return 'Registration Failed! Please try again later.'

#     return render_template('register.html')

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # Get the incoming message content
#     incoming_message = request.form.get('Body', '')
#     sender_phone_number = request.form.get('From', '')

#     # Process the incoming message
#     response = process_message(incoming_message, sender_phone_number)

#     # Generate a TwiML response
#     twiml_response = MessagingResponse()
#     twiml_response.message(response)

#     return str(twiml_response)

# def process_message(message, sender_phone_number):
#     # Assume the message contains the role and the visitor's name and response
#     # Extract the role, visitor's name, and response from the message
#     role, visitor_name, response = extract_role_visitor_response(message)

#     # Update the visitor's document in the 'visitors' collection with the response
#     db.visitors.update_one({'name': visitor_name}, {'$set': {'response': response}})

#     # Create a new document in the 'messages' collection for the respective role
#     db.messages.insert_one({
#         'role': role,
#         'sender_phone_number': sender_phone_number,
#         'visitor_name': visitor_name,
#         'response': response
#     })

#     # Send a notification to the security phone number
#     send_notification_to_security({'name': visitor_name, 'contact': sender_phone_number, 'hod_response': response})

#     return "Thank you for your response!"

# def send_notifications_to_security():
#     # Retrieve the latest messages from the 'messages' collection for HOD and Director
#     hod_message = db.messages.find_one({'role': 'HOD'}, sort=[('_id', -1)])
#     director_message = db.messages.find_one({'role': 'Director'}, sort=[('_id', -1)])

#     if hod_message:
#         # Send notification to security for HOD's response
#         send_notification_to_security(hod_message)

#     if director_message:
#         # Send notification to security for Director's response
#         send_notification_to_security(director_message)

# if __name__ == '__main__':
#     # Start the background scheduler to send notifications to security personnel every 5 minutes
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(func=send_notifications_to_security, trigger='interval', minutes=5)
#     scheduler.start()

#     app.run(debug=True)





