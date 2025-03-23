from google.cloud import dialogflowcx_v3
from google.cloud.dialogflowcx_v3 import SessionsClient
from google.cloud.dialogflowcx_v3.types import TextInput, QueryInput, DetectIntentRequest
import os

class DialogflowClient:
    def __init__(self):
        self.project_id = "ng-project-102"
        self.location = "global"
        #self.agent_id = "e58d1635-38cf-4fad-b53e-6d1e61ae59c9"
        self.agent_id = "8157d479-b72c-4abe-a955-a28dd6ef6f1d"
        self.agent_path = f"projects/{self.project_id}/locations/{self.location}/agents/{self.agent_id}"
        self.session_client = SessionsClient()
        
    def detect_intent(self, text, session_id):
        """
        Detects the intent of the text input and returns the response
        """
        session_path = f"{self.agent_path}/sessions/{session_id}"
        
        text_input = TextInput(text=text)
        query_input = QueryInput(
            text=text_input,
            language_code="en-US"
        )
        
        request = DetectIntentRequest(
            session=session_path,
            query_input=query_input
        )
        
        response = self.session_client.detect_intent(request)
        return response

    def get_response_text(self, response):
        """
        Extracts the response text from the Dialogflow response
        """
        if response.query_result.response_messages:
            return response.query_result.response_messages[0].text.text[0]
        return "" 