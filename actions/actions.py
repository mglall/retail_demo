from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import requests
import json
import urllib.request
# change this to the location of your SQLite file


#class SurveySubmit(Action):
#    def name(self) -> Text:
#        return "action_survey_submit"
#    async def run(
#        self,
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#       domain: Dict[Text, Any],
#   ) -> List[Dict[Text, Any]]:

#       dispatcher.utter_message(template="utter_open_feedback")
#        dispatcher.utter_message(template="utter_survey_end")
#        return [SlotSet("survey_complete", True)]


class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

       

        # get email slot
        email = (tracker.get_slot("email"))
        email = email.replace("(","").replace(")","")
        email = email.strip('"')


        # connect to api
        r = requests.get(f"https://orderes.herokuapp.com/api/todo/{email}")
                
        data_row = r.json()

        if data_row:
            # convert tuple to list
            data_list = list(data_row.items())

            # respond with order status
            dispatcher.utter_message(response ="utter_order_status",status=data_list[9][1])
            
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response ="utter_no_order")
            
            return []



class CancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get email slot
        email = (tracker.get_slot("email"))
        email = email.replace("(","").replace(")","")
        email = email.strip('"')

        # connect to api

        response = requests.put(f"https://orderes.herokuapp.com/api/todo/{email}?status=cancelled")
        response = response.json()
        response = list(response.items())
       
        if response[9][1]=="cancelled":
            
            # confirm cancellation
            dispatcher.utter_message(response ="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response ="utter_no_order")
            return []


class ReturnOrder(Action):
    def name(self) -> Text:
        return "action_return"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get email slot
        email = (tracker.get_slot("email"))
        email = email.replace("(","").replace(")","")
        email = email.strip('"')

        # connect to api

        r = requests.get(f"https://orderes.herokuapp.com/api/todo/{email}")
        data_row = r.json()

        if data_row:
            # change status of entry
            requests.put(f"https://orderes.herokuapp.com/api/todo/{email}?status=returning")
           
            # confirm return
            dispatcher.utter_message(response ="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response ="utter_no_order")
            
            return []


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        

        # get slots and save as var
        model = (tracker.get_slot("model"))  
        capacity = (tracker.get_slot("capacity"))
        colors = (tracker.get_slot("colors"))
        # place cursor on correct row based on search criteria
        r = requests.get(f"https://iphoneapi.herokuapp.com/api/todo/{model}/{capacity}/{colors}")
        data_row = r.json()
        
        
        if len(data_row) >3 :
            # provide in stock message
            dispatcher.utter_message(response ="utter_in_stock")
            slots_to_reset = ["model", "capacity", "colors"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(response ="utter_no_stock")
            slots_to_reset = ["model", "capacity", "colors"]
            return [SlotSet(slot, None) for slot in slots_to_reset]




class ActionColorsAvailable(Action):
    def name(self) -> Text:
        return "action_colors_available"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        

        # get slots and save as var
        model = (tracker.get_slot("model"))  
        
        # fetch data from iphone mongodb collections
        data = requests.get(f"https://iphoneapi.herokuapp.com/api/todo/{model}")
        data_ro = data.json()
        color = []
        for i in data_ro:
            if i["colors"] not in color:
                color.append(i["colors"])
         
        
        
        if data_ro:        
            
            # respond with colors available
            dispatcher.utter_message(text =f"the available colors for {model} is {color}")
            return []

        else:
            # db didn't have an entry with this model
            dispatcher.utter_message(response ="utter_no_stock")
            return []


class ActionCapacityAvailable(Action):
    def name(self) -> Text:
        return "action_capacity_available"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        

        # get slots and save as var
        model = (tracker.get_slot("model"))  
        
        # place cursor on correct row based on search criteria
        data = requests.get(f"https://iphoneapi.herokuapp.com/api/todo/{model}")
        data_run = data.json()
        storage = []
        for i in data_run:
            if i["capacity"] not in storage:
                storage.append(i["capacity"])
        
        
        if data_run:        

            # respond with order status
            dispatcher.utter_message(text =f"the capacity available for {model} is {storage}")
            
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response ="utter_no_stock")
            
            return []

