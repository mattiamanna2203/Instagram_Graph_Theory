"""
QUANDO SI IMPORTA QUESTO BOT FARE LE SEGUENTI COSE:
    - Inserire le credenziali dei propri account instagram
    - Modificare i percorsi file
"""



#%% Pacchetti
## Importazione pacchetti per selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
#from selenium.common.exceptions import TimeoutException

## Per automatizzare comportamenti particolari
#import pyautogui


## Per aprire cartelle
import os
import shutil

## Importazione pacchetti per gestire HTML
from bs4 import BeautifulSoup

## Pacchetti per lavorare con stringhe
#import re #regex

## Importazione pacchetti per esportare in csv
import pandas as pd  

## Per lavorare con le date
#from datetime import date 

## Per utilizzare time.sleep
import time 

## Barra di caricamento 
from tqdm import tqdm as tqdm

## Gestire warnings
import warnings
warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.")




#%% Definizione parametri

## Definizione variabili globali
global relogs 
global passwords 
global usernames 

## Scelta profilo per scraping
relogs =    1
usernames = {1:""}
passwords = {1:""}


## Definizione percorsi file

### Path per il driver
path_driver= "Scraper/chromedriver130" #Questo è un driver per mac-arm64 per google versione (va aggiornato ogni volta che c'è un aggiornamento sostanziale di chrome)

### Path per IG Tool following extractor 
path_crx="Scraper/Strumento di Esportazione Follower di Instagram  IG Follower Export Tool 1.3.18.0.crx"


path_utenti_da_estrarre = "/Data/File di log/scraping1_+500following.csv"

path_utenti_estratti = "/Data/File di log/scraping4.csv"

path_utenti_problemi = "/Data/File di log/scraping4_errori.csv"

### Path della cartella nella quale il sistema operativo salva i dati
download_folder = "specificare"

### Path per la cartella dove salvare i following per ogni utente
path_csv_following = "/Data"


#%% Codice


########################################################################
########################################################################
################### PRENDERE GLI UTENTI DEL TIER X #####################
########################################################################

utenti_da_estrarre=pd.read_csv(path_utenti_da_estrarre)
utenti_estratti=pd.read_csv(path_utenti_estratti)
utenti_estratti2=pd.read_csv(path_utenti_problemi)

utenti_da_estrarre = list(utenti_da_estrarre.user)
utenti_estratti=list(utenti_estratti.user)
utenti_estratti2 =  list(utenti_estratti2.user)

lista_utenti = list(filter(lambda x: x not in utenti_estratti, utenti_da_estrarre))
lista_utenti = list(filter(lambda x: x not in utenti_estratti2, lista_utenti))
########################################################################
########################################################################
########################################################################
########################################################################
def click_cookie_button():
    """
    Questa funzione si occupa di accettare i cookies quando si fa il log-in per instagram.  
    Siccome in data 06/12/2023 ho riscontrato problemi con il metodo di  accettazione 3, inizialemente l'unico, ho
    implementato questa funzione in modo che possa gestire questo problema.
    """
    try:
        # Metodo di accettazione 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Consenti tutti i cookie']"))).click()
        print("Cookie accettati metodo 1")
        return 
    except:
        pass
    
    try:
        # Metodo di  accettazione 2
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button._a9-- _ap36 _a9_0"))).click()
        print("Cookie accettati metodo 2")
        return 
    except:
        pass

    try:
        # Metodo di  accettazione 3
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button._a9--._ap36._a9_0"))).click()
        print("Cookie accettati metodo 3")
        return 
    except:
        pass



def cliccare_su_ignora():
    """
    Questa funzione prova a cliccare sul tasto antiscraping che appare ogni tanto. 
    """
    # Se appare la finestra che indica sospetti di essere un bot, cliccare sul tasto Ignora
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Ignora']"))).click()
    except:
        pass
    
    # Se appare la finestra che indica sospetti di essere un bot, cliccare sul tasto Ignora
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Ignora']"))).click()
    except:
        pass 
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Ignora']"))).click()
    except:
        pass 

