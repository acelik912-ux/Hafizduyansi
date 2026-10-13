// ============================================================================
//  HAFIZ DÜNYASI – GÖRSEL GEZGİN  v4   (tek dosya: App.js)
//  v4: 30 sabit bölümlü ANA EKRAN, profil, Yazar şifresi, logo
//
//  TAMAMEN TELEFONDA ÇALIŞIR:
//   1) YAZAR  : Resimleri yükle, butonları yerleştir, "Paketi dışa aktar" ile
//               tek bir .zip dosyası üret (resimler + butonlar içinde) ve paylaş.
//   2) OKUYUCU: Aynı uygulamayı açar, "Paket aç" ile o .zip'i seçer, gezer,
//               kendi çıpalarını (notlarını) ekler. Düzenleme yok.
//   Yazar, paketi tekrar "içe aktarıp" düzenlemeye devam edebilir.
//
//  KLASÖR: Yazar modunda resimler klasörlere ayrılabilir (liste ekranında).
//
//  SES: Her butona bir ses dosyası bağlanabilir (butona basınca çalar). Ses
//  dosyaları da pakete (.zip) girer.
//
//  Gerekli paketler:
//    npx expo install expo-image-picker expo-file-system expo-sharing \
//      expo-document-picker expo-audio @react-native-async-storage/async-storage \
//      react-native-safe-area-context
//    npm i jszip          (Snack'te: Add dependency -> jszip)
// ============================================================================
import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, Image, Pressable, FlatList, Modal, TextInput, ScrollView,
  StyleSheet, PanResponder, Animated, BackHandler, StatusBar, Alert,
  ActivityIndicator, Platform, KeyboardAvoidingView, Easing, useWindowDimensions,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as ImagePicker from 'expo-image-picker';
import * as Sharing from 'expo-sharing';
import * as DocumentPicker from 'expo-document-picker';
import { createAudioPlayer, setAudioModeAsync } from 'expo-audio';
import JSZip from 'jszip';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';

let FileSystem;
try { FileSystem = require('expo-file-system/legacy'); }   // SDK 54+
catch (e) { FileSystem = require('expo-file-system'); }    // eski SDK

// ----------------------------------------------------------------- sabitler
const STORE_KEY = 'gorsel_gezgin_v2';
const USER_KEY = 'gorsel_gezgin_user_v1';
const MODE_KEY = 'gorsel_gezgin_mode_v1';
const PASS_KEY = 'gorsel_gezgin_pass_v1';
const SEC_N = 30;
const isSec = (id) => /^sec\d+$/.test(String(id));
const hashPw = (p) => { let h = 5381; const s2 = String(p); for (let i = 0; i < s2.length; i++) h = ((h << 5) + h + s2.charCodeAt(i)) | 0; return String(h); };
const greeting = () => { const h = new Date().getHours(); return h < 6 ? 'İyi geceler' : h < 12 ? 'Günaydın' : h < 18 ? 'İyi günler' : 'İyi akşamlar'; };
// 30 sabit bölüm = kimliği sec1..sec30 olan klasörler (eksikse tamamlanır)
function ensureSections(d) {
  const folders = d.folders || [];
  const secs = [];
  for (let i = 1; i <= SEC_N; i++) {
    const found = folders.find((f) => f.id === 'sec' + i);
    secs.push(found || { id: 'sec' + i, name: 'Bölüm ' + i, cover: null });
  }
  return { ...d, folders: [...secs, ...folders.filter((f) => !isSec(f.id))] };
}
const DIR = FileSystem.documentDirectory + 'sayfalar/';
const ADIR = FileSystem.documentDirectory + 'sesler/';
const C = {
  bg: '#0B1020', card: '#151B2E', card2: '#1F2740', line: '#2C3654',
  text: '#F4F1E8', sub: '#98A2BC', accent: '#D4AF37', blue: '#4F8CFF',
  danger: '#FF5C6C', ok: '#35C98A',
};
const ANCH = [
  { k: 'stuck', t: 'Takıldım', c: '#FF5C6C' },
  { k: 'repeat', t: 'Tekrar et', c: '#FFB020' },
  { k: 'solid', t: 'Pekiştirdim', c: '#35C98A' },
];
const anchColor = (k) => (ANCH.find((a) => a.k === k) || ANCH[0]).c;
const MIN_SIZE = 0.05;
const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const safeName = (x) => String(x || '').replace(/[^a-zA-Z0-9_.-]/g, '_');
const extOf = (f, d = 'jpg') => ((String(f || '').match(/\.([a-zA-Z0-9]{2,5})$/) || [])[1] || d).toLowerCase();

// Dosya adı -> sabit sayfa kimliği
function slug(name) {
  return String(name || '')
    .replace(/\.[^.]+$/, '')
    .replace(/İ/g, 'i').replace(/I/g, 'i').toLowerCase()
    .replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g')
    .replace(/ü/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c')
    .replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
}

const srcOf = (img) => ({ uri: DIR + img.file });

function fit(cw, ch, iw, ih) {
  if (!cw || !ch || !iw || !ih) return { x: 0, y: 0, w: 0, h: 0 };
  const sc = Math.min(cw / iw, ch / ih);
  const w = iw * sc, h = ih * sc;
  return { x: (cw - w) / 2, y: (ch - h) / 2, w, h };
}

async function ensureDir() {
  const info = await FileSystem.getInfoAsync(DIR);
  if (!info.exists) await FileSystem.makeDirectoryAsync(DIR, { intermediates: true });
  const ai = await FileSystem.getInfoAsync(ADIR);
  if (!ai.exists) await FileSystem.makeDirectoryAsync(ADIR, { intermediates: true });
}

// ---- ses çalma (tek seferde bir ses)
let _player = null;
function stopSound() {
  if (_player) { try { _player.remove(); } catch (e) {} _player = null; }
}
function playSound(file) {
  try {
    stopSound();
    _player = createAudioPlayer({ uri: ADIR + file });
    _player.play();
  } catch (e) { /* ses çalınamazsa sessizce geç */ }
}

async function pickImages(multiple) {
  try {
    const r = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'], allowsMultipleSelection: multiple, quality: 1,
    });
    if (r.canceled) return [];
    return r.assets || [];
  } catch (e) {
    Alert.alert('Hata', 'Galeri açılamadı: ' + e.message);
    return [];
  }
}

function targetLabel(t, images) {
  if (!t) return 'Hedef yok';
  if (t.type === 'back') return '◀ Geri';
  if (t.type === 'home') return '⌂ Başlangıç';
  if (t.type === 'next') return 'Sonraki ▶';
  if (t.type === 'prev') return '◀ Önceki';
  const im = images.find((i) => i.id === t.id);
  return im ? '→ ' + im.name : '⚠ Silinmiş';
}

// ---------------------------------------------------------- PAKET (.zip) İŞLERİ
// Paket içeriği:  project.json  +  images/<id>.<uzantı>
async function exportPackage(data, onProgress) {
  const zip = new JSZip();
  const soundMap = {};                       // yerel dosya adı -> paketteki ad
  let sn = 0;
  const mapSound = (snd) => {
    if (!snd || !snd.file) return null;
    if (!soundMap[snd.file]) soundMap[snd.file] = 's' + (++sn) + '.' + extOf(snd.file, 'mp3');
    return { name: snd.name, file: soundMap[snd.file] };
  };
  const meta = {
    version: 4, startId: data.startId,
    folders: (data.folders || []).map((f) => ({ id: f.id, name: f.name, cover: f.cover ? safeName(f.id) + '.' + extOf(f.cover) : null })),
    images: data.images.map((im) => ({
      id: im.id, name: im.name, w: im.w, h: im.h, folder: im.folder || null,
      buttons: im.buttons.map((b) => (b.sound ? { ...b, sound: mapSound(b.sound) } : b)),
      file: safeName(im.id) + '.' + extOf(im.file),
    })),
  };
  zip.file('project.json', JSON.stringify(meta));
  for (const f of data.folders || []) {
    if (!f.cover) continue;
    try {
      const cb = await FileSystem.readAsStringAsync(DIR + f.cover, { encoding: 'base64' });
      zip.file('covers/' + safeName(f.id) + '.' + extOf(f.cover), cb, { base64: true });
    } catch (e) { /* eksik kapak atlanır */ }
  }
  for (let i = 0; i < data.images.length; i++) {
    const im = data.images[i];
    onProgress && onProgress(i + 1, data.images.length);
    const b64 = await FileSystem.readAsStringAsync(DIR + im.file, { encoding: 'base64' });
    zip.file('images/' + meta.images[i].file, b64, { base64: true });
  }
  for (const local of Object.keys(soundMap)) {
    try {
      const sb = await FileSystem.readAsStringAsync(ADIR + local, { encoding: 'base64' });
      zip.file('sounds/' + soundMap[local], sb, { base64: true });
    } catch (e) { /* eksik ses dosyası atlanır */ }
  }
  onProgress && onProgress(data.images.length, data.images.length, true);
  const out = await zip.generateAsync({ type: 'base64', compression: 'STORE' }); // resimler zaten sıkışık
  const path = FileSystem.cacheDirectory + 'hafiz_dunyasi.zip';
  await FileSystem.writeAsStringAsync(path, out, { encoding: 'base64' });
  if (!(await Sharing.isAvailableAsync())) throw new Error('Bu cihazda paylaşım desteklenmiyor.');
  await Sharing.shareAsync(path, { mimeType: 'application/zip', dialogTitle: 'Paketi paylaş', UTI: 'public.zip-archive' });
}

// Kullanıcıya dosya seçtirir, paketi açar, resimleri uygulama klasörüne yazar.
// Başarılıysa {images, startId} döner; iptalse null.
async function readPackage(onProgress) {
  const r = await DocumentPicker.getDocumentAsync({ type: '*/*', copyToCacheDirectory: true });
  if (r.canceled || !r.assets || !r.assets.length) return null;
  const b64 = await FileSystem.readAsStringAsync(r.assets[0].uri, { encoding: 'base64' });
  const zip = await JSZip.loadAsync(b64, { base64: true });
  const pj = zip.file('project.json');
  if (!pj) throw new Error('Bu bir Hafız Dünyası paketi değil (project.json bulunamadı).');
  const meta = JSON.parse(await pj.async('string'));
  if (!meta || !Array.isArray(meta.images) || !meta.images.length) throw new Error('Pakette resim yok.');

  await FileSystem.deleteAsync(DIR, { idempotent: true });
  await FileSystem.deleteAsync(ADIR, { idempotent: true });
  await ensureDir();
  const stamp = Date.now().toString(36);          // önbellek sorunu olmasın diye her içe aktarmada yeni dosya adı
  const images = [];
  const written = new Set();
  for (let i = 0; i < meta.images.length; i++) {
    const im = meta.images[i];
    onProgress && onProgress(i + 1, meta.images.length);
    const f = zip.file('images/' + im.file);
    if (!f) continue;
    const bytes = await f.async('base64');
    const file = stamp + '_' + safeName(im.id) + '.' + extOf(im.file);
    await FileSystem.writeAsStringAsync(DIR + file, bytes, { encoding: 'base64' });
    const buttons = [];
    for (const b of im.buttons || []) {
      let nb = b;
      if (b.sound && b.sound.file) {
        const sf = zip.file('sounds/' + b.sound.file);
        if (sf) {
          const nf = stamp + '_' + safeName(b.sound.file);
          if (!written.has(nf)) {
            await FileSystem.writeAsStringAsync(ADIR + nf, await sf.async('base64'), { encoding: 'base64' });
            written.add(nf);
          }
          nb = { ...b, sound: { name: b.sound.name, file: nf } };
        } else nb = { ...b, sound: null };
      }
      buttons.push(nb);
    }
    images.push({ id: im.id, name: im.name, w: im.w, h: im.h, buttons, file, folder: im.folder || null });
  }
  if (!images.length) throw new Error('Paketteki resimler okunamadı.');
  const startId = images.find((x) => x.id === meta.startId) ? meta.startId : images[0].id;
  const folders = [];
  for (const f of Array.isArray(meta.folders) ? meta.folders : []) {
    if (!f || !f.id || !f.name) continue;
    let cover = null;
    if (f.cover) {
      const cf = zip.file('covers/' + f.cover);
      if (cf) {
        cover = stamp + '_cv_' + safeName(f.cover);
        await FileSystem.writeAsStringAsync(DIR + cover, await cf.async('base64'), { encoding: 'base64' });
      }
    }
    folders.push({ id: f.id, name: f.name, cover });
  }
  const fset = new Set(folders.map((f) => f.id));
  images.forEach((im) => { if (im.folder && !fset.has(im.folder)) im.folder = null; });
  return { images, startId, folders };
}

