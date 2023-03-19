/**
 * @return {number}
 */
export function GausSquare(points, square) {
    let s = 0;
    let k = points.length - 2;
    if (points[0] !== points[k] || points[1] !== points[k + 1]) {
        return -1;
    }
    for (let i = 0; i < k; i++) {
        if (i % 2 === 0) {
            s += (points[i] * points[i + 3]);
        } else {
            s -= (points[i] * points[i + 1]);
        }
    }
    return Math.round(Math.abs(s) * square * 50) / 100;
}
