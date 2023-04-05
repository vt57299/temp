import json
import string
import random
from json import JSONDecodeError
from datetime import datetime,date

def AutoGenerate_EventID():
    #generate a random Event ID
    Event_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Event_ID

def Register(type,member_json_file,organizer_json_file,Full_Name,Email,Password):
    '''Register the member/ogranizer based on the type with the given details'''
    if type.lower()=='organizer':
        f=open(organizer_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
    else:
        f=open(member_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()


def Login(type,members_json_file,organizers_json_file,Email,Password):
    '''Login Functionality || Return True if successful else False'''
    d=0
    if type.lower()=='organizer':
        f=open(organizers_json_file,'r+')
    else:
        f=open(members_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        f.close()
        return False
    for i in range(len(content)):
        if content[i]["Email"]==Email and content[i]["Password"]==Password:
            d=1
            break
    if d==0:
        f.close()
        return False
    f.close()
    return True

def Create_Event(org, events_json_file, Event_Name, Start_Date, Start_Time, End_Date, End_Time, Capacity, Availability):
    '''Create an Event with the details entered by organizer'''
    
    '''Create an event for the given organizer with the given details'''
    Event_ID = AutoGenerate_EventID()
    f = open(events_json_file, 'r+')
    try:
        content = json.load(f)
    except JSONDecodeError:
        content = []
    event = {
        "Event ID": Event_ID,
        "Event Name": Event_Name,
        "Organizer": org,
        "Start Date": Start_Date,
        "Start Time": Start_Time,
        "End Date": End_Date,
        "End Time": End_Time,
        "Users Registered": [],
        "Capacity": Capacity,
        "Availability": Availability
    }
    content.append(event)
    f.seek(0)
    f.truncate()
    json.dump(content, f)
    f.close()



    

def View_Events(org,events_json_file):
    '''Return a list of all events created by the logged in organizer'''
   
    '''Return a list of all events created by the logged in organizer'''

    f = open(events_json_file, 'r')
    try:
        content = json.load(f)
    except JSONDecodeError:
        content = []
    f.close()

    org_events = []
    for event in content:
        if event["Organizer"] == org:
            org_events.append(event)

    return org_events


def View_Event_ByID(events_json_file,event_ID):
    '''Return details of the event for the event ID entered by user'''
    

   
    with open(events_json_file, 'r') as f:
        events = json.load(f)
    for event in events:
        if str(event['Event ID']) == event_ID:
            return event
    return None


    

def Update_Event(org,events_json_file,event_id,detail_to_be_updated,updated_detail):
    '''Update Event by ID || Take the key name to be updated from member, then update the value entered by user for that key for the selected event
    || Return True if successful else False'''
     
   
    
    with open(events_json_file) as f:
        events = json.load(f)
    # Find the event by ID
    for event in events:
        if event['Event ID'] == event_id:
            
            if detail_to_be_updated not in ['Event Name', 'Start Date', 'Start Time', 'End Date', 'End Time','Capacity','Availability']:
                return False
            # Check if the detail value is valid
            if detail_to_be_updated in ['Start Date', 'End Date']:
                try:
                    updated_detail = datetime.strptime(updated_detail, '%Y-%m-%d').date()
                except ValueError:
                    return False
            elif detail_to_be_updated in ['Start Time', 'End Time']:
                try:
                    updated_detail = datetime.strptime(updated_detail, '%H:%M').time()
                except ValueError:
                    return False
            elif detail_to_be_updated == 'Capacity':
                try:
                    updated_detail = int(updated_detail)
                except ValueError:
                    return False
            elif detail_to_be_updated == 'Availability':
                try:
                    updated_detail = int(updated_detail)
                except ValueError:
                    return False
    # Update the event detail
    event[detail_to_be_updated] = updated_detail
    #
    with open(events_json_file, 'w') as f:
        json.dump(events, f, indent=4)
    return True

   

    

    


    

    

   


def Delete_Event(org,events_json_file,event_ID):
    '''Delete the Event with the entered Event ID || Return True if successful else False'''

    


    
    with open(events_json_file) as f:
        events = json.load(f)

    
    for i, event in enumerate(events):
        if event['EventID'] == event_ID and event['Organizer'] == org:
            del events[i]
            break
    else:
        
        return False

    with open(events_json_file, 'w') as f:
        json.dump(events, f)

    return True



def Register_for_Event(events_json_file,event_id,Full_Name):
    '''Register the logged in member in the event with the event ID entered by member. 
    (append Full Name inside the "Users Registered" list of the selected event)) 
    Return True if successful else return False'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    with open(events_json_file, 'r') as f:
        events_data = json.load(f)
        
        for event in events_data:
            if event['Event ID'] == event_id:
                event['Users Registered'].append(Full_Name)
                event['Date Registered'].append(date_today)
                event['Time Registered'].append(current_time)
                
                with open(events_json_file, 'w') as f:
                    json.dump(events_data, f, indent=4)
                
                return True
                
    return False
       

def fetch_all_events(events_json_file,Full_Name,event_details,upcoming_ongoing):
    '''View Registered Events | Fetch a list of all events of the logged in memeber'''
    '''Append the details of all upcoming and ongoing events list based on the today's date/time and event's date/time'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    with open(events_json_file) as f:
        events_data = json.load(f)

    all_events = []
    for event_id, event in events_data.items():
        if Full_Name in event["Users Registered"]:
            event_date = event["Event Date"]
            event_time = event["Event Time"]
            event_datetime = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
            
            if upcoming_ongoing == "upcoming":
                if event_datetime > now:
                    all_events.append((event_id, event))
            elif upcoming_ongoing == "ongoing":
                if event_datetime <= now:
                    all_events.append((event_id, event))
            else:
                all_events.append((event_id, event))

    if all_events:
        event_details["Events"] = {}
        for event_id, event in all_events:
            event_details["Events"][event_id] = event
        return True
    else:
        return False
    

def Update_Password(members_json_file,Full_Name,new_password):
    '''Update the password of the member by taking a new passowrd || Return True if successful else return False'''


    '''Update the password of the member by taking a new passowrd || Return True if successful else return False'''
    with open(members_json_file, 'r') as f:
        members = json.load(f)

    for member in members:
        if member["Full Name"] == Full_Name:
            member["Password"] = new_password
            with open(members_json_file, 'w') as f:
                json.dump(members, f, indent=4)
            return True

    return False


def View_all_events(events_json_file):
    '''Read all the events created | DO NOT change this function'''
    '''Already Implemented Helper Function'''
    details=[]
    f=open(events_json_file,'r')
    try:
        content=json.load(f)
        f.close()
    except JSONDecodeError:
        f.close()
        return details
    for i in range(len(content)):
        details.append(content[i])
    return details