// ------------------------------------------------------------ küçük bileşenler
function Btn({ title, onPress, kind = 'primary', style, disabled }) {
  const bg = kind === 'primary' ? C.accent : kind === 'danger' ? C.danger : C.card2;
  const fg = kind === 'primary' ? '#1A1500' : '#fff';
  return (
    <Pressable
      onPress={onPress} disabled={disabled}
      style={({ pressed }) => [s.btn, { backgroundColor: bg, opacity: disabled ? 0.4 : pressed ? 0.8 : 1 }, style]}>
      <Text style={[s.btnText, { color: fg }]}>{title}</Text>
    </Pressable>
  );
}

function NameModal({ prompt, onDone }) {
  const [text, setText] = useState('');
  useEffect(() => { if (prompt) setText(prompt.initial || ''); }, [prompt]);
  if (!prompt) return null;
  return (
    <Modal transparent animationType="fade" visible onRequestClose={() => onDone(null)}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={[s.center, { backgroundColor: 'rgba(0,0,0,0.55)' }]}>
        <View style={s.dialog}>
          <Text style={s.h2}>{prompt.title}</Text>
          <TextInput
            value={text} onChangeText={setText} autoFocus selectTextOnFocus
            placeholder="İsim yaz…" placeholderTextColor={C.sub} style={s.input}
            onSubmitEditing={() => onDone(text.trim() || null)} />
          <View style={{ flexDirection: 'row', gap: 10, marginTop: 14 }}>
            <Btn title="Vazgeç" kind="ghost" onPress={() => onDone(null)} style={{ flex: 1 }} />
            <Btn title="Tamam" onPress={() => onDone(text.trim() || null)} style={{ flex: 1 }} />
          </View>
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

// ------------------------------------------------------------ KARŞILAMA EKRANI
function Welcome({ insets, readerEmpty, onAuthor, onReader, onOpen, onBack }) {
  return (
    <View style={{ flex: 1, backgroundColor: C.bg, paddingTop: insets.top, paddingBottom: insets.bottom }}>
      <View style={[s.center, { gap: 14 }]}>
        <Image source={require('./logo.png')} style={{ width: 190, height: 190 }} resizeMode="contain" />
        {readerEmpty ? (
          <>
            <Text style={{ color: C.sub, textAlign: 'center', lineHeight: 22 }}>
              Sana gönderilen .zip paketini seç.{'\n'}Kaydedildikten sonra her açılışta doğrudan başlar.
            </Text>
            <Btn title="📦 Paketi aç (.zip)" onPress={onOpen} style={{ width: '100%', maxWidth: 420 }} />
            <Btn title="‹ Geri" kind="ghost" onPress={onBack} style={{ width: '100%', maxWidth: 420 }} />
          </>
        ) : (
          <>
            <Text style={{ color: C.sub, textAlign: 'center', lineHeight: 22 }}>Ne yapmak istiyorsun?</Text>
            <Pressable onPress={onReader} style={[s.dialog, { alignItems: 'center' }]}>
              <Text style={{ fontSize: 30 }}>📦</Text>
              <Text style={s.h2}>Okuyucu</Text>
              <Text style={{ color: C.sub, textAlign: 'center' }}>Bana gönderilen paketi aç ve gez</Text>
            </Pressable>
            <Pressable onPress={onAuthor} style={[s.dialog, { alignItems: 'center' }]}>
              <Text style={{ fontSize: 30 }}>✎</Text>
              <Text style={s.h2}>Yazar</Text>
              <Text style={{ color: C.sub, textAlign: 'center' }}>Resim yükle, buton yerleştir, paket üretip paylaş (şifreli)</Text>
            </Pressable>
          </>
        )}
      </View>
    </View>
  );
}

// ---------------------------------------------------- düzenleyici: buton kutusu
function Hotspot({ btn, W, H, selected, label, onSelect, onTap, onCommit }) {
  const [r, setR] = useState({ x: btn.x, y: btn.y, w: btn.w, h: btn.h });
  const rRef = useRef(r);
  const startR = useRef(r);
  const dims = useRef({ W, H }); dims.current = { W, H };
  const cb = useRef({}); cb.current = { onSelect, onTap, onCommit, selected };
  const wasSel = useRef(false);

  useEffect(() => {
    const n = { x: btn.x, y: btn.y, w: btn.w, h: btn.h };
    rRef.current = n; setR(n);
  }, [btn.x, btn.y, btn.w, btn.h]);

  const apply = (n) => { rRef.current = n; setR(n); };

  const mover = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onPanResponderTerminationRequest: () => false,
    onPanResponderGrant: () => { startR.current = rRef.current; wasSel.current = cb.current.selected; cb.current.onSelect(); },
    onPanResponderMove: (_, g) => {
      const { W, H } = dims.current; if (!W || !H) return;
      const a = startR.current;
      apply({ ...a, x: clamp(a.x + g.dx / W, 0, 1 - a.w), y: clamp(a.y + g.dy / H, 0, 1 - a.h) });
    },
    onPanResponderRelease: (_, g) => {
      cb.current.onCommit(rRef.current);
      if (Math.abs(g.dx) < 5 && Math.abs(g.dy) < 5 && wasSel.current) cb.current.onTap();
    },
    onPanResponderTerminate: () => cb.current.onCommit(rRef.current),
  })).current;

  const sizer = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onPanResponderTerminationRequest: () => false,
    onPanResponderGrant: () => { startR.current = rRef.current; cb.current.onSelect(); },
    onPanResponderMove: (_, g) => {
      const { W, H } = dims.current; if (!W || !H) return;
      const a = startR.current;
      apply({ ...a, w: clamp(a.w + g.dx / W, MIN_SIZE, 1 - a.x), h: clamp(a.h + g.dy / H, MIN_SIZE, 1 - a.y) });
    },
    onPanResponderRelease: () => cb.current.onCommit(rRef.current),
    onPanResponderTerminate: () => cb.current.onCommit(rRef.current),
  })).current;

  return (
    <View
      {...mover.panHandlers}
      style={[s.hot, selected && s.hotSel, { left: r.x * W, top: r.y * H, width: r.w * W, height: r.h * H }]}>
      <Text style={s.hotText} numberOfLines={2}>{btn.label ? btn.label + '\n' : ''}{label}{btn.sound ? ' 🔊' : ''}</Text>
      {selected && (
        <View {...sizer.panHandlers} style={s.handle}>
          <Text style={{ color: '#fff', fontSize: 14, fontWeight: '800' }}>⇲</Text>
        </View>
      )}
    </View>
  );
}

// ------------------------------------------------------ buton ayar sayfası
function ButtonSheet({ visible, btn, images, currentId, onChange, onClose, onUpload, onPickSound, onDelete, onDuplicate, insets }) {
  const { width } = useWindowDimensions();
  const [q, setQ] = useState('');
  if (!btn) return null;
  const tgt = btn.target;
  const cell = Math.floor((width - 32 - 20) / 3);
  const setTarget = (t) => onChange({ target: t });
  const isT = (type, id) => tgt && tgt.type === type && (id === undefined || tgt.id === id);
  const ql = q.trim().toLowerCase();
  const matches = images.filter((i) => !ql || i.name.toLowerCase().includes(ql));
  const shown = matches.slice(0, 30);

  const Row = ({ active, title, sub, onPress }) => (
    <Pressable onPress={onPress} style={[s.row, active && { borderColor: C.accent, backgroundColor: '#2A2640' }]}>
      <View style={{ flex: 1 }}>
        <Text style={s.rowTitle}>{title}</Text>
        {!!sub && <Text style={s.rowSub}>{sub}</Text>}
      </View>
      {active && <Text style={{ color: C.accent, fontSize: 18 }}>✓</Text>}
    </Pressable>
  );

  return (
    <Modal transparent visible={visible} animationType="slide" onRequestClose={onClose}>
      <View style={{ flex: 1, justifyContent: 'flex-end' }}>
        <Pressable style={StyleSheet.absoluteFill} onPress={onClose}>
          <View style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.55)' }} />
        </Pressable>
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
          <View style={[s.sheet, { paddingBottom: insets.bottom + 12 }]}>
            <View style={s.grab} />
            <ScrollView keyboardShouldPersistTaps="handled" showsVerticalScrollIndicator={false}>
              <Text style={s.h2}>Buton ayarları</Text>

              <Text style={s.secTitle}>Buton adı (isteğe bağlı)</Text>
              <TextInput
                value={btn.label || ''} onChangeText={(t) => onChange({ label: t })}
                placeholder="Sadece düzenlerken görünür" placeholderTextColor={C.sub} style={s.input} />

              <Text style={s.secTitle}>Bu butona basınca ne olsun?</Text>
              <Row active={!tgt} title="Hiçbir şey (pasif)" sub="Dokunuşu yutar, sayfa değişmez" onPress={() => setTarget(null)} />
              <Row active={isT('next')} title="Sonraki sayfa ▶" sub="Listedeki sıraya göre (şablon için ideal)" onPress={() => setTarget({ type: 'next' })} />
              <Row active={isT('prev')} title="◀ Önceki sayfa" sub="Listedeki sıraya göre (şablon için ideal)" onPress={() => setTarget({ type: 'prev' })} />
              <Row active={isT('back')} title="◀ Geldiğim sayfaya dön" sub="Geçmişteki bir önceki sayfa" onPress={() => setTarget({ type: 'back' })} />
              <Row active={isT('home')} title="⌂ Başlangıç sayfası" sub="Ana sayfa olarak seçtiğin resim" onPress={() => setTarget({ type: 'home' })} />

              <Text style={s.secTitle}>Veya belirli bir resme git ({images.length})</Text>
              <TextInput
                value={q} onChangeText={setQ} placeholder="Resim ara…" placeholderTextColor={C.sub}
                style={[s.input, { marginBottom: 10 }]} />
              <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10 }}>
                {shown.map((im) => {
                  const active = isT('image', im.id);
                  return (
                    <Pressable key={im.id} onPress={() => setTarget({ type: 'image', id: im.id })}
                      style={[s.thumbWrap, { width: cell }, active && { borderColor: C.accent }]}>
                      <Image source={srcOf(im)} style={{ width: '100%', height: cell * 0.75 }} resizeMode="cover" />
                      <Text style={s.thumbName} numberOfLines={1}>{im.name}{im.id === currentId ? ' (bu)' : ''}</Text>
                      {active && <View style={s.tick}><Text style={{ color: '#1A1500', fontWeight: '800' }}>✓</Text></View>}
                    </Pressable>
                  );
                })}
              </View>
              {matches.length > shown.length && (
                <Text style={{ color: C.sub, marginTop: 8 }}>{matches.length - shown.length} sonuç daha var, aramayı daralt.</Text>
              )}
              <Btn title="＋ Yeni resim yükle ve hedef yap" kind="ghost" onPress={onUpload} style={{ marginTop: 12 }} />

              <Text style={s.secTitle}>Ses (isteğe bağlı)</Text>
              <View style={s.row}>
                <View style={{ flex: 1 }}>
                  <Text style={s.rowTitle} numberOfLines={1}>{btn.sound ? '🔊 ' + btn.sound.name : 'Ses yok'}</Text>
                  <Text style={s.rowSub}>Butona basınca çalar</Text>
                </View>
              </View>
              <View style={{ flexDirection: 'row', gap: 8 }}>
                <Btn title={btn.sound ? 'Sesi değiştir' : '🎵 Ses seç'} kind="ghost" onPress={onPickSound} style={{ flex: 1.4 }} />
                {btn.sound && <Btn title="▶ Dinle" kind="ghost" onPress={() => playSound(btn.sound.file)} style={{ flex: 1 }} />}
                {btn.sound && <Btn title="Kaldır" kind="danger" onPress={() => { stopSound(); onChange({ sound: null }); }} style={{ flex: 1 }} />}
              </View>

              <Text style={s.secTitle}>Geçiş efekti</Text>
              <View style={{ flexDirection: 'row', gap: 8 }}>
                {[['none', 'Yok'], ['fade', 'Solma'], ['slide', 'Kayma']].map(([k, t]) => (
                  <Pressable key={k} onPress={() => onChange({ transition: k })}
                    style={[s.chip, (btn.transition || 'fade') === k && { backgroundColor: C.accent, borderColor: C.accent }]}>
                    <Text style={{ color: (btn.transition || 'fade') === k ? '#1A1500' : C.text, fontWeight: '700' }}>{t}</Text>
                  </Pressable>
                ))}
              </View>

              <View style={{ flexDirection: 'row', gap: 10, marginTop: 20 }}>
                <Btn title="Çoğalt" kind="ghost" onPress={onDuplicate} style={{ flex: 1 }} />
                <Btn title="Sil" kind="danger" onPress={onDelete} style={{ flex: 1 }} />
                <Btn title="Tamam" onPress={onClose} style={{ flex: 1 }} />
              </View>
            </ScrollView>
          </View>
        </KeyboardAvoidingView>
      </View>
    </Modal>
  );
}

