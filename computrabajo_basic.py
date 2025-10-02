from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://bo.computrabajo.com/")
# Tiempo de espera explicito para toda la pagina
wait = WebDriverWait(driver, 10)

# Obteniendo la entrada de texto de busqueda
buscador_cargo = wait.until(EC.presence_of_element_located((By.ID, "prof-cat-search-input")))
buscador_cargo.send_keys("Developer"+ Keys.ENTER)

# Obteniendo los anuncios encontrados
anuncios = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "box_offer"))
)
print(f"Se encontraron {len(anuncios)} anuncios")

# Quitar el pop up si aparece
try:
    boton_ahora_no = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Ahora no']"))
    )
    print("Se encontró el botón 'Ahora no'")
    boton_ahora_no.click()
except:
    print("No se encontró el botón 'Ahora no'")

wait.until(
    EC.invisibility_of_element((By.ID, "pop-up-webpush-background"))
)
    
for anuncio in anuncios:
    
    anuncio.click()
    time.sleep(1)
    detail_section = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME,"show_detail"))
    )
   
    titulo_anuncio = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title_offer"))
    ).text
    empresa_anuncio = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.fs16>a"))
    ).text
    lugar_anuncio = WebDriverWait(detail_section, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.fs16>a"))
    ).text
    



    print(f"{titulo_anuncio} - {empresa_anuncio}")
    detail_close = WebDriverWait(detail_section, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "i_close"))
    )
    detail_close.click()
    # find the element with class box_detail then check if it has not the class show_detail
    wait.until(EC.invisibility_of_element((By.CLASS_NAME, "show_detail")))
time.sleep(200)
driver.quit()