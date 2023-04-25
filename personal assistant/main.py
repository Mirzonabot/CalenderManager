from flask import Flask, render_template, request, jsonify
import openai
import json
import jira

openai.api_key = "API_KEY"



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/save-audio', methods=['POST'])
def save_audio():
    audio_data = request.get_data()
    with open('audio.webm', 'wb') as f:
        f.write(audio_data)
    # response = "[{\"time_of_day\": \"morning\", \"task\": \"wake up\"}, {\"time_of_day\": \"morning\", \"task\": \"brush teeth\"}, {\"time_of_day\": \"morning\", \"task\": \"eat breakfast\"}, {\"time_of_day\": \"morning\", \"task\": \"go to school\"}, {\"time_of_day\": \"afternoon\", \"task\": \"go to school\"}, {\"time_of_day\": \"afternoon\", \"task\": \"eat lunch\"}, {\"time_of_day\": \"afternoon\", \"task\": \"go to school\"}, {\"time_of_day\": \"evening\", \"task\": \"go to school\"}, {\"time_of_day\": \"evening\", \"task\": \"eat dinner\"}, {\"time_of_day\": \"evening\", \"task\": \"go to sleep\"}]"
    response = trascribe()
    print(json.loads(response))
    return jsonify({'message': 'Audio saved successfully',
                    'tasks': json.loads(response)})
def trascribe():
    audio_file= open("audio.webm", "rb")

    transcript = openai.Audio.transcribe("whisper-1",audio_file)
    print(transcript)

    string_transcript = str(transcript)



    print(string_transcript)

    template = "\""+string_transcript + "f\" This is the desription of a jira tiket. Can you rephrase it and make sure the response is in the following json format: {'summary':'##summary','description':'##description','issue_type':'##issue_type','priority':'##priority'}"


    model = "text-davinci-002"
    temperature = 0.5

    response = openai.Completion.create(
        engine=model,
        prompt=template,
        temperature=temperature,
        max_tokens=300
    )
    print(response)
    print(response.choices[0].text)
    return response.choices[0].text

# def add_jira_task():




# trascribe()


if __name__ == '__main__':
    app.run()