// ------------------------------------------------------------- DÜZENLEYİCİ
function Editor({ image, images, onBack, onPlay, onChange, onUploadNew, onPickSound, insets }) {
  const [box, setBox] = useState({ w: 0, h: 0 });
  const [sel, setSel] = useState(null);
  const [sheet, setSheet] = useState(false);
  const rect = fit(box.w, box.h, image.w, image.h);
  const selBtn = image.buttons.find((b) => b.id === sel) || null;

  const setButtons = (fn) => onChange(image.id, (im) => ({ ...im, buttons: fn(im.buttons) }));
  const patchBtn = (id, patch) => setButtons((bs) => bs.map((b) => (b.id === id ? { ...b, ...patch } : b)));

  const addButton = () => {
    const b = { id: uid(), x: 0.35, y: 0.42, w: 0.3, h: 0.12, label: '', target: null, transition: 'fade' };
    setButtons((bs) => [...bs, b]);
    setSel(b.id);
  };
  const dupButton = () => {
    if (!selBtn) return;
    const b = { ...selBtn, id: uid(), x: clamp(selBtn.x + 0.04, 0, 1 - selBtn.w), y: clamp(selBtn.y + 0.04, 0, 1 - selBtn.h) };
    setButtons((bs) => [...bs, b]);
    setSel(b.id);
  };
  const delButton = () => {
    if (!selBtn) return;
    const id = selBtn.id;
    setSheet(false);
    setButtons((bs) => bs.filter((b) => b.id !== id));
    setSel(null);
  };
  const uploadForTarget = async () => {
    const id = selBtn && selBtn.id;
    setSheet(false);
    await new Promise((r) => setTimeout(r, 350));
    const newId = await onUploadNew();
    if (newId && id) patchBtn(id, { target: { type: 'image', id: newId } });
    setTimeout(() => setSheet(true), 250);
  };

  const pickSoundForBtn = async () => {
    const id = selBtn && selBtn.id;
    stopSound();
    setSheet(false);
    await new Promise((r) => setTimeout(r, 350));
    const snd = await onPickSound();
    if (snd && id) patchBtn(id, { sound: snd });
    setTimeout(() => setSheet(true), 250);
  };

  return (
    <View style={{ flex: 1, backgroundColor: C.bg, paddingTop: insets.top }}>
      <View style={s.header}>
        <Pressable onPress={onBack} style={s.hBtn}><Text style={s.hBtnText}>‹ Liste</Text></Pressable>
        <Text style={s.hTitle} numberOfLines={1}>{image.name}</Text>
        <Pressable onPress={onPlay} style={[s.hBtn, { backgroundColor: C.ok }]}><Text style={s.hBtnText}>▶ Dene</Text></Pressable>
      </View>

      <Pressable style={{ flex: 1 }} onPress={() => setSel(null)}>
        <View style={{ flex: 1 }} onLayout={(e) => setBox({ w: e.nativeEvent.layout.width, h: e.nativeEvent.layout.height })}>
          <View style={{ position: 'absolute', left: rect.x, top: rect.y, width: rect.w, height: rect.h }}>
            <Image source={srcOf(image)} style={{ width: '100%', height: '100%' }} resizeMode="stretch" />
            {image.buttons.map((b) => (
              <Hotspot
                key={b.id} btn={b} W={rect.w} H={rect.h} selected={b.id === sel}
                label={targetLabel(b.target, images)}
                onSelect={() => setSel(b.id)} onTap={() => setSheet(true)}
                onCommit={(r) => patchBtn(b.id, r)} />
            ))}
          </View>
        </View>
      </Pressable>

      <View style={[s.toolbar, { paddingBottom: insets.bottom + 10 }]}>
        {selBtn ? (
          <>
            <Btn title="＋ Buton" kind="ghost" onPress={addButton} style={{ flex: 1 }} />
            <Btn title="⚙ Hedef / Ayar" onPress={() => setSheet(true)} style={{ flex: 1.6 }} />
            <Btn title="🗑" kind="danger" onPress={delButton} style={{ width: 52 }} />
          </>
        ) : (
          <>
            <Btn title="＋ Buton ekle" onPress={addButton} style={{ flex: 1 }} />
            <Text style={s.hint}>{image.buttons.length} buton · sürükle, köşeden boyutlandır, ikinci dokunuşta ayar aç</Text>
          </>
        )}
      </View>

      <ButtonSheet
        visible={sheet && !!selBtn} btn={selBtn} images={images} currentId={image.id} insets={insets}
        onChange={(p) => selBtn && patchBtn(selBtn.id, p)}
        onClose={() => { stopSound(); setSheet(false); }} onUpload={uploadForTarget} onPickSound={pickSoundForBtn}
        onDelete={delButton} onDuplicate={() => { setSheet(false); dupButton(); }} />
    </View>
  );
}

// ------------------------------------------------------- ÇIPA (kullanıcı notu)
function AnchorSheet({ edit, onSave, onDelete, onClose, insets }) {
  const [type, setType] = useState('stuck');
  const [note, setNote] = useState('');
  useEffect(() => { if (edit) { setType(edit.a.type || 'stuck'); setNote(edit.a.note || ''); } }, [edit]);
  if (!edit) return null;
  return (
    <Modal transparent visible animationType="slide" onRequestClose={onClose}>
      <View style={{ flex: 1, justifyContent: 'flex-end' }}>
        <Pressable style={StyleSheet.absoluteFill} onPress={onClose}><View style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.5)' }} /></Pressable>
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
          <View style={[s.sheet, { paddingBottom: insets.bottom + 14 }]}>
            <View style={s.grab} />
            <Text style={s.h2}>📌 Hafız çıpası</Text>
            <Text style={s.secTitle}>Bu yer senin için ne?</Text>
            <View style={{ flexDirection: 'row', gap: 8 }}>
              {ANCH.map((a) => (
                <Pressable key={a.k} onPress={() => setType(a.k)}
                  style={[s.chip, { borderColor: a.c }, type === a.k && { backgroundColor: a.c }]}>
                  <Text style={{ color: '#fff', fontWeight: '700' }}>{a.t}</Text>
                </Pressable>
              ))}
            </View>
            <Text style={s.secTitle}>Not (isteğe bağlı)</Text>
            <TextInput
              value={note} onChangeText={setNote} multiline placeholder="Örn: 3. satırda hep karıştırıyorum"
              placeholderTextColor={C.sub} style={[s.input, { height: 90, paddingTop: 12, textAlignVertical: 'top' }]} />
            <View style={{ flexDirection: 'row', gap: 10, marginTop: 16 }}>
              {!edit.isNew && <Btn title="Sil" kind="danger" onPress={onDelete} style={{ flex: 1 }} />}
              <Btn title="Vazgeç" kind="ghost" onPress={onClose} style={{ flex: 1 }} />
              <Btn title="Kaydet" onPress={() => onSave({ ...edit.a, type, note: note.trim() })} style={{ flex: 1 }} />
            </View>
          </View>
        </KeyboardAvoidingView>
      </View>
    </Modal>
  );
}

function AnchorList({ visible, anchors, images, onJump, onRemove, onClose, insets }) {
  const [f, setF] = useState(null);
  const all = [];
  Object.keys(anchors || {}).forEach((pid) => {
    const im = images.find((i) => i.id === pid);
    if (!im) return;
    anchors[pid].forEach((a) => all.push({ ...a, pid, pname: im.name }));
  });
  const list = all.filter((a) => !f || a.type === f);
  return (
    <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
      <View style={{ flex: 1, backgroundColor: C.bg, paddingTop: insets.top + 8 }}>
        <View style={[s.header, { paddingTop: 4 }]}>
          <Text style={[s.title, { flex: 1, fontSize: 24 }]}>📌 Çıpalarım ({all.length})</Text>
          <Pressable onPress={onClose} style={s.hBtn}><Text style={s.hBtnText}>Kapat</Text></Pressable>
        </View>
        <View style={{ flexDirection: 'row', gap: 8, paddingHorizontal: 16, marginBottom: 8 }}>
          <Pressable onPress={() => setF(null)} style={[s.chip, { height: 36 }, !f && { backgroundColor: C.card2 }]}><Text style={{ color: '#fff' }}>Hepsi</Text></Pressable>
          {ANCH.map((a) => (
            <Pressable key={a.k} onPress={() => setF(f === a.k ? null : a.k)}
              style={[s.chip, { height: 36, borderColor: a.c }, f === a.k && { backgroundColor: a.c }]}>
              <Text style={{ color: '#fff', fontSize: 12, fontWeight: '700' }}>{a.t}</Text>
            </Pressable>
          ))}
        </View>
        <FlatList
          data={list} keyExtractor={(a) => a.id} contentContainerStyle={{ padding: 16, paddingBottom: insets.bottom + 20 }}
          ListEmptyComponent={<Text style={{ color: C.sub, textAlign: 'center', marginTop: 40, lineHeight: 22 }}>Henüz çıpa yok.{'\n'}Bir sayfada ekrana uzun basıp "Buraya çıpa koy" de.</Text>}
          renderItem={({ item }) => (
            <Pressable onPress={() => onJump(item)} style={s.aRow}>
              <View style={[s.aDot, { backgroundColor: anchColor(item.type) }]} />
              <View style={{ flex: 1 }}>
                <Text style={s.rowTitle} numberOfLines={1}>{item.pname}</Text>
                {!!item.note && <Text style={s.rowSub} numberOfLines={2}>{item.note}</Text>}
              </View>
              <Pressable onPress={() => onRemove(item)} hitSlop={10}><Text style={{ color: C.danger, fontSize: 18 }}>✕</Text></Pressable>
            </Pressable>
          )} />
      </View>
    </Modal>
  );
}

