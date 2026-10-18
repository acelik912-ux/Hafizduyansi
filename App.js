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
import React, { useState, useEffect, useRef, useMemo } from 'react';
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
import nacl from 'tweetnacl';
import { pbkdf2Async } from '@noble/hashes/pbkdf2';
import { sha256 } from '@noble/hashes/sha256';
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
  { k: 'custom', t: '✏ Kendi çıpam', c: '#4F8CFF' },
];
const PALETTE = ['#4F8CFF', '#A06BFF', '#FF6BB5', '#FF8A3D', '#FFD23F', '#35C98A', '#2EC4D6', '#FFFFFF'];
const anchColor = (k) => (ANCH.find((a) => a.k === k) || ANCH[0]).c;
const anchColorOf = (a) => (a.type === 'custom' && a.color ? a.color : anchColor(a.type));
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
// ======================================================== ŞİFRELİ PAKET (.hdz)
// Biçim: 'HDZ1' | tuz(16) | yineleme(4) | parça boyutu(4) | düz boyut(4) | parçalar (her biri +16 bayt doğrulama)
// Anahtar: PBKDF2-SHA256(şifre, tuz). Şifreleme: XSalsa20-Poly1305 (tweetnacl), parça başına sayaçlı nonce.
const HDZ_ITER = 60000;
const HDZ_CHUNK = 1024 * 1024;
const B64CH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
const B64REV = (() => { const t = new Uint8Array(256).fill(255); for (let i = 0; i < 64; i++) t[B64CH.charCodeAt(i)] = i; return t; })();
const tick = () => new Promise((r) => setTimeout(r, 0));

