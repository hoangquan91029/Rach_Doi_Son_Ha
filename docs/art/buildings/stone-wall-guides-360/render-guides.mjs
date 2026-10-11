import {createRequire} from 'node:module';import {fileURLToPath} from 'node:url';
const require=createRequire('/home/kieu-hoang-quan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json'),sharp=require('sharp'),dir=fileURLToPath(new URL('.',import.meta.url));
for(const axis of ['X','Y']){await sharp(dir+`guide-${axis}.svg`).png().toFile(dir+`guide-${axis}.png`);await sharp(dir+`guide-${axis}.svg`).resize(42,42,{fit:'fill',kernel:'lanczos3'}).png().toFile(dir+`preview42-${axis}.png`);}
