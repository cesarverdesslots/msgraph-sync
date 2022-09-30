from msgraph_api import MSGraphAPI
# from maquina import Maquina

msgraph = MSGraphAPI()
msgraph.get_token()

# maquina = Maquina({"numero_maquina": "987654", "serial_number": "Y321", "fabricante": "IGT"})
# sharepoint_machine_id = msgraph.insert_machine(maquina)
# print(sharepoint_machine_id)

# msgraph.update_machine(14, {"serial_number": "X124", "juego": "Otro juego"})

# maquina = msgraph.get_machine_by_id(14)
# print(maquina._data)

msgraph.delete_machine(12)