function utf8Bytes(str) {
  const out = []; const s = String(str);
  for (let i = 0; i < s.length; i++) {
    let c = s.charCodeAt(i);
    if (c >= 0xd800 && c <= 0xdbff && i + 1 < s.length) { const d = s.charCodeAt(i + 1); if (d >= 0xdc00 && d <= 0xdfff) { c = 0x10000 + ((c - 0xd800) << 10) + (d - 0xdc00); i++; } }
    if (c < 0x80) out.push(c);
    else if (c < 0x800) out.push(0xc0 | (c >> 6), 0x80 | (c & 63));
    else if (c < 0x10000) out.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    else out.push(0xf0 | (c >> 18), 0x80 | ((c >> 12) & 63), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
  }
  return new Uint8Array(out);
}

function bytesToB64(u8) {
  const n = u8.length, outLen = Math.ceil(n / 3) * 4;
  const codes = new Uint8Array(outLen);
  let o = 0, i = 0;
  for (; i + 2 < n; i += 3) {
    const v = (u8[i] << 16) | (u8[i + 1] << 8) | u8[i + 2];
    codes[o++] = B64CH.charCodeAt((v >> 18) & 63); codes[o++] = B64CH.charCodeAt((v >> 12) & 63);
    codes[o++] = B64CH.charCodeAt((v >> 6) & 63); codes[o++] = B64CH.charCodeAt(v & 63);
  }
  if (n - i === 1) {
    const v = u8[i] << 16;
    codes[o++] = B64CH.charCodeAt((v >> 18) & 63); codes[o++] = B64CH.charCodeAt((v >> 12) & 63); codes[o++] = 61; codes[o++] = 61;
  } else if (n - i === 2) {
    const v = (u8[i] << 16) | (u8[i + 1] << 8);
    codes[o++] = B64CH.charCodeAt((v >> 18) & 63); codes[o++] = B64CH.charCodeAt((v >> 12) & 63); codes[o++] = B64CH.charCodeAt((v >> 6) & 63); codes[o++] = 61;
  }
  const parts = [];
  for (let k = 0; k < outLen; k += 8192) parts.push(String.fromCharCode.apply(null, codes.subarray(k, Math.min(outLen, k + 8192))));
  return parts.join('');
}

function b64ToBytes(input) {
  const str = input.indexOf('\n') >= 0 || input.indexOf('\r') >= 0 ? input.replace(/[\r\n]/g, '') : input;
  let len = str.length, pad = 0;
  if (str.charCodeAt(len - 1) === 61) pad++;
  if (str.charCodeAt(len - 2) === 61) pad++;
  const out = new Uint8Array((len * 3) / 4 - pad);
  let o = 0;
  for (let i = 0; i < len; i += 4) {
    const a = B64REV[str.charCodeAt(i)], b = B64REV[str.charCodeAt(i + 1)], c = B64REV[str.charCodeAt(i + 2)], d = B64REV[str.charCodeAt(i + 3)];
    const v = (a << 18) | (b << 12) | ((c & 63) << 6) | (d & 63);
    if (o < out.length) out[o++] = (v >> 16) & 255;
    if (o < out.length) out[o++] = (v >> 8) & 255;
    if (o < out.length) out[o++] = v & 255;
  }
  return out;
}

function randBytes(n) {   // tuz için: benzersiz olması yeter (gizli olması gerekmez)
  const seed = Date.now() + ':' + Math.random() + ':' + Math.random() + ':' + Math.random() * 1e17;
  return nacl.hash(utf8Bytes(seed)).slice(0, n);
}
const putU32 = (a, o, v) => { a[o] = (v >>> 24) & 255; a[o + 1] = (v >>> 16) & 255; a[o + 2] = (v >>> 8) & 255; a[o + 3] = v & 255; };
const getU32 = (a, o) => ((a[o] << 24) | (a[o + 1] << 16) | (a[o + 2] << 8) | a[o + 3]) >>> 0;
const chunkNonce = (i) => { const n = new Uint8Array(24); n[0] = i & 255; n[1] = (i >>> 8) & 255; n[2] = (i >>> 16) & 255; n[3] = (i >>> 24) & 255; return n; };
const deriveKey = (password, salt, iters) => pbkdf2Async(sha256, utf8Bytes(password), salt, { c: iters, dkLen: 32, asyncTick: 20 });
const isHdzB64 = (b64) => b64.startsWith('SERa');                    // 'HDZ' -> base64 'SERa'

async function encryptHdz(plain, password, onProgress) {
  const salt = randBytes(16);
  const key = await deriveKey(password, salt, HDZ_ITER);
  const nCh = Math.max(1, Math.ceil(plain.length / HDZ_CHUNK));
  const out = new Uint8Array(32 + plain.length + nCh * 16);
  out.set([0x48, 0x44, 0x5a, 0x31], 0); out.set(salt, 4);
  putU32(out, 20, HDZ_ITER); putU32(out, 24, HDZ_CHUNK); putU32(out, 28, plain.length);
  let off = 32;
  for (let i = 0; i < nCh; i++) {
    const box = nacl.secretbox(plain.subarray(i * HDZ_CHUNK, Math.min(plain.length, (i + 1) * HDZ_CHUNK)), chunkNonce(i), key);
    out.set(box, off); off += box.length;
    onProgress && onProgress(i + 1, nCh);
    await tick();
  }
  return out;
}

async function decryptHdz(bytes, password, onProgress) {
  const bad = (code, msg) => { const e = new Error(msg); e.code = code; return e; };
  if (bytes.length < 32 || bytes[0] !== 0x48 || bytes[1] !== 0x44 || bytes[2] !== 0x5a || bytes[3] !== 0x31) throw bad('FORMAT', 'Bu şifreli bir Hafız Dünyası paketi değil.');
  const salt = bytes.slice(4, 20), iters = getU32(bytes, 20), chunk = getU32(bytes, 24), total = getU32(bytes, 28);
  if (iters < 1000 || iters > 500000 || chunk < 1024 || chunk > 16 * 1024 * 1024) throw bad('FORMAT', 'Paket başlığı geçersiz.');
  const nCh = Math.max(1, Math.ceil(total / chunk));
  if (bytes.length !== 32 + total + nCh * 16) throw bad('CORRUPT', 'Dosya eksik ya da bozuk (tam indirilmemiş olabilir).');
  const key = await deriveKey(password, salt, iters);
  const plain = new Uint8Array(total);
  let off = 32, po = 0;
  for (let i = 0; i < nCh; i++) {
    const clen = Math.min(total - i * chunk, chunk) + 16;
    const opened = nacl.secretbox.open(bytes.subarray(off, off + clen), chunkNonce(i), key);
    if (!opened) throw bad(i === 0 ? 'BADPW' : 'CORRUPT', i === 0 ? 'Şifre yanlış ya da dosya bozuk.' : 'Dosya bozuk.');
    plain.set(opened, po); po += opened.length; off += clen;
    onProgress && onProgress(i + 1, nCh);
    await tick();
  }
  return plain;
}

async function exportPackage(data, onProgress, sectionId, password) {
  let fname = 'hafiz_dunyasi_tum';
  if (sectionId) {                           // yalnızca bu bölümü paketle
    const f = (data.folders || []).find((x) => x.id === sectionId);
    const imgs = data.images.filter((i) => i.folder === sectionId);
    if (!f || !imgs.length) throw new Error('Bu bölümde resim yok.');
    data = { startId: imgs[0].id, folders: [f], images: imgs };
    fname = 'hafiz_' + safeName(sectionId) + '_' + safeName(f.name);
  }
  const zip = new JSZip();
  const soundMap = {};                       // yerel dosya adı -> paketteki ad
  let sn = 0;
  const mapSound = (snd) => {
    if (!snd || !snd.file) return null;
    if (!soundMap[snd.file]) soundMap[snd.file] = 's' + (++sn) + '.' + extOf(snd.file, 'mp3');
    return { name: snd.name, file: soundMap[snd.file] };
  };
  const meta = {
    version: 5, kind: sectionId ? 'section' : 'all', section: sectionId || null, startId: data.startId,
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
  if (password) {                                  // şifreli paket (.hdz)
    const zipBytes = await zip.generateAsync({ type: 'uint8array', compression: 'STORE' }); // resimler zaten sıkışık
    onProgress && onProgress(0, 0, 'key');
    const enc = await encryptHdz(zipBytes, password, (i, n) => onProgress && onProgress(i, n, 'enc'));
    const path = FileSystem.cacheDirectory + fname + '.hdz';
    await FileSystem.writeAsStringAsync(path, bytesToB64(enc), { encoding: 'base64' });
    if (!(await Sharing.isAvailableAsync())) throw new Error('Bu cihazda paylaşım desteklenmiyor.');
    await Sharing.shareAsync(path, { mimeType: 'application/octet-stream', dialogTitle: 'Şifreli paketi paylaş', UTI: 'public.data' });
  } else {                                         // şifresiz düz zip
    const out = await zip.generateAsync({ type: 'base64', compression: 'STORE' });
    const path = FileSystem.cacheDirectory + fname + '.zip';
    await FileSystem.writeAsStringAsync(path, out, { encoding: 'base64' });
    if (!(await Sharing.isAvailableAsync())) throw new Error('Bu cihazda paylaşım desteklenmiyor.');
    await Sharing.shareAsync(path, { mimeType: 'application/zip', dialogTitle: 'Paketi paylaş', UTI: 'public.zip-archive' });
  }
}

// Kullanıcıya dosya seçtirir, paketi açar, resimleri uygulama klasörüne yazar.
// Başarılıysa {images, startId} döner; iptalse null.
async function readPackage(onProgress, beforeWipe, askPw) {
  const r = await DocumentPicker.getDocumentAsync({ type: '*/*', copyToCacheDirectory: true });
  if (r.canceled || !r.assets || !r.assets.length) return null;
  const b64 = await FileSystem.readAsStringAsync(r.assets[0].uri, { encoding: 'base64' });
  let zip;
  if (isHdzB64(b64)) {                               // şifreli paket (.hdz)
    if (!askPw) throw new Error('Şifre sorulamadı.');
    const bytes = b64ToBytes(b64);
    let plain = null;
    const pw = await askPw(async (text) => {
      try { plain = await decryptHdz(bytes, text, (i, n) => onProgress && onProgress(i, n, 'dec')); return true; }
      catch (e) { if (e.code === 'BADPW') return false; throw e; }
    });
    if (pw === null || !plain) return null;
    zip = await JSZip.loadAsync(plain);
  } else zip = await JSZip.loadAsync(b64, { base64: true });   // eski şifresiz zip
  const pj = zip.file('project.json');
  if (!pj) throw new Error('Bu bir Hafız Dünyası paketi değil (project.json bulunamadı).');
  const meta = JSON.parse(await pj.async('string'));
  if (meta && meta.kind === 'cuz') return await readCuzPackage(zip, meta, onProgress);   // meyve bahçesi paketi
  if (!meta || !Array.isArray(meta.images) || !meta.images.length) throw new Error('Pakette resim yok.');

  const isSection = meta.kind === 'section';
  if (!isSection) {                                   // tam paket: önce onay, sonra eski içeriği sil
    if (beforeWipe && !(await beforeWipe())) return null;
    await FileSystem.deleteAsync(DIR, { idempotent: true });
    await FileSystem.deleteAsync(ADIR, { idempotent: true });
  }
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
  return { images, startId, folders, kind: isSection ? 'section' : 'all', section: meta.section || (folders[0] && folders[0].id) || null };
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
  const [title, setTitle] = useState('');
  const [color, setColor] = useState('#4F8CFF');
  useEffect(() => { if (edit) { setType(edit.a.type || 'stuck'); setNote(edit.a.note || ''); setTitle(edit.a.title || ''); setColor(edit.a.color || '#4F8CFF'); } }, [edit]);
  if (!edit) return null;
  return (
    <Modal transparent visible animationType="slide" onRequestClose={onClose}>
      <View style={{ flex: 1, justifyContent: 'flex-end' }}>
        <Pressable style={StyleSheet.absoluteFill} onPress={onClose}><View style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.5)' }} /></Pressable>
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
          <View style={[s.sheet, { paddingBottom: insets.bottom + 14 }]}>
            <View style={s.grab} />
            <Text style={s.h2}>📌 Hafız çıpası</Text>
            <ScrollView keyboardShouldPersistTaps="handled" style={{ maxHeight: 460 }}>
            <Text style={s.secTitle}>Bu yer senin için ne?</Text>
            <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
              {ANCH.map((a) => (
                <Pressable key={a.k} onPress={() => setType(a.k)}
                  style={[s.chip, { borderColor: a.k === 'custom' ? color : a.c }, type === a.k && { backgroundColor: a.k === 'custom' ? color : a.c }]}>
                  <Text style={{ color: '#fff', fontWeight: '700' }}>{a.t}</Text>
                </Pressable>
              ))}
            </View>
            {type === 'custom' && (
              <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 12 }}>
                {PALETTE.map((c) => (
                  <Pressable key={c} onPress={() => setColor(c)}
                    style={{ width: 34, height: 34, borderRadius: 17, backgroundColor: c, borderWidth: color === c ? 3 : 1, borderColor: color === c ? '#fff' : C.line }} />
                ))}
              </View>
            )}
            <Text style={s.secTitle}>Çıpa adı (kendin yaz, isteğe bağlı)</Text>
            <TextInput
              value={title} onChangeText={setTitle} maxLength={30} placeholder="Örn: Sure geçişi"
              placeholderTextColor={C.sub} style={s.input} />
            <Text style={s.secTitle}>Not (isteğe bağlı)</Text>
            <TextInput
              value={note} onChangeText={setNote} multiline placeholder="Örn: 3. satırda hep karıştırıyorum"
              placeholderTextColor={C.sub} style={[s.input, { height: 90, paddingTop: 12, textAlignVertical: 'top' }]} />
            </ScrollView>
            <View style={{ flexDirection: 'row', gap: 10, marginTop: 16 }}>
              {!edit.isNew && <Btn title="Sil" kind="danger" onPress={onDelete} style={{ flex: 1 }} />}
              <Btn title="Vazgeç" kind="ghost" onPress={onClose} style={{ flex: 1 }} />
              <Btn title="Kaydet" onPress={() => onSave({ ...edit.a, type, note: note.trim(), title: title.trim(), color })} style={{ flex: 1 }} />
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
              <View style={[s.aDot, { backgroundColor: anchColorOf(item) }]} />
              <View style={{ flex: 1 }}>
                <Text style={s.rowTitle} numberOfLines={1}>{item.title || item.pname}</Text>
                {!!item.title && <Text style={s.rowSub} numberOfLines={1}>{item.pname}</Text>}
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
function Viewer({ startId, homeId, images, authorMode, user, onUser, onExit, onHome, onEdit, onImport, onResetMode, insets }) {
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

  // ---- iki parmakla yakınlaştırma (1x–5x), yakınken tek parmakla kaydırma
  const zScale = useRef(new Animated.Value(1)).current;
  const zTx = useRef(new Animated.Value(0)).current;
  const zTy = useRef(new Animated.Value(0)).current;
  const zs = useRef({ s: 1, tx: 0, ty: 0 });
  const zoomedRef = useRef(false);
  const dims = useRef({});
  const [zoomed, setZoomed] = useState(false);
  dims.current = { w: width, h: height, rw: rect.w, rh: rect.h };
  const applyZ = (s, tx, ty) => {
    const d = dims.current;
    s = Math.min(5, Math.max(1, s));
    const mx = Math.max(0, (d.rw * s - d.w) / 2), my = Math.max(0, (d.rh * s - d.h) / 2);
    tx = Math.min(mx, Math.max(-mx, tx)); ty = Math.min(my, Math.max(-my, ty));
    zs.current = { s, tx, ty };
    zScale.setValue(s); zTx.setValue(tx); zTy.setValue(ty);
    const z = s > 1.02;
    if (z !== zoomedRef.current) { zoomedRef.current = z; setZoomed(z); }
  };
  const pinch = useRef(null);
  const origin = useRef({ gx: 0, gy: 0, tx: 0, ty: 0, n: 0 });
  const wantZoom = (e, g) => e.nativeEvent.touches.length >= 2 || (zs.current.s > 1.02 && (Math.abs(g.dx) > 6 || Math.abs(g.dy) > 6));
  const zoomPan = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => false,
    onMoveShouldSetPanResponderCapture: wantZoom,
    onMoveShouldSetPanResponder: wantZoom,
    onPanResponderTerminationRequest: () => false,
    onPanResponderGrant: (e) => {
      pinch.current = null;
      origin.current = { gx: 0, gy: 0, tx: zs.current.tx, ty: zs.current.ty, n: e.nativeEvent.touches.length };
    },
    onPanResponderMove: (e, g) => {
      const ts = e.nativeEvent.touches, d = dims.current;
      if (ts.length !== origin.current.n) {                 // parmak sayısı değişti: referansı yenile
        origin.current = { gx: g.dx, gy: g.dy, tx: zs.current.tx, ty: zs.current.ty, n: ts.length };
        pinch.current = null;
      }
      if (ts.length >= 2) {
        const dist = Math.hypot(ts[0].pageX - ts[1].pageX, ts[0].pageY - ts[1].pageY);
        const mx = (ts[0].pageX + ts[1].pageX) / 2, my = (ts[0].pageY + ts[1].pageY) / 2;
        if (!pinch.current) pinch.current = { d0: Math.max(1, dist), mx0: mx, my0: my, ...zs.current };
        const p = pinch.current, s = Math.min(5, Math.max(1, p.s * dist / p.d0)), cx = d.w / 2, cy = d.h / 2;
        applyZ(s, (mx - cx) - (s / p.s) * (p.mx0 - cx - p.tx), (my - cy) - (s / p.s) * (p.my0 - cy - p.ty));
      } else {
        const o = origin.current;
        applyZ(zs.current.s, o.tx + (g.dx - o.gx), o.ty + (g.dy - o.gy));
      }
    },
    onPanResponderRelease: () => { pinch.current = null; if (zs.current.s < 1.05) applyZ(1, 0, 0); },
    onPanResponderTerminate: () => { pinch.current = null; if (zs.current.s < 1.05) applyZ(1, 0, 0); },
  })).current;
  useEffect(() => { applyZ(1, 0, 0); }, [img.id]);       // sayfa değişince yakınlaştırmayı sıfırla

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
      return { ...u, hide: false, anchors: { ...(u.anchors || {}), [pid]: nl } };
    });
    setAnchorEdit(null);
  };
  const removeAnchor = (pid, id) =>
    onUser((u) => ({ ...u, anchors: { ...(u.anchors || {}), [pid]: ((u.anchors || {})[pid] || []).filter((x) => x.id !== id) } }));

  const openMenuAt = (e) => {
    const { pageX, pageY } = e.nativeEvent;
    const z = zs.current, cx = width / 2, cy = height / 2;     // ekran -> sayfa koordinatı (yakınlaştırma ters çevrilir)
    const px = cx + (pageX - cx - z.tx) / z.s, py = cy + (pageY - cy - z.ty) / z.s;
    setPress({ x: (px - rect.x) / rect.w, y: (py - rect.y) / rect.h });
    setMenu(true);
  };
  const showHints = () => { setMenu(false); setHints(true); setTimeout(() => setHints(false), 2500); };
  const lastOk = user.last && user.last !== cur && images.find((i) => i.id === user.last);

  return (
    <View style={{ flex: 1, backgroundColor: '#000' }}>
      <View style={{ flex: 1 }} {...zoomPan.panHandlers}>
      <Animated.View style={{ flex: 1, transform: [{ translateX: zTx }, { translateY: zTy }, { scale: zScale }] }}>
      <Pressable
        style={{ flex: 1 }} delayLongPress={600}
        onLongPress={openMenuAt}>
        <Animated.View style={{ flex: 1, opacity: fade, transform: [{ translateX: slide }] }}>
          <View style={{ position: 'absolute', left: rect.x, top: rect.y, width: rect.w, height: rect.h }}>
            <Image source={srcOf(img)} style={{ width: '100%', height: '100%' }} resizeMode="stretch" resizeMethod="scale" />
            {img.buttons.map((b) => (
              <Pressable
                key={b.id} onPress={() => go(b)} onLongPress={openMenuAt} delayLongPress={600}
                style={{
                  position: 'absolute', left: b.x * rect.w, top: b.y * rect.h, width: b.w * rect.w, height: b.h * rect.h,
                  backgroundColor: hints ? 'rgba(79,140,255,0.35)' : 'transparent',
                  borderWidth: hints ? 2 : 0, borderColor: C.blue,
                }} />
            ))}
          </View>
        </Animated.View>
        <View pointerEvents="box-none" style={{ position: 'absolute', left: rect.x, top: rect.y, width: rect.w, height: rect.h, zIndex: 50, elevation: 10 }}>
          {!user.hide && pageAnchors.map((a) => (
              <Pressable
                key={a.id} hitSlop={14} onLongPress={openMenuAt} delayLongPress={600}
                onPress={() => setAnchorEdit({ pid: img.id, a, isNew: false })}
                style={[s.pin, { left: a.x * rect.w - 10, top: a.y * rect.h - 10, backgroundColor: anchColorOf(a) }]}>
                <Text style={{ fontSize: 10 }}>{a.note ? '📝' : '📌'}</Text>
                {!!a.title && (
                  <View pointerEvents="none" style={[s.pinTag, a.x > 0.55 ? { right: 24 } : { left: 24 }, { backgroundColor: anchColorOf(a) }]}>
                    <Text style={{ color: anchColorOf(a) === '#FFFFFF' || anchColorOf(a) === '#FFD23F' ? '#111' : '#fff', fontSize: 10, fontWeight: '800' }} numberOfLines={1}>{a.title}</Text>
                  </View>
                )}
              </Pressable>
            ))}
        </View>
      </Pressable>
      </Animated.View>
      </View>

      {zoomed && (
        <Pressable onPress={() => applyZ(1, 0, 0)} hitSlop={10}
          style={{ position: 'absolute', right: 12, bottom: insets.bottom + 16, zIndex: 70, backgroundColor: 'rgba(0,0,0,0.65)', borderRadius: 18, paddingHorizontal: 14, paddingVertical: 8, borderWidth: 1, borderColor: 'rgba(255,255,255,0.25)' }}>
          <Text style={{ color: '#fff', fontWeight: '800', fontSize: 13 }}>⤢ Sığdır</Text>
        </Pressable>
      )}

      <Pressable onPress={onHome || onExit} hitSlop={10}
        style={{ position: 'absolute', left: 12, top: insets.top + 8, zIndex: 70, flexDirection: 'row', alignItems: 'center', gap: 6,
          backgroundColor: 'rgba(0,0,0,0.6)', borderRadius: 18, paddingHorizontal: 12, paddingVertical: 7, borderWidth: 1, borderColor: 'rgba(255,255,255,0.25)' }}>
        <Text style={{ fontSize: 15 }}>🏠</Text>
        <Text style={{ color: '#fff', fontWeight: '800', fontSize: 13 }}>Ana ekran</Text>
      </Pressable>

      {pageAnchors.length > 0 && (
        <Pressable onPress={() => onUser((u) => ({ ...u, hide: !u.hide }))} hitSlop={10}
          style={{ position: 'absolute', right: 12, top: insets.top + 8, zIndex: 60, backgroundColor: 'rgba(0,0,0,0.65)', borderRadius: 16, paddingHorizontal: 12, paddingVertical: 6 }}>
          <Text style={{ color: '#fff', fontWeight: '800' }}>{user.hide ? '🙈' : '📌'} {pageAnchors.length}</Text>
        </Pressable>
      )}

      {tip && (
        <View pointerEvents="none" style={[s.tip, { bottom: insets.bottom + 30 }]}>
          <Text style={{ color: '#fff', textAlign: 'center', lineHeight: 20 }}>
            Ekrana <Text style={{ fontWeight: '800' }}>uzun basarak</Text> menüyü aç ve 📌 çıpa koy.{'\n'}<Text style={{ fontWeight: '800' }}>İki parmakla</Text> yakınlaştır.
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
function Library({ onMove, onMergeFolder, initialFold, onHome, data, insets, clip, onAdd, onOpen, onPlay, onRename, onSetStart, onRemove, onCopy, onPasteOne, onOpenPaste, onSort, onExport, onImport, onResetMode, onSetFolder, onNewFolder, onRenameFolder, onDeleteFolder }) {
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
  const reorder = !!cf && cf !== 'none' && !q.trim();       // bir bölüm seçiliyken sıra okları açılır
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
            <Text style={[s.pillText, { color: '#1A1500' }]}>⬆ Tümünü dışa aktar (şifreli)</Text>
          </Pressable>
          <Pressable style={s.pill} onPress={onImport}><Text style={s.pillText}>⬇ Paket içe aktar</Text></Pressable>
          <Pressable style={s.pill} onPress={() => onSort(cf)}><Text style={s.pillText}>{cf && cf !== 'none' ? 'Bu bölümü A→Z sırala' : 'A→Z / 1→30 sırala'}</Text></Pressable>
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
        {folders.length > 0 && <Text style={{ color: C.sub, fontSize: 12, marginTop: 6 }}>{cf && cf !== 'none' ? 'Sıra: ▲▼ oklarıyla değiştir. 1. sayfa bölüme girince ilk açılır.' : 'Bölüm adına basılı tut: yeniden adlandır'}</Text>}
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
          renderItem={({ item, index }) => (
            <Pressable
              onPress={() => onOpen(item.id)} onLongPress={() => setActionImg(item)}
              style={({ pressed }) => [s.card, { width: cw, opacity: pressed ? 0.85 : 1 }]}>
              <Image source={srcOf(item)} style={{ width: '100%', height: cw * 0.75 }} resizeMode="cover" />
              <View style={{ padding: 10 }}>
                <Text style={s.cardName} numberOfLines={1}>{item.name}</Text>
                <Text style={{ color: C.sub, fontSize: 12, marginTop: 2 }} numberOfLines={1}>{item.buttons.length} buton{cf === null && item.folder && fmap[item.folder] ? ' · 📁 ' + fmap[item.folder] : ''}</Text>
              </View>
              {reorder && (
                <>
                  <View style={[s.ordNum, { top: cw * 0.75 - 36 }]}><Text style={{ color: '#fff', fontWeight: '900', fontSize: 13 }}>{index + 1}</Text></View>
                  <View style={s.ordBox}>
                    <Pressable onPress={() => onMove(item.id, 'up')} hitSlop={6} style={[s.ordBtn, index === 0 && { opacity: 0.35 }]}><Text style={s.ordTxt}>▲</Text></Pressable>
                    <Pressable onPress={() => onMove(item.id, 'down')} hitSlop={6} style={[s.ordBtn, index === list.length - 1 && { opacity: 0.35 }]}><Text style={s.ordTxt}>▼</Text></Pressable>
                  </View>
                </>
              )}
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
            <Btn title="⏫ Bölümün ilk sayfası yap (en başa)" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onMove(im.id, 'top'))} />
            <Btn title="⏬ En sona al" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onMove(im.id, 'bottom'))} />
            <Btn title="⌂ Uygulama başlangıç sayfası yap" kind="ghost" style={s.menuBtn} onPress={() => act((im) => onSetStart(im.id))} />
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
  const [wait, setWait] = useState(false);
  useEffect(() => { setA(''); setB(''); setErr(''); setWait(false); }, [prompt]);
  if (!prompt) return null;
  const create = prompt.mode === 'create';
  const min = prompt.min || 4;
  const submit = async () => {
    if (wait) return;
    if (create) {
      if (a.length < min) return setErr(`En az ${min} karakter olmalı.`);
      if (a !== b) return setErr('İki şifre aynı değil.');
      onDone(a);
    } else if (prompt.check) {
      setWait(true);
      try { const ok = await prompt.check(a); if (!ok) setErr('Şifre yanlış.'); else onDone(a || 'ok'); }
      catch (e) { setErr(e.message || 'Hata oluştu.'); }
      setWait(false);
    } else onDone(a || 'ok');
  };
  return (
    <Modal transparent animationType="fade" visible onRequestClose={() => onDone(null)}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]}>
        <View style={s.dialog}>
          <Text style={s.h2}>{prompt.title || (create ? '🔒 Yazar şifresi oluştur' : '🔒 Yazar şifresi')}</Text>
          <Text style={{ color: C.sub, marginBottom: 10, lineHeight: 19 }}>
            {prompt.desc || (create ? 'Yazar moduna girerken bu şifre sorulacak. Unutursan uygulama verisini silmek gerekir; bir yere not et.' : 'Yazar moduna girmek için şifreni yaz.')}
          </Text>
          <TextInput value={a} onChangeText={(v) => { setA(v); setErr(''); }} autoFocus secureTextEntry
            placeholder="Şifre" placeholderTextColor={C.sub} style={s.input} onSubmitEditing={create ? undefined : submit} />
          {create && <TextInput value={b} onChangeText={(v) => { setB(v); setErr(''); }} secureTextEntry
            placeholder="Şifre (tekrar)" placeholderTextColor={C.sub} style={[s.input, { marginTop: 8 }]} onSubmitEditing={submit} />}
          {!!err && <Text style={{ color: C.danger, marginTop: 8 }}>{err}</Text>}
          <View style={{ flexDirection: 'row', gap: 10, marginTop: 14 }}>
            <Btn title="Vazgeç" kind="ghost" onPress={() => onDone(null)} style={{ flex: 1 }} />
            {prompt.optional && <Btn title="Şifresiz" kind="ghost" onPress={() => onDone('')} style={{ flex: 1 }} />}
            <Btn title={wait ? 'Çözülüyor…' : 'Tamam'} onPress={submit} disabled={wait} style={{ flex: 1 }} />
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
// ---- alt gezinme çubuğu (başparmakla erişim): Ana Sayfa · Bahçe · Profil
const NAV_H = 76;
function BottomBar({ active, insets, items }) {
  return (
    <View pointerEvents="box-none" style={{ position: 'absolute', left: 12, right: 12, bottom: insets.bottom + 8, zIndex: 60 }}>
      <View style={{ height: 62, borderRadius: 31, backgroundColor: 'rgba(21,27,46,0.97)', borderWidth: 1, borderColor: C.line, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-around', paddingHorizontal: 8, elevation: 12, shadowColor: '#000', shadowOpacity: 0.4, shadowRadius: 8, shadowOffset: { width: 0, height: 3 } }}>
        {items.map((it) => {
          const on = it.k === active;
          return (
            <Pressable key={it.k} onPress={on ? undefined : it.onPress} hitSlop={6}
              style={{ height: 48, minWidth: on ? 108 : 64, borderRadius: 24, paddingHorizontal: 14, alignItems: 'center', justifyContent: 'center', flexDirection: on ? 'row' : 'column', gap: on ? 8 : 0, backgroundColor: on ? C.accent : 'transparent' }}>
              <Text style={{ fontSize: on ? 20 : 22 }}>{it.icon}</Text>
              <Text style={{ color: on ? '#1A1500' : C.sub, fontWeight: '800', fontSize: on ? 14 : 11 }}>{it.label}</Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

function Home({ nav, cuz, onOpenCuz, onExportSec, data, user, author, insets, onPlay, onProfile, onLibrary, onExport, onImport, onPassword, onResetMode, onCover, onRenameSec, onAddTo }) {
  const { width } = useWindowDimensions();
  const [menu, setMenu] = useState(null);
  const profile = user.profile || {};
  const secs = (data.folders || []).filter((f) => isSec(f.id));
  const countOf = (id) => data.images.filter((i) => i.folder === id).length;
  const firstOf = (id) => { const im = data.images.find((i) => i.folder === id); return im ? im.id : null; };
  const tw = Math.floor((width - 32 - 14) / 2) - 1;   // 2 sütun, ekranı doldurur
  const last = user.last && data.images.find((i) => i.id === user.last);
  const tap = (f) => {
    const cn = parseInt(String(f.id).replace('sec', ''), 10);
    if (cuz && cuz[cn]) { onOpenCuz(cn); return; }               // meyve bahçesi (cüz) içeriği varsa onu aç
    const st = firstOf(f.id);
    if (st) onPlay(st);
    else if (author) setMenu(f);
    else Alert.alert(f.name, 'Bu bölüm henüz boş.');
  };
  const act = (fn) => { const f = menu; setMenu(null); setTimeout(() => fn(f), 250); };
  return (
    <View style={{ flex: 1, backgroundColor: C.bg }}>
      <ScrollView contentContainerStyle={{ paddingBottom: insets.bottom + NAV_H + 24 }} showsVerticalScrollIndicator={false}>
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


        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 14 }} contentContainerStyle={{ gap: 8, paddingHorizontal: 16 }}>
          {author ? (
            <>
              <Pressable style={[s.pill, { backgroundColor: C.accent }]} onPress={() => onLibrary(null)}><Text style={[s.pillText, { color: '#1A1500' }]}>✎ Tüm resimler</Text></Pressable>
              <Pressable style={s.pill} onPress={onExport}><Text style={s.pillText}>⬆ Tümünü dışa aktar</Text></Pressable>
              <Pressable style={s.pill} onPress={onImport}><Text style={s.pillText}>⬇ İçe aktar</Text></Pressable>
              <Pressable style={s.pill} onPress={onPassword}><Text style={s.pillText}>🔒 Şifre</Text></Pressable>
              <Pressable style={s.pill} onPress={onResetMode}><Text style={s.pillText}>⚙ Mod seç</Text></Pressable>
            </>
          ) : (
            <Pressable style={[s.pill, { backgroundColor: C.accent }]} onPress={onImport}><Text style={[s.pillText, { color: '#1A1500' }]}>📦 Paket aç</Text></Pressable>
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
            const n = countOf(f.id) + (cuz && cuz[parseInt(String(f.id).replace('sec', ''), 10)] ? 1 : 0);
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

      <BottomBar active="home" insets={insets} items={nav} />

      <Modal transparent visible={!!menu} animationType="fade" onRequestClose={() => setMenu(null)}>
        <Pressable style={[s.center, { backgroundColor: 'rgba(0,0,0,0.6)' }]} onPress={() => setMenu(null)}>
          <View style={s.dialog}>
            <Text style={s.h2} numberOfLines={1}>{menu && menu.name}</Text>
            <Btn title="🖼 Kapak resmi seç" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onCover(f.id))} />
            <Btn title="Aa Adını değiştir" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onRenameSec(f.id))} />
            <Btn title="＋ Bu bölüme resim ekle" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onAddTo(f.id))} />
            <Btn title="✎ Bu bölümün resimlerini düzenle" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onLibrary(f.id))} />
            {menu && !!firstOf(menu.id) && <Btn title="📦 Bu bölümü dışa aktar (şifreli)" kind="ghost" style={s.menuBtn} onPress={() => act((f) => onExportSec(f.id))} />}
            {menu && !!firstOf(menu.id) && <Btn title="▶ Bölümü aç" style={s.menuBtn} onPress={() => act((f) => onPlay(firstOf(f.id)))} />}
          </View>
        </Pressable>
      </Modal>
    </View>
  );
}

// =============================================================== MEYVE BAHÇESİ (CÜZ) MODÜLÜ
// Bir cüz = 20 ağaç = 20 sayfa. Ağaç 1: Fatiha + Bakara'nın süslü ilk sayfaları (olduğu gibi).
// Ağaç 2-20: mushaf sayfası; her ağaçta en çok 5 meyve = 5 ayet başı (siyah, kırmızı, sarı, yeşil, lacivert).
// 5'ten fazlaysa "SAYFA DEVAMI" ile aynı sayfanın ikinci ağaç ekranı açılır.
const TREE_IMGS = [];            // gömülü varsayılan ağaç yok: Yazar modunda galeriden eklenir
const GARDEN_BG = null;           // gömülü varsayılan arka plan yok: Yazar modunda galeriden seçilir
const TREE_NAMES = ['Kayısı', 'Portakal', 'Trabzon Hurması', 'Antep Fıstığı', 'Çam', 'Limon', 'Armut', 'Muz', 'Kiraz', 'Muşmula',
  'Kuşburnu', 'Medine Hurması', 'Dut', 'Şeftali', 'Zeytin', 'İncir', 'Nar', 'Üzüm', 'Elma', 'Badem'];
const TREE_ANCH = [[0.5, 0.25], [0.711, 0.358], [0.289, 0.358], [0.711, 0.5], [0.289, 0.5]];   // ağaç görselindeki 5 meyve konumu (oran)
const FRUIT_COL = ['#111111', '#D32F2F', '#F2A900', '#2E9E4F', '#1F3C88'];                      // sıra: siyah, kırmızı, sarı, yeşil, lacivert
const FRUIT_SIDE = ['top', 'right', 'left', 'right', 'left'];
const GOLD = '#D4AF37';

function Plate({ title, onPress, style, small }) {
  return (
    <Pressable onPress={onPress} hitSlop={8}
      style={({ pressed }) => [{ backgroundColor: '#0B0B0B', borderWidth: 2, borderColor: GOLD, borderRadius: 10, paddingHorizontal: small ? 10 : 16, paddingVertical: small ? 6 : 9, opacity: pressed ? 0.8 : 1 }, style]}>
      <Text style={{ color: '#F2C94C', fontWeight: '900', fontSize: small ? 13 : 16, letterSpacing: 0.5 }}>{title}</Text>
    </Pressable>
  );
}
function RoundBtn({ icon, onPress }) {
  return (
    <Pressable onPress={onPress} hitSlop={8}
      style={{ width: 44, height: 44, borderRadius: 22, backgroundColor: 'rgba(0,0,0,0.62)', borderWidth: 1.5, borderColor: GOLD, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 20 }}>{icon}</Text>
    </Pressable>
  );
}

// bahçedeki ağaç: hafifçe sallanır, dokununca zıplar
function TreeTile({ i, w, onOpen }) {
  const sway = useRef(new Animated.Value(0)).current;
  const pop = useRef(new Animated.Value(1)).current;
  useEffect(() => {
    const dur = 2400 + (i % 5) * 330;
    const a = Animated.loop(Animated.sequence([
      Animated.timing(sway, { toValue: 1, duration: dur, delay: (i % 4) * 220, useNativeDriver: true }),
      Animated.timing(sway, { toValue: 0, duration: dur, useNativeDriver: true }),
    ]));
    a.start(); return () => a.stop();
  }, []);
  const th = w * 0.92 * (4 / 3);
  const press = () => {
    Animated.sequence([
      Animated.timing(pop, { toValue: 1.2, duration: 140, useNativeDriver: true }),
      Animated.spring(pop, { toValue: 1, friction: 3, useNativeDriver: true }),
    ]).start();
    setTimeout(onOpen, 260);
  };
  return (
    <Pressable onPress={press} style={{ width: w, alignItems: 'center', marginBottom: 6 }}>
      <View style={{ position: 'absolute', bottom: 32, width: w * 0.55, height: 12, borderRadius: 20, backgroundColor: 'rgba(0,0,0,0.28)' }} />
      <Animated.View style={{ transform: [{ scale: pop }, { translateY: th / 2 }, { rotate: sway.interpolate({ inputRange: [0, 1], outputRange: ['-1.8deg', '1.8deg'] }) }, { translateY: -th / 2 }] }}>
        <Image source={TREE_IMGS[i]} style={{ width: w * 0.92, height: th }} resizeMode="contain" />
      </Animated.View>
      <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: 'rgba(11,11,11,0.78)', borderWidth: 1.5, borderColor: GOLD, borderRadius: 14, paddingHorizontal: 9, paddingVertical: 3, marginTop: -6 }}>
        <Text style={{ color: '#F2C94C', fontWeight: '900', fontSize: 13 }}>{i + 1}</Text>
        <Text style={{ color: '#fff', fontWeight: '700', fontSize: 11 }} numberOfLines={1}>{TREE_NAMES[i]}</Text>
      </View>
    </Pressable>
  );
}

