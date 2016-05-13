# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

# response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
#                   _class="navbar-brand",_href="http://www.web2py.com/",
#                   _id="web2py-logo")

response.logo = IMG(_src=URL('static','images/logo-lojinha.png'),_class="navbar-brand", _id="logo-lojinha")

response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

# response.menu = [
#     (T('Home'), False, URL('home', 'index'), [])
# ]

DEVELOPMENT_MENU = True




#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    fun = request.function
    
    # MENU BARRA LATERAL
    response.barraL = UL(_class='nav')
    if ctr == 'daschboard':
      response.barraL.append(LI(A(I(_class='ti-panel'),P('dashboard'),_href='#'),_class='active'))
    else:
      response.barraL.append(LI(A(I(_class='ti-panel'),P('dashboard'),_href='#')))  
      pass
    if ctr == 'cadastros':
      response.barraL.append(LI(A(I(_class='ti-id-badge'),P('cadastros'),_href='../cadastros/clientes'),_class='active'))
    else:
      response.barraL.append(LI(A(I(_class='ti-id-badge'),P('cadastros'),_href='../cadastros/clientes'))) 
    if ctr == 'clientes':
      response.barraL.append(LI(A(I(_class='ti-layout-grid2-alt'),P('clientes'),_href='../clientes/atualizar'),_class='active'))
    else:
      response.barraL.append(LI(A(I(_class='ti-layout-grid2-alt'),P('clientes'),_href='../clientes/atualizar')))
      pass
    if ctr == 'vendas':
      response.barraL.append(LI(A(I(_class='ti-pie-chart'),P('vendas'),_href='../vendas/historico'),_class='active'))
    else:
      response.barraL.append(LI(A(I(_class='ti-pie-chart'),P('vendas'),_href='../vendas/historico')))  
      pass
    if ctr == 'alerta':
      response.barraL.append(LI(A(I(_class='ti-bell'),P('alerta'),_href='#'),_class='active'))
    else:
      response.barraL.append(LI(A(I(_class='ti-bell'),P('alerta'),_href='#'))) 
      pass
    # FIM MENU BARRA LATERAL

    # SUB MENU
    response.subMenu = UL()
    if fun == 'clientes':
      response.subMenu.append(LI(A('Clientes',_href='clientes'),_class='subMenuAtivo'))
      response.subMenu.append(LI(' / '))
    else:
      response.subMenu.append(LI(A('Clientesss',_href='clientes')))
      response.subMenu.append(LI(' / '))
    if ctr == 'representantes':
      response.subMenu.append(LI(A('Representantes',_href='representantes'),_class='subMenuAtivo'))
      response.subMenu.append(LI(' / '))
    else:
      response.subMenu.append(LI(A('Representantes',_href='representantes')))
      response.subMenu.append(LI(' / '))
    if ctr == 'funcionarios':
      response.subMenu.append(LI(A('Funcionários',_href='funcionarios'),_class='subMenuAtivo'))
    else:
      response.subMenu.append(LI(A('Funcionários',_href='funcionarios')))
    # FIM SUB MENU

if 'auth' in globals():
    if not auth.is_logged_in():  
        response.menu = []
    else:  
        if auth.has_membership('admin_2') or auth.has_membership('admin') :
            auth.settings.expiration = 864000 #10 dias de sessao aberta 
            response.menu += [
                
                  # (T('Home'), False, URL('default', 'index?menu=principal'), []),
                  (T('Vendas'),False, None, [
                    (T('Caixa'), False, URL('caixa', 'etapa_1?menu=caixa'), []),
                    (T('historico'), False, URL('caixa', 'historico?menu=caixa'), []),
                    #(T('Controle Cheque'), False, URL('caixa', 'historico?menu=caixa'), []),
                    (T('Controle Cheque'), False, URL('caixa', 'aguardaLancamento?menu=caixa'), []),
                  ]),
                  (T('Clientes'), False, URL('clientes', 'listarClientes?menu=clientes'), []),
                  (T('Funcionários'), False, URL('funcionarios', 'listarFuncionarios?menu=funcionarios'), []),
                  (T('Produtos'), False, URL('produtos', 'listarProdutos?menu=produtos'), []),
                  (T('Representantes'), False, URL('representantes', 'listarRepresentantes?menu=representantes'), []),
                  
                  (T('Operacional'),False, None, [
                    (T('Separar itens venda'), False, URL('pedidos', 'abertos?menu=operacional'), [])
                  ]),

                  # (T('Produtos'), False, None, [
                  #   (T('Listar Produtos'), False, URL('produtos', 'listarProdutos'), []),
                  #   (T('Cadastro Produtos'), False, URL('produtos', 'cadastrarProdutos'), [])
                  # ])
                ]  
        elif auth.has_membership('operacional_A'):
            response.menu = [
                (T('Operacional'),False, None, [
                    # (T('Separar itens venda'), False, URL('pedidos', 'abertos?menu=operacional'), []),
                    (T('Separar itens venda'), False, URL('pedidos', 'abertos?menu=operacional'), [])
                  ]),

                  # (T('Produtos'), False, None, [
                  #   (T('Listar Produtos'), False, URL('produtos', 'listarProdutos'), []),
                  #   (T('Cadastro Produtos'), False, URL('produtos', 'cadastrarProdutos'), [])
                  # ])
                ]  


if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
