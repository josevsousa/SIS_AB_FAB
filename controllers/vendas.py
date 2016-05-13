@auth.requires_login()
def historico():
    hoje = datetime.now()
    mesAno = hoje.strftime('%m/%Y')
    hoje = hoje.strftime('%Y-%m')#pega apenas o ano e mes atual

    # se receber datas de inicio e fim
    if request.vars.inicial:
        formListar = db((db.historicoVendas.dataVenda >= request.vars.inicial) & (db.historicoVendas.dataVenda <= request.vars.final)).select()      
    else: 
        formListar = db(db.historicoVendas.dataVenda.like(hoje+'%')).select()#busca pelo ano e mes atual   

    return dict(formListar=formListar, mesAtual=mesAno)

def excluirVendaRegistrada():
    codigo = request.vars.transitory
    print codigo
    db(db.historicoVendas.codigoVenda == codigo).update(deletado=True)
    db(db.pendentes.codigo == codigo).update(status='Finalizado')
    db(db.parcelados.codigo == codigo).update(excluido=True)
    return ''
    


def imprimir():
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