// ----------------------------------------------------------------- OYNATICI
function Viewer({ startId, homeId, images, authorMode, user, onUser, onExit, onEdit, onImport, onResetMode, insets }) {
  const { width, height } = useWindowDimensions();
  const [cur, setCur] = useState(startId);
  const [menu, setMenu] = useState(false);
  const [press, setPress] = useState(null);
  const [hints, setHints] = useState(false);
  const [anchorEdit, setAnchorEdit] = useState(null);
  const [listOpen, setListOpen] = useState(false);
  const [tip, setTip] = useState(false);
  const stack = useRef([]);
  const slide = useRef(new Animated.Value(0)).current;
  const fade = useRef(new Animated.Value(1)).current;
  const busy = useRef(false);

  const idx = Math.max(0, images.findIndex((i) => i.id === cur));
  const img = images[idx];
  const rect = fit(width, height, img.w, img.h);
  const anchors = user.anchors || {};
  const pageAnchors = anchors[img.id] || [];

  useEffect(() => { onUser((u) => (u.last === img.id ? u : { ...u, last: img.id })); }, [img.id]);
  useEffect(() => {
    if (!user.seen) {
      setTip(true);
      const t = setTimeout(() => { setTip(false); onUser((u) => ({ ...u, seen: true })); }, 4500);
      return () => clearTimeout(t);
    }
  }, []);

  const transition = (kind, back, apply) => {
    if (busy.current) return;
    if (kind === 'none') return apply();
    busy.current = true;
    if (kind === 'slide') {
      Animated.timing(slide, { toValue: back ? width : -width, duration: 160, easing: Easing.in(Easing.quad), useNativeDriver: true }).start(() => {
        apply(); slide.setValue(back ? -width : width);
        Animated.timing(slide, { toValue: 0, duration: 220, easing: Easing.out(Easing.cubic), useNativeDriver: true }).start(() => { busy.current = false; });
      });
    } else {
      Animated.timing(fade, { toValue: 0, duration: 140, useNativeDriver: true }).start(() => {
        apply();
        Animated.timing(fade, { toValue: 1, duration: 180, useNativeDriver: true }).start(() => { busy.current = false; });
      });
    }
  };

  const go = (b) => {
    if (b.sound && b.sound.file) playSound(b.sound.file);
    const t = b.target; if (!t) return;
    let next = null, back = false;
    if (t.type === 'image') next = t.id;
    else if (t.type === 'home') next = homeId;
    else if (t.type === 'next' || t.type === 'prev') {
      const seq = images.filter((i) => (i.folder || null) === (img.folder || null));   // sadece aynı bölümde
      const sp = seq.findIndex((i) => i.id === img.id);
      if (t.type === 'next') next = seq[sp + 1] && seq[sp + 1].id;
      else { next = seq[sp - 1] && seq[sp - 1].id; back = true; }
    }
    else if (t.type === 'back') {
      if (!stack.current.length) return;
      next = stack.current[stack.current.length - 1]; back = true;
      stack.current.pop();
      transition(b.transition || 'fade', true, () => setCur(next));
      return;
    }
    if (!next || !images.find((i) => i.id === next)) return;
    stack.current.push(cur);
    if (stack.current.length > 100) stack.current.shift();
    transition(b.transition || 'fade', back, () => setCur(next));
  };

  const jumpTo = (id) => {
    if (!id || id === cur || !images.find((i) => i.id === id)) return;
    stack.current.push(cur);
    transition('fade', false, () => setCur(id));
  };

  const goBack = () => {
    if (!stack.current.length) return false;
    const p = stack.current.pop();
    transition('fade', true, () => setCur(p));
    return true;
  };

  useEffect(() => {
    const sub = BackHandler.addEventListener('hardwareBackPress', () => {
      if (anchorEdit || listOpen) return false;
      if (menu) { setMenu(false); return true; }
      if (goBack()) return true;
      onExit(); return true;              // ana ekrana (ya da yazar ekranına) dön
    });
    return () => sub.remove();
  });

  const inside = press && press.x >= 0 && press.x <= 1 && press.y >= 0 && press.y <= 1;
  const saveAnchor = (a) => {
    const pid = anchorEdit.pid;
    onUser((u) => {
      const list = (u.anchors || {})[pid] || [];
      const has = list.some((x) => x.id === a.id);
      const nl = has ? list.map((x) => (x.id === a.id ? a : x)) : [...list, a];
      return { ...u, anchors: { ...(u.anchors || {}), [pid]: nl } };
    });
    setAnchorEdit(null);
  };
  const removeAnchor = (pid, id) =>
    onUser((u) => ({ ...u, anchors: { ...(u.anchors || {}), [pid]: ((u.anchors || {})[pid] || []).filter((x) => x.id !== id) } }));

  const showHints = () => { setMenu(false); setHints(true); setTimeout(() => setHints(false), 2500); };
  const lastOk = user.last && user.last !== cur && images.find((i) => i.id === user.last);

  return (
    <View style={{ flex: 1, backgroundColor: '#000' }}>
      <Pressable
        style={{ flex: 1 }} delayLongPress={600}
        onLongPress={(e) => {
          const { pageX, pageY } = e.nativeEvent;
          setPress({ x: (pageX - rect.x) / rect.w, y: (pageY - rect.y) / rect.h });
          setMenu(true);
        }}>
        <Animated.View style={{ flex: 1, opacity: fade, transform: [{ translateX: slide }] }}>
          <View style={{ position: 'absolute', left: rect.x, top: rect.y, width: rect.w, height: rect.h }}>
            <Image source={srcOf(img)} style={{ width: '100%', height: '100%' }} resizeMode="stretch" />
            {img.buttons.map((b) => (
              <Pressable
                key={b.id} onPress={() => go(b)}
                style={{
                  position: 'absolute', left: b.x * rect.w, top: b.y * rect.h, width: b.w * rect.w, height: b.h * rect.h,
                  backgroundColor: hints ? 'rgba(79,140,255,0.35)' : 'transparent',
                  borderWidth: hints ? 2 : 0, borderColor: C.blue,
                }} />
            ))}
            {!user.hide && pageAnchors.map((a) => (
              <Pressable
                key={a.id} hitSlop={8}
                onPress={() => setAnchorEdit({ pid: img.id, a, isNew: false })}
                style={[s.pin, { left: a.x * rect.w - 15, top: a.y * rect.h - 15, backgroundColor: anchColor(a.type) }]}>
                <Text style={{ fontSize: 14 }}>{a.note ? '📝' : '📌'}</Text>
              </Pressable>
            ))}
          </View>
        </Animated.View>
      </Pressable>

      {tip && (
        <View pointerEvents="none" style={[s.tip, { bottom: insets.bottom + 30 }]}>
          <Text style={{ color: '#fff', textAlign: 'center', lineHeight: 20 }}>
            Ekrana <Text style={{ fontWeight: '800' }}>uzun basarak</Text> menüyü aç{'\n'}ve takıldığın yere 📌 çıpa koy
          </Text>
        </View>
      )}

      {menu && (
        <Pressable style={[StyleSheet.absoluteFill, { backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'center', padding: 36 }]} onPress={() => setMenu(false)}>
          <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center' }}>
            <View style={s.dialog}>
              <Text style={s.h2} numberOfLines={1}>{img.name}</Text>
              <Btn title="📌 Buraya çıpa koy" style={s.menuBtn} disabled={!inside}
                onPress={() => {
                  setMenu(false);
                  setAnchorEdit({ pid: img.id, isNew: true, a: { id: uid(), x: clamp(press.x, 0.02, 0.98), y: clamp(press.y, 0.02, 0.98), type: 'stuck', note: '' } });
                }} />
              <Btn title="📋 Çıpalarım" kind="ghost" style={s.menuBtn} onPress={() => { setMenu(false); setListOpen(true); }} />
              <Btn title={user.hide ? '👁 Çıpaları göster' : '🙈 Çıpaları gizle'} kind="ghost" style={s.menuBtn}
                onPress={() => { setMenu(false); onUser((u) => ({ ...u, hide: !u.hide })); }} />
              {lastOk && <Btn title="↩ Kaldığım yere dön" kind="ghost" style={s.menuBtn} onPress={() => { setMenu(false); jumpTo(user.last); }} />}
              <Btn title="◀ Geri" kind="ghost" style={s.menuBtn} disabled={!stack.current.length} onPress={() => { setMenu(false); goBack(); }} />
              <Btn title="⌂ Başlangıca git" kind="ghost" style={s.menuBtn} onPress={() => { setMenu(false); jumpTo(homeId); }} />
              {authorMode && <Btn title="◻ Butonları 2 sn göster" kind="ghost" style={s.menuBtn} onPress={showHints} />}
              {authorMode && <Btn title="✎ Bu sayfayı düzenle" kind="ghost" style={s.menuBtn} onPress={() => onEdit(cur)} />}
              {authorMode && <Btn title="✕ Denemeyi kapat" style={s.menuBtn} onPress={onExit} />}
              {!authorMode && <Btn title="📦 Başka paket aç" kind="ghost" style={s.menuBtn} onPress={() => { setMenu(false); onImport(); }} />}
              {!authorMode && <Btn title="🏠 Ana ekran" style={s.menuBtn} onPress={() => { setMenu(false); onExit(); }} />}
            </View>
          </ScrollView>
        </Pressable>
      )}

      <AnchorSheet
        edit={anchorEdit} insets={insets} onSave={saveAnchor} onClose={() => setAnchorEdit(null)}
        onDelete={() => { removeAnchor(anchorEdit.pid, anchorEdit.a.id); setAnchorEdit(null); }} />
      <AnchorList
        visible={listOpen} anchors={anchors} images={images} insets={insets}
        onClose={() => setListOpen(false)}
        onJump={(a) => { setListOpen(false); setTimeout(() => jumpTo(a.pid), 200); }}
        onRemove={(a) => removeAnchor(a.pid, a.id)} />
    </View>
  );
}

// --------------------------------------------- toplu yapıştırma (şablon) penceresi
function PasteModal({ visible, images, clipCount, onApply, onClose, insets }) {
  const [sel, setSel] = useState({});
  const [mode, setMode] = useState('add');
  const [q, setQ] = useState('');
  const ql = q.trim().toLowerCase();
  const list = images.filter((i) => !ql || i.name.toLowerCase().includes(ql));
  const count = Object.keys(sel).filter((k) => sel[k]).length;
  const selectAll = () => { const n = { ...sel }; list.forEach((i) => { n[i.id] = true; }); setSel(n); };
  return (
    <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
      <View style={{ flex: 1, backgroundColor: C.bg, paddingTop: insets.top + 8 }}>
        <View style={[s.header, { paddingTop: 4 }]}>
          <Text style={[s.title, { flex: 1, fontSize: 22 }]}>📥 {clipCount} butonu yapıştır</Text>
          <Pressable onPress={onClose} style={s.hBtn}><Text style={s.hBtnText}>Kapat</Text></Pressable>
        </View>
        <View style={{ paddingHorizontal: 16, gap: 8 }}>
          <TextInput value={q} onChangeText={setQ} placeholder="Sayfa ara… (ör. agac)" placeholderTextColor={C.sub} style={s.input} />
          <View style={{ flexDirection: 'row', gap: 8 }}>
            <Pressable onPress={() => setMode('add')} style={[s.chip, mode === 'add' && { backgroundColor: C.accent }]}><Text style={{ color: mode === 'add' ? '#1A1500' : '#fff', fontWeight: '700' }}>Üstüne ekle</Text></Pressable>
            <Pressable onPress={() => setMode('replace')} style={[s.chip, mode === 'replace' && { backgroundColor: C.accent }]}><Text style={{ color: mode === 'replace' ? '#1A1500' : '#fff', fontWeight: '700' }}>Mevcutları değiştir</Text></Pressable>
          </View>
          <View style={{ flexDirection: 'row', gap: 8 }}>
            <Btn title={`Listedekilerin hepsini seç (${list.length})`} kind="ghost" onPress={selectAll} style={{ flex: 1, height: 40 }} />
            <Btn title="Temizle" kind="ghost" onPress={() => setSel({})} style={{ height: 40 }} />
          </View>
        </View>
        <FlatList
          data={list} keyExtractor={(i) => i.id} contentContainerStyle={{ padding: 16 }}
          initialNumToRender={20} windowSize={7}
          renderItem={({ item }) => (
            <Pressable onPress={() => setSel((p) => ({ ...p, [item.id]: !p[item.id] }))} style={s.aRow}>
              <View style={[s.check, sel[item.id] && { backgroundColor: C.accent, borderColor: C.accent }]}>
                {sel[item.id] && <Text style={{ color: '#1A1500', fontWeight: '900' }}>✓</Text>}
              </View>
              <Text style={[s.rowTitle, { flex: 1 }]} numberOfLines={1}>{item.name}</Text>
              <Text style={s.rowSub}>{item.buttons.length} buton</Text>
            </Pressable>
          )} />
        <View style={[s.bottomBar, { paddingBottom: insets.bottom + 12, position: 'relative' }]}>
          <Btn title={`${count} sayfaya uygula`} disabled={!count} style={{ flex: 1 }}
            onPress={() => { onApply(Object.keys(sel).filter((k) => sel[k]), mode); setSel({}); }} />
        </View>
      </View>
    </Modal>
  );
}

