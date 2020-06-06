export const isClientSide = (): boolean => {
    return !!(typeof window !== 'undefined' && window.document && window.document.createElement);
};

export const isServerSide = (): boolean => !isClientSide();

export const renderSide = (): string => (isClientSide() ? 'client' : 'server');
