export interface ISocketState {
  socket: WebSocket | null;
  isConnected: boolean;
  error: string;
}
