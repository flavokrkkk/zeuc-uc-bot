import { asyncThunkCreator, buildCreateSlice } from "@reduxjs/toolkit";
import { ISocketState } from "./types";
import { rootReducer } from "@/shared/store";

const createSliceWithThunks = buildCreateSlice({
  creators: { asyncThunk: asyncThunkCreator },
});

export const initialState: ISocketState = {
  socket: null,
  isConnected: false,
  error: "",
};

export const socketSlice = createSliceWithThunks({
  name: "socketSlice",
  initialState,
  selectors: {
    isConnected: (state) => state.isConnected,
    socket: (state) => state.socket,
    error: (state) => state.error,
  },
  reducers: (create) => ({
    connectionSocket: create.asyncThunk<
      WebSocket,
      void,
      { rejectValue: string }
    >(
      async (_, { rejectWithValue }) => {
        try {
          const token = localStorage.getItem("token");
          const sockets = new WebSocket(
            `ws://localhost:8080/ws?token=${token}`
          );
          return sockets;
        } catch (err) {
          return rejectWithValue(`${err}`);
        }
      },
      {
        pending: (state) => {
          state.isConnected = false;
          state.error = "";
        },
        fulfilled: (state, { payload }) => ({
          ...state,
          socket: payload,
          isConnected: true,
        }),
        rejected: (state) => {
          state.error = "No connection";
          state.isConnected = false;
        },
      }
    ),
  }),
}).injectInto(rootReducer);

export const socketReducer = socketSlice.reducer;
export const socketActions = socketSlice.actions;
export const socketSelectors = socketSlice.selectors;
