# Actividad 2 – Documento de Formulación del Proyecto
### Samuel García Torres
### Geraldine de los Angeles Rios Lameda 
### Diego Alejandro Salgado Gonzalez
### Corporación Universitaria Iberoamericana
### Ingeniería de Software
### Proyecto de Software
### Tatiana Cabrera
### 5 de oct. de 25

-----------------------------------------------------------------------------------

# Introducción	
A continuación, se detalla un cambio en el sector de la salud, un cambio pensando en la experiencia del usuario, la manera en solicitar y obtener respuesta para una cita médica, se ha desarrollado un aplicativo web el cual no solo ofrece el agendar una cita médica si no que la clasifica según la prioridad (normal, prioritaria y urgente), esto a través de un Modelo de Machine Learning debidamente entrenado con una serie de preguntas que se le realizaran a cada usuario registrado.
 
# Proyecto de Citas
## Contextualización del Problema
En la actualidad, la digitalización de los servicios médicos ha permitido que los pacientes puedan agendar citas a través de plataformas virtuales lo cual representa un gran avance en términos de accesibilidad y comodidad para los usuarios de los servicios de salud. Sin embargo, la mayoría de estos sistemas funcionan únicamente bajo un esquema de disponibilidad de agenda es decir que las citas se son signadas en orden en el cual se agendaron, sin considerar factores médicos relevantes que indiquen la urgencia o prioridad real de cada paciente.
Esta situación provoca que pacientes con condiciones críticas o que requieren atención prioritaria por sus antecedentes médicos  deban esperar turnos similares a quienes presentan dolencias menores, lo que puede retrasar diagnósticos y tratamientos oportunos, generando consecuencias negativas en la salud y en la percepción de eficiencia del sistema médico.
En el contexto actual, donde los servicios de salud enfrentan sobrecarga y alta demanda, se hace necesario contar con herramientas inteligentes que permitan clasificar automáticamente el nivel de prioridad de cada cita médica en función de la información clínica inicial proporcionada por el paciente. Esto sería un gran avance para el sector salud.
## Planteamiento del problema
Los sistemas tradicionales de gestión de citas médicas virtuales carecen de un mecanismo que evalúe y clasifique el nivel de urgencia de los pacientes en el momento de solicitar la cita que como se mencionó anteriormente es un problema para pacientes que presentan una mayor urgencia por razonas medicas previas. Al tratar todas las solicitudes de manera uniforme, se genera una desventaja para aquellas personas que presentan síntomas graves o con riesgo de complicaciones inmediatas, quienes deberían tener prioridad en la atención.
Esta ausencia de priorización no solo afecta la calidad del servicio, sino que también puede poner en riesgo la salud y seguridad de los usuarios. Surge entonces la necesidad de implementar un sistema inteligente capaz de procesar los datos médicos iniciales y, mediante técnicas de Machine Learning, determinar si la cita debe ser catalogada como normal, prioritaria o urgente, optimizando la asignación de recursos médicos y garantizando una atención más justa y eficaz para todos los usuarios.
## Pregunta problema
¿Cómo diseñar e implementar un sistema web inteligente que permita la gestión de citas médicas con clasificación automática de prioridades?
# Objetivos
## Objetivo General
Diseñar e implementar un primer prototipo de un sistema web inteligente de gestión de citas médicas que permita el registro de usuarios, la recolección de datos médicos básicos y la clasificación automática de las citas en niveles de prioridad (normal, prioritaria o urgente), garantizando una atención más eficiente y oportuna para los pacientes, con un sistema de persistencia que garantice la agregación de futuros módulos y de ese modo garantizar su futuro escalamiento.
## Objetivos Específicos
1.	Desarrollar un frontend ligero, intuitivo y responsive que facilite la interacción de los usuarios en procesos como registro, inicio de sesión, agendamiento, consulta y cancelación de citas médicas.
2.	Implementar un backend modular con FastAPI que gestione la lógica de negocio, la comunicación con la base de datos y la integración de un modelo de Machine Learning para la clasificación automática de prioridades médicas.
3.	Diseñar y entrenar un modelo de Machine Learning capaz de procesar datos médicos iniciales de los pacientes y determinar el nivel de urgencia de la cita, almacenando la información en una base de datos para su posterior consulta y análisis.

# Alcance del proyecto
Como primera versión El alcance del proyecto Gestor de Citas Médicas Inteligente comprende el desarrollo de un sistema web funcional que permita a los usuarios registrarse, iniciar sesión y agendar citas médicas a través de una interfaz sencilla, intuitiva y adaptable a distintos dispositivos. El sistema recopilará datos médicos básicos para garantizar información mínima consistente que serán suministrados por los mismos usuarios, mediante la integración de un modelo de Machine Learning, clasificará automáticamente cada cita en niveles de prioridad: normal, prioritaria o urgente. Además, se implementará un historial de citas donde el usuario podrá consultar, confirmar o cancelar sus registros. La arquitectura estará basada en un frontend ligero en HTML, CSS y JavaScript, un backend en Python con FastAPI, una base de datos SQL y un control de versiones con GitHub, delimitando el proyecto a funcionalidades esenciales y excluyendo integraciones avanzadas como pagos en línea o conexión con sistemas hospitalarios externos, como no contamos con acceso a costos de disponibilidad de hospitales y de personal médico este primer prototipo no contara con estos dados para agendar la cita, sin embargo al contar con una arquitectura modular el proyecto podría conectarse a este tipo de funcionalidades.
 
# Estructura del desglose EDT
Ilustración 1 - Estructura del Desglose EDT

 <img width="624" height="288" alt="image" src="https://github.com/user-attachments/assets/11ee8249-8a11-4b36-9f49-d51a383877c0" />

