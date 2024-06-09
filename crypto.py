from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from rich import print
from rich.table import Table

class Controller:
    def __init__(self) -> None:
        self.user = User()
        self.menu = MenuManager()
        self.data = DataBase()

    def Run(self):
        while True:
            self.menu.ShowMenu(self.user)
            menuoption = self.menu.GetAnswer()
            print('\n')
            
            if menuoption == 1:
                #update info and show
                listelements = self.data.UpdateData()
                print(self.data.AllElementsInTable(listelements))

            elif menuoption == 2:
                #filter the data
                print("Select an option:")
                print("1. Lowest price (Price column)")
                print("2. Highest percentage change (%Change column)")
                option = None
                while option not in [1, 2]:
                    option = int(input("Enter your choice (1 or 2): "))
                num_cryptos = int(input("Enter the number of cryptocurrencies to filter: "))

                sortedcrypto= self.data.BestsCryptoCurrencies(listelements, option, num_cryptos)
                print(self.data.AllElementsInTable(sortedcrypto))

            elif menuoption == 3:
                crypto = input("Enter the Symbol or the Name of the crypto that you want find: ")
                findcrypto= self.data.SearchCryptoCurrencie(listelements, crypto)
                if findcrypto:
                    print(self.data.AllElementsInTable(findcrypto))
                else:
                    print('We could not find your crypto')

            elif menuoption == 4:
                num_cryptos = int(input("Enter the number of cryptocurrencies to filter: "))

                sortedcrypto= self.data.HighPriceAndPositiveChange(listelements, num_cryptos)
                print(self.data.AllElementsInTable(sortedcrypto))

            elif menuoption == 5:
                link = input('link: ')
                sortedcrypto= self.data.addCoin(listelements, link)
                print(self.data.AllElementsInTable(sortedcrypto))
            elif menuoption == 6:
                break
            else:
                print('Enter a valid option')

class User:
    def __init__(self) -> None:
        self.menu = "1. Update information\n2. Best CryptoCurrencies\n3. Search CryptoCurrencies\n4. High Cost and positive change CryptoCurrencies \n5. Add crypto \n6. Exit"

    def GetMenu(self):
        return self.menu
    
class MenuManager:    
    def ShowMenu(self, user):
        print(user.GetMenu())
    def GetAnswer(self):
        try:
            return int(input("option: "))
        except:
            return 10
    
        
class DataBase:
    def __init__(self) -> None:
        self.Data = []

    def UpdateData(self):
        # Configurar opciones de Chrome
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        # Conectar al driver y a la página web
        service = ChromeService(executable_path="C:\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://finance.yahoo.com/crypto?offset=0&count=100")
        # Extraer la siguiente información 
        # Symbol, Name, Price (Intraday), Change, %Change y Market Cap
        Symbol = driver.find_elements(By.XPATH, "//a[@data-test='quoteLink']")
        Name = driver.find_elements(By.XPATH, "//td[@class='Va(m) Ta(start) Px(10px) Fz(s)']")
        Price = driver.find_elements(By.XPATH, "//fin-streamer[@data-field='regularMarketPrice']")
        Change = driver.find_elements(By.XPATH, "//fin-streamer[@data-field='regularMarketChange']")
        Changepercentage = driver.find_elements(By.XPATH, "//fin-streamer[@data-field='regularMarketChangePercent']")
        Marketcap = driver.find_elements(By.XPATH, "//fin-streamer[@data-field='marketCap']")
        # Extraer el texto en la lista
        def extract_text(lst):
            # Caso base
            if not lst:
                return lst
            # Caso recursivo
            rest = extract_text(lst[1:])
            lst[0] = lst[0].text
            return [lst[0]] + rest
        
        def extract_attribute(lst, attribute):
            # Caso base
            if not lst:
                return lst
            # Caso recursivo
            rest = extract_attribute(lst[1:], attribute)
            lst[0] = lst[0].get_attribute(attribute)
            return [lst[0]] + rest
        
        Symbol = extract_text(Symbol)
        Name = extract_text(Name)
        Price = extract_attribute(Price, 'value')
        Change = extract_text(Change)
        Changepercentage = extract_attribute(Changepercentage, 'value')
        Marketcap = extract_text(Marketcap)
        # Unir elementos
        listelements = list(zip(Symbol, Name, Price, Change, Changepercentage, Marketcap))
        driver.quit()
        return listelements

    
    def addCoin(self, listelements, link):
        # Configurar opciones de Chrome
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        # Conectar al driver y a la página web
        service = ChromeService(executable_path="C:\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(link)
        # Extraer la siguiente información 
        # Symbol, Name, Price (Intraday), Change, %Change y Market Cap
        cadena = driver.find_elements(By.XPATH, "//div[@class='D(ib) Mend(20px)']")
        cadena2 =  driver.find_elements(By.XPATH, "//h1[@class='D(ib) Fz(18px)']")
        Marketcap = driver.find_elements(By.XPATH, "//td[@data-test='MARKET_CAP-value']")

        # Extraer el texto en la lista
        def extract_text(lst):
            # Caso base
            if not lst:
                return lst
            # Caso recursivo
            rest = extract_text(lst[1:])
            lst[0] = lst[0].text
            return [lst[0]] + rest

        cadena = extract_text(cadena)
        cadena2 = extract_text(cadena2)
        cadena3 = extract_text(Marketcap)

        cadena=cadena[0]
        cadena2=cadena2[0]
        Marketcap=cadena3[0]

        indice_signo = cadena.index('-') if '-' in cadena else cadena.index('+')
        Price = cadena[:indice_signo]

        indice_parentesis = cadena.index('(')
        indice_cierre_parentesis = cadena.index(')')
        Changepercentage = cadena[indice_parentesis+1:indice_cierre_parentesis]

        indice_porcentaje = cadena.index('%')
        Change =cadena[indice_signo:indice_parentesis-1]

        partes = cadena2.split(" (")
        Name = partes[0]
        Symbol = partes[1][:-1]

        # Imprimir los resultados
        lista = [Symbol,Name,Price,Change,Changepercentage,Marketcap]

        devuelve = self.SearchCryptoCurrencie( listelements, lista[0])
        driver.quit()
        if devuelve:
            print('el elemento ya se encuentra')
            self.AllElementsInTable(devuelve)
            return listelements
        else:
            listelements.append(tuple(lista))
            return listelements


    def AllElementsInTable(self, listelements):
        table = Table('Num', 'Symbol', 'Name', 'Price (Intraday)', 'Change', '%Change', 'Market Cap')
        for i, row in enumerate(listelements, 1):
            table.add_row(str(i), *row)
        return table

    def BestsCryptoCurrencies(self, listelements, option, num):
        #lowest price option
        if option == 1:
            sorted_crypto = sorted(listelements, key=lambda x: float(x[2].replace(',', '')))
        #Highest percentage change    
        else:
            sorted_crypto = sorted(listelements, key=lambda x: float(x[4][:-1]), reverse=True)

        return(sorted_crypto[:num])

    def SearchCryptoCurrencie(self, listelements, crypto):
        return list(filter(lambda x: x[0]==crypto or x[1]==crypto, listelements))

    def HighPriceAndPositiveChange(self, listelements, num):
        def fun(variable):
            if (variable[4][0] == '+'):
                return True
            else:
                return False
        sorted_crypto = filter(fun, listelements)
        sorted_crypto = sorted(sorted_crypto, key=lambda x: float(x[2].replace(',', '')),reverse=True)
        return sorted_crypto[:num]


if __name__ == '__main__':
    system = Controller()
    system.Run()