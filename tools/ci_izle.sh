#!/bin/bash
# CI'da derleme sırasında her 60 sn disk/bellek/günlük sonunu aab-log dalına yazar (runner çökerse son durum görülsün).
# Kullanım: ci_izle.sh <build.txt yolu> (GH_TOKEN, GITHUB_REPOSITORY gerekli); arka planda çalıştırılır.
B="$1"; D=/tmp/logrepo
rm -rf $D && mkdir -p $D && cd $D && git init -q && git config user.name ci && git config user.email ci@example.com
git remote add origin "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git checkout -q --orphan aab-log
while true; do
  { date -u; df -h / | tail -1; free -m | sed -n 2p; echo "--- du"; du -sm "$GITHUB_WORKSPACE"/flutter_app/android/paket* "$GITHUB_WORKSPACE"/flutter_app/android/app/build "$GITHUB_WORKSPACE"/flutter_app/build /home/runner/.gradle 2>/dev/null; echo "--- build.txt son"; tail -40 "$B" 2>/dev/null; } > $D/izle.txt
  git add izle.txt && git commit -qm izle && git push -qf origin aab-log >/dev/null 2>&1
  sleep 60
done
