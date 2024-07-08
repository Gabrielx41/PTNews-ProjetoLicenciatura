from collections import defaultdict
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
from verifica_login import verifica_login
from redis_utils.redis_jornais import obter_dados_jornais, obter_num_noticias
from redis_utils.redis_utilizador import obter_dados_utilizadores, utilizador_existe, remover_user, utilizador_admin
from urllib.parse import quote_plus
from functools import wraps
from guardar_password import guardar_password
import re
from redis.commands.search.query import Query
import urllib.parse
from uteis import *
import requests
from redis_utils.redis_grafo import get_keywords_redis
from grafo.uteis import build_graph_for_keyword

load_dotenv(override=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")
login_manager = LoginManager(app)


@app.route('/')
@login_required
def home_page():
    if(utilizador_existe(current_user.id)):
        return render_template("HomePage.html", navbar = True, isAdmin = current_user.is_admin)
    else:
        return redirect("/logout")

class User(UserMixin):
    def __init__(self, username, is_admin = False):
        self.id = username
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(username):
    isAdmin = utilizador_admin(username)
    return User(username, isAdmin)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    
    if current_user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            login, _ = verifica_login(request.form['username'], request.form['password'])
            if (login):
                #Iniciar a sessão
                user = User(request.form['username'])
                login_user(user)
                return redirect("/")
            else:
                return redirect("/login?error=" + quote_plus('Credenciais inválidas. Por favor, tente novamente.'))
        else:
            return render_template("LoginPage.html")



@app.route('/logout')
@login_required
def logout_page():
    # Fazer logout
    logout_user()
    return redirect("/login")



# Página de erro
@app.errorhandler(Exception)
@login_required
def handle_error(error):
    if(utilizador_existe(current_user.id)):
        return render_template('Error.html', isAdmin = current_user.is_admin)
    else:
        return redirect("/logout")
    

# Redirecionar o utilizador para a página de login quando não estiver autenticado
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return redirect('/error')

    return decorated_function


@app.route('/admin')
@login_required
@admin_required
def admin_page():
    if(utilizador_existe(current_user.id)):
        return render_template("AdminPage.html", navbar = True, isAdmin = current_user.is_admin)
    else:
        return redirect("/logout")


@app.route('/lista/utilizadores')
@login_required
@admin_required
def lista_utilizadores():
    if(utilizador_existe(current_user.id)):
        return jsonify(obter_dados_utilizadores(Query('*').paging(0, 10000)))
    else:
        return redirect("/logout")


@app.route('/adicionar/utilizador', methods=['POST'])
@login_required
@admin_required
def adicionar_utilizador():
    username, password, isAdmin = request.json.get('username'), request.json.get('password'), request.json.get('isAdmin')
    if len(password) < 8:
        return jsonify({'error': 'A password deve ter pelo menos 8 caracteres'})
# Verifica se a password possui pelo menos um número
    elif not any(char.isdigit() for char in password):
        return jsonify({'error': 'A password deve conter pelo menos um número'})
# Verifica se a password possui pelo menos uma letra maiúscula
    elif not any(char.isupper() for char in password):
        return jsonify({'error': 'A password deve conter pelo menos uma letra maiúscula'})
# Verifica se a password possui pelo menos uma letra minúscula
    elif not any(char.islower() for char in password):
        return jsonify({'error': 'A password deve conter pelo menos uma letra minúscula'})
# Verifica se a password possui pelo menos um caractere especial
    elif not re.search(r'[!@#$%^&*()_+{}|:"<>?/\-=[\];\',./]', password):
        return jsonify({'error': 'A password deve conter pelo menos um caractere especial'})
    
    if(isAdmin == 'admin'):
        isAdmin = True
    else:
        isAdmin = False

    if(utilizador_existe(current_user.id)):
        resposta = guardar_password(username, password, isAdmin)
        if resposta:
            return jsonify({'success': resposta})
        else:
            return jsonify({'error': 'Já existe um utilizador com esse username.'})
    else:
        return redirect("/logout")


@app.route('/remover/utilizador', methods=['POST'])
@login_required
@admin_required
def remover_utilizador():
    username = request.json.get('username')
    if(utilizador_existe(current_user.id)):
        resposta = remover_user(username)
        return jsonify({'success': resposta})
    else:
        return redirect("/logout")



@app.route('/api/<nome_jornal>/ultimas')
@login_required
def api_jornais(nome_jornal):
    if(utilizador_existe(current_user.id)):
        ordem = request.args.get('ordem')
        
        paginaAtual = int(request.args.get('paginaAtual'))
        paginaAtual = (paginaAtual-1) * 12
        
        if(nome_jornal != "24h"):
            query = Query(f'@source:{nome_jornal} -@content:"null"').sort_by('published', False).paging(paginaAtual, 12)
            query = ordenar(ordem, query)
            
            dados = obter_dados_jornais(query)
        else:
            hoje = datetime.now().timestamp()
            ontem = (datetime.now() - timedelta(days=1)).timestamp()
            query = Query(f'@published:[{ontem} {hoje}] -@content:"null"').sort_by('published', False).paging(paginaAtual, 12)
            query = ordenar(ordem, query)
            
            dados = obter_dados_jornais(query)

        return jsonify({'dados': dados})
    else:
        return redirect("/logout")
    
    
@app.route('/api/<nome_jornal>/ultimas/num_noticias')
@login_required
def api_jornais_num_noticias(nome_jornal):
    if(utilizador_existe(current_user.id)):
        if(nome_jornal != "24h"):
            query = Query(f'@source:{nome_jornal} -@content:"null"').paging(0,100000)
            totalNoticias = obter_num_noticias(query)
            
            query2 = Query(f'@source:{nome_jornal} -@content:"null"').sort_by('published', False).paging(0,1)
            query3 = Query(f'@source:{nome_jornal} -@content:"null"').sort_by('published', True).paging(0,1)
            
            inicio = obter_dados_jornais(query2)[0]['published']
            fim = obter_dados_jornais(query3)[0]['published']
        else:
            hoje = datetime.now().timestamp()
            ontem = (datetime.now() - timedelta(days=1)).timestamp()
            query = Query(f'@published:[{ontem} {hoje}] -@content:"null"').paging(0,100000)
            totalNoticias = obter_num_noticias(query)

            inicio = hoje
            fim = ontem

        return jsonify({"num_noticias": totalNoticias, "inicio": inicio, "fim": fim})
    else:
        return redirect("/logout")


@app.route('/media/<nome_jornal>')
@login_required
def jornais_page(nome_jornal):
    if(utilizador_existe(current_user.id)):
        return render_template("JornaisPage.html", navbar = True, isAdmin = current_user.is_admin, nome_jornal=nome_jornal, show_spinner = True)
    else:
        return redirect("/logout")

@app.route('/api/pesquisa', methods=['POST'])
@login_required
def api_pesquisa():
    if(utilizador_existe(current_user.id)):
        session['selectedOpt'], session['searchText'], session['dataMin'], session['dataMax'], session['jornal'], session['psqExata'] = request.json['selectedOpt'], request.json.get('searchText'), request.json.get('minDate'), request.json.get('maxDate'), request.json.get('jornal'), request.json.get('psqExata')
        return jsonify({'success': 'Dados guardados com sucesso'})
    else:
        return redirect("/logout")


jornais =[
          "DNoticias",
          "Eco",
          "JNegocios",
          "Público",
          "Observador",
          "NAM",
          "IOnline",
          "Expresso",
          "Renascenca",
          "Sapo24",
          "SicNoticias"
         ]

@app.route('/api/pesquisa/<selectedOption>')
@login_required
def api_pesquisa_selectOpt(selectedOption):
    if(utilizador_existe(current_user.id)):
        resultado = []
        
        dataMin, dataMax = to_timestamp(session.get('dataMin')), to_timestamp(session.get('dataMax'))
        
        searchText = session.get('searchText')

        ordem = request.args.get('ordem')
        
        sources = session.get('jornal')
        
        paginaAtual = int(request.args.get('paginaAtual'))
        paginaAtual = (paginaAtual-1) * 12
        
        if(dataMin < dataMax):
            dataMin, dataMax = dataMax, dataMin

        tempSearchText = searchText
        
        searchText = searchText.replace("\"", "'")
        
        if (session.get('psqExata') and selectedOption != "grafo"):
            searchText = f'"{searchText}"'

        jornal = ""
        if (sources):
            jornal = "@source:"
            for i, source in enumerate(sources):
                jornal += source
                if i < len(sources) - 1:
                    jornal += "|"
        
        match selectedOption:
            case 'texto':
                query = Query(f'{jornal} @published:[{dataMax} {dataMin}] @title|content|lead:{searchText} -@content:"null"').paging(paginaAtual, 12)
                query = ordenar(ordem, query)
                resultado = obter_dados_jornais(query)
                
            case 'imagem':
                query = Query(f'{jornal} @published:[{dataMax} {dataMin}] @title|lead|images:{searchText} -@content:"null"').paging(paginaAtual, 12)
                query = ordenar(ordem, query)
                resultado = obter_dados_jornais(query)
                
            case 'autor':
                query = Query(f'{jornal} @published:[{dataMax} {dataMin}] @authors:{searchText} -@content:"null"').paging(paginaAtual, 12)
                query = ordenar(ordem, query)
                resultado = obter_dados_jornais(query)
            
            case 'percentagem':
                global jornais
                dicionario = {}
                dicionario_sentiment = {}
                total = 0

                for jornaal in jornais:
                    query = Query(f'@published:[{dataMax} {dataMin}] @source:{jornaal} @title|lead|images:{searchText} -@content:"null"').paging(0,1000000)
                    num = obter_num_noticias(query)
                    dicionario[jornaal] = num
                    total += num

                if(total == 0):
                    dicionario = {}

                total = 0
                for sentiment in ["Neutro", "Positivo", "Negativo"]:
                    query2 = Query(f'@published:[{dataMax} {dataMin}] @title|lead|images:{searchText} @sentiment:{sentiment} -@content:"null"').paging(0,1000000)
                    num2 = obter_num_noticias(query2)
                    dicionario_sentiment[sentiment] = num2

                    total += num2

                if(total == 0):
                    dicionario_sentiment = {}

                if ((not dicionario_sentiment and not dicionario)):
                    resultado = []
                else:
                    resultado = [{"num_noticias": dicionario,"num_sentiment": dicionario_sentiment}]
                
            case 'grafo':
                window_size = 0
                target_word = searchText.lower()
                ii_coccur = get_keywords_redis("keywords")
                    
                graphs = {}  # Dicionário para armazenar os grafos

                for i in range(5, 21):
                    top_cooccurrences = ii_coccur.get_top_cooccurrences(target_word, window_size=window_size, top_n=i)
                    if top_cooccurrences:
                        graph = build_graph_for_keyword(ii_coccur, target_word, top_cooccurrences)
                        graphs[i] = graph
                if graphs:
                    resultado = [graphs]
    
        if resultado:
            return jsonify({"data": resultado, "searchText": tempSearchText, "jornal": sources, 'inicio': dataMin, 'fim': dataMax, 'psqExata': session.get('psqExata')})
        else:
            return jsonify({"data": [], "searchText": tempSearchText, "jornal": sources, 'inicio': dataMin, 'fim': dataMax})
        
    else:
        return redirect("/logout")


@app.route('/api/pesquisa/num_noticias/<selectedOption>')
@login_required
def api_pesquisa_num_noticias_selectOpt(selectedOption):
    if(utilizador_existe(current_user.id)):
        dataMin, dataMax = to_timestamp(session.get('dataMin')), to_timestamp(session.get('dataMax'))
        searchText = session.get('searchText')
        
        sources = session.get('jornal')

        searchText = searchText.replace("\"", "'")
        
        if (session.get('psqExata')):
            searchText = f'"{searchText}"'

        if(dataMin < dataMax):
            dataMin, dataMax = dataMax, dataMin
            
        jornal = ""
        if (sources):
            jornal = "@source:"
            for i, source in enumerate(sources):
                jornal += source
                if i < len(sources) - 1:
                    jornal += "|"

        match selectedOption:
            case 'texto':
                query2 = Query(f'{jornal} @published:[{dataMax} {dataMin}] @title|content|lead:{searchText} -@content:"null"').paging(0,1000000)
                totalNoticias = obter_num_noticias(query2)
                
            case 'imagem':
                query2 = Query(f'{jornal} @published:[{dataMax} {dataMin}] @title|lead|images:{searchText} -@content:"null"').paging(0,1000000)
                totalNoticias = obter_num_noticias(query2)
                
            case 'autor':
                query2 = Query(f'{jornal} @published:[{dataMax} {dataMin}] @authors:{searchText} -@content:"null"').paging(0,1000000)
                totalNoticias = obter_num_noticias(query2)
                
            case 'percentagem':
                global jornais
                dicionario = {}
                
                for jornaal in jornais:
                    query = Query(f'@published:[{dataMax} {dataMin}] @source:{jornaal} -@content:"null"').paging(0,1000000)
                    num = obter_num_noticias(query)
                    dicionario[jornaal] = num

                totalNoticias = dicionario
            case 'grafo':
                totalNoticias = 1

        return jsonify(totalNoticias)
        
    else:
        return redirect("/logout")


@app.route('/pesquisa')
@login_required
def pesquisa_page():
    if(utilizador_existe(current_user.id)):
        return render_template("PesquisaPage.html", navbar = True, isAdmin = current_user.is_admin, selectedOption=session.get('selectedOpt'), show_spinner = True)
    else:
        return redirect("/logout")


@app.route('/api/estatisticas')
@login_required
def api_estatisticas():
    global jornais
    if(utilizador_existe(current_user.id)):
        query = Query('*').paging(0, 100000)
        
        resultados = obter_dados_jornais(query)

            ############ Número de notícias publicadas por dia ############
        contagem_por_jornal_e_data = defaultdict(lambda: defaultdict(int))

        for doc in resultados:
            timestamp = float(doc['published'])
            data_publicacao = datetime.fromtimestamp(timestamp).date()
            
            jornal = doc.get('source')
            contagem_por_jornal_e_data["Total"][data_publicacao.strftime("%d/%m/%Y")] += 1
            contagem_por_jornal_e_data[jornal][data_publicacao.strftime("%d/%m/%Y")] += 1

        resultado1 = {jornal: dict(contagem_por_jornal_e_data[jornal]) for jornal in contagem_por_jornal_e_data}
        

            ############ Top pessoas citadas e Top localizações ############
        pessoas_citadas = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        organizacoes = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for noticia in resultados:
            timestamp = float(noticia['published'])
            data_publicacao = datetime.fromtimestamp(timestamp).date()
            
            jornal = noticia.get('source')
            entities = noticia['entities']

            if 'PER' in entities and entities['PER'] is not None:
                for entidade in entities['PER']:
                    pessoas_citadas[jornal][data_publicacao][entidade] += 1
                    pessoas_citadas["Total"][data_publicacao][entidade] += 1
            
            if 'ORG' in entities and entities['ORG'] is not None:
                for entidade in entities['ORG']:
                    organizacoes[jornal][data_publicacao][entidade] += 1
                    organizacoes["Total"][data_publicacao][entidade] += 1

        top_pessoas_citadas = defaultdict(lambda: defaultdict(tuple))
        top_organizacoes = defaultdict(lambda: defaultdict(tuple))

        for source, dias in pessoas_citadas.items():
            for dia, entidades in dias.items():
                if entidades:
                    top_entidade = sorted(entidades.items(), key=lambda x: x[1], reverse=True)[0]
                    top_pessoas_citadas[source][dia] = top_entidade

        for source, dias in organizacoes.items():
            for dia, entidades in dias.items():
                if entidades:
                    top_entidade = sorted(entidades.items(), key=lambda x: x[1], reverse=True)[0]
                    top_organizacoes[source][dia] = top_entidade

        resultado3 = {source: {data.strftime("%d/%m/%Y"): top for data, top in dias.items()} for source, dias in top_pessoas_citadas.items()}
        resultado5 = {source: {data.strftime("%d/%m/%Y"): top for data, top in dias.items()} for source, dias in top_organizacoes.items()}

            ############ Autores com mais publicações ############
        top_autores = defaultdict(int)

        # Iterar sobre cada notícia
        for noticia in resultados:
            autores = noticia['authors']
            if autores != None:
                for autor in autores:
                    top_autores[autor['name']] += 1
                    # top_autores['Outros'] += 1

        resultado2 = dict(sorted(top_autores.items(), key=lambda x: x[1], reverse=True)[:11])

        # total_outros = resultado2['Outros']
        # del resultado2['Outros']

        # for autor, publicacoes in resultado2.items():
        #     total_outros -= publicacoes

        # resultado2['Outros'] = total_outros
        

            ############ wordcloud ############
        top_keywords = defaultdict(int)

        # Iterar sobre cada notícia
        for noticia in resultados:
            keywords = noticia['keywords']
            if keywords != None:
                for keyword in keywords:
                    top_keywords[keyword] += (1 * keywords[keyword])

        top_keywords = dict(sorted(top_keywords.items(), key=lambda x: x[1], reverse=True)[:25])

        top_keywords = normalize_scores(top_keywords)

        criar_wordcloud(top_keywords)


            ############ Análise de sentimentos das notícias ############
        dicionario_sentimentos = defaultdict(lambda: defaultdict(int))

        for noticia in resultados:
            jornal = noticia.get('source')
            sentiment = noticia.get('sentiment')
            if sentiment in ["Neutro", "Positivo", "Negativo"]:
                dicionario_sentimentos[jornal][sentiment] += 1
                dicionario_sentimentos["Total"][sentiment] += 1
        
        for source, sentiment_counts in dicionario_sentimentos.items():
            total = sum(sentiment_counts.values())
            percentages = {sentiment: round((count / total) * 100, 2) for sentiment, count in sentiment_counts.items()}
            dicionario_sentimentos[source] = percentages

        resultado4 = {source: dict(dicionario_sentimentos[source]) for source in dicionario_sentimentos}
        
        
        resultado = {
            'Número de notícias publicadas' : resultado1,
            'Autores com mais publicações' : resultado2,
            'wordcloud' : {},
            'Principais pessoas citadas' : resultado3,
            'Análise de sentimentos' : resultado4,
            'Organizações com maior destaque' : resultado5
        }
        
        return jsonify(resultado)
    else:
        return redirect("/logout")


@app.route('/estatisticas')
@login_required
def estatisticas_page():
    if(utilizador_existe(current_user.id)):
        return render_template("EstatisticasPage.html", navbar = True, isAdmin = current_user.is_admin, show_spinner = True)
    else:
        return redirect("/logout")


@app.route('/noticia/<path:id>')
@login_required
def notica_page(id):
    if(utilizador_existe(current_user.id)):
        id = id.replace('&g&', '%')
        decoded_id = urllib.parse.unquote(id)
        
        try:
            source, id_noticia = decoded_id.split(':https:')
            id_noticia = id_noticia.replace('-', ' ')
        except:
            source, id_noticia = decoded_id.split(':')
            id_noticia = id_noticia.replace('-', ' ')

        query = Query(f'@id:{id_noticia} @source:{source}')
        noticia = obter_dados_jornais(query)
        
        if(noticia):
            noticia = noticia[0]
            noticia['published'] = to_date(noticia['published'])
            
            noticia['keywords'] = list(noticia['keywords'].keys())

            session["entidades"] = noticia['entities']['LOC']
        
        contentInicio = get_content_highlighter(noticia["content"][:1000], noticia["keywords"])

        if len(noticia["content"]) > 1000 and (noticia["content"][999] == " " or noticia["content"][1000] == " "):
            noticia["content"] = get_content_highlighter(noticia["content"][1000:], noticia["keywords"])
            noticia["content"] = " " + noticia["content"]
        else:
            noticia["content"] = get_content_highlighter(noticia["content"][1000:], noticia["keywords"])
        
        return render_template("NoticiaPage.html", navbar = True, isAdmin = current_user.is_admin, noticia = noticia, contentInicio = contentInicio)
    else:
        return redirect("/logout")


@app.route('/mapa')
@login_required
def mapa_page():
    if(utilizador_existe(current_user.id)):
        entidades = session['entidades']
        if entidades:
            ListOfLatitudes, ListOfLongitudes, ListOfNames = get_coordenadas(entidades)
            map_plotter(ListOfLatitudes, ListOfLongitudes, ListOfNames)
        return render_template("NoticiaMap.html")
    else:
        return redirect("/logout")


@app.route('/download_image')
@login_required
def download_image():
    if(utilizador_existe(current_user.id)):
        image_url = request.args.get('url')
        try:
            with requests.get(image_url, stream=True) as r:
                # Abra um arquivo temporário para escrever os dados da imagem
                with open("./static/images/imagem.png", "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return "imagem"
        except:
            return ""
    else:
        return redirect("/logout")

@app.route('/top_topics')
@login_required
def top_topics():
    if(utilizador_existe(current_user.id)):
        top_topics = get_top_topics(20)
        resultado = []
        num_noticias = {}
        ordem = []
        for topic in top_topics:
            query = Query(f'@title|content|lead:"{topic}" -@content:"null"').sort_by('published', False).paging(0, 4)
            dados = obter_dados_jornais(query)
            numNoticias = obter_num_noticias(query)
            if (dados):
                ordem.append(topic)
                resultado.append({topic: dados})
                num_noticias[topic] = numNoticias
                
        return jsonify({"top_topics": resultado, "num_noticias": num_noticias})
    else:
        return redirect("/logout")

@app.route('/trends')
@login_required
def trends():
    if(utilizador_existe(current_user.id)):
        return render_template("Trends.html", navbar = True, isAdmin = current_user.is_admin, show_spinner = True)
    else:
        return redirect("/logout")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)