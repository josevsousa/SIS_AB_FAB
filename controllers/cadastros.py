def equipe():
	return locals()

def clientes():
	grid = db(db.clientes.id>0).select('id','nome','foto_cliente')

	# form = crud.update(db.clientes,request.args(0))

	return locals()
