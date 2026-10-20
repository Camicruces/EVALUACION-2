import urllib.parse
import requests

main_api = "https://graphhopper.com/api/1/route?"
# PEGA TU CLAVE DENTRO DE LAS COMILLAS EN LA SIGUIENTE LINEA:
key = "TU_CLAVE_AQUI" 

def geocodificar(localizacion, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": localizacion, "limit": "1", "key": key, "locale": "es"})
    reply = requests.get(url)
    json_data = reply.json()
    if reply.status_code == 200 and "hits" in json_data and len(json_data["hits"]) > 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        nombre = json_data["hits"][0]["name"]
        return lat, lng, nombre
    return None, None, None

def formatear_tiempo(ms):
    seg = ms / 1000
    return f"{int(seg // 60)} min {int(seg % 60)} seg"

while True:
    print("\n" + "="*40)
    origen = input("Origen (o 's' / 'salir'): ").strip()
    if origen.lower() in ["s", "salir"]:
        print("Saliendo del programa...")
        break
        
    destino = input("Destino (o 's' / 'salir'): ").strip()
    if destino.lower() in ["s", "salir"]:
        print("Saliendo del programa...")
        break

    lat1, lng1, nom1 = geocodificar(origen, key)
    lat2, lng2, nom2 = geocodificar(destino, key)

    if not lat1 or not lat2:
        print("[ERROR] No se encontro la ubicacion. Verifique la API Key o el nombre.")
        continue

    url = main_api + urllib.parse.urlencode([
        ("point", f"{lat1},{lng1}"),
        ("point", f"{lat2},{lng2}"),
        ("vehicle", "car"),
        ("locale", "es"),
        ("key", key)
    ])
    
    json_data = requests.get(url).json()

    if "paths" in json_data:
        path = json_data["paths"][0]
        print("\n--- RESUMEN DEL VIAJE ---")
        print(f"De: {nom1} a {nom2}")
        print(f"Distancia: {path['distance'] / 1000:.2f} km") # 2 decimales
        print(f"Tiempo: {formatear_tiempo(path['time'])}")
        
        print("\nINSTRUCCIONES PASO A PASO:")
        for i, paso in enumerate(path["instructions"], 1):
            print(f"{i}. {paso['text']} ({paso['distance'] / 1000:.2f} km)")
    else:
        print("[ERROR] No se pudo calcular la ruta.")
