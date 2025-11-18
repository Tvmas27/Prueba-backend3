# cliente_autonomo.py
import requests
import subprocess
import time
import sys

def iniciar_servidor_si_no_esta():
    """Inicia el servidor Django si no está ejecutándose"""
    try:
        response = requests.get("http://localhost:8000/", timeout=2)
        print("✅ Servidor ya está ejecutándose")
        return True
    except:
        print("🔧 Iniciando servidor Django...")
        try:
            # Iniciar servidor en segundo plano
            subprocess.Popen([
                sys.executable, "manage.py", "runserver"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Esperar a que el servidor esté listo
            for i in range(15):
                try:
                    response = requests.get("http://localhost:8000/", timeout=2)
                    if response.status_code == 200:
                        print("✅ Servidor iniciado correctamente")
                        return True
                except:
                    time.sleep(1)
                    if i % 3 == 0:
                        print(f"   Esperando servidor... ({i+1}/15)")
            
            print("❌ No se pudo iniciar el servidor")
            return False
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
            return False

def probar_api():
    """Prueba la API de productos"""
    if not iniciar_servidor_si_no_esta():
        return
    
    print("\n🚀 PROBANDO API DE PRODUCTOS")
    print("=" * 40)
    
    # 1. Obtener productos existentes
    try:
        response = requests.get("http://localhost:8000/api/productos/")
        if response.status_code == 200:
            data = response.json()
            print(f"📦 Productos existentes: {len(data.get('productos', []))}")
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 2. Crear nuevo producto
    nuevo_producto = {
        "nombre": "Monitor 24\" Full HD",
        "precio": 200,
        "stock": 10,
        "descripcion": "Monitor LED Full HD",
        "disponible": True
    }
    
    try:
        response = requests.post("http://localhost:8000/api/productos/", json=nuevo_producto)
        print(f"\n📝 Creando producto... Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ PRODUCTO CREADO EXITOSAMENTE!")
            print(f"   🆔 ID: {data['producto']['id']}")
            print(f"   📛 Nombre: {data['producto']['nombre']}")
            print(f"   💰 Precio: ${data['producto']['precio']}")
            print(f"   📦 Stock: {data['producto']['stock']}")
        else:
            print(f"❌ Error creando producto: {response.text}")
    
    except Exception as e:
        print(f"💥 Error: {e}")
    
    # 3. Listar todos los productos
    print("\n📋 LISTA COMPLETA DE PRODUCTOS:")
    try:
        response = requests.get("http://localhost:8000/api/productos/")
        if response.status_code == 200:
            data = response.json()
            for producto in data.get('productos', []):
                estado = "🟢" if producto['disponible'] else "🔴"
                print(f"   {estado} {producto['id']}: {producto['nombre']} - ${producto['precio']}")
    except Exception as e:
        print(f"❌ Error listando productos: {e}")

if __name__ == "__main__":
    probar_api()
    print("\n🎯 Ejecuta este archivo directamente:")
    print("   python cliente_autonomo.py")