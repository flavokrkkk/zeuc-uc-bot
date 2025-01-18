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
}

export const { deleteAccessToken, getAccessToken, setAccessToken } =
  new TokenService();
