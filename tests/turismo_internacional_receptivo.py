import asyncio
import pandas as pd
from playwright.async_api import async_playwright, expect


async def turismo_receptivo_internacional():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True, slow_mo=50)

        context = await browser.new_context(ignore_https_errors=True)

        page = await context.new_page()

        print("Navegando a la página del Yvera")
        await page.goto("https://tableros.yvera.tur.ar/turismo_internacional/")

        await page.get_by_role("link", name="RECEPTIVO").first.click()

        # ----- SELECTOR DE AÑOS -----

        input_anio = page.locator("#paso + .selectize-control .selectize-input")
        await input_anio.click()

        dropdown = page.locator(".selectize-dropdown.single:visible")
        await expect(dropdown).to_be_visible()

        years_to_select = range(2016, 2025)
        print("Seleccionando años...")
        for year in years_to_select:
            await dropdown.get_by_role("option", name=str(year)).click()
            print(f" - Año {year} seleccionado.")

        await page.keyboard.press("Escape")

        await page.wait_for_timeout(10000)

        # ----- SELECTOR DE PROVINCIA -----

        input_provincia = page.locator("#prov + .selectize-control .selectize-input")
        await input_provincia.click()

        dropdown = page.locator(".selectize-dropdown.single:visible")
        await expect(dropdown).to_be_visible()

        await dropdown.get_by_role("option", name="Mendoza").click()

        await page.keyboard.press("Escape")

        # ----- FILTROS -----

        await page.locator("#agrup + .selectize-control").get_by_role("combobox").click()

        await page.get_by_role("option", name="Tipo de visitante").click()
        await page.get_by_role("option", name= "Paso", exact=True).click()
        await page.get_by_role("option", name="País de residencia (agrup.)").click()

        # ----- DESCARGA -----

        await page.wait_for_selector(selector="#btnSearchReceptivo", state="visible")

        await page.locator("#btnSearchReceptivo").click()

        async with page.expect_download(timeout=30000) as download_info:
            await page.locator("#downloadCSVRec").click()
        
        download = await download_info.value
        
        # Guardamos el archivo con el nombre que nos sugiere el servidor
        file_path = f"descargas/turismo_internacional_receptivo.csv"
        await download.save_as(file_path)
        
        print(f"Archivo descargado y guardado en: {file_path}")
        print(f"URL de descarga: {download.url}")

        await browser.close()                                                                                                                                                            

async def join_data():
    
    df_unificado = pd.DataFrame(index=None)

    df_cordoba = pd.read_csv("./descargas/perfil_receptivo_internacional_Aerop. Córdoba.csv", delimiter=";", )