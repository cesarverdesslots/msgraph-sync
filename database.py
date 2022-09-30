class Database():

    def start_machine_sync(self):
        # abre la base de datos y pone todos los campos en delete = True
        pass

    def machine_marked_for_delete(self):
        # devuelve una lista de tuples con la forma [(numero_maquina, msgraph_id), ..]
        # de las máquinas que tienen delete = true
        pass

    def delete_machine(self, numero_maquina):
        # borra la máquina de la base de datos con el número de maáquina
        pass

    def insert_machine(self, data, id):
        # inserta la nueva máquina en la base de datos cargando el id y seteando delete = False
        pass

    def update_machine(self, data):
        # realiza los cambios en la base de datos cargando el id y seteando delete = False
        pass

    def get_sharepoint_machine_id(self):
        # retorna el id de la máquina en la lista de sharepoint
        pass