def log_in_instagram():
    """
    Questa funzione gestisce il processo accesso nell'account di instagram.  
    Non prende parametri, utilizza le variabili globali:
    - relogs 
    - passwords 
    - usernames  
    """
    global service, driver, options
    
    service = Service(executable_path=path_driver)
    options = webdriver.ChromeOptions()

    options.add_extension(path_crx)
    driver = webdriver.Chrome(service=service, options=options)


    #driver.maximize_window()
    driver.set_window_size(600, 800) 
    driver.set_window_position(0,0)
    
    #time.sleep(60)
    driver.get("https://www.instagram.com/") 
    
    # Recupera gli ID delle schede aperte
    ## Chiudere la finestra del TOOL IG che compare.
    time.sleep(2)

 

    # Consenti tutti i cookie
    click_cookie_button()

    
    username=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
    password=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))
    #Eliminare eventuali cose scritte nei box per il login
    username.clear()
    password.clear()

    
    # Inserire le proprie credenziali
    
    ## Inserire username
    time.sleep(2)
    username.send_keys(usernames[relogs])
    

    ## Inserire password
    time.sleep(2)
    password.send_keys(passwords[relogs])
    
    
    ## Cliccare sul pulsante di accesso
    time.sleep(1)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()
    
    
    # Se appare la finestra che indica sospetti di essere un bot, cliccare sul tasto Ignora
    cliccare_su_ignora()
    

    time.sleep(60)


    



def scrape_tool(profile_name):
    print("launching")
    
    # Launch the exporting tool
    driver.get("chrome-extension://kicgclkbiilobmccmmidfghnijgfamdb/options.html")
    #---------------------------------------------------------------------------------#
    
    
    # Insert the  nickname  of the profile to scrape
    ## Identify the cell where the name must be written
    instagram_profile=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Instagram user name like @cristiano or a full URL']")))
    
    ## Delete old text, if there is one.
    instagram_profile.clear()
    
    ## Insert the new nickname
    instagram_profile.send_keys(profile_name)
    #---------------------------------------------------------------------------------#
    
    
    # Parameter setup
    ## Setup the request delays
    delays=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Seconds']")))

    ### Delete old text, if there is one.
    delays.clear()
    
    ### Insert new delay
    delays.send_keys("20")
    
    
    ## Specify that following must be taken
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @value='2']"))).click()
    #---------------------------------------------------------------------------------#
    
    
    # Launch the analysis
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Start New Parsing ']"))).click()
    #---------------------------------------------------------------------------------#
    
    time.sleep(60)
    
    last_extraction = 0 
    iterazioni = 0
    while True:
        
        # Get extraction info
        
        html=driver.page_source # Get the html
        html=BeautifulSoup(html,'html.parser')           # Convert the string into a beautifulSoup object
        html = html.find_all("div",{"class":"stat-row"}) # Select the table that contain the info
        
        extraction_info = {} # Initialize the dictionary
        for col in html:
            
            left = col.find("span",{"class":"left"}).text 
            right = col.find("span",{"class":"right"}).text
    
    
            # Extract the total number of following
            if (left == "Total profiles") or (left == "Found profiles"):
                extraction_info[left] = int(right) 
        
    
            else:
                extraction_info[left] = right
                
    
    
    
        # Check if we must exit the loop or not
        #print(extraction_info)
        
        
        # Break the loop in case of errors
        if extraction_info["Errors"] == " Your Instagram Account was suspended. ":
            return {"user":profile_name,
                    "following_estratti":extraction_info["Found profiles"],
                    "following_totali":extraction_info["Total profiles"],
                    "Errors":1,
                    "Error code":" Your Instagram Account was suspended. "
                    }
        
        if  extraction_info["Errors"] ==" IG user name is invalid ":
            return {"user":profile_name,
                    "following_estratti":extraction_info["Found profiles"],
                    "following_totali":extraction_info["Total profiles"],
                    "Errors":1,
                    "Error code":" IG user name is invalid "
                    }
            
     
        
        
        ## If Found profiles are equal or bigger than the profiles available we retrieved all the profiles SO EXIT THE LOOP
        if (extraction_info["Found profiles"] >= extraction_info["Total profiles"]) : #or (extraction_info["Status"] == " Finished ")
            break
        
        ## Check if the loop is stuck
        
        ### If the loop is stuck add + 1, when this counter will reach 10 we will exit the loop
        if last_extraction ==  extraction_info["Found profiles"]:
            iterazioni += 1
           
            
        ### Restart the counter if the loop comes out from a stuck
        else:
            iterazioni = 0 
          
        ### If the loop is stuck 6 times (1 minute) exit the loop
        if iterazioni >= 6:
            if  extraction_info["Found profiles"] == 0:
                return {"user":profile_name,
                        "following_estratti":extraction_info["Found profiles"],
                        "following_totali":extraction_info["Total profiles"],
                        "Errors":1,
                        "Error code":" Loop stuck, check if private "
                        }
        
            break
        last_extraction = extraction_info["Found profiles"]
        time.sleep(10)



    

    #---------------------------------------------------------------------------------#
    

    # Export the data
    ## Identify the button to export the data and click
    
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[class='export-button-left']"))).click()
    #---------------------------------------------------------------------------------#
        
        time.sleep(60)
        return {"user":profile_name,
                "following_estratti":extraction_info["Found profiles"],
                "following_totali":extraction_info["Total profiles"],
                "Errors":0}
    except:
        time.sleep(60)
        return {"user":profile_name,
                "following_estratti":extraction_info["Found profiles"],
                "following_totali":extraction_info["Total profiles"],
                "Errors":1,
                "Error code":"Unknown"
                }

