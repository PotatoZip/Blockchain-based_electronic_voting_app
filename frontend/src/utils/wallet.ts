import { Wallet } from "ethers";

// Key used to store the encrypted keystore JSON in localStorage
const KEYSTORE_KEY = "evote_keystore";
let memoryPasswordCache: string | null = null;

/**
 * By default we cache the password in memory only (cleared when the page reloads)
 * This avoids prompting the user repeatedly during the current page session while ensuring
 * the password is never stored in any browser storage
 */
async function defaultPasswordGetter(): Promise<string> {
  if (memoryPasswordCache) return memoryPasswordCache;
  const p = prompt("Enter wallet password:");
  if (!p) throw new Error("Password is required");
  memoryPasswordCache = p;
  return p;
}

/**
 * Ensure that a wallet exists, generating a new one if necessary
 */
export async function ensureWallet(
  passwordGetter?: () => Promise<string>
): Promise<Wallet> {
  // Check if we have an existing keystore
  const pwGetter = passwordGetter ?? defaultPasswordGetter;
  const existing = localStorage.getItem(KEYSTORE_KEY);
  if (existing) {
    const pass = await pwGetter();
    try {
      const w = (await Wallet.fromEncryptedJson(
        existing,
        pass
      )) as unknown as Wallet;
      return w;
    } catch (error) {
      memoryPasswordCache = null;
      throw new Error("You entered wrong wallet password");
    }
  }
  // If wallet does not exist – generate
  const wallet = Wallet.createRandom() as unknown as Wallet;
  const pass = await pwGetter();
  const json = await wallet.encrypt(pass);
  localStorage.setItem(KEYSTORE_KEY, json);
  return wallet;
}

export async function getAddress(
  passwordGetter?: () => Promise<string>
): Promise<string> {
  const w = await ensureWallet(passwordGetter);
  return w.address;
}

/**
 * Encrypt and sign a message with the wallet's private key
 */
export async function signMessage(
  message: string,
  passwordGetter?: () => Promise<string>
): Promise<{ signature: string; address: string }> {
  const wallet = await ensureWallet(passwordGetter);
  const sig = await wallet.signMessage(message);
  return { signature: sig, address: wallet.address };
}

/**
 * Clear cached memory password (keeps keystore JSON in localStorage)
 * Use when user explicitly logs out of the session but wants to keep the keystore.
 */
export function clearWalletSession(): void {
  memoryPasswordCache = null;
}

export function clearWallet(): void {
  memoryPasswordCache = null;
  try {
    localStorage.removeItem(KEYSTORE_KEY);
  } catch (e) {}
}

export async function resetWalletForNewElection(): Promise<void> {
  clearWallet();
  await ensureWallet();
}
