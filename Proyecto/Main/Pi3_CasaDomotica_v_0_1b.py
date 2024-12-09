# El programa es comunicarà entre plaques mitjançanmt un diccionari on s'enviarà la part del diccionari que s'hagi modificat entre les 
#plaques. Cada x segons o minuts, s'enviarà el diccionari complert per a comprovar que estigui tot actualitzat (poder una versió següent)
# El programa compararà el diccionari anterior, mitjançant un sort i la creació d'una llista, amb l'actual i compararà si ho ha algun 
#canvi. Si són iguals ignorarà les llibreries i no farà res. Si no és igual, realitzarà l'acció que hagi de fer per a actualitzar
#l'estat dels components.
# També o en substitució, l'alterrnativa seria que agafés una variable buida en la que si ho ha un canvi en algún sensor o en alguna 
#acció cap a un actuador, aquesta variable estarà plena amb el canvi a realitzar i actuarà en consequwencia el sistema, per exemple amb una
#referència del q s'està modificant.

#estat_casa = { llum_menjador : {llums,5}, llum_cuina : {llums,0}, sensor_gas : {gas,0}, estat_alarma : {alarma,{"armada","desactivada"}}}
#estat_casa = { llum : {menjador : 5}, llum : {cuina : 0}, gas : {mq135 : 0}, {alarma : {alarma : {"armada","desactivada"}}}
#keys_estat_casa = { llum : "llum", gas : "gas", alarma : "alarma"}
estat_casa = { llum_menjador : 5, llum_cuina : 0, gas_cuina : 0, alarma_general : {"armada","desactivada"}}
objecte_casa = { llum_menjador : pcaLM, llum_cuina : pcaLC, gas_cuina : mq1351, alarma_general : alarmaG}

estat_casa = { "llum_menjador" : {"estat" : 5, "objecte" : llum_M}, "alarmaGeneral": {"estat": "activada", "armada" : True, "objecte": "alarmaGeneral"},

#En una primera versió, enviarem només el diccionari dinàmic, la part del diccionari estatic la posarem en un diccionari intern de cada placa.


#######
estat_complet = {
    "llum": {"estat": "ON", "objecte": "menjador"},
    "gas": {"estat": "OFF", "objecte": "cuina"},
    "alarma": {"estat": "activada", "objecte": "dormitori"},
}

# Accés fàcil a tots els atributs
for clau, dades in estat_complet.items():
    print(f"{clau.capitalize()} està {dades['estat']} a {dades['objecte']}")
-> Llum està ON a menjador
Gas està OFF a cuina
Alarma està activada a dormitori

##
# Canviar l'estat de la llum
estat_complet["llum"]["estat"] = "OFF"

# Afegir un nou atribut
estat_complet["llum"]["intensitat"] = 75

# Resultat
print(estat_complet["llum"])
-> {'estat': 'OFF', 'objecte': 'menjador', 'intensitat': 75}


######
estat_casa[llum_menjador] = 3

if lum_menjador:
    pca.encen("menjador",3)   
    
envia = {llum_cuina : 6}

estat_casa[llum_cuina] = 6