function Fruit({ x, y, d, color, n, delay, onPress }) {
  const bob = useRef(new Animated.Value(0)).current;
  const pulse = useRef(new Animated.Value(1)).current;
  useEffect(() => {
    const a = Animated.loop(Animated.sequence([
      Animated.timing(bob, { toValue: 1, duration: 1700, delay, useNativeDriver: true }),
      Animated.timing(bob, { toValue: 0, duration: 1700, useNativeDriver: true }),
    ]));
    a.start(); return () => a.stop();
  }, []);
  const tap = () => {
    Animated.sequence([
      Animated.timing(pulse, { toValue: 1.4, duration: 120, useNativeDriver: true }),
      Animated.timing(pulse, { toValue: 1, duration: 150, useNativeDriver: true }),
    ]).start();
    setTimeout(onPress, 170);
  };
  return (
    <Animated.View style={{ position: 'absolute', left: x - d / 2, top: y - d / 2, width: d, height: d, transform: [{ translateY: bob.interpolate({ inputRange: [0, 1], outputRange: [-3, 3] }) }, { scale: pulse }] }}>
      <Pressable onPress={tap} hitSlop={12}
        style={{ width: d, height: d, borderRadius: d / 2, borderWidth: 3.5, borderColor: color, backgroundColor: 'rgba(255,255,255,0.06)' }}>
        <View style={{ position: 'absolute', top: -9, right: -9, width: 21, height: 21, borderRadius: 11, backgroundColor: color, borderWidth: 1.5, borderColor: '#fff', alignItems: 'center', justifyContent: 'center' }}>
          <Text style={{ color: color === '#F2A900' ? '#222' : '#fff', fontSize: 11, fontWeight: '900' }}>{n}</Text>
        </View>
      </Pressable>
    </Animated.View>
  );
}

