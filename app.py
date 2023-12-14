from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from openai import OpenAI
# import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

db.init_app(app)
app.app_context().push()

client = OpenAI(api_key="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")
# openai.api_key = "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"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(30), nullable=False)
    end = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(255))

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/api/process_command',methods=['GET', 'POST'])
def process_command():
    if request.method == 'POST':
        data = request.get_json()
        # print(data)

        prompt = f"You are a calendar assistant that helps the user manage his or her calendar. You can add events, delete events, and view events. From the following information, give me a string separated by commas that contains the date, event title, start time, end time, and description:{data['command']}"
        
        

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful calendar assistant"},
                  {"role": "user", "content": prompt}],
        # prompt=prompt,
        # temperature=0.75,
        # max_tokens=4,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0.6,
        )

        
        print(response.choices[0].message.content)
        string = response.choices[0].message.content
        parts= string.split(',')
        for part in parts:
            print(part)

        title = parts[0]
        start = parts[1]
        end = parts[2]
        desc = parts[3]

        new_event = Event(
            title=title,
            start=start,
            end=end,
            desc=desc
        )
        db.session.add(new_event)
        db.session.commit()
        # return jsonify({'message': 'Command processed successfully!'})
      # Extract information from the response
        # extracted_info = [s.strip() for s in str(response.choices[0].text).split(',')]
        
        # Return the extracted information
        # return jsonify({
        #     'title': extracted_info[0],
        #     'start': extracted_info[1],
        #     'end': extracted_info[2],
        #     'desc': extracted_info[3],
        #     'message': 'Command processed successfully!'
        # })
        return 'Command processed successfully!'

@app.route('/api/events', methods=['GET', 'POST'])
def events():
    if request.method == 'GET':
        events = Event.query.all()
        event_list = []
        for event in events:
            event_list.append({
                'id': event.id,
                'title': event.title,
                'start': event.start,
                'end': event.end,
                'desc': event.desc
            })
        return jsonify(event_list)
    elif request.method == 'POST':
        data = request.get_json()


        
        new_event = Event(
            title=data['title'],
            start=data['start'],
            end=data['end'],
            desc=data.get('desc', '')
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event added successfully!'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
