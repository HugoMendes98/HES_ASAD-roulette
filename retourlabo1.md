Niveau présentation :

 Diagramme de classe trop grand -> faire plusieurs slide pour le présenter.


 Use case 

 Include -> il faut  (se fait pointer par le principal)

 Extends -> il peut (il point sur le principal)


 DFD (pas de séparation, par composant mais plutôt par processus


 Requirement (fonctionnel)

 Manque des requirement car penser après avoir fait le diagramme -> solution : versionner le diagramme et le mettre à jour 

 Machine d’état :
 Pas de transition sur le diagramme





Deployement: aider avec un diagramm de component:  

```
  +-----+           +------+    +-----+
  |     |           |      |    |     |
  | c1  |-----------|black |----| db? |
  |     |       ----| board|    |     |
  +-----+     /     +------+    +-----+
            /
 +-----+  /
 |     |/    /
 |  c2 |    /
 |     |   /
 +-----+  /
         /
 +-----+ I
 |     |/
 |  c3 |
 |     |
 +-----+
  
  
```

ajouuter `1-----*` entre client server



si diagramm too big, décompose and zoom and multi slide