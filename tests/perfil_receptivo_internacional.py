import asyncio
from playwright.async_api import async_playwright, expect
import pandas as pd

async def perfil_receptivo_internacional():

    async with async_playwright() as p:

        pasos = ["Ezeiza y Aeroparque", "Aerop. Córdoba", "Aerop. Mendoza", "Cristo Redentor", "Puerto de Buenos Aires"]

        browser = await p.chromium.launch(headless=True, slow_mo=50)

        context = await browser.new_context(ignore_https_errors=True)

        page = await context.new_page()

        print("Navegando a la página del Yvera")
        await page.goto("https://tableros.yvera.tur.ar/turismo_internacional/")

        await page.get_by_role("link", name="PERFIL RECEPTIVO").first.click()

        # ----- SELECTOR DE AÑOS -----

        input_anio = page.locator("#anio_encuesta + .selectize-control .selectize-input")
        await input_anio.click()
        dropdown = page.locator(".selectize-dropdown.multi:visible")
        await expect(dropdown).to_be_visible()
        years_to_select = range(2019, 2025)
        print("Seleccionando años...")
        for year in years_to_select:
            await dropdown.get_by_role("option", name=str(year)).click()
            print(f" - Año {year} seleccionado.")
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(10000)

        # ----- FILTROS -----

        await page.locator("#agrup_p + .selectize-control").get_by_role("combobox").click()
        await page.get_by_role("option", name="Pais de residencia").click()
        await page.get_by_role("option", name= "Provincia visitada", exact=True).click()

        for paso in pasos:

            # ----- SELECTOR DE PASO -----

            input_paso = page.locator("#paso + .selectize-control .selectize-input")
            await input_paso.click()

            dropdown_paso = page.locator(".selectize-dropdown.single:visible")
            await expect(dropdown_paso).to_be_visible()

            await dropdown_paso.get_by_role("option", name=paso).click()

            # ----- SELECTOR DE PROVINCIA -----

            input_provincia = page.locator("#provincia + .selectize-control .selectize-input")
            await input_provincia.click()

            dropdown = page.locator(".selectize-dropdown.multi:visible")
            await expect(dropdown).to_be_visible()

            await page.keyboard.press("Backspace")
            await dropdown.get_by_role("option", name="Mendoza").click()

            await page.keyboard.press("Escape")

            # ----- DESCARGA -----

            await page.wait_for_selector(selector="#btnSearchPerfil", state="visible")

            await page.locator("#btnSearchPerfil").click()

            async with page.expect_download(timeout=30000) as download_info:
                await page.locator("#downloadCSVPerfil").click()
            
            download = await download_info.value
            
            # Guardamos el archivo con el nombre que nos sugiere el servidor
            file_path = f"/descargas/perfil_receptivo_internacional_{paso}.csv"
            await download.save_as(file_path)
            
            print(f"Archivo descargado y guardado en: {file_path}")
            print(f"URL de descarga: {download.url}")

        await browser.close()                                                                                                                                                                                                              

async def join_data():

    df_cordoba = pd.read_csv("./descargas/perfil_receptivo_internacional_Aerop. Córdoba.csv", delimiter=",", low_memory=False)
    df_cordoba["Paso"] = "Aeropuerto de Córdoba"
    df_puerto = pd.read_csv("./descargas/perfil_receptivo_internacional_Puerto de Buenos Aires.csv", delimiter=",", low_memory=False)
    df_puerto["Paso"] = "Puerto de Buenos Aires"
    df_ezeiza_aeroparque = pd.read_csv("./descargas/perfil_receptivo_internacional_Ezeiza y Aeroparque.csv", delimiter=",", low_memory=False)
    df_ezeiza_aeroparque["Paso"] = "Ezeiza y Aeroparque"
    df_cristo = pd.read_csv("./descargas/perfil_receptivo_internacional_Cristo Redentor.csv", delimiter=",", low_memory=False)
    df_cristo["Paso"] = "Cristo Redentor"
    df_mendoza = pd.read_csv("./descargas/perfil_receptivo_internacional_Aerop. Mendoza.csv", delimiter=",", low_memory=False)
    df_mendoza["Paso"] = "Aeropuerto de Mendoza"

    df_final = pd.concat([df_cordoba, df_puerto, df_ezeiza_aeroparque, df_cristo, df_mendoza], axis=0)

    df_final.to_csv("/descargas/perfil_receptivo_internacional_unificado.csv", sep=";", index=False)