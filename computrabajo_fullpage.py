from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def iniciar_driver():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://bo.computrabajo.com/")
    driver.maximize_window()
    return driver

def quitar_popup(wait):
    try:
        boton_ahora_no = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Ahora no']"))
        )
        boton_ahora_no.click()
    except:
        pass
    wait.until(
        EC.invisibility_of_element((By.ID, "pop-up-webpush-background"))
    )

def extraer_datos_anuncio(anuncio, wait):
    anuncio.click()
    time.sleep(1)
    detail_section = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "box_detail"))
    )
    titulo_anuncio = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title_offer"))
    ).text
    header_detail = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "header_detail"))
    )
    div_contenedor = header_detail.find_element(By.TAG_NAME, "div")
    parrafos = div_contenedor.find_elements(By.TAG_NAME, "p")
    subtexto_anuncio = parrafos[0].text if len(parrafos) > 0 else ""
    empresa_anuncio = parrafos[1].text if len(parrafos) > 1 else ""
    lugar_anuncio = parrafos[2].text if len(parrafos) > 2 else ""
    mbB_div = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mbB"))
    )
    mbB_parrafos = mbB_div.find_elements(By.TAG_NAME, "p")
    pago_anuncio = jornada_anuncio = lugar_trabajo_anuncio = contrato_anuncio = ""
    for p in mbB_parrafos:
        icon = p.find_element(By.TAG_NAME, "span")
        icon_class = icon.get_attribute("class")
        texto = p.text.strip()
        if "i_money" in icon_class:
            pago_anuncio = texto
        elif "i_clock" in icon_class:
            jornada_anuncio = texto
        elif "i_home" in icon_class:
            lugar_trabajo_anuncio = texto
        elif "i_find" in icon_class:
            contrato_anuncio = texto
    descripcion_anuncio = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "t_word_wrap"))
    ).text
    requisitos_ul = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "ul"))
    )
    requisitos_anuncio = [req.text.strip() for req in requisitos_ul.find_elements(By.TAG_NAME, "li")]
    return {
        "titulo": titulo_anuncio,
        "empresa": empresa_anuncio,
        "lugar": lugar_anuncio,
        "subtexto": subtexto_anuncio,
        "pago": pago_anuncio,
        "jornada": jornada_anuncio,
        "lugar_trabajo": lugar_trabajo_anuncio,
        "contrato": contrato_anuncio,
        "descripcion": descripcion_anuncio,
        "requisitos": ", ".join(requisitos_anuncio)
    }

def main():
    driver = iniciar_driver()
    wait = WebDriverWait(driver, 10)
    buscador_cargo = wait.until(EC.presence_of_element_located((By.ID, "prof-cat-search-input")))
    buscador_cargo.send_keys("Developer" + Keys.ENTER)
    anuncios = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "box_offer"))
    )
    print(f"Se encontraron {len(anuncios)} anuncios")
    quitar_popup(wait)
    anuncios_data = []
    for anuncio in anuncios:
        datos = extraer_datos_anuncio(anuncio, wait)
        anuncios_data.append(datos)
    pd.DataFrame(anuncios_data).to_csv("anuncios.csv", index=False)
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()