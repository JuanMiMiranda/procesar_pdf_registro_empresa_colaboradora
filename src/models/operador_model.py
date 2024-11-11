

class Operador:
  def __init__(self,nif_operador, razon_social,cob_fija, cob_fwa, cob_movil, nif_grupo_operador, grupo_operador, nif_replegal, nombre_replegal, nif_notificacion,
                 representante_notificacion, email_notificacion, servicio_fija, servicio_movil, servicio_fwa, servicio_movil_virtual, servicio_otros):
        self.nif_operador = nif_operador
        self.razon_social = razon_social
        self.cob_fija = cob_fija
        self.cob_fwa = cob_fwa
        self.cob_movil = cob_movil
        self.nif_grupo_operador = nif_grupo_operador
        self.grupo_operador = grupo_operador
        self.nif_replegal = nif_replegal
        self.nombre_replegal = nombre_replegal
        self.nif_notificacion = nif_notificacion
        self.representante_notificacion = representante_notificacion
        self.email_notificacion = email_notificacion
        self.servicio_fija = servicio_fija
        self.servicio_movil = servicio_movil
        self.servicio_fwa = servicio_fwa
        self.servicio_movil_virtual = servicio_movil_virtual
        self.servicio_otros = servicio_otros