// ------------------------------------------------------------------ LİSTE
function Library({ onMergeFolder, initialFold, onHome, data, insets, clip, onAdd, onOpen, onPlay, onRename, onSetStart, onRemove, onCopy, onPasteOne, onOpenPaste, onSort, onExport, onImport, onResetMode, onSetFolder, onNewFolder, onRenameFolder, onDeleteFolder }) {
  const { width } = useWindowDimensions();
  const [actionImg, setActionImg] = useState(null);
  const [q, setQ] = useState('');
  const [fold, setFold] = useState(initialFold || null);          // null = tümü, 'none' = klasörsüz, yoksa klasör kimliği
  const [folderMenu, setFolderMenu] = useState(null);
  const [moveImg, setMoveImg] = useState(null);
  const [mergeFrom, setMergeFrom] = useState(null);
  const folders = data.folders || [];
  const fmap = {}; folders.forEach((f) => { fmap[f.id] = f.name; });
  const cf = fold === null || fold === 'none' || fmap[fold] ? fold : null;
  const countIn = (id) => data.images.filter((i) => i.folder === id).length;
  const noneCount = data.images.filter((i) => !i.folder || !fmap[i.folder]).length;
  const cw = (width - 16 * 3) / 2;
  const act = (fn) => { const im = actionImg; setActionImg(null); setTimeout(() => fn(im), 250); };
  const ql = q.trim().toLowerCase();
  const list = data.images.filter((i) =>
    (!ql || i.name.toLowerCase().includes(ql)) &&
    (cf === null || (cf === 'none' ? (!i.folder || !fmap[i.folder]) : i.folder === cf)));

  return (
    <View style={{ flex: 1, backgroundColor: C.bg, paddingTop: insets.top }}>
      <View style={{ paddingHorizontal: 16, paddingTop: 14 }}>
        <Text style={s.title}>Yazar Modu</Text>
        <Text style={{ color: C.sub, marginTop: 2 }}>{data.images.length} sayfa · dokun: düzenle · basılı tut: seçenekler</Text>
        <TextInput value={q} onChangeText={setQ} placeholder="Sayfa ara…" placeholderTextColor={C.sub} style={[s.input, { marginTop: 12 }]} />
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 10 }} contentContainerStyle={{ gap: 8 }}>
          <Pressable style={s.pill} onPress={onHome}><Text style={s.pillText}>🏠 Ana ekran</Text></Pressable>
          <Pressable style={[s.pill, !data.images.length && { opacity: 0.4 }, { backgroundColor: C.accent }]} disabled={!data.images.length} onPress={onExport}>
            <Text style={[s.pillText, { color: '#1A1500' }]}>⬆ Paketi dışa aktar (.zip)</Text>
          </Pressable>
          <Pressable style={s.pill} onPress={onImport}><Text style={s.pillText}>⬇ Paket içe aktar</Text></Pressable>
          <Pressable style={s.pill} onPress={onSort}><Text style={s.pillText}>A→Z / 1→30 sırala</Text></Pressable>
          <Pressable style={[s.pill, !clip && { opacity: 0.4 }]} disabled={!clip} onPress={onOpenPaste}>
            <Text style={s.pillText}>📥 Yapıştır{clip ? ` (${clip.length})` : ''}</Text>
          </Pressable>
          <Pressable style={s.pill} onPress={onResetMode}><Text style={s.pillText}>⚙ Mod seç</Text></Pressable>
        </ScrollView>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 10 }} contentContainerStyle={{ gap: 8 }}>
          <Pressable style={[s.pill, cf === null && { backgroundColor: C.accent }]} onPress={() => setFold(null)}>
            <Text style={[s.pillText, cf === null && { color: '#1A1500' }]}>Tümü ({data.images.length})</Text>
          </Pressable>
          {folders.map((f) => (
            <Pressable key={f.id} style={[s.pill, cf === f.id && { backgroundColor: C.accent }]}
              onPress={() => setFold(f.id)} onLongPress={() => setFolderMenu(f)}>
              <Text style={[s.pillText, cf === f.id && { color: '#1A1500' }]}>{isSec(f.id) ? f.name : '📁 ' + f.name} ({countIn(f.id)})</Text>
            </Pressable>
          ))}
          {folders.length > 0 && (
            <Pressable style={[s.pill, cf === 'none' && { backgroundColor: C.accent }]} onPress={() => setFold('none')}>
              <Text style={[s.pillText, cf === 'none' && { color: '#1A1500' }]}>Klasörsüz ({noneCount})</Text>
            </Pressable>
          )}
        </ScrollView>
        {folders.length > 0 && <Text style={{ color: C.sub, fontSize: 12, marginTop: 6 }}>Bölüm adına basılı tut: yeniden adlandır</Text>}
      </View>

      {data.images.length === 0 ? (
        <View style={s.empty}>
          <Text style={{ fontSize: 54 }}>🖼️</Text>
          <Text style={[s.h2, { marginTop: 10 }]}>Henüz resim yok</Text>
          <Text style={{ color: C.sub, textAlign: 'center', marginTop: 6, lineHeight: 20 }}>
            Resimleri yükle, butonları yerleştir, sonra "Paketi dışa aktar" ile tek bir .zip üretip paylaş.
          </Text>
        </View>
      ) : (
        <FlatList
          data={list} keyExtractor={(i) => i.id} numColumns={2}
          initialNumToRender={8} windowSize={5} removeClippedSubviews
          contentContainerStyle={{ padding: 16, paddingBottom: 140 }}
          columnWrapperStyle={{ gap: 16 }} ItemSeparatorComponent={() => <View style={{ height: 16 }} />}
          ListEmptyComponent={<Text style={{ color: C.sub, textAlign: 'center', marginTop: 40, lineHeight: 22 }}>Burada resim yok.{'\n'}Bir resme basılı tutup "Klasöre taşı" seç.</Text>}
          renderItem={({ item }) => (
            <Pressable
              onPress={() => onOpen(item.id)} onLongPress={() => setActionImg(item)}
              style={({ pressed }) => [s.card, { width: cw, opacity: pressed ? 0.85 : 1 }]}>
              <Image source={srcOf(item)} style={{ width: '100%', height: cw * 0.75 }} resizeMode="cover" />
              <View style={{ padding: 10 }}>
                <Text style={s.cardName} numberOfLines={1}>{item.name}</Text>
                <Text style={{ color: C.sub, fontSize: 12, marginTop: 2 }} numberOfLines={1}>{item.buttons.length} buton{cf === null && item.folder && fmap[item.folder] ? ' · 📁 ' + fmap[item.folder] : ''}</Text>
              </View>
              {data.startId === item.id && <View style={s.badge}><Text style={s.badgeText}>⌂ Başlangıç</Text></View>}
              <Pressable style={s.more} onPress={() => setActionImg(item)} hitSlop={8}><Text style={{ color: '#fff', fontSize: 18 }}>⋯</Text></Pressable>
            </Pressable>
          )} />
      )}

      <View style={[s.bottomBar, { paddingBottom: insets.bottom + 12 }]}>
        <Btn title="＋ Resim yükle" onPress={() => onAdd(fmap[cf] ? cf : null)} style={{ flex: 1.4 }} />
        <Btn title="▶ Kullanıcı gibi dene" kind="ghost" disabled={!data.images.length} onPress={() => onPlay(null)} style={{ flex: 1.2 }} />
      </View>

      <Modal transparent visible={!!actionImg} animationType="fade" onRequestClose={() => setActionImg(null)}>
        <Pressable style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]} onPress={() => setActionImg(null)}>
          <View style={s.dialog}>
            <Text style={s.h2} numberOfLines={1}>{actionImg && actionImg.name}</Text>
            <Btn title="✎ Butonları düzenle" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onOpen(im.id))} />
            <Btn title="▶ Buradan dene" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onPlay(im.id))} />
            <Btn title="📋 Butonlarını kopyala" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onCopy(im.id))} />
            {clip && <Btn title={`📥 ${clip.length} butonu buna yapıştır`} kind="ghost" style={s.menuBtn} onPress={() => act((im) => onPasteOne(im.id))} />}
            <Btn title="Aa Yeniden adlandır" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onRename(im.id))} />
            <Btn title="📁 Klasöre taşı" kind="ghost" style={s.menuBtn} onPress={() => act((im) => setMoveImg(im))} />
            <Btn title="⌂ Başlangıç sayfası yap" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onSetStart(im.id))} />
            <Btn title="🗑 Sil" kind="danger" style={s.menuBtn} onPress={() => act((im) => onRemove(im.id))} />
          </View>
        </Pressable>
      </Modal>

      <Modal transparent visible={!!moveImg} animationType="fade" onRequestClose={() => setMoveImg(null)}>
        <Pressable style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]} onPress={() => setMoveImg(null)}>
          <View style={s.dialog}>
            <Text style={s.h2} numberOfLines={1}>📁 {moveImg && moveImg.name}</Text>
            <ScrollView style={{ maxHeight: 340 }}>
              <Btn title="Klasörsüz" kind={moveImg && (!moveImg.folder || !fmap[moveImg.folder]) ? 'primary' : 'ghost'} style={s.menuBtn}
                onPress={() => { onSetFolder(moveImg.id, null); setMoveImg(null); }} />
              {folders.map((f) => (
                <Btn key={f.id} title={'📁 ' + f.name} kind={moveImg && moveImg.folder === f.id ? 'primary' : 'ghost'} style={s.menuBtn}
                  onPress={() => { onSetFolder(moveImg.id, f.id); setMoveImg(null); }} />
              ))}
            </ScrollView>
          </View>
        </Pressable>
      </Modal>

      <Modal transparent visible={!!mergeFrom} animationType="fade" onRequestClose={() => setMergeFrom(null)}>
        <Pressable style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]} onPress={() => setMergeFrom(null)}>
          <View style={s.dialog}>
            <Text style={s.h2} numberOfLines={2}>"{mergeFrom && mergeFrom.name}" hangi bölüme taşınsın?</Text>
            <ScrollView style={{ maxHeight: 380 }}>
              {folders.filter((f) => isSec(f.id)).map((f) => (
                <Btn key={f.id} title={f.name + ' (' + countIn(f.id) + ')'} kind="ghost" style={s.menuBtn}
                  onPress={() => { const from = mergeFrom; setMergeFrom(null); setFold(f.id); onMergeFolder(from.id, f.id); }} />
              ))}
            </ScrollView>
          </View>
        </Pressable>
      </Modal>

      <Modal transparent visible={!!folderMenu} animationType="fade" onRequestClose={() => setFolderMenu(null)}>
        <Pressable style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]} onPress={() => setFolderMenu(null)}>
          <View style={s.dialog}>
            <Text style={s.h2} numberOfLines={1}>📁 {folderMenu && folderMenu.name}</Text>
            <Btn title="Aa Yeniden adlandır" kind="ghost" style={s.menuBtn}
              onPress={() => { const f = folderMenu; setFolderMenu(null); setTimeout(() => onRenameFolder(f.id), 250); }} />
            {folderMenu && !isSec(folderMenu.id) && <Btn title="➡ Tüm resimleri bir bölüme taşı" kind="ghost" style={s.menuBtn}
              onPress={() => { const f = folderMenu; setFolderMenu(null); setTimeout(() => setMergeFrom(f), 250); }} />}
            {folderMenu && !isSec(folderMenu.id) && <Btn title="🗑 Klasörü sil (resimler silinmez)" kind="danger" style={s.menuBtn}
              onPress={() => { const f = folderMenu; setFolderMenu(null); if (fold === f.id) setFold(null); setTimeout(() => onDeleteFolder(f.id), 250); }} />}
          </View>
        </Pressable>
      </Modal>
    </View>
  );
}

