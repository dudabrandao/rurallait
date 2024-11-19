import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

class Firebase:
    def __init__(self):
        self.cred = credentials.Certificate("./rural-lait-firebase-adminsdk-dosxm-22907e39b0.json")
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(self.app)

    def auth(self, id):
        local = self.db.collection('users').document(id)
        content = local.get()
        if content.exists:
            return True
        else:
            return False

    def insertSensor(self, id, data):
        local = self.db.collection('users').document(id).collection('sensores')
        data["data"] = datetime.datetime.now(tz=datetime.timezone.utc)
        local.add(data)

    def getConfig(self, id):
        local = self.db.collection('users').document(id).collection('config').stream()
        for doc in local:
            return doc.to_dict()
