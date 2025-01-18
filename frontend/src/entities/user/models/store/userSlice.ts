import { rootReducer } from "@/shared/store";
import { asyncThunkCreator, buildCreateSlice } from "@reduxjs/toolkit";
import { IUserState } from "./types";
import { TelegramUser } from "@/shared/types/telegram";
import { MutationObserver } from "@tanstack/react-query";
import { queryClient } from "@/shared/api/queryClient";
import { setUserCredentials } from "../../libs/userService";
import { setAccessToken } from "@/entities/token/libs/tokenService";

const createSliceWithThunks = buildCreateSlice({
  creators: { asyncThunk: asyncThunkCreator },
});

const initialState: IUserState = {
  user: null,
};

export const userSlice = createSliceWithThunks({
  name: "userSlice",
  initialState,
  selectors: {
    userInfo: (state) => state.user,
  },
  reducers: (create) => ({
    setUserCredentials: create.asyncThunk<
      TelegramUser,
      Partial<TelegramUser> & { id: number; username: string },
      { rejectValue: string }
    >(async (telegramUser, { rejectWithValue }) => {
      try {
        await new MutationObserver(queryClient, {
          mutationFn: setUserCredentials,
          mutationKey: ["telegram-user"],
          onSuccess: (data) => {
            if (data) {
              setAccessToken(data.access_token);
            }
          },
        }).mutate(telegramUser);
        return telegramUser;
      } catch (e) {
        return rejectWithValue(String(e));
      }
    }),
  }),
}).injectInto(rootReducer);

export const userActions = userSlice.actions;
export const userSelectors = userSlice.selectors;
