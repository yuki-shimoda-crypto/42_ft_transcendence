## 必要なこと

1. redisでチャンネルを作る
   - ユーザネームを保存する
1. 試合の組み合わせを作る
1. Gameを開始する
1. Gameの結果を保存する
1. Game結果をもとに次の試合をする
1. Tournamentに描画する

```mermaid
sequenceDiagram
    participant ユーザー
    participant ブラウザ
    participant Django
    participant Postgres
    ユーザー->>ブラウザ:人数、ユーザネーム入力
    ブラウザ->>Django:ユーザーネームの送信
    Django->>Postgres:GuestUser:にユーザーネームを保存
    Django->>Postgres:Tournament(DB)作成
    Django->>Postgres:TournamentMATCH(DB)作成
    Django-->>ブラウザ:画面遷移:register->bracket

    loop Roundが0になるまで
        loop 現在のRoundの試合がすべて終わるまで
            ブラウザ->>Django:game開始
            Django->>Postgres:Match取得
            Postgres-->>Django:response
            Django-->>ブラウザ:画面遷移:bracket->gameplay && match送る
            ブラウザ->>Django:game終了:勝者を送る
            Django->>Postgres:勝者を書き込む
            Django-->>ブラウザ:画面遷移:gameplay->bracket
        end
        Django->>Django:Round--
        Django->>Postgres:TournamentMATCH(DB)作成
    end

```

<!-- User: SortedSet
[
    [0, "name0"],
    [1, "name1"],
    [2, "name2"],
]

Winner: SortedSet
[
    [00, "name0"],
    [01, "name0"],
    [00, "name0"],
    [00, "name0"],
    [00, "name0"],
] -->

```
Match: List(queue)
[
    {
        player1: ${user_id},
        player2: ${user_id},
    },
]
```

guest_user

- id
- username

tournament_results

- id
- tournament_id(tournament.id)
- round
- user1(gusest_user.id)
- user2(guest_user_id)
- winner(guest_user_id)

tournament

- id
- partipants_amount
- timestamp
- winner
