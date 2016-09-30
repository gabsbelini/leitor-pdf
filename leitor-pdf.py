# -*- coding: utf-8 -*-


from tkinter import *
from collections import Counter
import PyPDF2
import operator
import json
from nltk.corpus import stopwords



'''-----Funçao principal do programa, engloba todas as outras funcoes de abertura de arquivo, fechamento de arquivo, leitura
 do pdf, e extração das informações de metadados----'''

def principal(arq1, arq2, pdf):
    cachedStopWords = stopwords.words("english") # armazena as stopwords da língua inglesa

    def abreArtigo(arq1): # criação dos arquivos com codificação utf-8
        artigo = open(arq1+'.txt', 'w+', encoding='utf-8')
        return artigo

    def abreBibliografia(arq2):
        bibliografia = open(arq2+'.txt', 'w', encoding='utf-8')
        return bibliografia

    def abreCabecalho():
        cabecalho = open('cabecalho.txt', 'w', encoding='utf-8')
        return cabecalho

    def abrePDF(pdf):
        pdfFileObj = open(pdf, 'rb')  # abre o arquivo pdf para leitura em modo binário
        return pdfFileObj

    def criapdfReader(pdfFileObj):
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # cria objeto leitura
        return pdfReader

    def calculaNumpages(pdfReader): # printa o número de páginas do arquivo
        numpages = pdfReader.numPages
        print('numpages: ', numpages)
        numpages -= 1
        return numpages
    def carregaLista_escreveArtigo(pdfReader, artigo, numpages):
        listatotal = []
        iterador = 0
        while iterador <= numpages:
            if (iterador >= 0):
                pagina = pdfReader.getPage(iterador)
                pagetext = (pagina.extractText())
                artigo.write(pagetext)
                artigo.write("\n\r") # ret
                provisoria = pagetext.split()
                listatotal = listatotal + provisoria
            iterador += 1
        return listatotal
    def procuraObjetivo(listatotal):
        x = open('objetivo.txt', 'w', encoding='utf-8')
        for p in listatotal:
            if ('objective') in p:
                indiceo = listatotal.index(p)
                for k in listatotal[indiceo:]:
                    if ('\n') in k or ('\r') in k or ('\r\n') in k or ('.') in k:
                        indiceofinal = listatotal.index(k)
                        x.write(' '.join(listatotal[(indiceo-10):(indiceofinal+10)]))
                        return None
    def calcula_indice_bib(listatotal):
        indice_bib = 0
        for x in listatotal:
            if ('References') in x:
                indice_bib = listatotal.index(x)
                print('indice bibliografia: ', indice_bib)
        return indice_bib

    def procuraTitulo(listatotal):
        for x in listatotal:
            if 'Titulo' in x or 'Title' in x:
                indice_tit = listatotal.index(x)
                return indice_tit
    def recebeIndiceTitFinal(listatotal, indice_tit):
        for x in listatotal[indice_tit:]:
            if 'Abstract' in x or'Resumo' in x or 'abstract' in x:
                indice_tit_final = listatotal.index(x)
                print(indice_tit_final,'indice final')
                return indice_tit_final
    def escreveTit(listatotal, indice_tit, indice_tit_final, cabecalho):
        for x in listatotal[indice_tit:indice_tit_final]:
            cabecalho.write(x)
            cabecalho.write(' ')
        cabecalho.close()

    def escreve_arquivo_bib(listatotal, indice_bib, bibliografia):
        for x in listatotal[indice_bib:]:
            bibliografia.write(x)
            bibliografia.write(' ')

    def fecha_txts(artigo, bibliografia, cabecalho):
        bibliografia.close()
        artigo.close()
        cabecalho.close()
    artigo = abreArtigo(arq1)
    bibliografia = abreBibliografia(arq2)
    cabecalho = abreCabecalho()
    pdfFileObj = abrePDF(pdf)
    pdfReader = criapdfReader(pdfFileObj)
    numpages = calculaNumpages(pdfReader)
    listatotal = carregaLista_escreveArtigo(pdfReader, artigo, numpages)
    indice_tit = procuraTitulo(listatotal)
    procuraObjetivo(listatotal)
    indice_tit_final = recebeIndiceTitFinal(listatotal, indice_tit)
    escreveTit(listatotal, indice_tit, indice_tit_final, cabecalho)

    print('indice titulo: ', indice_tit)

    indice_bib = calcula_indice_bib(listatotal)
    #print(listatotal)
    escreve_arquivo_bib(listatotal, indice_bib, bibliografia)
    fecha_txts(artigo, bibliografia, cabecalho)

    lower_words = [word.lower() for word in listatotal[:indice_bib]]  # deixa as palavras em minusculo
    stop_free_listatotal = ([word for word in lower_words if word not in cachedStopWords])  # retira stopwords
    word_counts = Counter(stop_free_listatotal)  # atribui valor de quantas vezes uma palavra aparece no texto
    newword_counts = dict(sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)[:10])  # monta dict com 10 maxs x,y
    print(newword_counts)
    maximos10 = []
    for item in newword_counts.values():  # apenas os maxs values do dict
        maximos10.append(item)
    maximos10.sort(reverse=True)
    maximos10_palavras = []
    for key in newword_counts:
        maximos10_palavras.append(key)
    maxx = max(word_counts.values())  # maximo valor do word_counts atribuido a maxx
    keys = [l for l, j in word_counts.items() if j == maxx]  # cria lista com palavras mais usadas, condicao aqui eh ser A mais usada
    def escreveinfo(newword_counts, lower_words, stop_free_listatotal, keys, maxx):
        info = open('info.txt', 'w')
        info.write('Palavras mais usadas seguidas do numero de vezes que cada uma foi usada:\n')
        json.dump(newword_counts, info)
        info.write('\nPalavra mais usada no texto: '+ keys[0]+' usada %d vezes'% maxx)
        info.write('\nQuantidade de palavras no texto com \'stop words\': '+ str(len(lower_words)))
        info.write('\nQuantidade de palavras no texto sem \'stop words\': '+ str(len(stop_free_listatotal)))
    escreveinfo(newword_counts, lower_words, stop_free_listatotal, keys, maxx)

root = Tk()


def abrePDF(event):
    arq1 = entry2.get()
    arq2 = entry3.get()
    pdf = (entry1.get())

    principal(arq1, arq2, pdf)


botao = Label(root, text='OK', bg='green', fg='white')
botao.grid(row=3, column=1)
botao.bind('<Button-1>', abrePDF)
frame = Frame(root, width=400, height=400)
label1 = Label(root, text='Nome do PDF')
label3 = Label(root, text='arquivo de bibliografia')
label2 = Label(root, text='arquivo texto')
entry1 = Entry(root)
entry2 = Entry(root)
entry3 = Entry(root)
label1.grid(row=0, sticky=E)
entry1.grid(row=0, column=1)
label2.grid(row=1, column=0)
entry2.grid(row=1, column=1)
label3.grid(row=2, column=0)
entry3.grid(row=2, column=1)

root.mainloop()