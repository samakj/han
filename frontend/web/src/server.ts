import express, { Express } from 'express';
import cors from 'cors';

import { getPageSource } from '@han/ssr';
import { defaultPort, serviceWorkerEndpoint, serviceWorkerRoot, staticEndpoint, staticRoot } from '@han/ssr/config';

const port: string = process.env.PORT || defaultPort;
const server: Express = express();

server.use(cors());
server.use(staticEndpoint, express.static(staticRoot));
server.use(serviceWorkerEndpoint, express.static(serviceWorkerRoot));

server.get('/service-worker.js', (request, response) => response.sendFile('/js/service-worker.js'));
server.get('*', getPageSource);

server.listen(port);
console.log(`Listening at http://localhost:${port}`);
