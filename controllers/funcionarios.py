# -*- coding: utf-8 -*-

# @auth.requires_login()
def cadastrarFuncionarios():
  	return dict(formCadastro=crud.create(db.funcionarios))

# @auth.requires_login()
def listarFuncionarios():
	funcionarios = db(db.funcionarios.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('Funcionarios','deletar',args=[self.Funcionarios.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('funcionarios','select',args=[self.funcionarios.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('funcionarios','update',args=[self.funcionarios.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_id=self.funcionarios.id,_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('funcionarios','select',args=[self.funcionarios.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('funcionarios','update',args=[self.funcionarios.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	funcionarios.setvirtualfields(campos_virtual = Virtual())		
	
	return dict(formListar=funcionarios,d=funcionarios)

@auth.requires_login()
def todos():
    grid = db(db.funcionarios.id>0).select('id','nome','foto_funcionario','matricula')
    # formClientesAdd = crud.update(db.clientes,request.args(0))
    formCreate = crud.create(db.funcionarios)

    return locals()


@auth.requires_login()
def cadastrar():
	form = crud.create(db.funcionarios)
	return dict(form=form)    

@auth.requires_login()
def editar():
    codigo = request.vars.codigo
    form = crud.update(db.funcionarios, codigo)
    
    # pegar a foto do cliente

    # form = crud.update(db.clientes, cod)
    # crud.settings.delete_next = URL('caixa')
    # form = 'jose'
    # return "%s %s"%(form,"<script> aplicar_estilo_form();</script>")
    return dict(form=form)

@auth.requires_login()
def buscar_funcionario():
	#codigo do funcionario recebido
	cod = request.vars.transitory
	#cadastro do funcionario recebido
	funcionario = db(db.funcionarios.id == cod).select()

	#busca avatar do funcionario
	img = URL('default','download',args=funcionario[0].foto_funcionario)
	if img == "/SIS_AB_FAB/default/download//":
		img = URL('static','assets/img/faces/face-0.png')
	else:
		img = URL('default','download',args=funcionario[0].foto_funcionario)
		pass

	cracha = DIV(
		DIV(
			IMG(_src=img,_class="avatar border-white"),
			H4('%s'%funcionario[0].nome,BR(),SPAN('%s'%funcionario[0].matricula,_class='cracha'),_class='title'),
			_class="author"),
			P('%s'%(funcionario[0].fixo),_class="description text-center"),
			DIV(
				FORM(
					DIV(
						DIV(
							DIV(
								LABEL('cnpj/cpf'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%funcionario[0].cnpj_cpf),
								_class="form-group"),
							_class="col-md-7"),
						DIV(
							DIV(
								LABEL('matrícula'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%funcionario[0].matricula),
								_class="form-group"),
							_class="col-md-5"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('endereço'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s N: %s'%(funcionario[0].endereco,funcionario[0].numero)),
								_class="form-group"),
							_class="col-md-12"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('cidade'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%funcionario[0].cidade),
								_class="form-group"),
							_class="col-md-6"),
						DIV(
							DIV(
								LABEL('bairro'),
								INPUT(_type="text", _class="form-control border-input",_style='background-color: #F1F1F1', _disabled=True, _value='%s'%funcionario[0].bairro),
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

# ===================================================
#select
def select():
	table = db(db.funcionarios.id==request.args[0]).select()
	return dict(table=table)
#insert
def inserir():
	return dict(form=crud.create(db.funcionarios))
#update
def update():
	return dict(formUpdate=crud.update(db.funcionarios,request.args(0),_class="formEditar"))
#delete
@auth.requires_membership('admin')
def deletar():
	db(db.funcionarios.id == request.vars.cod).delete()
	return ''



