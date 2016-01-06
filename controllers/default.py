# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    from datetime import datetime, timedelta
    meses = 1
    dias_por_mes = 30
    hoje = datetime.now()
    dt_futura = hoje + timedelta(dias_por_mes*meses)

    # dados para o grafico
    ano = int(hoje.strftime('%Y'))
    ano = ano - 3
    dadosgraf = []
    for i in range(1,4):
        #burcar dados do grafico
        dadosgraf.append([ano+i,[49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]])
    
    # mandar as datas dos debitos pendentes


    # response.flash = T("Seja bem vindo!  %s !"%(hoje.strftime('%d/%m/%Y')))
    return locals()

def cheques_boletos():
    from datetime import datetime, timedelta
    meses = 1
    dias_por_mes = 30
    hoje = datetime.now()
    dt_futura = hoje + timedelta(dias_por_mes*meses)

    pattern = '%' + request.vars.transitory + '%' #primeira letra maiusculo
    query = db(db.parcelados.id>0 and db.parcelados.statusPagamento != True and db.parcelados.dataVencimento.like(pattern) ).select()
    
    itens = ''
    for i in query:
        itens = itens+"<tr><td>%s</td><td>%s</td><td>%s</td><td>R$ %s</td><td>%s</td><td>%s</td><tr>"%(i.tipoVenda, (i.dataVencimento).strftime('<b style="color:red">%d</b>/%m/%Y'), i.parcela, i.valor, i.cliente, i.representante)
        pass
    table = XML("%s"%itens)  
    # table = query   
                                  
    return table

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