// ------------------------------------------------------------- ŞİFRE PENCERESİ
function PassModal({ prompt, onDone }) {
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [err, setErr] = useState('');
  useEffect(() => { setA(''); setB(''); setErr(''); }, [prompt]);
  if (!prompt) return null;
  const create = prompt.mode === 'create';
  const submit = () => {
    if (create) {
      if (a.length < 4) return setErr('En az 4 karakter olmalı.');
      if (a !== b) return setErr('İki şifre aynı değil.');
      onDone(a);
    } else if (prompt.check && !prompt.check(a)) setErr('Şifre yanlış.');
    else onDone(a || 'ok');
  };
  return (
    <Modal transparent animationType="fade" visible onRequestClose={() => onDone(null)}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]}>
        <View style={s.dialog}>
          <Text style={s.h2}>{create ? '🔒 Yazar şifresi oluştur' : '🔒 Yazar şifresi'}</Text>
          <Text style={{ color: C.sub, marginBottom: 10, lineHeight: 19 }}>
            {create ? 'Yazar moduna girerken bu şifre sorulacak. Unutursan uygulama verisini silmek gerekir; bir yere not et.' : 'Yazar moduna girmek için şifreni yaz.'}
          </Text>
          <TextInput value={a} onChangeText={(v) => { setA(v); setErr(''); }} autoFocus secureTextEntry
            placeholder="Şifre" placeholderTextColor={C.sub} style={s.input} onSubmitEditing={create ? undefined : submit} />
          {create && <TextInput value={b} onChangeText={(v) => { setB(v); setErr(''); }} secureTextEntry
            placeholder="Şifre (tekrar)" placeholderTextColor={C.sub} style={[s.input, { marginTop: 8 }]} onSubmitEditing={submit} />}
          {!!err && <Text style={{ color: C.danger, marginTop: 8 }}>{err}</Text>}
          <View style={{ flexDirection: 'row', gap: 10, marginTop: 14 }}>
            <Btn title="Vazgeç" kind="ghost" onPress={() => onDone(null)} style={{ flex: 1 }} />
            <Btn title="Tamam" onPress={submit} style={{ flex: 1 }} />
          </View>
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

// ---------------------------------------------------------------- PROFİL PENCERESİ
function ProfileModal({ visible, profile, onSave, onPhoto, onRemovePhoto, onAuthor, onClose }) {
  const [name, setName] = useState('');
  useEffect(() => { if (visible) setName(profile.name || ''); }, [visible]);
  return (
    <Modal transparent animationType="fade" visible={visible} onRequestClose={onClose}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]}>
        <View style={s.dialog}>
          <Text style={s.h2}>Profilim</Text>
          <View style={{ alignItems: 'center', marginBottom: 12 }}>
            <Pressable onPress={onPhoto} style={s.avatarBig}>
              {profile.photo ? <Image source={{ uri: profile.photo }} style={{ width: '100%', height: '100%' }} /> : <Text style={{ fontSize: 40 }}>🎓</Text>}
            </Pressable>
            <Text style={{ color: C.sub, fontSize: 12, marginTop: 6 }}>Fotoğraf için dokun</Text>
            {!!profile.photo && <Pressable onPress={onRemovePhoto}><Text style={{ color: C.danger, fontSize: 12, marginTop: 4 }}>Fotoğrafı kaldır</Text></Pressable>}
          </View>
          <TextInput value={name} onChangeText={setName} placeholder="Adın" placeholderTextColor={C.sub} style={s.input} />
          <View style={{ flexDirection: 'row', gap: 10, marginTop: 14 }}>
            <Btn title="Kapat" kind="ghost" onPress={onClose} style={{ flex: 1 }} />
            <Btn title="Kaydet" onPress={() => onSave(name.trim())} style={{ flex: 1 }} />
          </View>
          {onAuthor && (
            <Pressable onPress={onAuthor} style={{ alignSelf: 'center', marginTop: 16, padding: 6 }}>
              <Text style={{ color: C.sub, fontSize: 12 }}>🔒 Yazar girişi</Text>
            </Pressable>
          )}
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

// ----------------------------------------------------------------- ANA EKRAN (30 bölüm)
function Home({ data, user, author, insets, onPlay, onProfile, onLibrary, onExport, onImport, onPassword, onResetMode, onCover, onRenameSec, onAddTo }) {
  const { width } = useWindowDimensions();
  const [menu, setMenu] = useState(null);
  const profile = user.profile || {};
  const secs = (data.folders || []).filter((f) => isSec(f.id));
  const countOf = (id) => data.images.filter((i) => i.folder === id).length;
  const firstOf = (id) => { const im = data.images.find((i) => i.folder === id); return im ? im.id : null; };
  const tw = Math.floor((width - 32 - 14) / 2) - 1;   // 2 sütun, ekranı doldurur
  const last = user.last && data.images.find((i) => i.id === user.last);
  const tap = (f) => {
    const st = firstOf(f.id);
    if (st) onPlay(st);
    else if (author) setMenu(f);
    else Alert.alert(f.name, 'Bu bölüm henüz boş.');
  };
  const act = (fn) => { const f = menu; setMenu(null); setTimeout(() => fn(f), 250); };
  return (
    <View style={{ flex: 1, backgroundColor: C.bg }}>
      <ScrollView contentContainerStyle={{ paddingBottom: insets.bottom + 30 }} showsVerticalScrollIndicator={false}>
        <Pressable onPress={onProfile} style={[s.homeHead, { paddingTop: insets.top + 14 }]}>
          <View style={s.avatar}>
            {profile.photo ? <Image source={{ uri: profile.photo }} style={{ width: '100%', height: '100%' }} /> : <Text style={{ fontSize: 28 }}>🎓</Text>}
          </View>
          <View style={{ flex: 1 }}>
            <Text style={{ color: C.sub, fontSize: 15 }}>{greeting()} ☀️</Text>
            <Text style={{ color: C.text, fontSize: 21, fontWeight: '800' }} numberOfLines={1}>{profile.name || 'Profilini oluştur'}</Text>
          </View>
          <Text style={{ color: C.sub, fontSize: 22 }}>⋯</Text>
        </Pressable>

        <Image source={require('./logo.png')} style={{ width: '100%', height: 190, marginTop: 6 }} resizeMode="contain" />

        {!!last && (
          <Pressable onPress={() => onPlay(last.id)} style={s.resume}>
            <Text style={{ fontSize: 26 }}>↩</Text>
            <View style={{ flex: 1 }}>
              <Text style={{ color: '#fff', fontSize: 16, fontWeight: '800' }}>Kaldığın yerden devam et</Text>
              <Text style={{ color: 'rgba(255,255,255,0.85)', marginTop: 2 }} numberOfLines={1}>{last.name}</Text>
            </View>
          </Pressable>
        )}

        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 14 }} contentContainerStyle={{ gap: 8, paddingHorizontal: 16 }}>
          {author ? (
            <>
              <Pressable style={[s.pill, { backgroundColor: C.accent }]} onPress={() => onLibrary(null)}><Text style={[s.pillText, { color: '#1A1500' }]}>✎ Tüm resimler</Text></Pressable>
              <Pressable style={s.pill} onPress={onExport}><Text style={s.pillText}>⬆ Dışa aktar</Text></Pressable>
              <Pressable style={s.pill} onPress={onImport}><Text style={s.pillText}>⬇ İçe aktar</Text></Pressable>
              <Pressable style={s.pill} onPress={onPassword}><Text style={s.pillText}>🔒 Şifre</Text></Pressable>
              <Pressable style={s.pill} onPress={onResetMode}><Text style={s.pillText}>⚙ Mod seç</Text></Pressable>
            </>
          ) : (
            <Pressable style={[s.pill, { backgroundColor: C.accent }]} onPress={onImport}><Text style={[s.pillText, { color: '#1A1500' }]}>📦 Paket aç (.zip)</Text></Pressable>
          )}
        </ScrollView>

        <Text style={[s.secTitle, { marginHorizontal: 16, marginTop: 22 }]}>Bölümler</Text>
        {!author && !data.images.length && (
          <Text style={{ color: C.sub, marginHorizontal: 16, marginBottom: 10, lineHeight: 20 }}>
            Sana gönderilen .zip paketini yukarıdaki "Paket aç" ile seç. Bölümler dolacak.
          </Text>
        )}
        <View style={{ flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 16, gap: 14, justifyContent: 'space-between' }}>
          {secs.map((f, i) => {
            const n = countOf(f.id);
            return (
              <Pressable key={f.id} onPress={() => tap(f)} onLongPress={author ? () => setMenu(f) : undefined} delayLongPress={450}
                style={({ pressed }) => [s.tile, { width: tw, height: Math.round(tw * 1.3), opacity: pressed ? 0.8 : n || author ? 1 : 0.5 }]}>
                {f.cover
                  ? <Image source={{ uri: DIR + f.cover }} style={StyleSheet.absoluteFill} resizeMode="cover" />
                  : <View style={[StyleSheet.absoluteFill, s.center, { padding: 0 }]}><Text style={{ color: C.line, fontSize: 64, fontWeight: '900' }}>{i + 1}</Text></View>}
                <View style={s.tileNum}><Text style={{ color: '#fff', fontSize: 11, fontWeight: '800' }}>{i + 1}</Text></View>
                {author && <View style={s.tileCnt}><Text style={{ color: '#fff', fontSize: 11, fontWeight: '800' }}>{n}</Text></View>}
                <View style={s.tileName}><Text style={{ color: '#fff', fontWeight: '700', fontSize: 14 }} numberOfLines={1}>{f.name}</Text></View>
              </Pressable>
            );
          })}
        </View>
        {author && <Text style={{ color: C.sub, fontSize: 12, textAlign: 'center', marginTop: 14 }}>Bölüme basılı tut: kapak resmi, ad, resim ekle</Text>}
      </ScrollView>

      <Modal transparent visible={!!menu} animationType="fade" onRequestClose={() => setMenu(null)}>
        <Pressable style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]} onPress={() => setMenu(null)}>
          <View style={s.dialog}>
            <Text style={s.h2} numberOfLines={1}>{menu && menu.name}</Text>
            <Btn title="🖼 Kapak resmi seç" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onCover(f.id))} />
            <Btn title="Aa Adını değiştir" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onRenameSec(f.id))} />
            <Btn title="＋ Bu bölüme resim ekle" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onAddTo(f.id))} />
            <Btn title="✎ Bu bölümün resimlerini düzenle" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onLibrary(f.id))} />
            {menu && !!firstOf(menu.id) && <Btn title="▶ Bölümü aç" style={s.menuBtn} onPress={() => act((f) => onPlay(firstOf(f.id)))} />}
          </View>
        </Pressable>
      </Modal>
    </View>
  );
}