function VerseLabel({ ay, x, y, w, h, color, onPress }) {
  return (
    <Pressable onPress={onPress}
      style={{ position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 12, borderWidth: 3, borderColor: color, backgroundColor: '#FFF6D9', alignItems: 'center', justifyContent: 'center', elevation: 5, shadowColor: '#000', shadowOpacity: 0.35, shadowRadius: 4, shadowOffset: { width: 0, height: 2 } }}>
      <Image source={{ uri: DIR + ay.start.file }} style={{ width: w - 10, height: h - 8 }} resizeMode="contain" />
    </Pressable>
  );
}

function AyahPanel({ item, idx, total, W, H, onPrev, onNext, onClose }) {
  const sc = useRef(new Animated.Value(0.85)).current;
  const op = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    sc.setValue(0.85); op.setValue(0);
    Animated.parallel([Animated.spring(sc, { toValue: 1, friction: 7, useNativeDriver: true }), Animated.timing(op, { toValue: 1, duration: 180, useNativeDriver: true })]).start();
  }, [idx]);
  const a = item.a, cw = Math.min(W - 24, 520), iw = cw - 30;
  const nx = useRef(onNext), pv = useRef(onPrev), ix = useRef([idx, total]); nx.current = onNext; pv.current = onPrev; ix.current = [idx, total];
  const swipe = useRef(PanResponder.create({                // sağa/sola kaydır: önceki / sonraki ayet
    onMoveShouldSetPanResponder: (e, g) => Math.abs(g.dx) > 14 && Math.abs(g.dx) > Math.abs(g.dy) * 2,
    onPanResponderRelease: (e, g) => {
      const [i, n] = ix.current;
      if (g.dx < -50 && i < n - 1) nx.current(); else if (g.dx > 50 && i > 0) pv.current();
    },
  })).current;
  return (
    <Animated.View {...swipe.panHandlers} style={{ width: cw, maxHeight: H * 0.88, opacity: op, transform: [{ scale: sc }], backgroundColor: '#FFF8E1', borderRadius: 18, borderWidth: 3, borderColor: GOLD, padding: 14 }}>
      <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 8 }}>
        <View style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: FRUIT_COL[item.k], marginRight: 8 }} />
        <Text style={{ flex: 1, color: '#3B2A10', fontWeight: '900', fontSize: 16 }}>{a.sname} · {a.no}. ayet</Text>
        <Pressable onPress={onClose} hitSlop={10} style={{ width: 34, height: 34, borderRadius: 17, backgroundColor: '#3B2A10', alignItems: 'center', justifyContent: 'center' }}>
          <Text style={{ color: '#fff', fontSize: 16, fontWeight: '900' }}>✕</Text>
        </Pressable>
      </View>
      <ScrollView style={{ maxHeight: H * 0.6 }} showsVerticalScrollIndicator={false}>
        <Image source={{ uri: DIR + a.full.file }} style={{ width: iw, aspectRatio: a.full.w / a.full.h, alignSelf: 'center' }} resizeMode="contain" />
      </ScrollView>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
        <Plate small title="◀ ÖNCEKİ" onPress={idx > 0 ? onPrev : undefined} style={{ opacity: idx > 0 ? 1 : 0.35 }} />
        <Text style={{ color: '#6B5A3A', fontWeight: '700' }}>{idx + 1} / {total}</Text>
        <Plate small title="SONRAKİ ▶" onPress={idx < total - 1 ? onNext : undefined} style={{ opacity: idx < total - 1 ? 1 : 0.35 }} />
      </View>
    </Animated.View>
  );
}

// ======================================================= ORMAN GEZGİNİ (derinlikli ağaç seçici)
// 20 ağaç = 10 çift. Ön çift büyük, arkaya doğru küçülür. Parmağı AŞAĞI çekince öndeki çift aşağı kayıp çıkar,
// arkadaki çift öne gelir (ormanda ilerlersin). Yukarı çekince geri dönersin. Bırakınca en yakın çifte oturur.
// Her ağacın altında o sayfanın başı (ilk ayet başı) bir kutuda durur. Öndeki ağaca/kutuya dokununca sayfa açılır;
// arkadaki ağaca dokunursan önce öne gelir.
const FOREST = { a: 0.6, horizon: 0.30, x0: 0.26, wt: 0.54, boxH: 66, step: 150 };
const D_SAMPLES = [10, 8, 6, 5, 4, 3.5, 3, 2.5, 2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25, 0, -0.25, -0.5, -0.75, -1, -1.2];
const fS = (d) => 1 / (1 + FOREST.a * d);
const fOp = (d) => (d >= 0 ? Math.max(0.55, 1 - 0.06 * d) : Math.max(0, 1 + d * 1.3));
const fBox = (d) => (d > 2.6 ? 0 : d > 1.6 ? 2.6 - d : d >= -0.4 ? 1 : Math.max(0, 1 + (d + 0.4) * 2));

// ---- Yazar: ağaç görselini değiştir + 5 meyve konumunu elle ayarla (telefondan, derleme gerekmez)
const clamp01 = (v) => Math.min(1, Math.max(0, v));
const treeSrc = (trees, i) => (trees && trees[i] && trees[i].file ? { uri: DIR + trees[i].file } : (TREE_IMGS.length ? TREE_IMGS[i % TREE_IMGS.length] : null));
const treeAnch = (trees, i) => (trees && trees[i] && trees[i].anch) || TREE_ANCH;

function AnchorHandle({ k, pos, bw, bh, onMove }) {
  const start = useRef([0, 0]);
  const posRef = useRef(pos); posRef.current = pos;
  const mv = useRef(onMove); mv.current = onMove;
  const dim = useRef([bw, bh]); dim.current = [bw, bh];
  const pr = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onPanResponderGrant: () => { start.current = [...posRef.current]; },
    onPanResponderMove: (e, g) => mv.current(k, [clamp01(start.current[0] + g.dx / dim.current[0]), clamp01(start.current[1] + g.dy / dim.current[1])]),
  })).current;
  return (
    <View {...pr.panHandlers} style={{ position: 'absolute', left: pos[0] * bw - 26, top: pos[1] * bh - 26, width: 52, height: 52, alignItems: 'center', justifyContent: 'center' }}>
      <View style={{ width: 40, height: 40, borderRadius: 20, borderWidth: 4, borderColor: FRUIT_COL[k], backgroundColor: 'rgba(255,255,255,0.12)' }} />
      <View style={{ position: 'absolute', top: 2, right: 2, width: 21, height: 21, borderRadius: 11, backgroundColor: FRUIT_COL[k], borderWidth: 1.5, borderColor: '#fff', alignItems: 'center', justifyContent: 'center' }}>
        <Text style={{ color: k === 2 ? '#222' : '#fff', fontSize: 11, fontWeight: '900' }}>{k + 1}</Text>
      </View>
    </View>
  );
}
function AnchorEditor({ idx, trees, W, H, insets, onSave, onClose }) {
  const [a, setA] = useState(() => treeAnch(trees, idx).map((p) => [...p]));
  const bw = Math.min(W - 24, (H - insets.top - insets.bottom - 230) * 0.75), bh = bw * (4 / 3);
  const move = (k, p) => setA((cur) => cur.map((q, i) => (i === k ? p : q)));
  return (
    <Modal visible animationType="slide" onRequestClose={onClose}>
      <View style={{ flex: 1, backgroundColor: '#10182B', paddingTop: insets.top + 8, paddingBottom: insets.bottom + 10, alignItems: 'center' }}>
        <Text style={{ color: '#fff', fontWeight: '900', fontSize: 16 }}>Meyve konumları · {TREE_NAMES[idx % TREE_NAMES.length]}</Text>
        <Text style={{ color: '#98A2BC', fontSize: 12, textAlign: 'center', marginTop: 4, marginBottom: 8, paddingHorizontal: 16 }}>
          5 halkayı ağaçtaki meyvelerin üstüne sürükle. Sıra: 1 siyah (üst), 2 kırmızı, 3 sarı, 4 yeşil, 5 lacivert.
        </Text>
        <View style={{ width: bw, height: bh, backgroundColor: '#7FB6E8', borderRadius: 10, overflow: 'hidden' }}>
          <Image source={treeSrc(trees, idx)} style={{ width: bw, height: bh }} resizeMode="contain" />
          {a.map((p, k) => <AnchorHandle key={k} k={k} pos={p} bw={bw} bh={bh} onMove={move} />)}
        </View>
        <View style={{ flexDirection: 'row', gap: 10, marginTop: 12, paddingHorizontal: 12 }}>
          <Btn title="Varsayılan" kind="ghost" onPress={() => setA(TREE_ANCH.map((p) => [...p]))} style={{ flex: 1 }} />
          <Btn title="İptal" kind="ghost" onPress={onClose} style={{ flex: 1 }} />
          <Btn title="Kaydet" onPress={() => onSave(a)} style={{ flex: 1 }} />
        </View>
      </View>
    </Modal>
  );
}

// ---- ağacı sağa sola sürükleme (Yazar "yerleştirme" modu) + yer tutucu
function DragTree({ enabled, av, W, getS, onEnd, style, children }) {
  const base = useRef(0);
  const en = useRef(enabled); en.current = enabled;
  const gs = useRef(getS); gs.current = getS;
  const end = useRef(onEnd); end.current = onEnd;
  const pr = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => en.current,
    onMoveShouldSetPanResponder: () => en.current,
    onPanResponderTerminationRequest: () => false,
    onPanResponderGrant: () => { av.stopAnimation((v) => { base.current = v; }); },
    onPanResponderMove: (e, g) => av.setValue(base.current + g.dx / Math.max(0.3, gs.current())),
    onPanResponderRelease: () => { av.stopAnimation((v) => end.current(v / W)); },
  })).current;
  return <View {...pr.panHandlers} style={style}>{children}</View>;
}
function TreeHole({ author }) {
  return (
    <View style={{ flex: 1, margin: 10, borderRadius: 16, borderWidth: 2, borderStyle: 'dashed', borderColor: 'rgba(255,255,255,0.7)', backgroundColor: 'rgba(0,0,0,0.14)', alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 34 }}>🌳</Text>
      <Text style={{ color: '#fff', fontWeight: '800', fontSize: 12, textAlign: 'center', marginTop: 4 }}>{author ? 'Basılı tut:\nağaç görseli ekle' : 'Ağaç yok'}</Text>
    </View>
  );
}

