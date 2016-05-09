# -*- coding: utf-8 -*-

@auth.requires_login()
def etapa_1():
    if not session.parcelada:
        session.parcelada = " "

    representante = ''   
    if session.representante:
        representante = db(db.representantes.id == session.representante ).select('nome')[0].nome

    # form cliente e representante
    form = SQLFORM.factory(
        Field('Cliente',default=session.cliente, requires = IS_NOT_EMPTY(error_message = "Digite o nome do cliente"
            ), widget = SQLFORM.widgets.autocomplete(
            request, db.clientes.nome, limitby=(0,5), min_length=1)),
        #     # Field('Cliente',default=session.cliente , requires = IS_IN_DB(db, Clientes.nome, error_message = 'Escolha um cliente'),
            # Field('Cliente', default=session.cliente, requires = IS_IN_DB(db, Clientes.nome, error_message = 'Escolha um representante') ),
            Field('Representante',default=representante , requires = IS_IN_DB(db, Representantes.nome, error_message = 'Escolha um representante'))
        )
    if form.process().accepted:
        session.cliente = form.vars.Cliente
        session.idCliente = db(db.clientes.nome == form.vars.Cliente).select('id')[0].id
        session.representante = db(db.representantes.nome == form.vars.Representante ).select('id')[0].id
        #cria codigo da venda  
        if not session.codigo_venda:
            from datetime import datetime
            now = datetime.now()
            session.codigo_venda =  now.strftime("%y%m%d""%S%M%H")
            pass    
        redirect(URL('etapa_2?menu=caixa')) 
    

    return dict(form=form)   


# ------------------ ETAPA 2 ---------------------
@auth.requires_login()
def etapa_2():
    grid = db(Itens.codigoVenda == session.codigo_venda).select() 
    # ---- sTotal
    sTotal = 0.0
    for iten in grid:
        sTotal += float(iten.valorTotal)  
    session.sTotal = sTotal
    # ---- fim sTotal
    return dict(grid=grid, sTotal=sTotal)

def produto():
    codigo = request.vars.codigo
    produto = request.vars.produto
    qtde = request.vars.qtde


    valorUn = (db(db.produtos.codigo_produto == codigo).select('preco_produto_lojinha'))[0].preco_produto_lojinha
    valorTotal = int(qtde)*round(float(valorUn),2)
    Itens.insert(codigoVenda=session.codigo_venda,codigoIten=codigo,produto=produto,quantidade=qtde,valorUnidade=valorUn,valorTotal=valorTotal)
    #redirect(URL('etapa_2?menu=caixa')) 
 
def delItem():
    index = request.vars.transitory
    # index = index.split(";")
    db(Itens.id == index).delete()
    # session.venda_sTotal = float(session.venda.sTotal) - float(index[1]) #subtração do valor dos itens

def buscaCodigo():
    cod = request.vars.transitory
    iten = db(db.produtos.codigo_produto == "%s"%cod).select('nome_produto') 
    # se o iten existir!
    if iten:
        ret =  "$('#no_table_qtde').attr('disabled',false).focus();$('#no_table_produto').val(%s);$('#no_table_codigo').css('color','#555').parent().removeClass('has-error')"% repr(iten[0].nome_produto)
    else:
        ret =  "$('#no_table_qtde').attr('disabled',true);$('#no_table_codigo').parent().addClass('has-error').children().focus().css('color','red');$('#no_table_produto').val('')"
        pass
    return ret

def buscaProduto():
    prod = request.vars.transitory
    iten = db(db.produtos.nome_produto == "%s"%prod).select('codigo_produto') 
    # se o iten existir!
    if iten:
        ret =  "$('#no_table_qtde').attr('disabled',false).focus();$('#no_table_codigo').val(%s);$('#no_table_produto').css('color','#555').parent().removeClass('has-error');$('input[type=submit]');"% repr(iten[0].codigo_produto)
    else:
        ret =  "$('#no_table_qtde').attr('disabled',true);$('#no_table_produto').parent().addClass('has-error').children().focus().css('color','red');$('#no_table_codigo').val('')"
        pass
    return ret
