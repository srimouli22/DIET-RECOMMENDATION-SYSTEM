import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'client.json'

def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service




def add_event(mail,diet):
   # creates one hour event tomorrow 10 AM IST
   service = get_calendar_service()
   start_time = datetime(2021, 12, 15, 12, 30, 0)
   end_time = start_time + timedelta(hours=4)
   timezone = 'Asia/Kolkata'

   event = {
       'summary': 'IPL 2021',
       'location': 'abu dhabi',
       'description': diet,
       'start': {
           'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
           'timeZone': timezone,
       },
       'end': {
           'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
           'timeZone': timezone,
       },
       'attendees': [
           {'email': mail },
       ],
       'reminders': {
           'useDefault': False,
           'overrides': [
               {'method': 'email', 'minutes': 24 * 60},
               {'method': 'popup', 'minutes': 10},
           ],
       },
   }
   event_result = service.events().insert(calendarId='poojasalapu@gmail.com', body=event).execute()










