const secretKey = "9fGDzagmHOCYEvjw";

export async function generateKey(): Promise<CryptoKey> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secretKey).slice(0, 16);
  return await crypto.subtle.importKey("raw", keyData, "AES-GCM", false, [
    "encrypt",
    "decrypt",
  ]);
}

export async function encrypt<T>(data: T, key: CryptoKey) {
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
    tag: Array.from(authTag),
  };
}

export async function decrypt(
  encryptedResponse: { iv: number[]; data: number[]; tag: number[] },
  secretKeyString: string
) {
  const { data, iv, tag } = encryptedResponse;

  const secretKeyBuffer = new TextEncoder().encode(secretKeyString);

  const cryptoKey = await crypto.subtle.importKey(
    "raw",
    secretKeyBuffer,
    { name: "AES-GCM" },
    false,
    ["decrypt"]
  );

  const encryptedDataWithTag = new Uint8Array([...data, ...tag]);
  const initializationVector = new Uint8Array(iv);

  try {
    const decrypted = await crypto.subtle.decrypt(
      {
        name: "AES-GCM",
        iv: initializationVector,
      },
      cryptoKey,
      encryptedDataWithTag
    );

    return JSON.parse(new TextDecoder().decode(decrypted));
  } catch (error) {
    console.error("Ошибка при расшифровке:", error);
    throw error;
  }
}
