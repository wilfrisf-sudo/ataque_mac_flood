# Laboratorio de Seguridad: Ataque DoS mediante Inundación de Tabla CAM (MAC Flooding)

**Autor:** Wilfri Solano Frias  
**Matrícula:** 2024-2364 

---

## 1. Objetivo del Laboratorio
Conocer las vulnerabilidades y peligros reales de los conmutadores al agotar el espacio físico de almacenamiento de sus tablas de reenvío (memoria CAM), analizando cómo la falta de políticas de seguridad perimetral permite forzar al switch a degradar su funcionamiento y actuar como un Hub (difusión masiva o *fail-open*).

---

## 2. Objetivo del Script
Generar e inyectar de manera asíncrona y continua miles de tramas Ethernet con identidades de hardware de Capa 2 aleatorias en el plano de datos, con el fin de desbordar la tabla de direcciones MAC del switch y colapsar la asignación de memoria dinámica del plano de reenvío.

### 2.1. Requisitos para utilizar la herramienta
* **Sistema Operativo:** Kali Linux.
* **Lenguaje:** Python 3.x.
* **Librerías/Dependencias:** Scapy (módulos básicos del núcleo: `sendp`, `Ether`, `IP`, `ICMP`, `RandMAC`, `RandIP`). No requiere submódulos externos adicionales.
* **Entorno de Red:** La interfaz de red (`eth0`) debe estar configurada en modo promiscuo y conectada hacia un puerto del switch que tenga permitido el aprendizaje dinámico de direcciones MAC sin restricciones activas de seguridad.

### 2.2. Parámetros Usados
El script admite y manipula las siguientes variables y funciones dinámicas:

**Bucle While de Inyección Dinámica (Líneas 25-27)**
* `RandMAC()`: Función que genera al vuelo direcciones de hardware de origen y destino únicas para forzar nuevos registros en la tabla CAM.
* `RandIP()`: Creación de paquetes IP falsos con cargas ICMP que simulan tráfico legítimo de red para engañar la lógica de aprendizaje de la infraestructura de red.

**Bloque de Envío y Configuración Principal (Líneas 31, 49 y 50)**
* `sendp`: Inyección de tramas directo en Capa 2 sin almacenamiento previo en la memoria RAM del atacante, garantizando un rendimiento óptimo.
* `NIC_OBJETIVO = "eth0"`: Interfaz local del atacante encargada de conectarse al entorno virtual de GNS3.
* `TOTAL_TRAMAS = 50000`: Límite máximo de paquetes basura fijado para la ráfaga de estrés.

---

## 3. Documentación del Funcionamiento del Script
Al ejecutarse, el script valida los permisos locales a nivel de kernel y abre un canal de transmisión directo con la interfaz física seleccionada. El bucle principal genera en microsegundos tramas estructuralmente válidas pero con direcciones MAC de origen aleatorias. 

Cuando el switch SWI2 recibe cada paquete por su interfaz `Ethernet0/1`, inspecciona obligatoriamente el encabezado de Capa 2 para aprender la ubicación del host. Al detectar una MAC nueva en cada trama, la asocia a ese puerto y la registra dentro de su memoria de estado estático (tabla CAM). Como el script transmite miles de MACs distintas de manera continua, la memoria dinámica del switch se desborda rápidamente. Al quedarse sin espacio libre, el conmutador purga los registros legítimos y entra en modo *fail-open*, replicando todo el tráfico entrante de la LAN por todos sus puertos (comportamiento idéntico al de un Hub).

---

## 4. Documentación de la Red

### 4.1. Topología
* **Descripción:** Infraestructura virtualizada en GNS3 diseñada para evaluar el comportamiento del plano de reenvío ante ráfagas masivas de suplantación física en accesos.
* **VLANs Configuradas:** VLAN 1 (Nativa / Por defecto).
* **Direccionamiento IP:**
  * **Segmento de Red:** `192.168.124.0` / `255.255.255.0`
  * **Atacante (Kali Linux):** IP estática `192.168.124.135` / `255.255.255.0` (Interfaz `eth0`).
* **Interfaces Clave (SWI2):**
  * `Ethernet0/0`: Conectada hacia un Router de la infraestructura (utilizado para validar la función natural del protocolo CDP).
  * `Ethernet0/1`: Conectada directamente al host del atacante Kali Linux.

---

## 5. Contramedidas (Mitigación)

Para contrarrestar la inundación y proteger la tabla de reenvío del switch, se aplica la característica nativa *Port Security* en los puertos de acceso de usuarios:

### 5.1 Mitigación Estricta: Acción de Apagado (Shutdown)
Consiste en fijar la interfaz física en modo acceso, limitar el aprendizaje automático de direcciones MAC a una sola identidad legítima e indicar el apagado automático del puerto si ingresan tramas provenientes de direcciones de hardware desconocidas.


SWI2# configure terminal
SWI2(config)# interface Ethernet0/1
SWI2(config-if)# switchport mode access
SWI2(config-if)# switchport port-security
SWI2(config-if)# switchport port-security maximum 1
SWI2(config

---

## 6. Evidencias

### 6.1. Demostración en Video
En el siguiente enlace se encuentra el video demostrativo (máx. 5 minutos) donde se visualiza la topología con mi nombre y matrícula, la fecha y hora, la ejecución del ataque y la aplicación de la contramedida:  

https://www.youtube.com/watch?v=eB26bVR1--8&list=PLGfNWxn7Di3BhsEEifmTJKXP4_U9fla7P&index=4

### 6.2. Capturas de Pantalla

**A. Diseño de la Topología en GNS3**

<img width="466" height="498" alt="imagen" src="https://github.com/user-attachments/assets/0694040a-aef4-4330-933c-5ea6a041fe36" />

**B.Tabla MAC sin ser atacada (Saturación de la CAM)**

<img width="357" height="132" alt="imagen" src="https://github.com/user-attachments/assets/7c872e62-db83-4950-a728-210e089e96ee" />

**C. Ejecución del Script en Kali Linux** 

<img width="583" height="84" alt="imagen" src="https://github.com/user-attachments/assets/9ebc7da2-870e-4422-83d1-0ddb4c527783" />

**D. Desbordamiento de la Tabla MAC (Saturación de la CAM)**

<img width="511" height="580" alt="imagen" src="https://github.com/user-attachments/assets/011add14-9d7b-49b9-8c7d-333b50a847ba" />

**E. Aplicación de Contramedidas**

<img width="379" height="67" alt="imagen" src="https://github.com/user-attachments/assets/fcc08061-7c11-4ca6-b6da-96ef91db2e3d" />

<img width="822" height="21" alt="imagen" src="https://github.com/user-attachments/assets/03048abb-1328-45d7-af33-c1dbd87ea810" />
