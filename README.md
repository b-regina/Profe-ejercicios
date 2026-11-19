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

## Catálogo de fichas

Antes, el portal y la ficha de ayuda se describían con dos bloques de módulo casi iguales. Esa duplicación obliga a mantener la misma configuración en varios lugares y facilita que las llamadas terminen teniendo diferencias accidentales.

El bloque `locals` define el mapa `catalogo`, con las claves `portal` y `ayuda`. Una única llamada al módulo local `modulo_ficha` utiliza `for_each = local.catalogo` para crear una instancia por cada entrada. Cada instancia recibe `each.value` como nombre y comparte `var.entorno`. Así reutilizamos la implementación del módulo sin copiar su definición.

La clave identifica la instancia: por ejemplo, `portal` aparece en la dirección `module.fichas["portal"]`. No es el nombre de la ficha. El valor asociado a esa clave es el que se pasa como nombre: `var.nombre_aplicacion` para `portal` y `"portal-ayuda"` para `ayuda`.

La salida `resumen` recorre las instancias del módulo con una expresión `for` y construye un mapa con la misma clave para cada una. Cada resumen muestra los valores previstos de `nombre` y `entorno`; no representa recursos aplicados.

| Escenario | Ficha `portal` | Ficha `ayuda` | Entorno común |
| --- | --- | --- | --- |
| Predeterminado | `portal-demo` | `portal-ayuda` | `pruebas` |
| Integración (`escenario-integracion.tfvars`) | `portal-interno` | `portal-ayuda` | `integracion` |

### Prueba de gobierno y evidencias

Como prueba controlada, añadimos temporalmente `informes = "portal-informes"` al catálogo. OpenTofu aceptó la configuración y generó un plan con tres recursos `terraform_data`, incluida la instancia `module.fichas["informes"].terraform_data.ficha`. La política Python rechazó el plan con `POLÍTICA RECHAZADA: se esperaban exactamente dos cambios.` La política también limita las direcciones a `portal` y `ayuda`, y comprueba el tipo de recurso, las acciones, los campos, los nombres y los entornos permitidos.

Retiramos la entrada no autorizada y la política se mantuvo sin cambios. La ejecución del pipeline volvió a finalizar correctamente. Esto distingue la validación técnica —si OpenTofu puede interpretar y planificar una configuración— del gobierno de infraestructura —si el cambio cumple las reglas aprobadas por la organización—.

| Evidencia | Resultado |
| --- | --- |
| Base del ejercicio 7: [`4bf3e60`](https://github.com/b-regina/Profe-ejercicios/commit/4bf3e600bc159f7e95d9d30d8bd6f285a5b60b02) | La ejecución de Actions [44512522208](https://github.com/b-regina/Profe-ejercicios/actions/runs/44512522208) terminó correctamente. |
| Prueba de rechazo: [`9e12576`](https://github.com/b-regina/Profe-ejercicios/commit/9e1257638055901a6a1dc165f0b13ea15999c544) | La ejecución [44512695034](https://github.com/b-regina/Profe-ejercicios/actions/runs/44512695034) falló en la política del plan predeterminado, como se esperaba. |
| Corrección: [`6813dec`](https://github.com/b-regina/Profe-ejercicios/commit/6813dec8a271983fa9415c4f27bd4ab2146c2c37) | La ejecución de recuperación [44514278257](https://github.com/b-regina/Profe-ejercicios/actions/runs/44514278257) completó correctamente los planes y ambas políticas. |

### Límites del laboratorio

El módulo usa `terraform_data` para representar fichas ficticias. Los ejercicios calculan planes, pero no ejecutan `tofu apply`, no despliegan recursos cloud y no proporcionan una plataforma real de autoservicio. Las políticas del laboratorio son didácticas; no equivalen a controles de producción protegidos.

Las claves de `for_each` forman parte de las direcciones de las instancias. Si esas direcciones cambian en una infraestructura que ya se aplicó, OpenTofu podría proponer reemplazos; antes de aplicar, el equipo debe evaluar y gestionar la migración del estado, por ejemplo con bloques `moved` cuando corresponda.

## Política del laboratorio

La política acepta exactamente dos fichas ficticias: `portal` y `ayuda`. Exige que compartan un entorno permitido para mantener ambas partes del ejemplo alineadas; `validate` comprueba la coherencia técnica de la configuración, `plan` calcula los cambios previstos y la política decide si esos cambios respetan las reglas del laboratorio.

En GitHub Actions puedes revisar los planes, las decisiones de ambas políticas y el resumen de resultados del trabajo **Validacion IaC**; también se publica un artefacto de evidencia con ese resumen. Aquí solo se calculan planes con datos ficticios: no se ejecuta `apply` ni se despliega infraestructura. Esta política es didáctica y no equivale a una aprobación de producción.