# ------------------ FIM DA ETAPA 2 ---------------------

# ----------------------- ETAPA 3 -----------------------
@auth.requires_login()
def etapa_3():
    return dict(sTotal = session.sTotal, sTotal_F = double_real(session.sTotal).real())
# ------------------ FIM DA ETAPA 3 ---------------------

# @auth.requires_login()
def clientes_retorno():
    pattern = '%' + request.vars.itens + '%' #primeira letra maiusculo
    selecionado = [row for row in db(db.clientes.nome.like(pattern)).select()] #select no db
    #se a session nao existir criar ela

    if not session.venda.codigo:
        from datetime import datetime
        now = datetime.now()
        # session.venda.codigo =  "%s%s%s%s%s%s"% (now.second,now.minute,now.hour,now.day,now.month,now.year)
        session.venda.codigo =  now.strftime("%y%m%d""%S%M%H")

    
        # response.flash = "Codigo da venda : %s"%session.vendaAtual_codigo  

    for s in selecionado:
        session.venda.nome = s.nome
        session.venda.celular = s.celular
        session.venda.email = s.email

    # userDiv = UL(
    #   LI(STRONG('Nome : '),SPAN(session.vendaAtual_nome,_id="nn"),_class="list-group-item"),
    #   LI(STRONG('Celular : '),SPAN(session.vendaAtual_celuar),_class="list-group-item"),
    #   LI(STRONG('E-mail : '),SPAN(session.vendaAtual_email),_class="list-group-item"),_class="list-group")

# @auth.requires_login()
def fecharVenda():
    index = request.vars.transitory
    index = index.split(";")
    # dados a gravar no db
    codigoVenda = session.codigo_venda
    idCliente = db(Clientes.nome == session.cliente ).select('id')[0].id
    
    # print '----------------------------- 1'   
    tipoVenda = index[0]
    valorVenda = index[1]
    valorDesconto = index[2]
    #parcelados = parcelado(index[5])
    # pegar o nome do representante e gravar o id no historico

    # print '-----------------------------2'
    representante = session.representante
    enviarEmail = 'S' 
    # Parcela, DataVencimento, Valor

    # Parcela, DataVencimento, Valor
    vendedor = session.auth.user.email #pegar usuario logado        
    itensVenda = crud.select(Itens, Itens.codigoVenda == '%s'%codigoVenda,['codigoIten','quantidade','produto','valorUnidade','valorTotal'])
    
    if valorDesconto == '':
        valorDesconto = '0.00'
        pass
    db.historicoVendas.insert(codigoVenda = codigoVenda,clienteEmail = idCliente,tipoVenda = tipoVenda,valorVenda = valorVenda,valorDesconto = valorDesconto,  vendedor = vendedor, representante = representante ) 
    viewDesc = ""
    if valorDesconto != "0.00":
        valorT = (float(valorVenda) + float(valorDesconto))
        viewDesc = "<h3><b>Total</b> : R$ %.2f - <b>Desconto</b> : <span>R$ %.2f</span></h3>"%(valorT, float(valorDesconto))

    if enviarEmail == 'N':
        enviar_email(codigoVenda)    

    temp_codigoVenda = session.codigo_venda
    session.__delitem__('codigo_venda')
    session.__delitem__('cliente')
    session.__delitem__('representante') 
    pass
#--------------------------------    




def reenviar_email():
    cod = request.vars.transitory
    enviar_email(cod)


