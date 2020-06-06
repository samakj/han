const SECOND = 1000;
const MINUTE = 60 * SECOND;
const HOUR = 60 * MINUTE;

export const CACHE_NAME = 'main';
export const CACHE_VERSION = 'v1';
export const CACHE_FULL_NAME = `${CACHE_NAME}_${CACHE_VERSION}`;
export const CACHE_EXPIRY = HOUR;
export const PRECACHE_FILES: string[] = [];
export const DONT_CACHE: string[] = [];
export const DEV_DONT_CACHE: string[] = [
    'http://localhost:8080/',
];
