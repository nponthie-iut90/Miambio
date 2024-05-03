from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)


# Sujet 3

produits = [
    {'id': 1, 'nomproduit': 'Pain Blanc', 'indiceglycémiqueproduit': '75', 'image': 'Painblanc.jpeg'},
    {'id': 2, 'nomproduit': 'Pomme de terre cuite', 'indiceglycémiqueproduit': '85', 'image': 'PommeTerre.jpeg'},
    {'id': 3, 'nomproduit': 'Frites', 'indiceglycémiqueproduit': '75', 'image': 'Frites.jpeg'},
    {'id': 4, 'nomproduit': 'Brocoli', 'indiceglycémiqueproduit': '30', 'image': 'Brocoli.jpeg'},
    {'id': 5, 'nomproduit': 'Salade', 'indiceglycémiqueproduit': '15', 'image': 'Salade.jpeg'},
    {'id': 6, 'nomproduit': 'Tofu', 'indiceglycémiqueproduit': '15', 'image': 'Tofu.jpeg'},
    {'id': 7, 'nomproduit': 'couscous', 'indiceglycémiqueproduit': '60', 'image': 'Couscous.jpeg'},
]


@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/produit/show')
def show_produit():
    # print(articles)
    return render_template('/produit/show_produit.html', produits=produits)

@app.route('/produit/add', methods=['GET'])
def add_produit():
    return render_template('produit/add_produit.html', produits=produits)

@app.route('/produit/add', methods=['POST'])
def valid_add_produit():
    id = request.form.get('id', '')
    nomproduit = request.form.get('nomproduit', '')
    produit_id = request.form.get('produit_id')
    indiceglycémiqueproduit = request.form.get('indiceglycémiqueproduit', '')
    image = request.form.get('image', '')
    message = u'produit modifié , id:'+id + '---- produit_id :' + produit_id + ' ----nomproduit :' + nomproduit + ' - indiceglycémiqueproduit:'+  indiceglycémiqueproduit + ' - image:' + image + + u' ------ pour le produit d identifiant :' + id
    print(message)
    flash(message, 'alert-success')
    return redirect('/produit/show')

@app.route('/produit/delete', methods=['GET'])
def delete_produit():
    id = request.args.get('id', '')
    message=u'un produit supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/produit/show')

@app.route('/produit/edit', methods=['GET'])
def edit_produit():
    id = request.args.get('id', '')
    id=int(id)
    produits= produits[id-1]
    return render_template('/produit/edit_produit.html', produits=produits)

@app.route('/produit/edit', methods=['POST'])
def valid_edit_produit():
    id = request.form.get('id', '')
    nomproduit = request.form.get('nomproduit', '')
    produit_id = request.form.get('produit_id')
    indiceglycémiqueproduit = request.form.get('indiceglycémiqueproduit', '')
    image = request.form.get('image', '')
    message = u'produit modifié , id:'+id + '---- produit_id :' + produit_id + ' ----nomproduit :' + nomproduit + ' - indiceglycémiqueproduit:'+  indiceglycémiqueproduit + ' - image:' + image + + u' ------ pour le produit d identifiant :' + id
    print(message)  
    flash(message, 'alert-success')
    return redirect('/produit/show')

# routes de Nathan
@app.route('/production/show')
def show_production():
    mycursor = get_db().cursor()
    sql = '''
    SELECT production.Id_production, produits.Libellé_produit, maraichers.Nom_maraicher,
     production.surface_cultivee
    FROM production
    JOIN maraichers ON production.Id_maraicher = maraichers.Id_maraicher
    JOIN produits ON production.Id_produit = produits.Id_produit;
    '''
    mycursor.execute(sql)
    liste_production = mycursor.fetchall()

    return render_template('production/show_production.html', production=liste_production)


