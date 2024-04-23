```mermaid
stateDiagram-v2
    State1: Idle
    State2: Bidable
    State3: Waiting
    State4: Result

    [*] --> State1
    State1 --> State2
    State2 --> State3
    State3 --> State4
    State4 --> State1

    note left of State1
        Jeu en cours de préparation
    end note

    note left of State2
        Peut recevoir des paris
    end note

    note right of State3
        Les paris sont fermés
    end note

    note right of State4
        Affichage des résultats
    end note
```