function ForestPicker({ bottomPad, arrange, onMove, trees, author, onMenu, pages, W, H, insets, onOpen }) {
  const pairs = Math.ceil(pages.length / 2);
  const pos = useRef(new Animated.Value(0)).current;
  const posRef = useRef(0);
  const base = useRef(0);
  const lastFront = useRef(0);
  const [front, setFront] = useState(0);
  const [moved, setMoved] = useState(false);
  const hint = useRef(new Animated.Value(0)).current;
  const dxAVs = useRef({}).current;
  const dxAV = (i) => { if (!dxAVs[i]) dxAVs[i] = new Animated.Value(((trees && trees[i] && trees[i].dx) || 0) * W); return dxAVs[i]; };
  useEffect(() => { Object.keys(dxAVs).forEach((kk) => dxAVs[kk].setValue(((trees && trees[kk] && trees[kk].dx) || 0) * W)); }, [trees]);
  useEffect(() => {
    const id = pos.addListener(({ value }) => {
      posRef.current = value;
      const r = Math.round(value);
      if (r !== lastFront.current) { lastFront.current = r; setFront(r); if (r > 0) setMoved(true); }
    });
    const a = Animated.loop(Animated.sequence([
      Animated.timing(hint, { toValue: 1, duration: 800, useNativeDriver: true }),
      Animated.timing(hint, { toValue: 0, duration: 800, useNativeDriver: true }),
    ]));
    a.start();
    return () => { pos.removeListener(id); a.stop(); };
  }, []);
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const settle = (t) => Animated.spring(pos, { toValue: t, friction: 8, tension: 60, useNativeDriver: true }).start();
  const pan = useRef(PanResponder.create({
    onMoveShouldSetPanResponder: (e, g) => Math.abs(g.dy) > 8 && Math.abs(g.dy) > Math.abs(g.dx),
    onPanResponderGrant: () => { pos.stopAnimation((v) => { base.current = v; }); },
    onPanResponderMove: (e, g) => pos.setValue(clamp(base.current + g.dy / FOREST.step, -0.15, pairs - 1 + 0.15)),
    onPanResponderRelease: (e, g) => settle(clamp(Math.round(posRef.current + g.vy * 0.35), 0, pairs - 1)),
    onPanResponderTerminate: () => settle(clamp(Math.round(posRef.current), 0, pairs - 1)),
  })).current;

  const wt = W * FOREST.wt, ht = wt * (4 / 3), yH = H * FOREST.horizon, yF = H - insets.bottom - 118 - (bottomPad || 0);
  const hc = ht + 8 + FOREST.boxH, k = ht - hc / 2, x0 = W * FOREST.x0;
  const tap = (idx, j) => { if (Math.abs(posRef.current - j) < 0.4) onOpen(idx); else settle(j); };

  const items = [];
  for (let j = pairs - 1; j >= 0; j--) {
    for (let side = 0; side < 2; side++) {
      const idx = 2 * j + side; if (idx >= pages.length) continue;
      const sg = side === 0 ? -1 : 1, page = pages[idx];
      const inp = D_SAMPLES.map((d) => j - d);
      const mk = (fn) => pos.interpolate({ inputRange: inp, outputRange: D_SAMPLES.map(fn), extrapolate: 'clamp' });
      const sc = mk(fS), ty = mk((d) => (yF - yH) * (fS(d) - 1)), txb = mk((d) => sg * x0 * (fS(d) - 1)), op = mk(fOp), bo = mk(fBox);
      const tx = Animated.add(txb, Animated.multiply(dxAV(idx), sc));
      items.push(
        <Animated.View key={idx} style={{ position: 'absolute', left: W / 2 + sg * x0 - wt / 2, top: yF - ht, width: wt, height: hc, opacity: op,
          transform: [{ translateX: tx }, { translateY: ty }, { translateY: k }, { scale: sc }, { translateY: -k }] }}>
          <View style={{ position: 'absolute', left: wt * 0.2, top: ht - 9, width: wt * 0.6, height: 16, borderRadius: 20, backgroundColor: 'rgba(0,0,0,0.30)' }} />
          <DragTree enabled={!!arrange} av={dxAV(idx)} W={W} getS={() => fS(j - posRef.current)} onEnd={(v) => onMove(idx, v)} style={{ width: wt, height: ht }}>
            <Pressable onPress={() => tap(idx, j)} onLongPress={author ? () => onMenu(idx) : undefined} delayLongPress={500}
              style={{ width: wt, height: ht, borderRadius: 12, borderWidth: arrange ? 2 : 0, borderStyle: 'dashed', borderColor: GOLD }}>
              {treeSrc(trees, idx)
                ? <Image source={treeSrc(trees, idx)} style={{ width: wt, height: ht }} resizeMode="contain" />
                : <TreeHole author={author} />}
            </Pressable>
          </DragTree>
          <Animated.View style={{ position: 'absolute', left: 0, top: ht + 8, width: wt, height: FOREST.boxH, opacity: bo }}>
            <Pressable onPress={() => tap(idx, j)}
              style={{ flex: 1, borderRadius: 12, borderWidth: 3, borderColor: GOLD, backgroundColor: '#FFF6D9', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
              <View style={{ position: 'absolute', top: 0, left: 0, backgroundColor: '#0B0B0B', paddingHorizontal: 8, paddingVertical: 2, borderBottomRightRadius: 10 }}>
                <Text style={{ color: '#F2C94C', fontWeight: '900', fontSize: 11 }}>{idx + 1} · {TREE_NAMES[idx % TREE_NAMES.length]}</Text>
              </View>
              {page.kind === 'special'
                ? <Text style={{ color: '#3B2A10', fontWeight: '900', fontSize: 15, marginTop: 10 }}>Fatiha · Bakara</Text>
                : <Image source={{ uri: DIR + page.ayat[0].start.file }} style={{ width: wt - 24, height: FOREST.boxH - 28, marginTop: 14 }} resizeMode="contain" />}
            </Pressable>
          </Animated.View>
        </Animated.View>,
      );
    }
  }
  return (
    <View style={{ flex: 1 }} {...pan.panHandlers}>
      {items}
      <View style={{ position: 'absolute', right: 8, top: yH + 20, alignItems: 'center', gap: 6 }}>
        {Array.from({ length: pairs }).map((_, i) => (
          <View key={i} style={{ width: i === front ? 9 : 6, height: i === front ? 9 : 6, borderRadius: 5, backgroundColor: i === front ? GOLD : 'rgba(255,255,255,0.55)' }} />
        ))}
      </View>
      {!moved && (
        <Animated.View pointerEvents="none" style={{ position: 'absolute', left: 0, right: 0, top: insets.top + 118, alignItems: 'center', opacity: hint, transform: [{ translateY: hint.interpolate({ inputRange: [0, 1], outputRange: [-4, 8] }) }] }}>
          <View style={{ backgroundColor: 'rgba(0,0,0,0.6)', borderWidth: 1.5, borderColor: GOLD, borderRadius: 16, paddingHorizontal: 14, paddingVertical: 6 }}>
            <Text style={{ color: '#fff', fontWeight: '800' }}>▼  aşağı çek, ormanda ilerle</Text>
          </View>
        </Animated.View>
      )}
    </View>
  );
}

// ================================================================ SERBEST ORMAN (en fazla 30 resim)
// Bağımsız ekran: istediğin resimleri (en fazla 30) ekle; resimler ikili sıralarla derinliğe dizilir.
// Parmağı aşağı çek: ön çift kayıp çıkar, arkadaki öne gelir. Yazar: sağa sola yerleştir, boyutu ayarla,
// altına yazı yaz, istersen bir cüze bağla. Hepsi uygulamadan, derleme gerekmez.
const FF_MAX = 30;
const FF_DEF = { wt: 0.54, x0: 0.26, a: 0.6, horizon: 0.30 };
const stepBtn = { width: 38, height: 38, borderRadius: 19, backgroundColor: '#1F2740', alignItems: 'center', justifyContent: 'center' };
function Stepper({ label, value, step, min, max, onChange, fmt }) {
  const dec = () => onChange(Math.max(min, +(value - step).toFixed(3)));
  const inc = () => onChange(Math.min(max, +(value + step).toFixed(3)));
  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', paddingVertical: 3 }}>
      <Text style={{ color: '#fff', fontWeight: '700', flex: 1 }}>{label}</Text>
      <Pressable onPress={dec} hitSlop={6} style={stepBtn}><Text style={{ color: '#fff', fontSize: 20, fontWeight: '900' }}>－</Text></Pressable>
      <Text style={{ color: GOLD, fontWeight: '900', width: 58, textAlign: 'center' }}>{fmt ? fmt(value) : value}</Text>
      <Pressable onPress={inc} hitSlop={6} style={stepBtn}><Text style={{ color: '#fff', fontSize: 20, fontWeight: '900' }}>＋</Text></Pressable>
    </View>
  );
}

function FreeForest({ items, cfg, arrange, author, W, H, insets, bottomPad, onMove, onTap, onMenu }) {
  const c = { ...FF_DEF, ...(cfg || {}) };
  const sOf = (d) => 1 / Math.max(0.12, 1 + c.a * d);
  const pairs = Math.max(1, Math.ceil(items.length / 2));
  const pairsRef = useRef(pairs); pairsRef.current = pairs;
  const pos = useRef(new Animated.Value(0)).current;
  const posRef = useRef(0), base = useRef(0), lastFront = useRef(0);
  const [front, setFront] = useState(0);
  const dxAVs = useRef({}).current;
  const dxAV = (it) => { if (!dxAVs[it.id]) dxAVs[it.id] = new Animated.Value((it.dx || 0) * W); return dxAVs[it.id]; };
  useEffect(() => { items.forEach((it) => { if (dxAVs[it.id]) dxAVs[it.id].setValue((it.dx || 0) * W); }); }, [items]);
  useEffect(() => {
    const id = pos.addListener(({ value }) => {
      posRef.current = value;
      const r = Math.round(value);
      if (r !== lastFront.current) { lastFront.current = r; setFront(r); }
    });
    return () => pos.removeListener(id);
  }, []);
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const settle = (t) => Animated.spring(pos, { toValue: t, friction: 8, tension: 60, useNativeDriver: true }).start();
  const pan = useRef(PanResponder.create({
    onMoveShouldSetPanResponder: (e, g) => Math.abs(g.dy) > 8 && Math.abs(g.dy) > Math.abs(g.dx),
    onPanResponderGrant: () => { pos.stopAnimation((v) => { base.current = v; }); },
    onPanResponderMove: (e, g) => pos.setValue(clamp(base.current + g.dy / FOREST.step, -0.15, pairsRef.current - 1 + 0.15)),
    onPanResponderRelease: (e, g) => settle(clamp(Math.round(posRef.current + g.vy * 0.35), 0, pairsRef.current - 1)),
    onPanResponderTerminate: () => settle(clamp(Math.round(posRef.current), 0, pairsRef.current - 1)),
  })).current;

  const wt = W * c.wt, yH = H * c.horizon, yF = H - insets.bottom - 112 - (bottomPad || 0), x0 = W * c.x0;
  const tap = (it, j) => { if (Math.abs(posRef.current - j) < 0.4) onTap(it); else settle(j); };
  if (!items.length) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 30 }}>
        <Text style={{ fontSize: 46 }}>🌲</Text>
        <Text style={{ color: '#fff', fontWeight: '900', fontSize: 17, textAlign: 'center', marginTop: 8, textShadowColor: '#000', textShadowRadius: 4 }}>
          {author ? 'Henüz resim yok' : 'Burada henüz bir şey yok'}
        </Text>
        {author && <Text style={{ color: '#fff', textAlign: 'center', marginTop: 6, textShadowColor: '#000', textShadowRadius: 4 }}>Sol üstteki ＋ ile galeriden resim ekle (en fazla {FF_MAX}).</Text>}
      </View>
    );
  }
  const nodes = [];
  for (let j = pairs - 1; j >= 0; j--) {
    for (let side = 0; side < 2; side++) {
      const idx = 2 * j + side; if (idx >= items.length) continue;
      const it = items[idx], sg = side === 0 ? -1 : 1;
      const asp = Math.min(2, Math.max(0.5, it.w && it.h ? it.h / it.w : 4 / 3));
      const iw = wt * (it.sc || 1), ih = iw * asp, hasLab = !!(it.label && it.label.trim());
      const hc = ih + (hasLab ? 8 + 44 : 0), k = ih - hc / 2;
      const inp = D_SAMPLES.map((d) => j - d);
      const mk = (fn) => pos.interpolate({ inputRange: inp, outputRange: D_SAMPLES.map(fn), extrapolate: 'clamp' });
      const sc = mk(sOf), ty = mk((d) => (yF - yH) * (sOf(d) - 1)), txb = mk((d) => sg * x0 * (sOf(d) - 1)), op = mk(fOp), bo = mk(fBox);
      const tx = Animated.add(txb, Animated.multiply(dxAV(it), sc));
      nodes.push(
        <Animated.View key={it.id} style={{ position: 'absolute', left: W / 2 + sg * x0 - iw / 2, top: yF - ih, width: iw, height: hc, opacity: op,
          transform: [{ translateX: tx }, { translateY: ty }, { translateY: k }, { scale: sc }, { translateY: -k }] }}>
          <View style={{ position: 'absolute', left: iw * 0.2, top: ih - 9, width: iw * 0.6, height: 16, borderRadius: 20, backgroundColor: 'rgba(0,0,0,0.30)' }} />
          <DragTree enabled={!!arrange} av={dxAV(it)} W={W} getS={() => sOf(j - posRef.current)} onEnd={(v) => onMove(it.id, v)} style={{ width: iw, height: ih }}>
            <Pressable onPress={() => tap(it, j)} onLongPress={author ? () => onMenu(it.id) : undefined} delayLongPress={500}
              style={{ width: iw, height: ih, borderRadius: 12, borderWidth: arrange ? 2 : 0, borderStyle: 'dashed', borderColor: GOLD }}>
              <Image source={{ uri: DIR + it.file }} style={{ width: iw, height: ih }} resizeMode="contain" />
            </Pressable>
          </DragTree>
          {hasLab && (
            <Animated.View style={{ position: 'absolute', left: 0, top: ih + 8, width: iw, height: 44, opacity: bo }}>
              <Pressable onPress={() => tap(it, j)} onLongPress={author ? () => onMenu(it.id) : undefined}
                style={{ flex: 1, borderRadius: 12, borderWidth: 3, borderColor: GOLD, backgroundColor: '#FFF6D9', alignItems: 'center', justifyContent: 'center', paddingHorizontal: 6 }}>
                <Text style={{ color: '#3B2A10', fontWeight: '900', fontSize: 13, textAlign: 'center' }} numberOfLines={2}>{it.label}</Text>
              </Pressable>
            </Animated.View>
          )}
        </Animated.View>,
      );
    }
  }
  return (
    <View style={{ flex: 1 }} {...pan.panHandlers}>
      {nodes}
      <View style={{ position: 'absolute', right: 8, top: yH + 20, alignItems: 'center', gap: 6 }}>
        {Array.from({ length: pairs }).map((_, i) => (
          <View key={i} style={{ width: i === front ? 9 : 6, height: i === front ? 9 : 6, borderRadius: 5, backgroundColor: i === front ? GOLD : 'rgba(255,255,255,0.55)' }} />
        ))}
      </View>
    </View>
  );
}

