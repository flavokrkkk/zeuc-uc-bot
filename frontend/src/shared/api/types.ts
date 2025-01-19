import { QueryMeta } from "@tanstack/react-query";

export interface IQueryMetadata {
  queryKey: string[];
  signal: AbortSignal;
  meta: QueryMeta | undefined;
  pageParam?: unknown;
  direction?: unknown;
}