def enviar_email(codigo):
    historico = db(db.historicoVendas.codigoVenda == '%s'%codigo).select('tipoVenda','valorVenda','valorDesconto','dataVenda','clienteEmail')
    desconto = historico[0].valorDesconto
    total = historico[0].valorVenda
    itens = crud.select(Itens, Itens.codigoVenda == '%s'%codigo,['codigoIten','quantidade','produto','valorUnidade','valorTotal'])
    
    subTotal = (float(total)+float(desconto))
    tipoVenda = historico[0].tipoVenda 
    # email = historico[0].clienteEmail
    email = 'jose.vicente.de.sousa@gmail.com'
    emailSimples = "|---------------- RECIBO DE COMPRA ----------------|\n" \
    " ### ESSE DISPOSITIVO NAO E POSSIVEL VISUALIZAR OS DADOS ###\n" \
    " ### Por gentileza visualize no seu email."

    if desconto != 0.0:
        mostrarDesconto = "[ Total =  R$ %.2f ] - [ Desconto = R$ %.2f ]"%(float(subTotal),float(desconto))
    else:
        mostrarDesconto = '' 
    pass   

    #------------ edit HTML email
    emailHTML = '<div style="padding: 20px 29px;border: 1px solid #D2D2D2;border-radius: 11px;"><div class="adM"><br></div>'\
    '<div style="text-align:center;border-bottom: 1px solid #DADADA;padding-bottom: 17px !important;">'\
        '<img src="https://dl.dropboxusercontent.com/u/11469395/ArtesanalBaby/logo/logo-lojinha.png" width="95pt" class="CToWUd">'\
    '</div>'\
    '<p></p>'\
    '<h2 style="color: #F78100;text-align: center;">Romaneio ArtesanalBaby ( codigo : %s )</h2>'\
    '<p></p>'\
    '<p>Recibo emitido em: %s</p>'\
        '<div>'\
            '%s'\
            '%s'\
        '</div>'\
        '<h4><b>SUB-TOTAL</b> = R$ %.2f  |  <b>Tipo pag</b> : %s </h4>'\
            '<p style="border-bottom: 1px solid #DADADA;padding-bottom: 17px !important;">Nos visite: <a href="http://www.artesanalbaby.com.br" target="_blank">www.artesanalbaby.com.br</a></p>'\
            '<p></p>'\
            '<h3 style="color: #B1B1B1;text-align: center;">Muito Obrigado pela compra! Volte sempre.</h3>'\
            '<div class="yj6qo"></div>'\
            '<div class="adL">'\
                '<p></p>'\
               ' <br>'\
            '</div>'\
        '</div></div>'%(codigo,(historico[0].dataVenda).strftime("%d/%m/%Y as %H:%M:%S"),itens,mostrarDesconto,float(total),tipoVenda)    
    #------------ fim edit HTML email 

    if mail:
        if mail.send(to=["%s"%email],
            subject='Romaneio ArtesanalBaby Cod:%s'%codigo,
            message=[emailSimples, emailHTML]
        ):
            response.flash = 'Romaneio enviado a sucesso!'
        else:
            response.flash = 'Problema ao enviars o email!'
    else:
        response.flash = 'Unable to send the email : email parameters not defined' 
     



#@auth.requires_membership('admin') 
@auth.requires_login()
def historico():
    # data atual
    # from datetime import datetime
    hoje = datetime.now()
    mesAno = hoje.strftime('%m/%Y')
    hoje = hoje.strftime('%Y-%m')#pega apenas o ano e mes atual

    # formulario de busca entre datas
    form = SQLFORM.factory(
        Field("date_initial", requires=IS_NOT_EMPTY(error_message="Campo vazio")),
        Field("date_final", requires=IS_NOT_EMPTY(error_message="Campo vazio")),
        formstyle='divs',
        submit_button="Search",
        )

    # formulario aceito
    if form.process().accepted:
        # pegando as datas escolhidas 
        date_initial = form.vars.date_initial 
        date_initial = date_initial.split('/')
        date_initial = "%s-%s-%s"%(date_initial[2],date_initial[0],date_initial[1])
        date_final = form.vars.date_final 
        date_final = date_final.split('/')
        data_final = "%s-%s-%s"%(date_final[2],date_final[0],date_final[1])

        # fazendo consulta entre as datas ecolhidas
        formListar = db((db.historicoVendas.dataVenda >= date_initial) & (db.historicoVendas.dataVenda <= data_final)).select()      
    else:
        #buscar registro do mes e ano atual
        formListar = db(db.historicoVendas.dataVenda.like(hoje+'%')).select()#busca pelo ano e mes atual    
    
    return dict(formListar=formListar, mesAtual=mesAno, form=form)

 

