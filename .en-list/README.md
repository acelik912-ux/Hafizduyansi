# en-list

Bu klasör projenin iş listesidir. Her iş `tasks/` altında ayrı bir JSON dosyasıdır.
VS Code'daki **en-list** eklentisi bu dosyaları gösterir; yapay zekâ yardımcısı doğrudan düzenler.

## İş dosyası

```json
{
  "id": "0001",
  "title": "Yapılacak iş",
  "group": "",
  "status": "todo",
  "order": 10,
  "notes": [
    { "by": "user", "text": "açıklama", "at": "2026-01-01T10:00:00.000Z" },
    { "by": "ai", "text": "yapılanın özeti", "at": "2026-01-01T11:00:00.000Z" }
  ],
  "created": "2026-01-01T10:00:00.000Z",
  "updated": "2026-01-01T11:00:00.000Z",
  "closed": null
}
```

## Durumlar

| status | Anlamı |
|---|---|
| todo | sırada |
| doing | üzerinde çalışılıyor |
| question | yardımcı soru sordu, cevap bekliyor |
| skipped | yapılmadı / bilerek yapılmadı (nedeni notta) |
| done | yapıldı ve doğrulandı |

## Yardımcı için kurallar

1. İşler `order` alanına göre küçükten büyüğe sırayla yapılır.
2. Başlarken `status: "doing"`, bitince `status: "done"` ve `closed` alanına zaman yazılır.
3. `title` kullanıcının metnidir, değiştirilmez. Açıklama `notes` dizisine `by: "ai"` ile eklenir.
4. Karar gerekiyorsa `status: "question"` yapılır, soru nota yazılır ve sıradaki işe geçilir.
   Kullanıcı `by: "user"` notuyla cevap verince işe geri dönülür.
5. Her yazmadan önce dosya yeniden okunur; yalnızca ilgili işin dosyası değiştirilir.
6. Yeni iş eklemek: `tasks/` içindeki en büyük numaranın bir fazlasıyla yeni dosya açılır.
