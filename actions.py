from rasa_core.actions import Action
from rasa_core_sdk.events import SlotSet
import httplib2



class ActionExample(Action):

    def name(self):
        # you can then use action_example in your stories
        return "action_example"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        s=str(tracker.get_slot("website"))
        URL="https://www."+s+".com"
        try:
            resp, content = httplib2.Http().request(URL)
            if resp.status==200:
                response="""{} is up and running  """.format(s)
                dispatcher.utter_message(response)
            else:
                dispatcher.utter_message("Sorry!")
        except:
            dispatcher.utter_message("Sorry! an exception occured in accessing "+s+" website")
        return []

class ActionStartJenkinsBuild(Action):
    def name(self):
        return "action_jenkins"

    def run(self, dispatcher, tracker, domain):
        job = tracker.get_slot("app_name")
        URL = "http://localhost:8080/job/"+job+"/build?token=remote_enable_token"
        try:
            resp, content = httplib2.Http().request(URL)
            if resp.status==201:
                response="Job successfully triggered"
                dispatcher.utter_message(response)
                dispatcher.utter_message(str(content.decode('utf-8')))
            else:
                dispatcher.utter_message("status code :"+str(resp.status))
                dispatcher.utter_message(content.decode())
        except:
            dispatcher.utter_message("Sorry! an exception occured in triggering the job")
        return []

        
class ActionStartJenkinsBuildWithParams(Action):
    def name(self):
        return "action_jenkins_param"

    def run(self, dispatcher, tracker, domain):
        job = tracker.get_slot("app_name")
        if(tracker.get_slot("param")=="environment"):
            param = "Environment"
        pvalue = (tracker.get_slot("pvalue")).upper()
        URL = "http://localhost:8080/job/"+job+"/buildWithParameters?token=remote_enable_token&"+param+"="+pvalue
        try:
            resp, content = httplib2.Http().request(URL)
            if resp.status==201:
                response="Job successfully triggered with "+param+"="+pvalue
                dispatcher.utter_message(response)
                dispatcher.utter_message(str(content.decode('utf-8')))
            else:
                dispatcher.utter_message("status code :"+str(resp.status))
                dispatcher.utter_message(content.decode())
        except:
            dispatcher.utter_message("Sorry! an exception occured in triggering the job")
        return []        