@app.route('/production/edit', methods=['GET'])
def show_edit_production_form():
    print("affichage du formulaire de modification d'une production")
    print(request.args)
    print(request.args.get('id'))

    mycursor = get_db().cursor()

    production_id = request.args.get('id', 0)

    produits_sql = '''SELECT Id_produit, Libellé_produit FROM produits;'''
    mycursor.execute(produits_sql)
    produits = mycursor.fetchall()
    maraichers_sql = '''SELECT Id_maraicher, Nom_maraicher FROM maraichers;'''
    mycursor.execute(maraichers_sql)
    maraichers = mycursor.fetchall()

    production_sql = '''
    SELECT Id_production AS id, Id_produit, Id_maraicher, surface_cultivee
    FROM production
    WHERE Id_production = %s;
    '''
    mycursor.execute(production_sql, (production_id,))
    liste_production = mycursor.fetchone()

    return render_template('production/edit_production.html', produits=produits, maraichers=maraichers,
                           production=liste_production)


@app.route('/production/edit', methods=['POST'])
def edit_production():
    print("une modification d'une production a eu lieu:")

    production_id = request.form.get('id')
    produit_id = request.form.get('produit')
    maraicher_id = request.form.get('maraicher')
    surface_cultivee = request.form.get('surface')
    message = ('id: ' + production_id + ', produit: ' + produit_id + ', maraicher: ' + maraicher_id +
               ', surface cultivee: ' + surface_cultivee)
    print(message)

    mycursor = get_db().cursor()
    sql = '''
    UPDATE production
    SET Id_produit=%s, Id_maraicher=%s, surface_cultivee=%s
    WHERE Id_production=%s;
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
    sql = "DELETE FROM production WHERE Id_production=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    print(request.args)
    print(request.args.get('id'))

    return redirect('/production/show')


@app.route('/production/add', methods=['GET'])
def add_production_form():
    print("affichage du formulaire d'ajout d'une production")

    mycursor = get_db().cursor()

    produit_sql = '''SELECT Id_produit, Libellé_produit FROM produits;'''
    mycursor.execute(produit_sql)
    produits = mycursor.fetchall()
    maraicher_sql = '''SELECT Id_maraicher, Nom_maraicher FROM maraichers;'''
    mycursor.execute(maraicher_sql)
    maraichers = mycursor.fetchall()

    return render_template('production/add_production.html', produits=produits, maraichers=maraichers)


@app.route('/production/add', methods=['POST'])
def add_production():
    print("ajout d'une production")

    produit_id = request.form.get('produit')
    maraicher_id = request.form.get('maraicher')
    surface_cultivee = request.form.get('surface')
    message = 'produit: ' + produit_id + ', maraicher: ' + maraicher_id + ', surface cultivee: ' + surface_cultivee
    print(message)

    mycursor = get_db().cursor()
    sql = "INSERT INTO production (Id_produit, Id_maraicher, surface_cultivee) VALUES (%s, %s, %s);"
    tuple_param = (produit_id, maraicher_id, surface_cultivee)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/production/show')


@app.route('/production/etat')
def show_production_state():
    mycursor = get_db().cursor()

    # État 1: Nombre de maraîchers par produit
    sql_nombre_maraichers_produit = '''
        SELECT produits.Libellé_produit AS produit, COUNT(DISTINCT maraichers.Id_maraicher) AS nombre_maraichers
        FROM production
        JOIN maraichers ON production.Id_maraicher = maraichers.Id_maraicher
        JOIN produits ON production.Id_produit = produits.Id_produit
        GROUP BY produits.Libellé_produit;'''
    mycursor.execute(sql_nombre_maraichers_produit)
    etat_maraichers = mycursor.fetchall()

    # État 2: Surface totale de production par produit
    sql_surface_totale_production_produit = '''
        SELECT produits.Libellé_produit AS produit, SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN produits ON production.Id_produit = produits.Id_produit
        GROUP BY produits.Libellé_produit;'''
    mycursor.execute(sql_surface_totale_production_produit)
    etat_surface_totale = mycursor.fetchall()

    sql_surface_par_maraicher = '''
        SELECT production.Id_maraicher, maraichers.Nom_maraicher AS maraicher,
        SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN maraichers ON production.Id_maraicher = maraichers.Id_maraicher
        GROUP BY production.Id_maraicher, maraichers.Nom_maraicher;
        '''
    mycursor.execute(sql_surface_par_maraicher)
    etat_surface_par_maraicher = mycursor.fetchall()

    return render_template('production/etat_production.html', etat_maraichers=etat_maraichers,
                           etat_surface_totale=etat_surface_totale,
                           etat_surface_par_maraicher=etat_surface_par_maraicher)

# ROUTES D'ANNA

@app.route('/recolte/show')
def show_recolte():
    mycursor = get_db().cursor()
    sql='''
 SELECT  Id_recolte AS id,  quantite_recoltee AS qtRecolte, Id_Semaine AS semaine, Id_produit AS id_produit, Id_Maraicher AS id_maraicher
 FROM recolte
    ORDER BY id;
    '''
    mycursor.execute(sql)
    recoltes = mycursor.fetchall()
    return render_template('recolte/show_recolte.html', recoltes=recoltes)

@app.route('/recolte/add', methods=['GET'])
def add_recolte():
    print('''affichage du formulaire pour saisir une récolte''')
    mycursor = get_db().cursor()
    sql='''SELECT * FROM Semaine
    '''
    mycursor.execute(sql)
    semaines = mycursor.fetchall()

    sql='''SELECT * FROM Produits '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''SELECT * FROM Maraichers '''
    mycursor.execute(sql)
    maraichers = mycursor.fetchall()

    return render_template('recolte/add_recolte.html' , semaines=semaines , produits=produits , maraichers=maraichers)


