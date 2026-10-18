import {defineConfig} from 'vite';
import {fileURLToPath} from 'node:url';
const entry=name=>fileURLToPath(new URL(name,import.meta.url));
export default defineConfig({server:{proxy:{'/ws':{target:'ws://127.0.0.1:3000',ws:true},'/health':'http://127.0.0.1:3000'}},build:{target:'es2022',rollupOptions:{input:{game:entry('./index.html'),scene:entry('./client/art-direction-scene.html'),viewer:entry('./client/pixel-sprite-viewer.html')}}}});
