# Mi copia para practicar · laboratorio de IaC e IA

Este repositorio es **tu copia personal** del proyecto ficticio `portal-demo`. Puedes usarla para ensayar el recorrido del alumnado. La [plantilla original](https://github.com/b-regina/iac-ia-laboratorio-demo) es el enlace que debes compartir para que cada participante cree su propia copia.

## Cómo continuar en esta copia

1. Descarga la [Guía del ejercicio 1](GUIAS/Guia_Alumnado_Ejercicio_1.docx?raw=1). Como **ya tienes una copia**, puedes leer el paso de creación y comenzar en **Paso 2 · Comprueba la ejecución inicial**.
2. Abre **Actions → Validacion IaC** y comprueba la ejecución de este repositorio.
3. Para practicar la edición desde el navegador, abre [esta copia en github.dev](https://github.dev/b-regina/Profe-ejercicios), modifica `variables.tf`, haz **Commit & Push** y busca la ejecución correspondiente en Actions.

**Esta copia no es el enlace de entrada del alumnado.** La ruta común de clase utiliza el navegador, una copia personal por alumno, el editor web y la IA en otra pestaña. OpenTofu se instala temporalmente en el ejecutor de Actions; no hay que instalarlo en el ordenador.

## Guías de trabajo

| Orden | Word descargable | Qué añade al mismo proyecto |
| --- | --- | --- |
| 1 | [Primera configuración y primer plan](GUIAS/Guia_Alumnado_Ejercicio_1.docx?raw=1) | Copia, IA, cambio y comprobación. |
| 2 | [Dos escenarios](GUIAS/Guia_Alumnado_Ejercicio_2.docx?raw=1) | Variables y comparación de planes. |
| 3 | [Revisión y gobierno](GUIAS/Guia_Alumnado_Ejercicio_3.docx?raw=1) | Reglas, rama y pull request. |
| 4 | [Automatización y evidencias](GUIAS/Guia_Alumnado_Ejercicio_4.docx?raw=1) | Workflow, error y diagnóstico. |
| 5 | [Módulo reutilizable](GUIAS/Guia_Alumnado_Ejercicio_5.docx?raw=1) | Dos fichas desde un módulo local. |

Los archivos de código iniciales siguen en la raíz: `variables.tf`, `main.tf` y `outputs.tf`. El workflow está en `.github/workflows/validacion.yml`. El proyecto calcula planes con `terraform_data`; no aplica cambios ni despliega infraestructura comercial.

## Arquitectura ficticia

El módulo local `modulo_ficha` permite describir el portal principal y la ficha de ayuda sin duplicar la definición del recurso. Cada llamada recibe su nombre y el entorno común: en el escenario predeterminado se prevén `portal-demo` y `portal-ayuda` en `pruebas`; en integración, `portal-interno` y `portal-ayuda` en `integracion`.

El pipeline revisa recursivamente el formato, valida la configuración y ejecuta ambos planes; también genera un resumen y un artefacto de evidencia. Solo se calculan planes de `terraform_data`: no hay `apply`, servicios cloud, infraestructura desplegada, costes de infraestructura ni observabilidad real. Antes de aprobar una configuración, el equipo debe revisar el cambio de código, los planes y la evidencia.
