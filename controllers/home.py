@auth.requires_login()
def index():
    hoje = datetime.now()
    mesAno = hoje.strftime('%m/%Y')
    hoje = hoje.strftime('%Y-%m')#pega apenas o ano e mes atual

    # se receber datas de inicio e fim
    if request.vars.inicial:
        formListar = db((db.historicoVendas.dataVenda >= request.vars.inicial) & (db.historicoVendas.dataVenda <= request.vars.final)).select()      
    else: 
        formListar = db(db.historicoVendas.dataVenda.like(hoje+'%')).select()#busca pelo ano e mes atual   

    return dict(formListar=formListar, mesAtual=mesAno)
