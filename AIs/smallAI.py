#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################# PRE-DEFINED CONSTANTS ############################################# ############################################ CONSTANTES PRÉ-DÉFINIES ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    In this section, you will find some pre-defined constants that are needed for the game                      #    Dans cette section, vous trouvez des constantes pré-définies nécessaires pour la partie                     #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    TEAM_NAME : string                                                                                          #    TEAM_NAME : string                                                                                          #
#    ------------------                                                                                          #    ------------------                                                                                          #
#                                                                                                                #                                                                                                                #
#        This constant represents your name as a team                                                            #        Cette constante représente le nom de votre équipe                                                       #
#        Please change the default value to a string of your choice                                              #        Veuillez en changer la valeur par une chaîne de caractères de votre choix                               #
#                                                                                                                #                                                                                                                #
#    MOVE_XXX : char                                                                                             #    MOVE_XXX : char                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        The four MOVE_XXX constants represent the possible directions where to move                             #        Les quatre constantes MOVE_XXX représentent les directions possibles où se déplacer                     #
#        The "turn" function should always return one of these constants                                         #        La fonction "turn" doit toujours renvoyer l'une d'entre elles                                           #
#        Please do not edit them (any other value will be considered incorrect and thus ignored)                 #        Merci de ne pas les éditer (toute autre valeur sera considérée comme incorrecte et sera ignorée)        #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

TEAM_NAME = "Greedy"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###################################################################################################################################################################################################################################
########################################### SPACE FOR FREE EXPRESSION ########################################### ############################################ ZONE D'EXPRESSION LIBRE ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    In this file, you will two functions: "preprocessing" and "turn"                                            #    Dans ce fichier, vous trouverez deux fonctions : "preprocessing" et "turn"                                  #
#    You need to edit these functions to create your PyRat program                                               #    Vous devez éditer ces fonctions pour réaliser votre programme PyRat                                         #
#    However, you are not limited to them, and you can write any Python code in this file                        #    Toutefois, vous n'êtes pas limité(e), et vous pouvez écrire n'importe quel code Python dans ce fichier      #
#    Please use the following space to write your additional constants, variables, functions...                  #    Merci d'utiliser l'espace ci-dessous pour écrire vos constantes, variables, fonctions...                    #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
# Useful imports #
##################

import heapq

###################################################################################################################################################################################################################################
# Transforms a pair of locations into a move going from the first to the second #
#################################################################################

def locationsToMove (location1, location2) :
    
    # Depends on the difference
    difference = (location1[0] - location2[0], location1[1] - location2[1])
    if difference == (1, 0) :
        return MOVE_LEFT
    elif difference == (-1, 0) :
        return MOVE_RIGHT
    elif difference == (0, -1) :
        return MOVE_UP
    elif difference == (0, 1) :
        return MOVE_DOWN
    else :
        raise Exception("Invalid location provided")

###################################################################################################################################################################################################################################
# Dijkstra's algorithm to compute the shortest paths from the initial locations to all the nodes #
# Returns for each location the previous one that leads to the shortest path                     #
##################################################################################################

def dijkstra (mazeMap, initialLocation) :
    
    # We initialize the min-heap with the source node
    # Distances and routes are updated once the nodes are visited for the first time
    # The temporary values are stored in the min-heap
    minHeap = [(0, initialLocation, None)]
    distances = {}
    routes = {}
    
    # Main loop
    while len(minHeap) != 0 :
        (distance, location, predecessor) = heapq.heappop(minHeap)
        if location not in distances :
            distances[location] = distance
            routes[location] = predecessor
            for neighbor in mazeMap[location] :
                newDistanceToNeighbor = distance + mazeMap[location][neighbor]
                heapq.heappush(minHeap, (newDistanceToNeighbor, neighbor, location))
    
    # Result
    return (routes, distances)
    
###################################################################################################################################################################################################################################
# Takes as an input the result of Dijkstra's algorithm        #
# Returns the sequence of nodes from sourceNode to targetNode #
###############################################################

def routesToPath (routes, targetNode) :
    
    # Recursive reconstruction
    if not targetNode :
        return []
    elif targetNode in routes :
        return routesToPath(routes, routes[targetNode]) + [targetNode]
    else :
        raise Exception("Impossible to reach target")

###################################################################################################################################################################################################################################
# Returns the sequence of moves in the maze associated to a path in the graph #
###############################################################################

