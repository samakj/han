export interface ExtendableEvent extends Event {
    waitUntil: (callback: Promise<void>) => void;
}

export interface FetchEvent extends ExtendableEvent {
    request: Request;

    respondWith: (response: Promise<Response>) => void;
}
