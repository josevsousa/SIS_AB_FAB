@auth.requires_membership('admin')
def cadastrarRepresentantes():
	menu = 'representantes'
	return dict(formCadastro=crud.create(db.representantes))

# @auth.requires_login()
def listarRepresentantes():
	representantes = db(db.representantes.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('representantes','deletar',args=[self.representantes.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('representantes','select',args=[self.representantes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('representantes','update',args=[self.representantes.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('representantes','select',args=[self.representantes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	representantes.setvirtualfields(campos_virtual = Virtual())		

	return dict(formListar=representantes)

# ============== select insert update ==============
# def selectCrud():
# 	todos = crud.select(db.produtos, db.produtos.id == request.args(0),['codigo_produto','nome_produto','preco_produto_lojinha','dataGravado'])
# 	return dict(form=todos)


@auth.requires_login()
def todos():
    grid = db(db.representantes.id>0).select('id','nome','foto_representante','matricula')
    # formrepresentantesAdd = crud.update(db.representantes,request.args(0))
    formCreate = crud.create(db.representantes)

    return locals()

@auth.requires_login()
def cadastrar():
	form = crud.create(db.representantes)

	return dict(form=form)    

@auth.requires_login()
def editar():
    codigo = request.vars.codigo
    form = crud.update(db.representantes, codigo)
    
    # pegar a foto do representante

    # form = crud.update(db.representantes, cod)
    # crud.settings.delete_next = URL('caixa')
    # form = 'jose'
    # return "%s %s"%(form,"<script> aplicar_estilo_form();</script>")
    return dict(form=form)


@auth.requires_login()
def buscar_representante():
	#codigo do representante recebido
	cod = request.vars.transitory
	#cadastro do representante recebido
	representante = db(db.representantes.id == cod).select()
	#busca avatar do representante
	img = URL('default','download',args=representante[0].foto_representante)
	if img == "/SIS_AB_FAB/default/download//":
		img = URL('static','assets/img/faces/face-0.png')
	else:
		img = URL('default','download',args=representante[0].foto_representante)
		pass

	cracha =DIV(
		DIV(
			IMG(_src=img,_class="avatar border-white"),
			H4('%s'%representante[0].nome,BR(),SPAN('%s'%representante[0].matricula,_class='matricula'),_class='title'),
			_class="author"),
			P('%s [ %s ]'%(representante[0].celular,representante[0].operadora),_class="description text-center"),
			DIV(
				FORM(
					DIV(
						DIV(
							DIV(
								LABEL('cnpj/cpf'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%representante[0].cnpj_cpf),
								_class="form-group"),
							_class="col-md-7"),
						DIV(
							DIV(
								LABEL('insc'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%representante[0].insc),
								_class="form-group"),
							_class="col-md-5"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('email'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%(representante[0].email)),
								_class="form-group"),
							_class="col-md-12"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('endereço'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s N: %s'%(representante[0].endereco,representante[0].numero)),
								_class="form-group"),
							_class="col-md-12"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('cidade'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%representante[0].cidade),
								_class="form-group"),
							_class="col-md-6"),
						DIV(
							DIV(
								LABEL('bairro'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%representante[0].bairro),
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


#select
def select():
	table = db(db.representantes.id==request.args[0]).select()
	return dict(table=table)
#insert
@auth.requires_membership('admin')
def inserir():
	return dict()
	#return dict(form=crud.create(db.produtos))
#update
@auth.requires_membership('admin')
def update():
	return dict(form=crud.update(db.representantes,request.args(0)))
#delete
def deletar():
	print request.vars.cod
	db(db.representantes.id == request.vars.cod).delete()
	return ''


# ===================================================
