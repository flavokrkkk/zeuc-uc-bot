import {
  deleteAccessToken,
  getAccessToken,
} from "@/entities/token/libs/tokenService";
import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  AxiosError,
} from "axios";

import { RequestOptions } from "https";
import { decrypt, encrypt, generateKey } from "../helpers/cryptoHash";

export class AxiosClient {
  private baseQueryV1Instance: AxiosInstance;

  constructor(baseURL: string, withAuth = false) {
    const config: AxiosRequestConfig = {
      baseURL,
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
      },
    };

    this.baseQueryV1Instance = axios.create(config);

    if (withAuth) {
      this.addAuthInterceptor();
    }
  }

  private addAuthInterceptor() {
    let cryptoKey: CryptoKey | null = null;
    (async () => {
      cryptoKey = await generateKey();
    })();

    this.baseQueryV1Instance.interceptors.request.use(async (config) => {
      const token = getAccessToken();
      if (config && config.headers && token) {
        config.headers["Authorization"] = `Bearer ${token}`;
      } else {
        deleteAccessToken();
      }

      if (config.data && cryptoKey) {
        config.data = await encrypt(config.data, cryptoKey);
      }

      return config;
    });

    this.baseQueryV1Instance.interceptors.response.use(
      async (response) => {
        if (
          response.data &&
          response.data.data &&
          response.data.iv &&
          response.data.tag &&
          cryptoKey
        ) {
          const encryptedResponse = {
            iv: response.data.iv,
            data: response.data.data,
            tag: response.data.tag,
          };

          try {
            const decryptedData = await decrypt(
              encryptedResponse,
              "9fGDzagmHOCYEvjw"
            );
            response.data = decryptedData;
          } catch (error) {
            console.error("Ошибка при расшифровке:", error);
          }
        }
        return response;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }

  public getInstance() {
    return this.baseQueryV1Instance;
  }

  private handleResponse<T>(response: AxiosResponse<T>): AxiosResponse<T> {
    return response;
  }

  private handleError(error: AxiosError<{ message?: string }>): never {
    const message = error.response?.data?.message || error.message || "Error";
    throw new Error(message);
  }

  public async get<T>(
    url: string,
    params: Omit<RequestOptions, "body"> = {}
  ): Promise<AxiosResponse<T>> {
    try {
      const response = await this.baseQueryV1Instance.get<T>(url, { params });
      return this.handleResponse(response);
    } catch (error) {
      this.handleError(error as AxiosError<{ message?: string }>);
    }
  }

  public async post<T>(
    url: string,
    data?: Record<string, unknown>,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    try {
      const response = await this.baseQueryV1Instance.post<T>(
        url,
        data,
        config
      );
      return this.handleResponse(response);
    } catch (error) {
      this.handleError(error as AxiosError<{ message?: string }>);
    }
  }

  public async put<T>(
    url: string,
    data?: Record<string, unknown>,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    try {
      const response = await this.baseQueryV1Instance.put<T>(url, data, config);
      return this.handleResponse(response);
    } catch (error) {
      this.handleError(error as AxiosError<{ message?: string }>);
    }
  }

  public async patch<T>(
    url: string,
    data?: Record<string, unknown>,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    try {
      const response = await this.baseQueryV1Instance.patch<T>(
        url,
        data,
        config
      );
      return this.handleResponse(response);
    } catch (error) {
      this.handleError(error as AxiosError<{ message?: string }>);
    }
  }

  public async delete<T>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    try {
      const response = await this.baseQueryV1Instance.delete<T>(url, config);
      return this.handleResponse(response);
    } catch (error) {
      this.handleError(error as AxiosError<{ message?: string }>);
    }
  }
}

export const axiosNoAuth = new AxiosClient("http://http://81.177.221.219:8000/api/");
export const axiosAuth = new AxiosClient("http://http://81.177.221.219:8000/api/", true);
