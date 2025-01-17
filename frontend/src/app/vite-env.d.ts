/// <reference types="vite/client" />

import { Telegram } from "./shared/types/telegram";

declare global {
  interface Window {
    Telegram: Telegram;
  }
}

export {};