@app.route('/recolte/edit', methods=['GET'])
def edit_recolte():
    print('''Modifier une récolte''')
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql=''' SELECT  Id_recolte AS id,  quantite_recoltee AS qtRecolte, Id_Semaine AS semaine, Id_produit AS id_produit, Id_Maraicher AS id_maraicher
 FROM recolte
    WHERE Id_Recolte=%s;'''
    mycursor.execute(sql,id)
    recolte = mycursor.fetchone()

    mycursor = get_db().cursor()
    sql='''SELECT * FROM Semaine
    '''
    mycursor.execute(sql)
    semaines = mycursor.fetchall()

    sql='''SELECT * FROM Produits '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''SELECT * FROM Maraichers '''
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
    tuple_param=(qtRecolte,semaine,id_produit,id_maraicher)
    sql="INSERT INTO recolte(Id_recolte, quantite_recoltee, Id_Semaine, Id_produit, Id_Maraicher) VALUES (NULL, %s, %s, %s, %s);"
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
    sql="UPDATE recolte SET quantite_recoltee = %s, Id_Semaine=%s,  Id_produit=%s, Id_Maraicher= %s WHERE Id_recolte=%s;"
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

# LES ROUTES DE SIMONE

@app.route('/')
@app.route('/produit/show')
def show_produit():
    mycursor = get_db().cursor()
    sql='''
 SELECT  Id_produit AS id,  libelle_produit AS lbproduit, Id_categorie_produit AS cgid
    FROM Produits
    ORDER BY id;
    '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()
    return render_template('produit/show_produit.html', produits=produits)

@app.route('/produit/add', methods=['GET'])
def add_produit():
    mycursor = get_db().cursor()
    sql = '''Select * from categorie_produit'''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()
    return render_template('produit/add_produit.html',categories=categorie)



@app.route('/produit/add', methods=['POST'])
def valid_add_produit():
    print('''ajout du produit dans le tableau''')
    lbproduit = request.form.get('lbproduit')
    Id_categorie_produit = request.form.get('Id_categorie_produit')
    message = u' produit ajouté , lbproduit:' + lbproduit + ' - Id_categorie_produit:' + Id_categorie_produit
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(lbproduit,Id_categorie_produit)
    sql = "INSERT INTO Produits(libelle_produit,Id_categorie_produit,Id_produit) VALUES (%s,%s,NULL)"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/produit/show')
@app.route('/produit/delete')
def delete_produit():
    print('''suppression d'un produit''')
    id = request.args.get('id', None)
    verifier = []
    mycursor = get_db().cursor()
    sql="SELECT * FROM recolte WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM produit WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM periode_de_vente WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM Vente WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    print(verifier)
    if len(verifier) ==0 :
        sql = "DELETE FROM Produits WHERE Id_produit=%s;"
        mycursor.execute(sql, id)
        get_db().commit()
    else:
        print("ce n'est pas possible")
    print(f'''le produit dans le tableau {id} a été supprimer''' )
    return redirect('/produit/show')

