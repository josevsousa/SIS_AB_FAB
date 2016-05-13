def equipe():
	return locals()

def clientes():
    grid = db(db.clientes.id>0).select('id','nome','foto_cliente')
    # formClientesAdd = crud.update(db.clientes,request.args(0))
    formClientesAdd = crud.create(db.clientes)
    return locals()

def formClientes():
    print 'entrei no formClientes'
    
    # ------------- row 1
    # tipo = SELECT(OPTION('Pessoa Física',_value='pessoa_fisica'),OPTION('Pessoa Jurídica',_value='pessoa_juridica'),_class="form-control border-input")
    # tipo_4 = DIV(DIV(LABEL('Tipo cliente'),tipo,_class="form-group"),_class="col-md-4")
    # nome = INPUT(_type="text", _class="form-control border-input", _placeholder="Company", _value="")
    # nome_8 = DIV(DIV(LABEL('Nome'),nome,_class="form-group"),_class='col-md-8')
    # row_1 = DIV(tipo_4,nome_8,_class="row")

    # # ------------- row 2
    # telefone = INPUT(_type="text", _class="form-control border-input", _placeholder="Telefone", _value="")
    # telefone_4 = DIV(LABEL('Telefone'),telefone,_class='col-md-4')
    # celular = INPUT(_type="text", _class="form-control border-input", _placeholder="Celular", _value="")
    # celular_5 = DIV(LABEL('Celular'),celular,_class='col-md-5')
    # operadora = SELECT(OPTION('CLARO',_value='claro'),OPTION('VIVO',_value='vivo'),OPTION('TIM',_value='tim'),OPTION('OI',_value='OI'),_class="form-control border-input")
    # operadora_3 = DIV(LABEL('Operadora'),operadora,_class='col-md-3')
    # row_2 = DIV(telefone_4,celular_5,operadora_3,_class='row')

    # # -------------- row 4
    # email = INPUT(_type="text", _class="form-control border-input", _placeholder="e-mail", _value="")
    # email_8 = DIV(LABEL('E-mail'),email,_class='col-md-8')
    # cep = INPUT(_type="text", _class="form-control border-input", _placeholder="cep", _value="")
    # cep_4 = DIV(LABEL('CEP'),cep,_class='col-md-4')
    # row_3 = DIV(email_8,cep_4,_class='row')

    # # -------------- row 5
    # endereco = INPUT(_type="text", _class="form-control border-input", _placeholder="endereço", _value="")
    # endereco_10 = DIV(LABEL('Endereço'),endereco,_class='col-md-10')
    # numero = INPUT(_type="text", _class="form-control border-input", _placeholder="00", _value="")
    # numero_2 = DIV(LABEL('Número'),numero,_class='col-md-2')
    # row_4 = DIV(endereco_10,numero_2,_class='row')

    # -------------- row 5
    # cidade = INPUT(_type="text", _class="form-control border-input", _placeholder="endereço", _value="")
    # cidade_4 = DIV(LABEL('Endereço'),endereco,_class='col-md-4')
    # numero = INPUT(_type="text", _class="form-control border-input", _placeholder="00", _value="")
    # numero_2 = DIV(LABEL('Número'),numero,_class='col-md-2')
    # row_4 = DIV(endereco_10,numero_2,_class='row')

    meuForm = ""\
    '<form id="form_clientes">'\
    	'<div class="row">'\
        	'<div class="col-md-5">'\
                '<div class="form-group">'\
                    '<label>Company</label>'\
                    '<input type="text" class="form-control border-input" disabled="" placeholder="Company" value="Artesanal Baby">'\
                '</div>'\
            '</div>'\
        '</div>'\
        '<div class="text-center">'\
            '<button type="text" id="btForm" class=" btn btn-default btn-fill btn-wd">+ Adcionar</button>'\
        '</div>'\
        '<div class="clearfix"></div>'\
    '</form>'

    # form = crud.insert(db.clientes)
    # form = FORM(row_1,row_2,row_3,row_4, _id="form_clientes")
    return meuForm