import { rootReducer } from "@/shared/store";
import {
  asyncThunkCreator,
  buildCreateSlice,
  PayloadAction,
} from "@reduxjs/toolkit";
import { IUserState } from "./types";
import { TelegramUser } from "@/shared/types/telegram";
import { MutationObserver } from "@tanstack/react-query";
import { queryClient } from "@/shared/api/queryClient";
import {
  getCurrentUser,
  getUserDiscount,
  setUserCredentials,
} from "../../libs/userService";
import { setAccessToken } from "@/entities/token/libs/tokenService";
import {
  ICurrentUserResponse,
  IUserDiscount,
  IUserResponse,
} from "../../types/types";
import { decrypt } from "@/shared/helpers/cryptoHash";

const createSliceWithThunks = buildCreateSlice({
  creators: { asyncThunk: asyncThunkCreator },
});

const initialState: IUserState = {
  user: null,
  currentUser: null,
  userDiscount: [],
  userPaymentHistory: [],
  userBonusesHistory: [],
};

export const userSlice = createSliceWithThunks({
  name: "userSlice",
  initialState,
  selectors: {
    userInfo: (state) => state.user,
    userDiscount: (state) => state.userDiscount,
    currentUser: (state) => state.currentUser,
    userPaymentHistory: (state) => state.userPaymentHistory,
    userBonusesHistory: (state) => state.userBonusesHistory,
  },
  reducers: (create) => ({
    setPointsUser: create.reducer(
      (state, { payload }: PayloadAction<number>) => {
        if (state.currentUser) {
          state.currentUser.bonuses = state.currentUser.bonuses + payload;
        }
      }
    ),
    setUserCredentials: create.asyncThunk<
      TelegramUser,
      Partial<TelegramUser> & { id: number; username: string },
      { rejectValue: string }
    >(
      async (telegramUser, { rejectWithValue }) => {
        try {
          await new MutationObserver(queryClient, {
            mutationFn: setUserCredentials,
            mutationKey: ["telegram-user"],
            onSuccess: async (data) => {
              if (data) {
                const response: { iv: []; data: []; tag: [] } = data;
                const decryptedData: IUserResponse = await decrypt(
                  response,
                  "9fGDzagmHOCYEvjw"
                );
                setAccessToken(decryptedData.access_token);
              }
            },
          }).mutate(telegramUser);
          return telegramUser;
        } catch (e) {
          return rejectWithValue(String(e));
        }
      },
      {
        fulfilled: (state, { payload }) => {
          state.user = payload;
        },
      }
    ),
    getAsyncCurrentUser: create.asyncThunk<
      ICurrentUserResponse,
      void,
      { rejectValue: string }
    >(
      async (_, { rejectWithValue }) => {
        try {
          const response = await getCurrentUser();
          return response;
        } catch (e) {
          return rejectWithValue(String(e));
        }
      },
      {
        fulfilled: (state, { payload }) => {
          state.currentUser = payload;
        },
      }
    ),
    getAsyncDiscount: create.asyncThunk<
      Array<IUserDiscount>,
      void,
      { rejectValue: string }
    >(
      async (_, { rejectWithValue }) => {
        try {
          const response = await getUserDiscount();
          return response;
        } catch (e) {
          return rejectWithValue(String(e));
        }
      },
      {
        fulfilled: (state, { payload }) => {
          state.userDiscount = payload;
        },
      }
    ),
    setPaymentHistory: create.reducer(
      (state, { payload }: PayloadAction<IUserState["userPaymentHistory"]>) => {
        state.userPaymentHistory = payload.map((payload) => ({
          ...payload,
          id: crypto.randomUUID(),
        }));
      }
    ),
    setBonusesHistory: create.reducer(
      (state, { payload }: PayloadAction<IUserState["userBonusesHistory"]>) => {
        state.userBonusesHistory = payload.map((payload) => ({
          ...payload,
          id: crypto.randomUUID(),
        }));
      }
    ),
    setCurrentUser: create.reducer(
      (state, { payload }: PayloadAction<ICurrentUserResponse>) => {
        state.currentUser = payload;
      }
    ),
  }),
}).injectInto(rootReducer);

export const userActions = userSlice.actions;
export const userSelectors = userSlice.selectors;
