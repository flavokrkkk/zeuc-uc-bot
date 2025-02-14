class TokenService {
  public setAccessToken(accessToken: string) {
    localStorage.setItem("accessToken", accessToken);
  }

  public deleteAccessToken() {
    localStorage.removeItem("accessToken");
  }

  public getAccessToken() {
    return localStorage.getItem("accessToken");
  }

  public getStateCloseShop() {
    return localStorage.getItem("state_shop");
  }

  public setStateCloseShop(value: boolean) {
    return localStorage.setItem("state_shop", String(value));
  }
}

export const {
  deleteAccessToken,
  getAccessToken,
  setAccessToken,
  setStateCloseShop,
  getStateCloseShop,
} = new TokenService();
