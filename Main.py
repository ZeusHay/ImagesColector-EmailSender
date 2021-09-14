import smtplib, email.message
from typing import cast
from selenium import webdriver
from config import *

def getPageImages(imagesCount: 3):
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get("https://lojahaven.com.br/")
    driver.find_element_by_xpath('//*[@id="menu-item-6232"]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div[2]/div/div/div[2]/ul/li[5]/a').click()
    imageList = []
    for _ in range(imagesCount):
        _ = _ + 1
        elementCalca = driver.find_elements_by_xpath(f'//*[@id="wrapper"]/div[2]/div[3]/div/div/div[2]/ul/li[{_}]/div/figure/a[1]/img')
        imageList.append(elementCalca[0].get_attribute('src'))
        
    return imageList
def send_mail_function(Titulo, Conteudo, Destinatario):
    msg = email.message.Message()
    msg['Subject'] = f"{Titulo}"
    msg['From'] = f"{Config['email']}"
    password = f"{Config['senha']}"
    msg['To'] = f"{Destinatario}"
    content = f"{Conteudo}"

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(content)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email Enviado com Sucesso')
def checks():
    email = True
    senha = True
    imagesCount = True
    destinatario = True
    mensagem = True
    titulo = True

    if (Config['imagesCount'] < 0):
        imagesCount = False
        print('Você escolheu uma quantidade de imagens menor quê 1')

    if not(Config['email']):
        email = False
        print('Você não escolheu nenhum Email para login.')

    if not(Config['senha']):
        senha = False
        print('Você não definiu a senha de login.')

    if not(Config['destinatário']):
        destinatario = False
        print('Você não escolheu nenhum destinatario')

    if not(Config['mensagem']):
        mensagem = False
        print('Você não atribuiu nenhuma mensagem ao e-mail!')

    if not(Config['titulo']):
        titulo = False
        print('Você não selecionou nenhum ttitulo')

    if (email and senha and imagesCount and destinatario and mensagem and titulo):
        return True
    else:
        return False

setup = checks()
if (setup):
    images = getPageImages(Config['imagesCount'])
    ImagensList = ""
    count = 0
    for image in images:
        try:
            count = count + 1
            ImagensList = ImagensList + f"""<p>Imagem {count}:</p>
        <p><img src="{image}" alt="imagem{count}" /></p>
        """
        except Exception as e:
            pass

    send_mail_function(Config['titulo'], Config['mensagem'] + f'{ImagensList}', Config['destinatário'])