// -------------------------------------------------------------------- KÖK
function Root() {
  const insets = useSafeAreaInsets();
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);            // false | 'mesaj'
  const [mode, setMode] = useState(null);             // null | 'author' | 'reader'
  const [data, setData] = useState({ images: [], startId: null });
  const [user, setUser] = useState({ anchors: {}, last: null, seen: false, hide: false });
  const [screen, setScreen] = useState({ name: 'home' });
  const [passPrompt, setPassPrompt] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const [namePrompt, setNamePrompt] = useState(null);
  const [clip, setClip] = useState(null);
  const [pasteOpen, setPasteOpen] = useState(false);
  const dataRef = useRef(data); dataRef.current = data;
  const AUTHOR = mode === 'author';

  useEffect(() => {
    try { setAudioModeAsync({ playsInSilentMode: true }); } catch (e) {}
  }, []);

  useEffect(() => {
    (async () => {
      try {
        await ensureDir();
        const raw = await AsyncStorage.getItem(STORE_KEY);
        const d = ensureSections(raw ? JSON.parse(raw) : { images: [], startId: null });
        setData(d);
        const m = await AsyncStorage.getItem(MODE_KEY);
        if (m === 'author' || m === 'reader') setMode(m);
        const u = await AsyncStorage.getItem(USER_KEY);
        if (u) setUser((p) => ({ ...p, ...JSON.parse(u) }));
      } catch (e) { /* ilk açılış */ }
      setReady(true);
    })();
  }, []);

  useEffect(() => {
    if (!ready) return;
    const t = setTimeout(() => { AsyncStorage.setItem(STORE_KEY, JSON.stringify(data)).catch(() => {}); }, 250);
    return () => clearTimeout(t);
  }, [data, ready]);

  useEffect(() => {
    if (!ready) return;
    const t = setTimeout(() => { AsyncStorage.setItem(USER_KEY, JSON.stringify(user)).catch(() => {}); }, 250);
    return () => clearTimeout(t);
  }, [user, ready]);

  useEffect(() => {
    const sub = BackHandler.addEventListener('hardwareBackPress', () => {
      if (AUTHOR && screen.name === 'editor') { setScreen({ name: 'library' }); return true; }
      if (AUTHOR && screen.name === 'library') { setScreen({ name: 'home' }); return true; }
      return false;
    });
    return () => sub.remove();
  }, [screen, mode]);

  const promptName = (title, initial = '') => new Promise((res) => setNamePrompt({ title, initial, res }));
  const finishPrompt = (v) => { namePrompt.res(v); setNamePrompt(null); };

  const askPass = (kind, check) => new Promise((res) => setPassPrompt({ mode: kind, check, res }));
  const finishPass = (v) => { passPrompt.res(v); setPassPrompt(null); };
  const enterAuthor = async () => {
    let stored = null;
    try { stored = await AsyncStorage.getItem(PASS_KEY); } catch (e) {}
    if (!stored) {
      const p = await askPass('create');
      if (!p) return false;
      await AsyncStorage.setItem(PASS_KEY, hashPw(p));
      return true;
    }
    return !!(await askPass('enter', (x) => hashPw(x) === stored));
  };
  const changePassword = async () => {
    const stored = await AsyncStorage.getItem(PASS_KEY);
    if (stored && !(await askPass('enter', (x) => hashPw(x) === stored))) return;
    await new Promise((r) => setTimeout(r, 300));
    const p = await askPass('create');
    if (p) { await AsyncStorage.setItem(PASS_KEY, hashPw(p)); Alert.alert('Tamam', 'Şifre değiştirildi.'); }
  };
  const chooseMode = async (m) => {
    if (m === 'author' && !(await enterAuthor())) return;
    setMode(m);
    AsyncStorage.setItem(MODE_KEY, m).catch(() => {});
    setScreen({ name: 'home' });
  };
  const resetMode = () => {
    setMode(null);
    AsyncStorage.removeItem(MODE_KEY).catch(() => {});
    setScreen({ name: 'home' });
  };

  // ---- profil
  const saveProfileName = (name) => { setUser((u) => ({ ...u, profile: { ...(u.profile || {}), name } })); setProfileOpen(false); };
  const pickPhoto = async () => {
    try {
      const r = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'], allowsEditing: true, aspect: [1, 1], quality: 0.7 });
      if (r.canceled || !r.assets || !r.assets.length) return;
      const to = FileSystem.documentDirectory + 'profil_' + uid() + '.jpg';
      await FileSystem.copyAsync({ from: r.assets[0].uri, to });
      const old = (user.profile || {}).photo;
      if (old) FileSystem.deleteAsync(old, { idempotent: true }).catch(() => {});
      setUser((u) => ({ ...u, profile: { ...(u.profile || {}), photo: to } }));
    } catch (e) { Alert.alert('Fotoğraf eklenemedi', e.message); }
  };
  const removePhoto = () => {
    const old = (user.profile || {}).photo;
    if (old) FileSystem.deleteAsync(old, { idempotent: true }).catch(() => {});
    setUser((u) => ({ ...u, profile: { ...(u.profile || {}), photo: null } }));
  };
  const authorFromProfile = () => { setProfileOpen(false); setTimeout(() => chooseMode('author'), 300); };

  const importAssets = async (assets, names = []) => {
    await ensureDir();
    const taken = new Set(dataRef.current.images.map((i) => i.id));
    const out = [];
    for (let i = 0; i < assets.length; i++) {
      const a = assets[i];
      const orig = a.fileName || '';
      const base = slug(orig) || 'p_' + uid();
      let id = base, n = 2;
      while (taken.has(id)) { id = base + '_' + n++; }
      taken.add(id);
      const file = id + '_' + Date.now().toString(36) + '.' + extOf(a.uri.split('?')[0]);
      await FileSystem.copyAsync({ from: a.uri, to: DIR + file });
      out.push({
        id, file, w: a.width || 1000, h: a.height || 1000, buttons: [],
        name: names[i] || (orig ? orig.replace(/\.[^.]+$/, '') : 'Resim ' + (dataRef.current.images.length + i + 1)),
      });
    }
    return out;
  };
  const appendImages = (imgs, folder = null) =>
    setData((d) => ({
      ...d,
      images: [...d.images, ...imgs.map((i) => (folder ? { ...i, folder } : i))],
      startId: d.startId || imgs[0].id,
    }));

  const addMany = async (folder = null) => {
    const assets = await pickImages(true);
    if (!assets.length) return;
    assets.sort((a, b) => (a.fileName || '').localeCompare(b.fileName || '', 'tr', { numeric: true }));
    setBusy('Kaydediliyor…');
    try { appendImages(await importAssets(assets), folder); }
    catch (e) { Alert.alert('Hata', 'Resim kaydedilemedi: ' + e.message); }
    setBusy(false);
  };

  const uploadOne = async () => {
    const assets = await pickImages(false);
    if (!assets.length) return null;
    const def = assets[0].fileName ? assets[0].fileName.replace(/\.[^.]+$/, '') : 'Resim ' + (dataRef.current.images.length + 1);
    const name = await promptName('Yeni resmin adı', def);
    if (name === null) return null;
    setBusy('Kaydediliyor…');
    try {
      const [img] = await importAssets(assets, [name]);
      appendImages([img]);
      setBusy(false);
      return img.id;
    } catch (e) { setBusy(false); Alert.alert('Hata', e.message); return null; }
  };

  const pickSound = async () => {
    try {
      const r = await DocumentPicker.getDocumentAsync({ type: 'audio/*', copyToCacheDirectory: true });
      if (r.canceled || !r.assets || !r.assets.length) return null;
      const a = r.assets[0];
      await ensureDir();
      const file = uid() + '.' + extOf(a.name || a.uri, 'mp3');
      await FileSystem.copyAsync({ from: a.uri, to: ADIR + file });
      return { file, name: (a.name || 'Ses').replace(/\.[^.]+$/, '') };
    } catch (e) { Alert.alert('Ses eklenemedi', e.message); return null; }
  };

  const updateImage = (id, fnOrPatch) =>
    setData((d) => ({
      ...d,
      images: d.images.map((i) => (i.id !== id ? i : typeof fnOrPatch === 'function' ? fnOrPatch(i) : { ...i, ...fnOrPatch })),
    }));

  // ---- klasörler
  const newFolder = async () => {
    const name = await promptName('Klasör adı', '');
    if (!name) return null;
    const id = 'f_' + uid();
    setData((d) => ({ ...d, folders: [...(d.folders || []), { id, name }] }));
    return id;
  };
  const renameFolder = async (id) => {
    const f = (dataRef.current.folders || []).find((x) => x.id === id); if (!f) return;
    const n = await promptName('Klasör adı', f.name);
    if (n) setData((d) => ({ ...d, folders: (d.folders || []).map((x) => (x.id === id ? { ...x, name: n } : x)) }));
  };
  const deleteFolder = (id) => {
    const f = (dataRef.current.folders || []).find((x) => x.id === id); if (!f) return;
    if (isSec(id)) { Alert.alert('Silinemez', '30 bölüm sabittir. İstersen adını değiştirebilirsin.'); return; }
    Alert.alert('Klasörü sil', `"${f.name}" klasörü silinecek. İçindeki resimler silinmez, klasörsüz kalır.`, [
      { text: 'Vazgeç', style: 'cancel' },
      {
        text: 'Sil', style: 'destructive',
        onPress: () => setData((d) => ({
          ...d,
          folders: (d.folders || []).filter((x) => x.id !== id),
          images: d.images.map((i) => (i.folder === id ? { ...i, folder: null } : i)),
        })),
      },
    ]);
  };
  const setFolder = (imgId, folderId) => updateImage(imgId, { folder: folderId });
  const mergeFolder = (fromId, toId) => {
    const from = (dataRef.current.folders || []).find((x) => x.id === fromId);
    const to = (dataRef.current.folders || []).find((x) => x.id === toId);
    if (!from || !to) return;
    const n = dataRef.current.images.filter((i) => i.folder === fromId).length;
    Alert.alert('Taşı', `"${from.name}" içindeki ${n} resim "${to.name}" bölümüne taşınacak ve eski klasör silinecek.`, [
      { text: 'Vazgeç', style: 'cancel' },
      {
        text: 'Taşı',
        onPress: () => setData((d) => ({
          ...d,
          images: d.images.map((i) => (i.folder === fromId ? { ...i, folder: toId } : i)),
          folders: (d.folders || []).filter((x) => x.id !== fromId),
        })),
      },
    ]);
  };
  const setCover = async (fid) => {
    const assets = await pickImages(false);
    if (!assets.length) return;
    try {
      await ensureDir();
      const file = 'cv_' + uid() + '.' + extOf(assets[0].uri.split('?')[0]);
      await FileSystem.copyAsync({ from: assets[0].uri, to: DIR + file });
      const f = (dataRef.current.folders || []).find((x) => x.id === fid);
      if (f && f.cover) FileSystem.deleteAsync(DIR + f.cover, { idempotent: true }).catch(() => {});
      setData((d) => ({ ...d, folders: (d.folders || []).map((x) => (x.id === fid ? { ...x, cover: file } : x)) }));
    } catch (e) { Alert.alert('Kapak eklenemedi', e.message); }
  };

  const rename = async (id) => {
    const im = data.images.find((i) => i.id === id);
    const n = await promptName('Resmin adı', im ? im.name : '');
    if (n) updateImage(id, { name: n });
  };

  const removeImage = (id) => {
    const im = data.images.find((i) => i.id === id); if (!im) return;
    Alert.alert('Resmi sil', `"${im.name}" ve üzerindeki butonlar silinecek. Bu resme giden butonlar pasif olacak.`, [
      { text: 'Vazgeç', style: 'cancel' },
      {
        text: 'Sil', style: 'destructive', onPress: async () => {
          try { await FileSystem.deleteAsync(DIR + im.file, { idempotent: true }); } catch (e) {}
          setData((d) => {
            const images = d.images.filter((i) => i.id !== id).map((i) => ({
              ...i,
              buttons: i.buttons.map((b) => (b.target && b.target.type === 'image' && b.target.id === id ? { ...b, target: null } : b)),
            }));
            return { ...d, images, startId: d.startId === id ? (images[0] ? images[0].id : null) : d.startId };
          });
        },
      },
    ]);
  };

  const sortAll = () =>
    setData((d) => ({ ...d, images: [...d.images].sort((a, b) => a.name.localeCompare(b.name, 'tr', { numeric: true })) }));

  const copyButtons = (id) => {
    const im = data.images.find((i) => i.id === id); if (!im) return;
    if (!im.buttons.length) { Alert.alert('Boş', 'Bu sayfada kopyalanacak buton yok.'); return; }
    setClip(im.buttons.map((b) => ({ ...b })));
    Alert.alert('Kopyalandı', `${im.buttons.length} buton panoda. Başka sayfaya yapıştırabilirsin.\n\nİpucu: Önceki/Sonraki hedefleri sayfa sırasına göre çalışır, bu yüzden şablon olarak ideal.`);
  };
  const pasteTo = (ids, mode2) => {
    if (!clip) return;
    const set = new Set(ids);
    setData((d) => ({
      ...d,
      images: d.images.map((i) => {
        if (!set.has(i.id)) return i;
        const fresh = clip.map((b) => ({ ...b, id: uid() }));
        return { ...i, buttons: mode2 === 'replace' ? fresh : [...i.buttons, ...fresh] };
      }),
    }));
    setPasteOpen(false);
    Alert.alert('Tamam', `${ids.length} sayfaya yapıştırıldı.`);
  };

  // ---- paket dışa / içe aktarma
  const doExport = async () => {
    setBusy('Paket hazırlanıyor…');
    try {
      await exportPackage(dataRef.current, (i, n, done) =>
        setBusy(done ? 'Zip oluşturuluyor…' : `Paket hazırlanıyor… ${i}/${n}`));
    } catch (e) { Alert.alert('Dışa aktarılamadı', e.message); }
    setBusy(false);
  };

  const doImport = () => {
    const run = async () => {
      setBusy('Paket açılıyor…');
      try {
        const pkg = await readPackage((i, n) => setBusy(`Paket açılıyor… ${i}/${n}`));
        if (pkg) {
          setData(ensureSections(pkg));
          setScreen({ name: 'home' });
          Alert.alert('Hazır', `${pkg.images.length} sayfa yüklendi.`);
        }
      } catch (e) { Alert.alert('Paket açılamadı', e.message); }
      setBusy(false);
    };
    if (dataRef.current.images.length) {
      Alert.alert('Paket yükle', 'Şu anki içerik silinip seçeceğin paketle değiştirilecek. (Çıpaların korunur.)', [
        { text: 'Vazgeç', style: 'cancel' },
        { text: 'Devam', onPress: run },
      ]);
    } else run();
  };

  const homeId = data.startId && data.images.find((i) => i.id === data.startId) ? data.startId : (data.images[0] && data.images[0].id);
  const play = (id, from = 'library') => setScreen({ name: 'viewer', id: id || homeId, from });
  const secStart = (folder) => { const im = data.images.find((i) => (i.folder || null) === (folder || null)); return im ? im.id : null; };

  if (!ready) return <View style={[s.center, { backgroundColor: C.bg }]}><ActivityIndicator color={C.accent} size="large" /></View>;

  let body;
  if (!mode) {
    body = <Welcome insets={insets} onAuthor={() => chooseMode('author')} onReader={() => chooseMode('reader')} />;
  } else if (screen.name === 'viewer' && data.images.length) {
    const vid = screen.id && data.images.find((i) => i.id === screen.id) ? screen.id : homeId;
    const vimg = data.images.find((i) => i.id === vid);
    body = (
      <Viewer
        key={vid} startId={vid} homeId={secStart(vimg && vimg.folder) || homeId} images={data.images}
        authorMode={AUTHOR} user={user} onUser={setUser} insets={insets}
        onExit={() => setScreen({ name: AUTHOR && screen.from === 'library' ? 'library' : 'home' })}
        onEdit={(id) => setScreen({ name: 'editor', id })}
        onImport={doImport} onResetMode={resetMode} />
    );
  } else if (AUTHOR && screen.name === 'editor' && data.images.find((i) => i.id === screen.id)) {
    body = (
      <Editor
        key={screen.id} image={data.images.find((i) => i.id === screen.id)} images={data.images} insets={insets}
        onBack={() => setScreen({ name: 'library' })} onPlay={() => play(screen.id, 'library')}
        onChange={updateImage} onUploadNew={uploadOne} onPickSound={pickSound} />
    );
  } else if (AUTHOR && screen.name === 'library') {
    body = (
      <Library
        key={screen.fold || 'all'} onMergeFolder={mergeFolder} initialFold={screen.fold || null} onHome={() => setScreen({ name: 'home' })}
        data={data} insets={insets} clip={clip} onAdd={addMany}
        onOpen={(id) => setScreen({ name: 'editor', id })} onPlay={(id) => play(id, 'library')}
        onRename={rename} onSetStart={(id) => setData((d) => ({ ...d, startId: id }))} onRemove={removeImage}
        onCopy={copyButtons} onPasteOne={(id) => pasteTo([id], 'add')} onOpenPaste={() => setPasteOpen(true)}
        onSort={sortAll} onExport={doExport} onImport={doImport} onResetMode={resetMode}
        onSetFolder={setFolder} onNewFolder={newFolder} onRenameFolder={renameFolder} onDeleteFolder={deleteFolder} />
    );
  } else {
    body = (
      <Home
        data={data} user={user} author={AUTHOR} insets={insets}
        onPlay={(id) => play(id, 'home')} onProfile={() => setProfileOpen(true)}
        onLibrary={(fold) => setScreen({ name: 'library', fold })}
        onExport={doExport} onImport={doImport} onPassword={changePassword} onResetMode={resetMode}
        onCover={setCover} onRenameSec={renameFolder} onAddTo={(fid) => addMany(fid)} />
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: C.bg }}>
      <StatusBar hidden={screen.name === 'viewer'} barStyle="light-content" />
      {body}
      {AUTHOR && (
        <PasteModal visible={pasteOpen} images={data.images} clipCount={clip ? clip.length : 0} insets={insets}
          onClose={() => setPasteOpen(false)} onApply={pasteTo} />
      )}
      <NameModal prompt={namePrompt} onDone={finishPrompt} />
      <PassModal prompt={passPrompt} onDone={finishPass} />
      <ProfileModal visible={profileOpen} profile={user.profile || {}} onSave={saveProfileName}
        onPhoto={pickPhoto} onRemovePhoto={removePhoto} onAuthor={AUTHOR ? null : authorFromProfile} onClose={() => setProfileOpen(false)} />
      {!!busy && (
        <View style={[StyleSheet.absoluteFill, s.center, { backgroundColor: 'rgba(0,0,0,0.55)' }]}>
          <ActivityIndicator color="#fff" size="large" />
          <Text style={{ color: '#fff', marginTop: 10 }}>{typeof busy === 'string' ? busy : 'Bekleyin…'}</Text>
        </View>
      )}
    </View>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <Root />
    </SafeAreaProvider>
  );
}

