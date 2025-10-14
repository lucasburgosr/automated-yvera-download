import asyncio
from playwright.async_api import async_playwright, expect


async def conectividad_terrestre_mendoza():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True, slow_mo=50)

        context = await browser.new_context(ignore_https_errors=True)

        page = await context.new_page()

        print("Navegando a la página del Yvera")
        await page.goto("https://tableros.yvera.tur.ar/conectividad_terrestre/")

        await page.get_by_role("link", name="SERVICIOS REGULARES").click()

        input_fecha = page.locator(".input-daterange .form-control").first

        await input_fecha.click()

        date_picker = page.locator(".datepicker-days")
        await expect(date_picker).to_be_visible()

        await date_picker.locator(".datepicker-switch").click()
        await page.locator(".datepicker-months .datepicker-switch").click()

        year_to_select = "2019"
        year_locator = page.locator(
            ".datepicker-years").get_by_text(year_to_select)
        prev_button = page.locator(".datepicker-years .prev")

        while not await year_locator.is_visible():
            await prev_button.click()
            await page.wait_for_timeout(100)

        await year_locator.click()

        await page.locator(".datepicker-months").get_by_text("Ene").click()

        await date_picker.locator("td.day:not(.old):not(.new)", has_text="1").first.click()

        await expect(input_fecha).to_have_value("2019-01-01")

        await page.locator('[data-id="provinciaDest"]').click()

        await page.get_by_role("button", name="Deseleccionar todo").click()

        dropdown_menu = page.locator(".dropdown-menu.open")

        await dropdown_menu.get_by_text("Mendoza", exact=True).click() 

        await page.keyboard.press("Escape")

        await page.locator("#agrup3 + .selectize-control").get_by_role("combobox").click()

        await page.get_by_role("option", name="Mes").click()
        await page.get_by_role("option", name="Provincia Origen").click()
        await page.get_by_role("option", name="Provincia Destino").click()
        await page.get_by_role("option", name="Día").click()
        await page.get_by_role("option", name="Localidad Origen").click()
        await page.get_by_role("option", name="Localidad Destino").click()

        await page.wait_for_selector(selector="#btnSearch", state="visible")

        await page.locator("#btnSearch").click()

        async with page.expect_download(timeout=30000) as download_info:
            await page.locator("#downloadCSV").click()
        
        download = await download_info.value
        
        # Guardamos el archivo con el nombre que nos sugiere el servidor
        file_path = f"/descargas/conectividad_terrestre_mendoza.csv"
        await download.save_as(file_path)
        
        print(f"Archivo descargado y guardado en: {file_path}")
        print(f"URL de descarga: {download.url}")

        await browser.close()       

async def conectividad_terrestre_pais():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True, slow_mo=50)

        context = await browser.new_context(ignore_https_errors=True)

        page = await context.new_page()

        print("Navegando a la página del Yvera")
        await page.goto("https://tableros.yvera.tur.ar/conectividad_terrestre/")

        await page.get_by_role("link", name="SERVICIOS REGULARES").click()

        input_fecha = page.locator(".input-daterange .form-control").first

        await input_fecha.click()

        date_picker = page.locator(".datepicker-days")
        await expect(date_picker).to_be_visible()

        await date_picker.locator(".datepicker-switch").click()
        await page.locator(".datepicker-months .datepicker-switch").click()

        year_to_select = "2019"
        year_locator = page.locator(
            ".datepicker-years").get_by_text(year_to_select)
        prev_button = page.locator(".datepicker-years .prev")

        while not await year_locator.is_visible():
            await prev_button.click()
            await page.wait_for_timeout(100)

        await year_locator.click()

        await page.locator(".datepicker-months").get_by_text("Ene").click()

        await date_picker.locator("td.day:not(.old):not(.new)", has_text="1").first.click()

        await expect(input_fecha).to_have_value("2019-01-01")

        await page.locator("#agrup3 + .selectize-control").get_by_role("combobox").click()

        await page.get_by_role("option", name="Mes").click()
        await page.get_by_role("option", name="Provincia Origen").click()
        await page.get_by_role("option", name="Provincia Destino").click()

        await page.wait_for_selector(selector="#btnSearch", state="visible")

        await page.locator("#btnSearch").click()

        async with page.expect_download(timeout=30000) as download_info:
            await page.locator("#downloadCSV").click()
        
        download = await download_info.value
        
        # Guardamos el archivo con el nombre que nos sugiere el servidor
        file_path = f"/descargas/conectividad_terrestre_pais.csv"
        await download.save_as(file_path)
        
        print(f"Archivo descargado y guardado en: {file_path}")
        print(f"URL de descarga: {download.url}")

        await browser.close()       
