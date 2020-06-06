export const uniformRandomNo = (mean: number, deviation: number): number =>
    (Math.random() - 0.5) * deviation + mean;

export const randomChoice = (iterable: any[]): any =>
    iterable && iterable.length ? iterable[Math.floor(Math.random() * iterable.length)] : null;
