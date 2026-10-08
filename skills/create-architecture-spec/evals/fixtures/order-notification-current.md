# 現行仕様

- Order Serviceは注文確定トランザクションの完了後、Notification Serviceの `POST /internal/order-confirmed` を同期呼出しする。
- 接続タイムアウトは2秒で、失敗時は1回だけ再試行する。
- 2回とも失敗すると注文は確定したまま、`notification_failed` を注文レコードへ記録する。
- 運用者は管理画面から失敗通知を手動再送する。
- Notification Serviceは `orderId` を使った重複排除を行っている。
- HTTP本文は `orderId`、`userId`、`confirmedAt` を持つ。
