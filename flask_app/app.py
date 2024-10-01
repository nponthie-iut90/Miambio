from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",  # à modifier
            user="login",  # à modifier
            password="mdp",  # à modifier
            database="BDD",  # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.route('/')
def show_layout():
    return render_template('layout.html')


# ROUTES D'ANNA

@app.route('/recolte/show')
def show_recolte():
    mycursor = get_db().cursor()
    sql='''
        SELECT id_recolte, quantite_recoltee, id_semaine, id_produit, id_maraicher
        FROM recolte
        ORDER BY id_recolte;
    '''
    mycursor.execute(sql)
    recoltes = mycursor.fetchall()
    sql = '''SELECT * FROM maraichers'''
    mycursor.execute(sql)
    maraichers = mycursor.fetchall()

    sql = '''SELECT * FROM produits'''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    return render_template('recolte/show_recolte.html', recoltes=recoltes, maraichers=maraichers, produits=produits)

@app.route('/recolte/add', methods=['GET'])
def add_recolte():
    print('''affichage du formulaire pour saisir une récolte''')
    mycursor = get_db().cursor()
    sql='''SELECT * FROM semaine'''
    mycursor.execute(sql)
    semaines = mycursor.fetchall()

    sql='''SELECT * FROM produits'''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''SELECT * FROM maraichers'''
    mycursor.execute(sql)
    maraichers = mycursor.fetchall()

    return render_template('recolte/add_recolte.html' , semaines=semaines , produits=produits , maraichers=maraichers)


@app.route('/recolte/edit', methods=['GET'])
def edit_recolte():
    print('''Modifier une récolte''')
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql='''
        SELECT  id_recolte as id,  quantite_recoltee AS qtRecolte, Id_Semaine AS semaine, Id_produit AS id_produit, Id_Maraicher AS id_maraicher
        FROM recolte
        WHERE id_recolte=%s;'''
    mycursor.execute(sql,id)
    recolte = mycursor.fetchone()

    mycursor = get_db().cursor()
    sql='''SELECT * FROM semaine'''
    mycursor.execute(sql)
    semaines = mycursor.fetchall()

    sql='''SELECT * FROM produits'''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''SELECT * FROM maraichers'''
    mycursor.execute(sql)
    maraichers = mycursor.fetchall()
    return render_template('recolte/edit_recolte.html', recolte=recolte , semaines=semaines , produits=produits , maraichers=maraichers)


@app.route('/recolte/add', methods=['POST'])
def valid_add_recolte():
    print('''ajout de récolte dans le tableau''')
    qtRecolte = request.form.get('qtRecolte')
    semaine = request.form.get('Id_Semaine')
    id_produit = request.form.get('Id_produit')
    id_maraicher = request.form.get('Id_Maraicher')

    message = ' - Quantité récoltée :' + qtRecolte + ' - semaine n° :' + semaine +' - produit n° :' + id_produit +' - récolté par :' + id_maraicher
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(qtRecolte, semaine, id_produit, id_maraicher)
    sql="INSERT INTO recolte(id_recolte, quantite_recoltee, id_semaine, id_produit, id_maraicher) VALUES (NULL, %s, %s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/recolte/show')

@app.route('/recolte/edit', methods=['POST'])
def valid_edit_recolte():
    print('''modification de la récolte ''')
    id = request.form.get('id')
    qtRecolte = request.form.get('qtRecolte')
    semaine = request.form.get('Id_Semaine')
    id_produit = request.form.get('Id_produit')
    id_maraicher = request.form.get('Id_Maraicher')
    print(qtRecolte,semaine,id_produit,id_maraicher,id)


    mycursor = get_db().cursor()
    sql="UPDATE recolte SET quantite_recoltee = %s, id_semaine=%s,  id_produit=%s, id_maraicher= %s WHERE id_recolte=%s;"
    mycursor.execute(sql,(qtRecolte,semaine,id_produit,id_maraicher,id))
    get_db().commit()
    return redirect('/recolte/show')

@app.route('/recolte/delete' , methods=['GET'])
def delete_recolte():
    print('''suppression d'une récolte''')
    id = request.args.get('id', 'heyyy')
    mycursor = get_db().cursor()
    sql = "DELETE FROM recolte WHERE Id_recolte=%s;"
    mycursor.execute(sql, id)
    get_db().commit()
    print('La recolte avec le numéro '+id + 'a été supprimé')
    return redirect('/recolte/show')


