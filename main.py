from eva_api import EVAAPI
from msgraph_api import MSGraphAPI
from database import Database

eva = EVAAPI()
eva.get_token()
eva.start_machine_sync()

msgraph = MSGraphAPI()
msgraph.get_token()

database = Database()
database.start_machine_sync()

while eva.more_machines():
    data_eva_machine = eva.get_next_machine()

    if database.exist_machine(data_eva_machine["numero_maquina"]):
        # Obtiene los datos de la última búsqueda en la base de datos
        data_database_machine = database.get_machine_data()
        # Verifica si hay que algún cambio en algún campo
        changed_fields = data_eva_machine.get_diferences(data_database_machine)
        if changed_fields:
            # Se reflejan los cambios en la lista de sharepoint para ese id
            msgraph.update_machine(sharepoint_machine_id, changed_fields)
            # Se reflejan los cambios en la base de datos para ese número de máquina
            database.update_machine(data_eva_machine)
    else:
        # Inserta la nueva máquina en sharepoint y obtiene el id
        sharepoint_machine_id = msgraph.insert_machine(data_eva_machine)
        # Inserta la nueva máquina en la base de datos
        database.insert_machine(data_eva_machine, sharepoint_machine_id)


marked_for_delete = database.machine_marked_for_delete()

for to_delete in marked_for_delete:
    # Obtiene el id para ese número de máquina de la base de datos
    sharepoint_machine_id = database.get_sharepoint_machine_id(data_eva_machine["numero_maquina"])
    # Borra la máquina de sharepoint con el id
    msgraph.delete_machine(sharepoint_machine_id)
    # Borra la máquina de a base de máquinas con el número de máquina
    database.delete_machine(data_eva_machine["numero_maquina"])
