@auth.requires_membership('admin')
def cadastrarProdutos():
	menu = 'produtos'




	#max = db.produtos.id.max()
	#max_id = db().select(max).first()[max]
	#ultimo_evento = db.eventos[max_id]
		

	return dict(formCadastro=crud.create(db.produtos))

@auth.requires_login()
def listarProdutos():
	produtos = db(db.produtos.id>0).select()
	#return dict(livros=livros)	

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('produtos','deletar',args=[self.produtos.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('produtos','select',args=[self.produtos.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('produtos','update',args=[self.produtos.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('produtos','select',args=[self.produtos.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	produtos.setvirtualfields(campos_virtual = Virtual())	

    #config produtos
	configProdutos = db(Produtos_config.id>0).select()
	ultima_porcentage = configProdutos.last().aumento
	ultima_alteracao = configProdutos.last().data_criacao.strftime("%d/%m/%Y as %H:%M:%S")

	return dict(formListar=produtos, ultima_porcentage=ultima_porcentage, ultima_alteracao=ultima_alteracao)

def almentarValorProduto():
	valorAumento = request.vars.valorAumento
	valorAumento = int(valorAumento)
	produtos = db(Produtos.id>0).select('id','preco_produto_lojinha')
	#é pra diminuir ou almentar o valor?
	if valorAumento > 0:
		for produto in produtos:
			db(Produtos.id == produto.id).update(preco_produto_lojinha_backup=produto.preco_produto_lojinha)
			# montar o novo valor 
			valor = float(produto.preco_produto_lojinha)
			aumento = float((valor*valorAumento)/100)
			db(Produtos.id == produto.id).update(preco_produto_lojinha=(valor+aumento))
			pass
		db.produtos_config.insert(aumento=valorAumento)
	else: #é 0	
		for produto in produtos:
			db(Produtos.id == produto.id).update(preco_produto_lojinha_backup=produto.preco_produto_lojinha)
			# montar o novo valor 
			valor = float(produto.preco_produto_lojinha)
			aumento = float((valor*valorAumento)/100)
			db(Produtos.id == produto.id).update(preco_produto_lojinha=(valor+aumento))		
			pass
		db.produtos_config.insert(aumento=valorAumento)	
		pass

def resetarValorProduto():
    produtos = db(Produtos.id>0).select()
    for produto in produtos:
        print produto.preco_produto_lojinha
        db(Produtos.id == produto.id).update(preco_produto_lojinha=produto.preco_produto_lojinha_backup)
        pass
    produtosConfig = db(db.produtos_config.id>0).select()
    produtosConfigDel = produtosConfig.last().id
    crud.delete(db.produtos_config, produtosConfigDel)
    

# ============== select insert update ==============
# def selectCrud():
# 	todos = crud.select(db.produtos, db.produtos.id == request.args(0),['codigo_produto','nome_produto','preco_produto_lojinha','dataGravado'])
# 	return dict(form=todos)

#select
def select():
	table = db(db.produtos.id==request.args[0]).select()
	return dict(table=table)
#insert
@auth.requires_membership('admin')
def inserir():
	return dict()
	#return dict(form=crud.create(db.produtos))
#update
@auth.requires_membership('admin')
def update():
	return dict(form=crud.update(db.produtos,request.args(0)))
#delete
def deletar():
	print request.vars.cod
	db(db.produtos.codigo_produto == request.vars.cod).delete()
	return ''

# ===================================================

@auth.requires_login()
def cadastrar():
	form = crud.create(db.produtos)
	return dict(form=form)    


@auth.requires_login()
def todos():
    grid = db(db.produtos.id>0).select()
    # formrepresentantesAdd = crud.update(db.representantes,request.args(0))
    formCreate = crud.create(db.produtos)

    return locals()

@auth.requires_login()
def editar():
    codigo = request.vars.codigo
    form = crud.update(db.produtos, codigo)
    
    
    # pegar a foto do cliente

    # form = crud.update(db.clientes, cod)
    # crud.settings.delete_next = URL('caixa')
    # form = 'jose'
    # return "%s %s"%(form,"<script> aplicar_estilo_form();</script>")
    return dict(form=form)

@auth.requires_login()
def buscar_produto():
	#codigo do produto recebido
	cod = request.vars.transitory
	#cadastro do produto recebido
	produto = db(db.produtos.id == cod).select()


	#busca avatar do produto
	img = URL('default','download',args=produto[0].foto_produto)
	print img
	if img == "/SIS_AB_FAB/default/download":
		img = URL('static','assets/img/faces/noFotoo.png')
	else:
		img = URL('default','download',args=produto[0].foto_produto)
		pass


	cracha = DIV(
		DIV(
			IMG(_src=img,_class="avatar border-white"),
			H4('%s'%produto[0].nome_produto,BR(),SPAN('%s'%produto[0].codigo_produto,_class='cracha'),_class='title'),
			_class="author"),
			DIV(
				FORM(
					DIV(
						DIV(
							DIV(
								LABEL('Valor'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%double_real(produto[0].preco_produto_lojinha).real()),
								_class="form-group"),
							_class="col-md-6"),
						DIV(
							DIV(
								LABEL('Tamanho'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%produto[0].tamanho),
								_class="form-group"),
							_class="col-md-6"),
						_class="row"),
					),
				_class="content"),
			HR(),
			DIV(
				DIV(
					A('editar',_href="editar?codigo=%s"%cod, _class="btn btn-default btn-wd"),
					_id="edicao",
					_class="col-md-12"),
				_class="row text-center"),
		_class="content")
	return cracha	