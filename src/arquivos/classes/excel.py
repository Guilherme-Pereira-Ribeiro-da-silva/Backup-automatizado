import xlrd

class excel:
    def __init__(self,caminho_excel):
        self.excel = xlrd.open_workbook(caminho_excel)
        self.colunas = self.excel.sheet_by_index(0)
        self.numlinhas = self.colunas.nrows


    def GetInfoSites(self):
        #No excel, as seguintes colunas representam
        #0 - url,2 - usuário cpanel, 3 - senha cpanel,6 - usuário wordpress,
        # 7 - senha wordpress, 8 - sufixo url wordpress
        #As infoormações começam na linha 3(começando do 0)
        colunas = [0, 2, 3, 6, 7, 8]
        numlinhas = self.numlinhas - 6
        info = self.criarMatrix(numlinhas,len(colunas))
        linha_inicial = 6;

        for i in range(0,len(colunas)):
            linha_atual = linha_inicial
            celula_esta_vazia = False
            while celula_esta_vazia == False and linha_atual < self.numlinhas:
                valor = self.colunas.cell_value(linha_atual,colunas[i])
                celula_esta_vazia = True if len(valor) == 0 else celula_esta_vazia
                #as informações que serão necessárias começam apenas na linha 7
                info[linha_atual - 6][i] = valor
                linha_atual+=1

        return info

    def criarMatrix(self,len,height):
        matrix = [0] * len
        for i in range (len):
            matrix[i] = [0] * height
        return matrix