function FreeForestScreen({ forest, ui, author, insets, nav, cuzData, onAdd, onMove, onUpdate, onDelete, onReorder, onCfg, onPickBg, onUi, onLabel, onLink, onReplace, onResetPos, onClear, onOpenCuz }) {
  const { width: W, height: H } = useWindowDimensions();
  const items = forest.items || [];
  const cfg = { ...FF_DEF, ...(forest.cfg || {}) };
  const [arrange, setArrange] = useState(false);
  const [settings, setSettings] = useState(false);
  const [menuId, setMenuId] = useState(null);
  const [preview, setPreview] = useState(null);
  const mi = menuId ? items.find((x) => x.id === menuId) : null;
  const tapItem = (it) => { if (it.cuz && cuzData && cuzData[it.cuz]) onOpenCuz(it.cuz); else setPreview(it); };
  const bg = ui.bgForest && ui.bgForest.file ? { uri: DIR + ui.bgForest.file } : null;
  return (
    <View style={{ flex: 1, backgroundColor: C.bg }}>
      {bg
        ? <Image source={bg} style={StyleSheet.absoluteFill} resizeMode="cover" />
        : <View style={StyleSheet.absoluteFill}><View style={{ flex: 3, backgroundColor: '#8EC9F2' }} /><View style={{ flex: 7, backgroundColor: '#4C8F57' }} /></View>}
      <FreeForest items={items} cfg={forest.cfg} arrange={arrange} author={author} W={W} H={H} insets={insets} bottomPad={NAV_H - 8}
        onMove={onMove} onTap={tapItem} onMenu={setMenuId} />
      <View pointerEvents="box-none" style={{ position: 'absolute', left: 0, right: 0, top: insets.top + 10, flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, gap: 8 }}>
        {author ? <RoundBtn icon="＋" onPress={onAdd} /> : <View style={{ width: 44 }} />}
        <View style={{ flex: 1, alignItems: 'center' }}>
          {!ui.hideTitle && (
            <View style={{ backgroundColor: '#0B0B0B', borderWidth: 2.5, borderColor: GOLD, borderRadius: 12, paddingHorizontal: 22, paddingVertical: 8 }}>
              <Text style={{ color: '#F2C94C', fontWeight: '900', fontSize: 20, letterSpacing: 1 }}>ORMAN</Text>
            </View>
          )}
        </View>
        {author ? (<><RoundBtn icon="✥" onPress={() => setArrange(!arrange)} /><RoundBtn icon="⚙" onPress={() => setSettings(true)} /></>) : <View style={{ width: 44 }} />}
      </View>
      {arrange && (
        <View style={{ position: 'absolute', left: 12, right: 12, top: insets.top + 66, flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: 'rgba(0,0,0,0.74)', borderWidth: 1.5, borderColor: GOLD, borderRadius: 14, padding: 8 }}>
          <Text style={{ flex: 1, color: '#fff', fontWeight: '700', fontSize: 12 }}>✥ Resmi sağa sola sürükle; bırakınca kaydolur</Text>
          <Plate small title="BİTTİ" onPress={() => setArrange(false)} />
        </View>
      )}
      <BottomBar active="forest" insets={insets} items={nav} />

      <Modal transparent visible={!!mi} animationType="fade" onRequestClose={() => setMenuId(null)}>
        <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.65)', alignItems: 'center', justifyContent: 'center' }} onPress={() => setMenuId(null)}>
          {mi && (
            <Pressable onPress={() => {}} style={{ width: Math.min(W - 40, 380), backgroundColor: C.card, borderRadius: 16, padding: 16, gap: 8 }}>
              <Text style={{ color: '#fff', fontWeight: '900', fontSize: 17 }}>{items.findIndex((x) => x.id === mi.id) + 1}. resim</Text>
              <Stepper label="Boyut" value={mi.sc || 1} step={0.1} min={0.4} max={2} fmt={(v) => '%' + Math.round(v * 100)} onChange={(v) => onUpdate(mi.id, { sc: v })} />
              <Btn title="🖼 Resmi değiştir" kind="ghost" onPress={() => { const id = mi.id; setMenuId(null); setTimeout(() => onReplace(id), 250); }} />
              <Btn title="Aa Altına yazı yaz" kind="ghost" onPress={() => { const id = mi.id; setMenuId(null); setTimeout(() => onLabel(id), 250); }} />
              <Btn title={mi.cuz ? `🔗 Bağlı cüz: ${mi.cuz} (değiştir)` : '🔗 Bir cüze bağla'} kind="ghost" onPress={() => { const id = mi.id; setMenuId(null); setTimeout(() => onLink(id), 250); }} />
              <View style={{ flexDirection: 'row', gap: 8 }}>
                <Btn title="⇧ Öne al" kind="ghost" style={{ flex: 1 }} onPress={() => onReorder(mi.id, -1)} />
                <Btn title="⇩ Arkaya al" kind="ghost" style={{ flex: 1 }} onPress={() => onReorder(mi.id, 1)} />
              </View>
              <Btn title="↔ Konumu sıfırla" kind="ghost" onPress={() => onUpdate(mi.id, { dx: 0 })} />
              <Btn title="🗑 Sil" kind="danger" onPress={() => { const id = mi.id; setMenuId(null); onDelete(id); }} />
            </Pressable>
          )}
        </Pressable>
      </Modal>

      <Modal transparent visible={settings} animationType="fade" onRequestClose={() => setSettings(false)}>
        <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.65)', alignItems: 'center', justifyContent: 'center' }} onPress={() => setSettings(false)}>
          <Pressable onPress={() => {}} style={{ width: Math.min(W - 40, 390), backgroundColor: C.card, borderRadius: 16, padding: 16, gap: 6 }}>
            <Text style={{ color: '#fff', fontWeight: '900', fontSize: 17, marginBottom: 2 }}>Orman ayarları · {items.length}/{FF_MAX} resim</Text>
            <Stepper label="Resim boyutu" value={cfg.wt} step={0.04} min={0.3} max={0.8} fmt={(v) => '%' + Math.round(v * 100)} onChange={(v) => onCfg({ wt: v })} />
            <Stepper label="Sağ-sol açıklık" value={cfg.x0} step={0.02} min={0.1} max={0.42} fmt={(v) => '%' + Math.round(v * 100)} onChange={(v) => onCfg({ x0: v })} />
            <Stepper label="Derinlik etkisi" value={cfg.a} step={0.1} min={0.2} max={0.8} fmt={(v) => v.toFixed(1)} onChange={(v) => onCfg({ a: v })} />
            <Stepper label="Ufuk yüksekliği" value={cfg.horizon} step={0.02} min={0.18} max={0.5} fmt={(v) => '%' + Math.round(v * 100)} onChange={(v) => onCfg({ horizon: v })} />
            <Btn title="＋ Resim ekle" onPress={() => { setSettings(false); setTimeout(onAdd, 250); }} />
            <Btn title="🖼 Orman arka planı seç" kind="ghost" onPress={() => { setSettings(false); setTimeout(() => onPickBg('bgForest'), 250); }} />
            <Btn title={ui.hideTitle ? 'Plakayı göster' : 'ORMAN plakasını gizle'} kind="ghost" onPress={() => onUi({ hideTitle: !ui.hideTitle })} />
            <Btn title="↔ Tüm konumları sıfırla" kind="ghost" onPress={() => { onResetPos(); setSettings(false); }} />
            <Btn title="🗑 Tüm resimleri sil" kind="danger" onPress={() => { setSettings(false); onClear(); }} />
          </Pressable>
        </Pressable>
      </Modal>

      <Modal transparent visible={!!preview} animationType="fade" onRequestClose={() => setPreview(null)}>
        <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.9)', alignItems: 'center', justifyContent: 'center' }} onPress={() => setPreview(null)}>
          {preview && (
            <>
              <Image source={{ uri: DIR + preview.file }} style={{ width: W - 24, height: H * 0.76 }} resizeMode="contain" />
              {!!preview.label && <Text style={{ color: '#fff', fontWeight: '900', fontSize: 18, marginTop: 10, textAlign: 'center' }}>{preview.label}</Text>}
              <Text style={{ color: C.sub, marginTop: 8 }}>Kapatmak için dokun</Text>
            </>
          )}
        </Pressable>
      </Modal>
    </View>
  );
}