def pathToMoves (path) :
    
    # Recursive reconstruction
    if len(path) <= 1 :
        return []
    else :
        return [locationsToMove(path[0], path[1])] + pathToMoves(path[1:])

###################################################################################################################################################################################################################################
# Function that finds the closest piece of cheese #
###################################################

def findClosestPieceOfCheese (distances, piecesOfCheese) :
    
    # We return the cheese associated with the minimum distance
    distancesToCheese = {cheese : distances[cheese] for cheese in piecesOfCheese}
    return min(distancesToCheese, key=distancesToCheese.get)

###################################################################################################################################################################################################################################
############################################# PREPROCESSING FUNCTION ############################################ ########################################### FONCTION DE PRÉ-TRAITEMENT ##########################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function is executed once at the very beginning of the game                                            #    Cette fonction est exécutée une unique fois au tout début de la partie                                      #
#    It allows you to make some computations before the players are allowed to move                              #    Vous pouvez y effectuer des calculs avant que les joueurs ne puissent commencer à bouger                    #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #
#    ---------------------------------------------------------                                                   #    ---------------------------------------------------------                                                   #
#                                                                                                                #                                                                                                                #
#        Map of the maze as a data structure                                                                     #        Structure de données représentant la carte du labyrinthe                                                #
#        mazeMap[x] gives you the neighbors of cell x                                                            #        mazeMap[x] renvoie les voisins de la case x                                                             #
#        mazeMap[x][y] gives you the weight of the edge linking cells x and y                                    #        mazeMap[x][y] renvoie le poids de l'arête reliant les cases x et y                                      #
#        if mazeMap[x][y] is undefined, there is no edge between cells x and y                                   #        Si mazeMap[x][y] n'est pas défini, les cases x et y ne sont pas reliées par une arête                   #
#                                                                                                                #                                                                                                                #
#    mazeWidth : int                                                                                             #    mazeWidth : int                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Width of the maze, in number of cells                                                                   #        Largeur du labyrinthe, en nombre de cases                                                               #
#                                                                                                                #                                                                                                                #
#    mazeHeight : int                                                                                            #    mazeHeight : int                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Height of the maze, in number of cells                                                                  #        Hauteur du labyrinthe, en nombre de cases                                                               #
#                                                                                                                #                                                                                                                #
#    playerLocation : pair(int, int)                                                                             #    playerLocation : pair(int, int)                                                                             #
#    -------------------------------                                                                             #    -------------------------------                                                                             #
#                                                                                                                #                                                                                                                #
#        Initial location of your character in the maze                                                          #        Emplacement initial de votre personnage dans le labyrinthe                                              #
#        It is a pair (line, column), with (0, 0) being the top-left cell in the maze                            #        C'est une paire (ligne, colonne), (0, 0) étant la case en haut à gauche du labyrinthe                   #
#        playerLocation[0] gives you your current line                                                           #        playerLocation[0] renvoie votre ligne actuelle                                                          #
#        playerLocation[1] gives you your current column                                                         #        playerLocation[1] renvoie votre colonne actuelle                                                        #
#        mazeMap[playerLocation] gives you the cells you can access directly                                     #        mazeMap[playerLocation] renvoie les cases auxquelles vous pouvez accéder directement                    #
#                                                                                                                #                                                                                                                #
#    opponentLocation : pair(int, int)                                                                           #    opponentLocation : pair(int, int)                                                                           #
#    ---------------------------------                                                                           #    ---------------------------------                                                                           #
#                                                                                                                #                                                                                                                #
#        Initial location opponent's character in the maze                                                       #        Emplacement initial du personnage de votre adversaire dans le labyrinthe                                #
#        The opponent's location can be used just as playerLocation                                              #        La position de l'adversaire peut être utilisée comme pour playerLocation                                #
#        If you are playing in single-player mode, this variable is undefined                                    #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
#    piecesOfCheese : list(pair(int, int))                                                                       #    piecesOfCheese : list(pair(int, int))                                                                       #
#    -------------------------------------                                                                       #    -------------------------------------                                                                       #
#                                                                                                                #                                                                                                                #
#        Locations of all pieces of cheese in the maze                                                           #        Emplacements des morceaux de fromage dans le labyrinthe                                                 #
#        The locations are given in no particular order                                                          #        Les emplacements sont données dans un ordre quelconque                                                  #
#        As for the players locations, these locations are pairs (line, column)                                  #        Comme pour les positions des joueurs, ces emplacements sont des paires (ligne, colonne)                 #
#                                                                                                                #                                                                                                                #
#    timeAllowed : float                                                                                         #    timeAllowed : float                                                                                         #
#    -------------------                                                                                         #    -------------------                                                                                         #
#                                                                                                                #                                                                                                                #
#        Time that is allowed for preprocessing, in seconds                                                      #        Temps alloué pour le pré-traitement, en secondes                                                        #
#        After this time, players will have the right to move                                                    #        Après ce temps, les joueurs pourront commencer à bouger                                                 #
#        If your preprocessing is too long, you will still finish it                                             #        Si votre pré-traitement est trop long, vous terminerez quand même son exécution                         #
#        However, it will not prevent your opponent from moving                                                  #        Toutefois, cela n'empêchera pas votre adversaire de bouger                                              #
#        Make sure to finish your preprocessing within the allowed time                                          #        Assurez vous de terminer votre pré-traitement dans le temps imparti                                     #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function does not return anything                                                                      #    Cette fonction ne renvoie rien                                                                              #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
    
    # Nothing to do
    pass
    
