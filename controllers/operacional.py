
# -*- conding: utf-8 -*-
@auth.requires_login()
def separar():
	from datetime import datetime
	pedidos = db(db.historicoVendas.id>0 and db.historicoVendas.status_venda!='Finalizada').select()
	return dict(pedidos=pedidos)


def pedido():
	cod = request.vars.cod
	data = request.vars.dataSolicitacao
	grid = db(Itens.codigoVenda == cod).select()
	head = H3("COD: [ %s ]  aberto em %s"%(cod, data))


	#pegar lista do historicoVendas.itensVendaPendente e jogar na tela 
	return dict(head=head,grid=grid,cod=cod)