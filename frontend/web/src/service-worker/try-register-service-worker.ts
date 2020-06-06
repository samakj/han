export const tryRegisterServiceWorker = (): void => {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .register('/service-worker.bundle.js')
            .then((registration: ServiceWorkerRegistration): void =>
                console.log('Service worker registered: ', registration.scope),
            )
            .catch((error: Error): void =>
                console.log('Service worker registration failed:', error),
            );
    }
};