def naming_csv(user,download_folder,path_csv_following):
    """
    Questa funzione prendere il file csv scaricato dalla funzione export_data, lo rinomina e lo sposta nella directory appropriata.  
    """
    os.chdir(download_folder) #Andare alla cartella download nella quale il csv sarà importato
        
    directory_download_files = os.listdir()        #Ottenere una lista di tutti i file presenti sulla directory 
    for i in directory_download_files:             #Iterare sui file per trovare quello esatto
    
        if i == f"{user}_following.csv":            #Se è un csv allora è quello giusto
            
            nuovo_nome_file = f"{user}-following.csv"
            os.rename(i,nuovo_nome_file) #Rinominare secondo una sintassi definita
            
            
            #Viene messo nella cartella TIER-One, se già vi è un file di questo tipo elimina il nuovo file.
            try:
                shutil.move(nuovo_nome_file, path_csv_following)

            except:
                os.remove(nuovo_nome_file)

            break
  






log_in_instagram()

#for i in tqdm(["ddmcs2023"]):
#for i in tqdm(["mahna_mannaa","fsgnjkgsfhijgskjn","ddmcs2023","aurora_ricci"]):
for i in tqdm(lista_utenti):



    results = scrape_tool(i)
    #print(results)
    if results["Errors"] == 0:
        # Inizio scrittura nel file di log
        df=pd.read_csv(path_utenti_estratti)
        
        provvisorio = pd.DataFrame([{"user":results["user"],
                                     "following_estratti":results["following_estratti"],
                                     "following_totali ":results["following_totali"]}
                                    ])
        
        df=pd.concat([df,provvisorio])
        df.to_csv(path_utenti_estratti ,index=False)
        ## Fine scrittura nel file di log
        naming_csv(results["user"],download_folder,path_csv_following)
        
        
    
    else:
        df=pd.read_csv(path_utenti_problemi)
        
        provvisorio = pd.DataFrame([{"user":results["user"],
                                     "errore":results["Error code"]}])
        
        df=pd.concat([df,provvisorio])
        df.to_csv(path_utenti_problemi ,index=False)

    driver.refresh()