###################################################################################################################################################################################################################################
################################################# TURN FUNCTION ################################################# ############################################ FONCTION DE TOUR DE JEU ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    Once the preprocessing is over, the game starts and players can start moving                                #    Une fois le pré-traitement terminé, la partie démarre et les joueurs peuvent commencer à bouger             #
#    The "turn" function is called at regular times                                                              #    La fonction "turn" est appelée à intervalles réguliers                                                      #
#    You should determine here your next move, given a game configuration                                        #    Vous devez déterminer ici votre prochain mouvement, étant donnée une configuration du jeu                   #
#    This decision will then be applied, and your character will move in the maze                                #    Cette décision sera ensuite appliquée, et votre personnage se déplacera dans le labyrinthe                  #
#    Then, the "turn" function will be called again with the new game configuration                              #    Ensuite, la fonction "turn" sera appelée à nouveau, avec la nouvelle configuration du jeu                   #
#    This process is repeated until the game is over                                                             #    Ce processus est répété jusqu'à la fin de la partie                                                         #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #
#    ---------------------------------------------------------                                                   #    ---------------------------------------------------------                                                   #
#                                                                                                                #                                                                                                                #
#        Same argument as for the "preprocessing" function                                                       #        Même paramètre que pour la fonction "preprocessing"                                                     #
#        The value of mazeMap does not change between two calls of function "turn"                               #        La valeur de mazeMap ne change pas d'un appel à l'autre de la fonction "turn"                           #
#                                                                                                                #                                                                                                                #
#    mazeWidth : int                                                                                             #    mazeWidth : int                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        Same argument as for the "preprocessing" function                                                       #        Même paramètre que pour la fonction "preprocessing"                                                     #
#        The value of mazeWidth does not change between two calls of function "turn"                             #        La valeur de mazeWidth ne change pas d'un appel à l'autre de la fonction "turn"                         #
#                                                                                                                #                                                                                                                #
#    mazeHeight : int                                                                                            #    mazeHeight : int                                                                                            #
#    ----------------                                                                                            #    ----------------                                                                                            #
#                                                                                                                #                                                                                                                #
#        Same argument as for the "preprocessing" function                                                       #        Même paramètre que pour la fonction "preprocessing"                                                     #
#        The value of mazeHeight does not change between two calls of function "turn"                            #        La valeur de mazeHeight ne change pas d'un appel à l'autre de la fonction "turn"                        #
#                                                                                                                #                                                                                                                #
#    playerLocation : pair(int, int)                                                                             #    playerLocation : pair(int, int)                                                                             #
#    -------------------------------                                                                             #    -------------------------------                                                                             #
#                                                                                                                #                                                                                                                #
#        Current location of your character in the maze                                                          #        Emplacement actuel de votre personnage dans le labyrinthe                                               #
#        At the first call of function "turn", it will be your initial location                                  #        Au premier appel de la fonction "turn", ce sera votre emplacement initial                               #
#                                                                                                                #                                                                                                                #
#    opponentLocation : pair(int, int)                                                                           #    opponentLocation : pair(int, int)                                                                           #
#    ---------------------------------                                                                           #    ---------------------------------                                                                           #
#                                                                                                                #                                                                                                                #
#        Current location of your opponent's character in the maze                                               #        Emplacement actuel de votre personnage dans le labyrinthe                                               #
#        At the first call of function "turn", it will be your opponent's initial location                       #        Au premier appel de la fonction "turn", ce sera votre emplacement initial                               #
#        If you are playing in single-player mode, this variable is undefined                                    #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
#    playerScore : float                                                                                         #    playerScore: float                                                                                          #
#    -------------------                                                                                         #    ------------------                                                                                          #
#                                                                                                                #                                                                                                                #
#        Your current score when the turn begins                                                                 #        Votre score actuel au début du tour                                                                     #
#        It is initialized at 0, and increases by 1 when you eat a piece of cheese                               #        Il est initialisé à 0, et augmente de 1 pour chaque morceau de fromage mangé                            #
#        If you reach the same piece of cheese as your opponent at the same moment, it is worth 0.5 points       #        Si vous arrivez sur le même morceau de fromage que votre adversaire au même moment, il vaut 0.5 points  #
#        If you are playing in single-player mode, this variable is undefined                                    #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
#    opponentScore : float                                                                                       #    opponentScore: float                                                                                        #
#    ---------------------                                                                                       #    --------------------                                                                                        #
#                                                                                                                #                                                                                                                #
#        The score of your opponent when the turn begins                                                         #        Le score de votre adversaire au début du tour                                                           #
#                                                                                                                #                                                                                                                #
#    piecesOfCheese : list(pair(int, int))                                                                       #    piecesOfCheese : list(pair(int, int))                                                                       #
#    -------------------------------------                                                                       #    -------------------------------------                                                                       #
#                                                                                                                #                                                                                                                #
#        Locations of all remaining pieces of cheese in the maze                                                 #        Emplacements des morceaux de fromage restants dans le labyrinthe                                        #
#        The list is updated at every call of function "turn"                                                    #        La liste est mise à jour à chaque appel de la fonction "turn"                                           #
#                                                                                                                #                                                                                                                #
#    timeAllowed : float                                                                                         #    timeAllowed : float                                                                                         #
#    -------------------                                                                                         #    -------------------                                                                                         #
#                                                                                                                #                                                                                                                #
#        Time that is allowed for determining the next move to perform, in seconds                               #        Temps alloué pour le calcul du prochain mouvement, en secondes                                          #
#        After this time, the decided move will be applied                                                       #        Après ce temps, le mouvement choisi sera appliqué                                                       #
#        If you take too much time, you will still finish executing your code, but you will miss the deadline    #        Si vous prenez trop de temps, votre code finira quand-même son excution, mais vous raterez le timing    #
#        Your move will then be considered the next time PyRat checks for players decisions                      #        Votre mouvement sera alors considéré la prochaine fois que PyRat vérifiera les décisions des joueurs    #
#        However, it will not prevent your opponent from moving if he respected the deadline                     #        Toutefois, cela n'empêchera pas votre adversaire de bouger s'il a respecté le timing                    #
#        Make sure to finish your computations within the allowed time                                           #        Assurez vous de terminer vos calculs dans le temps imparti                                              #
#        Also, save some time to ensure that PyRat will receive your decision before the deadline                #        Aussi, gardez un peu de temps pour garantir que PyRat recevra votre decision avant la fin du temps      #
#        If you are playing in synchronous mode, this variable is undefined                                      #        Si vous jouez en mode synchrone, cette variable n'est pas définie                                       #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    This function should return one of the following constants: MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP       #    Cette fonction renvoie l'une des constantes suivantes : MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP           #
#    The returned constant represents the move you decide to perform: down, left, right, up                      #    La constante renvoyée représente le mouvement que vous décidez d'effectuer : bas, gauche, droite, haut      #
#    Any other value will be ignored and will lead to a turn spent without moving                                #    Toute autre valeur sera ignorée, et entraînera la perte du tour de jeu                                      #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    
    # We use Dijkstra's algorithm from the current location
    (routes, distances) = dijkstra(mazeMap, playerLocation)
    
    # We find the closest pieces of cheese using the distances
    closestPieceOfCheese = findClosestPieceOfCheese(distances, piecesOfCheese)
    
    # Using the routes, we find the next move
    resultMoves = pathToMoves(routesToPath(routes, closestPieceOfCheese))
    return resultMoves[0]
    
###################################################################################################################################################################################################################################
###################################################################################################################################################################################################################################
