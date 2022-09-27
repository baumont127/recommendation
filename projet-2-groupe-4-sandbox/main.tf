terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.95.0"
    }
  }

  backend "http" {
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_subscription" "subscription" {
}

resource "azurerm_resource_group" "p2_rg" {
  name     = "p7-projet2"
  location = "France Central"
}

resource "azurerm_app_service_plan" "p2_asp" {
  name                = "p7-projet2-app-service-plan"
  location            = azurerm_resource_group.p2_rg.location
  resource_group_name = azurerm_resource_group.p2_rg.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Free"
    size = "F1"
  }
}

# For each group: create an app service resource
resource "azurerm_app_service" "app_service" {
  for_each = toset(["groupe1", "groupe2", "groupe3", "groupe4", "groupe5"])

  name                = "p7-projet2-${each.value}-app-service"
  location            = azurerm_resource_group.p2_rg.location
  resource_group_name = azurerm_resource_group.p2_rg.name
  app_service_plan_id = azurerm_app_service_plan.p2_asp.id

  site_config {
    linux_fx_version          = "PYTHON|3.8"
    scm_type                  = "LocalGit"
    always_on                 = false
    use_32_bit_worker_process = true
    websockets_enabled        = true
  }
}

# For each user: assign the editor role to the group app service
resource "azurerm_role_assignment" "app_service_role_assignment" {
  for_each = {
    avasilache = {
      group        = "groupe1"
      principal_id = "60d818b5-0a6d-4ef2-aa9c-1b7db0745d5a"
    }
    mdebot = {
      group        = "groupe1"
      principal_id = "7577f92e-87a9-4479-92f3-10e030665e98"
    }
    tquach = {
      group        = "groupe1"
      principal_id = "784d201f-dce3-4920-a541-780a356b9e68"
    }

    kzeghmati = {
      group        = "groupe2"
      principal_id = "c2e0a49e-b437-4dcb-8bfd-30fc99651b76"
    }
    mboulli = {
      group        = "groupe2"
      principal_id = "abf6322e-4427-4cb9-b2bb-66b02369f24f"
    }
    abroumi = {
      group        = "groupe2"
      principal_id = "53dc4c9c-3f94-417f-a7ad-6fc4642c5b0d"
    }

    gcaferra = {
      group        = "groupe3"
      principal_id = "beee6421-90a1-4daf-8e72-6db181182643"
    }
    cferrand = {
      group        = "groupe3"
      principal_id = "07907939-33fe-45d2-a621-347b863b8948"
    }
    wvalerio = {
      group        = "groupe3"
      principal_id = "09842680-21ca-4310-a3bb-7c07afb58a63"
    }

    nboukachab = {
      group        = "groupe4"
      principal_id = "6b300ba5-e864-4cac-b380-6fc391aed854"
    }
    rzein = {
      group        = "groupe4"
      principal_id = "1720026a-eef4-4cee-962a-cb4e12691471"
    }
    cbaumont = {
      group        = "groupe4"
      principal_id = "6657a8ea-e868-496c-9180-836bc0f03cb8"
    }

    theadrapson = {
      group        = "groupe5"
      principal_id = "ef93c8c2-6d22-4216-ac42-145b4988396f"
    }
    dardiles = {
      group        = "groupe5"
      principal_id = "a3443234-555e-4c4b-ad6a-6f47468bf7d1"
    }
  }

  scope                = azurerm_app_service.app_service[each.value.group].id
  role_definition_name = "Contributor"
  principal_id         = each.value.principal_id
}

# For each group: create a cognitive service for text analytics
resource "azurerm_cognitive_account" "text_analytics" {
  for_each = toset(["groupe1", "groupe2", "groupe3", "groupe4"])

  name                = "p7-projet2-${each.value}-text-analytics"
  location            = azurerm_resource_group.p2_rg.location
  resource_group_name = azurerm_resource_group.p2_rg.name
  kind                = "TextAnalytics"
  sku_name            = "S"
}

# For each user: assign the editor role to the group text analytics
resource "azurerm_role_assignment" "text_analytics_role_assignment" {
  for_each = {
    avasilache = {
      group        = "groupe1"
      principal_id = "60d818b5-0a6d-4ef2-aa9c-1b7db0745d5a"
    }
    mdebot = {
      group        = "groupe1"
      principal_id = "7577f92e-87a9-4479-92f3-10e030665e98"
    }
    tquach = {
      group        = "groupe1"
      principal_id = "784d201f-dce3-4920-a541-780a356b9e68"
    }

    kzeghmati = {
      group        = "groupe2"
      principal_id = "c2e0a49e-b437-4dcb-8bfd-30fc99651b76"
    }
    mboulli = {
      group        = "groupe2"
      principal_id = "abf6322e-4427-4cb9-b2bb-66b02369f24f"
    }
    abroumi = {
      group        = "groupe2"
      principal_id = "53dc4c9c-3f94-417f-a7ad-6fc4642c5b0d"
    }

    gcaferra = {
      group        = "groupe3"
      principal_id = "beee6421-90a1-4daf-8e72-6db181182643"
    }
    cferrand = {
      group        = "groupe3"
      principal_id = "07907939-33fe-45d2-a621-347b863b8948"
    }
    wvalerio = {
      group        = "groupe3"
      principal_id = "09842680-21ca-4310-a3bb-7c07afb58a63"
    }

    nboukachab = {
      group        = "groupe4"
      principal_id = "6b300ba5-e864-4cac-b380-6fc391aed854"
    }
    rzein = {
      group        = "groupe4"
      principal_id = "1720026a-eef4-4cee-962a-cb4e12691471"
    }
    cbaumont = {
      group        = "groupe4"
      principal_id = "6657a8ea-e868-496c-9180-836bc0f03cb8"
    }
  }

  scope                = azurerm_cognitive_account.text_analytics[each.value.group].id
  role_definition_name = "Contributor"
  principal_id         = each.value.principal_id
}