// ------------------------------------------------------------------ stiller
const s = StyleSheet.create({
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 24 },
  title: { color: C.text, fontSize: 30, fontWeight: '800' },
  h2: { color: C.text, fontSize: 19, fontWeight: '700', marginBottom: 8 },
  secTitle: { color: C.sub, fontSize: 12, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 0.6, marginTop: 18, marginBottom: 8 },
  btn: { height: 48, borderRadius: 14, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 14 },
  btnText: { fontSize: 15, fontWeight: '700' },
  input: { backgroundColor: C.card2, color: C.text, borderRadius: 12, paddingHorizontal: 14, height: 46, fontSize: 16, borderWidth: 1, borderColor: C.line },
  dialog: { backgroundColor: C.card, borderRadius: 20, padding: 18, width: '100%', maxWidth: 420, borderWidth: 1, borderColor: C.line },
  menuBtn: { marginTop: 8 },
  header: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 10, gap: 10 },
  hTitle: { flex: 1, color: C.text, fontSize: 17, fontWeight: '700', textAlign: 'center' },
  hBtn: { backgroundColor: C.card2, paddingHorizontal: 12, height: 38, borderRadius: 10, alignItems: 'center', justifyContent: 'center' },
  hBtnText: { color: '#fff', fontWeight: '700' },
  toolbar: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingHorizontal: 12, paddingTop: 10, backgroundColor: C.card, borderTopWidth: 1, borderTopColor: C.line },
  hint: { flex: 1.8, color: C.sub, fontSize: 12, lineHeight: 16 },
  hot: { position: 'absolute', backgroundColor: 'rgba(79,140,255,0.28)', borderWidth: 2, borderColor: C.blue, borderRadius: 6, alignItems: 'center', justifyContent: 'center', overflow: 'hidden' },
  hotSel: { backgroundColor: 'rgba(255,170,40,0.30)', borderColor: '#FFAA28', borderWidth: 3 },
  hotText: { color: '#fff', fontSize: 11, fontWeight: '700', textAlign: 'center', textShadowColor: '#000', textShadowRadius: 3 },
  handle: { position: 'absolute', right: 0, bottom: 0, width: 30, height: 30, backgroundColor: '#FFAA28', borderTopLeftRadius: 10, alignItems: 'center', justifyContent: 'center' },
  sheet: { backgroundColor: C.card, borderTopLeftRadius: 24, borderTopRightRadius: 24, paddingHorizontal: 16, paddingTop: 10, maxHeight: 660 },
  grab: { alignSelf: 'center', width: 40, height: 5, borderRadius: 3, backgroundColor: C.line, marginBottom: 12 },
  row: { flexDirection: 'row', alignItems: 'center', backgroundColor: C.card2, borderRadius: 12, padding: 12, marginBottom: 8, borderWidth: 1.5, borderColor: 'transparent' },
  rowTitle: { color: C.text, fontSize: 15, fontWeight: '600' },
  rowSub: { color: C.sub, fontSize: 12, marginTop: 2 },
  thumbWrap: { backgroundColor: C.card2, borderRadius: 12, overflow: 'hidden', borderWidth: 2, borderColor: 'transparent' },
  thumbName: { color: C.text, fontSize: 12, padding: 6, fontWeight: '600' },
  tick: { position: 'absolute', top: 6, right: 6, width: 24, height: 24, borderRadius: 12, backgroundColor: C.accent, alignItems: 'center', justifyContent: 'center' },
  chip: { flex: 1, height: 42, borderRadius: 12, borderWidth: 1.5, borderColor: C.line, backgroundColor: C.card2, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 8 },
  pill: { height: 36, borderRadius: 18, paddingHorizontal: 14, backgroundColor: C.card2, alignItems: 'center', justifyContent: 'center' },
  pillText: { color: '#fff', fontWeight: '700', fontSize: 13 },
  card: { backgroundColor: C.card, borderRadius: 16, overflow: 'hidden', borderWidth: 1, borderColor: C.line },
  cardName: { color: C.text, fontSize: 15, fontWeight: '700' },
  badge: { position: 'absolute', top: 8, left: 8, backgroundColor: C.ok, borderRadius: 8, paddingHorizontal: 8, paddingVertical: 3 },
  badgeText: { color: '#fff', fontSize: 11, fontWeight: '800' },
  more: { position: 'absolute', top: 8, right: 8, width: 32, height: 32, borderRadius: 16, backgroundColor: 'rgba(0,0,0,0.55)', alignItems: 'center', justifyContent: 'center' },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 40, paddingBottom: 100 },
  bottomBar: { position: 'absolute', left: 0, right: 0, bottom: 0, flexDirection: 'row', gap: 10, paddingHorizontal: 16, paddingTop: 12, backgroundColor: C.card, borderTopWidth: 1, borderTopColor: C.line },
  pin: { position: 'absolute', width: 30, height: 30, borderRadius: 15, borderWidth: 2, borderColor: '#fff', alignItems: 'center', justifyContent: 'center', shadowColor: '#000', shadowOpacity: 0.5, shadowRadius: 4, elevation: 5 },
  tip: { position: 'absolute', alignSelf: 'center', backgroundColor: 'rgba(11,16,32,0.88)', paddingHorizontal: 18, paddingVertical: 12, borderRadius: 16, borderWidth: 1, borderColor: C.accent },
  aRow: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: C.card, borderRadius: 14, padding: 14, marginBottom: 10, borderWidth: 1, borderColor: C.line },
  aDot: { width: 16, height: 16, borderRadius: 8 },
  homeHead: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 14, backgroundColor: '#152040' },
  avatar: { width: 58, height: 58, borderRadius: 18, backgroundColor: '#2B2373', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' },
  avatarBig: { width: 96, height: 96, borderRadius: 30, backgroundColor: '#2B2373', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' },
  resume: { flexDirection: 'row', alignItems: 'center', gap: 14, marginHorizontal: 16, marginTop: 10, padding: 16, borderRadius: 18, backgroundColor: '#3E8E5A' },
  tile: { borderRadius: 16, overflow: 'hidden', backgroundColor: C.card2, borderWidth: 1, borderColor: C.line },
  tileNum: { position: 'absolute', top: 6, left: 6, backgroundColor: 'rgba(0,0,0,0.55)', borderRadius: 9, minWidth: 22, height: 22, paddingHorizontal: 5, alignItems: 'center', justifyContent: 'center' },
  tileCnt: { position: 'absolute', top: 6, right: 6, backgroundColor: C.ok, borderRadius: 9, minWidth: 22, height: 22, paddingHorizontal: 5, alignItems: 'center', justifyContent: 'center' },
  tileName: { position: 'absolute', left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', paddingHorizontal: 8, paddingVertical: 6 },
  check: { width: 24, height: 24, borderRadius: 7, borderWidth: 2, borderColor: C.line, alignItems: 'center', justifyContent: 'center' },
});
