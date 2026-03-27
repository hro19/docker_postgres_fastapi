"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const apiBase =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

type SunTimesResponse = {
  today_sunset: string;
  tomorrow_sunrise: string;
};

const formatJstTime = (isoText: string): string =>
  new Intl.DateTimeFormat("ja-JP", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: "Asia/Tokyo",
  }).format(new Date(isoText));

export default function Home() {
  const [message, setMessage] = useState<string>("読み込み中…");
  const [todaySunset, setTodaySunset] = useState<string>("読み込み中…");
  const [tomorrowSunrise, setTomorrowSunrise] = useState<string>("読み込み中…");

  useEffect(() => {
    fetch(`${apiBase}/`, { method: "GET" })
      .then((r) => r.json())
      .then((data) => setMessage(data?.message ?? "FastAPI is running"))
      .catch(() => setMessage("取得に失敗しました（API が起動しているか確認してください）"));

    fetch(`${apiBase}/chiba/sun-times`, { method: "GET" })
      .then((r) => {
        if (!r.ok) {
          throw new Error("failed to fetch sun times");
        }
        return r.json() as Promise<SunTimesResponse>;
      })
      .then((data) => {
        setTodaySunset(formatJstTime(data.today_sunset));
        setTomorrowSunrise(formatJstTime(data.tomorrow_sunrise));
      })
      .catch(() => {
        setTodaySunset("取得に失敗しました");
        setTomorrowSunrise("取得に失敗しました");
      });
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-white p-8 text-neutral-900">
      <section className="grid w-full max-w-2xl gap-4 sm:grid-cols-2">
        <article className="rounded-xl border border-neutral-200 bg-neutral-50 p-6 shadow-sm">
          <p className="text-sm text-neutral-600">千葉の本日の日没</p>
          <p className="mt-2 text-3xl font-bold tracking-tight">{todaySunset}</p>
        </article>
        <article className="rounded-xl border border-neutral-200 bg-neutral-50 p-6 shadow-sm">
          <p className="text-sm text-neutral-600">千葉の明日の夜明け</p>
          <p className="mt-2 text-3xl font-bold tracking-tight">{tomorrowSunrise}</p>
        </article>
      </section>
      <p className="text-2xl font-semibold tracking-tight">{message}</p>
      <div className="flex items-center gap-4">
        <Link href="/posts" className="text-sm text-blue-700 underline">
          投稿一覧へ
        </Link>
        <Link href="/posts/add" className="text-sm text-blue-700 underline">
          新規投稿へ
        </Link>
      </div>
    </main>
  );
}
