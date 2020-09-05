import os, json
from flask import request, Response, Flask
from app import detect_intent_texts, send_message, channel_info, list_channels, make_slack_response, \
    send_message_as_user, channel_text
from google.protobuf.json_format import MessageToDict
from config import SLACK_WEBHOOK_SECRET, credential_path, project_id

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# config setup and set secret key
application = Flask(__name__)

application.config.from_pyfile('config.py')

@application.route('/slack/actions', methods=['POST'])
def actions():
    if request.method == 'POST':
        try:
            parsed_json = request.form['payload']
            json_data = json.loads(parsed_json)
            response = json_data['actions'][0]['selected_options'][0]['value']
            # response = json_data['actions'][0]['value']   [use this to get button response]
            send_message_as_user('CT559GGSD', response)
            return Response(), 200
        except Exception as e:
            print(e)
    return Response(), 200


@application.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
    return Response(), 200


@application.route('/slack/send_msg', methods=['POST', 'GET'])
def send_msg():
    try:
        channel_data = channel_info('C01AV5KCA1W')
        channel_history = channel_text('C01AV5KCA1W')
        if channel_history['user'] == 'U01A27S0WMB':
            user_intent = detect_intent_texts(project_id, "unique",
                                              channel_history['text'],
                                              'en')
            dict_data = MessageToDict(message=user_intent)
            response = dict_data
            send_message('C01AV5KCA1W', response)
        return Response(), 200
    except Exception as e:
        print(e)


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(debug=True)