@app.route('/produit/edit', methods=['GET'])
def edit_produit():
    print('''affichage du formulaire pour modifier un étudiant''')
    id=request.args.get('id')
    mycursor = get_db().cursor()

    sql = '''
     SELECT  Id_produit AS id,  libelle_produit AS lbproduit, Id_categorie_produit AS cgid
        FROM Produits
        WHERE Id_produit = %s
        '''
    mycursor.execute(sql,id)
    produit = mycursor.fetchone()
    sql='''SELECT * FROM categorie_produit'''
    mycursor.execute(sql)
    categories = mycursor.fetchall()
    return render_template('produit/edit_produit.html', produit=produit ,  categories=categories)

@app.route('/produit/edit', methods=['POST'])
def valid_edit_produit():
    print('''affichage du formulaire pour modifier un étudiant''')
    id=request.form.get('id')
    categorie = request.form.get('Id_categorie_produit')
    lbproduit = request.form.get('lbproduit')
    print(id)
    print(categorie)

    mycursor = get_db().cursor()
    sql = '''UPDATE Produits SET libelle_produit=%s , Id_categorie_produit=%s WHERE Id_produit = %s'''
    mycursor.execute(sql,(lbproduit,categorie,id))
    get_db().commit()
    return redirect('/produit/show')


# Route de Mickaël

@app.route('/')
@app.route('/vente/show')
def show_vente():
    mycursor = get_db().cursor()
    sql='''SELECT id_Vente AS id, Prix_de_vente AS prix, Quantitée_vendue AS Quantitée_vendue, Prix_total_de_vente AS Prix_total, id_Semaine AS Semaine, id_produit AS produit, id_Marché AS Marché, id_Maraicher AS Maraichers
    FROM vente
    ORDER BY Prix_de_vente;'''
    mycursor.execute(sql)
    liste_ventes = mycursor.fetchall()
    return render_template('vente/show_vente.html', vente=liste_ventes)

@app.route('/vente/add', methods=['GET'])
def add_vente():
    print('Affichage du formulaire pour saisir une vente')
    mycursor = get_db().cursor()
    # Assuming you have a query to fetch products from the database
    Semaine_sql='''SELECT * FROM Semaine'''
    mycursor.execute(Semaine_sql)
    Semaine = mycursor.fetchall()
    produits_sql = '''SELECT * FROM Produits;'''
    mycursor.execute(produits_sql)
    products = mycursor.fetchall()
    Marché_sql='''SELECT * FROM Marché;'''
    mycursor.execute(Marché_sql)
    Marché = mycursor.fetchall()
    maraichers_sql='''SELECT * FROM maraichers;'''
    mycursor.execute(maraichers_sql)
    Maraichers = mycursor.fetchall()

    return render_template('vente/add_vente.html', produits=products, Maraichers=Maraichers, Semaines=Semaine, Marché=Marché)