function CuzReader({ nav, ui, onPickBg, onUi, onBgReset, onTreeMove, onTreesResetPos, cd, insets, onHome, trees, author, onPickTree, onTreeAnch, onTreeReset }) {
  const { width: W, height: H } = useWindowDimensions();
  const pages = cd.pages;
  const seq = useMemo(() => {
    const s = [];
    pages.forEach((p, pi) => {
      const n = p.kind === 'special' ? p.imgs.length : Math.max(1, Math.ceil(p.ayat.length / 5));
      for (let k = 0; k < n; k++) s.push({ p: pi, s: k, n });
    });
    return s;
  }, [cd]);
  const flat = useMemo(() => {
    const f = [];
    pages.forEach((p, pi) => { if (p.kind === 'ayat') p.ayat.forEach((a, j) => f.push({ p: pi, s: Math.floor(j / 5), k: j % 5, a })); });
    return f;
  }, [cd]);
  const [cur, setCur] = useState(-1);          // -1 = bahçe
  const [open, setOpen] = useState(-1);        // açık ayet (flat sırası)
  const [tmenu, setTmenu] = useState(-1);       // yazar: ağaç menüsü
  const [settings, setSettings] = useState(false); // yazar: bahçe ayarları
  const [arrange, setArrange] = useState(false);   // yazar: ağaçları sağa sola yerleştirme modu
  const [editIdx, setEditIdx] = useState(-1);    // yazar: meyve konumu düzenleyici
  const trans = useRef(new Animated.Value(1)).current;
  const dirRef = useRef(1);
  const animate = (dir) => { dirRef.current = dir; trans.setValue(0); Animated.timing(trans, { toValue: 1, duration: 280, useNativeDriver: true }).start(); };
  const go = (i, dir = 1) => { if (i < 0 || i >= seq.length) return; animate(dir); setCur(i); };
  const toGarden = () => { animate(-1); setCur(-1); setOpen(-1); };
  const back = () => (cur > 0 ? go(cur - 1, -1) : toGarden());
  const next = () => (cur < seq.length - 1 ? go(cur + 1, 1) : toGarden());
  const closePanel = () => {
    const f = flat[open]; setOpen(-1);
    if (f) { const i = seq.findIndex((x) => x.p === f.p && x.s === f.s); if (i >= 0 && i !== cur) go(i, 1); }
  };

  let content;
  if (cur < 0) {
    content = (
      <View style={{ flex: 1 }}>
        <ForestPicker bottomPad={NAV_H - 8} arrange={arrange} onMove={onTreeMove} trees={trees} author={author} onMenu={setTmenu} pages={pages} W={W} H={H} insets={insets} onOpen={(i) => { const k = seq.findIndex((x) => x.p === i); if (k >= 0) go(k, 1); }} />
        <View pointerEvents="box-none" style={{ position: 'absolute', left: 0, right: 0, top: insets.top + 10, flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, gap: 10 }}>
          <RoundBtn icon="🏠" onPress={onHome} />
          <View style={{ flex: 1, alignItems: 'center' }}>
            {!ui.hideTitle && (
              <View style={{ backgroundColor: '#0B0B0B', borderWidth: 2.5, borderColor: GOLD, borderRadius: 12, paddingHorizontal: 22, paddingVertical: 8 }}>
                <Text style={{ color: '#F2C94C', fontWeight: '900', fontSize: 20, letterSpacing: 1 }}>{(cd.name || 'CÜZ').toUpperCase()}</Text>
              </View>
            )}
          </View>
          {author ? <RoundBtn icon="⚙" onPress={() => setSettings(true)} /> : <View style={{ width: 44 }} />}
        </View>
        <BottomBar active="garden" insets={insets} items={nav} />
        {arrange && (
          <View style={{ position: 'absolute', left: 12, right: 12, top: insets.top + 66, flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: 'rgba(0,0,0,0.74)', borderWidth: 1.5, borderColor: GOLD, borderRadius: 14, padding: 8 }}>
            <Text style={{ flex: 1, color: '#fff', fontWeight: '700', fontSize: 12 }}>✥ Ağacı sağa sola sürükle; bırakınca kaydolur</Text>
            <Plate small title="BİTTİ" onPress={() => setArrange(false)} />
          </View>
        )}
      </View>
    );
  } else {
    const it = seq[cur], page = pages[it.p];
    const topH = insets.top + 112, botH = insets.bottom + 96;
    const header = (
      <View style={{ position: 'absolute', left: 0, right: 0, top: insets.top + 8, zIndex: 20 }}>
        <View style={{ flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, gap: 10 }}>
          <RoundBtn icon="🏠" onPress={onHome} />
          <View style={{ flex: 1, alignItems: 'center' }}>
            <View style={{ backgroundColor: '#0B0B0B', borderWidth: 2.5, borderColor: GOLD, borderRadius: 12, paddingHorizontal: 14, paddingVertical: 5, alignItems: 'center' }}>
              <Text style={{ color: '#F2C94C', fontWeight: '900', fontSize: 15 }}>{(cd.name || 'CÜZ').toUpperCase()} · SAYFA {it.p + 1}</Text>
              <Text style={{ color: '#fff', fontSize: 11, fontWeight: '700' }}>{TREE_NAMES[it.p]}{it.n > 1 ? `  (${it.s + 1}/${it.n})` : ''}</Text>
            </View>
          </View>
          <RoundBtn icon="🌳" onPress={toGarden} />
        </View>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', paddingHorizontal: 10, marginTop: 8 }}>
          <Plate title="◀ ÖNCE" onPress={back} />
          <Plate title="SONRA ▶" onPress={next} />
        </View>
      </View>
    );
    let body = null, bottom = null;
    if (page.kind === 'special') {
      const im = page.imgs[it.s];
      body = (
        <ScrollView style={{ position: 'absolute', left: 0, right: 0, top: topH, bottom: 0 }} contentContainerStyle={{ alignItems: 'center', paddingBottom: insets.bottom + 20 }}>
          <Text style={{ color: '#fff', fontWeight: '900', fontSize: 15, marginBottom: 6, textShadowColor: '#000', textShadowRadius: 4 }}>{it.s === 0 ? 'Fatiha Suresi' : 'Bakara Suresi'}</Text>
          <Image source={{ uri: DIR + im.file }} style={{ width: W - 16, aspectRatio: im.w / im.h, borderRadius: 8, borderWidth: 2, borderColor: GOLD }} resizeMode="contain" />
        </ScrollView>
      );
    } else {
      const avail = H - topH - botH;
      const sh = Math.min(avail, (W * 0.84) * (4 / 3), 700), sw = sh * 0.75;
      const sl = (W - sw) / 2, st = topH + (avail - sh) / 2;
      const group = page.ayat.slice(it.s * 5, it.s * 5 + 5);
      const fd = sw * 0.155, lh = Math.min(56, sh * 0.142 - 5);
      const nodes = [];
      group.forEach((ay, k) => {
        const an = treeAnch(trees, it.p)[k], ax = sl + an[0] * sw, ay_ = st + an[1] * sh, side = FRUIT_SIDE[k];
        let lx, lw, ly = ay_ - lh / 2;
        if (side === 'top') { lw = Math.min(150, W * 0.4); lx = ax - lw / 2; ly = ay_ - fd / 2 - 14 - lh; }
        else if (side === 'left') { lx = 6; lw = Math.max(72, ax - fd / 2 - 10 - 6); }
        else { lx = ax + fd / 2 + 10; lw = Math.max(72, W - 6 - lx); lx = W - 6 - lw; }
        const fi = flat.findIndex((f) => f.p === it.p && f.s === it.s && f.k === k);
        nodes.push(
          <VerseLabel key={'l' + k} ay={ay} x={lx} y={ly} w={lw} h={lh} color={FRUIT_COL[k]} onPress={() => setOpen(fi)} />,
          <Fruit key={'f' + k} x={ax} y={ay_} d={fd} n={k + 1} color={FRUIT_COL[k]} delay={k * 260} onPress={() => setOpen(fi)} />,
        );
      });
      body = (
        <>
          <Pressable onLongPress={author ? () => setTmenu(it.p) : undefined} delayLongPress={500} style={{ position: 'absolute', left: sl, top: st, width: sw, height: sh }}>
            {treeSrc(trees, it.p) ? <Image source={treeSrc(trees, it.p)} style={{ width: sw, height: sh }} resizeMode="contain" /> : <TreeHole author={author} />}
          </Pressable>
          {nodes}
        </>
      );
      const nextPage = pages[it.p + 1];
      if (it.s < it.n - 1) bottom = <Plate title="SAYFA DEVAMI  ▶" onPress={next} style={{ paddingHorizontal: 26, paddingVertical: 12 }} />;
      else if (nextPage && nextPage.kind === 'ayat' && nextPage.ayat.length) {
        const na = nextPage.ayat[0];
        bottom = (
          <Pressable onPress={next} style={{ flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: '#FFF6D9', borderWidth: 3, borderColor: GOLD, borderRadius: 16, paddingHorizontal: 14, paddingVertical: 6 }}>
            <Text style={{ fontSize: 22 }}>📌</Text>
            <Image source={{ uri: DIR + na.start.file }} style={{ width: 110, height: 42 }} resizeMode="contain" />
            <Text style={{ color: '#3B2A10', fontWeight: '900' }}>SONRAKİ SAYFA ▶</Text>
          </Pressable>
        );
      } else bottom = <Plate title="🌳  BAHÇEYE DÖN" onPress={toGarden} style={{ paddingHorizontal: 26, paddingVertical: 12 }} />;
    }
    content = (
      <View style={{ flex: 1 }}>
        <View style={[StyleSheet.absoluteFill, { backgroundColor: 'rgba(0,0,0,0.10)' }]} />
        {body}
        {header}
        {bottom && <View style={{ position: 'absolute', left: 0, right: 0, bottom: insets.bottom + 16, alignItems: 'center', zIndex: 20 }}>{bottom}</View>}
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: C.bg }}>
      {(() => {
        const b = cur < 0 ? ui.bgGarden : ui.bgPage;
        return b && b.file
          ? <Image source={{ uri: DIR + b.file }} style={StyleSheet.absoluteFill} resizeMode="cover" />
          : <View style={StyleSheet.absoluteFill}><View style={{ flex: 3, backgroundColor: '#8EC9F2' }} /><View style={{ flex: 7, backgroundColor: '#4C8F57' }} /></View>;
      })()}
      <Animated.View style={{ flex: 1, opacity: trans, transform: [{ translateX: trans.interpolate({ inputRange: [0, 1], outputRange: [dirRef.current * 44, 0] }) }] }}>
        {content}
      </Animated.View>
      <Modal transparent visible={open >= 0} animationType="fade" onRequestClose={closePanel}>
        <View style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.74)', alignItems: 'center', justifyContent: 'center' }}>
          {open >= 0 && flat[open] && (
            <AyahPanel item={flat[open]} idx={open} total={flat.length} W={W} H={H}
              onPrev={() => setOpen(open - 1)} onNext={() => setOpen(open + 1)} onClose={closePanel} />
          )}
        </View>
      </Modal>
      <Modal transparent visible={tmenu >= 0} animationType="fade" onRequestClose={() => setTmenu(-1)}>
        <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.65)', alignItems: 'center', justifyContent: 'center' }} onPress={() => setTmenu(-1)}>
          <View style={{ width: Math.min(W - 40, 360), backgroundColor: C.card, borderRadius: 16, padding: 16, gap: 8 }}>
            <Text style={{ color: '#fff', fontWeight: '900', fontSize: 17, marginBottom: 4 }}>{tmenu >= 0 ? `${tmenu + 1}. ağaç · ${TREE_NAMES[tmenu % TREE_NAMES.length]}` : ''}</Text>
            <Btn title="🖼 Ağaç görselini değiştir" kind="ghost" onPress={() => { const i = tmenu; setTmenu(-1); setTimeout(() => onPickTree(i), 250); }} />
            <Btn title="📍 Meyve konumlarını ayarla" kind="ghost" onPress={() => { const i = tmenu; setTmenu(-1); setTimeout(() => setEditIdx(i), 250); }} />
            <Btn title="↺ Varsayılana dön" kind="ghost" onPress={() => { const i = tmenu; setTmenu(-1); onTreeReset(i); }} />
            <Text style={{ color: C.sub, fontSize: 12, marginTop: 4 }}>Ağaç tüm cüzlerde aynı sayfa sırasına uygulanır. Şeffaf arka planlı PNG kullan.</Text>
          </View>
        </Pressable>
      </Modal>
      <Modal transparent visible={settings} animationType="fade" onRequestClose={() => setSettings(false)}>
        <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.65)', alignItems: 'center', justifyContent: 'center' }} onPress={() => setSettings(false)}>
          <View style={{ width: Math.min(W - 40, 380), backgroundColor: C.card, borderRadius: 16, padding: 16, gap: 8 }}>
            <Text style={{ color: '#fff', fontWeight: '900', fontSize: 17, marginBottom: 2 }}>Bahçe ayarları</Text>
            <Btn title="✥ Ağaçları sağa sola yerleştir" onPress={() => { setSettings(false); setArrange(true); }} />
            <Btn title="🖼 Orman arka planı seç" kind="ghost" onPress={() => { setSettings(false); setTimeout(() => onPickBg('bgGarden'), 250); }} />
            <Btn title="🖼 Ağaç sayfası arka planı seç" kind="ghost" onPress={() => { setSettings(false); setTimeout(() => onPickBg('bgPage'), 250); }} />
            <Btn title={ui.hideTitle ? 'Cüz plakasını göster' : 'Cüz plakasını gizle (arka planda yazıyorsa)'} kind="ghost" onPress={() => onUi({ hideTitle: !ui.hideTitle })} />
            <Btn title="↔ Tüm ağaç konumlarını sıfırla" kind="ghost" onPress={() => { onTreesResetPos(); setSettings(false); }} />
            <Btn title="↺ Arka planları varsayılana döndür" kind="ghost" onPress={() => { onBgReset(); setSettings(false); }} />
            <Text style={{ color: C.sub, fontSize: 12, marginTop: 2 }}>Ağaç görseli eklemek için bir ağaca basılı tut.</Text>
          </View>
        </Pressable>
      </Modal>
      {editIdx >= 0 && <AnchorEditor idx={editIdx} trees={trees} W={W} H={H} insets={insets} onClose={() => setEditIdx(-1)} onSave={(an) => { onTreeAnch(editIdx, an); setEditIdx(-1); }} />}
    </View>
  );
}

