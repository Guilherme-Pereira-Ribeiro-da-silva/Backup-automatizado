from excel import excel
from backup import backup
import shutil
import os
import time

def InteracaoComOUsuario():
    while True:
        try:
            info = LerExcel(input("Olá,digite o caminho do arquivo excel com as informações de acesso: "))
            print(" ")
            caminho = input("certo.Agora digite o local onde você deseja que os backups sejem salvos(pasta padrão é a raiz do c:): ")

            CriarDiretoriosBackup(caminho,info)
            break
        except:
            #caminho inválido,excel inválido ou com a pasta destino já existente
            print("\033[91m {}\033[00m".format("\nInformações inválidas foram inseridas.Você tem certeza de que o excel e o caminho da"
                                               "do existem, e que já não está ocupado? Tente novamente\n"))

    print(" ")
    print("Certo.Os backups serão realizados")
    GerarRedicencias()
    RealizarBackups(info, caminho)

def GerarRedicencias():
    for i in range(3):
        time.sleep(1)
        print(".",end="")
    time.sleep(1)

def LerExcel(caminho):
    excel_classe = excel("E:\\backup-automatizado\\venv\\src\\arquivos\\excel.xls")
    return excel_classe.GetInfoSites()


def CriarDiretoriosBackup(caminho,info):
    os.mkdir(caminho + "\\backups")
    for i in range(len(info)):
        os.mkdir(caminho + "\\backups" + "\\" + str(info[i][0]))


def RealizarBackups(info,pastaraizcaminho):
    numsucessos = 0
    numfalhas = 0

    for i in range(len(info)):
        browser = backup()
        print("\n("+ str(i + 1) +"/"+ str(len(info)) +") realizando o backup do website: " + info[i][0])
        GerarRedicencias()

        try:
            urlcpanel = "https:\\\\" + info[i][0] + "\\cpanel"
            logincpanel = info[i][1]
            senhacpanel = info[i][2]

            LogarCpanel(logincpanel, senhacpanel, urlcpanel, browser)

            nomearquivo = BaixarBD(browser, pastaraizcaminho)

            # Movendo o arquivo para o local correto
            origem = pastaraizcaminho + "\\" + nomearquivo
            destino = pastaraizcaminho + "\\" + "backups" + "\\" + info[i][0] + "\\" + nomearquivo
            shutil.move(origem, destino)

            print("\033[92m {}\033[00m".format("\nBackup do banco de dados concluído com sucesso!"))

            # fechando a tela do bd e abrindo a do gerenciador de arquivos
            browser.FecharTelaAtual()
            browser.TrocarDePagina(0)  # voltando o browser para a página inicial
            idgerenciador = "item_file_manager"
            browser.ClicarNoElemento(idgerenciador)
            browser.TrocarDePagina(1)  # trocando para a página do gerenciador com id 1

            # esvaziando a lixeira para sobrar espaço para o backup
            EsvaziarLixeira(browser)
            BaixarArquivosSite(browser, pastaraizcaminho)

            # transferindo o backup para o local correto
            origem = pastaraizcaminho + "\\" + "backupsite.zip"
            destino = pastaraizcaminho + "\\" + "backups" + "\\" + info[i][0] + "\\" + "backupsite.zip"
            shutil.move(origem, destino)

            print("\033[92m {}\033[00m".format("\nBackup do website concluído com sucesso!"))

            # fechando a tela do gerenciador e abrindo a do wordpress
            browser.FecharTelaAtual()
            browser.TrocarDePagina(0)  # voltando o browser para a página inicial
            url = "https:\\\\" + info[i][0] + "\\" + info[i][5]
            browser.AbrirBrowser(url)

            # logando no wordpress
            loginwordpress = info[i][3]
            senhawordpress = info[i][4]
            LogarWordpress(browser, loginwordpress, senhawordpress)

            # atualizando os plugins
            AtualizarPlugins(browser)

            print("\033[92m {}\033[00m".format("\nPlugins Atualizados com sucesso!"))

            print("\033[92m {}\033[00m".format("\nBackup concluído com sucesso!"))
            numsucessos += 1
        except:
            print("\033[91m {}\033[00m".format("\nHouve um erro e o backup não pode ser executado,passando para o próximo..."))

        browser.FecharBrowser()
        GerarRedicencias()



    print("\033[92m {}\033[00m".format("\n" + str(numsucessos) + " Backups concluídos com sucesso!"))
    print("\033[91m {}\033[00m".format("\n" + str(numfalhas) + " Backups não foram concluídos devido a falha"))


def LogarCpanel(login,senha,url,browser):
    browser.AbrirBrowser(url)
    idinputlogin = "user"
    idinputsenha = "pass"
    idbuttonsubmit = "login_submit"

    browser.InserirInfoElemento(idinputlogin,login)
    browser.InserirInfoElemento(idinputsenha,senha)
    browser.ClicarNoElemento(idbuttonsubmit)

