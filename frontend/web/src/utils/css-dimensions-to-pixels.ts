import { isServerSide } from '@han/utils/render-side';

export const cssDimensionToPixels = (value: string): number => {
    if (isServerSide()) {
        return null;
    }
    if (value.includes('rem')) {
        const pxPerRem = parseFloat(
            getComputedStyle(document.documentElement).fontSize.replace('px', ''),
        );
        return pxPerRem * parseFloat(value.replace('rem', ''));
    }
    if (value.includes('px')) {
        return parseFloat(value.replace('px', ''));
    }

    return parseFloat(value);
};
