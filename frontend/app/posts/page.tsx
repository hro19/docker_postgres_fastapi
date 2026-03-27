"use client";

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
  type PaginationState,
} from "@tanstack/react-table";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

const apiBase =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

type Category = {
  id: number;
  name: string;
};

type PostRow = {
  id: number;
  title: string;
  content: string;
  thumbnail: string;
  created_at: string;
  edited_at: string;
  categories: Category[];
};

type PaginatedPosts = {
  items: PostRow[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
};

export default function PostsPage() {
  const [data, setData] = useState<PostRow[]>([]);
  const [rowCount, setRowCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      try {
        const page = pagination.pageIndex + 1;
        const perPage = pagination.pageSize;
        const res = await fetch(
          `${apiBase}/posts?page=${page}&perPage=${perPage}`,
        );
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        const json = (await res.json()) as PaginatedPosts;
        if (cancelled) {
          return;
        }
        setData(json.items);
        setRowCount(json.total);
      } catch {
        if (!cancelled) {
          setData([]);
          setRowCount(0);
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [pagination.pageIndex, pagination.pageSize]);

  const pageCount = Math.max(1, Math.ceil(rowCount / pagination.pageSize) || 1);

  const columns = useMemo<ColumnDef<PostRow>[]>(
    () => [
      { accessorKey: "id", header: "ID", size: 56 },
      { accessorKey: "title", header: "タイトル" },
      {
        accessorKey: "content",
        header: "本文",
        cell: ({ getValue }) => (
          <span
            className="block max-w-[20rem] truncate"
            title={String(getValue())}
          >
            {String(getValue())}
          </span>
        ),
      },
      {
        accessorKey: "thumbnail",
        header: "サムネイル",
        cell: ({ getValue }) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={String(getValue())}
            alt=""
            width={96}
            height={54}
            className="rounded object-cover"
          />
        ),
      },
      {
        id: "categories",
        header: "カテゴリー",
        accessorFn: (row) => row.categories.map((c) => c.name).join(", "),
      },
      {
        accessorKey: "created_at",
        header: "作成日時",
        cell: ({ getValue }) =>
          new Date(String(getValue())).toLocaleString("ja-JP"),
      },
      {
        accessorKey: "edited_at",
        header: "更新日時",
        cell: ({ getValue }) =>
          new Date(String(getValue())).toLocaleString("ja-JP"),
      },
    ],
    [],
  );

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    pageCount,
    rowCount,
    onPaginationChange: setPagination,
    state: { pagination },
  });

  return (
    <div className="mx-auto max-w-[1400px] bg-white px-4 py-8 text-neutral-900">
      <div className="mb-4 flex flex-wrap items-baseline gap-4">
        <h1 className="text-xl font-semibold">投稿一覧</h1>
        <Link href="/" className="text-sm text-blue-700 underline">
          トップへ
        </Link>
      </div>

      <div className="overflow-x-auto rounded border border-neutral-200">
        <table className="w-full border-collapse text-left text-sm">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="border-b border-neutral-200 bg-neutral-50">
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className="px-3 py-2 font-medium text-neutral-700"
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-3 py-8 text-center text-neutral-500"
                >
                  読み込み中…
                </td>
              </tr>
            ) : table.getRowModel().rows.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-3 py-8 text-center text-neutral-500"
                >
                  データがありません
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <tr
                  key={row.id}
                  className="border-b border-neutral-100 hover:bg-neutral-50/80"
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-3 py-2 align-middle">
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-sm">
        <p className="text-neutral-600">
          全 {rowCount} 件
          {rowCount > 0 && (
            <>
              {" "}
              （{pagination.pageIndex + 1} / {pageCount} ページ）
            </>
          )}
        </p>
        <div className="flex flex-wrap items-center gap-2">
          <label className="flex items-center gap-2">
            <span className="text-neutral-600">表示件数</span>
            <select
              className="rounded border border-neutral-300 bg-white px-2 py-1"
              value={pagination.pageSize}
              onChange={(e) => {
                const next = Number(e.target.value);
                table.setPageSize(next);
                table.setPageIndex(0);
              }}
            >
              {[5, 10, 25, 50].map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            className="rounded border border-neutral-300 px-2 py-1 disabled:opacity-40"
            onClick={() => table.setPageIndex(0)}
            disabled={!table.getCanPreviousPage()}
          >
            先頭
          </button>
          <button
            type="button"
            className="rounded border border-neutral-300 px-2 py-1 disabled:opacity-40"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            前へ
          </button>
          <button
            type="button"
            className="rounded border border-neutral-300 px-2 py-1 disabled:opacity-40"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            次へ
          </button>
          <button
            type="button"
            className="rounded border border-neutral-300 px-2 py-1 disabled:opacity-40"
            onClick={() => table.setPageIndex(table.getPageCount() - 1)}
            disabled={!table.getCanNextPage()}
          >
            末尾
          </button>
        </div>
      </div>
    </div>
  );
}
