const secretKey = "yourSharedSecretKey";

export async function generateKey(): Promise<CryptoKey> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secretKey).slice(0, 16);
  return await crypto.subtle.importKey("raw", keyData, "AES-GCM", false, [
    "encrypt",
    "decrypt",
  ]);
}
export async function encrypt<T>(data: T, key: CryptoKey) {
  console.log(key)
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encodedData = new TextEncoder().encode(JSON.stringify(data));
  const encrypted = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    encodedData
  );
  const tagLength = 16;
  const encryptedData = new Uint8Array(encrypted);
  const ciphertext = encryptedData.slice(0, -tagLength);
  const authTag = encryptedData.slice(-tagLength);
  
  return {
    iv: Array.from(iv),
    data: Array.from(ciphertext),
    tag: Array.from(authTag)
  };
}

export async function decrypt(
  encryptedResponse: Record<string, ArrayBuffer>,
  key: CryptoKey
) {
  const { data, iv } = encryptedResponse;
  const decrypted = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: new Uint8Array(iv) },
    key,
    new Uint8Array(data)
  );
  return JSON.parse(new TextDecoder().decode(decrypted));
}