@app.route('/recolte/etat', methods=['GET'])
def recolte_etat():
    connection = get_db()
    mycursor = connection.cursor()

    sql_recolte_semaine = '''
    SELECT Id_Semaine, Id_produit, SUM(Quantite_recoltee) AS TotalRecolte
    FROM recolte
    GROUP BY Id_Semaine, Id_produit
    ORDER BY Id_Semaine, Id_produit;
    '''
    mycursor.execute(sql_recolte_semaine)
    etat_recolte_totale = mycursor.fetchall()

    mycursor.execute(sql_recolte_semaine)
    state_data = mycursor.fetchall()

    return render_template('recolte/etat_recolte.html',
                           etat_recolte_totale=etat_recolte_totale)




# LES ROUTE DE SIMONE


@app.route('/produit/show')
def show_produit():
    mycursor = get_db().cursor()
    sql='''
    SELECT id_produit, libelle_produit, id_categorie_produit
    FROM produits
    ORDER BY id_produit
    '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()
    return render_template('produit/show_produit.html', produits=produits)


@app.route('/produit/add', methods=['GET'])
def add_produit():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM categorie_produit'''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()
    return render_template('produit/add_produit.html', categories=categorie)



@app.route('/produit/add', methods=['POST'])
def valid_add_produit():
    print('''ajout du produit dans le tableau''')
    lbproduit = request.form.get('lbproduit')
    Id_categorie_produit = request.form.get('Id_categorie_produit')
    message = u' produit ajouté , lbproduit:' + lbproduit + ' - Id_categorie_produit:' + Id_categorie_produit
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(lbproduit,Id_categorie_produit)
    sql = "INSERT INTO produits(libelle_produit, id_categorie_produit, id_produit) VALUES (%s, %s, NULL)"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/produit/show')

@app.route('/produit/delete')
def delete_produit():
    print('''suppression d'un produit''')
    id = request.args.get('id', None)
    verifier = []
    mycursor = get_db().cursor()
    sql="SELECT * FROM recolte WHERE id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM production WHERE id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM periode_de_vente WHERE id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM vente WHERE id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    print(verifier)
    if len(verifier) ==0 :
        sql = "DELETE FROM produits WHERE id_produit=%s;"
        mycursor.execute(sql, id)
        get_db().commit()
    else:
        print("ce n'est pas possible")
    print(f'''le produit dans le tableau {id} a été supprimer''' )
    return redirect('/produit/show')

@app.route('/produit/edit', methods=['GET'])
def edit_produit():
    print('''affichage du formulaire pour modifier un produit''')
    id=request.args.get('id')
    mycursor = get_db().cursor()

    sql = '''
    SELECT Id_produit, libelle_produit, id_categorie_produit
    FROM produits  
    WHERE id_produit = %s
    '''
    mycursor.execute(sql, id)
    produit = mycursor.fetchone()

    sql = '''SELECT * FROM categorie_produit'''
    mycursor.execute(sql)
    categories = mycursor.fetchall()

    return render_template('produit/edit_produit.html', produit=produit, categories=categories)


