locals {
  catalogo = {
    portal   = var.nombre_aplicacion
    ayuda    = "portal-ayuda"
    informes = "portal-informes"
  }
}

module "fichas" {
  source   = "./modulo_ficha"
  for_each = local.catalogo

  nombre  = each.value
  entorno = var.entorno
}
