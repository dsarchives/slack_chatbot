import os
from slackclient import SlackClient
from flask import Response
import dialogflow
from config import SLACK_TOKEN_CHANNEL, credential_path

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def list_channels():
    slack_client = SlackClient(SLACK_TOKEN_CHANNEL)
    channels_call = slack_client.api_call("conversations.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def channel_info(channel_id):
    slack_client = SlackClient(SLACK_TOKEN_CHANNEL)
    channel_info = slack_client.api_call("conversations.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None


def channel_text(channel_id):
    slack_client = SlackClient(SLACK_TOKEN_CHANNEL)
    channel_msg = slack_client.api_call("conversations.history", channel=channel_id)
    if channel_info:
        return channel_msg['messages'][0]
    return None


def send_message(channel_id, response):
    slack_client = SlackClient(SLACK_TOKEN_CHANNEL)
    if response['fulfillmentMessages']:
        final_text = response['fulfillmentMessages'][0]['text']['text'][0]

        slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=final_text
        )
    # if response.get('blocks') is not None:
    #     slack_client.api_call(
    #         "chat.postMessage",
    #         channel=channel_id,
    #         blocks=response['blocks']
    #     )
    #
    # if response.get('attachments') is not None:
    #     slack_client.api_call(
    #         "chat.postMessage",
    #         channel=channel_id,
    #         attachments=response['attachments']
    #     )

    return Response(), 200


def send_message_as_user(channel_id, response):
    slack_client = SlackClient(SLACK_TOKEN_CHANNEL)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=response,
        as_user=True
        # icon_emoji=':new_moon_with_face:'
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)         # getting text input
        query_input = dialogflow.types.QueryInput(text=text_input)  # preparing query input for intent detection
        response = session_client.detect_intent(
            session=session, query_input=query_input)       # preparing response

        return response.query_result                        # accessing query


