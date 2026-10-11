import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require=createRequire('/home/kieu-hoang-quan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const sharp=require('sharp');
const dir=fileURLToPath(new URL('.',import.meta.url));
await sharp(dir+'guide.svg').png().toFile(dir+'guide.png');
console.log(JSON.stringify(await sharp(dir+'guide.png').metadata()));
