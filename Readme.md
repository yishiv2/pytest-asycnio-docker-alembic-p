## **pytest-asyncioの使い方(eventloopsのスコープ管理など)についての確認用**

```bash
pytest --capture=no -v -s
```
※コンテナ起動(sessionスコープ)　-> alenbicでマイグレーション(sessionスコープ)　->データセットアップ(functionスコープ)　->テスト実施


 参考 https://pytest-asyncio.readthedocs.io/en/latest/index.html