// cüz paketi (.zip / .hdz içinde kind:'cuz'): dosyaları uygulamaya yazar, sayfa yapısını döndürür
async function readCuzPackage(zip, meta, onProgress) {
  await ensureDir();
  const stamp = Date.now().toString(36);
  const names = [];
  const all = [];
  (meta.pages || []).forEach((p) => {
    if (p.kind === 'special') (p.imgs || []).forEach((im) => all.push(im));
    else (p.ayat || []).forEach((a) => { all.push(a.start); all.push(a.full); });
  });
  const map = {};
  let i = 0;
  for (const im of all) {
    i++; onProgress && onProgress(i, all.length);
    if (map[im.file]) continue;
    const f = zip.file(im.file);
    if (!f) throw new Error('Pakette eksik dosya: ' + im.file);
    const local = stamp + '_' + im.file.replace(/[^A-Za-z0-9._-]/g, '_');
    await FileSystem.writeAsStringAsync(DIR + local, await f.async('base64'), { encoding: 'base64' });
    map[im.file] = local; names.push(local);
  }
  const fix = (im) => ({ file: map[im.file], w: im.w, h: im.h });
  const pages = (meta.pages || []).map((p) => (p.kind === 'special'
    ? { kind: 'special', title: p.title, imgs: (p.imgs || []).map(fix) }
    : { kind: 'ayat', ayat: (p.ayat || []).map((a) => ({ sura: a.sura, sname: a.sname, no: a.no, start: fix(a.start), full: fix(a.full) })) }));
  return { kind: 'cuz', cuz: meta.cuz, name: meta.name || meta.cuz + '. Cüz', pages, files: names };
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
      if (screen.name === 'cuz' || screen.name === 'forest') { setScreen({ name: 'home' }); return true; }
      return false;
    });
    return () => sub.remove();
  }, [screen, mode]);

  const promptName = (title, initial = '') => new Promise((res) => setNamePrompt({ title, initial, res }));
  const finishPrompt = (v) => { namePrompt.res(v); setNamePrompt(null); };

  const askPass = (kind, check, opts) => new Promise((res) => setPassPrompt({ mode: kind, check, res, ...(opts || {}) }));
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
  const pickTree = async (idx) => {
    const assets = await pickImages(false);
    if (!assets.length) return;
    try {
      await ensureDir();
      const a0 = assets[0], file = 'tree_' + idx + '_' + uid() + '.' + extOf(a0.uri.split('?')[0]);
      await FileSystem.copyAsync({ from: a0.uri, to: DIR + file });
      const old = (dataRef.current.trees || {})[idx];
      if (old && old.file) FileSystem.deleteAsync(DIR + old.file, { idempotent: true }).catch(() => {});
      setData((d) => ({ ...d, trees: { ...(d.trees || {}), [idx]: { ...(old || {}), file, w: a0.width, h: a0.height } } }));
    } catch (e) { Alert.alert('Ağaç eklenemedi', e.message); }
  };
  const treeAnchSave = (idx, anch) => setData((d) => ({ ...d, trees: { ...(d.trees || {}), [idx]: { ...((d.trees || {})[idx] || { file: null }), anch } } }));
  const treeReset = (idx) => {
    const old = (dataRef.current.trees || {})[idx];
    if (old && old.file) FileSystem.deleteAsync(DIR + old.file, { idempotent: true }).catch(() => {});
    setData((d) => { const tr = { ...(d.trees || {}) }; delete tr[idx]; return { ...d, trees: tr }; });
  };
  const pickBg = async (kind) => {
    const assets = await pickImages(false);
    if (!assets.length) return;
    try {
      await ensureDir();
      const a0 = assets[0], file = 'bg_' + kind + '_' + uid() + '.' + extOf(a0.uri.split('?')[0]);
      await FileSystem.copyAsync({ from: a0.uri, to: DIR + file });
      const old = ((dataRef.current.ui || {})[kind] || {}).file;
      if (old) FileSystem.deleteAsync(DIR + old, { idempotent: true }).catch(() => {});
      setData((d) => ({ ...d, ui: { ...(d.ui || {}), [kind]: { file } } }));
    } catch (e) { Alert.alert('Arka plan eklenemedi', e.message); }
  };
  const uiPatch = (patch) => setData((d) => ({ ...d, ui: { ...(d.ui || {}), ...patch } }));
  const bgReset = () => {
    const u = dataRef.current.ui || {};
    [u.bgGarden, u.bgPage, u.bgForest].forEach((b) => { if (b && b.file) FileSystem.deleteAsync(DIR + b.file, { idempotent: true }).catch(() => {}); });
    uiPatch({ bgGarden: null, bgPage: null, bgForest: null });
  };
  const treeMove = (idx, dx) => setData((d) => ({ ...d, trees: { ...(d.trees || {}), [idx]: { ...((d.trees || {})[idx] || { file: null }), dx } } }));
  const treesResetPos = () => setData((d) => { const tr = {}; Object.keys(d.trees || {}).forEach((kk) => { tr[kk] = { ...d.trees[kk], dx: 0 }; }); return { ...d, trees: tr }; });
  const ffSet = (fn) => setData((d) => ({ ...d, forest: fn(d.forest || { items: [], cfg: {} }) }));
  const ffUpdate = (id, patch) => ffSet((f) => ({ ...f, items: (f.items || []).map((x) => (x.id === id ? { ...x, ...patch } : x)) }));
  const ffCfg = (patch) => ffSet((f) => ({ ...f, cfg: { ...(f.cfg || {}), ...patch } }));
  const ffAdd = async () => {
    const have = ((dataRef.current.forest || {}).items || []).length;
    if (have >= FF_MAX) { Alert.alert('En fazla ' + FF_MAX + ' resim', 'Yeni resim eklemek için önce birini sil.'); return; }
    const assets = await pickImages(true);
    if (!assets.length) return;
    try {
      await ensureDir();
      const add = [];
      for (const a0 of assets.slice(0, FF_MAX - have)) {
        const id = uid(), file = 'orm_' + id + '.' + extOf(a0.uri.split('?')[0]);
        await FileSystem.copyAsync({ from: a0.uri, to: DIR + file });
        add.push({ id, file, w: a0.width, h: a0.height, dx: 0, sc: 1, label: '', cuz: 0 });
      }
      ffSet((f) => ({ ...f, items: [...(f.items || []), ...add] }));
      if (assets.length > FF_MAX - have) Alert.alert('Sınır', 'En fazla ' + FF_MAX + ' resim eklenebilir; fazlası alınmadı.');
    } catch (e) { Alert.alert('Resim eklenemedi', e.message); }
  };
  const ffReplace = async (id) => {
    const assets = await pickImages(false);
    if (!assets.length) return;
    try {
      await ensureDir();
      const a0 = assets[0], file = 'orm_' + uid() + '.' + extOf(a0.uri.split('?')[0]);
      await FileSystem.copyAsync({ from: a0.uri, to: DIR + file });
      const old = ((dataRef.current.forest || {}).items || []).find((x) => x.id === id);
      if (old && old.file) FileSystem.deleteAsync(DIR + old.file, { idempotent: true }).catch(() => {});
      ffUpdate(id, { file, w: a0.width, h: a0.height });
    } catch (e) { Alert.alert('Resim değiştirilemedi', e.message); }
  };
  const ffDelete = (id) => {
    const old = ((dataRef.current.forest || {}).items || []).find((x) => x.id === id);
    if (old && old.file) FileSystem.deleteAsync(DIR + old.file, { idempotent: true }).catch(() => {});
    ffSet((f) => ({ ...f, items: (f.items || []).filter((x) => x.id !== id) }));
  };
  const ffReorder = (id, delta) => ffSet((f) => {
    const a = [...(f.items || [])], i = a.findIndex((x) => x.id === id), j = i + delta;
    if (i < 0 || j < 0 || j >= a.length) return f;
    [a[i], a[j]] = [a[j], a[i]]; return { ...f, items: a };
  });
  const ffLabel = async (id) => {
    const it = ((dataRef.current.forest || {}).items || []).find((x) => x.id === id); if (!it) return;
    const n = await promptName('Resmin altındaki yazı (silmek için - yaz)', it.label || '');
    if (n === null || n === undefined) return;
    ffUpdate(id, { label: n.trim() === '-' ? '' : n.trim() });
  };
  const ffLink = async (id) => {
    const it = ((dataRef.current.forest || {}).items || []).find((x) => x.id === id); if (!it) return;
    const n = await promptName('Hangi cüze bağlansın? (1-30, kaldırmak için 0)', it.cuz ? String(it.cuz) : '');
    if (n === null || n === undefined) return;
    const v = parseInt(n, 10);
    ffUpdate(id, { cuz: !isNaN(v) && v >= 1 && v <= 30 ? v : 0 });
  };
  const ffResetPos = () => ffSet((f) => ({ ...f, items: (f.items || []).map((x) => ({ ...x, dx: 0 })) }));
  const ffClear = () => Alert.alert('Tüm resimleri sil', 'Ormandaki bütün resimler silinecek.', [
    { text: 'Vazgeç', style: 'cancel' },
    { text: 'Sil', style: 'destructive', onPress: () => {
      ((dataRef.current.forest || {}).items || []).forEach((x) => { if (x.file) FileSystem.deleteAsync(DIR + x.file, { idempotent: true }).catch(() => {}); });
      ffSet((f) => ({ ...f, items: [] }));
    } },
  ]);
  const lastCuz = useRef(null);
  const openGarden = () => {
    const ks = Object.keys(dataRef.current.cuz || {});
    if (!ks.length) { Alert.alert('Henüz bahçe yok', 'Önce bir cüz paketi yükle (Paket aç).'); return; }
    const n = lastCuz.current && dataRef.current.cuz[lastCuz.current] ? lastCuz.current : parseInt(ks[0], 10);
    setScreen({ name: 'cuz', cuz: n });
  };
  const navItems = [
    { k: 'home', icon: '🏠', label: 'Ana Sayfa', onPress: () => setScreen({ name: 'home' }) },
    { k: 'garden', icon: '🌳', label: 'Bahçe', onPress: openGarden },
    { k: 'forest', icon: '🌲', label: 'Orman', onPress: () => setScreen({ name: 'forest' }) },
    { k: 'profile', icon: '👤', label: 'Profil', onPress: () => setProfileOpen(true) },
  ];
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

  const sortAll = (fold) =>
    setData((d) => {
      const cmp = (a, b) => a.name.localeCompare(b.name, 'tr', { numeric: true });
      if (!fold || fold === 'none') return { ...d, images: [...d.images].sort(cmp) };
      const slots = []; d.images.forEach((x, i) => { if (x.folder === fold) slots.push(i); });
      const sorted = slots.map((i) => d.images[i]).sort(cmp);
      const imgs = [...d.images]; slots.forEach((si, k) => { imgs[si] = sorted[k]; });
      return { ...d, images: imgs };
    });
  // bir bölümün içinde sayfayı yukarı/aşağı/en başa/en sona taşır
  const moveImage = (id, how) =>
    setData((d) => {
      const im = d.images.find((i) => i.id === id); if (!im) return d;
      const key = im.folder || null;
      const slots = []; d.images.forEach((x, i) => { if ((x.folder || null) === key) slots.push(i); });
      const items = slots.map((i) => d.images[i]);
      const pos = items.findIndex((x) => x.id === id);
      let np = pos;
      if (how === 'up') np = Math.max(0, pos - 1);
      else if (how === 'down') np = Math.min(items.length - 1, pos + 1);
      else if (how === 'top') np = 0;
      else if (how === 'bottom') np = items.length - 1;
      if (np === pos) return d;
      const [it] = items.splice(pos, 1); items.splice(np, 0, it);
      const imgs = [...d.images]; slots.forEach((si, k) => { imgs[si] = items[k]; });
      return { ...d, images: imgs };
    });

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
  const askPkgPassword = () => askPass('create', null, {
    title: '🔒 Paket şifresi', min: 6, optional: true,
    desc: 'Şifre yazarsan paket kilitlenir; paylaşmayacaksan "Şifresiz" seç, düz zip çıkar. Şifreli paket bu şifreyle kilitlenecek. Okuyucuya şifreyi ayrıca ilet. Unutulursa paket kurtarılamaz, bir yere not et. Uzun ve tahmin edilmesi zor bir şifre daha güvenlidir.',
  });
  const exportCb = (what) => (i, n, ph) =>
    setBusy(ph === 'key' ? 'Şifre anahtarı hazırlanıyor…' : ph === 'enc' ? `Şifreleniyor… ${i}/${n}` : ph ? 'Zip oluşturuluyor…' : `${what} hazırlanıyor… ${i}/${n}`);

  const doExport = async () => {
    const pw = await askPkgPassword(); if (pw === null) return;
    setBusy('Paket hazırlanıyor…');
    try { await exportPackage(dataRef.current, exportCb('Paket'), null, pw); }
    catch (e) { Alert.alert('Dışa aktarılamadı', e.message); }
    setBusy(false);
  };

  const doExportSection = async (fid) => {
    const pw = await askPkgPassword(); if (pw === null) return;
    setBusy('Bölüm hazırlanıyor…');
    try { await exportPackage(dataRef.current, exportCb('Bölüm'), fid, pw); }
    catch (e) { Alert.alert('Dışa aktarılamadı', e.message); }
    setBusy(false);
  };

  // tam pakette eski içerik silineceği için onay ister (bölüm paketi sormadan birleşir)
  const confirmWipe = () => (!dataRef.current.images.length ? true : new Promise((res) =>
    Alert.alert('Tam paket', 'Bu paket TÜM içeriği içeriyor. Şu anki içerik silinip yerine geçecek. (Çıpaların korunur.)', [
      { text: 'Vazgeç', style: 'cancel', onPress: () => res(false) },
      { text: 'Devam', onPress: () => res(true) },
    ], { onDismiss: () => res(false) })));

  const doImport = async () => {
    setBusy('Paket açılıyor…');
    try {
      const pkg = await readPackage(
        (i, n, ph) => setBusy(ph === 'dec' ? `Şifre çözülüyor… ${i}/${n}` : `Paket açılıyor… ${i}/${n}`),
        confirmWipe,
        (check) => askPass('enter', check, { title: '🔒 Paket şifresi', desc: 'Bu paketin şifresini yaz. Şifreyi paketi gönderen kişi sana iletmiş olmalı.' }));
      if (pkg && pkg.kind === 'cuz') {
        const old = (dataRef.current.cuz || {})[pkg.cuz];
        if (old && old.files) old.files.forEach((fn) => FileSystem.deleteAsync(DIR + fn, { idempotent: true }).catch(() => {}));
        setData((d) => ({ ...d, cuz: { ...(d.cuz || {}), [pkg.cuz]: { name: pkg.name, pages: pkg.pages, files: pkg.files } } }));
        setScreen({ name: 'home' });
        Alert.alert('Hazır', `${pkg.name} meyve bahçesi yüklendi. Ana ekranda ${pkg.cuz}. bölüme dokun.`);
      } else if (pkg && pkg.kind === 'section') {
        // sadece bu bölümü değiştir; diğer bölümlere dokunma
        const d = dataRef.current, sid = pkg.section;
        const nf = (pkg.folders || []).find((f) => f.id === sid) || { id: sid, name: 'Bölüm', cover: null };
        const oldF = (d.folders || []).find((f) => f.id === sid);
        const incoming = new Set(pkg.images.map((i) => i.id));
        d.images.filter((i) => i.folder === sid).forEach((i) => {
          FileSystem.deleteAsync(DIR + i.file, { idempotent: true }).catch(() => {});
          (i.buttons || []).forEach((b) => { if (b.sound && b.sound.file) FileSystem.deleteAsync(ADIR + b.sound.file, { idempotent: true }).catch(() => {}); });
        });
        if (oldF && oldF.cover) FileSystem.deleteAsync(DIR + oldF.cover, { idempotent: true }).catch(() => {});
        const keep = d.images.filter((i) => i.folder !== sid && !incoming.has(i.id));
        const folders = (d.folders || []).some((f) => f.id === sid)
          ? d.folders.map((f) => (f.id === sid ? { ...f, name: nf.name, cover: nf.cover } : f))
          : [...(d.folders || []), nf];
        setData(ensureSections({ ...d, images: [...keep, ...pkg.images], folders }));
        setScreen({ name: 'home' });
        Alert.alert('Hazır', `"${nf.name}" bölümü güncellendi (${pkg.images.length} sayfa). Diğer bölümlere dokunulmadı.`);
      } else if (pkg) {
        setData(ensureSections(pkg));
        setScreen({ name: 'home' });
        Alert.alert('Hazır', `${pkg.images.length} sayfa yüklendi.`);
      }
    } catch (e) { Alert.alert('Paket açılamadı', e.message); }
    setBusy(false);
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
        onHome={() => setScreen({ name: 'home' })}
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
        onSort={sortAll} onMove={moveImage} onExport={doExport} onImport={doImport} onResetMode={resetMode}
        onSetFolder={setFolder} onNewFolder={newFolder} onRenameFolder={renameFolder} onDeleteFolder={deleteFolder} />
    );
  } else if (screen.name === 'forest') {
    body = (
      <FreeForestScreen
        forest={data.forest || { items: [], cfg: {} }} ui={data.ui || {}} author={AUTHOR} insets={insets} nav={navItems} cuzData={data.cuz || {}}
        onAdd={ffAdd} onMove={(id, dx) => ffUpdate(id, { dx })} onUpdate={ffUpdate} onDelete={ffDelete} onReorder={ffReorder} onCfg={ffCfg}
        onPickBg={pickBg} onUi={uiPatch} onLabel={ffLabel} onLink={ffLink} onReplace={ffReplace} onResetPos={ffResetPos} onClear={ffClear}
        onOpenCuz={(n) => { lastCuz.current = n; setScreen({ name: 'cuz', cuz: n }); }} />
    );
  } else if (screen.name === 'cuz' && data.cuz && data.cuz[screen.cuz]) {
    body = <CuzReader nav={navItems} key={screen.cuz} cd={data.cuz[screen.cuz]} insets={insets} onHome={() => setScreen({ name: 'home' })}
      trees={data.trees || {}} ui={data.ui || {}} onPickBg={pickBg} onUi={uiPatch} onBgReset={bgReset} onTreeMove={treeMove} onTreesResetPos={treesResetPos} author={AUTHOR} onPickTree={pickTree} onTreeAnch={treeAnchSave} onTreeReset={treeReset} />;
  } else {
    body = (
      <Home
        nav={navItems} cuz={data.cuz || {}} onOpenCuz={(n) => { lastCuz.current = n; setScreen({ name: 'cuz', cuz: n }); }}
        data={data} user={user} author={AUTHOR} insets={insets}
        onPlay={(id) => play(id, 'home')} onProfile={() => setProfileOpen(true)}
        onLibrary={(fold) => setScreen({ name: 'library', fold })}
        onExportSec={doExportSection} onExport={doExport} onImport={doImport} onPassword={changePassword} onResetMode={resetMode}
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
  pinTag: { position: 'absolute', top: -2, maxWidth: 130, paddingHorizontal: 6, paddingVertical: 1, borderRadius: 8 },
  ordNum: { position: 'absolute', left: 8, top: 8, minWidth: 28, height: 28, borderRadius: 14, paddingHorizontal: 6, backgroundColor: 'rgba(0,0,0,0.7)', alignItems: 'center', justifyContent: 'center' },
  ordBox: { position: 'absolute', right: 8, bottom: 8, flexDirection: 'row', gap: 8 },
  ordBtn: { width: 38, height: 38, borderRadius: 19, backgroundColor: C.accent, alignItems: 'center', justifyContent: 'center' },
  ordTxt: { color: '#1A1500', fontWeight: '900', fontSize: 15 },
  pin: { position: 'absolute', width: 20, height: 20, borderRadius: 10, borderWidth: 1.5, borderColor: '#fff', alignItems: 'center', justifyContent: 'center', shadowColor: '#000', shadowOpacity: 0.5, shadowRadius: 4, elevation: 5 },
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
