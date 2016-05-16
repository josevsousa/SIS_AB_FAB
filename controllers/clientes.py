# -*- coding: utf-8 -*-

# @auth.requires_login()
def cadastrarClientes():
  	return dict(formCadastro=crud.create(db.clientes))

@auth.requires_login()
def listarClientes():
	clientes = db(db.clientes.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('clientes','deletar',args=[self.clientes.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('clientes','select',args=[self.clientes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('clientes','update',args=[self.clientes.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_id=self.clientes.id,_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('clientes','select',args=[self.clientes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('clientes','update',args=[self.clientes.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	clientes.setvirtualfields(campos_virtual = Virtual())		
	
	return dict(formListar=clientes)

@auth.requires_login()
def todos():
    grid = db(db.clientes.id>0).select('id','nome','foto_cliente')
    # formClientesAdd = crud.update(db.clientes,request.args(0))
    formCreate = crud.create(db.clientes)

    return locals()

@auth.requires_login()
def cadastrar():
	form = crud.create(db.clientes)
	return dict(form=form)    


@auth.requires_login()
def editar():
    codigo = request.vars.codigo
    form = crud.update(db.clientes, codigo)
    
    # pegar a foto do cliente

    # form = crud.update(db.clientes, cod)
    # crud.settings.delete_next = URL('caixa')
    # form = 'jose'
    # return "%s %s"%(form,"<script> aplicar_estilo_form();</script>")
    return dict(form=form)

@auth.requires_login()
def buscar_cliente():
	#codigo do cliente recebido
	cod = request.vars.transitory
	#cadastro do cliente recebido
	cliente = db(db.clientes.id == cod).select()

	#busca avatar do cliente
	img = URL('default','download',args=cliente[0].foto_cliente)
	if img == "/SIS_AB_FAB/default/download//":
		img = URL('static','assets/img/faces/face-0.png')
	else:
		img = URL('default','download',args=cliente[0].foto_cliente)
		pass

	cracha = DIV(
		DIV(
			IMG(_src=img,_class="avatar border-white"),
			H4('%s'%cliente[0].nome,BR(),H5('%s'%cliente[0].email),_class="title"),
			_class="author"),
			P('%s'%cliente[0].fixo,_class="description text-center"),
			DIV(
				FORM(
					DIV(
						DIV(
							DIV(
								LABEL('cnpj/cpf'),
								INPUT(_type="text", _class="form-control border-input", _value='%s'%cliente[0].cnpj_cpf),
								_class="form-group"),
							_class="col-md-7"),
						DIV(
							DIV(
								LABEL('insc'),
								INPUT(_type="text", _class="form-control border-input", _value='%s'%cliente[0].insc),
								_class="form-group"),
							_class="col-md-5"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('endereço'),
								INPUT(_type="text", _class="form-control border-input", _value='%s N: %s'%(cliente[0].endereco,cliente[0].numero)),
								_class="form-group"),
							_class="col-md-12"),
						_class="row"),
					DIV(
						DIV(
							DIV(
								LABEL('cidade'),
								INPUT(_type="text", _class="form-control border-input", _value='%s'%cliente[0].cidade),
								_class="form-group"),
							_class="col-md-6"),
						DIV(
							DIV(
								LABEL('bairro'),
								INPUT(_type="text", _class="form-control border-input", _value='%s'%cliente[0].bairro),
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

                                    # <div class="row">
                                    #     <div class="col-md-6">
                                    #         <div class="form-group">
                                    #             <label>First Name</label>
                                    #             <input type="text" class="form-control border-input" placeholder="Company" value="{{=auth.user.first_name}}">
                                    #         </div>
                                    #     </div>
                                    #     <div class="col-md-6">
                                    #         <div class="form-group">
                                    #             <label>Last Name</label>
                                    #             <input type="text" class="form-control border-input" placeholder="Last Name" value="{{=auth.user.last_name}}">
                                    #         </div>
                                    #     </div>
                                    # </div>



# ===================================================
#select
def select():
	table = db(db.clientes.id==request.args[0]).select()
	return dict(table=table)
#insert
def inserir():
	return dict(form=crud.create(db.clientes))
#update
def update():
	return dict(formUpdate=crud.update(db.clientes,request.args(0),_class="formEditar"))
#delete
@auth.requires_membership('admin')
def deletar():
	db(db.clientes.id == request.vars.cod).delete()
	return ''


def atualizar():
	return locals()


