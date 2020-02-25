import logging
import json
import requests

from cmd import Cmd

logger = logging.getLogger(__name__)
class MyPrompt(Cmd):
    intro = "Python Demo To-Do Application. Type ? to list commands"

    def do_exit(self, input):
        '''exit the application.'''
        print("Bye")
        return True

    def do_show(self, input):
        incomplete = []
        complete = []
        try:
            incomplete = requests.get("http://localhost:5000/get/incomplete")
            complete = requests.get("http://localhost:5000/get/complete")
            inc_data = json.loads(incomplete.text)
            com_data = json.loads(complete.text)
            print("Incomplete\n")
            print("----------\n")
            for entry in inc_data:
                print("Id: " + str(entry[0]) + " Task: " + entry[1] + "\n")
            print("Complete\n")
            print("----------\n")
            for entry in com_data:
                print("Id: " + str(entry[0]) + " Task: " + entry[1] + "\n")
        except Exception as ex:
            logger.exception("Error occured.")
            pass

    def do_add(self, text):
        try:
            response = requests.post("http://localhost:5000/add/" + text)
            print(response.text)
            if response.ok:
                self.do_show(None)
        except Exception as ex:
            logger.exception("Error occured.")
            pass

    def do_complete(self, id):
        try:
            response = requests.post("http://localhost:5000/complete/task/" + str(id))
            print(response.text)
            if response.ok:
                self.do_show(None)
        except Exception as ex:
            logger.exception("Error occured.")
            pass

    def do_save(self, input):
        try:
            response = requests.post("http://localhost:5000/save/tasks")
            print(response.text)
            if response.ok:
                self.do_show(None)
        except Exception as ex:
            logger.exception("Error occured.")
            pass

MyPrompt().cmdloop()