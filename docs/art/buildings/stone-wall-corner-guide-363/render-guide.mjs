import {createRequire} from 'node:module';import {fileURLToPath} from 'node:url';
const require=createRequire('/home/kieu-hoang-quan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json'),sharp=require('sharp'),dir=fileURLToPath(new URL('.',import.meta.url));
await sharp(dir+'guide.svg').png().toFile(dir+'guide.png');await sharp(dir+'guide.svg').resize(42,42,{fit:'fill',kernel:'lanczos3'}).png().toFile(dir+'preview42.png');
