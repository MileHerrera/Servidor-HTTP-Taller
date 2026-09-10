# Servidor
Verbos HTTP:


**GET:** Se utiliza solo para obtener/leer datos. Es seguro (ya que no altera el estado del servidor) y es idempotente


**POST:** Se utiliza para crear un nuevo recurso. No es seguro ni idempotente
Post no es idempotente, porque si se envia la misma peticion varias veces, el servidor seguira creando un nuevo recurso por cada llamada, alterando el estado cada vez.


**PATCH:** Se utiliza para modificar de manera parcial un recurso que ya existe en el servidor(parcial porque solo modifica campos indicados).No es seguro y pero si es idempotente


**DELETE:** Se utiliza para eliminar un recurso existente. No es seguro y es idempotente
