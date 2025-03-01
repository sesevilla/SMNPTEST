import telnetlib
import os
import subprocess
import time
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Limpiar pantalla antes de ejecutar
os.system('cls' if os.name == 'nt' else 'clear')

# Banner con colores
print(Fore.CYAN + "=" * 40)
print(Fore.CYAN + "     ✉ ENVÍO DE EMAILS VIA TELNET ✉     ")
print(Fore.CYAN + "=" * 40)

# Solicitar dominio al usuario
domain = input(Fore.YELLOW + "\n🔹 Ingrese el dominio (ejemplo.com): " + Style.RESET_ALL)

# Obtener el servidor MX usando el comando dig
def get_mx_server(domain):
    print(Fore.MAGENTA + "🔍 Buscando servidor MX para:", domain)
    try:
        result = subprocess.run(["dig", "+short", "MX", domain], capture_output=True, text=True)
        mx_record = result.stdout.splitlines()
        
        if mx_record:
            mx_server = mx_record[0].split()[1]  # Tomamos el primer servidor MX
            print(Fore.GREEN + "✅ Servidor MX encontrado:", mx_server)
            return mx_server
        else:
            raise Exception("No se encontró un servidor MX para este dominio.")
    except Exception as e:
        print(Fore.RED + "❌ Error al obtener el servidor MX:", e)
        print(Fore.RED + "⚠ Verifique que el dominio sea correcto e intente nuevamente.")
        return None

# Obtener el servidor SMTP a partir del dominio
SMTP_SERVER = get_mx_server(domain)
if SMTP_SERVER is None:
    exit(1)

SMTP_PORT = 25  # Puerto 25 por defecto

# Solicitar información del correo
print(Fore.CYAN + "\n📧 CONFIGURACIÓN DEL MENSAJE")
print(Fore.CYAN + "=" * 30)

FROM_EMAIL = input(Fore.YELLOW + "✉ Ingrese el correo de origen: " + Style.RESET_ALL)
FROM_NAME = input(Fore.YELLOW + "🏷 Etiqueta del remitente (Ej: Soporte Técnico): " + Style.RESET_ALL).strip() or FROM_EMAIL
TO_EMAIL = input(Fore.YELLOW + "📩 Ingrese el correo de destino: " + Style.RESET_ALL)
TO_NAME = TO_EMAIL
SUBJECT = input(Fore.YELLOW + "📌 Asunto del correo: " + Style.RESET_ALL)
BODY = input(Fore.YELLOW + "📝 Ingrese el cuerpo del correo: " + Style.RESET_ALL)

# Iniciar la conexión Telnet
try:
    print(Fore.MAGENTA + "\n🌐 Conectando con el servidor SMTP...")
    tn = telnetlib.Telnet(SMTP_SERVER, SMTP_PORT)
    print(Fore.GREEN + "✅ Conexión establecida.")
    print(tn.read_until(b"220").decode())

    # Enviar el comando HELO
    tn.write(b"HELO tudominio.com\r\n")
    print(Fore.CYAN + "💬 HELO enviado.")
    print(tn.read_until(b"250").decode())

    # Enviar el MAIL FROM
    tn.write(f"MAIL FROM:<{FROM_EMAIL}>\r\n".encode())
    print(Fore.CYAN + "💬 MAIL FROM enviado.")
    print(tn.read_until(b"250").decode())

    # Enviar el RCPT TO
    tn.write(f"RCPT TO:<{TO_EMAIL}>\r\n".encode())
    print(Fore.CYAN + "💬 RCPT TO enviado.")
    print(tn.read_until(b"250").decode())

    # Iniciar el mensaje con DATA
    tn.write(b"DATA\r\n")
    print(Fore.CYAN + "💬 DATA enviado.")
    print(tn.read_until(b"354").decode())

    # Escribir el cuerpo del mensaje correctamente formateado
    mensaje = (
        f"From: {FROM_NAME} <{FROM_EMAIL}>\r\n"
        f"To: {TO_NAME}\r\n"
        f"Subject: {SUBJECT}\r\n\r\n"
        f"{BODY}\r\n.\r\n"
    )

    tn.write(mensaje.encode())
    print(Fore.GREEN + "✅ Mensaje enviado con éxito.")
    print(tn.read_until(b"250").decode())

    # Cerrar conexión con QUIT
    tn.write(b"QUIT\r\n")
    print(Fore.CYAN + "🚪 Cerrando conexión con el servidor.")
    print(tn.read_until(b"221").decode())

    # Cerrar la conexión Telnet
    tn.close()
    print(Fore.GREEN + "\n✅ Correo enviado correctamente.")

except Exception as e:
    print(Fore.RED + f"❌ Error: {e}")
