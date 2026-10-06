"""يولّد ملفات PWA (manifest + service worker)"""
import os
import json


class PwaGenerator:
    """يولّد ملفات PWA الإضافية"""

    def __init__(self, program, output_dir='./build'):
        self.program = program
        self.output_dir = output_dir
        self.app_name = program.name or 'بيان'
        self.short_name = self.app_name[:12]

    def generate(self):
        """يولّد manifest.json + service worker + أيقونة"""
        created = []

        # 1) manifest.json
        manifest = {
            "name": self.app_name,
            "short_name": self.short_name,
            "description": self.program.purpose or "تطبيق بلغة بيان",
            "start_url": "./index.html",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#667eea",
            "orientation": "portrait",
            "dir": "rtl",
            "lang": "ar",
            "icons": [
                {
                    "src": "icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ]
        }

        manifest_path = os.path.join(self.output_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        created.append(manifest_path)
        print(f"   📄 manifest.json")

        # 2) service worker
        sw = '''// Service Worker — يخلي التطبيق يشتغل offline
const CACHE_NAME = 'byan-app-v1';
const urlsToCache = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
                  .map(name => caches.delete(name))
      );
    })
  );
});
'''
        sw_path = os.path.join(self.output_dir, 'sw.js')
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(sw)
        created.append(sw_path)
        print(f"   📄 sw.js")

        # 3) أيقونة SVG مبدئية (ممكن تتغير)
        icon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="100" fill="#667eea"/>
  <text x="50%" y="55%" font-size="260" text-anchor="middle"
        dominant-baseline="middle" fill="white" font-family="sans-serif">ب</text>
</svg>'''
        icon_path = os.path.join(self.output_dir, 'icon.svg')
        with open(icon_path, 'w', encoding='utf-8') as f:
            f.write(icon_svg)
        created.append(icon_path)
        print(f"   📄 icon.svg")

        return created