def historico_print():
    # codigo da venda
    cod_venda = request.vars.cod 
    # historico da venda ( venda referente ao cod_venda )
    historico_venda = db(Historico.codigoVenda == "%s"%cod_venda).select() 
    # ok ate aqui
    # itens da venda 
    itens_venda =  db(Itens.codigoVenda == "%s"%cod_venda).select('codigoIten','quantidade','produto','valorUnidade','valorTotal')


    # ver se a venda foi parcelada
    if historico_venda[0].tipoVenda == 'cheque' or historico_venda[0].tipoVenda == 'boleto':
        # enviar a tabela com as parcelas para a view
        itens_parcelas = db(Parcelando.codigo_venda == "%s"%cod_venda).select('parcela','data_vencimento','valor')
        
    else:
        itens_parcelas = ""
        pass    
    return dict(historico_venda=historico_venda,itens_venda=itens_venda, itens_parcelas=itens_parcelas) 

def cancelarVenda():  
    # limpar itens do db
    db(Itens.codigoVenda == session.codigo_venda).delete()
    # session.venda
    session.__delitem__('codigo_venda')
    session.__delitem__('cliente')
    session.__delitem__('representante')
    #redirect(URL('etapa_1?menu=caixa')) 
    #session.flash = 'Pedido Cancelado!'

def excluirVendaRegistrada():
    codigo = request.vars.transitory
    db(db.historicoVendas.codigoVenda == codigo).update(deletado=True)
    db(db.pendentes.codigo == codigo).update(status='Finalizado')
    db(db.parcelados.codigo == codigo).update(excluido=True)
    return ''

@auth.requires_login()
def aguardaLancamento():
    query = (Historico.tipoVenda=='cheque') & (Historico.aguardandoLancamento==True)
    table = db(query).select()
    qt = len(table)
    return locals()

@auth.requires_login()
def compensado():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'compensado') 
    table = db(query).select()
    qt = len(table)
    return locals()

@auth.requires_login()
def repassado():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'repassado') 
    table = db(query).select()
    qt = len(table)
    return locals()

@auth.requires_login()
def devolvidoAoCliente():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'devolvido ao cliente') 
    table = db(query).select()
    qt = len(table)
    return locals()

@auth.requires_login()
def devolvido1():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'devolvido 1-vez') 
    table = db(query).select()
    qt = len(table)
    return locals()

@auth.requires_login()
def devolvido2():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'devolvido 2-vez') 
    table = db(query).select()
    qt = len(table)
    return locals()

#update
def atualizarParcelados():
    index = request.vars.transitory
    index = index.split(';')
    # from datetime import datetime
    data = datetime.now()
    # mesAno = hoje.strftime('%m/%Y')
    # hoje = hoje.strftime('%Y-%m')#pega apenas o ano e mes atual
    if index[3] == 'compensado':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 00:00:00"),receptor=index[5],data_up=data)
    elif index[3] == 'repassado':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 00:00:00"),receptor=index[5],data_up=data)
    elif index[3] == 'devolvido ao cliente':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 00:00:00"),receptor=index[5],data_up=data)
    elif index[3] == 'devolvido 1-vez':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 00:00:00"),receptor=index[5],data_up=data)
    else:
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 00:00:00"),receptor=index[5],data_up=data)
        pass
    # db(db.parcelados.id == index[0]).update(numero_cheque=index[1],cliente=index[2],statusLancament=index[3],dataVencimento=(index[4]+" 00:00:00"),repasse_nome=index[5])
   
