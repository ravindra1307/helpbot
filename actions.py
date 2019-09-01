from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, Restarted

import sqlite3

class action_search_jobs(Action):
    def name(self) -> Text:
        return "action_search_jobs"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        conn = sqlite3.connect('job_data.db')     
        cuisine = tracker.get_slot('skills')
        cuisine = cuisine.replace(' ',',')
        
        if ',' in cuisine:
               result = [x.strip() for x in cuisine.split(',')]
      
        if 'and' in result:
            result.remove('and')
        
        if len(result)>2:       
                q = conn.execute("SELECT DISTINCT company,position from joblistings \
                          WHERE skills_req like '%{}%' or  skills_req like '%{}%' or  skills_req like '%{}%' LIMIT 5\
                          ".format(result[0].lower(),result[1].lower(),result[2].lower()))
        elif len(result)==2:
                q = conn.execute("SELECT DISTINCT company,position from joblistings \
                          WHERE skills_req like '%{}%' or  skills_req like '%{}%' LIMIT 5 \
                          ".format(result[0].lower(),result[1].lower()))
        else:
            q = conn.execute("SELECT DISTINCT company,position from joblistings \
                          WHERE skills_req like '%{}%' LIMIT 5 \
                          ".format(result[0].lower()))


        r=(q.fetchall())
        dispatcher.utter_message("select the position for which you want to enquire")
        buttons = []
        
        for row in r:
            
            title = ("company {} position {}".format(row[0],row[1]))
            payload = ('company {} position {}'.format(row[0],row[1]))
            buttons.append({ "title": title, "payload": payload })
            
        dispatcher.utter_button_message("",buttons)       

class action_search_job_desc(Action):
    def name(self) -> Text:
        return "action_search_job_desc"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      company = tracker.get_slot('company')
      job = tracker.get_slot('job')
      q = conn.execute("select job_description from joblistings where company='{}' and position='{}' ".format(company.lower(),job.lower()))
      
      r=(q.fetchall())
      for row in r:
          x=row[0]
    
      dispatcher.utter_message(x)

class action_greet(Action):
    def name(self) -> Text:
        return "action_greet"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      
      message = (tracker.latest_message)['text']
      sent = [i for i in message.split(' ')]
      
      words = ["wtf",
         "WTF",
         "what the fuck",
         "what the f**k",
         "f*uck",
         "f*uck you",
         "fucker",
         "You suck",
         "I hate you",
         "idiot",
         "stfu",
         "shut the f*** up",
         "f*uk",
         "f**k",
         "fuck",
         "wtf?",
         "wtf bot",
         ]
      
      flag = 0
      for j in sent:    
        if j in words:
            flag = 1    
      if flag==1:
        
        dispatcher.utter_template('utter_out_of_context',tracker)
      else:
        dispatcher.utter_template('utter_greet',tracker)

class action_detail(Action):
    def name(self) -> Text:
        return "action_detail"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      
      name = tracker.get_slot('name')
      dispatcher.utter_message('name is ' + name.lower())
      email = tracker.get_slot('email')
      dispatcher.utter_message('email is ' + email.lower())
      experience = tracker.get_slot('experience')
      dispatcher.utter_message('experience is ' + experience.lower())
      qualification = tracker.get_slot('qualification')
      dispatcher.utter_message('qualification is ' + qualification.lower())
      phone = tracker.get_slot('phone')
      dispatcher.utter_message('phone is ' + phone.lower())

      conn = sqlite3.connect('registration_data.db')     
      
      q = conn.execute("INSERT INTO data (name,email,experience,qualification,phone) VALUES ('{}','{}','{}','{}','{}')"
                 .format(name.lower(),email.lower(),experience.lower(),qualification.lower(),phone.lower()))
      conn.commit()
      conn.close()


class action_questions(Action):
    def name(self) -> Text:
        return "action_questions"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      
      faq = tracker.get_slot('faq')
          #'utter_{}'.format(faq.upper())
      dispatcher.utter_template('utter_{}'.format(faq.upper()),tracker)


class action_search_exp(Action):
    def name(self) -> Text:
        return "action_search_exp"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      company = tracker.get_slot('company')
      job = tracker.get_slot('job')
      q = conn.execute("select exp_req from joblistings where company='{}' and position='{}' ".format(company.lower(),job.lower()))
      
      r=(q.fetchall())
      for row in r:
          x=row[0]
    
      dispatcher.utter_message(x+' years')



class action_search_jobtime(Action):
    def name(self) -> Text:
        return "action_search_jobtime"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      company = tracker.get_slot('company')
      job = tracker.get_slot('job')
      q = conn.execute("select job_time from joblistings where company='{}' and position='{}' ".format(company.lower(),job.lower()))
      
      r=(q.fetchall())
      for row in r:
          x=row[0]
    
      dispatcher.utter_message('timing is :' + x)



   
class action_search_salary(Action):
    def name(self) -> Text:
        return "action_search_salary"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      company = tracker.get_slot('company')
      job = tracker.get_slot('job')
      q = conn.execute("select package from joblistings where company='{}' and position='{}' ".format(company.lower(),job.lower()))
      
      r=(q.fetchall())
      for row in r:
          x=row[0]
    
      dispatcher.utter_message(x)

class action_search_address(Action):
    def name(self) -> Text:
        return "action_search_address"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      cuisine = tracker.get_slot('company')
      q = conn.execute("select job_location from joblistings where company='{}' ".format(cuisine.lower()))
      
      r=(q.fetchall())
      for row in r:
          x=row[0]
    
      dispatcher.utter_message("address of {} is ".format(cuisine.lower()) + x)

  
class action_skills(Action):
    def name(self) -> Text:
        return "action_skills"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      #cuisine = 'data scientist'
      cuisine = tracker.get_slot('company') or tracker.get_slot('job')
      q = conn.execute("select skills_req from joblistings where company='{}' OR position='{}' ".format(cuisine.lower(),cuisine.lower()))

      r=(q.fetchall())
      for row in r:
          x=row[0]
      
      dispatcher.utter_message("skills required are " + x)

class action_eligibility_criteria(Action):
    def name(self) -> Text:
        return "action_eligibility_criteria"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
      conn = sqlite3.connect('job_data.db')     
      #cuisine = 'data scientist'
      cuisine = tracker.get_slot('company') or tracker.get_slot('job')
      q = conn.execute("select qual_req from joblistings where company='{}' OR position='{}' ".format(cuisine.lower(),cuisine.lower()))
      
      r=(q.fetchall())
      for row in r:
          x=row[0]
      
      dispatcher.utter_message("qualifications required are " + x)
       
        
        
        
class action_restarting(Action):
    """ This is for restarting the chat"""

    def name(self):
        return "action_restarting"

    def run(self, dispatcher, tracker, domain):
        
        return [Restarted()]
