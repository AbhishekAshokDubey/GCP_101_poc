# [START imports]


# import sys
# sys.path.insert(1, r'C:\Program Files (x86)\Google\google_appengine')
# sys.path.insert(1, r'C:\Program Files (x86)\Google\google_appengine\lib\yaml\lib')
# sys.path.insert(1, 'lib')
# 
# if 'google' in sys.modules:
#     del sys.modules['google']

import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
# [END imports]



# https://cloud.google.com/appengine/docs/python/tools/protorpc/messages/messageclass
# https://snop-optimizer.appspot.com/_ah/api/explorer

class welltype(messages.Enum):
    completed = 1
    aborted = 2
    inprogress = 3
    planned = 4

class equipementId(messages.Message):
    id = messages.StringField(1)

class equipement_list(messages.Message):
    equipement_list_name = messages.StringField(1)
    all_equipments = messages.MessageField(equipementId, 2, repeated=True)
    all_available = messages.BooleanField(3)

class well_class(messages.Message):
    well_id = messages.StringField(1, required=True)
    well_state = messages.EnumField(welltype,2)
    equipements = messages.MessageField(equipement_list, 3)
    total_cost = messages.IntegerField(4)


eq1 = equipementId(id="id_1")
eq2 = equipementId(id="id_2")
eq3 = equipementId(id="id_3")

eq_list = equipement_list(equipement_list_name='type a resources')
eq_list.all_equipments = [eq1,eq2,eq3]
eq_list.all_available = True

well1 = well_class(well_id="random_id", well_state=welltype.completed)
well1.equipements = eq_list
well1.total_cost = 1000



@endpoints.api(name='ads_slb', version='v1', description='Our new api')
class ads_slb_api(remote.Service):

    @endpoints.method(
        # This method does not take a request message.
        message_types.VoidMessage,
        # This method returns a GreetingCollection message.
        well_class,
        path='name',
        http_method='GET',
        name='ads_slb.welcome')
    def list_greetings(self, unused_request):
        return well1


# [START api_server]
api = endpoints.api_server([ads_slb_api])
# [END api_server]


# ref : https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/endpoints/backend/main.py