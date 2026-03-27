/**
 * TanStack Table にページ番号 UI は無いため、0-based のインデックス列を組み立てる。
 * ページが多いときは両端・現在付近を残し、飛びがある箇所に ellipsis を挟む。
 */
export function buildVisiblePageIndices(
  currentIndex: number,
  totalPages: number,
): (number | "ellipsis")[] {
  if (totalPages <= 0) {
    return [];
  }
  if (totalPages <= 9) {
    return Array.from({ length: totalPages }, (_, i) => i);
  }

  const set = new Set<number>();
  set.add(0);
  set.add(totalPages - 1);
  for (let d = -2; d <= 2; d++) {
    const i = currentIndex + d;
    if (i > 0 && i < totalPages - 1) {
      set.add(i);
    }
  }

  const sorted = [...set].sort((a, b) => a - b);
  const out: (number | "ellipsis")[] = [];
  for (let k = 0; k < sorted.length; k++) {
    const cur = sorted[k]!;
    if (k > 0 && cur - sorted[k - 1]! > 1) {
      out.push("ellipsis");
    }
    out.push(cur);
  }
  return out;
}
