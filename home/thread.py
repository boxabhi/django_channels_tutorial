import threading
from .models import *
from faker import Faker
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer
fake = Faker()
import random
import time

class CreateStudentsThread(threading.Thread):
    
    def __init__(self , total):
        self.total = total 
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            print('Thread execution started')
            channel_layer = get_channel_layer()
            current_total = 0
            for i in range(self.total):
                current_total += 1
                student_obj = Students.objects.create(
                    student_name = fake.name(),
                    student_email = fake.email(),
                    address = fake.address(),
                    age = random.randint(10 , 50)
                )
                channel_layer = get_channel_layer()
                data = {'id' : current_total ,'current_total' :current_total , 'total' : self.total, 'student_name' : student_obj.student_name , 'student_age' : str(student_obj.age) , 'address' : student_obj.address}
                print(data)
                async_to_sync(channel_layer.group_send)(
                    'new_consumer_group' , {
                        'type' : 'send_notification',
                        'value' : json.dumps(data)
                    }
                )
                #time.sleep(1)
        except Exception as e:
            print(e)
            