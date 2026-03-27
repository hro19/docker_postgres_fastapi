"use client";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState, type DragEvent, type FormEvent } from "react";
import Select, { type MultiValue } from "react-select";

const apiBase =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

type Category = {
  id: number;
  name: string;
};

type CategoryOption = {
  value: number;
  label: string;
};

type CreatePostPayload = {
  title: string;
  content: string;
  thumbnail: string;
  category_ids: number[];
};

const toDataUrl = (file: File): Promise<string> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(new Error("failed to read file"));
    reader.readAsDataURL(file);
  });

export default function PostAddPage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategoryIds, setSelectedCategoryIds] = useState<number[]>([]);
  const [thumbnailDataUrl, setThumbnailDataUrl] = useState("");
  const [message, setMessage] = useState("必要項目を入力してください。");
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDragActive, setIsDragActive] = useState(false);

  const categoryOptions = useMemo<CategoryOption[]>(
    () => categories.map((c) => ({ value: c.id, label: c.name })),
    [categories],
  );

  const selectedCategoryOptions = useMemo(
    () => categoryOptions.filter((o) => selectedCategoryIds.includes(o.value)),
    [categoryOptions, selectedCategoryIds],
  );

  useEffect(() => {
    void (async () => {
      setIsLoadingCategories(true);
      try {
        const res = await fetch(`${apiBase}/posts/categories`);
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        const json = (await res.json()) as Category[];
        setCategories(json);
      } catch {
        setMessage("カテゴリ取得に失敗しました。API起動を確認してください。");
      } finally {
        setIsLoadingCategories(false);
      }
    })();
  }, []);

  async function setThumbnailFromFile(file: File): Promise<void> {
    if (!file.type.startsWith("image/")) {
      setMessage("画像ファイルを選択してください。");
      return;
    }
    const dataUrl = await toDataUrl(file);
    setThumbnailDataUrl(dataUrl);
    setMessage("画像を読み込みました。");
  }

  async function onDrop(e: DragEvent<HTMLDivElement>): Promise<void> {
    e.preventDefault();
    setIsDragActive(false);
    const file = e.dataTransfer.files?.[0];
    if (!file) return;
    await setThumbnailFromFile(file);
  }

  async function onSubmit(e: FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      setMessage("タイトル・本文は必須です。");
      return;
    }
    if (selectedCategoryIds.length === 0) {
      setMessage("カテゴリを1つ以上選択してください。");
      return;
    }

    setIsSubmitting(true);
    setMessage("投稿を作成中…");
    try {
      const payload: CreatePostPayload = {
        title: title.trim(),
        content: content.trim(),
        thumbnail: thumbnailDataUrl,
        category_ids: selectedCategoryIds,
      };
      const res = await fetch(`${apiBase}/posts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      setMessage("投稿を作成しました。");
      setTitle("");
      setContent("");
      setSelectedCategoryIds([]);
      setThumbnailDataUrl("");
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch {
      setMessage("投稿作成に失敗しました。");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl bg-white px-4 py-8 text-neutral-900">
      <div className="mb-5 flex flex-wrap items-center gap-4">
        <h1 className="text-2xl font-semibold">新規投稿</h1>
        <Link href="/posts" className="text-sm text-blue-700 underline">
          投稿一覧
        </Link>
      </div>

      <form onSubmit={onSubmit} className="space-y-4 rounded border border-neutral-200 p-5">
        <div className="space-y-2">
          <Label htmlFor="post-title">タイトル</Label>
          <Input
            id="post-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength={255}
            required
            placeholder="投稿のタイトル"
            autoComplete="off"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="post-content">本文</Label>
          <Textarea
            id="post-content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            placeholder="本文を入力"
          />
        </div>

        <div className="block">
          <span className="mb-1 block text-sm font-medium">カテゴリ（複数選択可）</span>
          <Select<CategoryOption, true>
            inputId="post-categories"
            instanceId="post-categories"
            isMulti
            isDisabled={isLoadingCategories}
            options={categoryOptions}
            value={selectedCategoryOptions}
            onChange={(next: MultiValue<CategoryOption>) => {
              setSelectedCategoryIds((next ?? []).map((o) => o.value));
            }}
            placeholder="カテゴリを選択…"
            classNamePrefix="rs"
            theme={(t) => ({
              ...t,
              borderRadius: 6,
              colors: {
                ...t.colors,
                primary25: "rgb(239 246 255)",
                primary: "rgb(29 78 216)",
              },
            })}
          />
        </div>

        <div>
          <p className="mb-1 text-sm font-medium">
            画像（任意・ドロップまたはクリック）
          </p>
          <div
            className={
              isDragActive
                ? "rounded border-2 border-dashed border-blue-500 bg-blue-50 p-5 text-center"
                : "rounded border-2 border-dashed border-neutral-300 bg-neutral-50 p-5 text-center"
            }
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragActive(true);
            }}
            onDragLeave={() => setIsDragActive(false)}
            onDrop={(e) => void onDrop(e)}
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                fileInputRef.current?.click();
              }
            }}
          >
            <p className="text-sm text-neutral-700">
              ここに画像ファイルをドロップ、またはクリックして選択
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (!file) return;
                void setThumbnailFromFile(file);
              }}
            />
          </div>
          {thumbnailDataUrl && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={thumbnailDataUrl}
              alt="アップロード画像プレビュー"
              className="mt-3 max-h-64 rounded border border-neutral-200 object-contain"
            />
          )}
        </div>

        <div className="flex items-center justify-between gap-4">
          <p className="text-sm text-neutral-600">{message}</p>
          <button
            type="submit"
            disabled={isSubmitting || isLoadingCategories}
            className="rounded bg-blue-700 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
          >
            {isSubmitting ? "送信中…" : "投稿を作成"}
          </button>
        </div>
      </form>
    </main>
  );
}
