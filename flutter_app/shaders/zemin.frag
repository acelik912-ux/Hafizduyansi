#version 460 core
precision highp float;
#include <flutter/runtime_effect.glsl>

// 3B bahçe zemini: ekrandaki her pikseli yer düzlemindeki dünya noktasına çevirir (perspektif doğru),
// çim ve taş yol dokularını örnekler. Her şey dünyaya sabittir: kamera hareket etmedikçe hiçbir şey kımıldamaz.
uniform vec2 uSize;     // tuval boyutu
uniform float uYH;      // ufuk çizgisi (ekran y)
uniform float uF;       // odak uzaklığı (piksel)
uniform float uGoz;     // göz yüksekliği (m)
uniform float uCos;     // kamera yönü
uniform float uSin;
uniform float uCamX;
uniform float uCamZ;
uniform float uCitX;    // çit yarı genişliği
uniform float uZ0;      // çit başı
uniform float uZ1;      // çit sonu
uniform float uYol;     // yol yarı genişliği

uniform sampler2D uGI;  // çim (ince)
uniform sampler2D uGK;  // çim (1/8)
uniform sampler2D uPI;  // yol (ince)
uniform sampler2D uPK;  // yol (1/8)

layout(location = 0) out vec4 fragColor;

const vec3 CIM_ORT = vec3(0.2170, 0.4078, 0.1253);
const vec3 YOL_ORT = vec3(0.5974, 0.5554, 0.4720);
const float CIM_M = 3.2;      // çim dokusunun metre karşılığı
const vec2 YOL_M = vec2(1.7, 3.4);
// doku payları (tools/zemin_doku.py): ince 4 px, küçük 1 px
const float GI_N = 2048.0, GK_N = 256.0;
const vec2 PI_N = vec2(1024.0, 2048.0), PK_N = vec2(128.0, 256.0);

float h21(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float vn(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(mix(h21(i), h21(i + vec2(1.0, 0.0)), f.x), mix(h21(i + vec2(0.0, 1.0)), h21(i + vec2(1.0, 1.0)), f.x), f.y);
}

vec2 pay(vec2 uv, vec2 n, float p) {
  // fract + kenarlardaki sarmalı paylı görüntü içinde konumlandır
  return (vec2(p) + fract(uv) * n) / (n + vec2(2.0 * p));
}

void main() {
  vec2 fc = FlutterFragCoord().xy;
  float sy = fc.y - uYH;
  if (sy < 0.5) {
    fragColor = vec4(0.0);
    return;
  }
  float d = uGoz * uF / sy;                       // derinlik (m)
  float yan = (fc.x - uSize.x * 0.5) * d / uF;
  float wx = uCamX + yan * uCos + d * uSin;
  float wz = uCamZ - yan * uSin + d * uCos;
  float fpv = d * d / (uGoz * uF);                // bir pikselin yerdeki dikey kapladığı alan (m)
  float ax = abs(wx);

  // ---- çim (ince doku -> küçük doku -> ortalama renk: uzakta titreşim olmasın)
  vec2 gw = vec2(wx, wz) / CIM_M;
  float tg = fpv / (CIM_M / GI_N);
  vec3 gI = texture(uGI, pay(gw, vec2(GI_N), 4.0)).rgb;
  vec3 gK = texture(uGK, pay(gw, vec2(GK_N), 1.0)).rgb;
  vec3 cim = mix(gI, gK, smoothstep(1.0, 3.0, tg));
  cim = mix(cim, CIM_ORT, smoothstep(9.0, 36.0, tg));
  // geniş ölçekli doğal renk değişimi (açık/koyu, hafif sararmış yamalar)
  float b1 = vn(vec2(wx, wz) * 0.23), b2 = vn(vec2(wx, wz) * 0.7 + 17.0);
  cim *= 0.86 + 0.3 * b1 + 0.1 * (b2 - 0.5);
  cim = mix(cim, cim * vec3(1.22, 1.1, 0.7), smoothstep(0.62, 0.9, b2) * 0.45);

  vec3 col = cim;

  bool icerde = ax < uCitX && wz > uZ0 && wz < uZ1;
  if (icerde) {
    // biçilmiş çim şeritleri (yol boyunca)
    float band = floor((ax - uYol) / 1.15);
    float serit = mod(band, 2.0) < 0.5 ? 1.05 : 0.95;
    col *= mix(1.0, serit, step(uYol, ax) * (1.0 - smoothstep(6.0, 12.0, d)));

    // çiçek tarhı (toprak)
    float tarh = step(uCitX - 1.0, ax) * step(ax, uCitX - 0.15) * step(uZ0 + 1.0, wz) * step(wz, uZ1 - 1.0);
    float inc = 1.0 - smoothstep(0.012, 0.05, fpv);
    float toprak = 0.78 + 0.28 * (vn(vec2(wx, wz) * 38.0) - 0.5) * inc + 0.35 * (vn(vec2(wx, wz) * 6.0) - 0.5);
    vec3 soil = vec3(0.37, 0.25, 0.17) * toprak;
    col = mix(col, soil, tarh);

    // taş yol
    float e = uYol - ax + (vn(vec2(wz * 3.1, ax * 2.3)) - 0.5) * 0.06;
    float m = smoothstep(0.0, 0.012, e);
    vec2 pw = vec2((wx + uYol) / YOL_M.x, wz / YOL_M.y);
    float tp = fpv / (YOL_M.x / PI_N.x);
    vec3 pI = texture(uPI, pay(pw, PI_N, 4.0)).rgb;
    vec3 pK = texture(uPK, pay(pw, PK_N, 1.0)).rgb;
    vec3 yol = mix(pI, pK, smoothstep(1.0, 3.0, tp));
    yol = mix(yol, YOL_ORT, smoothstep(9.0, 36.0, tp));
    yol *= 0.9 + 0.2 * vn(vec2(wx, wz) * 0.9);
    // yolun kenarındaki toprak şerit
    float kenar = smoothstep(-0.09, 0.0, e) * (1.0 - m);
    vec3 topr = vec3(0.45, 0.36, 0.24) * (0.85 + 0.3 * vn(vec2(wx, wz) * 25.0));
    col = mix(col, topr, kenar * 0.85);
    col = mix(col, yol, m);
  } else {
    // çitin dışı: açık, hafif sararmış çayır
    col *= vec3(1.12, 1.1, 0.82);
  }

  // yakında çok az koyu, hava perspektifi: uzakta açık yeşil sis
  col *= mix(0.9, 1.0, smoothstep(0.8, 5.0, d));
  float sis = 1.0 - exp(-d * (icerde ? 0.018 : 0.03));
  vec3 sisRengi = vec3(0.60, 0.78, 0.50);
  col = mix(col, sisRengi, clamp(sis, 0.0, 0.9));
  col *= vec3(1.03, 1.02, 0.97);
  fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
