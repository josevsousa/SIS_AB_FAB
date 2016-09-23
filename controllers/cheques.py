@auth.requires_login()
def aguardandoLancamento():
    query = (Historico.tipoVenda=='cheque') & (Historico.aguardandoLancamento==True) & (Historico.deletado==False)
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
    table = db(query).select(orderby='data_vencimento')
    qt = len(table)
    return locals()

@auth.requires_login()
def devolvido1():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'devolvido 1-vez') 
    table = db(query).select(orderby='data_vencimento')
    qt = len(table)
    return locals()

@auth.requires_login()
def devolvido2():
    query = (Parcelando.tipo == 'cheque') & (Parcelando.status == 'devolvido 2-vez') 
    table = db(query).select(orderby='data_vencimento')
    qt = len(table)
    return locals()


#update
def atualizarParcelados():
    index = request.vars.transitory
    index = index.split(';')
    print index
    if index[3] == 'compensado':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 01:01:01"),receptor=index[5])
    elif index[3] == 'repassado':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 01:01:01"),receptor=index[5])
    elif index[3] == 'devolvido ao cliente':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 01:01:01"),receptor=index[5])
    elif index[3] == 'devolvido 1-vez':
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 01:01:01"),receptor=index[5])
    else:
        db(db.parcelando.id == index[0]).update(numero_cheque=index[1],proprietario=index[2],status=index[3],data_vencimento=(index[4]+" 01:01:01"),receptor=index[5])
        pass
    # db(db.parcelados.id == index[0]).update(numero_cheque=index[1],cliente=index[2],statusLancament=index[3],dataVencimento=(index[4]+" 01:01:01"),repasse_nome=index[5])
   
def gridParcelas():
    index = request.vars.transitory
    index = index.split(';')
    print '========= ',index[0]
    # dados recebidos
    qtde_parc = int(index[0]) # quantidade de parcelas
    valor = "%.2f"%(float(index[1])/qtde_parc)
    valor = double_real(valor).real() # valor total dividido pela quantidade de parcelas
    cliente = index[2]
    dataAtual = datetime.now()
    # confecção da grid pra a view
    table = TABLE(THEAD(TR(TH('Parc',_class="grid_parcela"),TH('Nº cheque',_class="grid_cheque"),TH('Banco',_class="grid_banco"),TH('Nome no cheque',_class='grid_dono'),TH('Data parcela',_class='grid_data'),TH('Valor parcela'))),_class="table table-condensed", _id="tab_calculo_parcelas")
    tbody = TBODY()
    for i in range(qtde_parc):
        dataAtual = (dataAtual + timedelta(30))
        dataParc =  dataAtual.strftime('%Y-%m-%d')
        # monta a parcela
        tbody.append(TR(TD(i+1,_class="grid_parcela"),TD(INPUT(_type='text',_value='00000000',_class='form-control inputGrid'),_class="grid_cheque"),TD(SELECT(OPTION('Nossa Caixa',_value='nossa_caixa'),OPTION('Santander',_value='santander'),OPTION('Caixa Econômica',_value='caixa_economica'),OPTION('banco do Brasil',_value='banco_do_Brasil'),OPTION('HSBC',_value='HSBC'),OPTION('Itau',_value='Itau'),OPTION('bradesco',_value='bradesco'),_class="form-control", _id="banco"),_class='grid_banco'),TD(INPUT(_type='text',_value=cliente,_class='form-control inputGrid'),_class='grid_dono'),TD(INPUT(_type='date',_value=dataParc,_class='form-control inputGrid')),TD(INPUT(_type='text',_value=valor,_class='form-control inputGrid real'))))    
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
	for row in table:
	    cells = row.split(';')
	    n_cheque = cells[0]
	    nome = cells[1].strip() #tira espaços vazios no inicio e fim da palavra
	    dt = cells[2].split('-')
	    dt = "%s-%s-%s 01:01:01"%(dt[0],dt[1],dt[2])
	    valor = float(cells[3])
	    banco = cells[4]
	    # print "[%s] %s %s %s %s %s"%(codigo,n_parcela,n_cheque,nome,dt,valor)
	    
	    inserido = Parcelando.insert(parcela=n_parcela,codigo_venda=codigo,tipo='cheque', status='compensado',data_vencimento=dt,proprietario=nome,numero_cheque=n_cheque,valor=valor,banco=banco)


	    # Parcelados.insert(numeroChequ=n_cheque,cliente=nome,dataVencimento=dt,valor=valor,representante=6,statusLancament='compensado',data_compensado=dataAtual)
	    # print "Parcelados.insert(codigo='%s',tipoVenda='cheque',numeroChequ='%s',cliente='%s',dataVencimento='%s',valor='%s',representante='%s',statusLancament='compensado',data_compensado='%s')"%(codigo,n_cheque,nome,dt,valor,'6',dataAtual)
	    n_parcela += 1

	# table = ''
	# alterar o historico de vendas
	# print codigo

	db(db.historicoVendas.codigoVenda=="%s"%codigo).update(aguardandoLancamento = False)

pass    