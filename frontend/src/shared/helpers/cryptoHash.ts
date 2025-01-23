export async function generateKey(): Promise<CryptoKey> {
  return await crypto.subtle.generateKey(
    {
      name: "AES-GCM",
      length: 256,
    },
    true,
    ["encrypt", "decrypt"]
  );
}

export async function exportKey(key: CryptoKey): Promise<ArrayBuffer> {
  return await crypto.subtle.exportKey("raw", key);
}

(async () => {
  try {
    const key = await generateKey();
    const exportedKey = await exportKey(key);
    console.log("Экспортированный ключ:", new Uint8Array(exportedKey));
  } catch (error) {
    console.error("Ошибка при генерации или экспорте ключа:", error);
  }
})();

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
