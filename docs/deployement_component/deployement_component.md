# Diagram deployement et composant

J'utilise plantUML, voila le WIP

```plantuml
@startuml
frame "<b>deployement</b> roulette App" {


    node "<<device>> x86_64 based machine"{

        node "Python flask application" as Backend{
            [app.py]
        }

        node "Database Server" as DB {
            [db.sqlite]
        }
   }

}

frame "client" {
   node "<<device>> browser"{
       [HTML]
   }
}

[Backend] --- [DB] : <<protocol>> TCP/IP (5432) or Unix socket
[Backend] --- [client] : <<protocol>> Web socket

@enduml
```



Component Diagram

```
@startuml
node "<<provided interface>> Roulette UI" as rouletteui {

}


node "<<provided interface>> Add/remove funds UI" as moneyui{

}



node "<<provided interface>> Login UI" as loginui{

}

component "<<subsystem>> onlineCasino" as front {


  [:gameEngine] as gameengine
  [:LoginEngine] as loginengine
  [:cashExchangeEngine] as cashexchange
}

component "<<substytem>> UserInfoVault" as bank {
  component [:AccountData] as data
}


gameengine --> data : update funds  (required interface, dependency)
cashexchange --> data : update funds  (required interface, dependency)

loginengine --> data : verify user data (required interface, dependency)
loginengine --> data : add new user (required interface, dependency)


loginui -- loginengine : port
moneyui -- cashexchange : port
rouletteui -- gameengine : port
@enduml
```

