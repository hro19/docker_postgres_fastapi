"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const apiBase =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export default function Home() {
  const [message, setMessage] = useState<string>("読み込み中…");

  useEffect(() => {
    fetch(`${apiBase}/`, { method: "GET" })
      .then((r) => r.json())
      .then((data) => setMessage(data?.message ?? "FastAPI is running"))
      .catch(() => setMessage("取得に失敗しました（API が起動しているか確認してください）"));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-white p-8 text-neutral-900">
      <p className="text-2xl font-semibold tracking-tight">{message}</p>
      <Link href="/posts" className="text-sm text-blue-700 underline">
        投稿一覧へ
      </Link>
    </main>
  );
}
