import { parseISO } from "date-fns";
import { formatInTimeZone } from "date-fns-tz";

/** API の ISO 日時を日本時間（Asia/Tokyo）で表示用に整形する */
export function formatDateTimeJst(isoString: string): string {
  const d = parseISO(isoString);
  return formatInTimeZone(d, "Asia/Tokyo", "yyyy/M/d HH:mm:ss");
}
