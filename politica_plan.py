import json
import sys


EXPECTED_ADDRESSES = {
    "module.portal.terraform_data.ficha": "portal",
    "module.ayuda.terraform_data.ficha": "ayuda",
}
EXPECTED_INPUTS = {"nombre", "entorno"}
ALLOWED_ENVIRONMENTS = {"desarrollo", "pruebas", "integracion"}
SUCCESS_MESSAGE = (
    "POLÍTICA APROBADA: dos fichas ficticias, mismo entorno y sin operaciones reales"
)


def rechazar(motivo):
    print(f"POLÍTICA RECHAZADA: {motivo}")
    raise SystemExit(1)


def marcado_como(cambio, metadata_name, campo):
    metadata = cambio.get(metadata_name)
    if metadata is True:
        return True
    if not isinstance(metadata, dict):
        return False

    input_metadata = metadata.get("input")
    if input_metadata is True:
        return True
    return isinstance(input_metadata, dict) and input_metadata.get(campo) is True


def main():
    try:
        plan = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        rechazar("no se pudo leer un JSON válido del plan.")

    if not isinstance(plan, dict) or "resource_changes" not in plan:
        rechazar("el plan debe contener resource_changes.")

    cambios = plan["resource_changes"]
    if not isinstance(cambios, list):
        rechazar("resource_changes debe ser una lista.")
    if len(cambios) != 2:
        rechazar("se esperaban exactamente dos cambios.")

    cambios_por_direccion = {}
    for cambio_recurso in cambios:
        if not isinstance(cambio_recurso, dict):
            rechazar("cada cambio de recurso debe ser un objeto.")

        direccion = cambio_recurso.get("address")
        if not isinstance(direccion, str) or direccion not in EXPECTED_ADDRESSES:
            rechazar(f"dirección de recurso no permitida: {direccion!r}.")
        if direccion in cambios_por_direccion:
            rechazar(f"dirección de recurso repetida: {direccion}.")
        cambios_por_direccion[direccion] = cambio_recurso

    for direccion, ficha in EXPECTED_ADDRESSES.items():
        cambio_recurso = cambios_por_direccion.get(direccion)
        if cambio_recurso is None:
            rechazar(f"falta la ficha esperada: {direccion}.")
        if cambio_recurso.get("mode") != "managed":
            rechazar(f"{direccion} debe ser un recurso managed.")
        if cambio_recurso.get("type") != "terraform_data":
            rechazar(f"{direccion} debe ser de tipo terraform_data.")

        cambio = cambio_recurso.get("change")
        if not isinstance(cambio, dict):
            rechazar(f"falta change para {direccion}.")
        if cambio.get("actions") != ["create"]:
            rechazar(f"{direccion} solo puede tener la acción create.")

        despues = cambio.get("after")
        if not isinstance(despues, dict):
            rechazar(f"falta change.after para {direccion}.")
        entrada = despues.get("input")
        if not isinstance(entrada, dict):
            rechazar(f"falta change.after.input para {direccion}.")

        propiedades_extra = set(entrada) - EXPECTED_INPUTS
        if propiedades_extra:
            rechazar(
                f"{direccion} contiene entradas no permitidas: "
                f"{', '.join(sorted(propiedades_extra))}."
            )

        for campo in EXPECTED_INPUTS:
            if campo not in entrada:
                rechazar(f"falta {campo} en change.after.input de {direccion}.")
            if marcado_como(cambio, "after_unknown", campo):
                rechazar(f"{campo} de {direccion} tiene un valor desconocido.")
            if marcado_como(cambio, "after_sensitive", campo):
                rechazar(f"{campo} de {direccion} está marcado como sensible.")
            if not isinstance(entrada[campo], str):
                rechazar(f"{campo} de {direccion} debe ser una cadena conocida.")

        nombre = entrada["nombre"]
        entorno = entrada["entorno"]
        if not nombre.startswith("portal-"):
            rechazar(f"el nombre de {direccion} debe empezar por portal-.")
        if ficha == "ayuda" and nombre != "portal-ayuda":
            rechazar("la ficha de ayuda debe llamarse portal-ayuda.")
        if entorno not in ALLOWED_ENVIRONMENTS:
            rechazar(f"entorno no permitido para {direccion}: {entorno}.")

    entorno_portal = cambios_por_direccion[
        "module.portal.terraform_data.ficha"
    ]["change"]["after"]["input"]["entorno"]
    entorno_ayuda = cambios_por_direccion[
        "module.ayuda.terraform_data.ficha"
    ]["change"]["after"]["input"]["entorno"]
    if entorno_portal != entorno_ayuda:
        rechazar("portal y ayuda deben pertenecer al mismo entorno.")

    print(SUCCESS_MESSAGE)


if __name__ == "__main__":
    main()
