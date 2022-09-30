class Maquina():
    FIELDS = ["numero_maquina", "serial_number", "fabricante", "juego", "modelo", "progresivo", "tipo_progresivo", "cantidad_lineas", "creditos_maximos", "main_program", "pay_table", "base_program", "creditos_1", "porcentaje_1", "creditos_2", "porcentaje_2", "creditos_3", "porcentaje_3", "creditos_4", "porcentaje_4", "acepta_bill", "marca_bill", "modelo_bill", "version_bill", "impresora", "marca_printer", "modelo_printer", "version_printer", "sala", "area", "gerencia", "empresa", "estado_maquina", "pais_fabricacion", "fecha_fabricacion", "layout_x", "layout_y"]
    
    def __init__(self, data):
        self._id = None
        self._data = data

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data
    
    def get_field(self, field_name):
        return self._data[field_name]

    def get_diference(self, data):
        diference = {}
        for field in data:
            if self._data[field] != data[field]:
                diference[field] = data[field]
        return diference