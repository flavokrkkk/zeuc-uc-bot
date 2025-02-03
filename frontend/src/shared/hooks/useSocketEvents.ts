import { useEffect } from "react";
import { useAppSelector } from "./useAppSelector";
import { socketSelectors } from "@/entities/socket/models/store/socketSlice";

export const useWebSocketEvents = <T>(
  eventType: string,
  callback: (data: T) => void
) => {
  const socket = useAppSelector(socketSelectors.socket);

  useEffect(() => {
    if (!socket) return;

    socket.onmessage = (event: MessageEvent) => {
      try {
        const parsedData = JSON.parse(event.data);
        console.log(parsedData);
        if (parsedData.event === eventType) {
          callback(parsedData);
        }
      } catch (error) {
        console.error("Ошибка при парсинге сообщения:", error);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket соединение закрыто");
    };

    socket.onerror = (error: unknown) => {
      console.error("WebSocket ошибка:", error);
    };

    return () => {
      if (socket) {
        socket.onmessage = null;
      }
    };
  }, [socket, eventType, callback]);
};
