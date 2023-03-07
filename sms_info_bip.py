from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.model.sms_advanced_textual_request import SmsAdvancedTextualRequest
from infobip_api_client.model.sms_destination import SmsDestination
from infobip_api_client.model.sms_response import SmsResponse
from infobip_api_client.model.sms_textual_message import SmsTextualMessage
from infobip_api_client.model.sms_regional_options import SmsRegionalOptions
from infobip_api_client.model.sms_india_dlt_options import SmsIndiaDltOptions
from infobip_api_client.model.sms_textual_message import SmsTextualMessage
from infobip_api_client.api.send_sms_api import SendSmsApi
from infobip_api_client.exceptions import ApiException

"""
 * Send an sms message by using Infobip API.
 *
 * This example is already pre-populated with your account data:
 * 1. Your account Base URL
 * 2. Your account API key
 * 3. Your recipient phone number
 *
 * THIS CODE EXAMPLE IS READY BY DEFAULT. HIT RUN TO SEND THE MESSAGE!
 *
 * Send sms API reference: https://www.infobip.com/docs/api#channels/sms/send-sms-message
 * See Readme file for details.
"""

class SendSMS():
    BASE_URL = "https://k3xexn.api.infobip.com"
    API_KEY = "3325e719c9c3a0ea521c135924b752b3-ab2e6d8f-2233-49fc-a0c7-33599e2ea85e"

    SENDER = "TATALI"

    MESSAGE_TEXT = "Alert {0}, Tata AIA Life Insurance coverage of INR {1} is no longer active for {2} under policy no. {3} due to non-payment of premium. Renew and continue the protection cover for your {4} till you reach age of {5}. Click https://apps.tataaia.com/PG/#!/policyPayment"
    
    CONTENT_TEMPLATE_ID= "1107167444652925628"

   

    client_config = Configuration(
        host= BASE_URL,
        api_key={"APIKeyHeader": API_KEY},
        api_key_prefix={"APIKeyHeader": "App"},
    )

    api_client = ApiClient(client_config)

    def send(self, recipient,name,premium,company,contract,regard,age):
   
        message_text = self.MESSAGE_TEXT.format('DARPAN G BHANDARI','550000','Tata AIA Life Insurance Smart Income Plus','C233288712','loved ones','46')
        message_text  = self.MESSAGE_TEXT.format(name,premium,company,contract,regard,age)
       
        print(message_text)
        
        sms_request = SmsAdvancedTextualRequest(
                messages=[
                    SmsTextualMessage(
                        destinations=[
                            SmsDestination(
                                to=recipient,
                            ),
                        ],
                        _from=self.SENDER,
                        text=message_text,
                        regional=SmsRegionalOptions(
                        india_dlt=SmsIndiaDltOptions(
                        principal_entity_id= "1701158099336122810",  # noqa: E501
                        content_template_id= self.CONTENT_TEMPLATE_ID
                        ))
                        

                    )
                ])

        api_instance = SendSmsApi(self.api_client)

        try:
            api_response: SmsResponse = api_instance.send_sms_message(sms_advanced_textual_request=sms_request)
            print(api_response)
        except ApiException as ex:
            print("Error occurred while trying to send SMS message.")
            print(ex)