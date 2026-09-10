import json
from wsgiref.simple_server import make_server


tasks = []
next_id = 1

# funcion que arma y envia las rta HTTP
def enviar_respuesta(start_response, status, datos):
    headers = [("Content-Type", "application/json")]
    start_response(status, headers)
    return [json.dumps(datos).encode("utf-8")]

# funcion que extrae y convierte el body a JSON
def extraer_json(environ):
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        if content_length > 0:
            body_bytes = environ["wsgi.input"].read(content_length)
            return json.loads(body_bytes.decode("utf-8"))
    except (ValueError, TypeError):
        pass
    return {}

def app(environ, start_response):
    global next_id

    method = environ.get("REQUEST_METHOD")
    path = environ.get("PATH_INFO", "")

    # leer los datos que mandan en la peticion (body) usando la funcion
    request_body = extraer_json(environ)

    # leer/obtener todas las tareas
    if method == "GET" and path == "/tasks":
        return enviar_respuesta(start_response, "200 OK", tasks)

    # crea tarea nueva
    if method == "POST" and path == "/tasks":
        new_task = {
            "id": next_id,
            "title": request_body.get("title", ""),
            "done": request_body.get("done", False)
        }
        tasks.append(new_task)
        next_id += 1
        return enviar_respuesta(start_response, "201 Created", new_task)

    # rutas para una tarea especifica (/tasks/id)
    if path.startswith("/tasks/"):
        parts = path.split("/")
        
        # verificar que el id sea un numero
        if len(parts) == 3 and parts[2].isdigit():
            task_id = int(parts[2])
            
            # buscar la tarea en la lista
            task = next((t for t in tasks if t["id"] == task_id), None)

            # Eliminar una tarea
            if method == "DELETE":
                if task:
                    tasks.remove(task)
                    return enviar_respuesta(start_response, "200 OK", {"message": "Tarea eliminada"})
                return enviar_respuesta(start_response, "404 Not Found", {"error": "Tarea no encontrada"})

            # Modificar/actualizar una tarea
            if method == "PATCH":
                if task:
                    if "title" in request_body:
                        task["title"] = request_body["title"]
                    if "done" in request_body:
                        task["done"] = request_body["done"]
                    return enviar_respuesta(start_response, "200 OK", task)
                return enviar_respuesta(start_response, "404 Not Found", {"error": "Tarea no encontrada"})

            # leer/obtener una tarea
            if method == "GET":
                if task:
                    return enviar_respuesta(start_response, "200 OK", task)
                return enviar_respuesta(start_response, "404 Not Found", {"error": "Tarea no encontrada"})

    #cualquier otra combinacion
    return enviar_respuesta(start_response, "404 Not Found", {"error": "Ruta invalida"})


if __name__ == "__main__":
    with make_server("", 9292, app) as server:
        print("Servidor escuchando en http://localhost:9292...")
        server.serve_forever()