@app.route('/produit/edit', methods=['POST'])
def valid_edit_produit():
    print('''validation de la modification d'un produit''')
    id = request.form.get('id')
    categorie = request.form.get('Id_categorie_produit')
    lbproduit = request.form.get('lbproduit')

    mycursor = get_db().cursor()
    sql = '''UPDATE produits SET libelle_produit=%s , id_categorie_produit=%s WHERE id_produit = %s'''
    tuple_param = (lbproduit, categorie, id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/produit/show')


@app.route('/produit/etat', methods=['GET'])
def etat_produit():
    mycursor = get_db().cursor()

    # Retrieve the product ID from the request or another source
    id = request.args.get('id')

    sql = '''
        SELECT id_produit, libelle_produit, id_categorie_produit
        FROM produits
        WHERE id_produit = %s
    '''
    mycursor.execute(sql, (id,))
    product_info = mycursor.fetchone()

    sql_recolte = "SELECT * FROM recolte WHERE id_produit=%s"
    mycursor.execute(sql_recolte, (id,))
    recolte_info = mycursor.fetchall()

    sql_produit = "SELECT * FROM production WHERE id_produit=%s"
    mycursor.execute(sql_produit, (id,))
    produit_info = mycursor.fetchall()

    sql_periode_vente = "SELECT * FROM periode_de_vente WHERE id_produit=%s"
    mycursor.execute(sql_periode_vente, (id,))
    periode_vente_info = mycursor.fetchall()

    sql_vente = "SELECT * FROM vente WHERE id_produit=%s"
    mycursor.execute(sql_vente, (id,))
    vente_info = mycursor.fetchall()

    return render_template('produit/etat_produit.html', product=product_info, recolte=recolte_info, produit=produit_info, periode_vente=periode_vente_info, vente=vente_info)







# ROUTES DE NATHAN

@app.route('/production/show')
def show_production():
    mycursor = get_db().cursor()
    sql = '''
    SELECT production.id_production, produits.libelle_produit, maraichers.nom_maraicher, production.surface_cultivee
    FROM production
    JOIN maraichers ON production.id_maraicher = maraichers.id_maraicher
    JOIN produits ON production.id_produit = produits.id_produit;
    '''
    mycursor.execute(sql)
    liste_production = mycursor.fetchall()

    return render_template('production/show_production.html', production=liste_production)

@app.route('/production/edit', methods=['GET'])
def show_edit_production_form():
    print("Affichage du formulaire de modification d'une production")
    print(request.args)
    print(request.args.get('id'))

    mycursor = get_db().cursor()

    production_id = request.args.get('id', 0)

    produits_sql='''SELECT id_produit, libelle_produit FROM produits;'''
    mycursor.execute(produits_sql)
    produits = mycursor.fetchall()
    maraichers_sql='''SELECT id_maraicher, nom_maraicher FROM maraichers;'''
    mycursor.execute(maraichers_sql)
    maraichers = mycursor.fetchall()

    production_sql='''
    SELECT id_production, id_produit, id_maraicher, surface_cultivee
    FROM production
    WHERE id_production = %s;
    '''
    mycursor.execute(production_sql, (production_id,))
    liste_production = mycursor.fetchone()

    return render_template('production/edit_production.html', produits=produits, maraichers=maraichers, production=liste_production)

@app.route('/production/edit', methods=['POST'])
def edit_production():
    print("Une modification d'une production a eu lieu :")

    production_id = request.form.get('id')
    produit_id = request.form.get('produit')
    maraicher_id = request.form.get('maraicher')
    surface_cultivee = request.form.get('surface')
    message='ID : ' + production_id + ', produit : ' + produit_id + ', maraicher : ' + maraicher_id + ', surface cultivée : ' + surface_cultivee
    print(message)

    mycursor = get_db().cursor()
    sql = '''
    UPDATE production
    SET id_produit=%s, id_maraicher=%s, surface_cultivee=%s
    WHERE id_production=%s;
    '''
    tuple_param = (produit_id, maraicher_id, surface_cultivee, production_id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/production/show')

@app.route('/production/delete')
def delete_production():
    print("Suppression d'une production")

    id = request.args.get('id', 0)

    mycursor = get_db().cursor()
    tuple_param = (id,)
    sql = "DELETE FROM production WHERE id_production=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    print(request.args)
    print(request.args.get('id'))

    return redirect('/production/show')

@app.route('/production/add', methods=['GET'])
def add_production_form():
    print("Affichage du formulaire d'ajout d'une production")

    mycursor = get_db().cursor()

    produit_sql='''SELECT id_produit, libelle_produit FROM produits;'''
    mycursor.execute(produit_sql)
    produits = mycursor.fetchall()
    maraicher_sql='''SELECT Id_maraicher, nom_maraicher FROM maraichers;'''
    mycursor.execute(maraicher_sql)
    maraichers = mycursor.fetchall()

    return render_template('production/add_production.html', produits=produits, maraichers=maraichers)

@app.route('/production/add', methods=['POST'])
def add_production():
    print("Ajout d'une production")

    produit_id = request.form.get('produit')
    maraicher_id = request.form.get('maraicher')
    surface_cultivee = request.form.get('surface')
    message='produit: ' + produit_id + ', maraicher: ' + maraicher_id + ', surface cultivee: ' + surface_cultivee
    print(message)

    mycursor = get_db().cursor()
    sql = "INSERT INTO production(id_produit, id_maraicher, surface_cultivee) VALUES (%s, %s, %s);"
    tuple_param = (produit_id, maraicher_id, surface_cultivee)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/production/show')

@app.route('/production/etat')
def show_production_state():
    mycursor = get_db().cursor()

    # État 2: Surface totale de production par produit
    sql_surface_totale_production_produit = '''
        SELECT produits.libelle_produit AS produit, SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN produits ON production.id_produit = produits.id_produit
        GROUP BY produits.libelle_produit;'''
    mycursor.execute(sql_surface_totale_production_produit)
    etat_surface_totale = mycursor.fetchall()

    sql_surface_par_maraicher = '''
        SELECT production.id_maraicher, maraichers.nom_maraicher AS maraicher,
        SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN maraichers ON production.id_maraicher = maraichers.id_maraicher
        GROUP BY production.id_maraicher, maraichers.nom_maraicher;
        '''
    mycursor.execute(sql_surface_par_maraicher)
    etat_surface_par_maraicher = mycursor.fetchall()

    return render_template('production/etat_production.html',
                           etat_surface_totale=etat_surface_totale,
                           etat_surface_par_maraicher=etat_surface_par_maraicher)










# ROUTES DE MICKAEL



@app.route('/vente/show')
def show_vente():
    mycursor = get_db().cursor()
    sql='''
        SELECT *
        FROM vente
        ORDER BY prix_de_vente;
    '''
    mycursor.execute(sql)
    liste_ventes = mycursor.fetchall()
    return render_template('vente/show_vente.html', vente=liste_ventes)

@app.route('/vente/add', methods=['GET'])
def add_vente():
    print('Affichage du formulaire pour saisir une vente')
    mycursor = get_db().cursor()
    # Assuming you have a query to fetch products from the database
    Semaine_sql='''SELECT * FROM semaine'''
    mycursor.execute(Semaine_sql)
    Semaine = mycursor.fetchall()
    produits_sql = '''SELECT * FROM produits;'''
    mycursor.execute(produits_sql)
    products = mycursor.fetchall()
    marches_sql='''SELECT * FROM marches;'''
    mycursor.execute(marches_sql)
    marches = mycursor.fetchall()
    Maraichers_sql='''SELECT * FROM maraichers;'''
    mycursor.execute(Maraichers_sql)
    Maraichers = mycursor.fetchall()

    return render_template('vente/add_vente.html', produits=products, maraichers=Maraichers, semaines=Semaine, marches=marches)

@app.route('/vente/delete')
def delete_vente():
    print('''suppression d'une vente''')
    id=request.args.get('id',0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql = "DELETE FROM vente WHERE id_vente = %s;"
    mycursor.execute(sql, (id,))
    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id', 0)
    return redirect('/vente/show')

@app.route('/vente/edit', methods=['GET'])
def edit_vente():
    id = request.args.get('id')

    cursor = get_db().cursor()

    # Récupérer les informations de la vente en fonction de l'ID fourni
    sql_vente = '''
        SELECT id_vente, prix_de_vente, quantitee_vendue, prix_total_de_vente, id_semaine, id_produit, id_marche, id_maraicher
        FROM vente
        WHERE id_vente = %s;'''
    cursor.execute(sql_vente, (id,))
    vente = cursor.fetchone()

    # Récupérer d'autres données nécessaires comme Semaine, produits, marches, Maraichers
    Semaine_sql = '''SELECT * FROM semaine'''
    cursor.execute(Semaine_sql)
    Semaine = cursor.fetchall()

    produits_sql = '''SELECT * FROM produits;'''
    cursor.execute(produits_sql)
    products = cursor.fetchall()

    marches_sql = '''SELECT * FROM marches;'''
    cursor.execute(marches_sql)
    marches = cursor.fetchall()

    Maraichers_sql = '''SELECT * FROM maraichers;'''
    cursor.execute(Maraichers_sql)
    Maraichers = cursor.fetchall()

    return render_template('vente/edit_vente.html', vente=vente, semaines=Semaine, produits=products,
                           marches=marches, maraichers=Maraichers)


@app.route('/vente/add', methods=['POST'])
def add_vente_post():
    try:
        print('Ajout de la vente dans le tableau')

        prix = request.form.get('Prix')
        Quantite_vendue = request.form.get('Quantitée_vendue')
        Prix_total_de_vente = request.form.get('Prix_total_de_vente')
        Semaine = request.form.get('Id_Semaine')
        produit = request.form.get('Id_produit')
        marches = request.form.get('Id_marches')
        Maraichers = request.form.get('Id_Maraicher')

        message = f"Prix total de vente: {Prix_total_de_vente}, Prix de vente: {prix}, Quantite vendue: {Quantite_vendue}, Semaine: {Semaine}, produit: {produit}, marches: {marches}, Maraichers: {Maraichers}"
        print(message)

        mycursor = get_db().cursor()
        sql = '''INSERT INTO vente(prix_de_vente, quantitee_vendue, prix_total_de_vente, id_semaine, id_produit, id_marche, id_maraicher) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        tuple_param = (prix, Quantite_vendue, Prix_total_de_vente, Semaine, produit, marches, Maraichers)
        mycursor.execute(sql, tuple_param)
        get_db().commit()

        return redirect('/vente/show')
    except Exception as e:
        print("Error:", str(e))  # Display error message for debugging
        return "Une erreur s'est produite lors de l'ajout de la vente."


@app.route('/vente/edit', methods=['POST'])
def valid_edit_vente():
    try:
        print('Modification de la vente dans le tableau')

        # Récupération des données du formulaire
        id = request.form.get('id_vente')
        prix = request.form.get('Prix')
        quantite_vendue = request.form.get('Quantitée_vendue')
        prix_total_de_vente = request.form.get('Prix_total_de_vente')
        semaine = request.form.get('Semaine')
        produit = request.form.get('produit')
        marches = request.form.get('Marché')
        maraichers = request.form.get('Maraichers')
        print(id)

        # Construction de la requête SQL pour la mise à jour
        sql = '''
            UPDATE vente 
            SET prix_de_vente = %s, quantitee_vendue = %s, prix_total_de_vente = %s, id_semaine = %s, id_produit = %s, id_marche = %s, id_maraicher = %s
            WHERE id_vente = %s
        '''
        print(prix, quantite_vendue, prix_total_de_vente, semaine, produit, marches, maraichers, id)
        mycursor = get_db().cursor()
        mycursor.execute(sql, (prix, quantite_vendue, prix_total_de_vente, semaine, produit, marches, maraichers, id,))
        get_db().commit()

        return redirect('/vente/show')
    except Exception as e:
        print("Error:", str(e))  # Affichage du message d'erreur pour le débogage
        return "Une erreur s'est produite lors de la modification de la vente."

@app.route('/vente/etat')
def show_vente_state():
    mycursor = get_db().cursor()

    # État 1: Nombre de maraîchers par produit
    sql_nombre_maraichers_produit = '''
        SELECT produits.libelle_produit, COUNT(DISTINCT maraichers.id_maraicher) AS nombre_maraichers
        FROM production
        JOIN maraichers ON production.id_maraicher = maraichers.id_maraicher
        JOIN produits ON production.id_produit = produits.id_produit
        GROUP BY produits.libelle_produit;'''
    mycursor.execute(sql_nombre_maraichers_produit)
    etat_maraichers = mycursor.fetchall()

    # État 2: Surface totale de production par produit
    sql_surface_totale_production_produit = '''
        SELECT produits.libelle_produit, SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN produits ON production.id_produit = produits.id_produit
        GROUP BY produits.libelle_produit;
    '''
    mycursor.execute(sql_surface_totale_production_produit)
    etat_surface_totale = mycursor.fetchall()

    # État 3: surface par maraicher
    sql_surface_par_maraicher = '''
        SELECT production.id_maraicher, maraichers.nom_maraicher,
        SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN maraichers ON production.id_maraicher = maraichers.id_maraicher
        GROUP BY production.id_maraicher, maraichers.nom_maraicher;
    '''
    mycursor.execute(sql_surface_par_maraicher)
    etat_surface_par_maraicher = mycursor.fetchall()

    return render_template('vente/etat_vente.html', etat_maraichers=etat_maraichers,
                           etat_surface_totale=etat_surface_totale,
                           etat_surface_par_maraicher=etat_surface_par_maraicher)






if __name__ == '__main__':
    app.run(debug=True, port=5000)
