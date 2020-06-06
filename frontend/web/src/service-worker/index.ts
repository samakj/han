import { ExtendableEvent, FetchEvent } from '@han/service-worker/types';
import {
    CACHE_EXPIRY,
    CACHE_FULL_NAME,
    DEV_DONT_CACHE,
    DONT_CACHE,
    PRECACHE_FILES
} from '@han/service-worker/config';

const COMBINED_DONT_CACHE = [...DONT_CACHE, ...(process.env.NODE_ENV === 'development' ? DEV_DONT_CACHE : [])];

self.addEventListener('install', (event: ExtendableEvent): void => {
    console.log('Installing service worker...');
    event.waitUntil(
        cleanCaches()
            .then(getCurrentCache)
            .then(
                (cache: Cache): Promise<void> => {
                    console.log(`Cache opened, adding files...`);
                    return cache.addAll(PRECACHE_FILES);
                },
            )
            .catch(
                (error: Error): void => {
                    console.log('Error installing service worker: ', error);
                }
            )
    );
});

self.addEventListener('fetch', (event: FetchEvent): void => {
    event.respondWith(
        caches.match(event.request).then(
            (response: Response): Promise<Response> => {
                if (response) {
                    return Promise.resolve(response);
                }
                return performFetchRequest(event.request);
            },
        ),
    );
});

const cleanCaches = (): Promise<void> => caches
    .keys()
    .then(
        (cacheNames: string[]): Promise<void> => {
            return getCurrentCacheName()
                .then(
                    (currentCacheName: string): void => {
                        for (const cacheName of cacheNames) {
                            if (cacheName.indexOf(CACHE_FULL_NAME) == 0 && cacheName !== currentCacheName) {
                                console.log(`Deleting old cache '${cacheName}'.`);
                                caches.delete(cacheName)
                            }
                        }
                    }
                );
        },
    );

const getCurrentCacheName = (): Promise<string> => caches
    .keys()
    .then(
        (cacheNames: string[]): string => {
            const currentTimestamp: number = + new Date();
            let latestCacheTimestamp: number = null;

            for (const cacheName of cacheNames) {
                if (cacheName.indexOf(CACHE_FULL_NAME) == 0) {
                    const cacheOpened = parseInt(
                        cacheName.replace(`${CACHE_FULL_NAME}@`, ''),
                        10,
                    );

                    if (!latestCacheTimestamp || latestCacheTimestamp < cacheOpened ) {
                        latestCacheTimestamp = cacheOpened;
                    }
                }
            }

            return (
                `${CACHE_FULL_NAME}@` +
                `${currentTimestamp - latestCacheTimestamp < CACHE_EXPIRY ? latestCacheTimestamp : + new Date()}`
            )
        },
    );

const getCurrentCache = (): Promise<Cache> => getCurrentCacheName()
    .then((currentCache: string): Promise<Cache> => caches.open(currentCache));

const isInDontCache = (url: string): boolean => {
    for (const pattern of COMBINED_DONT_CACHE) {
        if (url.match(pattern)) return true;
    }
    return false;
};

const performFetchRequest = (request: Request): Promise<Response> => {
    const fetchRequestClone = request.clone();
    const cacheRequestClone = request.clone();

    return fetch(fetchRequestClone).then((response: Response) => {
        if (response && response.status === 200) {
            const cacheResponseClone = response.clone();
            getCurrentCache().then((cache: Cache): void => {
                if (!isInDontCache(request.url)) {
                    cache.put(cacheRequestClone, cacheResponseClone);
                }
            });
        }

        return response;
    });
};
