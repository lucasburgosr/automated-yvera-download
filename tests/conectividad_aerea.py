import asyncio
from playwright.async_api import async_playwright, expect
from datetime import datetime
from dateutil.relativedelta import relativedelta

async def conectividad_aerea_mendoza():

    async with async_playwright() as p:

        clasificaciones = ["Cabotaje", "Internacional"]
        
        browser = await p.chromium.launch(headless=True, slow_mo=50)

        context = await browser.new_context(ignore_https_errors=True)

        page = await context.new_page()

        await page.goto("https://tableros.yvera.tur.ar/conectividad/")

        await page.get_by_role("link", name="CONECTIVIDAD").click()

        for c in clasificaciones:

            # ----- SELECTOR DE CLASIFICACIÓN -----
            input_anio = page.locator("#clasificacion + .selectize-control")
            await input_anio.click()
            dropdown = page.locator(".selectize-dropdown.single:visible")
            await expect(dropdown).to_be_visible()
            await dropdown.get_by_role("option", name=c).click()

            if c == "Cabotaje":
                await page.locator("#agrup3-selectized").click()

                await page.get_by_role("option", name="Mes").click()
                await page.get_by_role("option", name="Empresa agrupada").click()
                await page.get_by_role("option", name="Origen aeropuerto").click()
                await page.get_by_role("option", name="Destino aeropuerto").click()
                await page.get_by_role("option", name="Origen provincia").click()
            else:
                await page.locator("#agrup3-selectized").click()
                await page.keyboard.press("Backspace") 
                await page.get_by_role("option", name="Origen país").click()
                await page.get_by_role("option", name="Origen localidad").click()

            async with page.expect_download(timeout=30000) as download_info:
                await page.locator("#downloadCSVConec").click()
            
            download = await download_info.value
            
            # Guardamos el archivo con el nombre que nos sugiere el servidor
            file_path = f"descargas/conectividad_aerea_{c}.csv"
            await download.save_as(file_path)
            
            print(f"Archivo descargado y guardado en: {file_path}")
            print(f"URL de descarga: {download.url}")

        await browser.close()