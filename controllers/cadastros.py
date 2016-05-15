def equipe():
	return locals()

@auth.requires_login()
def clientes():
    grid = db(db.clientes.id>0).select('id','nome','foto_cliente')
    # formClientesAdd = crud.update(db.clientes,request.args(0))
    formCreate = crud.create(db.clientes)

    avatar = ''


    return locals()

@auth.requires_login()
def cliente_busca():
    cod = request.vars.transitory
    # pegar a foto do cliente

    form = crud.update(db.clientes, cod)
    crud.settings.delete_next = URL('caixa')

    return "%s %s"%(form,"<script> aplicar_estilo_form();</script>")

