from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import sqlite3

app = Flask(__name__)

# creating a connection with db and create table
connection = sqlite3.connect("contactus.db")
create_table_query = "CREATE TABLE IF NOT EXISTS CONTACT (name TEXT, email TEXT,message TEXT)"
connection.execute(create_table_query)
create_table_crop = '''CREATE TABLE IF NOT EXISTS CROP (
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            mob TEXT NOT NULL,
            address TEXT,
            type TEXT NOT NULL,
            description TEXT,
            soil_ph BOOLEAN DEFAULT 0,
            nutrient_analysis BOOLEAN DEFAULT 0,
            pesticide_residue BOOLEAN DEFAULT 0,
            water_quality BOOLEAN DEFAULT 0,
            heavy_metal_contamination BOOLEAN DEFAULT 0,
            other BOOLEAN DEFAULT 0,
            info TEXT)'''
connection.execute(create_table_crop)


# Define responses for the chatbot
responses = {
    "hi": ["Hello! How can I assist you with agriculture today?", "Hi there! How can I help you?"],
    "how to grow": ["Growing crops requires good soil, adequate water, and sunlight. Let me know if you need details."],
    "best crops for": ["It depends on the climate and soil of your location. Let me know if you need specific suggestions."],
    "thank you": ["You're welcome! Let me know if you have more questions." "Glad to help!"],
    "what are kharif, rabi, and zaid crops?": [ "Kharif crops are sown with the onset of the monsoon and harvested at the end of the rainy season, like rice and maize. Rabi crops are sown after the monsoon, in winter, and harvested in spring; they include wheat and mustard. Zaid crops grow in the short season between Rabi and Kharif, including melons and cucumbers."],
    "can you explain more about the horticulture crops available?": ["Of course! Our horticulture crops include Avocado from NYC, Saffron from Paris, Litchi from Hong Kong, Sandalwood from Dubai, Mangoes from Tokyo, and Coffee from Singapore. Each is unique and suited to various climates!"],
    "how can i reach your support team?": ["You can contact us via email at info_earthlyendevour@gmail.com or WhatsApp at 9876543210. Additionally, follow us on social platforms like Instagram, LinkedIn, or GitHub!"],
    "what are the most popular crops in the portfolio section?":["We have kharif,rabi and zaid crops."],
    "can i get some farming tips from experts?":["Absolutely! Here’s one tip: 'The ultimate goal of farming is not just to grow crops but to cultivate and perfect human beings.' Another expert says, 'Agriculture is our wisest pursuit as it contributes to wealth, good morals, and happiness.'"],
    "what’s the best season for planting rabi crops?":["Rabi crops are best planted after the monsoon season, typically in winter, and are harvested in spring. They require a cooler climate for optimal growth."],
    "what locations are highlighted for horticulture?":["Our horticulture crops come from diverse locations: New York City for Avocado, Paris for Saffron, Hong Kong for Litchi, Dubai for Sandalwood, Tokyo for Mangoes, and Singapore for Coffee."],
    "do you have any image galleries for your crops?":["Yes, we do! You’ll find an image gallery in the 'Hero' and 'Crop Types' sections on our website, showcasing beautiful images of Kharif, Rabi, Zaid, and other horticultural crops."],
    "how can i book an agricultural consultation?":["To book a consultation, feel free to reach out through our contact form on the 'Contact Us' page. We’ll respond promptly to schedule a convenient time!"],
    "what is earthly endeavour's mission?":["Our mission is to support sustainable agriculture by sharing knowledge, providing crop recommendations, and offering consultations that help both new and seasoned farmers succeed in their agricultural pursuits."],
}

def get_response(user_message):
    for key in responses:
        if key in user_message.lower():
            return random.choice(responses[key])
    return "I'm sorry, I didn't understand that. Can you ask something else?"

# Define routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_message = request.json.get("message")
    response_text = get_response(user_message)
    return jsonify({"response": response_text})

@app.get('/about')
def about():
    return render_template('about.html')

@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/kharif')
def kharif():
    return render_template('kharif.html')

@app.get('/rabi')
def rabi():
    return render_template('rabi.html')

@app.get('/zaid')
def zaid():
    return render_template('zaid.html')

@app.get('/test')
def test():
    return render_template('test.html')

@app.post('/contact')
def handler():
    name = request.form['name']
    email = request.form['email']
    msg = request.form['message']
    # print(name,email,msg)
    with sqlite3.connect('contactus.db') as userdata:
        cursor = userdata.cursor()
        user_info_query = f"INSERT INTO CONTACT VALUES ('{name}','{email}','{msg}')"
        cursor.execute(user_info_query)
        userdata.commit()
    return render_template('index.html',message = "Message sent successfully")

@app.post('/details')
def details():
    name = request.form.get('name')
    email = request.form.get('email')
    mob = request.form.get('mob')
    address = request.form.get('address')
    crop_type = ','.join(request.form.getlist('type'))  # Concatenates selected options
    description = request.form.get('description')
    soil = bool(request.form.get('soil'))
    nutrient = bool(request.form.get('nutrient'))
    pesticide = bool(request.form.get('pesticide'))
    water = bool(request.form.get('water'))
    metal = bool(request.form.get('metal'))
    other = bool(request.form.get('other'))
    info = request.form.get('info')
    with sqlite3.connect('contactus.db') as userdata:
        cursor = userdata.cursor()
        user_info_query = f"INSERT INTO CROP VALUES ('{name}','{email}','{mob}','{address}','{crop_type}','{description}','{soil}','{nutrient}','{pesticide}','{water}','{metal}','{other}','{info}')"
        cursor.execute(user_info_query)
        userdata.commit()
    return render_template('test.html',message = "Message sent successfully")

if __name__ == "__main__":
    app.run(debug=True)