def BaixarBD(browser,pastaraizcaminho):
    #para executar está função o navegador já deve estar logado na página inicial do cpanel
    idbuttonphpmyadmin = "item_php_my_admin"
    time.sleep(5)
    browser.ClicarNoElemento(idbuttonphpmyadmin)

    #indo para a pag do bd, que terá o index 1 por ser a segunda a ser aberta
    browser.TrocarDePagina(1)

    time.sleep(5)

    xpathlinkbd = '//*[@id="pma_navigation_tree_content"]/ul/li[1]/a'
    #garantindo que está pegando o banco certo, não o information schema
    if browser.GetConteudoElemento(xpathlinkbd) == "information_schema":
        xpathlinkbd = '//*[@id="pma_navigation_tree_content"]/ul/li[2]/a'

    time.sleep(3)
    browser.ClicarElementoPorXPath(xpathlinkbd)
    #pegando o nome do banco de dados
    nomearquivobanco = browser.GetConteudoElemento(xpathlinkbd) + ".sql"


    xpathbotaoexportar = '//*[@id="topmenu"]/li[5]/a'
    time.sleep(3)
    browser.ClicarElementoPorXPath(xpathbotaoexportar)

    idbotaoconfirmar = "buttonGo"
    time.sleep(3)
    browser.ClicarNoElemento(idbotaoconfirmar)

    caminhodownload = pastaraizcaminho + "\\" + nomearquivobanco

    EsperarArquivoBaixar(caminhodownload)

    return nomearquivobanco

def EsperarArquivoBaixar(caminho):
    while True:
        if not os.path.isfile(caminho):
            time.sleep(2)
        else:
            break

def MoverArquivo(local,destino):
    shutil.move(local,destino)


def EsvaziarLixeira(browser):

    idlixeira = 'action-viewtrash'
    time.sleep(3)
    browser.ClicarNoElemento(idlixeira)

    idesvaziarlixeira = 'action-emptytrash'
    time.sleep(3)
    browser.ClicarNoElemento(idesvaziarlixeira)

    xpathconfirmaresvaziamento = '//*[@id="emptytrash"]/div[3]/span/button[1]'
    time.sleep(3)
    browser.ClicarElementoPorXPath(xpathconfirmaresvaziamento)


def BaixarArquivosSite(browser,pastaraizcaminho):
    #setando as informações necessárias para a compressão
    xpathbotaopublichtml = "//span[text()='public_html']/.."
    time.sleep(3)
    browser.ClicarElementoPorXPath(xpathbotaopublichtml)

    idselectall = 'action-selectall'
    time.sleep(3)
    browser.ClicarNoElemento(idselectall)

    iddivarquivos = "yuievtautoid-0"
    time.sleep(3)
    browser.CliqueDireitoElemento(iddivarquivos)

    idcompress = 'yui-gen21'
    time.sleep(3)
    browser.ClicarNoElemento(idcompress)

    time.sleep(1)

    xpathcheckboxzip = '//*[@id="compress-multifile"]/div[1]/label/input'
    browser.ClicarElementoPorXPath(xpathcheckboxzip)

    idinputcaminhocompress = 'compressfilepath'
    caminho = '/public_html/backupsite.zip'
    browser.LimparInput(idinputcaminhocompress)
    browser.InserirInfoElemento(idinputcaminhocompress,caminho)

    xpathbotaoconfirmar = '//*[@id="compress"]/div[3]/span/button[1]'
    browser.ClicarElementoPorXPath(xpathbotaoconfirmar)

    #esperar a compressão ser completa
    idmodalzipconcluido = "resultspanel_h"
    browser.EsperarElementoSerClicavel(idmodalzipconcluido)

    xpathfecharmodal = '//*[@id="resultspanel"]/a'
    browser.ClicarElementoPorXPath(xpathfecharmodal)

    time.sleep(3)
    xpathbotaozip = "//span[text()='backupsite.zip']/../../.."
    browser.DuploCliqueElementoXPath(xpathbotaozip)

    #apagar o arquivo
    ApagarArquivoBackup(browser, xpathbotaozip)

    #esperar o arquivo carregar no pc
    caminhodownload = pastaraizcaminho + "\\" + "backupsite.zip"
    EsperarArquivoBaixar(caminhodownload)




def ApagarArquivoBackup(browser,xpath):
    browser.CliqueDireitoElementoXPath(xpath)

    time.sleep(1)

    iddelete = "yui-gen18"
    browser.ClicarNoElemento(iddelete)

    time.sleep(2)

    xpathdeletar = '//*[@id="trash"]/div[3]/span/button[1]'
    browser.ClicarElementoPorXPath(xpathdeletar)


def LogarWordpress(browser,login,senha):
    idlogin = 'user_login'
    browser.InserirInfoElemento(idlogin,login)

    idsenha = 'user_pass'
    browser.InserirInfoElemento(idsenha,senha)

    idsubmit = 'wp-submit'
    browser.ClicarNoElemento(idsubmit)

def AtualizarPlugins(browser):
    xpathbotaoatualizar = '//*[@id="menu-dashboard"]/ul/li[3]/a'
    browser.ClicarElementoPorXPath(xpathbotaoatualizar)

    time.sleep(5)

    idselectall = 'plugins-select-all'
    browser.ClicarNoElemento(idselectall)

    idupgradeplugins = 'upgrade-plugins'
    browser.ClicarNoElemento(idupgradeplugins)

    time.sleep(15)


InteracaoComOUsuario()