# Metodología ágil 
La metodología que usaremos es Kanban, ya que nos permite visualizar las tareas en el tablero, esto ayuda a gestionar tareas en paralelo y priorizar las cargas reales del equipo. La metodología Kanban facilita la mejora continua, por la flexibilidad y el control del progreso sin necesidad de planificaciones rígidas.
https://www.notion.so/Proyecto-de-Software-Citas-282f222d7a0a80ad803dd0c6fb2374c3?source=copy_link
# Levantamiento de información
A través de las entrevistas y formularios que se realizaron a los stakeholders principales, en conclusión, si existe una necesidad de una aplicación que ayude con la gestión de citas.
 
Mapa de Stakeholders

Tabla 1 - Mapa de Stakeholders

<img width="764" height="653" alt="image" src="https://github.com/user-attachments/assets/132b4d1b-1609-4805-af45-0abfc1fb27c6" />

# Justificación
Corto plazo: Mejorar la gestión y administración de las citas médicas mediante la automatización del proceso de registro y clasificación permitiendo así una atención más rápida para los pacientes.

Mediano plazo: Optimizar la gestión de los recursos médicos y reducir los tiempos de espera.

Largo plazo: Contribuir al fortalecimiento digital del sistema de salud mediante una plataforma escalable que pueda integrarse con otros sistemas hospitalarios y evolucionar hacia una herramienta completa de gestión médica basada en análisis de datos e inteligencia artificial.

# Matriz de Riesgos
Abrir el link para ver la matriz de riegos completa
Ilustración 2 - Mapa de Calor de la Matriz de Riesgo

 <img width="625" height="356" alt="image" src="https://github.com/user-attachments/assets/c04e6d7a-d68e-4eb3-ab7f-62a5a45cdd2c" />

[Matriz de Riesgos-Proyectos Citas.xlsx](https://laiberocol-my.sharepoint.com/:x:/g/personal/dsalgad7_estudiante_ibero_edu_co/EYKhwoV4IkxMiQNM1Kt4wm0Bw5_-bJrohsK-qCj_bWPMFw?rtime=YAmAPmIE3kg)

# Presupuesto
El presupuesto se ha realizado con una simulación de un contrato de mantenimiento por seis meses, para ver el presupuesto detalladamente abrir el link. 
https://laiberocol-my.sharepoint.com/:x:/g/personal/dsalgad7_estudiante_ibero_edu_co/EYPLw-vXxKZBnY1Ed8Yfp28B9X4A1ovDEiqEli9nLSlXEA?e=sZN8Lt


# Diagrama de Flujo
Ilustración 3 - Diagrama de flujo de solución

 <img width="344" height="515" alt="image" src="https://github.com/user-attachments/assets/f4e1e28b-1e15-4849-9e9e-454b889cba9f" />

# Requisitos Funcionales y NO Funcionales
## Requisitos Funcionales:
•	RQF001: El sistema debe permitir el registro de usuarios solicitando nombre, correo electrónico y contraseña con validación.
•	RQF002: El sistema debe permitir a los usuarios iniciar sesión con correo y contraseña.
•	RQF003: El sistema debe proporcionar un formulario de agendamiento de citas donde se registren datos médicos básicos: edad, sexo, zona afectada, síntomas, condiciones previas y tiempo de evolución.
•	RQF004: El sistema debe almacenar los datos de las citas en una base de datos SQL.
•	RQF005: El sistema debe clasificar automáticamente la cita en tres niveles de prioridad (normal, prioritaria, urgente).
•	RQF006: El sistema debe permitir a los usuarios consultar el historial de citas.
•	RQF007: El sistema debe permitir a los usuarios cancelar citas previamente registradas.
•	RQF008: El sistema debe mostrar al usuario la confirmación de la cita y el nivel de prioridad asignado.
•	RQF009: El sistema debe contar con un módulo de administración para la gestión de usuarios y mantenimiento básico.

## Requisitos No Funcionales 
•	RNF001 (Usabilidad): La interfaz debe ser sencilla, intuitiva y responsive, accesible desde dispositivos móviles y de escritorio.
•	RNF002 (Rendimiento): El sistema debe procesar y clasificar una solicitud de cita en menos de 3 segundos.
•	RNF003 (Disponibilidad): El sistema debe estar disponible la mayoría del tiempo operando.
•	RNF004 (Seguridad): Las contraseñas deben almacenarse cifradas y el acceso debe realizarse con autenticación segura.
•	RNF005 (Escalabilidad): El sistema debe poder soportar un crecimiento en el número de usuarios sin afectar el rendimiento.
•	RNF006 (Mantenibilidad): El código debe estar modularizado y documentado para facilitar actualizaciones
•	RNF007 (Confiabilidad): Los datos almacenados en la base de datos no deben perderse en caso de un fallo del sistema.
•	RNF008 (Portabilidad): El backend debe poder desplegarse en servidores en la nube.
 
# Conclusiones
El sistema propuesto da respuesta a una necesidad que existe en el sector de la salud, se resuelve de una manera profesionalmente utilizando las herramientas tecnológicas, se prioriza a los pacientes como primera medida asegurándonos así mejorar la eficiencia, equidad en la atención médica y la experiencia de cada paciente.
El manejo y combinación de las tecnologías utilizadas permite la posibilidad de escalar el proyecto, de esta manera se busca la mejora continua pensando a futuro.

 
# Referencias
Pressman, Roger S., (2021) Ingeniería de software. McGraw-Hill Interamericana. Capitulo 24, 25, 26 página de la 490 a  548
Omaña, M. (2012). Manufactura esbelta: una contribución para el desarrollo de software con calidad. Red Enlace página de la 14 a  18.