@app.route('/vente/delete')
def delete_vente():
    print('''suppression d'une vente''')
    id=request.args.get('id',0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql = "DELETE FROM vente WHERE Id_Vente = %s;"
    mycursor.execute(sql, (id,))
    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id', 0)
    return redirect('/vente/show')

@app.route('/vente/edit', methods=['GET'])
def edit_vente():
    mycursor = get_db().cursor()
    print('''affichage du formulaire pour modifier une vente''')
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id')
    Semaine_sql='''SELECT * FROM Semaine'''
    mycursor.execute(Semaine_sql)
    Semaine = mycursor.fetchall()
    produits_sql = '''SELECT * FROM Produits;'''
    mycursor.execute(produits_sql)
    products = mycursor.fetchall()
    Marché_sql='''SELECT * FROM Marché;'''
    mycursor.execute(Marché_sql)
    Marché = mycursor.fetchall()
    maraichers_sql='''SELECT * FROM maraichers;'''
    mycursor.execute(maraichers_sql)
    Maraichers = mycursor.fetchall()
    sql = '''SELECT id_Vente AS id, Prix_de_vente AS prix, Quantitée_vendue AS Quantitée_vendue, Prix_total_de_vente AS Prix_total_de_vente, id_Semaine AS Semaine, id_produit AS Produit, id_Marché AS Marché, id_Maraicher AS Maraichers
    FROM vente
    WHERE id_Vente = %s;'''  # Suppression de la virgule après 'id'
    tuple_param = (id,)  # Ajout de la virgule pour former un tuple avec un seul élément
    mycursor.execute(sql, tuple_param)  # Utilisation du tuple_param dans execute()
    liste_ventes = mycursor.fetchone()
    print(liste_ventes)

    return render_template('vente/edit_vente.html', vente=liste_ventes, Semaines=Semaine, produits=products, Marché=Marché, Maraichers=Maraichers)


@app.route('/vente/add', methods=['POST'])
def valid_add_vente():
    print('Ajout de la vente dans le tableau')

    Prix = request.form.get('Prix')
    Quantitée_vendue = request.form.get('Quantitée_vendue')
    Prix_total_de_vente = request.form.get('Prix_total_de_vente')
    Semaine = request.form.get('Semaine')
    produit = request.form.get('produit')
    Marché = request.form.get('Marché')
    Maraichers = request.form.get('Maraichers')

    message = f"Prix total de vente: {Prix_total_de_vente}, Prix de vente: {Prix}, Quantite vendue: {Quantitée_vendue}, Semaine: {Semaine}, produit: {produit}, Marché: {Marché}, Maraichers: {Maraichers}"
    print(message)

    mycursor = get_db().cursor()
    sql = "INSERT INTO vente(Prix_de_vente, Quantitée_vendue, Prix_total_de_vente, id_Semaine, id_produit, id_Marché, id_Maraicher) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    tuple_param = (Prix, Quantitée_vendue, Prix_total_de_vente, Semaine, produit, Marché, Maraichers)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/vente/show')

@app.route('/vente/edit', methods=['POST'])
def valid_edit_vente():
    try:
        print('Modification de la vente dans le tableau')
        print(request.form)  # Vérification des données du formulaire à des fins de débogage

        # Récupération des données du formulaire
        id = request.form.get('id')
        Prix = request.form.get('Prix')
        Quantitée_vendue = request.form.get('Quantitée_vendue')
        Prix_total_de_vente = request.form.get('Prix_total_de_vente')
        Semaine = request.form.get('Semaine')
        produit = request.form.get('produit')
        Marché = request.form.get('Marché')
        Maraichers = request.form.get('Maraichers')

        # Construction du message avec vérification des valeurs None
        message = f"Prix total de vente: {Prix_total_de_vente if Prix_total_de_vente is not None else 'N/A'}, Prix de vente: {Prix if Prix is not None else 'N/A'}, Quantité vendue: {Quantitée_vendue if Quantitée_vendue is not None else 'N/A'}, Semaine: {Semaine if Semaine is not None else 'N/A'}, produit: {produit if produit is not None else 'N/A'}, Marché: {Marché if Marché is not None else 'N/A'}, Maraichers: {Maraichers if Maraichers is not None else 'N/A'}, id: {id if id is not None else 'N/A'}"
        print(message)

        mycursor = get_db().cursor()
        tuple_param = (Prix, Quantitée_vendue, Prix_total_de_vente, Semaine, produit, Marché, Maraichers, id)
        sql = "UPDATE vente SET Prix_de_vente = %s, Quantitée_vendue = %s, Prix_total_de_vente = %s, id_Semaine = %s, id_produit = %s, id_Marché = %s, id_Maraicher = %s WHERE Id_Vente = %s;"

        mycursor.execute(sql, tuple_param)
        get_db().commit()
        return redirect('/vente/show')
    except Exception as e:
        print("Error:", str(e))  # Affichage du message d'erreur pour le débogage
        return "Une erreur s'est produite lors de la modification de la vente."



if __name__ == '__main__':
    app.run(debug=True, port=5000)





if __name__ == '__main__':
    app.run()
