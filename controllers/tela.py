def table():
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

