import json
from xxlimited import Str
from msal import PublicClientApplication
from maquina import Maquina
from web_api import WebAPI

class MSGraphAPI(WebAPI):

    def __init__(self):
        super().__init__()
        self.AUTH_SERVER_URL = "https://login.microsoftonline.com/gruposlots.com.ar"
        self.CLIENT_SECRET_VALUE = "d5Y8Q~oeNpbWtBvStAKlcX9YBFZv_gUs-rGNNcCH"
        self.TENANT_ID = "8b319dc4-7d8e-4d30-8869-3f64e6195ea3"
        self.CLIENT_ID = "3e0f7e19-287f-496d-bfb7-4e57941a65c2"
        self.USER = "dei.corp@gruposlots.com.ar"
        self.PASSWORD = "TallerDEI1357"
        self.GRAPH_USER_SCOPES = ["User.Read", "Sites.ReadWrite.All"]
        self.SITE_ID = "e259c24a-b216-4f05-b0b7-9e8f7908febe"
        self.LISTA_ID = "9b039016-2acb-49b8-9c2d-3211001dc010"

    def get_token(self):
        app = PublicClientApplication(self.CLIENT_ID, authority=self.AUTH_SERVER_URL)

        result = app.acquire_token_by_username_password(self.USER, self.PASSWORD, 
                        scopes=self.GRAPH_USER_SCOPES)

        if "access_token" in result:
            self._token = result['access_token']
            self._authorization = {'Authorization': 'Bearer ' + self._token}
        else:
            raise Exception('get token error')


    def get_machine_by_id(self, id):
        # Devuelve la máquina de la lista de sharepoint con ese id
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items/{id}/fields"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.get_request(url, head, {})

        if response.status_code != 200:
            raise Exception('Error getting a machine from the sharepoint list')
        else:
            json_response = json.loads(response.text)
            data = {}
            for field in Maquina.FIELDS:
                if field == "numero_maquina":
                    field = "Title"
                if field in json_response:
                    if field == "Title":
                        data["numero_maquina"] = json_response[field]
                    else:
                        data[field] = json_response[field]
                    
            maquina = Maquina(data)

        return maquina


    def update_machine(self, id, changes):
        # Se reflejan los cambios en la lista de sharepoint dado un id

        if "numero_maquina" in changes:
            raise Exception('Error updating a machine in sharepoint list')

        body =  json.dumps({"fields": changes})
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items/{id}"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.patch_request(url, head, body)

        if response.status_code != 200:
            raise Exception('Error updating a machine in sharepoint list')

        return

    def insert_machine(self, maquina):
        # Agrega una máquina a la lista de sharepoint

        data = maquina._data
        if "numero_maquina" in data:
            data["Title"] = data["numero_maquina"]
            del data["numero_maquina"]
        else:
            raise Exception('Error inserting a machine in sharepoint list')

        body =  json.dumps({"fields": data})
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.post_request(url, head, body)

        if response.status_code != 201:
            raise Exception('Error inserting a machine in sharepoint list')
        else:
            data = json.loads(response.text)
            list_id = data["id"]

        return list_id


    def delete_machine(self, id):
        # Borra una máquina de la lista de sharepoint dado un id
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items/{id}"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.delete_request(url, head, {})

        if response.status_code != 204:
            raise Exception('Error deleting a machine in sharepoint list')

        return