def gridParcelas():
    index = request.vars.transitory
    index = index.split(';')

    # dados recebidos
    qtde_parc = int(index[0]) # quantidade de parcelas
    valor = "%.2f"%(float(index[1])/qtde_parc)
    valor = double_real(valor).real() # valor total dividido pela quantidade de parcelas
    cliente = index[2]
    dataAtual = datetime.now()
    # confecção da grid pra a view
    table = TABLE(THEAD(TR(TH('Parc',_class="grid_parcela"),TH('Nº cheque',_class="grid_cheque"),TH('Nome no cheque',_class='grid_dono'),TH('Data parcela',_class='grid_data'),TH('Valor parcela'))),_class="table table-striped table-condensed", _id="tab_calculo_parcelas")
    tbody = TBODY()
    for i in range(qtde_parc):
        dataAtual = (dataAtual + timedelta(30))
        dataParc =  dataAtual.strftime('%d-%m-%Y')
        # monta a parcela
        tbody.append(TR(TD(i+1,_class="grid_parcela"),TD(INPUT(_type='text',_value='00000000',_class='form-control inputGrid'),_class="grid_cheque"),TD(INPUT(_type='text',_value=cliente,_class='form-control inputGrid'),_class='grid_dono'),TD(INPUT(_type='text',_value=dataParc,_class='form-control inputGrid'),_class="grid_data"),TD(INPUT(_type='text',_value=valor,_class='form-control inputGrid real'))))    
    table.append(tbody)    
    # return table   
    return "%s%s"%(table,'<script>window.onload = carregar_masck();</script>')   

def gravarParcelas():
    index = request.vars.transitory
    index = index.split('|')
    codigo = index[0]
    parcelas = index[1]
    dataAtual = datetime.now()
    #gravar as parcelas
    table = parcelas.replace(',','.').split('@')
    n_parcela = 1
    # print table 
    for row in table:
        cells = row.split(';')
        n_cheque = cells[0]
        nome = cells[1].strip() #tira espaços vazios no inicio e fim da palavra
        dt = cells[2].split('-')
        dt = "%s-%s-%s 00:00:00"%(dt[2],dt[1],dt[0])
        valor = float(cells[3])
        print "[%s] %s %s %s %s %s"%(codigo,n_parcela,n_cheque,nome,dt,valor)
        Parcelando.insert(parcela=n_parcela,codigo_venda=codigo,tipo='cheque', status='compensado',data_vencimento=dt,proprietario=nome,numero_cheque=n_cheque,valor=valor,data_up=dataAtual)
        # Parcelados.insert(numeroChequ=n_cheque,cliente=nome,dataVencimento=dt,valor=valor,representante=6,statusLancament='compensado',data_compensado=dataAtual)
        # print "Parcelados.insert(codigo='%s',tipoVenda='cheque',numeroChequ='%s',cliente='%s',dataVencimento='%s',valor='%s',representante='%s',statusLancament='compensado',data_compensado='%s')"%(codigo,n_cheque,nome,dt,valor,'6',dataAtual)
        n_parcela += 1
    
    # table = ''
    # alterar o historico de vendas
    # print codigo
    db(db.historicoVendas.codigoVenda=="%s"%codigo).update(aguardandoLancamento = False)
    
    pass    

def parcelado():
    index = request.vars.transitory
    index = index.split('!')
    tabela = index[0].split('@')
    tipoVenda = index[1];
  

    for linha in tabela:
        linha = linha.split(',')
        parcela = linha[0]
        dataParcela = "%s 00:01:01"%linha[1]
        valorParcela = linha[2]
        codigoVenda = session.codigo_venda     
        proprietario = linha[3]
        dataAtual = datetime.now()
        
        #gravar no db parcelados
        # Parcelados.insert(codigo=codigoVenda, tipoVenda=tipoVenda, cliente=linha[3], parcela=parcela, dataVencimento=dataParcela, valor=valorParcela)
        Parcelando.insert(parcela=parcela,codigo_venda=codigoVenda,tipo='boleto', status='pendente',data_vencimento=dataParcela,proprietario=linha[3],valor=valorParcela,data_up=dataAtual)
        pass    