# Title 

## Author

```
Alban Favre
```

## Content

### S1

Pour le backend

gestion du token d'authentification (token dure 2h)

troisieme route pour le refresh du token, jwt ou similaire

quatrieme route /me, renvoie les infos user

signup and login

#### schema

use case (login sign up)

requirement authentification ?? -> ajouter joueur authentifié

data flow (auth)

entité relation: ajouter le mdp du user

### S2

securité dans le sens de l'infromation, mais aussi de l'integrité de la partie

https et du web socket s (wss)

backend only, empecher la triche avec des client modifié

#### schema

deployment update to https wss et certificat

udpate component

requirement https wss

### D1

si le jeu a deja commencé

si le serveur pete a 9h55, et que les paris ferment a 10h, et que c'est restauré a 10h05, on fait quoi ??? -> on redistribue la somme, mais seulement en bidable et waiting (ou relancer la roue plutot la restauration)

ajouter une variable is_canceled pour garder une trace des rounds annulé

front: si t'es deco message pour dire que ce que le user voit n'est pas garentis

#### schema

requirement: ajouter le concept de transaction et de restauration

### D2

vraiment pour le client, il doit pouvoir miser, partir manger et gagner ou perdre (deja implémenté)

### Bonus

- pouvoir voir les mise en RESULT
- on améliore le tapis (ajouter les piare couleur multi paris)
- multiple games
  - timer par game ??
- retirer les mises du tapis (un DELETE du bid)
- pouvoir recup l'historique ou/et game

